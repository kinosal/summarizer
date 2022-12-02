"""OpenAI API connector."""

# Import from standard library
import os
import logging

# Import from 3rd party libraries
import openai
import streamlit as st

# Assign credentials from environment variable or streamlit secrets dict
openai.api_key = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]

# Suppress openai request/response logging
# Handle by manually changing the respective APIRequestor methods in the openai package
# Does not work hosted on Streamlit since all packages are re-installed by Poetry
# Alternatively (affects all messages from this logger):
logging.getLogger("openai").setLevel(logging.WARNING)


class Openai:
    """OpenAI Connector."""

    @staticmethod
    def call(prompt: str) -> str:
        """Call OpenAI GPT with text prompt.
        Args:
            prompt: text prompt
        Return: predicted response text
        """
        kwargs = {
            "engine": "text-davinci-003",
            "prompt": prompt,
            "temperature": 0.8,
            "max_tokens": 50,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }
        try:
            response = openai.Completion.create(**kwargs)
            return response["choices"][0]["text"]

        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            st.error(f"OpenAI API error: {e}")
            return ""

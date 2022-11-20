"""OpenAI API connector."""

# Import from 3rd party libraries
import openai


class Openai:
    """OpenAI Connector."""

    def __init__(self, api_key) -> None:
        openai.api_key = api_key

    @staticmethod
    def call(prompt: str) -> str:
        """Call OpenAI GPT with text prompt.
        Args:
            prompt: text prompt
        Return: predicted response text
        """
        kwargs = {
            "engine": "text-davinci-002",
            "prompt": prompt,
            "temperature": 0.8,
            "max_tokens": 50,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }
        response = openai.Completion.create(**kwargs)
        return response["choices"][0]["text"]

"""Streamlit app to summarize text, e.g. blog articles"""

# Import from standard library
import os

# Import from 3rd party libraries
import streamlit as st
import streamlit.components.v1 as components

# Import modules
import scrape as scr
import summarize as sum

# Assign OpenAI API key from environment variable or streamlit secrets dict
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]

# Initialize OpenAi connector
openai = sum.Openai(OPENAI_API_KEY)

# Render streamlit page
st.set_page_config(page_title="Summarizer", page_icon="🤖")

st.title("Summarize web content")
st.write(
    """This mini-app scrapes the paragraphs from a web page,
    e.g. a blog post, and summarizes them into a Tweet-sized
    statement using OpenAI's GPT-3 based Davinci model."""
)
st.markdown(
    "You can find the code on [GitHub](https://github.com/kinosal/summarizer)."
)

selectbox = st.selectbox("Raw text or URL source", ("URL", "Raw text"))

summary_prompt = (
    "\n\nSummarize the main points from the above article in less than 120 characters:\n"
)
# summary_prompt = "\n\nTl;dr\n"


if selectbox == "Raw text":
    raw_text = st.text_area(label="Text", height=300, max_chars=6000)
    if raw_text:
        raw_summary = openai.call(prompt=raw_text + summary_prompt)
        st.text_area(
            label="Raw text summary",
            value=raw_summary.strip().replace("\n", " "),
            height=100,
        )

elif selectbox == "URL":
    url = st.text_input(label="URL")
    if url:
        scraper = scr.Scraper()
        response = scraper.request_url(url)
        print(response)
        if "invalid" in str(response).lower():
            st.error(str(response))
        elif response.status_code != 200:
            st.error(f"Response status {response.status_code}")
        else:
            url_text = scraper.extract_content(response)[:6000]
            url_summary = (
                openai.call(prompt=url_text + summary_prompt).strip().replace("\n", " ")
            )
            st.text_area(label="URL summary", value=url_summary, height=100)
            print(url_text)
            print(url_summary)
            components.html(
                f"""
                    <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-size="large" data-text="{url_summary}\n- AI generated summary via web-summarizer.streamlit.app of" data-url="{url}" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                """
            )

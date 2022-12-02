"""Streamlit app to summarize text, e.g. blog articles"""

# Import from standard library
import logging

# Import from 3rd party libraries
import streamlit as st
import streamlit.components.v1 as components

# Import modules
import scrape as scr
import summarize as sum

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)


# Define functions
def summarize(text: str) -> str:
    """Summarize text."""
    summary_prompt = (
        "\n\nSummarize the main points from the above article in less than 120 characters:\n\n"
    )
    openai = sum.Openai()
    return openai.call(prompt=text + summary_prompt).strip().replace("\n", " ")


# Render streamlit page
st.set_page_config(page_title="Summarizer", page_icon="🤖")

st.title("Summarize web content")
st.markdown(
    """This mini-app scrapes the paragraphs from a web page,
    e.g. a blog post, and summarizes them into a Tweet-sized
    statement using OpenAI's GPT-3 based [Davinci model](https://beta.openai.com/docs/models/overview). You can find the code on [GitHub](https://github.com/kinosal/summarizer) and the author on [Twitter](https://twitter.com/kinosal)."""
)

selectbox = st.selectbox("Raw text or URL source", ("URL", "Raw text"))

if selectbox == "Raw text":
    raw_text = st.text_area(label="Text", height=300, max_chars=6000)
    if raw_text:
        raw_summary = summarize(raw_text)
        st.text_area(
            label="Raw text summary",
            value=raw_summary,
            height=100,
        )
        logging.info(f"Text: {raw_text}\nSummary: {raw_summary}")

elif selectbox == "URL":
    url = st.text_input(label="URL")
    if url:
        scraper = scr.Scraper()
        response = scraper.request_url(url)
        if "invalid" in str(response).lower():
            st.error(str(response))
        elif response.status_code != 200:
            st.error(f"Response status {response.status_code}")
        else:
            url_text = scraper.extract_content(response)[:6000].strip().replace("\n", " ")
            url_summary = summarize(url_text)
            st.text_area(label="URL summary", value=url_summary, height=100)
            logging.info(f"URL: {url}\nSummary: {url_summary}")
            components.html(
                f"""
                    <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-size="large" data-text="{url_summary}\n- Summary generated via web-summarizer.streamlit.app of" data-url="{url}" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                """,
                height=45,
            )

st.markdown("""---""")
st.markdown("**Other Streamlit apps by [@kinosal](https://twitter.com/kinosal)**")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("[Tweet Generator](https://tweets.streamlit.app)")
with col2:
    st.markdown("[Code Translator](https://english-to-code.streamlit.app)")
with col3:
    st.markdown("[PDF Analyzer](https://pdf-keywords.streamlit.app)")

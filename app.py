"""Streamlit app to summarize text, e.g. blog articles"""

# Import from standard library
import logging

# Import from 3rd party libraries
import streamlit as st
import streamlit.components.v1 as components

# Import modules
import scrape as scr
import oai

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)


# Define functions
def summarize(text: str):
    """Summarize text."""
    summary_prompt = "\n\nSummarize the main points from the above article in less than 120 characters:\n\n"
    openai = oai.Openai()
    flagged = openai.moderate(text)
    if flagged:
        st.session_state.error = "Input flagged as inappropriate."
        return
    st.session_state.error = ""
    st.session_state.summary = (
        openai.complete(prompt=text + summary_prompt).strip().replace("\n", " ")
    )


# Render streamlit page
st.set_page_config(page_title="Summarizer", page_icon="🤖")
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "error" not in st.session_state:
    st.session_state.error = ""

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
        summarize(raw_text)
        if st.session_state.summary:
            st.text_area(
                label="Raw text summary",
                value=st.session_state.summary,
                height=100,
            )
            logging.info(f"Text: {raw_text}\nSummary: {st.session_state.summary}")
            st.button(
                label="Regenerate summary",
                type="secondary",
                on_click=summarize,
                args=[raw_text],
            )

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
            url_text = (
                scraper.extract_content(response)[:6000].strip().replace("\n", " ")
            )
            summarize(url_text)
            if st.session_state.summary:
                st.text_area(
                    label="URL summary", value=st.session_state.summary, height=100
                )
                logging.info(f"URL: {url}\nSummary: {st.session_state.summary}")
                # Force responsive layout for columns also on mobile
                st.write(
                    """<style>
                    [data-testid="column"] {
                        width: calc(50% - 1rem);
                        flex: 1 1 calc(50% - 1rem);
                        min-width: calc(50% - 1rem);
                    }
                    </style>""",
                    unsafe_allow_html=True,
                )
                col1, col2 = st.columns(2)
                with col1:
                    components.html(
                        f"""
                            <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-size="large" data-text="{st.session_state.summary}\n- Summary generated via web-summarizer.streamlit.app of" data-url="{url}" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                        """,
                        height=45,
                    )
                with col2:
                    st.button(
                        label="Regenerate summary",
                        type="secondary",
                        on_click=summarize,
                        args=[url_text],
                    )

if st.session_state.error:
    st.error(st.session_state.error)

if st.session_state.summary:
    st.markdown("""---""")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "**Other Streamlit apps by [@kinosal](https://twitter.com/kinosal)**"
        )
        st.markdown("[Tweet Generator](https://tweets.streamlit.app)")
        st.markdown("[Twitter Wrapped](https://twitter-likes.streamlit.app)")
        st.markdown("[Code Translator](https://english-to-code.streamlit.app)")
        st.markdown("[PDF Analyzer](https://pdf-keywords.streamlit.app)")
    with col2:
        st.write("If you like this app, please consider to")
        components.html(
            """
                <form action="https://www.paypal.com/donate" method="post" target="_top">
                <input type="hidden" name="hosted_button_id" value="8JJTGY95URQCQ" />
                <input type="image" src="https://pics.paypal.com/00/s/MDY0MzZhODAtNGI0MC00ZmU5LWI3ODYtZTY5YTcxOTNlMjRm/file.PNG" height="35" border="0" name="submit" title="Donate with PayPal" alt="Donate with PayPal button" />
                <img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1" />
                </form>
            """,
            height=45,
        )
        st.write("so I can keep it alive. Thank you!")

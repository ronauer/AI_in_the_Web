import streamlit as st

st.header("Page 1")

st.markdown("""

This is the text for page 1.

## Use markdown in Streamlit.

Just use `markdown`syntax for longer texts.
""")

if st.button("Go to page 2"):
    st.switch_page("08-page2.py")

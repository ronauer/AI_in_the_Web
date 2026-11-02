import streamlit as st

page1 = st.Page("08-page1.py", title="The first page", icon="🤔")
page2 = st.Page("08-page2.py", title="The second page", icon="📈")

pg = st.navigation(pages=[page1, page2])
pg.run()

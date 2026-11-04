import streamlit as st

page1 = st.Page("t1_page1.py", title="Game", icon="🤔")
page2 = st.Page("t1_page2.py", title="Stats", icon="⚙️")

pg = st.navigation(pages=[page1, page2])
pg.run()

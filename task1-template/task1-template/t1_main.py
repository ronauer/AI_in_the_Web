import streamlit as st


if "is_played" not in st.session_state:  
    st.session_state["is_played"] = False

# generates all the pages and runs the navigation bar
page1 = st.Page("t1_page1.py", title="Game", icon="🤔")
page2 = st.Page("t1_page2.py", title="Stats", icon="⚙️")

pg = st.navigation(pages=[page1, page2])
pg.run()

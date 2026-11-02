import streamlit as st

st.header("Hello, world!")
st.subheader("This is the subheader")
st.write("This a normal text paragraph.")

st.logo("ikwlogo.png")

rating = st.slider("Rating:", 0, 10)
if rating:
    st.subheader("Rating")
    st.write(f"Rating is {rating}")

# st.balloons()
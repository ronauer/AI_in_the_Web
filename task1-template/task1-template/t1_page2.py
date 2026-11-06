
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sn

#st.header("Statistics")


#hist_values = np.histogram(st.session_state["guessing_stats"],st.session_state["number_of_games"])
#st.bar_chart(hist_values)

st.header("Statistics")

if st.session_state["is_played"] == True:
    stats_df = pd.DataFrame({
        "Game": st.session_state["number_list"] ,
        "Number of Guesses": st.session_state["guessing_list"]
        })


    st.bar_chart(
        stats_df,
        x="Game",
        y="Number of Guesses", 
        x_label="Number of Games",
        y_label="Number of Guesses"
    )
    st.subheader("average guess:")
    st.write(stats_df.agg("mean"))
else:
    st.write("You have to play games to see the statistics!")


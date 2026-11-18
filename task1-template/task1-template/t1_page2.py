
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sn

#st.header("Statistics")


#hist_values = np.histogram(st.session_state["guessing_stats"],st.session_state["number_of_games"])
#st.bar_chart(hist_values)

st.header("Statistics")
# fetching game statistics
if st.session_state["is_played"] == True:
    stats_df = pd.DataFrame({
        "Number of Guesses": st.session_state["guessing_list"]
        }, index = st.session_state["number_list"])

    # initializing chart
    st.bar_chart(
        stats_df, 
        x_label="Game number",
        y_label="Number of Guesses"
    )

    st.subheader("Summary")
    # calculating statistics summary
    total_games = len(stats_df)
    avg_guesses = stats_df["Number of Guesses"].mean()

    summary_df = pd.DataFrame({
        "Total Games": [total_games],
        "Average Guesses": [avg_guesses]
    })
    # initializing chart without unnecesarry column
    st.dataframe(summary_df, hide_index=True)


    # Amount of hints used per game
    st.subheader("Amount of hints used per game")
    hints_df = pd.DataFrame({
        "Number of Hints": st.session_state["prompt_list"]
        }, index = st.session_state["number_list"])

    # initializing chart
    st.bar_chart(
        hints_df, 
        x_label="Game number",
        y_label="Number of Hints"
    )

else:
    st.write("You have to play games to see the statistics!")


import streamlit as st
import pandas as pd
import numpy as np
# import seaborn as sn
import matplotlib.pyplot as plt

#st.header("Statistics")


#hist_values = np.histogram(st.session_state["guessing_stats"],st.session_state["number_of_games"])
#st.bar_chart(hist_values)

st.header("Statistics")
# fetching game statistics
if st.session_state["is_played"] == True:

    st.markdown("### Number of guesses per game")
    stats_df = pd.DataFrame({
        "Number of Guesses": [guesses - 1 for guesses in st.session_state["guessing_list"]] # number of guesses bezieht nicht den richtigen guess ein
        }, index=st.session_state["number_list"])

    # initializing chart
    st.bar_chart(
        stats_df, 
        x_label="Game number",
        y_label="Number of Guesses"
    )

    st.markdown("#### Average Guesses")
    # calculating statistics summary
    total_games = len(stats_df)
    avg_guesses = stats_df["Number of Guesses"].mean()  


    summary_df = pd.DataFrame({
        "Total Games": [total_games],
        "Average Guesses": [avg_guesses]
    })
    # initializing chart without unnecesarry column
    st.dataframe(summary_df, hide_index=True)


    st.markdown("#### Resignations")
    gave_up = 0
    win = 0
    for i in range(len(st.session_state["gave_up_list"])):
        if st.session_state["gave_up_list"][i] == True:
            gave_up += 1
        else:
            win += 1

    st.write(f"You have won {win} game(s) and resigned or lost {gave_up} time(s).")        
                

    
    st.markdown("### Number of hints per game")

    hints_df = pd.DataFrame({
            "Number of Hints": st.session_state["prompt_list"]
            }, index = st.session_state["number_list"])

    
    # initializing chart
    st.bar_chart(
        hints_df, 
        x_label="Game number",
        y_label="Number of Hints"
    )


    # points

    st.markdown("### Points per game")
    st.markdown("The maximum amount of points is 200. Each guess costs 10 points and each hint costs 15 points.")
    points_df = pd.DataFrame({
            "Points": [
                max(0, 200 - (10 * (st.session_state["guessing_list"][i] - 1) + 15 * st.session_state["prompt_list"][i]))
                for i in range(st.session_state["number_of_games"])
                ]
            }, index = st.session_state["number_list"])
    
    
    # initializing chart
    st.bar_chart(
        points_df, 
        x_label="Game number",
        y_label="Points",
        # width=200,
        # height=400
    )

    #Quality of guesses
    
    st.markdown("### Quality of guesses per game")
    st.markdown("The quality of guesses is calculated by comparing the similarity between the guessed word and the correct word. A higher percentage indicates a closer match.")

    quality_df = pd.DataFrame(
        {"Quality": st.session_state["guess_qualities"]},
    index= range (1, len(st.session_state["guess_qualities"]) + 1))
    # initializing chart
    st.bar_chart(
        quality_df, 
        x_label="Game number",
        y_label="Quality of Guesses"
    )
    
else:
    st.write("You have to play games to see the statistics!")


import streamlit as st
import pandas as pd

st.header("Statistics")
st.markdown(
    "This page shows the statistics of your games. "
    "You can see how many guesses you needed per game, how many hints you used, "
    "how many points you earned and the quality of your guesses."
)

# if the user has played at least one game, the statistics are shown, otherwise a message is displayed
if st.session_state["is_played"]:  

    # number of guesses per game
    st.markdown("### Number of guesses per game")

    # creating a dataframe with the number of guesses per game and the game number
    stats_df = pd.DataFrame(
        {
            "Number of Guesses": [
                guesses - 1 for guesses in st.session_state["guessing_list"]
            ] 
        }, 
        index=st.session_state["number_list"],
    )

    # initializing chart
    st.bar_chart(
        stats_df, 
        x_label="Game number",
        y_label="Number of Guesses"
    )

    # statistic of average guesses
    st.markdown("#### Average Guesses")
    # calculating statistics summary for summary_df
    total_games = len(stats_df)
    avg_guesses = stats_df["Number of Guesses"].mean()  

    summary_df = pd.DataFrame(
        {
            "Total Games": [total_games],
            "Average Guesses": [avg_guesses],
        }
    )
    # initializing chart without unnecesarry column
    st.dataframe(summary_df, hide_index=True)

    # gave up and win statistics
    st.markdown("#### Resignations")

    # creating variables to count the number of games the user gave up and won
    gave_up = 0
    win = 0
    for i in range(len(st.session_state["gave_up_list"])):
        if st.session_state["gave_up_list"][i]:
            gave_up += 1
        else:
            win += 1

    # output of wins and losses
    st.write(
        f"You have won {win} game(s) and resigned or lost {gave_up} time(s)."
    )                 

    # statistics of number of hints per game
    st.markdown("### Number of hints per game (AI)")

    # creating data
    hints_df = pd.DataFrame(
        {"Number of Hints": st.session_state["prompt_list"]},
        index=st.session_state["number_list"],
    )
 
    # initializing chart
    st.bar_chart(
        hints_df, 
        x_label="Game number",
        y_label="Number of Hints",
    )

    # statistics of points
    st.markdown("### Points per game")
    st.markdown(
        "The maximum amount of points is 200. "
        "Each guess costs 10 points and each hint costs 15 points."
    )

    # creating data
    points_df = pd.DataFrame(
        {
            "Points": [
                0
                if st.session_state["gave_up_list"][i]
                else max(
                    0,
                    200 - (
                        10 * (st.session_state["guessing_list"][i] - 1) 
                        + 15 * st.session_state["prompt_list"][i]
                    ),
                )   # calculation of points, must be positive
                for i in range(st.session_state["number_of_games"])
            ]
        }, index=st.session_state["number_list"],
    )

    # calculating total points and output
    sum_points = points_df["Points"].sum() 
    st.markdown(f"Total points: {sum_points}")
    
    # initializing chart
    st.bar_chart(
        points_df, 
        x_label="Game number",
        y_label="Points",
    )

    # statistics of quality of guesses
    st.markdown("### Quality of guesses of the last game")
    st.markdown(
        "The quality of guesses is calculated by comparing the similarity " 
        "between the guessed word and the correct word. "
        "A higher percentage indicates a closer match."
    )

    # creating data
    quality_df = pd.DataFrame(
        {"Quality": st.session_state["guess_qualities"]},
        index=range(1, len(st.session_state["guess_qualities"]) + 1),
    )

    # initializing chart
    st.bar_chart(
        quality_df, 
        x_label="Number of submitted Guess",
        y_label="Quality of the Guess",
    )
    
else:
    st.write("You have to play games to see the statistics!")


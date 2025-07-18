import streamlit as st
import pandas as pd
import numpy as np

# Title and Introduction
st.title("Data Adventure RPG")
st.markdown(
    "Welcome, Data Detective! Embark on a quest to solve the city's data mysteries. "
    "Complete each challenge to unlock the next stage of your adventure."
)

# Initialize session state for game progress
if 'progress' not in st.session_state:
    st.session_state.progress = "character_setup"
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'avatar' not in st.session_state:
    st.session_state.avatar = None
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'specialty' not in st.session_state:
    st.session_state.specialty = ""
if 'case' not in st.session_state:
    st.session_state.case = ""
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []

### Character Setup
if st.session_state.progress == "character_setup":
    st.header("Character Setup")

    uploaded_avatar = st.file_uploader("Upload your avatar (optional image)", type=['png', 'jpg', 'jpeg'])
    if uploaded_avatar is not None:
        st.session_state.avatar = uploaded_avatar
        st.image(st.session_state.avatar)

    st.session_state.name = st.text_input("Enter your name")
    st.session_state.specialty = st.radio("Choose your specialty", ["Data", "Machine Learning", "Visualization"])

    if st.button("Begin Adventure!"):
        st.session_state.progress = "case_selection"
        st.session_state.achievements.append("Character created!")
        st.rerun()

### Case Selection
elif st.session_state.progress == "case_selection":
    st.header("Case Selection")

    st.write(f"Welcome, {st.session_state.name}! Let's solve a mystery.")
    st.session_state.case = st.selectbox(
        "Choose your case",
        ["Missing Data", "Outlier Detective", "Trend Analyzer"]
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Setup"):
            st.session_state.progress = "character_setup"
            st.rerun()
    with col2:
        if st.button("Start Case"):
            st.session_state.progress = "data_lab"
            st.session_state.achievements.append(f"Case selected: {st.session_state.case}")
            st.rerun()

### Data Lab
elif st.session_state.progress == "data_lab":
    st.header("Data Lab")

    # Sample dataset for the case
    df = pd.DataFrame({
        'A': np.random.randn(20),
        'B': np.random.rand(20) * 100,
        'C': np.random.choice(['X', 'Y', 'Z'], 20)
    })

    st.write("Here is your case data. Explore, filter, and visualize to find clues!")

    # Row 1: Dataframe, filter slider, and chart
    col1, col2 = st.columns([3, 2])
    with col1:
        st.dataframe(df)
    with col2:
        filter_val = st.slider("Select threshold for Column B", 0.0, 100.0, 50.0)
        st.write(f"Filtered data where B > {filter_val}")
        filtered_df = df[df['B'] > filter_val]
        st.dataframe(filtered_df)

    # Row 2: Visualization
    st.write("Visualize your findings:")
    chart_type = st.radio("Chart type", ["Line Chart", "Bar Chart"])
    if chart_type == "Line Chart":
        st.line_chart(filtered_df[['A', 'B']])
    else:
        st.bar_chart(filtered_df[['A', 'B']])

    # Row 3: Controls
    cc1, cc2 = st.columns(2)
    with cc1:
        if st.button("Back to Cases"):
            st.session_state.progress = "case_selection"
            st.rerun()
    with cc2:
        if st.button("I found a clue!"):
            st.session_state.progress = "puzzle_room"
            st.session_state.achievements.append("Clue found in data!")
            st.rerun()

### Puzzle Room
elif st.session_state.progress == "puzzle_room":
    st.header("Puzzle Room")

    st.write("Time for a riddle! Here's your puzzle:")
    st.markdown("**What is the capital of DataLand?**")

    answer = st.text_input("Your answer:")
    if answer.lower() == "datatown":
        st.success("Correct! The mayor thanks you.")
        st.session_state.achievements.append("Puzzle solved!")
        if st.button("Continue to Report"):
            st.session_state.progress = "report_station"
            st.rerun()
    else:
        st.warning("Try again!")
        if st.button("Give up and return to Data Lab"):
            st.session_state.progress = "data_lab"
            st.rerun()

### Report Station
elif st.session_state.progress == "report_station":
    st.header("Report Station")

    st.write("You solved the case—great job! Here’s your final report:")
    report = f"""
    **Data Adventure RPG Case Report**
    **Detective:** {st.session_state.name}
    **Specialty:** {st.session_state.specialty}
    **Case:** {st.session_state.case}
    **Achievements:** {', '.join(st.session_state.achievements)}
    """
    st.markdown(report)

    st.write("You can download your report as a .txt file:")
    st.download_button(
        label="Download Report",
        data=report,
        file_name="data_report.txt",
        mime="text/plain"
    )

    # Simplified leaderboard
    if {'Name': st.session_state.name, 'Case': st.session_state.case, 'Achievements': ', '.join(st.session_state.achievements)} not in st.session_state.leaderboard:
        st.session_state.leaderboard.append({
            'Name': st.session_state.name,
            'Case': st.session_state.case,
            'Achievements': ', '.join(st.session_state.achievements)
        })

    st.header("Leaderboard")
    if st.session_state.leaderboard:
        st.table(pd.DataFrame(st.session_state.leaderboard))

    if st.button("Start a New Adventure"):
        st.session_state.clear()
        st.rerun()

# Display avatar and achievements (always visible after setup)
if st.session_state.get('avatar'):
    st.sidebar.image(st.session_state.avatar, caption=f"{st.session_state.name}'s avatar")

if st.session_state.get('achievements'):
    st.sidebar.header("Achievements")
    for ach in st.session_state.achievements:
        st.sidebar.write("- " + ach)

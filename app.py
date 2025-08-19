import streamlit as st
import requests

# ========================
# ⚽ Fetch actual standings
# ========================
API_KEY = "YOUR_API_KEY"  # <-- put your Football-Data.org API key here
URL = "https://api.football-data.org/v4/competitions/PL/standings"

headers = {"X-Auth-Token": API_KEY}
response = requests.get(URL, headers=headers)

if response.status_code == 200:
    data = response.json()
    actual_table = [team["team"]["name"] for team in data["standings"][0]["table"]]
else:
    st.error("⚠️ Could not fetch standings from API")
    st.stop()

top5_actual = actual_table[:5]
bottom5_actual = actual_table[-5:]

# ========================
# 🎮 Scoring function
# ========================
def calculate_points(actual, predicted):
    points = 0
    top5_actual = actual[:5]
    bottom5_actual = actual[-5:]

    # First 5 = predicted top 5
    for i, team in enumerate(predicted[:5]):
        if team in top5_actual:
            if team == top5_actual[i]:
                points += 10
            else:
                points += 5

    # Last 5 = predicted bottom 5
    for i, team in enumerate(predicted[5:]):
        if team in bottom5_actual:
            if team == bottom5_actual[i]:
                points += 10
            else:
                points += 5

    return points

# ========================
# 🖥️ Streamlit UI
# ========================
st.title("⚽ Premier League Prediction Game")

st.markdown("Pick your **Top 5** and **Bottom 5** teams. Scoring:")
st.markdown("- ✅ Correct position = **10 points**")
st.markdown("- ⚠️ Correct team but wrong place in top/bottom 5 = **5 points**")
st.markdown("- ❌ No points for places 6–15")

teams = actual_table  # use current season teams

player_name = st.text_input("Your name:")

st.subheader("Your Top 5 Teams")
top5_pick = st.multiselect("Pick your Top 5 (in order)", teams, max_selections=5)

st.subheader("Your Bottom 5 Teams")
bottom5_pick = st.multiselect("Pick your Bottom 5 (in order)", teams, max_selections=5)

if st.button("Submit Prediction"):
    if len(top5_pick) == 5 and len(bottom5_pick) == 5 and player_name:
        prediction = top5_pick + bottom5_pick
        score = calculate_points(actual_table, prediction)

        st.success(f"🎉 {player_name}, you scored **{score} points**!")

        # Store results in session
        if "results" not in st.session_state:
            st.session_state["results"] = {}
        st.session_state["results"][player_name] = score
    else:
        st.error("⚠️ Please select exactly 5 teams for Top 5 and Bottom 5, and enter your name.")

# ========================
# 📊 Leaderboard
# ========================
if "results" in st.session_state and st.session_state["results"]:
    st.subheader("🏆 Leaderboard")
    ranked_results = dict(sorted(st.session_state["results"].items(), key=lambda x: x[1], reverse=True))

    for player, score in ranked_results.items():
        st.write(f"**{player}** — {score} points")

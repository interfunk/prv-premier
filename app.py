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
# 📝 Player Predictions
# ========================
predictions = {
    "Alice": [
        "Manchester City FC", "Arsenal FC", "Liverpool FC", "Chelsea FC", "Manchester United FC",
        "AFC Bournemouth", "Brentford FC", "Burnley FC", "Sunderland AFC", "Wolverhampton Wanderers FC"
    ],
    "Bob": [
        "Liverpool FC", "Arsenal FC", "Manchester City FC", "Tottenham Hotspur FC", "Newcastle United FC",
        "Everton FC", "Burnley FC", "Leeds United FC", "Crystal Palace FC", "AFC Bournemouth"
    ],
    "Jeff": [
        "Manchester City FC", "Sunderland AFC", "Tottenham Hotspur FC", "Liverpool FC", "Nottingham Forest FC",
        "AFC Bournemouth", "Brentford FC", "Burnley FC", "West Ham United FC", "Wolverhampton Wanderers FC"
    ]
    # ➕ Add more players here
}

# ========================
# 🏆 Leaderboard
# ========================
st.title("⚽ Premier League Prediction Leaderboard")

results = {player: calculate_points(actual_table, table) for player, table in predictions.items()}
ranked_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

st.subheader("Current Rankings")

for rank, (player, score) in enumerate(ranked_results.items(), start=1):
    st.write(f"**{rank}. {player} — {score} points**")

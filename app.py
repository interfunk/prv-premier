import streamlit as st
import os
import requests

# ========================
# ⚽ Fetch actual standings
# ========================

# ✅ Load API key from Streamlit Secrets
API_KEY = os.environ.get("FOOTBALL_API_KEY")
if not API_KEY:
    st.error("⚠️ API key not found! Did you set it in Streamlit Secrets?")

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
    details = []

    top5_actual = actual[:5]
    bottom5_actual = actual[-5:]

    # First 5 = predicted top 5
    for i, team in enumerate(predicted[:5]):
        if team in top5_actual:
            if team == top5_actual[i]:
                points += 10
                details.append(f"{team}: ✅ Exact position (+10)")
            else:
                points += 5
                details.append(f"{team}: ➕ Correct Top 5 (+5)")
        else:
            details.append(f"{team}: ❌ No points")

    # Last 5 = predicted bottom 5
    for i, team in enumerate(predicted[5:]):
        if team in bottom5_actual:
            if team == bottom5_actual[i]:
                points += 10
                details.append(f"{team}: ✅ Exact position (+10)")
            else:
                points += 5
                details.append(f"{team}: ➕ Correct Bottom 5 (+5)")
        else:
            details.append(f"{team}: ❌ No points")

    return points, details

# ========================
# 📝 Player Predictions
# ========================
predictions = {
	"Paulius": ['Liverpool FC', 'Chelsea FC', 'Arsenal FC', 'Manchester City FC', 'Newcastle United FC', 'Nottingham Forest FC', 'Leeds United FC', 'AFC Bournemouth', 'Sunderland AFC', 'Burnley FC'],
    "Tom": ['Liverpool FC', 'Chelsea FC', 'Arsenal FC', 'Manchester City FC', 'Newcastle United FC', 'Nottingham Forest FC', 'Leeds United FC', 'AFC Bournemouth', 'Sunderland AFC', 'Burnley FC'],
}

# ========================
# 🏆 Leaderboard
# ========================
st.title("PRV Premier League Prediction Leaderboard")

results = {}
details_map = {}
for player, table in predictions.items():
    score, details = calculate_points(actual_table, table)
    results[player] = score
    details_map[player] = details

ranked_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

# Small CSS for tooltips
st.markdown("""
<style>
.tooltip {
  position: relative;
  display: inline-block;
  cursor: help;
  font-weight: bold;
}
.tooltip .tooltiptext {
  visibility: hidden;
  width: 280px;
  background-color: #333;
  color: #fff;
  text-align: left;
  border-radius: 6px;
  padding: 8px;
  position: absolute;
  z-index: 1;
  bottom: 125%; 
  left: 50%;
  margin-left: -140px;
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 0.8rem;
  line-height: 1.2rem;
}
.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}
</style>
""", unsafe_allow_html=True)

st.subheader("Current Rankings")

for rank, (player, score) in enumerate(ranked_results.items(), start=1):
    breakdown_html = "<br>".join(details_map[player])
    st.markdown(
        f'<div class="tooltip">{rank}. {player} — {score} pts'
        f'<span class="tooltiptext">{breakdown_html}</span></div>',
        unsafe_allow_html=True
    )

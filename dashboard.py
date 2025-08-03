import streamlit as st
import pandas as pd
from mplsoccer import Radar, grid
import matplotlib.pyplot as plt
import numpy as np

# === Load data ===
@st.cache_data
def load_data():
    df = pd.read_csv("450mins.csv")  # Replace with your path
    df = df[df["minutesplayed"] > 300]
    return df

df = load_data()
st.title("Singapore Premier League Player Radar Dashboard")

# === Position and Team selection ===
col1, col2 = st.columns(2)

with col1:
    position = st.selectbox("Select position:", ["F", "M", "D", "GK"])

# Filter by position first for all calculations
df_position = df[df["position_new"] == position].copy()

with col2:
    # Get unique teams for the selected position
    teams = sorted(df_position["team_name"].unique())
    selected_team = st.selectbox("Select team:", ["All Teams"] + list(teams))

# Apply team filter for display only
if selected_team != "All Teams":
    df_filtered = df_position[df_position["team_name"] == selected_team].copy()
else:
    df_filtered = df_position.copy()

# === Compute stats based on position ===
# Calculate per 90 stats for all players in this position
df_position["goals_per_90"] = df_position["goals"] / df_position["minutesplayed"] * 90
df_position["xg_per_90"] = df_position["expectedgoals"] / df_position["minutesplayed"] * 90
df_position["shots_per_90"] = df_position["totalshots"] / df_position["minutesplayed"] * 90
df_position["assists_per_90"] = df_position["assists"] / df_position["minutesplayed"] * 90
df_position["keypasses_per_90"] = df_position["keypasses"] / df_position["minutesplayed"] * 90
df_position["bigchancescreated_per_90"] = df_position["bigchancescreated"] / df_position["minutesplayed"] * 90
df_position["dribbles_per_90"] = df_position["successfuldribbles"] / df_position["minutesplayed"] * 90
df_position["passes_per_90"] = df_position["totalpasses"] / df_position["minutesplayed"] * 90
df_position["tackles_per_90"] = df_position["tackles"] / df_position["minutesplayed"] * 90
df_position["interceptions_per_90"] = df_position["interceptions"] / df_position["minutesplayed"] * 90
df_position["clearances_per_90"] = df_position["clearances"] / df_position["minutesplayed"] * 90
df_position["saves_per_90"] = df_position["saves"] / df_position["minutesplayed"] * 90
df_position["goalsconceded_per_90"] = df_position["goalsconceded"] / df_position["minutesplayed"] * 90
df_position["longballs_per_90"] = df_position["totallongballs"] / df_position["minutesplayed"] * 90

# Also compute stats for filtered data (for display)
df_filtered = df_filtered.copy()
df_filtered["goals_per_90"] = df_filtered["goals"] / df_filtered["minutesplayed"] * 90
df_filtered["xg_per_90"] = df_filtered["expectedgoals"] / df_filtered["minutesplayed"] * 90
df_filtered["shots_per_90"] = df_filtered["totalshots"] / df_filtered["minutesplayed"] * 90
df_filtered["assists_per_90"] = df_filtered["assists"] / df_filtered["minutesplayed"] * 90
df_filtered["keypasses_per_90"] = df_filtered["keypasses"] / df_filtered["minutesplayed"] * 90
df_filtered["bigchancescreated_per_90"] = df_filtered["bigchancescreated"] / df_filtered["minutesplayed"] * 90
df_filtered["dribbles_per_90"] = df_filtered["successfuldribbles"] / df_filtered["minutesplayed"] * 90
df_filtered["passes_per_90"] = df_filtered["totalpasses"] / df_filtered["minutesplayed"] * 90
df_filtered["tackles_per_90"] = df_filtered["tackles"] / df_filtered["minutesplayed"] * 90
df_filtered["interceptions_per_90"] = df_filtered["interceptions"] / df_filtered["minutesplayed"] * 90
df_filtered["clearances_per_90"] = df_filtered["clearances"] / df_filtered["minutesplayed"] * 90
df_filtered["saves_per_90"] = df_filtered["saves"] / df_filtered["minutesplayed"] * 90
df_filtered["goalsconceded_per_90"] = df_filtered["goalsconceded"] / df_filtered["minutesplayed"] * 90
df_filtered["longballs_per_90"] = df_filtered["totallongballs"] / df_filtered["minutesplayed"] * 90

# === Choose radar stats based on position ===
if position == "F":  # Forwards
    params = [
        "Goals per 90", "Expected Goals per 90", "Shots per 90", "Goal Conversion %", 
        "Assists per 90", 
        "Key Passes per 90", "Big Chances Created per 90", "Dribbles per 90", 
        "Aerial Duel Win %"
    ]
    raw_stats = [
        "goals_per_90", "xg_per_90", "shots_per_90", "goalconversionpercentage", 
        "assists_per_90",
        "keypasses_per_90", "bigchancescreated_per_90", "dribbles_per_90",
        "aerialduelswonpercentage"
    ]
elif position == "M":  # Midfielders
    params = [
        "Assists per 90", "Key Passes per 90", "Big Chances Created per 90", "Dribbles per 90",
        "Passes per 90", "Pass Accuracy %", "Tackles per 90", "Interceptions per 90", "Duel Win %"
    ]
    raw_stats = [
        "assists_per_90", "keypasses_per_90", "bigchancescreated_per_90", "dribbles_per_90",
        "passes_per_90", "accuratepassespercentage", "tackles_per_90", "interceptions_per_90", "totalduelswonpercentage"
    ]
elif position == "D":  # Defenders
    params = [
        "Tackles per 90", "Interceptions per 90", "Clearances per 90", "Aerial Duel Win %",
        "Duel Win %", "Passes per 90", "Pass Accuracy %", "Clean Sheets", "Goals per 90"
    ]
    raw_stats = [
        "tackles_per_90", "interceptions_per_90", "clearances_per_90", "aerialduelswonpercentage",
        "totalduelswonpercentage", "passes_per_90", "accuratepassespercentage", "cleansheet(df)", "goals_per_90"
    ]
else:  # Goalkeepers
    params = [
        "Saves per 90", "Clean Sheets", "Goals Conceded per 90", "Saves from Inside Box",
        "Passes per 90", "Pass Accuracy %", "Long Balls per 90", "Long Ball Accuracy %",
    ]
    raw_stats = [
        "saves_per_90", "cleansheet(gk)", "goalsconceded_per_90", "savedshotsfrominsidethebox",
        "passes_per_90", "accuratepassespercentage", "longballs_per_90", "accuratelongballspercentage",
    ]

# === Player selection ===
if len(df_filtered) == 0:
    st.error("No players found for the selected position and team combination. Please try different filters.")
    st.stop()

player_name = st.selectbox(f"Select player:", df_filtered["player_name"].unique())

# Add comparison functionality
st.subheader("Player Comparison")
compare_players = st.multiselect(
    "Select player to compare with (max 1):",
    df_filtered["player_name"].unique(),
    default=None,
    max_selections=1
)

# Get selected player data
player_row = df_filtered[df_filtered["player_name"] == player_name].iloc[0]

# Calculate appropriate low and high values for each statistic
low = []
high = []
debug_info = []

for stat in raw_stats:
    if stat in df_position.columns:
        all_values = df_position[stat].dropna()
        if len(all_values) > 0:
            # Use StatsBomb's rule: 5th percentile for bottom, 95th percentile for top
            stat_min = all_values.quantile(0.05)  # Bottom 5%
            stat_max = all_values.quantile(1)  # Top 5%
            
            low.append(stat_min)
            high.append(stat_max)
            
            # Debug info
            debug_info.append({
                'stat': stat,
                'min': stat_min,
                'max': stat_max,
                'actual_min': all_values.min(),
                'actual_max': all_values.max(),
                'mean': all_values.mean()
            })
        else:
            low.append(0)
            high.append(100)
            debug_info.append({
                'stat': stat,
                'min': 0,
                'max': 100,
                'actual_min': 0,
                'actual_max': 0,
                'mean': 0
            })
    else:
        low.append(0)
        high.append(100)
        debug_info.append({
            'stat': stat,
            'min': 0,
            'max': 100,
            'actual_min': 0,
            'actual_max': 0,
            'mean': 0
        })

# Debug output
#st.subheader("Debug: Radar Boundaries (StatsBomb Rule)")
#debug_df = pd.DataFrame(debug_info)
#st.dataframe(debug_df, use_container_width=True)

#radar chart

# Calculate percentiles for the selected player
player_raw_values = []
for stat in raw_stats:
    if stat in player_row:
        player_raw_values.append(player_row[stat])
    else:
        player_raw_values.append(0)

# Get comparison players raw values
comparison_data = []
if compare_players:
    for comp_player in compare_players:
        comp_player_data = df_filtered[df_filtered["player_name"] == comp_player]
        if len(comp_player_data) > 0:
            comp_row = comp_player_data.iloc[0]
            comp_raw_values = []
            for stat in raw_stats:
                if stat in comp_row:
                    comp_raw_values.append(comp_row[stat])
                else:
                    comp_raw_values.append(0)
            comparison_data.append({
                'name': comp_player,
                'raw_values': comp_raw_values,
                'team': comp_row['team_name']
            })

radar = Radar(params, low, high, round_int=[False]*len(params), num_rings=4, ring_width=1, center_circle_radius=1)

# Creating the figure using the grid function from mplsoccer:
fig, axs = grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                title_space=0, endnote_space=0, grid_key='radar', axis=False)

# plot the radar
radar.setup_axis(ax=axs['radar'])
rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#1a1a1a', edgecolor='white', alpha=0.3)

# Draw main player radar
radar_output = radar.draw_radar_solid(player_raw_values, ax=axs['radar'],
                                 kwargs={'facecolor': '#aa65b2', 'alpha': 0.6, 'edgecolor': '#502a54', 'lw': 3})
radar_poly, vertices = radar_output

# Add scatter points for main player
axs['radar'].scatter(vertices[:, 0], vertices[:, 1],
                     c='#aa65b2', edgecolors='#502a54', marker='o', s=100, zorder=2)

# Draw comparison players if selected
if comparison_data:
    for i, comp_player in enumerate(comparison_data):        
        comp_radar_output = radar.draw_radar_solid(comp_player['raw_values'], ax=axs['radar'],
                                            kwargs={'facecolor': '#66d8ba', 'alpha': 0.6, 'edgecolor': '#216352', 'lw': 3})
        comp_poly, comp_vertices = comp_radar_output
        
        # Add scatter points for comparison player
        axs['radar'].scatter(comp_vertices[:, 0], comp_vertices[:, 1],
                            c='#66d8ba', edgecolors='#216352', marker='o', s=100, zorder=2)

# Draw range labels (percentile numbers on rings)
range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=12, color='black')

# Draw parameter labels
param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=15, color='black')

# Draw spoke lines from center to edge
radar.spoke(ax=axs['radar'], color='white', linestyle='--', linewidth=0.5, alpha=0.6)

# Add legend if comparing players
if comparison_data:
    legend_text = f"Main Player: {player_name} ({player_row['team_name']}) - Purple"
    axs['radar'].text(0.02, 0.98, legend_text, transform=axs['radar'].transAxes, 
                      fontsize=10, color='#aa65b2', weight='bold', va='top')
    
    comparison_colors = ['#66d8ba', '#697cd4', '#ff7f0e', '#d62728', '#9467bd']
    color_names = ['Teal', 'Blue', 'Orange', 'Red', 'Purple']
    
    for i, comp_player in enumerate(comparison_data):
        color = comparison_colors[i % len(comparison_colors)]
        color_name = color_names[i % len(color_names)]
        legend_text = f"Comparison: {comp_player['name']} ({comp_player['team']}) - {color_name}"
        axs['radar'].text(0.02, 0.95 - i*0.03, legend_text, transform=axs['radar'].transAxes, 
                          fontsize=10, color=color, weight='bold', va='top')

# adding the endnote and title text
position_names = {"F": "Forward", "M": "Midfielder", "D": "Defender", "GK": "Goalkeeper"}
team_info = f" ({player_row['team_name']})" if selected_team == "All Teams" else ""

#endnote and title text
endnote_text = axs['endnote'].text(0.99, 0.5, 'Data: Singapore Premier League 2024', fontsize=15,
                                   ha='right', va='center', color='black', weight='bold')
title1_text = axs['title'].text(0.01, 0.65, player_name, fontsize=25,
                                ha='left', va='center', color='black', weight='bold')
title2_text = axs['title'].text(0.01, 0.25, player_row['team_name'], fontsize=20,
                                ha='left', va='center', color='#1a1a1a')
title3_text = axs['title'].text(0.99, 0.65, 'Radar Chart', fontsize=25,
                                ha='right', va='center', color='black', weight='bold')
title4_text = axs['title'].text(0.99, 0.25, position_names[position], fontsize=20,
                                ha='right', va='center', color='black')

st.pyplot(fig)

# === Player stats table ===
st.subheader("Player Statistics (Raw Values)")
stats_display = {}
for i, param in enumerate(params):
    raw_stat = raw_stats[i]
    if raw_stat in player_row:
        if "percentage" in raw_stat:
            stats_display[param] = f"{player_row[raw_stat]:.1f}%"
        elif raw_stat in ["rating"]:
            stats_display[param] = f"{player_row[raw_stat]:.2f}"
        else:
            stats_display[param] = f"{player_row[raw_stat]:.2f}"
    else:
        stats_display[param] = "N/A"

stats_df = pd.DataFrame(list(stats_display.items()), columns=["Statistic", "Value"])
st.table(stats_df)

# Show comparison stats if comparing
if comparison_data:
    st.subheader("Comparison Statistics")
    comp_stats = []
    for comp in comparison_data:
        comp_row = df_filtered[df_filtered["player_name"] == comp['name']].iloc[0]
        comp_data = {"Player": comp['name'], "Team": comp['team']}
        for i, param in enumerate(params):
            raw_stat = raw_stats[i]
            if raw_stat in comp_row:
                if "percentage" in raw_stat:
                    comp_data[param] = f"{comp_row[raw_stat]:.1f}%"
                elif raw_stat in ["rating"]:
                    comp_data[param] = f"{comp_row[raw_stat]:.2f}"
                else:
                    comp_data[param] = f"{comp_row[raw_stat]:.2f}"
            else:
                comp_data[param] = "N/A"
        comp_stats.append(comp_data)
    
    comp_df = pd.DataFrame(comp_stats)
    st.dataframe(comp_df, use_container_width=True)

# === Team comparison (if team is selected) ===
if selected_team != "All Teams":
    st.subheader(f"Team Comparison - {selected_team}")
    
    # Show all players from the selected team in this position
    team_players = df_filtered[df_filtered["team_name"] == selected_team]
    
    if len(team_players) > 1:
        comparison_data = []
        for _, player in team_players.iterrows():
            player_percentiles = df_position[df_position["player_name"] == player["player_name"]].iloc[0].values.tolist()
            comparison_data.append({
                "Player": player["player_name"],
                "Team": player["team_name"],
                "Minutes": player["minutesplayed"],
                "Avg Percentile": f"{np.mean(player_percentiles):.1f}%"
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)

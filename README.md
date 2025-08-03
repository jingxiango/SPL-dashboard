# SPL Dashboard - Singapore Premier League Player Analytics

A comprehensive Streamlit dashboard for analyzing Singapore Premier League player statistics with interactive radar charts and player comparisons.

## 🚀 Features

### 📊 **Interactive Radar Charts**
- **Position-specific metrics** for Forwards, Midfielders, Defenders, and Goalkeepers
- **Organized by categories**: Attack, Midfield, Defense
- **Per-90 statistics** for fair comparison across different playing minutes
- **Flipped statistics** where lower values are better (errors, fouls, missed chances)

### 👥 **Player Comparison**
- **Compare up to 3 players** simultaneously
- **Cross-team comparisons** - compare players from different teams
- **Unique color coding** for each comparison player
- **Detailed statistics tables** for all compared players

### 🎯 **Smart Filtering**
- **Position-based filtering** (F, M, D, GK)
- **Team-specific analysis** or view all teams
- **Minimum playing time filter** (300+ minutes)
- **Error handling** for empty datasets

### 📈 **Advanced Analytics**
- **StatsBomb methodology** for radar chart boundaries (5th-95th percentile)
- **Per-90 calculations** for all key metrics
- **Percentage-based statistics** (pass accuracy, duel win rates, etc.)
- **Team comparison tables** with percentile rankings

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/jingxiango/SPL-dashboard.git
   cd SPL-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   streamlit run dashboard.py
   ```

## 📋 Requirements

The dashboard uses the following key libraries:
- `streamlit` - Web application framework
- `pandas` - Data manipulation and analysis
- `matplotlib` - Plotting and visualization
- `mplsoccer` - Soccer-specific radar charts
- `numpy` - Numerical computations

## 🎮 Usage

### Getting Started
1. **Select Position**: Choose from Forward (F), Midfielder (M), Defender (D), or Goalkeeper (GK)
2. **Choose Team**: Filter by specific team or view "All Teams"
3. **Select Player**: Pick the main player to analyze
4. **Add Comparisons**: Select up to 3 players to compare against

### Understanding the Radar Chart
- **Purple**: Main selected player
- **Other colors**: Comparison players (Teal, Blue, Orange, Red, Purple, Green, Pink, Brown)
- **Edge of chart**: Best performance in that metric
- **Center of chart**: Lower performance (except for flipped statistics)

### Position-Specific Metrics

#### **Forwards (F)**
- **Attack**: Goals per 90, Expected Goals per 90, Shots per 90, Goal Conversion %, Big Chances Missed per 90
- **Midfield**: Assists per 90, Key Passes per 90, Big Chances Created per 90, Dribbles per 90
- **Defense**: Aerial Duel Win %

#### **Midfielders (M)**
- **Attack**: Assists per 90, Expected Assists per 90, Key Passes per 90, Big Chances Created per 90
- **Midfield**: Dribbles per 90, Successful Dribbles %, Passes per 90, Pass Accuracy %, Final Third Passes per 90
- **Defense**: Tackles per 90, Interceptions per 90, Duel Win %

#### **Defenders (D)**
- **Attack**: Long Balls per 90, Long Ball Accuracy %
- **Midfield**: Passes per 90, Pass Accuracy %
- **Defense**: Tackles per 90, Interceptions per 90, Clearances per 90, Aerial Duel Win %, Duel Win %, Errors Leading to Shots, Fouls Per 90

#### **Goalkeepers (GK)**
- **Saves per 90**, Clean Sheets, Goals Conceded per 90, Saves from Inside Box
- **Passes per 90**, Pass Accuracy %, Long Balls per 90, Long Ball Accuracy %

## 📊 Data Source

The dashboard uses Singapore Premier League 2024 data with the following key metrics:
- **Basic stats**: Goals, assists, minutes played, appearances
- **Advanced metrics**: Expected goals, key passes, big chances created
- **Defensive stats**: Tackles, interceptions, clearances, saves
- **Passing stats**: Pass accuracy, final third passes, long balls
- **Duel stats**: Aerial duels, total duels, duel win percentages

## 🔧 Technical Details

### Data Processing
- **Minimum 300 minutes** playing time filter
- **Per-90 calculations** for all relevant statistics
- **Percentage conversions** for accuracy-based metrics
- **Error handling** for missing data and edge cases

### Visualization
- **Radar charts** using mplsoccer library
- **StatsBomb methodology** for chart boundaries
- **Color-coded comparisons** with unique colors per player
- **Responsive design** for different screen sizes

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 📞 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Data Source**: Singapore Premier League 2024  
**Last Updated**: August 2024  
**Version**: 1.0

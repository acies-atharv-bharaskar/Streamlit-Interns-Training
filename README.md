# Data Adventure RPG

An interactive web-based game that teaches data analysis concepts through a detective-themed adventure!

## 🎮 Game Overview

Embark on a quest to solve the city's data mysteries. Complete each challenge to unlock the next stage of your adventure.

### Features:
- **Character Creation**: Upload an avatar and choose your data specialty
- **Case Selection**: Choose from different mystery cases
- **Data Lab**: Explore, filter, and visualize data to find clues
- **Puzzle Challenges**: Solve riddles to progress
- **Achievement System**: Track your progress
- **Leaderboard**: Compare with other detectives
- **Report Generation**: Download your case reports

## 🚀 How to Run

### Option 1: Using uv (Recommended)
1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install Dependencies**:
   ```bash
   uv sync
   ```

3. **Run the Game**:
   ```bash
   uv run streamlit run data_adventure_rpg.py
   ```

### Option 2: Using pip
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Game**:
   ```bash
   streamlit run data_adventure_rpg.py
   ```

### Open Your Browser
The game will open at `http://localhost:8501`

## 🎯 Game Flow

1. **Character Setup**: Create your detective persona
2. **Case Selection**: Choose your mystery to solve
3. **Data Lab**: Analyze the case data using filters and charts
4. **Puzzle Room**: Solve the riddle to unlock the next stage
5. **Report Station**: Generate your final case report

## 🛠️ Technical Details

- Built with **Streamlit** for the web interface
- Uses **Pandas** for data manipulation
- **NumPy** for numerical operations
- Session state management for game progress
- Interactive data visualization

## 🎨 Customization Ideas

- Add more case types with different datasets
- Create more complex puzzles
- Add scoring system
- Implement different difficulty levels
- Add sound effects and animations

Enjoy your data detective adventure! 🕵️‍♂️📊 
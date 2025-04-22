# 🐍 Snake Web Arcade

An enhanced browser-based **Snake Game** with modern UI, Google login, user profiles, and leaderboard — built using **Flask, JavaScript, and HTML5 Canvas**.

## 🔥 Features

- 🎮 Playable Snake game in the browser
- 👤 Google-based Login & Signup
- 🧾 User profiles with high score, games played, and total time
- 🏆 Global leaderboard of top 100 players
- 📈 Score history chart using Chart.js
- ☁️ All user data stored in JSON (can later connect to DB)

## 🚀 Tech Stack

- **Frontend:** HTML5, CSS, JavaScript (Canvas, Chart.js)
- **Backend:** Python Flask
- **Auth:** Google OAuth via Flask-Dance
- **Storage:** `users.json` file (easy to extend to DB)

## 🛠️ Setup Instructions

```bash
git clone https://github.com/AnishPasupuleti/snake-game.git
cd snake-game
pip install -r requirements.txt
python app.py

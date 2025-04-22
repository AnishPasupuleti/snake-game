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

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AnishPasupuleti/snake-game.git
   cd snake-game


## 🛠️ Setup Instructions

### 📦 Install dependencies:
```bash
pip install -r requirements.txt
python app.py
 ```

🔐 **Configure Google OAuth**:  
Go to Google Cloud Console  
Create OAuth 2.0 Client ID credentials  
Set redirect URI:  http://localhost:5000/login/google/authorized

Add your `client_id` and `client_secret` in `app.py` file  

---

🧠 **How It Works**  
🕹️ Frontend renders the game using JavaScript Canvas  
🧠 Backend tracks users and scores via Google login  
📤 Score data is sent from browser to Flask `/update_score` API  
🗃️ `users.json` holds all player history, high scores, and stats  
📈 Dashboard visualizes your stats with a chart and play history  

---

📌 **Future Enhancements**  
🎯 Power-ups, speed modes, multiplayer support  
🌐 Switch to Firebase/PostgreSQL for cloud storage  
📊 In-depth analytics and personalized performance trends  
🧠 AI snake demo mode


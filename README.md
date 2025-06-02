# 🎲 Controlled Chaos
### A Game Randomizer (Rainbow Six Siege & Helldivers 2)

A Python tool that randomly assigns unique operators, stratagems, and boosters to players  
for the Rainbow Six Siege and Helldivers 2 video games.

---

<details>
  <summary>📚 Table of Contents</summary>
  <ol>
    <li><a href="#background">📖 Background</a></li>
    <li><a href="#about-the-program">💡 About the Program</a></li>
    <li><a href="#features">🚀 Features</a></li>
    <li><a href="#how-to-run">🛠️ How to Run</a></li>
    <li><a href="#planned-features">🗓️ Planned Features</a></li>
    <li><a href="#built-with">🧪 Built With</a></li>
    <li><a href="#license">📜 License</a></li>
    <li><a href="#author">👤 Author</a></li>
  </ol>
</details>

---

## 📖 Background

Following a casual evening out, I came home and played Helldivers 2 with a friend.  
After a few months of casual gameplay, we had found that the challenge had mostly disappeared.  
I felt this was largely because we tended to rely on the same familiar stratagems for our specific play-styles.

To shake things up, I thought it would be fun (and more chaotic) to randomize the stratagems we used during missions. Since Helldivers didn’t offer this feature, I figured why not build it myself.

What started as a very simple tool to pick random stratagems quickly turned into a fully customizable game randomizer — complete with player profiles, cooldowns, incompatible stratagem pairings, and much more.  
It’s reintroduced excitement, unpredictability, and countless hours of laughter and profanities in our game nights.

---

## 💡 About the Program

This program generates randomized loadouts for players in Rainbow Six Siege and Helldivers 2.  
Players are assigned unique combinations of operators (Siege) or stratagems, boosters, and armor (Helldivers),  
based on the operators/stratagems that have been previously generated for them within the last 7 days.

The program ensures fairness by avoiding duplication, honoring cooldown periods, and preventing banned combinations. Player sessions are saved to JSON files, and administrators can modify game data or view what’s available for each player.

---

## 🚀 Features

- Supports two video games: Rainbow Six Siege and Helldivers 2
- Tracks each player’s personalized game history in individual JSON files
- Prevents repeated stratagems, operators, boosters, and armor for a player within a 7-day cooldown period
- Detects and avoids incompatible stratagem combinations using a banned pair list
- Supports multiple randomness modes:
  - Complete Randomness (Helldivers)
  - Stratagem Category Spread (Helldivers)
  - Standard vs Quick Match (Siege)
- Allows game administrators to:
  - Add, edit, delete, and view game content and settings
  - Check what content is still available per player
- Automatically saves player selections and game state to files

---

## 🛠️ How to Run

1. Ensure you have **Python 3.10+** installed.
2. Place the necessary game data JSON file in the correct directory (`./Game_Data.json`).
3. Open the terminal in your project folder.
4. Run the program:

```bash
python3 main.py
```

---

## 🗓️ Planned Features

- Implement a web interface using Flask for multiplayer support.
- Develop a file locking system to prevent simultaneous writes and data corruption.
- Separate game data and player profile data to improve scalability and maintainability.
- Track the number of randomized games played per player each month.
- Introduce a redundancy file to back up player data in case the main file becomes corrupted.
- Enhance program’s interface for better usability and management of player profiles.

---

## 🔧 Built With

<p align="center">
  <a href="https://www.python.org">
    <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white">
  </a>
  <a href="https://www.json.org">
    <img src="https://img.shields.io/badge/Data-JSON-blueviolet?style=for-the-badge&logo=json&logoColor=white">
  </a>
  <a href="https://git-scm.com">
    <img src="https://img.shields.io/badge/Version%20Control-Git%20%26%20GitHub-orange?style=for-the-badge&logo=git&logoColor=white">
  </a>
  <a href="https://www.jetbrains.com/pycharm/">
    <img src="https://img.shields.io/badge/IDE-PyCharm-green?style=for-the-badge&logo=pycharm&logoColor=white">
  </a>
  <a href="https://www.microsoft.com/en-us/windows">
    <img src="https://img.shields.io/badge/Platform-Windows-darkred?style=for-the-badge&logo=windows&logoColor=white">
  </a>
</p>

<p align="right">(<a href="#top">back to top</a>)</p>

---

## 📜 License
This project is licensed under the MIT License.

---

## 👤 Author
Jason Anderson
Computer Science Student
Interests: Programming • Cybersecurity • Data Science

GitHub: @MapNotIncluded

<p align="right">(<a href="#top">back to top</a>)</p>

---
# 🎲 Controlled Chaos
### A Game Randomizer (Rainbow Six Siege & Helldivers 2)

A Python tool that randomly assigns unique operators, stratagems, and boosters to players 
for the Rainbow Six Siege and Helldivers 2 video games. 

---

## Background

Following a casual evening out, I came home and played Helldivers 2 with a friend. 
After a few months of casual gameplay, we had found that the challenge had mostly disappeared.
I felt this was largely because we tended to rely on the same familiar stratagems for our specific play-styles.

To shake things up, I thought it would be fun (and more chaotic) to randomize the stratagems we used during missions. 
Since Helldivers didn’t offer this feature, I figured why not build it myself.

What started as a very simple tool to pick random stratagems quickly turned into a fully customizable game randomizer 
— complete with player profiles, cooldowns, incompatible stratagem pairings, and so much more. 
It’s reintroduced excitement, unpredictability, and countless hours of laughter and profanities in our game nights.

---

## About the Program

This program generates randomized loadouts for players in Rainbow Six Siege and Helldivers 2.
Players are assigned unique combinations of operators (Siege) or stratagems, boosters, and armor (Helldivers), 
based on their personal unlock history and the operators/stratagems that have been previously generated for them within the last 7 days. 

The program ensures fairness by avoiding duplication, honouring cooldown periods, and preventing banned combinations. 
Player sessions are saved to json files, and administrators can modify game data or view what’s available for each player.

---

## Features

- 🎮 Supports two video games: *Rainbow Six Siege* and *Helldivers 2*
- 👤 Tracks each player’s personalized game history in individual JSON files
- 🔁 Prevents repeated stratagems, operators, boosters, and armor for a player within a 7-day cooldown period
- ⚠️ Detects and avoids incompatible stratagem combinations using a banned pair list
- 🎲 Supports multiple randomness modes:
  - Complete Randomness (Helldivers)
  - Stratagem Category Spread (Helldivers)
  - Standard vs Quick Match (Siege)
- 🧠 Allows game administrators to:
  - Add, edit, delete, and view game content and settings
  - Check what content is still available per player
- 💾 Automatically saves player selections and game state to files

---

## How to Run

1. Ensure you have **Python 3.10+** installed.
2. Place the necessary game data JSON file in the correct directory (`./Game_Data.json`).
3. Open the terminal in your project folder.
4. Run the program:

```bash
  python3 main.py
```

---

## Planned Features

- 📤 CSV export of recent player history for basic stats & Power BI dashboards
- 🌐 Web interface using Flask for multiplayer access
- 🔐 File locking system to prevent simultaneous writes and corruption
- ⚙️ Optional unit tests to validate cooldown expiry and banned pair enforcement

---

## 🔧 Built with:
- ![Python](https://img.shields.io/badge/Python-3.11-blue)
- ![JSON](https://img.shields.io/badge/Data-JSON-blueviolet)
- ![Git](https://img.shields.io/badge/Version%20Control-Git%20%26%20GitHub-orange)
- ![PyCharm](https://img.shields.io/badge/IDE-PyCharm-green)
- ![Windows](https://img.shields.io/badge/Platform-Windows-darkred)

---

## 📜 License
This project is licensed under the MIT License.

---

## 👤 Author

**Jason Anderson**  
_Computer Science Student_  
_Interests: Programming • Cybersecurity • Data Science_  
GitHub: @MapNotIncluded

---
# College-Football-Excel-Model

> **2025 Perfect CFP Bracket Achieved!** > This predictive model successfully forecasted every single matchup and the eventual national champion in the 2025 College Football Playoff.

Welcome to the **College Football Excel Model**. This project is a robust, data-driven forecasting tool that combines a backend Python web scraper with a Microsoft Excel dashboard. It is a baseline-driven model built on a sample of the previous 10 national champions for NCAA Division I FBS college football to accurately project playoff outcomes.

---

## The 2025 Perfect Bracket
In the 2025 season, this model achieved something extremely rare: **a 100% accurate prediction of the College Football Playoff bracket.** 

<img width="513" height="552" alt="CFP Perfect Bracket 2024-25" src="https://github.com/user-attachments/assets/60869162-d030-4c9a-ad91-11e607f8b3ec" />

**How it did it:**
* Accurately displays a total body of work for a team rather than relying on flawed, result-based ranking systems (like the AP Poll) that often fail to capture true season-long performance.
* Compares current teams against historical data patterns of previous National Champions.
* Heavily values dominant teams that play difficult schedules over teams with inflated records against weak opponents.

---

## Features & Methodology

The model consists of a Python backend (`cfb_model.py`) that scrapes live data and an Excel frontend (`College Football Model.xlsm`) that processes it. It evaluates teams based on a **"Total Points" benchmark system**: the model counts how many of a team's stats *fail* to meet historical championship baseline criteria. **The lower the point total, the stronger the team.**

Data is scraped from ESPN and TeamRankings, merged using fuzzy logic, and evaluates:
* **ESPN FPI & Resume Metrics:** Football Power Index (FPI) and Strength of Schedule (SOS).
* **Team Efficiencies:** Overall, Offensive, and Defensive Efficiencies.
* **Situational Success:** 3rd Down Conversion % (Offense & Defense) and Red Zone % (Offense & Defense).
* **Core Production:** Passing/Rushing Yards Per Game (For and Against) and Points Per Game (For and Against).
* **Discipline & Luck:** Penalties per game and Turnover Margin.

---

## How to Use the Model

### Prerequisites
Because this model uses a Python script to fetch data directly into Excel via `xlwings`, you must have both Excel and Python installed.
* **Microsoft Excel:** Macros must be enabled to run the refresh script.
* **Python 3.x:** Installed on your machine.
* **Python Libraries:** Install the required dependencies using pip:
  ```bash
  pip install requests beautifulsoup4 pandas fuzzywuzzy xlwings
  ```

### Setup & Usage Instructions
1. Clone the repository: Download both cfb_model.py and College Football Model.xlsm into the same folder on your computer.
2. Open the Excel file: Launch College Football Model.xlsm.
3. Refresh the Data: Click the "Refresh" button on the dashboard. This triggers the Python script to scrape the latest ESPN and TeamRankings data, match the team names, and push the fresh data directly into the 2025 sheet.
4. **Evaluate the Matchups:** * Look at the **Total Points** column. Remember, this number represents how many stats *do not* meet the baseline criteria. A lower number indicates a more statistically complete team.
     * Use the interface to compare two teams head-to-head based on historical championship data.

## Contributing & Feedback
If you have ideas for new metrics, want to help optimize the Python web scraper, or spot a bug in the calculations, feel free to open an issue or submit a pull request! Let's build the ultimate CFB forecasting community.

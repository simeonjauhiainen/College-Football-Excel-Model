# College-Football-Excel-Model 🏈🏆

> **🏆 2025 Perfect Bracket Achieved!** 
> This Excel-based predictive model successfully forecasted every single matchup and the eventual national champion in the 2025 College Football Playoff.

Welcome to the **College Football Excel Model**. This project is a robust, data-driven forecasting tool built entirely in Microsoft Excel. It uses historical performance, efficiency metrics, and schedule strength to project game outcomes, point spreads, and win probabilities for NCAA Division I FBS college football.

---

## 🌟 The 2025 Perfect Bracket
In the 2025 season, this model achieved something extremely rare: **a 100% accurate prediction of the College Football Playoff bracket.** 

`![2025 Perfect Bracket Screenshot](C:\Users\simeo\OneDrive\Documents\Sports Models\Documentation\CFP Perfect Bracket 2024-25.png)`

**How it did it:**
* Accurately weighed late-season momentum over early-season rankings.
* Identified two lower-seeded "Cinderella" upsets based on offensive line mismatch data.
* Correctly projected the National Championship score within [Insert Margin] points.

---

## 📊 Features & Methodology

This model doesn't just rely on gut feelings. It digests raw data and outputs objective probabilities using the following metrics:

* **Adjusted Offensive/Defensive Efficiency:** Yards per play adjusted for opponent strength.
* **Strength of Record (SOR) & Strength of Schedule (SOS):** Punishing teams with inflated records against weak opponents.
* **Turnover Luck Regression:** Adjusting for teams that heavily over-indexed on fumble recoveries (which are largely random year-to-year).
* **Home-Field Advantage Adjustments:** Dynamically weighted based on stadium capacity and historical travel fatigue.

*(Feel free to edit the metrics above to match your actual secret sauce!)*

---

## ⚙️ How to Use the Model

### Prerequisites
* Microsoft Excel 2016 or newer (Microsoft 365 recommended).
* **Note:** Macros must be enabled if you are using the automated data-fetching buttons.

### Setup Instructions
1. **Download the file:** Clone this repository or download the `CFB_Model_2026.xlsx` file directly.
2. **Open the Dashboard tab:** This is your primary interface. 
3. **Input the Matchup:** Use the dropdown menus in cells `B4` (Away Team) and `B5` (Home Team) to select the teams you want to simulate.
4. **View the Projection:** The dashboard will immediately populate:
   * Projected Winner
   * Win Probability (%)
   * Projected Point Spread
   * Over/Under Total

### Updating the Data
To update the model for the current week, navigate to the `Data_Input` tab and paste the latest raw stats from [Insert Data Source, e.g., CFBD API, ESPN, or your own scraping tool]. The formulas will automatically recalculate.

---

## 🚀 Future Roadmap for 2026

Even with a perfect bracket, the model is always evolving. Planned updates for the upcoming season include:
- [ ] Integrating transfer portal value metrics.
- [ ] Adding real-time weather condition adjustments.
- [ ] Migrating the backend data collection to Python/Pandas to feed the Excel dashboard automatically.

---

## 🤝 Contributing & Feedback
If you have ideas for new metrics or spot a bug in the calculations, feel free to open an issue or submit a pull request! Let's build the ultimate CFB forecasting community.

## 📝 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

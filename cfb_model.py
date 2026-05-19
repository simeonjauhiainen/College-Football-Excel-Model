import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
from fuzzywuzzy import process
import xlwings as xw
import re

def fetch_espn_table(url, column_names, columns_to_keep=None):
    """Fetches and parses a table from an ESPN FPI page."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Will raise an HTTPError for bad responses
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr")

    teams, stats = [], []
    found_stats = False

    for row in rows:
        text = [col.get_text(strip=True) for col in row.find_all("td")]
        if not text:
            continue
        # A simple heuristic to distinguish team rows from stat rows
        first_char = text[0][0] if text[0] else ''
        if first_char.isdigit() or first_char == '-':
            found_stats = True
        
        if found_stats:
            stats.append(text)
        else:
            teams.append(text)
        
    merged_rows = [team[:2] + stat for team, stat in zip(teams, stats)]
    df = pd.DataFrame(merged_rows, columns=column_names)

    if columns_to_keep:
        df = df[columns_to_keep]
    return df

# --- Step 1: Fetch all data from ESPN ---
# Fetch FPI base data
url_fpi = "https://www.espn.com/college-football/fpi/_/season/2025"
fpi_columns = ['Team', 'Conf', 'W-L', 'FPI', 'Rk', 'Trend', 'Proj W-L', 'Win Out%', '6Wins%', 'Win Div%', 'Win Conf%', 'Playoff%', 'Make NC%', 'Win NC%']
base_df = fetch_espn_table(url_fpi, fpi_columns, ['Team', 'Conf', 'W-L', 'FPI'])

# Fetch Resume data
url_resume = "https://www.espn.com/college-football/fpi/_/view/resume/season/2025"
resume_columns = ['Team', 'Conf', 'SOR', 'FPI', 'AP/CFP', 'SOS', 'Rem SOS', 'GC', 'AVGWP']
resume_df = fetch_espn_table(url_resume, resume_columns, ['Team', 'SOS'])

# Merge Resume into FPI
ncaaf = pd.merge(base_df, resume_df, on='Team')

# Fetch Efficiencies data
url_eff = "https://www.espn.com/college-football/fpi/_/view/efficiencies/season/2025"
eff_columns = ['Team', 'Conf', 'Overall Eff', 'Overall Rnk', 'Offense Eff', 'Offense Rnk', 'Defense Eff', 'Defense Rnk', 'Special Teams Eff', 'Special Teams Rnk']
eff_df = fetch_espn_table(url_eff, eff_columns, ['Team', 'Overall Eff', 'Offense Rnk', 'Defense Rnk'])

# Final ESPN merge
ncaaf = pd.merge(ncaaf, eff_df, on='Team')
ncaaf = ncaaf.map(lambda x: re.sub(r'é', 'e', x) if isinstance(x, str) else x)


# --- Step 2: Fetch all stats from TeamRankings ---
# Stat categories to scrape
urls = [
    'third-down-conversion-pct', 'opponent-third-down-conversion-pct', 'penalties-per-game',
    'passing-yards-per-game', 'opponent-passing-yards-per-game', 'opponent-red-zone-scoring-pct',
    'red-zone-scoring-pct', 'opponent-rushing-yards-per-game', 'rushing-yards-per-game',
    'opponent-points-per-game', 'points-per-game', 'average-scoring-margin',
    'average-team-passer-rating', 'opponent-yards-per-game', 'yards-per-game',
    'turnover-margin-per-game'
]

today = date.today()
teamrankings_df = None

for stat in urls:
    url = f'https://www.teamrankings.com/college-football/stat/{stat}?date={today.strftime("%Y-%m-%d")}'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="datatable")
    headers = [th.text.strip() for th in table.find("thead").find_all("th")]
    
    rows = []
    for tr in table.find("tbody").find_all("tr"):
        cells = [td.text.strip() for td in tr.find_all("td")]
        rows.append(cells)
    
    df = pd.DataFrame(rows, columns=headers)
    
    # Dynamically find the latest year column instead of hardcoding '2024'
    year_col = next((col for col in headers if str(today.year) in col), '2025')

    df = df[['Team', year_col]].rename(columns={year_col: stat})
    
    if teamrankings_df is None:
        teamrankings_df = df
    else:
        teamrankings_df = pd.merge(teamrankings_df, df, on='Team', how='outer')

# --- Step 3: Fuzzy Match Team Names and Merge DataFrames ---

# Get the list of "correct" team names from your primary DataFrame (ESPN)
espn_teams = ncaaf['Team'].unique()

# Define a dictionary for manual overrides. 
# Key: TeamRankings name, Value: ESPN name
manual_team_mapping = {
    'Arizona': 'Arizona Wildcats',
    'Buffalo': 'Buffalo Bulls',
    'C Michigan': 'Central Michigan Chippewas',
    'Duke': 'Duke Blue Devils',
    'E Carolina': 'East Carolina Pirates',
    'E Michigan': 'Eastern Michigan Eagles',
    'Florida': 'Florida Gators',
    'Florida Intl': 'Florida International Panthers',
    'Iowa': 'Iowa Hawkeyes',
    'Kansas': 'Kansas Jayhawks',
    'Louisiana': 'Louisiana Ragin\' Cajuns',
    'Miami OH': 'Miami (OH) RedHawks',
    'Mississippi': 'Ole Miss Rebels',
    'N Texas': 'North Texas Mean Green',
    'Ohio': 'Ohio Bobcats',
    'S Alabama': 'South Alabama Jaguars',
    'S Florida': 'South Florida Bulls',
    'San Jose St': 'San Jose State Spartans',
    'Texas': 'Texas Longhorns',
    'Virginia': 'Virginia Cavaliers',
    'W Kentucky': 'Western Kentucky Hilltoppers',
    'W Michigan': 'Western Michigan Broncos',
    'UMass': 'Massachusetts Minutemen'
}

# Create a final mapping from the TeamRankings names to the ESPN names
team_mapping = {}
unmatched_teams = []

for team in teamrankings_df['Team']:
    # First, check if the team is in our manual mapping
    if team in manual_team_mapping:
        team_mapping[team] = manual_team_mapping[team]
    else:
        # If not, use fuzzy matching to find the best fit
        match = process.extractOne(team, espn_teams, score_cutoff=85)
        
        if match:
            team_mapping[team] = match[0]
        else:
            unmatched_teams.append(team)

# Apply the mapping to standardize the team names
teamrankings_df['Team'] = teamrankings_df['Team'].map(team_mapping)
teamrankings_df.dropna(subset=['Team'], inplace=True)


# --- Step 4: Final Merge ---
# Merge the two DataFrames on the now-consistent 'Team' column
final_df = pd.merge(ncaaf, teamrankings_df, on='Team', how='outer').sort_values(by='Team')
final_df.columns = ['Team', 'Conf', 'W-L', 'FPI', 'SOS', 'Total Eff', 'Off Eff', 'Def Eff', '3rd Conv %', '3rd Conv % Def', 'Penalty/GM', 'Pass YPG', 'Opp Pass YPG', 'RZ Def', 'RZ Off', 'Opp Rush YPG', 'Rush YPG', 'Opp PPG', 'PPG', 'Avg MOV', 'Pass Eff', 'Opp YPG', 'YPG', 'TO MAR']
final_df = final_df.replace({
    "--": "-",
})
final_df = final_df.fillna("-")
final_df = final_df.map(lambda x: x.replace("+", "") if isinstance(x, str) else x)
final_df = final_df.sort_values(by='Team', ascending=True)
print(final_df[final_df['Team']=='San Jose State Spartans'])

wb = xw.Book.caller()
# wb = xw.books.open(r"C:\Users\simeo\OneDrive\Documents\Sports Models\College Football Model\College Football Model.xlsm")
sheet = wb.sheets("2025")
sheet["B13"].value = final_df.values
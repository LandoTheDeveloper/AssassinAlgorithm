import random
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = 'assassin-spring-2025-c7276756992d.json'
SPREADSHEET_ID = '1N6L44_3x4J4kkE6NKxoJkO0x74D729jYrhQAA3Au9bE'
SHEET_NAME = 'Data'

def get_sheet_client():
    """Authenticate and return the Google Sheets client."""
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client

def get_sheet_data():
    """Fetch data from the Google Sheet."""
    client = get_sheet_client()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    # Fetch all data
    data = sheet.get_all_records()
    #print("Fetched Data:", data)  # Debug: Print fetched data
    return data

def update_sheet_data(data):
    """Update the Google Sheet with new data."""
    client = get_sheet_client()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    # Clear the sheet and write updated data
    sheet.clear()
    # Write headers (first row)
    headers = ["Player", "Target", "Status", "Paid?", "Submitted Schedule?", "Number of Assassinations"]
    sheet.append_row(headers)
    # Write data rows
    for row in data:
        sheet.append_row([row["Player"], row["Target"], row["Status"], row["Paid?"], row["Submitted Schedule?"], row["Number of Assassinations"]])
    #print("Updated Data:", data)  # Debug: Print updated data

def assign_targets(players):
    """Assign targets to active players."""
    active_players = [player["Player"] for player in players if str(player["Status"]) == "1"]
    print("Active Players:", active_players)  # Debug: Print active players
    if not active_players:
        print("No active players found.")
        return {}
    random.shuffle(active_players)
    assignments = {}
    n = len(active_players)
    for i in range(n):
        assassin = active_players[i]
        target = active_players[(i + 1) % n]
        assignments[assassin] = target
    print("Assignments:", assignments)  # Debug: Print assignments

    # Set target to empty string for eliminated players
    for player in players:
        if str(player["Status"]) == "0":
            player["Target"] = ""
            print(f"Cleared target for eliminated player: {player['Player']}")

    return assignments

def main():
    # Fetch data from Google Sheet
    players = get_sheet_data()
    #print(f"Players: {players}")
    if not players:
        print("No players found in the Google Sheet.")
        return

    # Assign targets
    targets = assign_targets(players)

    # Update player data with targets and increment assassinations if target is eliminated
    for player in players:
        if player["Player"] in targets:
            player["Target"] = targets[player["Player"]]
            print(f"{player['Player']} → {player['Target']}")

            # Check if the target is eliminated (Status is "0")
            target_player = next((p for p in players if p["Player"] == player["Target"]), None)
            if target_player and target_player["Status"] == "0":
                # Increment the assassin's Number of Assassinations
                if player["Number of Assassinations"] == '':
                    player["Number of Assassinations"] = 1  # Initialize if empty
                else:
                    player["Number of Assassinations"] = int(player["Number of Assassinations"]) + 1
                print(f"Incremented assassinations for {player['Player']} (now {player['Number of Assassinations']})")

        if player["Status"] == '0':
            print(f"Eliminated: {player['Player']}")
            player["Target"] = ""  # Clear target for eliminated players

    # Update Google Sheet with new data
    update_sheet_data(players)

if __name__ == "__main__":
    main()
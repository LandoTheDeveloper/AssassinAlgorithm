import random
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = 'assassin-spring-2025-1bbc92be5fbc.json'
SPREADSHEET_ID = '1N6L44_3x4J4kkE6NKxoJkO0x74D729jYrhQAA3Au9bE'
SHEET_NAME = 'Data'

class Player:
    def __init__(self, name, target, status, paid, submitted_schedule, num_assassinations):
        self.name = name
        self.target = target
        self.status = status
        self.paid = paid
        self.submitted_schedule = submitted_schedule
        self.num_assassinations = num_assassinations

    def to_dict(self):
        return {
            "Player": self.name,
            "Target": self.target,
            "Status": self.status,
            "Paid?": self.paid,
            "Submitted Schedule?": self.submitted_schedule,
            "Number of Assassinations": self.num_assassinations
        }

def get_sheet_client():
    """Authenticate and return the Google Sheets client."""
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client

def get_sheet_data():
    """Fetch data from the Google Sheet."""
    client = get_sheet_client()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    data = sheet.get_all_records()
    players = [Player(
        name=row["Player"],
        target=row["Target"],
        status=row["Status"],
        paid=row["Paid?"],
        submitted_schedule=row["Submitted Schedule?"],
        num_assassinations=row["Number of Assassinations"] if row["Number of Assassinations"] else 0
    ) for row in data]
    return players

def update_sheet_data(players):
    """Update the Google Sheet with new data."""
    client = get_sheet_client()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    sheet.clear()
    headers = ["Player", "Target", "Status", "Paid?", "Submitted Schedule?", "Number of Assassinations"]
    sheet.append_row(headers)
    for player in players:
        sheet.append_row([
            player.name, player.target, player.status, player.paid, player.submitted_schedule, player.num_assassinations
        ])

def assign_targets(players):
    """Assign initial targets in a shuffled circular manner."""
    print("Shuffling players...")
    shuffled = players.copy()
    random.shuffle(shuffled)
    n = len(shuffled)
    
    print("Assigning targets...")
    for i in range(n):
        assassin = shuffled[i]
        
        # Check if target is assigned
        current_target_name = assassin.target
        current_target = None
        for player in players:
            if player.name == current_target_name:
                current_target = player
                break
            
        # If target is assigned:
        # If the assassin has an alive target, skip to the next player
        if current_target and str(current_target.status) == "1":
            print(f'{assassin.name} already has a target. Skipping...')
            continue
        
        # If the assassin has no alive target, assign the old targets target as the target
        # This means they assassinated their target
        elif current_target and str(current_target.status) == "0":
            print(f'{assassin.name} assassinated {current_target.name}.')
            
            assassin.num_assassinations += 1
            print(f"{assassin.name} now has {assassin.num_assassinations} eliminations.")
            
            assassin.target = current_target.target
            print(f'{assassin.name} --> {current_target.target}')
            
            current_target.target = ""
            print(f"{current_target.name} is now dead.")
            continue
        
        # If no target is assigned, assign a random target.
        else:
            if str(assassin.status) == "1":
                target = shuffled[(i + 1) % n]
                assassin.target = target.name
                print(f'{assassin.name} --> {target.name}')
            
            # Start of game: Set eliminations to 0
            if str(assassin.status) == "1":
                assassin.num_assassinations = 0
                print(f"{assassin.name}'s eliminations set to 0.")
        

def main():
    players = get_sheet_data()
    if not players:
        print("No players found in the Google Sheet.")
        return 
            
    # Assign active players their targets
    assign_targets(players)
    

    update_sheet_data(players)

if __name__ == "__main__":
    main()
import random
import csv

def assign_targets(active_players):
    """Assign initial targets in a shuffled circular manner."""
    shuffled = active_players.copy()
    random.shuffle(shuffled)
    assignments = {}
    n = len(shuffled)
    for i in range(n):
        assassin = shuffled[i]
        target = shuffled[(i + 1) % n]
        assignments[assassin] = target
    return assignments

def main():
    # Read the CSV file
    with open('db.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        rows = list(csv_reader)
    
    # Check if initial targets are needed
    active_players = []
    needs_initial_targets = False
    for row in rows:
        name, target, status = row[0], row[1], row[2]
        if status == '1':
            active_players.append(name)
            if not target:
                needs_initial_targets = True
    
    if needs_initial_targets:
        # Assign initial targets
        assignments = assign_targets(active_players)
        for row in rows:
            if row[0] in assignments:
                row[1] = assignments[row[0]]
    else:
        # Process eliminations
        eliminated_players = [row for row in rows if row[2] == '0' and row[1]]
        for eliminated_row in eliminated_players:
            eliminated_name = eliminated_row[0]
            eliminated_target = eliminated_row[1]
            
            # Find the assassin (active player targeting eliminated)
            assassin_row = next((r for r in rows if r[1] == eliminated_name and r[2] == '1'), None)
            if assassin_row:
                assassin_row[1] = eliminated_target  # Inherit target
            eliminated_row[1] = ''  # Clear eliminated player's target
    
    # Write updates back to CSV
    with open('db.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)
    
    # Display current targets
    print("Current Targets:")
    for row in rows:
        if row[2] == '1' and row[1]:
            print(f"{row[0]} → {row[1]}")

if __name__ == "__main__":
    main()
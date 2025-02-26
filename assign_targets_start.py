import random


def assign_targets(players):
    # Shuffle list of players
    random.shuffle(players)
    
    # Dict to store assignments
    assignments = {}
    
    # Assign each player the enxt player in the shuffled list
    for i in range(len(players)):
        # The last player gets the first player as their target
        if i == len(players) - 1:
            assignments[players[i]] = players[0]
        else:
            assignments[players[i]] = players[i + 1]
            
            
    return assignments

def main():
    players = ["Jaiden", "Adam", "Cole", "Lilly", 'Evan']
    
    targets = assign_targets(players)
    
    for player, target in targets.items():
        print(f"{player}'s target is {target}")
        
if __name__ == "__main__":
    main()

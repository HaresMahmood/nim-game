"""
`game.py`:
Command-line interface, represents a game of misère Nim.
AI can be modified to user minimax or MCTS.
Game states are represented in the following way:
   * [x, y, z]
      - Where `x`, `y` and `z` are the number of sticks in their
      respective pile, being the index at which they are present
      in the list.

Rules:
   * `x` number of piles with a random number of sticks is
   generated at the start of the game, where `x` is determined
   by the user.
   * The user chooses whether they want to start or not 
   (Player 1 or Player 2).
   * Once the game starts, each player can take up to 3 sticks at
   once from a single pile.
   * The player that has to take the last stick loses.
"""

__author__ = "Hares Mahmood"

import random # Import `random` module.
import minimax as nim # Import minimax functions.
import montecarlo as mc # import monte carlo functions.

"""
    Finds the mising element from a modified list.
"""
def findMissing(original, modified):
    copy = modified.copy() # Make a copy of the modified list.
    for o in original: # For each element in the orignal list, ...
        if o not in copy: # If the element is not found in the modified list, ...
            return original.index(o) # Return the index of the element.
        copy.remove(o) # If it is found, remove the element from te modified list.

"""
    Continuously asks for Integer input from the 
    human player through error handlings.
"""
def getInt(text):
    while True: # Infinite loop...
        try: # Try to...
            intVal = int(input(text)) # ... Get a number from the player, ...
            return intVal # ... And return it.
        except ValueError: # If player's inputs anything other than a number, ...
            continue # Continue with the loop (ask player for a number again).
        except KeyboardInterrupt: # If the player force-exits the application (CTRL + C), ...
            exit() # Exit the application.
        else: # If the player inputs a number, ...
            break # Break out of the loop.

"""
    Checks who's turn it is to play to display
    for the human player's information.
"""
def checkPlayer(state, player):
    return "You" if state[1] == player else "CPU"

def getHumanInput(state):
    while True: # Infinite loop...
        pile = getInt("From pile: ") # Get the pile-index from the player.
        number = getInt("Take: ") # Get the amount of sticks from the player.
        successor = nim.successor(nim.toggle(state), pile - 1, number) # Get the successor of the chosen state.

        if not(successor in nim.successors(state)): # If the chosen state is invalid (is not found in the list of successors from the original state), ...
            print("Invalid move. Please try again.") # Print an error message (ask player for input again).
        else: # If the chosen state is valid, ...
            break # Break out of the loop.

    return successor # Return a valid state.

"""
    Finds out how many sticks were removed and from 
    what pile, for the human player's information.
"""
def getComInput(state, successor):
    if len(state) != len(successor): # If a pile doesn't exist in the successor-state that does in the original-state, ...
        successor.insert(findMissing(state, successor), 0) # Insert an empty pile at the position it is in the original-state, into the successor-state.
    
    difference = [i - j for i, j in zip(state, successor)] # Subtract the successor-state from the original-state to see how many sticks have been removed and from what pile.
    sticks  = list((s for s in difference if s != 0))[0] # Take element that isn't equal to `0`, as that is the pile that has sticks taken away from.
    pile = difference.index(sticks) + 1 # Get the index of the pile that has the sticks taken away from.

    print(f"From pile {pile}\nTake {sticks}") # Print information.

"""
    Initializes and plays out a Nim game between a human
    and AI player.
"""
def game(isMontecarlo):
    # Print information.
    print("===============\n      Nim\n===============")
    print("===============\n  Game setup:\n===============\n")
    piles = getInt("Number of piles: ") # Get number of piles.
    sticks = getInt("Max sticks per pile: ") # Get maximum number of sticks per pile.
    player = getInt("Player 1 or Player 2? [1/2]: ") # Ask if human player wants to play first or second.

    state = tuple([[random.randrange(1, sticks) for i in range(piles)], 1]) # State with random amount of sticks.

    while not(nim.terminal(state)): # While the game hasn't ended, ...
        current = checkPlayer(state, player) # "Check" who's turn it is to play.

        # Print information.
        print("\n===============\nPlayer {0} ({1}):\n===============".format(state[1], checkPlayer(state, player)))
        print(f"State: {state[0]}\n")

        if state[1] == player: # If it's the human player's turn, ...
            state = getHumanInput(state) # Get values from player and assign them to `state`.
        else: # If it's the computer player's turn, ...
            value = None
            if isMontecarlo == True:
                value = mc.montecarlo_value(state)
            else:
                _, path = nim.minimax_value(state) # Get values.
                value = path[0]

            getComInput(state[0].copy(), value[0].copy()) # Print information for human player.

            state = value # Assign computer's chosen move to `state`.

    print("\n===============\n   Game set:\n===============\nWinner: Player {0} ({1}).".format(state[1], checkPlayer(state, player))) # Print information.

    

game(False) # Start game.
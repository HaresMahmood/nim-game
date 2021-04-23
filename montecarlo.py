"""
`montecarlo.py`:
General-purpose Monte Carlo Search Tree "algorithm".
Uses some functions from `minimax.py` for actions specific
to the game of Nim.

MCTS does not have time complexity, because the search can
be stopped at any time, and by default only runs for a 
certain amount of iterations.
"""

__author__ = "Hares Mahmood"

import random # Import `random` module.
import math # Import `math` module.
from collections import defaultdict # Import `defaultdict` module, to avoid having to check if item is in dictionary or not.
import minimax as nim # Import previously defined Nim functions.

rewards = defaultdict(int) # Total reward of each state.
visits = defaultdict(int) # Total number of visits for each state.
children = dict() # Children of each state.
player = 0 # Whether AI is player 1 or player 2.

"""
    Converts a state with a list of piles to a state with
    a tuple of piles.
"""
def tupleState(state):
    piles = tuple(state[0]) # Convert piles into a tuple.

    return (piles, state[1])

"""
    Converts a state with a tuple of piles to a state with
    a list of piles.
"""
def listState(state):
    piles = list(state[0]) # Convert piles into a list.

    return (piles, state[1])

"""
    Determines the utility value of a (terminal) state.
"""
def utility(state):
    return 1 if (state[1] != player) else 0 # Return `1` for win, `0` for loss.

"""
    Returns a random successor to the given state.
"""
def random_succcessor(state):
    # Return a random successor from the list of successors if the state is not a terminal state. Else, return `None`.
    return None if nim.terminal(state) else random.choice(nim.successors(listState(state), False))

"""
    Chooses the best successor for a state.
"""
def choose(state):
    if state not in children:
        return random_succcessor(state)

    def score(n):
        return float("-inf") if visits[n] == 0 else rewards[n] / visits[n]

    return max(children[state], key = score)

"""
    Finds an unexplored successor of the given state.
"""
def select(state):
    path = []

    while True: # Infinte loop...
        path.append(state)

        if state not in children or not children[state]: # If state is either unexplored, or terminal,...
            return path

        unexplored = children[state] - children.keys() # Get all unexplored states.

        if unexplored: # If there are unexplored states, ...
            path.append(unexplored.pop()) # Remove it from the `unexplored` list and add it to the path.
            
            return path

        # If no unexplored state has been found, ...
        state = uct(state) # ... Select a state from a deeper layer.

"""
    Select a successor by balancing exploration & exploitation.
"""
def uct(state):
    def formula(n):
        multiplier = 1 if state[1] != player else -1 # Negate exploitation value if it's the opponent's turn.
        exploitation = (rewards[n] / visits[n]) * multiplier # Forumula for exploitation (Number of wins divided by total reward).
        exploration = math.sqrt(math.log(visits[n]) / visits[n]) # Forumla for exploration (square root of log of number of simulations divided by total reward).

        return exploitation + exploration # Add up exploitation and exploration values.

    return max(children[state], key = formula) # Choose the successor state with the highest uct value.

"""
    Updates the `children` dictionary with the children of 
    the given state.
"""
def expand(state):
    if not (state in children): # If `state` is not a key in `children`, ...
        children[state] = nim.successors(listState(state), False) # Add the state as a key, aslong with its successors as its value.

"""
    Get the utility of a fully played-out game from the given 
    state to completion. 
"""
def simulate(state):
    invert_reward = True # Should the rewqrd be rewarded?

    while True: # Infinite loop...
        if nim.terminal(state): # If `state` is a terminal state, ...
            reward = utility(state) # Get its reward.
            return 1 - reward if invert_reward else reward # Invert the reward depending on who's playing - the virtual opponent or the AI's.

        state = random_succcessor(state) # Select a random successor.

        invert_reward = not invert_reward # Invert the reward

"""
    Sends the reward back to the parents of the state.
"""
def backpropagate(path, reward):
    for node in reversed(path): # For every state from parent to child in the path, ...
        visits[node] += 1 # Increment the times it's been visitied.
        rewards[node] += reward # Increase its reward.
        reward = 1 - reward  # Invert the reward.

"""
    Does Monte Carlo rollouts for the given number of 
    cycles and returns the optimal value afterwards.
"""
def montecarlo_value(state, cycles = 5000):
    state = tupleState(state) # Convert list state into a tuple.
    player = state[1] # Determine whether the AI player is player 1 or player 2.

    for _ in range(cycles):
        # Train for 1 iteration.
        path = select(state) # Get the path.   
        successor = path[-1] # Get the state at the end of the path.
        
        expand(successor) # Expand the successor.
        backpropagate(path, simulate(successor)) # Backpropogate the successor's value.
    
    return listState(choose(state)) # Return the best state.
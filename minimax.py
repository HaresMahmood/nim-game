"""
Pseudo code (https://en.wikipedia.org/wiki/Alpha-beta_pruning#Pseudocode):
function minimax(state, alpha, betal isMax) is
    if terminal(state) then
        return utility(state)

    multiplier = isMax ? -1 : 1
    value := multiplier * ∞

    for c in successors(states) do
        value := isMax ? max(value, minimax(c, alpha, beta, !isMax)) : min(value, minimax(c, alpha, beta, !isMax))

        if (isMax) then
            alpha = max(alpha, value)

            if (alpha >= beta) then
                break
        else
            beta = min(beta, value)

            if (beta <= alpha) then
                break

    return value
"""

"""
    Switches a Max-state to a Min-state, and vice versa.
"""
def toggle(state):
    state = list(state) # Convert tuple to list.
    state[1] = 2 if (state[1] == 1) else 1 # Edit values.
    state = tuple(state) # Convert list back to tuple.

    return state

"""
    Returns the successor of a given state, according to
    given values.
"""
def successor(state, index, amount, isList = True):
    piles = state[0].copy() if isList else list(state[0]).copy()

    if index > len(piles): # If the amount of sticks to remove is larger than the amount of sticks in the pile, ...
        return None # ... Don't remove any sticks, and return `None`.

    if piles[index] >= 1: # If there is at least `1` stick in the pile, ...
        piles[index] -= amount # ... Only remove stick(s) from pile.

    if piles[index] < 1: # If removing sticks from the pile results in the pile having a negative or `0` value, ...
        piles.pop(index) # Remove pile from state.

    state = list(state) # Convert tuple to list.
    state[0] = piles.copy() if isList else tuple(piles) # Add list of piles to tuple.
    state = tuple(state) # Convert list back to tuple.
    
    return state # Return state.

"""
    Returns a list of successors for a given state.
"""
def successors(state, isList = True):
    successors = [] # List to hold successor states.

    state = toggle(state) # Toggle player.

    for i in range(len(state[0])): # From each pile, ...
        for j in range(1, 4): # ... Remove 1, 2, and 3 sticks.
            successors.append(successor(state, i, j, isList)) # Add successor state to list.
    
    temp = []
    [temp.append(s) for s in successors if s not in temp] # Remove duplicates.
    successors = temp.copy();

    return successors


"""
    Determines whether a state is a terminal state.
"""
def terminal(state):
    return len(state[0]) == 0; # Return whether list of piles is empty.

"""
    Determines the utility value of a (terminal) state.
"""
def utility(state):
    return 1 if (state[1] == 1) else -1 # Return `1` for Max, `-1` for Min.



"""
    Determines the Minimax-value of state.
"""
def minimax_value(state, alpha = -float('inf'), beta = float('inf')):
    path = [] # Initialize an empty list.

    if terminal(state): # If `state` is a terminal-state, ...
        return utility(state), path # Return the utility-value (`1`/`-1`), and an empty list for path.
    
    multiplier = -1 if (state[1] == 1) else 1 # `-∞` for Max, `+∞` for Min.
    value = multiplier * float('inf') # Apply multiplier to `∞`.

    for c in successors(state): # For each successor, ...
        bestValue, newPath = minimax_value(c, alpha, beta) # Get successor's Minimax-value.
        bestValue = max(value, bestValue) if (state[1] == 1) else min(value, bestValue) # Use `max()` or `min()` depending if `c` is a Max- or Min-state.

        # Recurisvely append successors to `path`, if certain conditions are met (which are specific to Max- and Min-states), which build up the optimal play-path.
        if (state[1] == 1 and bestValue > value) or (state[1] == 2 and bestValue < value): path = [c] + newPath 

        value = bestValue # Assign `bestValue` to `value`, after we've checked which one is `max()` or `min()`.

        alpha = max(alpha, value) if (state[1] == 1) else alpha # Assign (new) `alpha`-value, if `c` is a Max-state.
        beta = min(beta, value) if (state[1] == 2) else beta # Assign (new) `beta`-value, if `c` is a Min-state.

        if (state[1] == 1 and alpha >= beta) or (state[1] == 2 and beta <= alpha): break # Prune based on whether `alpha` or `beta` is bigger, depending on whether `c` is a Max- or Min-state.

    return value, path # Return Minimax-value, along with the path.
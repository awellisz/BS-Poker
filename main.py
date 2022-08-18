import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from random import sample
import itertools

plt.rcParams["figure.figsize"] = (12,8)
plt.rcParams['figure.dpi'] = 300

# two, three, four, five, six, seven, eight, nine, ten, jack, queen, king, ace
# For simplicity later on (card comparison), it is easier for aces to be 14
numbers = [i for i in range(2, 15)]
deck = list(np.repeat(numbers, 4))

def shuffle(d, n):
    """
    Utility function
    Returns a hand (list) of length n with random cards from deck d
    """
    return sample(d, n)
  
def contains_all(a, b):
    """
    Utility function
    Check if array A contains all elements of B, including with repeated values.
    E.g. containsall([11, 4, 6], [4, 4]) -> False
    E.g. containsall([11, 4, 6], [6, 11]) -> True
    """
    counter_a = Counter(a)
    counter_b = Counter(b)
    return all(v <= counter_a[k] for k, v in counter_b.items())
  
def remove_match(hand, match):
    """
    Utility function
    Remove the list 'match' from the list 'hand'
    E.g. remove_match([3, 6, 8, 1, 1], [1, 6]) -> [3, 8, 1]
    (actually returns a Counter object instead of a list but example is just for clarity,
    the returned object effectively functions as a list in the hand-checking functions below)
    """
    new_hand = Counter(hand)
    new_hand.subtract(Counter(match))
    return new_hand
  
def high(hand, c):
    """
    Return whether or not the hand contains the given card (integer)
    """
    # Two's Wild
    return (2 in hand) or (c in hand)
  
def pair(hand, c):
    """
    Given a hand (np array), return whether or not it contains a pair of the given card (integer)
    """
    # All possible ways to have a pair
    matches = [[c, c], [c, 2], [2, 2]]
    
    for match in matches:
        if contains_all(hand, match):
            return True
    return False
  
def twopair(hand, c):
    """
    Given a hand, return whether or not it contains two pairs, the higher of which is of the given card 
    """
    # All possible ways to have a pair
    pair_matches = [[c, c], [c, 2], [2, 2]]
    
    # I'm sure there's a way to restructure pair() to not have to re-type this logic, but
    #   this works just fine, I think.
    for match in pair_matches:
        if contains_all(hand, match):
            # Subtract the match (most importantly, subtract the twos) from the hand
            new_hand = remove_match(hand, match)
            # Check if there is a pair of any lower card
            for i in range(2, c):
                if pair(new_hand, i):
                    return True
    return False
  
def threeok(hand, c):
    """
    Given a hand, return true if 3-of-a-kind of the given card exists
    """
    matches = [[c, c, c], [c, c, 2], [c, 2, 2], [2, 2, 2]]
    for match in matches:
        if contains_all(hand, match):
            return True
    return False
  
def straight(hand, card):
    """
    Return true if there's a straight to the given card
    """
    if (card < 6) or (len(hand) < 5):
        return False
   
    # Could automate by filling in all permutations of 0, 1, 2, 3, 4 deuces in 5 spots and fill the open spots w/ corresponding a/b/c/d/e
    # Total number of matches:
    # 1 + 5C1 + 5C2 + 5C3 + 5C4 = 1 + 5 + 10 + 10 + 5 = 31
    # Definitely will have to automate this for longer straights (TODO!)
    a, b, c, d, e = card, card-1, card-2, card-3, card-4
    matches = [[a,b,c,d,e], # no 2s
               [a,b,c,d,2], [a,b,c,2,e], [a,b,2,d,e], [a,2,c,d,e], [2,b,c,d,e], # one 2
               [a,b,c,2,2], [a,b,2,d,2], [a,2,c,d,2], [2,b,c,d,2], [a,b,2,2,e], # two 2s
               [a,2,c,2,e], [2,b,c,2,e], [a,2,2,d,e], [2,b,2,d,e], [2,2,c,d,e], 
               [a,b,2,2,2], [2,b,c,2,2], [2,2,c,d,2], [2,2,2,d,e], [a,2,2,2,e], # three 2s
               [2,b,2,d,2], [2,2,c,2,e], [a,2,2,d,2], [2,b,2,2,e], [a,2,c,2,2], 
               [2,2,2,2,e], [a,2,2,2,2], [2,b,2,2,2], [2,2,c,2,2], [2,2,2,2,e]] # four 2s
    
    for match in matches:
        if contains_all(hand, match):
            return True
    return False
  
def fullhouse(hand, c):
    """
    Return true if there is a full house where the given card c is the three of a kind
    """
    if (len(hand) < 5):
        return False
    
    threeok_matches = [[c, c, c], [c, c, 2], [c, 2, 2], [2, 2, 2]]
    
    for match in threeok_matches:
        if contains_all(hand, match):
            # Subtract the match (most importantly, subtract the twos) from the hand
            new_hand = remove_match(hand, match)
            # Test pairs of any other card
            for i in itertools.chain(range(2, c), range(c + 1, 15)):
                if pair(new_hand, i):
                    return True
    return False
  
def fourok(hand, c):
    """
    Return true if there is a four of a kind of the given card
    """
    # All possible fours of a kind
    # Probably some way to automate this but it's simple enough to hardcode
    matches = [[c, c, c, c], [c, c, c, 2], [c, c, 2, 2], [c, 2, 2, 2], [2, 2, 2, 2]]
    
    for match in matches:
        if contains_all(hand, match):
            return True
    return False
  
def evens(hand, c):
    """
    Return true if there's evens of the given card (i.e. four of a kind + any pair)
    """
    if (len(hand) < 6):
        return False
    
    fourok_matches = [[c, c, c, c], [c, c, c, 2], [c, c, 2, 2], [c, 2, 2, 2], [2, 2, 2, 2]]
    for match in fourok_matches:
        if contains_all(hand, match):
            new_hand = remove_match(hand, match)
            for i in itertools.chain(range(2, c), range(c + 1, 15)):
                if pair(new_hand, i):
                    return True
    return False
  
def fullerhouse(hand, c):
    """
    Return true if there's a fuller house of the given card (four of a kind of the card + three of a kind of any other card)
    """
    if (len(hand) < 7):
        return False
    
    fourok_matches = [[c, c, c, c], [c, c, c, 2], [c, c, 2, 2], [c, 2, 2, 2], [2, 2, 2, 2]]
    for match in fourok_matches:
        if contains_all(hand, match):
            new_hand = remove_match(hand, match)
            for i in itertools.chain(range(2, c), range(c + 1, 15)):
                if threeok(new_hand, i):
                    return True
    return False
  
def fiveok(hand, c):
    """
    Return true if five of a kind
    """
    if (len(hand) < 5):
        return False
    
    matches = [[c, c, c, c, 2], [c, c, c, 2, 2], [c, c, 2, 2, 2], [c, 2, 2, 2, 2]]
    for match in matches:
        if contains_all(hand, match):
            return True
    return False
  
def odds(hand, c):
    """
    Return true if odds (five of a kind of the given card + three of a kind of any other card)
    """
    if (len(hand) < 8):
        return False
    
    fiveok_matches = [[c, c, c, c, 2], [c, c, c, 2, 2], [c, c, 2, 2, 2], [c, 2, 2, 2, 2]]
    for match in fiveok_matches:
        if contains_all(hand, match):
            new_hand = remove_match(hand, match)
            for i in itertools.chain(range(2, c), range(c + 1, 15)):
                if threeok(new_hand, i):
                    return True
    return False
  
def fullesthouse(hand, c):
    """
    Return true if fullest house of the card (five of a kind + four of a kind of any other)
    """
    if (len(hand) < 9):
        return False
    
    fiveok_matches = [[c, c, c, c, 2], [c, c, c, 2, 2], [c, c, 2, 2, 2], [c, 2, 2, 2, 2]]
    for match in fiveok_matches:
        if contains_all(hand, match):
            new_hand = remove_match(hand, match)
            for i in itertools.chain(range(2, c), range(c + 1, 15)):
                if fourok(new_hand, i):
                    return True
    return False
  
def sixok(hand, c):
    """
    Return true if six of a kind of given card
    """
    if (len(hand) < 6):
        return False
    
    matches = [[c, c, c, c, 2, 2], [c, c, c, 2, 2, 2], [c, c, 2, 2, 2, 2]]
    for match in matches:
        if contains_all(hand, match):
            return True
    return False
  
def brimminghouse(hand, c):
    """
    Return true if brimming house of the given hand (6 of a kind + 4 of a kind of any other card)
    """
    
    if (len(hand) < 10):
        return False
    
    sixok_matches = [[c, c, c, c, 2, 2], [c, c, c, 2, 2, 2], [c, c, 2, 2, 2, 2]]
    for match in sixok_matches:
        if contains_all(hand, match):
            new_hand = remove_match(hand, match)
            for i in itertools.chain(range(2, c), range(c + 1, 15)):
                if fourok(new_hand, i):
                    return True
    return False
  
def sevenok(hand, c):
    """
    Return true if 7 of a kind of given card
    """
    if (len(hand) < 7):
        return False
    
    matches = [[c, c, c, c, 2, 2, 2], [c, c, c, 2, 2, 2, 2]]
    for match in matches:
        if contains_all(hand, match):
            return True
    return False
  
def eightok(hand, c):
    """
    Return true if 8 of a kind of given card
    """
    if (len(hand) < 8): 
        return False

    match = [c, c, c, c, 2, 2, 2, 2]
    return contains_all(hand, match)
  
def simulate(handsize, iterations, out = False):
    """
    Run a simulation of the specified number of iterations with hands of the specified size
    """
    
    ns = np.zeros(16)
    probs = np.zeros(16)
    funcs = [high, pair, twopair, threeok, straight, fullhouse, fourok, evens, fullerhouse, 
             fiveok, odds, fullesthouse, sixok, brimminghouse, sevenok, eightok]
    # For printing
    names = ["High card      ", 
             "Pair           ", 
             "Two pair       ", 
             "Three of a kind", 
             "Straight       ", 
             "Full house     ", 
             "Four of a kind ",
             "Evens          ", 
             "Fuller house   ", 
             "Five of a kind ", 
             "Odds           ", 
             "Fullest house  ", 
             "Six of a kind  ", 
             "Brimming house ",
             "Seven of a kind", 
             "Eight of a kind"]
    
    for i in range(iterations):
        hand = shuffle(deck, handsize)
        # Check whether there is each hand (highcard, pair, etc.) for each possible card, 2 - 14
        for c in range(2, 15):
            # Iterate over all the checking functions and update the counters (ns) if the check returns true
            for idx, func in enumerate(funcs):
                if func(hand, c):
                    ns[idx] += 1
   
    # This whole part is messy but doesn't really matter
    if out:
        print(f"Iterations: {iterations}")
        print("      Hand        |   Raw occurrences   | Normalized Occurrences | Probability")
    for i in range(16):
        # There are only 9 possible straights, not 13
        if (i == 4):
            probs[i] = ns[i] / (9 * iterations)
            if out:
                print(f"{names[i]}       {ns[i]}                    {ns[i]/9}      {probs[i]}")
            continue
        probs[i] = ns[i] / (13 * iterations)
        if out:
            print(f"{names[i]}       {ns[i]}                    {ns[i]/13}      {probs[i]}")
    return probs
        
    
# On my laptop (Thinkpad T480s) it takes ~500ms to run 100 iterations on 30-card hands and about ~270ms to run 100 iterations on 6-card hands.
# Look into njit with Numba 

# PLOT

# 27 possible hand sizes from 6 to 30, assuming minimum of 4 players and maximum of 6
handsizes = np.arange(4, 31, 1)
handsize_probs = []
iterations = 100

for i in range(27):
    probs = simulate(handsizes[i], iterations)
    handsize_probs.append(probs)

handsize_probs = np.asarray(handsize_probs)

names = ["High card", "Pair", "Two pair", "Three of a kind", "Straight", "Full house", "Four of a kind",
         "Evens", "Fuller house", "Five of a kind", "Odds", "Fullest house", "Six of a kind", 
         "Brimming house","Seven of a kind", "Eight of a kind"]

for i in range(16):
    plt.plot(handsizes, handsize_probs[:, i], label = names[i])
plt.legend()
plt.xlabel("Total Number of Cards in Play")
plt.ylabel("Probability")
plt.title("BS Poker: The Probability that the hand of a given card exists among all cards in play")
plt.show()

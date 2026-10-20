"""
Module M4: Recommendation Engine (Current vs Redesign)
Student: N. Somasekhar Naidu | Reg No: 192472347 | Seed: 2347
"""

def recommendation_current_sim(n):
    """
    Current design: T(n) = 4T(n/2) + n
    Closed form for T(1) = 1: T(n) = 2n^2 - n
    """
    return 2 * (n ** 2) - n

def recommendation_redesign_sim(n):
    """
    Proposed redesign: T(n) = 2T(n/2) + n
    Closed form for T(1) = 1: T(n) = n log2(n) + n
    """
    import math
    return n * math.log2(n) + n

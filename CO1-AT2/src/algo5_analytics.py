"""
Module M5: Sales Analytics Engine & Nightly Report Generator
Student: N. Somasekhar Naidu | Reg No: 192472347 | Seed: 2347
"""

import math

def analytics_engine_sim(n):
    """
    Analytics recurrence: T(n) = 2T(n/2) + n log2(n)
    Solution: T(n) = 0.5 * n * (log2 n)^2 + 0.5 * n * log2 n + n
    """
    log_n = math.log2(n)
    return 0.5 * n * (log_n ** 2) + 0.5 * n * log_n + n

def report_generator_cost(n):
    """
    Report generator: f(n) = 3n^2 + 10n log2(n) + 50
    """
    log_n = math.log2(n)
    return 3 * (n ** 2) + 10 * n * log_n + 50

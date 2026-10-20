"""
Algorithm 1: Iterative Linear Search (Sequential Brute-Force Scanning)
Student: N. Somasekhar Naidu | Reg No: 192472347 | Seed: 2347
"""

def linear_search(records, target_reg_no):
    comparisons = 0
    for record in records:
        comparisons += 1
        if record.reg_no == target_reg_no:  # BASIC OPERATION
            return record, comparisons
    return None, comparisons

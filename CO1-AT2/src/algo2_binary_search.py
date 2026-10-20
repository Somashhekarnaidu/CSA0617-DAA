"""
Algorithm 2: Recursive Binary Search (Divide-and-Conquer)
Student: N. Somasekhar Naidu | Reg No: 192472347 | Seed: 2347
"""

def binary_search_recursive(records, target_reg_no, low=0, high=None, comps=0):
    if high is None:
        high = len(records) - 1
        
    if low > high:
        return None, comps  # Base Case: Key absent
        
    mid = low + (high - low) // 2
    comps += 1
    
    if records[mid].reg_no == target_reg_no:  # BASIC OPERATION
        return records[mid], comps
    elif target_reg_no < records[mid].reg_no:
        return binary_search_recursive(records, target_reg_no, low, mid - 1, comps)
    else:
        return binary_search_recursive(records, target_reg_no, mid + 1, high, comps)

def binary_search_iterative(records, target_reg_no):
    low = 0
    high = len(records) - 1
    comps = 0
    while low <= high:
        mid = low + (high - low) // 2
        comps += 1
        if records[mid].reg_no == target_reg_no:
            return records[mid], comps
        elif target_reg_no < records[mid].reg_no:
            high = mid - 1
        else:
            low = mid + 1
    return None, comps

"""
dataset_generator.py
====================
Synthetic Student Record Generator for DAA Assignment 1.
University Student Record Retrieval System.

Student Details:
- Name: Somashekar Naidu
- Registration Number: 192472347
- Random Seed: 2347 (Last 4 digits of Registration Number: 192472347)
"""

import random
import time
from dataclasses import dataclass
from typing import List, Tuple

# Student Identity Configuration
STUDENT_REG_NO = 192472347
STUDENT_NAME = "Somashekar Naidu"
SEED = int(str(STUDENT_REG_NO)[-4:])  # 2347

FIRST_NAMES = [
    "Aarav", "Aditi", "Akhil", "Ananya", "Bhavya", "Chaitanya", "Deepak",
    "Divya", "Gautam", "Harini", "Ishaan", "Janani", "Karthik", "Kavya",
    "Madhav", "Meera", "Naveen", "Niharika", "Pranav", "Pooja", "Rahul",
    "Rithanya", "Sanjay", "Sneha", "Tarun", "Varun", "Vignesh", "Yamini"
]

LAST_NAMES = [
    "Naidu", "Sharma", "Reddy", "Iyer", "Patel", "Verma", "Rao", "Nair",
    "Kumar", "Singh", "Chowdhury", "Pillai", "Menon", "Bhat", "Gupta"
]

DEPARTMENTS = ["CSE", "ECE", "EEE", "MECH", "CIVIL", "IT", "AIDS", "CSBS"]

@dataclass
class StudentRecord:
    reg_no: int
    name: str
    dept: str
    cgpa: float
    semester: int

    def __repr__(self):
        return f"StudentRecord(reg_no={self.reg_no}, name='{self.name}', dept='{self.dept}', cgpa={self.cgpa:.2f}, sem={self.semester})"


def generate_dataset(n: int, seed: int = SEED, ensure_student_present: bool = True) -> List[StudentRecord]:
    """
    Generates a deterministic dataset of `n` unique StudentRecord objects.
    Guarantees that `STUDENT_REG_NO` is present in the dataset.
    """
    random.seed(seed)
    
    # Generate unique registration numbers in the range 100,000,000 to 999,999,999
    # reserving space for the student's own registration number
    reg_set = set()
    if ensure_student_present:
        reg_set.add(STUDENT_REG_NO)
    
    # Efficiently generate remaining unique keys
    while len(reg_set) < n:
        needed = n - len(reg_set)
        # Sample in batches for high performance up to 1,000,000
        batch = random.sample(range(100000000, 999999999), min(needed * 2, 500000))
        reg_set.update(batch)
        if len(reg_set) > n:
            # Trim excess while preserving STUDENT_REG_NO
            reg_list = list(reg_set)
            if STUDENT_REG_NO in reg_list:
                reg_list.remove(STUDENT_REG_NO)
                reg_list = reg_list[:n-1]
                reg_list.append(STUDENT_REG_NO)
            else:
                reg_list = reg_list[:n]
            reg_set = set(reg_list)
            break

    reg_numbers = list(reg_set)
    # Shuffle so that the student record isn't trivially at the beginning or end
    random.shuffle(reg_numbers)

    records = []
    for reg in reg_numbers:
        if reg == STUDENT_REG_NO:
            name = STUDENT_NAME
            dept = "CSE"
            cgpa = 9.45
            semester = 5
        else:
            name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            dept = random.choice(DEPARTMENTS)
            cgpa = round(random.uniform(6.5, 9.9), 2)
            semester = random.randint(1, 8)
        
        records.append(StudentRecord(reg, name, dept, cgpa, semester))

    return records


if __name__ == "__main__":
    print("=" * 70)
    print(f"DAA Assignment 1: Dataset Generator Verification")
    print(f"Student: {STUDENT_NAME} | Reg No: {STUDENT_REG_NO} | Seed: {SEED}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    for test_n in [1000, 10000]:
        t0 = time.perf_counter()
        ds = generate_dataset(test_n)
        t_gen = time.perf_counter() - t0
        found = any(r.reg_no == STUDENT_REG_NO for r in ds)
        print(f"[N = {test_n:7d}] Generated in {t_gen:.4f}s | Student Record Present: {found}")
        
    sample = [r for r in ds if r.reg_no == STUDENT_REG_NO][0]
    print(f"Sample Student Record: {sample}")

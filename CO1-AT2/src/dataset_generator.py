"""
ShopSphere Dataset Generator
Student: N. Somasekhar Naidu | Reg No: 192472347 | Seed: 2347
"""

import random

class StudentRecord:
    __slots__ = ['reg_no', 'name', 'dept', 'cgpa', 'sem']
    def __init__(self, reg_no, name, dept, cgpa, sem):
        self.reg_no = reg_no
        self.name = name
        self.dept = dept
        self.cgpa = cgpa
        self.sem = sem

    def __repr__(self):
        return f"StudentRecord(reg_no={self.reg_no}, name='{self.name}', dept='{self.dept}', cgpa={self.cgpa}, sem={self.sem})"

def generate_dataset(n, seed=2347):
    random.seed(seed)
    records = []
    
    # Anchor Student Record at index 0
    records.append(StudentRecord(192472347, "Somasekhar Naidu", "CSE", 9.45, 5))
    
    first_names = ["Aarav", "Aditi", "Bhavya", "Chirag", "Divya", "Eshan", "Farhan", "Gaurav", "Harini", "Ishaan", "Karthik", "Lavanya", "Manoj", "Naveen", "Pooja", "Rahul", "Sneha", "Tarun", "Varun", "Yukta"]
    last_names = ["Reddy", "Sharma", "Verma", "Patel", "Kumar", "Iyer", "Rao", "Nair", "Das", "Gupta", "Naidu", "Chowdhury", "Mishra", "Joshi", "Bhat"]
    departments = ["CSE", "ECE", "EEE", "MECH", "CIVIL", "IT", "AIDS"]
    
    # Generate unique 9-digit registration numbers starting with 1924...
    base_id = 192400000
    used_ids = {192472347}
    
    for i in range(1, n):
        reg = base_id + i
        if reg == 192472347:
            reg = base_id + n + 100
        used_ids.add(reg)
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        dept = random.choice(departments)
        cgpa = round(random.uniform(6.50, 9.95), 2)
        sem = random.randint(1, 8)
        records.append(StudentRecord(reg, name, dept, cgpa, sem))
        
    return records

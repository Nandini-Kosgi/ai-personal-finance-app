import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

CATEGORIES = {
    "income": ["Salary", "Bonus", "Freelance", "Refund"],
    "expense": ["Groceries", "Restaurants", "Rent", "Utilities", "Transport",
                "Healthcare", "Insurance", "Education", "Travel", "Shopping",
                "Entertainment", "Subscriptions", "Taxes", "Gifts"]
}

def random_date(start, end, rng):
    delta = end - start
    return start + timedelta(seconds=rng.integers(0, int(delta.total_seconds())))

def generate_transactions(n=10000, seed=123):
    rng = np.random.default_rng(seed)
    start = datetime(2022,1,1)
    end = datetime(2024,12,31,23,59,59)

    rows = []
    for i in range(n):
        is_income = rng.random() < 0.2  # 20% incomes
        if is_income:
            category = rng.choice(CATEGORIES["income"])
            amount = float(np.round(rng.normal(3000, 1200), 2))
            amount = max(500.0, amount)
            ttype = "income"
            desc = f"{category} payment"
        else:
            category = rng.choice(CATEGORIES["expense"])
            base = {
                "Groceries": (120,40),
                "Restaurants": (45,25),
                "Rent": (1400,100),
                "Utilities": (160,60),
                "Transport": (35,20),
                "Healthcare": (90,120),
                "Insurance": (110,35),
                "Education": (200,180),
                "Travel": (350,200),
                "Shopping": (120,90),
                "Entertainment": (60,40),
                "Subscriptions": (20,10),
                "Taxes": (600,400),
                "Gifts": (75,50),
            }[category]
            amount = float(np.round(np.abs(rng.normal(base[0], base[1])) + 1, 2))
            ttype = "expense"
            desc = f"{category} expense"
        date = random_date(start, end, rng)
        rows.append({
            "id": i+1,
            "date": date,
            "description": desc,
            "category": category,
            "amount": amount,
            "type": ttype,
            "account": rng.choice(["Checking","Credit Card","Savings"]),
            "merchant": rng.choice(["Amazon","Target","Walmart","Local Store","Employer","Airline","Utility Co."]),
            "tags": rng.choice(["", "family", "work", "recurring"]),
            "city": rng.choice(["Pittsburgh","Milwaukee","Chicago","Austin","Phoenix","Remote"]),
            "state": rng.choice(["PA","WI","IL","TX","AZ","NA"]),
        })
    df = pd.DataFrame(rows).sort_values("date")
    return df

if __name__ == "__main__":
    df = generate_transactions()
    df.to_csv("data/transactions_large.csv", index=False)
    print("Wrote data/transactions_large.csv", len(df))

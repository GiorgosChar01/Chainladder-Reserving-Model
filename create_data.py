import pandas as pd

def generate_dummy_claims(csv_filepath="dummy_claims.csv", accident_years=(2021, 2022, 2023),
                           base_paid=1000, decay=0.45, growth=0.15, seed=42):
    """
    Generates a synthetic incremental-paid-claims dataset laid out as a
    triangle (AccidentYear x DevelopmentYear) and writes it to CSV.

    Each accident year starts around `base_paid` (scaled up by `growth` per
    year to mimic exposure/inflation growth) and each later development
    period pays out roughly `decay` of the prior period, tapering off - a
    simple, deterministic stand-in for real claims development.
    """
    rows = []
    for i, year in enumerate(accident_years):
        year_base = base_paid * ((1 + growth) ** i)
        n_periods = len(accident_years) - i  # standard triangle shape
        payment = year_base
        for dev in range(1, n_periods + 1):
            rows.append({
                "AccidentYear": year,
                "DevelopmentYear": dev,
                "IncrementalPaid": round(payment)
            })
            payment *= decay

    df = pd.DataFrame(rows)
    df.to_csv(csv_filepath, index=False)
    return df

if __name__ == "__main__":
    print("Generating synthetic claims triangle...\n")
    data = generate_dummy_claims()
    print(data)
    print("\nSaved to dummy_claims.csv")

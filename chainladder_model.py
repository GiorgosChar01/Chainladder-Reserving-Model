import pandas as pd
import chainladder as cl

def calculate_manual_link_ratios(triangle_df):
    """
    Manually calculates volume-weighted age-to-age factors using pandas.
    Demonstrates 'under-the-hood' mathematical logic without relying on external actuarial packages.
    """
    # Shift the triangle to align development periods for division
    shifted_triangle = triangle_df.shift(-1, axis=1)
    
    # Create a mask to only keep rows where the NEXT period actually has data
    valid_rows = shifted_triangle.notna()
    
    # Calculate the sums using ONLY the matching data pairs
    sum_j = triangle_df[valid_rows].sum()
    sum_j_plus_1 = shifted_triangle[valid_rows].sum()
    
    # Calculate the volume-weighted link ratios (f_j)
    link_ratios = sum_j_plus_1 / sum_j
    
    # Drop the last period as it cannot be developed further
    return link_ratios.dropna()

def calculate_reserves(csv_filepath="dummy_claims.csv"):
    """Loads raw claims data from a CSV, builds a triangle, and fits the Mack model."""
    # 1. Ingest the raw data
    raw_data = pd.read_csv(csv_filepath)

    # --- FIX: chainladder's Triangle requires a genuine date-like development
    # vector, not a bare integer lag (1, 2, 3...). Passing DevelopmentYear
    # straight through raises "Development lags could not be determined."
    # Build a real evaluation date: AccidentYear + (DevelopmentYear - 1),
    # valued at year end.
    raw_data['AccidentYear'] = pd.to_datetime(raw_data['AccidentYear'].astype(str), format='%Y')
    raw_data['DevelopmentDate'] = raw_data.apply(
        lambda r: pd.Timestamp(year=r['AccidentYear'].year + r['DevelopmentYear'] - 1, month=12, day=31),
        axis=1
    )

    # 2. Convert the raw flat file into an actuarial Triangle object
    triangle = cl.Triangle(
        raw_data,
        origin='AccidentYear',
        development='DevelopmentDate',
        columns='IncrementalPaid',
        cumulative=False
    )

    # --- FIX: the triangle above is still INCREMENTAL. Feeding it straight
    # into MackChainladder makes the model treat each incremental cell as if
    # it were the cumulative-to-date value, which silently corrupts the
    # "Latest" and "Ultimate" figures. Convert to cumulative first.
    cumulative_triangle = triangle.incr_to_cum()

    # 3. Fit the model to generate the summary statistics
    model = cl.MackChainladder().fit(cumulative_triangle)

    # Return the CUMULATIVE triangle DataFrame (calculate_manual_link_ratios
    # expects cumulative values, matching how it's exercised in test_model.py)
    # and the summary dataframe.
    return cumulative_triangle.to_frame(), model.summary_.to_frame()

if __name__ == "__main__":
    print("Ingesting CSV and calculating reserves...\n")
    
    # Get the data
    raw_triangle, results = calculate_reserves()
    
    # 1. Demonstrate manual Pandas calculation
    print("--- 1. Manual Pandas Link Ratio Calculation ---")
    my_link_ratios = calculate_manual_link_ratios(raw_triangle)
    print(my_link_ratios)
    
    # 2. Output the full model summary
    print("\n--- 2. Full Mack Chainladder Summary ---")
    print(results.head())
    
    # Export to CSV
    results.to_csv("chainladder_reserves.csv")
    print("\nResults successfully saved to chainladder_reserves.csv")
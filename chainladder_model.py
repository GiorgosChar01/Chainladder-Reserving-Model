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
    
    # --- FIX: Convert ONLY AccidentYear into a Date object ---
    raw_data['AccidentYear'] = pd.to_datetime(raw_data['AccidentYear'].astype(str), format='%Y')
    # We leave DevelopmentYear alone because it represents numerical lags (e.g., 1, 2, 3)!
    
    # 2. Convert the raw flat file into an actuarial Triangle object
    triangle = cl.Triangle(
        raw_data, 
        origin='AccidentYear', 
        development='DevelopmentYear', 
        columns='IncrementalPaid',
        cumulative=False
    )
    
    # 3. Fit the model to generate the summary statistics
    model = cl.MackChainladder().fit(triangle)
    
    # Return both the raw triangle DataFrame and the summary dataframe
    return triangle.to_frame(), model.summary_.to_frame()

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
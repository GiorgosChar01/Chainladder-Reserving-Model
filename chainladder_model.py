import pandas as pd
import chainladder as cl

def calculate_manual_link_ratios(triangle_df):
    """
    Manually calculates volume-weighted age-to-age factors using pandas.
    Demonstrates 'under-the-hood' mathematical logic without relying on external actuarial packages.
    """
    # Shift the triangle to align development periods for division
    shifted_triangle = triangle_df.shift(-1, axis=1)
    
    # Calculate the sum of claims for period j and period j+1 (dropping NAs)
    sum_j = triangle_df.sum(skipna=True)
    sum_j_plus_1 = shifted_triangle.sum(skipna=True)
    
    # Calculate the volume-weighted link ratios (f_j)
    link_ratios = sum_j_plus_1 / sum_j
    
    # Drop the last period as it cannot be developed further
    return link_ratios.dropna()

def calculate_reserves(dataset_name="genins"):
    """Loads claims data, fits a Mack Chainladder model, and returns a summary."""
    # Load data
    triangle = cl.load_sample(dataset_name)
    
    # Fit model using MackChainladder to generate the summary statistics
    model = cl.MackChainladder().fit(triangle)
    
    # Return both the raw triangle DataFrame and the summary dataframe
    return triangle.to_frame(), model.summary_.to_frame()

if __name__ == "__main__":
    print("Calculating reserves...\n")
    
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
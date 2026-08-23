import pandas as pd
import chainladder as cl

def calculate_reserves(csv_filepath="dummy_claims.csv"):
    """Loads raw claims data from a CSV, builds a triangle, and fits the Mack model."""
    
    # 1. Ingest the raw data (mirroring real-world spreadsheet extraction)
    raw_data = pd.read_csv(csv_filepath)
    
    # 2. Convert the raw flat file into an actuarial Triangle object
    triangle = cl.Triangle(
        raw_data, 
        origin='AccidentYear', 
        development='DevelopmentYear', 
        columns='IncrementalPaid',
        cumulative=False # Tells the package these are incremental, not cumulative claims
    )
    
    # 3. Fit the model to generate the summary statistics
    model = cl.MackChainladder().fit(triangle)
    
    return model.summary_.to_frame()

if __name__ == "__main__":
    print("Ingesting CSV and calculating reserves...\n")
    
    results = calculate_reserves()
    
    print("--- Mack Chainladder Summary ---")
    print(results.head())
    
    # Export to CSV
    results.to_csv("chainladder_reserves.csv")
    print("\nResults successfully saved to chainladder_reserves.csv")
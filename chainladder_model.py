import pandas as pd
import chainladder as cl

def calculate_reserves(dataset_name="genins"):
    """Loads claims data, fits a Chainladder model, and returns a summary."""
    # Load data
    triangle = cl.load_sample(dataset_name)
    
    # Fit model
    model = cl.Chainladder().fit(triangle)
    
    # Return summary dataframe
    return model.summary_.to_frame()

if __name__ == "__main__":
    print("Calculating reserves...")
    results = calculate_reserves()
    
    print("\nModel Summary:")
    print(results.head())
    
    results.to_csv("chainladder_reserves.csv")
    print("\nResults successfully saved to chainladder_reserves.csv")

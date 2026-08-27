import pytest
import pandas as pd
from chainladder_model import calculate_manual_link_ratios, calculate_reserves

@pytest.fixture
def dummy_triangle():
    """Creates a predictable triangle DataFrame to test our math."""
    data = {
        12: [1000.0, 1100.0, 1200.0],
        24: [1500.0, 1650.0, None],
        36: [1650.0, None, None]
    }
    return pd.DataFrame(data, index=[2021, 2022, 2023])

def test_manual_link_ratios(dummy_triangle):
    """Tests if the math accurately calculates volume-weighted LDFs."""
    result = calculate_manual_link_ratios(dummy_triangle)
    
    # 12-to-24 month volume-weighted factor: (1500 + 1650) / (1000 + 1100) = 1.5
    assert round(result[12], 2) == 1.50
    
    # 24-to-36 month volume-weighted factor: 1650 / 1500 = 1.1
    assert round(result[24], 2) == 1.10

def test_calculate_reserves_end_to_end():
    """
    Regression test for the real pipeline: CSV -> Triangle -> MackChainladder.
    This is the part that used to crash (bad development lag) and, once
    that was fixed, used to silently return wrong numbers (incremental
    values fed into Mack instead of cumulative). Guards against both.
    """
    raw_triangle, results = calculate_reserves("dummy_claims.csv")

    # The returned triangle must be cumulative: values should not decrease
    # left-to-right within a row.
    numeric = raw_triangle.select_dtypes("number")
    for _, row in numeric.iterrows():
        vals = row.dropna().tolist()
        assert vals == sorted(vals)

    # 2021 is fully developed (1000 + 450 + 150), so its ultimate should
    # equal its latest cumulative value with ~zero IBNR.
    assert round(results.loc[results.index[0], "Ultimate"], 2) == 1600.0
    assert round(results.loc[results.index[0], "Latest"], 2) == 1600.0

    # Every row should have a positive Ultimate at least as large as Latest.
    assert (results["Ultimate"] >= results["Latest"] - 1e-6).all()
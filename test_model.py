import pytest
import pandas as pd
from chainladder_model import calculate_manual_link_ratios

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
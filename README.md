# Chainladder Reserving Model 📈

A Python implementation of the Chainladder method for projecting Incurred But Not Reported (IBNR) claims. 

This repository demonstrates a programmatic approach to casualty actuarial reserving, transitioning traditional spreadsheet-based models into efficient, reproducible Python scripts using the `chainladder-python` and `pandas` libraries.

## Features
* Calculates volume-weighted Age-to-Age factors (Link Ratios) and Cumulative Development Factors (CDFs).
* Projects ultimate losses across origin periods.
* Isolates IBNR reserves from a standard run-off triangle.
* Exports actuarial summaries into clean CSV formats for downstream reporting.

## Installation and Setup

1. **Clone the repository:**
```bash
git clone https://github.com/GiorgosChar01/Chainladder-Reserving-Model.git
cd Chainladder-Reserving-Model
python chainladder_model.py
```
## Model Output 

When the model is run, it successfully projects the Ultimate reserves and calculates the IBNR (Incurred But Not Reported) for each accident year. 

Here is a sample of the summary output:

| Accident Year | Latest Paid | IBNR | Ultimate |
| :--- | :--- | :--- | :--- |
| **2021** | 1,600 | 0 | 1,600 |
| **2022** | 1,670 | 173 | 1,843 |
| **2023** | 1,300 | 782 | 2,082 |
| **Total** | **4,570** | **955** | **5,525** |
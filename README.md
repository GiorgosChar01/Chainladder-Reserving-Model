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

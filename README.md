A Python-based pipeline for analyzing BPIC event logs using process mining techniques and dynamic behavioral analysis. It includes reusable functions for dataset creation, behavior preprocessing, and Granger causality analysis — plus example notebooks demonstrating results.


---

## 🚀 Usage

1. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2. **Run the main pipeline**:

    ```bash
    python src/main_pipeline.py
    ```

3. **Explore the notebooks** in the `notebooks/` folder for detailed analyses, including:
    - Behavioral event plots
    - Granger causality tests
    - Time series analysis

---

## 🛠️ Features

- ✅ Reads .xes files using PM4PY
- ✅ Converts logs to pandas DataFrames
- ✅ Preprocesses event data for behavioral analysis
- ✅ Prepares time series for Granger causality analysis
- ✅ Visualizes dynamic process behavior

---

## 🔧 Requirements

- Python 3.8+
- pm4py
- pandas
- DyLoPro
- matplotlib

*(See `requirements.txt` for the complete list.)*

---


## Author

Developed by [aurelieleribaux-1].  
For questions or feedback, please contact [aurelie.leribaux@kuleuven.be].

---

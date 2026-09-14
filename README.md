# CSV Insights AI

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Ollama](https://img.shields.io/badge/AI-Ollama%20(local)-green.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

Generates natural-language insights reports from any CSV file, using an AI
model running 100% locally via [Ollama](https://ollama.com) — no data sent to
any external API, and no per-use cost.

## How it works

1. The script reads the CSV with `pandas` and computes a **statistical
   summary** (size, data types, missing values, numeric statistics,
   correlations, and most frequent categories).
2. That summary — never the raw data — is sent as a prompt to a local model
   via Ollama (default: `llama3.2`).
3. The model returns a report in plain English, ready to be read by a
   non-technical audience.

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com) installed and running
- Model pulled: `ollama pull llama3.2`

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py sample_data.csv
```

Saving the report to a file:

```bash
python main.py sample_data.csv --output report.txt
```

Using a different Ollama model:

```bash
python main.py sample_data.csv --model mistral
```

## Example output

Running the tool on `sample_data.csv` (15 orders, some missing values)
produces a report like this:

```
$ python main.py sample_data.csv

**Dataset Overview**
The sample data file 'sample_data.csv' contains 15 rows and 8 columns,
providing a comprehensive dataset for analysis. The columns cover essential
information about customer orders, products, and regions.

**Data Quality**
* The most frequently missing value is in the 'quantity' column, with 2
  instances of missing data.
* The 'product' column has 1 instance of missing data, which may require
  further investigation to determine the cause.

**Key Patterns and Insights**
* The average order price is $1131.11, indicating a relatively high average
  spend per order.
* The most common product categories are 'Electronics' (10 instances) and
  'Furniture' (5 instances).

**Practical Recommendations for Next Steps**
1. Investigate missing values in the 'quantity' column.
2. Verify 'order_date' consistency for potential data-entry errors.
3. Analyze product category trends to optimize product offerings.
```

## Why send statistics instead of the full CSV?

- **Context limits and cost**: large datasets don't fit in the prompt, and
  LLMs aren't reliable at doing exact arithmetic over thousands of rows.
- **Privacy**: only aggregated data (averages, counts, correlations) reaches
  the model — relevant for clients with sensitive data.

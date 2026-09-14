# CSV Insights AI

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

## Why send statistics instead of the full CSV?

- **Context limits and cost**: large datasets don't fit in the prompt, and
  LLMs aren't reliable at doing exact arithmetic over thousands of rows.
- **Privacy**: only aggregated data (averages, counts, correlations) reaches
  the model — relevant for clients with sensitive data.

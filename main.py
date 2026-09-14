"""
CSV Insights AI
Reads a CSV, computes a statistical summary, and uses a local AI model (Ollama)
to generate a natural-language insights report.
"""

import argparse
import sys

import pandas as pd
import ollama

# On Windows, the console (cmd/PowerShell) doesn't use UTF-8 by default,
# which breaks accented/special characters on screen. This does not affect
# the file saved with --output, only what's printed to the terminal.
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def analyze_csv(filepath: str) -> dict:
    """Computes a statistical summary of the CSV (never sends raw data to the AI)."""
    df = pd.read_csv(filepath)

    summary = {
        "file": filepath,
        "n_rows": len(df),
        "n_columns": len(df.columns),
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
    }

    numeric_df = df.select_dtypes(include="number")
    if not numeric_df.empty:
        summary["numeric_stats"] = numeric_df.describe().round(2).to_dict()

    # Correlation only makes sense with 2+ numeric columns
    if numeric_df.shape[1] > 1:
        summary["correlations"] = numeric_df.corr().round(2).to_dict()

    # Text/category columns: top 5 most frequent values
    categorical_df = df.select_dtypes(include=["object", "string"])
    if not categorical_df.empty:
        top_values = {}
        for col in categorical_df.columns:
            top_values[col] = df[col].value_counts().head(5).to_dict()
        summary["most_frequent_values"] = top_values

    return summary


def build_prompt(summary: dict) -> str:
    """Builds the prompt sent to the model, with clear formatting instructions."""
    return f"""You are a data analyst. Analyze the statistical summary below,
extracted from the file '{summary['file']}', and write a clear, objective report
in English for a non-technical audience (the business owner, not a data scientist).

Structure the report as follows:
1. Dataset overview (size, columns, date range if applicable)
2. Data quality (missing values, inconsistencies)
3. Key patterns and insights (trends, correlations, dominant categories)
4. 3 practical recommendations for next steps

Statistical summary (JSON):
{summary}
"""


def generate_report(prompt: str, model: str) -> str:
    """Calls the local Ollama model and returns the report text."""
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]


def main():
    parser = argparse.ArgumentParser(
        description="Generates natural-language insights from a CSV using local AI (Ollama)."
    )
    parser.add_argument("csv_file", help="Path to the CSV file to analyze")
    parser.add_argument("--model", default="llama3.2", help="Ollama model to use (default: llama3.2)")
    parser.add_argument("--output", default=None, help=".txt file to save the report to")
    args = parser.parse_args()

    try:
        summary = analyze_csv(args.csv_file)
    except FileNotFoundError:
        print(f"Error: file '{args.csv_file}' not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: '{args.csv_file}' is empty or not a valid CSV.")
        sys.exit(1)

    prompt = build_prompt(summary)

    print(f"Analyzing '{args.csv_file}' with model '{args.model}'...\n")
    try:
        report = generate_report(prompt, args.model)
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        print("Make sure Ollama is running (`ollama serve`) and the model is pulled (`ollama pull llama3.2`).")
        sys.exit(1)

    print("=" * 60)
    print(report)
    print("=" * 60)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\nReport saved to: {args.output}")


if __name__ == "__main__":
    main()

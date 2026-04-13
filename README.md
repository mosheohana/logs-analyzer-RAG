# Logs Analyzer

A two-stage Python toolkit for analyzing Apache access logs:

1. **`log_analyzer.py`** – Parses raw log files, computes statistics, and generates visualizations.
2. **`rag_logs.py`** – Enables natural-language querying of parsed logs using Retrieval-Augmented Generation (RAG) with semantic search.

---

## Features

### Log Analyzer (`log_analyzer.py`)
- Loads raw Apache Combined Log Format files
- Parses each line via regex into structured fields: IP, timestamp, HTTP method, path, status code, and response size
- Converts fields to appropriate types (datetime, integer)
- Prints summary statistics:
  - Top 5 requesting IP addresses
  - HTTP status code distribution
  - Most requested URL paths
- Saves parsed data to `parsed_logs.csv`
- Generates bar charts and a time-series plot (requests per hour)

### RAG Query Interface (`rag_logs.py`)
- Loads `parsed_logs.csv` produced by the log analyzer
- Converts each log entry to a natural-language sentence
- Embeds all entries using `sentence-transformers` (`all-MiniLM-L6-v2`)
- Builds a FAISS index for fast nearest-neighbour retrieval
- Provides an interactive query loop: type a question in plain English and get the most relevant log entries back

Example queries:
- `failed login attempts`
- `suspicious IP activity`
- `many requests from same IP`
- `404 errors`
- `brute-force attack`

---

## Project Structure

```
logs-analyzer/
├── apache_logs.txt      # Raw Apache access log input
├── log_analyzer.py      # Stage 1: parse, analyze, and visualize
├── rag_logs.py          # Stage 2: semantic search over parsed logs
├── parsed_logs.csv      # Output of log_analyzer.py (auto-generated)
└── README.md
```

---

## Requirements

- Python 3.8+
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)
- [sentence-transformers](https://www.sbert.net/)
- [faiss-cpu](https://github.com/facebookresearch/faiss) (or `faiss-gpu`)

Install all dependencies with:

```bash
pip install pandas matplotlib sentence-transformers faiss-cpu
```

---

## Usage

### Step 1 – Parse and analyze the logs

```bash
python log_analyzer.py
```

This reads `apache_logs.txt`, prints statistics to the console, displays charts, and writes `parsed_logs.csv`.

### Step 2 – Query the logs in natural language

```bash
python rag_logs.py
```

The script indexes all log entries and starts an interactive prompt. Type any question about the logs and press **Enter** to see the most relevant entries. Type `exit` to quit.

---

## Example Output

```
Loaded 10000 log lines

Sample parsed rows:
             ip                      time method              path  status
0   192.168.1.1  2023-01-15 08:23:11+00:00    GET     /index.html     200
...

Top 5 IP addresses:
192.168.1.1    312
10.0.0.5       289
...

HTTP status code distribution:
200    7842
404     912
500     246
...
```

```
Indexed 10000 log entries.

Type your question (or 'exit'): 404 errors

Retrieved relevant log lines:
- At 2023-01-15 08:45:02+00:00 IP 10.0.0.9 sent GET request to /missing-page and server returned status 404.
...
```

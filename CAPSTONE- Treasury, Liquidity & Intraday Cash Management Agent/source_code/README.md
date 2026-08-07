# Treasury Liquidity Agent Demo

## Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Set your API key

```bash
export OPENAI_API_KEY=your_key_here
# Windows PowerShell:
# $env:OPENAI_API_KEY="your_key_here"
```

## Sanity check

```bash
python eval_harness.py
```

## Run the terminal demo

```bash
python main.py
```

## Run a stress scenario

```bash
python main.py --scenario delayed_settlement
python main.py --scenario large_withdrawal --amount 1000000
```

## Open the HTML demo

Open [demo.html](demo.html) directly in a browser, or serve the folder with:

```bash
python -m http.server 8000
```

# LLM Eval Harness

Regression testing for LLM prompt outputs.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Set your API key
export GOOGLE_API_KEY=your-key-here

# Run a test suite
harness run evals/test.yaml --verbose
```

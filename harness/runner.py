import yaml
from pathlib import Path
import os
from google import genai
from rich.table import Table
from rich.console import Console

console = Console()

def load_suite(path: Path):
    """Load YAML test suite."""
    with open(path) as f:
        return yaml.safe_load(f)

def run_case(client, model_name: str, prompt: str):
    """Send prompt to LLM and get response."""
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )
    return response.text.strip()

def score_exact(actual: str, expected: str):
    """Simple exact match scorer."""
    return 1.0 if actual.lower() == expected.lower() else 0.0

def run_suite(suite_path: Path, verbose: bool = False):
    """Main runner logic."""
    suite = load_suite(suite_path)
    
    # Configure Gemini client
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        console.print("[red]Error: GOOGLE_API_KEY environment variable not set[/red]")
        return
    
    client = genai.Client(api_key=api_key)
    
    results = []
    console.print(f"[blue][bold]Made by Vivek Manglani[/bold][/blue]")
    for case in suite['cases']:
        if verbose:
            console.print(f"[dim]Running {case['id']}...[/dim]")
        
        actual = run_case(client, suite['model'], case['prompt'])
        score = score_exact(actual, case['expected'])
        
        results.append({
            'id': case['id'],
            'prompt': case['prompt'],
            'expected': case['expected'],
            'actual': actual,
            'score': score,
            'passed': score >= 0.9
        })
    
    # Print results table
    table = Table(title=f"Results: {suite['name']}")
    table.add_column("Case", style="dim")
    table.add_column("Expected")
    table.add_column("Actual")
    table.add_column("Score", justify="right")
    table.add_column("Status")
    
    for r in results:
        status = "[green]✓ PASS[/green]" if r['passed'] else "[red]✗ FAIL[/red]"
        table.add_row(
            r['id'],
            r['expected'][:30],
            r['actual'][:30],
            f"{r['score']:.2f}",
            status
        )
    
    console.print(table)
    
    passed = sum(r['passed'] for r in results)
    total = len(results)
    console.print(f"\n[bold]Passed:[/bold] {passed}/{total}")
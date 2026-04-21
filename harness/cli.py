import typer
from rich.console import Console
from pathlib import Path
from harness.runner import run_suite
console = Console()

app = typer.Typer(help="LLM Eval Harness — regression testing for LLM outputs")

@app.command()
def run(
    suite: Path = typer.Argument(..., help="Path to eval YAML suite"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
):
    """Run an eval suite against LLM providers."""
    if not suite.exists():
        console.print(f"[red]Error: Suite not found at:[/red] {suite}")
        raise typer.Exit(code=1)
    run_suite(suite, verbose)
@app.command()
def show(
    run_id: str = typer.Argument(..., help="Run ID to inspect"),
):
    """Show results for a completed eval run."""
    print(f"Showing results for run: {run_id}")

@app.command()
def serve(
    port: int = typer.Option(8000, help="Port to bind"),
):
    """Start the results dashboard."""
    print(f"Starting dashboard on port {port}")


@app.command()
def compare(
    run_id_1: str = typer.Argument(...,help="First RunID to be compared"),
    run_id_2: str = typer.Argument(...,help="Second RunID to be compared"),
    failed: bool = typer.Option(False, "--failed-only", "-f", help = "Only show failed evals")
):
    """Compares 2 runs by their evals"""
    print(f"Comparing {run_id_1} and {run_id_2}")
    print(f"Failed only: {failed}")
if __name__ == "__main__":
    app()
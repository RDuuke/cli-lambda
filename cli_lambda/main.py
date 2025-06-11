from cli_lambda.java_scaffolder import scaffold_java_lambda
import typer
from pathlib import Path

app = typer.Typer()

@app.command()
def create_java(name: str):
    """
    Crea la estructura base de una Lambda Java con nombre `name`.
    """
    scaffold_java_lambda(name)


if __name__ == "__main__":
    app()

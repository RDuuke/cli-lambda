from cli_lambda.java_scaffolder import scaffold_java_lambda
import typer

app = typer.Typer(help="CLI para generar funciones AWS Lambda con arquitectura Java y SAM.")

@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")

@app.command()
def java(name: str):
    """
    Crea la estructura base de una Lambda Java con nombre `name`.
    """
    scaffold_java_lambda(name)


if __name__ == "__main__":
    app()

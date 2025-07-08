from cli_lambda.scaffolders.java import scaffold_java_lambda
from cli_lambda.scaffolders.nodejs import scaffold_nodejs_lambda
from cli_lambda.scaffolders.quarkus import scaffold_quarkus_lambda
import typer

app = typer.Typer(help="CLI para generar funciones AWS Lambda con arquitectura Java y SAM.")

@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")

@app.command()
def java(name: str, project_prefix: str = typer.Option("CL00079-CustomerInfoSiif", help="Prefijo del proyecto (ej. CL00079-CustomerInfoSiif)."), java_version: int = typer.Option(11, help="Versión de Java a usar (11 o 21).")):
    """
    Crea la estructura base de una Lambda Java con nombre `name`.
    """
    scaffold_java_lambda(name, project_prefix, java_version)

@app.command()
def node(name: str, lang: str = typer.Option("js", help="Lenguaje a usar: 'js' para JavaScript o 'ts' para TypeScript."), project_prefix: str = typer.Option("CL00079-CustomerInfoSiif", help="Prefijo del proyecto (ej. CL00079-CustomerInfoSiif).")):
    """
    Crea la estructura base de una Lambda Node.js con nombre `name`.
    """
    scaffold_nodejs_lambda(name, lang, project_prefix)

@app.command()
def quarkus(name: str, type: str = typer.Option("event", help="Tipo de trigger: 'event' para invocación directa o 'rest' para API Gateway."), project_prefix: str = typer.Option("CL00079-CustomerInfoSiif", help="Prefijo del proyecto (ej. CL00079-CustomerInfoSiif)."), graal: bool = typer.Option(False, help="Generar proyecto Quarkus con soporte para GraalVM (Native Image).")):
    """
    Crea la estructura base de una Lambda Java con Quarkus con nombre `name`.
    """
    scaffold_quarkus_lambda(name, type, project_prefix, graal)


if __name__ == "__main__":
    app()

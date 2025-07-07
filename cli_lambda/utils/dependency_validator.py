import shutil
import typer

def validate_dependencies():
    required_tools = {
        "java": "Java 11+",
        "mvn": "Apache Maven",
        "docker": "Docker",
        "sam": "AWS SAM CLI"
    }

    missing = []
    for tool, desc in required_tools.items():
        if shutil.which(tool) is None:
            missing.append(f"{tool} ({desc})")

    if missing:
        typer.echo("❌ Faltan las siguientes dependencias requeridas:")
        for item in missing:
            typer.echo(f"   - {item}")
        raise typer.Exit(code=1)
    else:
        typer.echo("✅ Todas las dependencias requeridas están instaladas.")

from pathlib import Path
import shutil
import typer
from cli_lambda.utils.template_renderer import render_template

TEMPLATES_DIR = Path(__file__).parent.parent / "templates/quarkus"

def scaffold_quarkus_lambda(name: str, type: str):
    if type == "event":
        _scaffold_event_driven(name)
    elif type == "rest":
        _scaffold_rest_api(name)
    else:
        typer.secho(f"❌ Tipo de trigger no soportado para Quarkus: {type}. Usa 'event' o 'rest'.", fg=typer.colors.RED)
        raise typer.Exit()

def _scaffold_event_driven(name: str):
    base_path = Path(name)
    project_name = name.replace("-", "").lower()
    _create_common_structure(base_path, project_name, "event")
    typer.secho(f"✅ Proyecto Quarkus (event-driven) '{name}' creado con éxito.", fg=typer.colors.GREEN)
    _print_next_steps()

def _scaffold_rest_api(name: str):
    base_path = Path(name)
    project_name = name.replace("-", "").lower()
    _create_common_structure(base_path, project_name, "rest")
    typer.secho(f"✅ Proyecto Quarkus (REST API) '{name}' creado con éxito.", fg=typer.colors.GREEN)
    _print_next_steps()

def _create_common_structure(base_path: Path, project_name: str, type: str):
    if base_path.exists():
        typer.secho(f"⚠️  El directorio '{base_path.name}' ya existe.", fg=typer.colors.YELLOW)
        raise typer.Exit()

    try:
        # Estructura de directorios
        src_main_java = base_path / "src/main/java/org/acme"
        (src_main_java / "application").mkdir(parents=True)
        (src_main_java / "domain").mkdir(parents=True)
        (src_main_java / "infrastructure").mkdir(parents=True)
        (base_path / "src/main/resources").mkdir(parents=True)
        (base_path / "src/test/java/org/acme/infrastructure").mkdir(parents=True)

        # Plantillas específicas del tipo
        type_templates_dir = TEMPLATES_DIR / type
        render_template("pom.xml.j2", base_path / "pom.xml", project_name, type_templates_dir)
        render_template("template.yaml.j2", base_path / "template.yaml", project_name, type_templates_dir)
        render_template("README.md.j2", base_path / "README.md", project_name, type_templates_dir)
        render_template("gitignore.template", base_path / ".gitignore", project_name, TEMPLATES_DIR)
        render_template("GEMINI.md.j2", base_path / "GEMINI.md", project_name, Path(__file__).parent.parent / "templates")

        if type == "event":
            render_template("EventHandler.java.j2", src_main_java / "infrastructure/EventHandler.java", project_name, type_templates_dir)
            render_template("EventHandlerTest.java.j2", base_path / "src/test/java/org/acme/infrastructure/EventHandlerTest.java", project_name, type_templates_dir)
        else: # rest
            render_template("GreetingResource.java.j2", src_main_java / "infrastructure/GreetingResource.java", project_name, TEMPLATES_DIR) # Re-usamos la plantilla original
            render_template("GreetingResourceTest.java.j2", base_path / "src/test/java/org/acme/infrastructure/GreetingResourceTest.java", project_name, type_templates_dir)

        # Plantillas comunes
        render_template("application/GreetingService.java.j2", src_main_java / "application/GreetingService.java", project_name, TEMPLATES_DIR)
        render_template("domain/Greeting.java.j2", src_main_java / "domain/Greeting.java", project_name, TEMPLATES_DIR) # Re-usamos la plantilla original
        render_template("src/main/resources/application.properties.j2", base_path / "src/main/resources/application.properties", project_name, TEMPLATES_DIR)

    except Exception as e:
        typer.secho(f"❌ Error al crear el proyecto: {e}", fg=typer.colors.RED)
        if base_path.exists():
            shutil.rmtree(base_path)
            typer.echo("🧹 Directorio del proyecto eliminado por limpieza.")
        raise typer.Exit()

def _print_next_steps():
    typer.echo("👉 Entra al directorio con: cd <nombre_del_proyecto>")
    typer.echo("🚀 Para empezar, ejecuta: mvn compile quarkus:dev")
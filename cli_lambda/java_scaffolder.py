from pathlib import Path
import shutil
from cli_lambda.utils import load_env_config
import typer
from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = Path(__file__).parent / "templates/java"

def scaffold_java_lambda(name: str):
    validate_dependencies()
    base_path = Path(name)
    project_name = name.replace("lda-", "").lower()
    
    if base_path.exists():
        typer.echo(f"⚠️ La carpeta '{name}' ya existe.")
        return
    
    try:
        # Crear estructura bajo src/main/java/com/<project_name>
        base_java = base_path / "src" / "main" / "java" / "com" / project_name
        (base_java / "dto").mkdir(parents=True)
        (base_java / "port").mkdir()
        (base_java / "adapter" / "output").mkdir(parents=True)
        (base_java / "usecase").mkdir()
        (base_java / "di").mkdir()

        # Generar archivos usando Jinja2
        render_template("Handler.java.j2", base_java / "Handler.java", project_name)
        render_template("OutputDto.java.j2", base_java / "dto" / "OutputDto.java", project_name)
        render_template("pom.xml.j2", base_path / "pom.xml", project_name)
        render_template("gitignore.template", base_path / ".gitignore", project_name)
        render_template("ResponseEntity.java.j2", base_java / "dto" / "ResponseEntity.java", project_name)
        render_template("StatusCode.java.j2", base_java / "dto" / "StatusCode.java", project_name)
        render_template("InputDto.java.j2", base_java / "dto" / "InputDto.java", project_name)


        render_readme("README.md.j2", base_path, project_name)
        render_codeartifact_script(base_path)


        # Plantilla SAM y pipeline
        render_sam_template(base_path, project_name)
        render_pipeline_file(base_path, name)

        # Archivo de evento para pruebas locales
        event_template_path = TEMPLATES_DIR / "event.template.json"
        (base_path / "event.json").write_text(event_template_path.read_text())

        typer.secho(f"✅ Proyecto Java '{name}' creado con éxito.", fg=typer.colors.GREEN)
        typer.echo(f"👉 Entra al directorio con:\n   cd {name}")
    except Exception as e:
        typer.secho(f"❌ Error al crear el proyecto: {e}", fg=typer.colors.RED)
        if base_path.exists():
            shutil.rmtree(base_path)
            typer.echo("🧹 Directorio eliminado por limpieza.")

def render_template(template_name: str, output_path: Path, package: str):
    template_path = TEMPLATES_DIR / template_name
    if not template_path.exists():
        raise FileNotFoundError(f"Template no encontrado: {template_path}")
    
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template(template_name)
    content = template.render(package_name=package)
    output_path.write_text(content, encoding="utf-8")

def render_sam_template(destination_dir: Path, name: str):
    name_pascal = ''.join(word.capitalize() for word in name.split('-'))
    resource_name = f"{name_pascal}Function"
    
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template("template.yaml.j2")

    output = template.render(
        resource_name=resource_name,
        package_name=name,
        api_path=name
    )

    (destination_dir / "template.yaml").write_text(output, encoding="utf-8")

def render_pipeline_file(destination_dir: Path, name: str):
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template("azure-pipeline.yaml.j2")

    output = template.render(name=name)
    (destination_dir / "azure-pipelines.yml").write_text(output, encoding="utf-8")

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


def render_codeartifact_script(destination_dir: Path):
    config = load_env_config()

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template("setup-codeartifact.ps1.j2")

    output = template.render(
        domain=config["domain"],
        domain_owner=config["domain_owner"],
        region=config["region"],
        repo_name=config["repo_name"],
        aws_profile=config["aws_profile"],
        server_id=config["server_id"]
    )

    (destination_dir / "setup-codeartifact.ps1").write_text(output, encoding="utf-8")


def render_readme(template_name: str, destination_dir: Path, project_name: str):
    resource_name = ''.join(word.capitalize() for word in project_name.split('-')) + "Function"
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template(template_name)

    output = template.render(
        project_name=project_name,
        resource_name=resource_name
    )

    (destination_dir / "README.md").write_text(output, encoding="utf-8")

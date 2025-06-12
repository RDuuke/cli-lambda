from pathlib import Path
import shutil
import typer
from jinja2 import Environment, FileSystemLoader


TEMPLATES_DIR = Path(__file__).parent / "templates/java"

def scaffold_java_lambda(name: str):
    validate_dependencies()  # 🔒 Verifica antes de continuar
    base_path = Path(name)
    project_name = name.replace("lda-", "").lower()
    if base_path.exists():
       typer.echo(f"⚠️ La carpeta '{name}' ya existe.")
       return
    
    try:
        # Crear estructura de carpetas
        (base_path / "src" / "application").mkdir(parents=True)
        (base_path / "src" / "domain").mkdir()
        (base_path / "src" / "infrastructure").mkdir()
        (base_path / "src" / "main" / "java" / "com" / project_name).mkdir(parents=True)
        (base_path / "src" / "test" / "java" / "com" / project_name).mkdir(parents=True)

        # Archivos generados desde templates
        fill_template("pom.xml.j2", base_path / "pom.xml", name)
        fill_template("Handler.java.j2", base_path / f"src/main/java/com/{project_name}/Handler.java", name)
        fill_template("Response.java.j2", base_path / f"src/main/java/com/{project_name}/Response.java", name)
        fill_template("HandlerTest.java.j2", base_path / f"src/test/java/com/{project_name}/HandlerTest.java", name)
        render_sam_template(base_path, name)
        render_pipeline_file(base_path, name)
        fill_template("gitignore.template", base_path / ".gitignore", name)

        event_template_path = TEMPLATES_DIR / "event.template.json"
        (base_path / "event.json").write_text(event_template_path.read_text())

        typer.echo(f"✅ Proyecto Java '{name}' creado con éxito.")
        typer.echo(f"👉 Entra al directorio con:\n   cd {name}")
    except Exception as e:
        typer.echo(f"❌ Error al crear el proyecto: {e}")
        if base_path.exists():
            shutil.rmtree(base_path)
            typer.echo("🧹 Directorio eliminado por limpieza.")

def fill_template(template_name: str, output_path: Path, name: str):
    project_name = name.replace("lda-", "")
    template_path = TEMPLATES_DIR / template_name
    content = template_path.read_text(encoding="utf-8")
    content = content.replace("{{package}}", f"com.{project_name.lower()}")
    content = content.replace("{{name}}", project_name)
    output_path.write_text(content, encoding="utf-8")


def render_sam_template(destination_dir: Path, name: str):
    name_clean = name.replace('lda-', '').lower()
    name_pascal = ''.join(word.capitalize() for word in name_clean.split('-'))
    resource_name = f"{name_pascal}Function"

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template("template.yaml.j2")

    output = template.render(
        resource_name=resource_name,
        package_name=name_clean,
        api_path=name_clean
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
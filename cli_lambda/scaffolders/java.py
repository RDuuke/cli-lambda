from pathlib import Path
import shutil
import typer
from cli_lambda.utils.template_renderer import render_template

TEMPLATES_DIR = Path(__file__).parent.parent / "templates/java"

def scaffold_java_lambda(name: str):
    base_path = Path(name)
    package_name = name.replace("-", "").lower()

    if base_path.exists():
        typer.secho(f"⚠️  El directorio '{name}' ya existe.", fg=typer.colors.YELLOW)
        raise typer.Exit()

    try:
        # Estructura de directorios principal de Maven
        src_main_java = base_path / "src/main/java" / f"com/{package_name}"
        src_main_resources = base_path / "src/main/resources"
        src_test_java = base_path / "src/test/java" / f"com/{package_name}"

        # Crear directorios de la arquitectura de capas
        (src_main_java / "application/usecase").mkdir(parents=True)
        (src_main_java / "domain/dto").mkdir(parents=True)
        (src_main_java / "domain/model").mkdir(parents=True)
        (src_main_java / "infrastructure").mkdir(parents=True)
        src_main_resources.mkdir(parents=True)
        (src_test_java / "infrastructure").mkdir(parents=True)

        # --- Renderizar archivos de configuración en la raíz ---
        render_template("pom.xml.j2", base_path / "pom.xml", package_name, TEMPLATES_DIR)
        render_template("README.md.j2", base_path / "README.md", package_name, TEMPLATES_DIR)
        render_template("checkstyle.xml.j2", base_path / "checkstyle.xml", package_name, TEMPLATES_DIR)
        render_template("template.yaml.j2", base_path / "template.yaml", package_name, TEMPLATES_DIR, handler_path=f"com.{package_name}.infrastructure.Handler")
        render_template("event.template.json", base_path / "event.json", package_name, TEMPLATES_DIR)
        render_template("gitignore.template", base_path / ".gitignore", package_name, TEMPLATES_DIR)
        render_template("GEMINI.md.j2", base_path / "GEMINI.md", package_name, Path(__file__).parent.parent / "templates")

        # --- Renderizar archivos de la capa de Dominio ---
        render_template("domain/dto/InputDto.java.j2", src_main_java / "domain/dto/InputDto.java", package_name, TEMPLATES_DIR)
        render_template("domain/dto/OutputDto.java.j2", src_main_java / "domain/dto/OutputDto.java", package_name, TEMPLATES_DIR)
        render_template("domain/dto/ResponseEntity.java.j2", src_main_java / "domain/dto/ResponseEntity.java", package_name, TEMPLATES_DIR)
        render_template("domain/dto/StatusCode.java.j2", src_main_java / "domain/dto/StatusCode.java", package_name, TEMPLATES_DIR)
        render_template("domain/model/HelloModel.java.j2", src_main_java / "domain/model/HelloModel.java", package_name, TEMPLATES_DIR)

        # --- Renderizar archivos de la capa de Aplicación ---
        render_template("application/usecase/HelloUseCase.java.j2", src_main_java / "application/usecase/HelloUseCase.java", package_name, TEMPLATES_DIR)

        # --- Renderizar archivos de la capa de Infraestructura ---
        render_template("infrastructure/Handler.java.j2", src_main_java / "infrastructure/Handler.java", package_name, TEMPLATES_DIR)

        # --- Renderizar archivos de configuración en resources ---
        render_template("log4j2.xml.j2", src_main_resources / "log4j2.xml", package_name, TEMPLATES_DIR)

        # --- Renderizar archivos de prueba ---
        render_template("HandlerTest.java.j2", src_test_java / "infrastructure/HandlerTest.java", package_name, TEMPLATES_DIR)

        typer.secho(f"✅ Proyecto Java '{name}' creado con éxito.", fg=typer.colors.GREEN)
        typer.echo(f"👉 Entra al directorio con:\n   cd {name}")
        typer.echo("🚀 Para empezar, ejecuta: mvn clean install")

    except Exception as e:
        typer.secho(f"❌ Error al crear el proyecto: {e}", fg=typer.colors.RED)
        if base_path.exists():
            shutil.rmtree(base_path)
            typer.echo("🧹 Directorio del proyecto eliminado por limpieza.")
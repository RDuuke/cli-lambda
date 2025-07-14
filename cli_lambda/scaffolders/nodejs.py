from pathlib import Path
import shutil
import typer
from cli_lambda.utils.template_renderer import render_template, render_readme

def scaffold_nodejs_lambda(name: str, lang: str, project_prefix: str):
    base_path = Path(name)
    project_name = name.replace("lda-", "").lower()
    
    if base_path.exists():
        typer.echo(f"[AVISO] La carpeta '{name}' ya existe.")
        return
    
    try:
        (base_path / "src").mkdir(parents=True)
        (base_path / "src" / "domain").mkdir()
        (base_path / "src" / "application").mkdir()
        (base_path / "src" / "infrastructure").mkdir()

        templates_base_dir = Path(__file__).parent.parent / "templates/nodejs"
        
        if lang == "ts":
            current_templates_dir = templates_base_dir / "ts"
            # Generar archivos usando Jinja2 para TypeScript
            # Create test directories
            (base_path / "test").mkdir(parents=True)
            (base_path / "test" / "unit").mkdir()
            (base_path / "test" / "unit" / "application").mkdir()
            (base_path / "test" / "unit" / "infrastructure").mkdir()

            # Render domain layer files
            render_template("domain/model.ts.j2", base_path / "src" / "domain" / "model.ts", project_name, current_templates_dir)
            render_template("domain/company.repository.ts.j2", base_path / "src" / "domain" / "company.repository.ts", project_name, current_templates_dir)
            render_template("domain/logger.interface.ts.j2", base_path / "src" / "domain" / "logger.interface.ts", project_name, current_templates_dir)

            # Render application layer files
            render_template("application/usecase.ts.j2", base_path / "src" / "application" / "usecase.ts", project_name, current_templates_dir)

            # Render infrastructure layer files
            render_template("infrastructure/company.repository.ts.j2", base_path / "src" / "infrastructure" / "company.repository.ts", project_name, current_templates_dir)
            render_template("infrastructure/console.logger.ts.j2", base_path / "src" / "infrastructure" / "console.logger.ts", project_name, current_templates_dir)
            render_template("infrastructure/dependencies.ts.j2", base_path / "src" / "infrastructure" / "dependencies.ts", project_name, current_templates_dir)
            render_template("infrastructure/handler.ts.j2", base_path / "src" / "infrastructure" / "handler.ts", project_name, current_templates_dir)

            # Render index.ts as the entry point
            render_template("index.ts.j2", base_path / "src" / "index.ts", project_name, current_templates_dir)

            # Render test files
            render_template("test/unit/application/get-company.usecase.test.ts.j2", base_path / "test" / "unit" / "application" / "get-company.usecase.test.ts", project_name, current_templates_dir)
            render_template("test/unit/infrastructure/handler.test.ts.j2", base_path / "test" / "unit" / "infrastructure" / "handler.test.ts", project_name, current_templates_dir)

            # Render root level files
            render_template("package.json.j2", base_path / "package.json", project_name, current_templates_dir, project_prefix=project_prefix)
            render_template("tsconfig.json.j2", base_path / "tsconfig.json", project_name, current_templates_dir, project_prefix=project_prefix)
            render_template("esbuild.config.ts.j2", base_path / "esbuild.config.ts", project_name, current_templates_dir, project_prefix=project_prefix)
            render_template("azure-pipelines.yml.j2", base_path / "azure-pipelines.yml", project_name, templates_base_dir, project_prefix=project_prefix)
            render_template("eslint.config.mjs.j2", base_path / "eslint.config.mjs", project_name, current_templates_dir, project_prefix=project_prefix)
            render_template("jest.config.ts.j2", base_path / "jest.config.ts", project_name, current_templates_dir)
            render_template("setup-jest.ts.j2", base_path / "setup-jest.ts", project_name, current_templates_dir)
            render_template(".env.example.j2", base_path / ".env.example", project_name, current_templates_dir)
            render_template("gitignore.template", base_path / ".gitignore", project_name, current_templates_dir)
        elif lang == "js":
            current_templates_dir = templates_base_dir / "js"
            # Generar archivos usando Jinja2 para JavaScript
            render_template("infrastructure/handler.js.j2", base_path / "infrastructure" / "handler.js", project_name, current_templates_dir)
            render_template("application/usecase.js.j2", base_path / "application" / "usecase.js", project_name, current_templates_dir)
            render_template("domain/model.js.j2", base_path / "domain" / "model.js", project_name, current_templates_dir)
            render_template("package.json.j2", base_path / "package.json", project_name, current_templates_dir, project_prefix=project_prefix)
            render_template("azure-pipelines.yml.j2", base_path / "azure-pipelines.yml", project_name, templates_base_dir, project_prefix=project_prefix)
            render_template("eslint.config.mjs.j2", base_path / "eslint.config.mjs", project_name, current_templates_dir, project_prefix=project_prefix)
        else:
            typer.secho(f"❌ Lenguaje no soportado para Node.js: {lang}. Usa 'js' o 'ts'.", fg=typer.colors.RED)
            if base_path.exists():
                shutil.rmtree(base_path)
            return

        render_readme("README.md.j2", base_path, project_name, current_templates_dir)
        render_template("GEMINI.md.j2", base_path / "GEMINI.md", project_name, Path(__file__).parent.parent / "templates")

        typer.secho(f"[OK] Proyecto Node.js ({lang}) '{name}' creado con éxito.", fg=typer.colors.GREEN)
        typer.echo(f"--> Entra al directorio con:\n   cd {name}")
    except Exception as e:
        typer.secho(f"[ERROR] Error al crear el proyecto: {e}", fg=typer.colors.RED)
        if base_path.exists():
            shutil.rmtree(base_path)
            typer.echo("[INFO] Directorio eliminado por limpieza.")

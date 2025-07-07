from pathlib import Path
import shutil
import typer
from cli_lambda.utils.template_renderer import render_template, render_readme

def scaffold_nodejs_lambda(name: str, lang: str, project_prefix: str):
    base_path = Path(name)
    project_name = name.replace("lda-", "").lower()
    
    if base_path.exists():
        typer.echo(f"⚠️ La carpeta '{name}' ya existe.")
        return
    
    try:
        (base_path / "domain").mkdir(parents=True)
        (base_path / "application").mkdir()
        (base_path / "infrastructure").mkdir()

        templates_base_dir = Path(__file__).parent.parent / "templates/nodejs"
        
        if lang == "ts":
            current_templates_dir = templates_base_dir / "ts"
            # Generar archivos usando Jinja2 para TypeScript
            render_template("infrastructure/handler.ts.j2", base_path / "infrastructure" / "handler.ts", project_name, current_templates_dir)
            render_template("application/usecase.ts.j2", base_path / "application" / "usecase.ts", project_name, current_templates_dir)
            render_template("domain/model.ts.j2", base_path / "domain" / "model.ts", project_name, current_templates_dir)
            render_template("package.json.j2", base_path / "package.json", project_name, current_templates_dir, project_prefix=project_prefix)
            render_template("tsconfig.json.j2", base_path / "tsconfig.json", project_name, current_templates_dir, project_prefix=project_prefix)
            render_template("esbuild.config.ts.j2", base_path / "esbuild.config.ts", project_name, current_templates_dir, project_prefix=project_prefix)
            render_template("azure-pipelines.yml.j2", base_path / "azure-pipelines.yml", project_name, current_templates_dir, project_prefix=project_prefix)
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
            render_template("azure-pipelines.yml.j2", base_path / "azure-pipelines.yml", project_name, current_templates_dir, project_prefix=project_prefix)
            render_template("eslint.config.mjs.j2", base_path / "eslint.config.mjs", project_name, current_templates_dir, project_prefix=project_prefix)
        else:
            typer.secho(f"❌ Lenguaje no soportado para Node.js: {lang}. Usa 'js' o 'ts'.", fg=typer.colors.RED)
            if base_path.exists():
                shutil.rmtree(base_path)
            return

        render_readme("README.md.j2", base_path / "README.md", project_name, current_templates_dir)
        render_template("GEMINI.md.j2", base_path / "GEMINI.md", project_name, Path(__file__).parent.parent / "templates")

        typer.secho(f"✅ Proyecto Node.js ({lang}) '{name}' creado con éxito.", fg=typer.colors.GREEN)
        typer.echo(f"👉 Entra al directorio con:\n   cd {name})
    except Exception as e:
        typer.secho(f"❌ Error al crear el proyecto: {e}", fg=typer.colors.RED)
        if base_path.exists():
            shutil.rmtree(base_path)
            typer.echo("🧹 Directorio eliminado por limpieza.")

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from cli_lambda.utils.env_config import load_env_config

def render_template(template_name: str, output_path: Path, package: str, templates_dir: Path, **kwargs):
    template_path = templates_dir / template_name
    if not template_path.exists():
        raise FileNotFoundError(f"Template no encontrado: {template_path}")
    
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    template = env.get_template(template_name)
    
    # Combina los argumentos básicos con los adicionales
    context = {
        "package_name": package,
        **kwargs
    }
    
    content = template.render(**context)
    output_path.write_text(content, encoding="utf-8")

def render_sam_template(destination_dir: Path, name: str, templates_dir: Path):
    name_pascal = ''.join(word.capitalize() for word in name.split('-'))
    resource_name = f"{name_pascal}Function"
    
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    template = env.get_template("template.yaml.j2")

    output = template.render(
        resource_name=resource_name,
        package_name=name,
        api_path=name
    )

    (destination_dir / "template.yaml").write_text(output, encoding="utf-8")

def render_pipeline_file(destination_dir: Path, name: str, templates_dir: Path):
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    template = env.get_template("azure-pipeline.yaml.j2")

    output = template.render(name=name)
    (destination_dir / "azure-pipelines.yml").write_text(output, encoding="utf-8")

def render_codeartifact_script(destination_dir: Path, templates_dir: Path):
    config = load_env_config()

    env = Environment(loader=FileSystemLoader(str(templates_dir)))
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

def render_readme(template_name: str, destination_dir: Path, project_name: str, templates_dir: Path):
    resource_name = ''.join(word.capitalize() for word in project_name.split('-')) + "Function"
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    template = env.get_template(template_name)

    output = template.render(
        project_name=project_name,
        resource_name=resource_name
    )

    (destination_dir / "README.md").write_text(output, encoding="utf-8")

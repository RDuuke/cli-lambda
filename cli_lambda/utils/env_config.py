import json
from pathlib import Path


def load_env_config() -> dict:
    config_path = Path(__file__).parent.parent / "env.json"
    if not config_path.exists():
        raise FileNotFoundError("Archivo env.json no encontrado en cli_lambda/. Agrega uno con configuración de CodeArtifact.")
    
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)

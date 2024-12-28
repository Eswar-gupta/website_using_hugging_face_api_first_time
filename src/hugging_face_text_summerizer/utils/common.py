from pathlib import Path
import yaml
from typing import Dict, Any,Union
import os,sys

ROOT_dir = Path(__file__).parent.parent.parent.parent.absolute()
sys.path.append(str(ROOT_dir))


def read_yaml_file(file_path: Union[str,Path])->Dict[str, Any]:
    yaml_path = Path(file_path)
    if not yaml_path.exists():
        raise FileNotFoundError(f"{yaml_path} not found")
    
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
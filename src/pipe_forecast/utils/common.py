import os
from box.exceptions import BoxValueError
import yaml
from pipe_forecast import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Lee un archivo YAML y devuelve su contenido como un objeto ConfigBox.
    
    Args:
        path_to_yaml (Path): Ruta al archivo YAML.

    Raises:
        ValueError: Si el archivo YAML está vacío.
        e: Excepción genérica para cualquier otro error.

    Returns:
        ConfigBox: Contenido del archivo YAML como un objeto ConfigBox.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"Archivo YAML: {path_to_yaml} cargado con éxito")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("El archivo YAML está vacío")
    except Exception as e:
        raise e

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Crea una lista de directorios especificados.
    
    Args:
        path_to_directories (list): Lista de rutas de los directorios a crear.
        verbose (bool, opcional): Muestra un mensaje de log si es True. Por defecto es True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Directorio creado en: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Guarda un diccionario de datos en un archivo JSON.
    
    Args:
        path (Path): Ruta al archivo JSON.
        data (dict): Datos a guardar en el archivo JSON.
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"Archivo JSON guardado en: {path}")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Carga datos desde un archivo JSON y los devuelve como un objeto ConfigBox.
    
    Args:
        path (Path): Ruta al archivo JSON.

    Returns:
        ConfigBox: Datos del archivo JSON como atributos de clase en lugar de un diccionario.
    """
    with open(path) as f:
        content = json.load(f)
    logger.info(f"Archivo JSON cargado con éxito desde: {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any, path: Path):
    """
    Guarda datos en un archivo binario.
    
    Args:
        data (Any): Datos a guardar como binario.
        path (Path): Ruta al archivo binario.
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"Archivo binario guardado en: {path}")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Carga datos desde un archivo binario.
    
    Args:
        path (Path): Ruta al archivo binario.

    Returns:
        Any: Objeto almacenado en el archivo binario.
    """
    data = joblib.load(path)
    logger.info(f"Archivo binario cargado desde: {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """
    Obtiene el tamaño de un archivo en KB.
    
    Args:
        path (Path): Ruta del archivo.

    Returns:
        str: Tamaño del archivo en KB.
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"
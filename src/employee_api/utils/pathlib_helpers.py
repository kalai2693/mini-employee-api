from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def get_data_directory() -> Path:
    return get_project_root() / "data"


def get_data_file(filename: str = "employees.json") -> Path:
    return get_data_directory() / filename

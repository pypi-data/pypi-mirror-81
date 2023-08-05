from .git import is_git, git_tagger, save_server_repositories_state, register_server_repositories, ensure_server, ensure_server_from_files, registry_from_server, server_state
from .arch import print_registry_tree, tagged_paths_to_tree, registry_paths, state_paths
from .tools import load_json, json_dump
from pathlib import Path


def print_server_registry_tree(base_path=Path.home()):
    registry = registry_from_server(base_path)
    print_registry_tree(registry, base_path)
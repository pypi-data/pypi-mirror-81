import os
from pathlib import Path
import git
from .tools import load_json, json_dump
from .defaults import DEFAULT_REPOSITORY_REGISTERY_FILENAME, DEFAULT_REPOSITORY_STATE_FILENAME


def is_git(path):
    path = Path(path)
    if not path.is_dir():
        return False
    dir_list = os.listdir(path)
    if ".git" not in dir_list:
        return False
    git_folder = path.joinpath(".git")
    if git_folder.is_dir():
        return True
    return False

def git_tagger(path):
    if is_git(path):
        return ["GitRepo"]
    return []


def _find_git_repositories(path=Path()):
    path = Path(path)
    repositories = []
    if is_git(path):
        repositories.append(path)
    else:
        for p in os.listdir(path):
            next_path = path.joinpath(p)
            if next_path.is_dir():
                repositories += _find_git_repositories(next_path)
    return repositories

def find_git_repositories(path=Path()):
    """
        Recursively looks for git repositories
        Starting at path
    """
    return [git.Repo(repo) for repo in _find_git_repositories(path)]

def _get_repo_remote(repo):
    remote = ""
    remotes = repo.remotes
    if remotes:
        urls = [url for url in remotes[0].urls]
        if urls:
            remote = urls[0]
    return remote

def _repo_name(repo):
    directory = Path(repo.working_dir)
    name = directory.stem
    return name

def _gather_repo_info(repo):
    home = Path.home()
    directory = Path(repo.working_dir)
    name = _repo_name(repo)
    data = {
        "path": str(directory.relative_to(home)),
        "remote": _get_repo_remote(repo),
    }
    return name, data

def gather_repos_info(repos):
    """
        Given a list of git.Repo object,
        Return their registery values
    """
    repositories = {}
    for repo in repos:
        name, data = _gather_repo_info(repo)
        repositories[name] = data
    return repositories

def _gather_repo_states(repo):
    name = _repo_name(repo)
    data = {
        "branch": repo.active_branch.name,
    }
    return name, data


def gather_repo_states(repos):
    """
        Given a list of git.Repo object,
        Return their current states
    """
    repositories = {}
    for repo in repos:
        name, data = _gather_repo_states(repo)
        repositories[name] = data
    return repositories


def registry_from_server(path=Path()):
    repositories = find_git_repositories(path)
    data = gather_repos_info(repositories)
    return data

def server_state(path=Path()):
    repositories = find_git_repositories(path)
    data = gather_repo_states(repositories)
    return data


def register_server_repositories(file=DEFAULT_REPOSITORY_REGISTERY_FILENAME, path=Path()):
    """
        Register all repositories found in the server
    """
    data = registry_from_server(path)
    json_dump(file, data)

def save_server_repositories_state(file=DEFAULT_REPOSITORY_STATE_FILENAME, path=Path()):
    """
        Save the server's repositories states
    """
    data = server_state(path)
    json_dump(file, data)

def _ensure_repo(registry, name, data, base_path=Path.home()):
    base_path = Path(base_path)
    registered_repo = registry.get(name)
    if registered_repo is None:
        raise Exception("Repo {name} is not in registry".format(
        name=name,
    ))
    path = registered_repo.get("path")
    if path is None:
        raise Exception("No path found in registery for {name}".format(
        name=name,
    ))
    path = base_path.joinpath(path)
    remote = registered_repo.get("remote")
    if remote is None:
        raise Exception("No remote found in registery for {name}".format(
        remote=remote,
    ))
    if not path.exists():
        print("Cloning missing repo {repo} to {path}".format(
            repo=name,
            path=path
        ))
        git.Repo.clone_from(remote, path, **data)
    repo = git.Repo(path)
    branch = data.get("branch")
    if branch is not None:
        active_branch = repo.active_branch.name
        if active_branch != branch:
            raise Exception("Active branch for repo {name} is {active_branch} instend of {branch}".format(
            name=name,
            active_branch=active_branch,
            branch=branch,
        ))

def ensure_server(registry, state, path=Path.home()):
    errors = []
    for name, data in state.items():
        try:
            _ensure_repo(registry, name, data, path)
        except Exception as e:
            errors.append(e)
    if errors:
        for e in errors:
            print(e)

def ensure_server_from_files(registry_file, state_file, path=Path.home()):
    registry = load_json(registry_file)
    state = load_json(state_file)
    ensure_server(registry, state, path)



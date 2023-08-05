from pathlib import Path
from os.path import join as joinpath
from treelib import Node, Tree


def paths_to_dict_tree(path_list, base_path=Path.home()):
    tree = {}
    base_path = Path(base_path).resolve()
    for path in path_list:
        path = base_path.joinpath(path).resolve()
        parent = tree
        for part in path.parts:
            if part not in parent:
                parent[part] = {}
            parent = parent[part]
    return tree


def registry_to_dict_tree(registry, base_path=Path.home()):
    path_list = [
        repo["path"]
        for repo in registry.values()
    ]
    return paths_to_dict_tree(path_list, base_path)


def paths_to_tree(path_list, base_path=Path.home()):
    tree = Tree()
    root = Path().resolve().root
    tree.create_node(root, root)

    base_path = Path(base_path).resolve()
    for path in path_list:
        path = base_path.joinpath(path).resolve()
        if len(path.parts) < 2:
            continue
        parent = path.parts[0]
        parts = path.parts[1:]
        for part in parts:
            current_path = joinpath(parent, part)
            if not tree.contains(current_path):
                tree.create_node(part, current_path, parent=parent)
            parent = current_path
    return tree

def tagged_paths_to_tree(path_list, base_path=Path.home(), taggers=[]):
    """
        Same as paths_to_tree but add tags
        taggers must contains functions in format

        def tagger(path: str) -> List[str]:
            ...
    """
    def tag_path(path):
        tags = []
        for func in taggers:
            tags += func(path)
        if not tags:
            return ""
        return " ({tags})".format(tags=", ".join(tags))

    tree = Tree()
    root = Path().resolve().root
    tree.create_node(root, root)

    base_path = Path(base_path).resolve()
    for path in path_list:
        path = base_path.joinpath(path).resolve()
        if len(path.parts) < 2:
            continue
        parent = path.parts[0]
        parts = path.parts[1:]
        for part in parts:
            current_path = joinpath(parent, part)
            if not tree.contains(current_path):
                tree.create_node(part + tag_path(current_path), current_path, parent=parent)
            parent = current_path
    return tree

def registry_paths(registry):
    return [
        repo["path"]
        for repo in registry.values()
    ]

def state_paths(registry, server_state):
    return [
        data["path"]
        for repo, data in registry.items()
        if repo in server_state
    ]

def registry_to_tree(registry, base_path=Path.home()):
    path_list = registry_paths(registry)
    return paths_to_tree(path_list, base_path)

def server_to_tree(registry, server_state, base_path=Path.home()):
    path_list = state_paths(registry, server_state)
    return paths_to_tree(path_list, base_path)


def paths_tree_string(path_list, base_path=Path.home()):
    tree = paths_to_tree(path_list, base_path)
    return tree.show(stdout=False)

def registry_tree_string(registry, base_path=Path.home()):
    tree = registry_to_tree(registry, base_path)
    return tree.show(stdout=False)

def server_tree_string(registry, server_state, base_path=Path.home()):
    tree = server_to_tree(registry, server_state, base_path)
    return tree.show(stdout=False)

def print_registry_tree(registry, base_path=Path.home()):
    tree = registry_to_tree(registry, base_path)
    tree.show()

# gitArch

Tool to maintain servers configurations homogeneous.



* Starting from a given path (default is user home path), it will find all git repositories recursively as relative path
* From that, we can make a registry (i.e. define the current server as a standard) or a state (to reproduce the server state)
* Using a registry and a server state, we can reproduce the server architecture



```python
from gitArch import *

# Saving a server state
save_server_repositories_state()	# Save the server's repositories states in a json file,
									# Using default filename and home path as default path
register_server_repositories()		# Register all repositories found in the server
									# Using default filename and home path as default path
    
# Applying a state on your machine    
ensure_server(registry, state)      # Using the registry, it will download all repositories mentionned in state
									# (as dict object) Using home path as default path
ensure_server_from_files			# Using the registry, it will download all repositories mentionned in state
									# (as string defining json files) Using home path as default path
```





```python
from gitArch import *

print_registry_tree(registry)		# Print the architecture tree from given path (default: home) 
load_json, json_dump				# Wrapper around json load/dumps
```



## Usage

```python
from gitArch import tagged_paths_to_tree, registry_from_server, registry_paths, git_tagger

registry = registry_from_server("/some/paths")
paths = registry_paths(registry)
tagged_paths_to_tree(paths, taggers=[git_tagger]).show()
```



## Todo

* make `register_server_repositories` able of extending existing registry
* make a module `ArchTools` with all path utilities
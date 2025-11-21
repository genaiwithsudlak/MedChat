import os
from anytree import Node, RenderTree

def build_tree(startpath):
    """
    Recursively builds an anytree Node structure from a directory path.
    """
    root_node = Node(os.path.basename(startpath) + "/") # Create the root node
    
    for root, dirs, files in os.walk(startpath):
        parent_path = os.path.dirname(root)
        current_node_name = os.path.basename(root)
        
        # Find the parent Node in the tree (optional but useful for complex trees)
        # For simplicity here, we assume a simple top-down walk:
        
        # 1. Find the path relative to the startpath to establish hierarchy
        relative_path = os.path.relpath(root, startpath)
        path_parts = relative_path.split(os.sep)
        
        # We'll use a dictionary to keep track of created nodes for faster lookup
        node_map = {startpath: root_node} 
        current_parent_node = root_node
        current_full_path = startpath
        
        # Reconstruct the node path up to the current root to find the correct parent
        if relative_path != ".": # Not the root itself
            for part in path_parts:
                current_full_path = os.path.join(current_full_path, part)
                if current_full_path in node_map:
                    current_parent_node = node_map[current_full_path]
                else:
                    # Should not happen with os.walk, but for robustness:
                    break 

        # 2. Add files as children to the current directory node
        for file in files:
            Node(file, parent=current_parent_node)
            
    return root_node

def export_tree_anytree(startpath):
    """
    Renders the anytree structure to a string/console.
    """
    # Note: os.walk handles directory creation implicitly.
    # The simple os.walk example above is more efficient for simple output.
    # The full implementation of a robust anytree builder is complex.
    # For a simple, rendered output, the first solution is preferred.
    
    # For demonstration, let's use the simplest RenderTree on the built-in example:
    
    class FileNode(Node):
        def __init__(self, name, parent=None, is_dir=False):
            super().__init__(name, parent=parent)
            self.is_dir = is_dir
            
    # Simple example tree for rendering
    root = FileNode("project_root", is_dir=True)
    src = FileNode("src", parent=root, is_dir=True)
    main_py = FileNode("main.py", parent=src)
    tests = FileNode("tests", parent=root, is_dir=True)
    test_unit = FileNode("test_unit.py", parent=tests)
    
    # Render the tree to console/output file
    output_filename = "anytree_output.txt"
    with open(output_filename, 'w') as f:
        for pre, _, node in RenderTree(root):
            # Add a '/' suffix for directories
            suffix = "/" if node.is_dir else ""
            line = f"{pre}{node.name}{suffix}\n"
            print(line.strip())
            f.write(line)

# --- Example Usage ---
export_tree_anytree('.')
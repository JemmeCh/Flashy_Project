from __future__ import annotations

from typing import Optional, List, Literal
from flashy.models.parameters.definition import ParameterDefinition
from flashy.models.parameters.container import ParameterContainer


class TreeNode:
    def __init__(
        self,
        name: str,
        *,
        node_type: Literal["root", "container", "group", "parameter"] = "group",
        definition: Optional[ParameterDefinition] = None,
        container: Optional[ParameterContainer] = None,
        parent: Optional["TreeNode"] = None,
    ):
        self.name = name
        self.node_type = node_type  # "root" | "container" | "group" | "parameter"
        
        self.definition = definition
        self.container = container
        
        self.parent: Optional["TreeNode"] = parent
        self.children: List["TreeNode"] = []
    
    # -------------------------
    # Tree structure operations
    # -------------------------
    
    def add_child(self, child: "TreeNode") -> None:
        child.parent = self
        self.children.append(child)
    
    def remove_child(self, child: "TreeNode") -> None:
        if child in self.children:
            self.children.remove(child)
            child.parent = None
    
    def child(self, row: int) -> "TreeNode | None":
        try:
            return self.children[row]
        except Exception:
            return None
    
    def child_count(self) -> int:
        return len(self.children)
    
    def row(self) -> int:
        if self.parent is None:
            return 0
        return self.parent.children.index(self)
    
    def find_path(self, *path: str) -> Optional["TreeNode"]:
        node = self
        
        for name in path:
            node = next(
                (child for child in node.children if child.display_name() == name),
                None,
            )
            if node is None:
                return None
        
        return node
    
    # -------------------------
    # Display helpers
    # -------------------------
    
    def display_name(self) -> str:
        if self.definition is not None:
            return self.definition.name
        return self.name
    
    def description(self) -> str:
        if self.definition:
            return self.definition.description
        return ""
    
    # -------------------------
    # Value access (leaf nodes)
    # -------------------------
    
    def get_value(self):
        if not self.definition or not self.container:
            return None
        return self.container.get_value(self.definition.key)
    
    def set_value(self, value):
        if self.definition and self.container:
            self.container.set_value(self.definition.key, value)
    
    # -------------------------
    # Helper functions
    # -------------------------
    
    @property
    def is_root(self):
        return self.node_type == "root"
    @property
    def is_container(self):
        return self.node_type == "container"
    @property
    def is_group(self):
        return self.node_type == "group"
    @property
    def is_parameter(self):
        return self.node_type == "parameter"
    
    # -------------------------
    # __func__
    # -------------------------
    
    def __eq__(self, other: object) -> bool:
        return self is other
    
    def __repr__(self) -> str:
        return f"<Node {self.node_type}: {self.display_name()}>"
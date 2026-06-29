from __future__ import annotations

from typing import Optional, List, Literal
from flashy.models.parameters.definition import ParameterDefinition
from flashy.models.parameters.container import ParameterContainer


class TreeNode:
    """
    Node of a hierarchical configuration tree.
    
    This class represents a generic tree structure used to organize parameter
    definitions and configuration containers in a hierarchical manner. Nodes
    can represent groups, parameters, containers, or the root of the tree.
    
    Each node may optionally hold a :class:`ParameterDefinition` and/or a
    :class:`ParameterContainer`, allowing it to act as both a structural and
    data-binding element within configuration trees.
    
    :ivar name: Internal name of the node.
    :vartype name: str
    :ivar node_type: Type of node ("root", "container", "group", "parameter").
    :vartype node_type: Literal["root", "container", "group", "parameter"]
    :ivar definition: Optional parameter definition associated with the node.
    :vartype definition: ParameterDefinition | None
    :ivar container: Optional parameter container associated with the node.
    :vartype container: ParameterContainer | None
    :ivar parent: Parent node in the tree, if any.
    :vartype parent: TreeNode | None
    :ivar children: List of child nodes.
    :vartype children: list[TreeNode]
    """
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
        """
        Add a child node to this node. The child's parent reference is updated automatically.
        
        :param child: Node to add as a child.
        :type child: TreeNode
        """
        child.parent = self
        self.children.append(child)
    
    def remove_child(self, child: "TreeNode") -> None:
        """
        Remove a child node from this node. If the child exists, it is 
        detached and its parent reference is cleared.
        
        :param child: Node to remove.
        :type child: TreeNode
        """
        if child in self.children:
            self.children.remove(child)
            child.parent = None
    
    def child(self, row: int) -> "TreeNode | None":
        """
        Return the child node at a given index.
        
        :param row: Index of the child.
        :type row: int
        :returns: Child node or None if index is invalid.
        :rtype: TreeNode | None
        """
        try:
            return self.children[row]
        except Exception:
            return None
    
    def child_count(self) -> int:
        """
        Return the number of children of this node.
        
        :returns: Number of child nodes.
        :rtype: int
        """
        return len(self.children)
    
    def row(self) -> int:
        """
        Return this node's index within its parent's children list.
        
        :returns: Index position in parent, or 0 if root.
        :rtype: int
        """
        if self.parent is None:
            return 0
        return self.parent.children.index(self)
    
    def find_path(self, *path: str) -> Optional["TreeNode"]:
        """
        Traverse the tree following a sequence of display names. Each path element 
        is matched against :meth:`display_name`.
        
        :param path: Sequence of node display names.
        :type path: str
        :returns: Target node if found, otherwise None.
        :rtype: TreeNode | None
        """
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
        """
        Return the display name of the node.
        
        If a :class:`ParameterDefinition` is attached, its name is used;
        otherwise the internal node name is returned.
        
        :returns: Display name of the node.
        :rtype: str
        """
        if self.definition is not None:
            return self.definition.name
        return self.name
    
    def description(self) -> str:
        """
        Return the node description if a definition is attached.
        
        :returns: Node description or empty string.
        :rtype: str
        """
        if self.definition:
            return self.definition.description
        return ""
    
    # -------------------------
    # Value access (leaf nodes)
    # -------------------------
    
    def get_value(self):
        """
        Retrieve the value associated with this node. Only applies if the node 
        is bound to a container and definition.
        
        :returns: Stored parameter value or None.
        """
        if not self.definition or not self.container:
            return None
        return self.container.get_value(self.definition.key)
    
    def set_value(self, value):
        """
        Set the value associated with this node. Only applies if the node 
        is bound to a container and definition.
        
        :param value: New value to assign.
        """
        if self.definition and self.container:
            self.container.set_value(self.definition.key, value)
    
    # -------------------------
    # Helper functions
    # -------------------------
    
    @property
    def is_root(self):
        """Whether this node is the root of the tree."""
        return self.node_type == "root"
    @property
    def is_container(self):
        """Whether this node represents a container."""
        return self.node_type == "container"
    @property
    def is_group(self):
        """Whether this node represents a group."""
        return self.node_type == "group"
    @property
    def is_parameter(self):
        """Whether this node represents a parameter leaf."""
        return self.node_type == "parameter"
    
    # -------------------------
    # __func__
    # -------------------------
    
    def __eq__(self, other: object) -> bool:
        return self is other
    
    def __repr__(self) -> str:
        return f"<Node {self.node_type}: {self.display_name()}>"
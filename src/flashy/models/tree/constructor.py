import msgspec

from flashy.models.tree.node import TreeNode
from flashy.detectors.map import DETECTOR_MAP
from flashy.digitizers.map import DIGITIZER_MAP

from typing import TYPE_CHECKING, List, Any
if TYPE_CHECKING:
    from flashy.models.user.config import UserConfig
    from flashy.models.analysis.config import AnalysisConfig
    from flashy.detectors.config import DetectorsConfig
    from flashy.detectors.detector import Detector
    from flashy.digitizers.config import DigitizersConfig
    from flashy.digitizers.digitizer import Digitizer


# =======================================================================
# Helper methods 
# =======================================================================

def create_root(root_name: str) -> TreeNode:
    """
    Create a root node for a configuration tree.
    
    :param root_name: Name of the root node.
    :type root_name: str
    :returns: Newly created root :class:`TreeNode`.
    :rtype: TreeNode
    """
    return TreeNode(
        name=root_name,
        parent=None,
        node_type="root",
        definition=None,
    )

def find_by_display_name(name: str, mapping_values):
    """
    Find an item in a mapping list by its display name.
    
    :param name: Display name to search for.
    :type name: str
    :param mapping_values: Iterable of objects containing a ``display_name`` attribute.
    :returns: Matching item or None if not found.
    """
    for item in mapping_values:
        if item.display_name == name:
            return item
    return None

def convert_config(tag, values, config_cls):
    """
    Convert a raw dictionary into a typed configuration object.
    
    This function wraps :func:`msgspec.convert` to attach a tag and convert
    values into the target configuration class.
    
    :param tag: Tag used for polymorphic decoding.
    :param values: Dictionary of configuration values.
    :param config_cls: Target configuration class type.
    :returns: Instantiated configuration object.
    """
    return msgspec.convert(
        {
            "tag": tag,
            "values": values,
        },
        type=config_cls,
    )

def ensure_path(parent_node: TreeNode, path: List[str]) -> TreeNode:
    """
    Ensure that a hierarchical path exists in a tree. Missing intermediate group 
    nodes are created automatically.
    
    :param parent_node: Starting node of the traversal.
    :type parent_node: TreeNode
    :param path: Sequence of group names defining the path.
    :type path: list[str]
    :returns: Final node corresponding to the last path segment.
    :rtype: TreeNode
    """
    current = parent_node
    for segment in path:
        next_node = next(
            (c for c in current.children
            if c.node_type == "group" and c.name == segment),
            None,
        )
        
        if next_node is None:
            next_node = TreeNode(
                name=segment,
                parent=current,
                node_type="group",
            )
            current.add_child(next_node)
        
        current = next_node
    return current

def add_container_parameters(parent_node: TreeNode, container):
    """
    Add all parameters from a container into a tree structure. Each parameter is 
    inserted under its defined hierarchical path.
    
    :param parent_node: Root node to attach parameters to.
    :type parent_node: TreeNode
    :param container: Parameter container exposing DEFINITIONS.
    """
    for param in container.DEFINITIONS.values():
        group_node = ensure_path(
            parent_node=parent_node,
            path=param.path.split('/')
        )
        node = TreeNode(
            name=param.name,
            parent=group_node,
            node_type='parameter',
            definition=param,
            container=container
        )
        group_node.add_child(node)

def get_branch_values(node: "TreeNode") -> dict[str, Any]:
    """
    Recursively collect parameter values from a tree branch.
    
    :param node: Root node of the branch.
    :type node: TreeNode
    :returns: Dictionary mapping parameter keys to values.
    :rtype: dict[str, Any]
    """
    values = {}
    
    for child in node.children:
        if not child.is_parameter:
            values.update(get_branch_values(child))
            continue
        assert child.definition
        values[child.definition.key] = child.get_value()
    return values

def combine_root_trees(trees: list[TreeNode], root_name: str = 'root') -> TreeNode:
    """
    Combine multiple trees under a single root node.
    
    :param trees: List of root trees to combine.
    :type trees: list[TreeNode]
    :param root_name: Name of the new combined root.
    :type root_name: str
    :returns: New root node containing all input trees.
    :rtype: TreeNode
    """
    root_node = create_root(root_name)
    for tree in trees:
        root_node.add_child(tree)
    return root_node

# =======================================================================
# Tree constructer methods 
# =======================================================================

def construct_user_tree(config: "UserConfig", root_name: str = 'root') -> TreeNode:
    """
    Construct a tree representation of the user configuration.
    
    :param config: User configuration container.
    :type config: UserConfig
    :param root_name: Name of the root node.
    :type root_name: str
    :returns: Root of the constructed tree.
    :rtype: TreeNode
    """
    root_node = create_root(root_name)
    add_container_parameters(root_node, config)
    return root_node

def construct_analysis_tree(config: "AnalysisConfig", root_name: str = 'root') -> TreeNode:
    """
    Construct a tree representation of the analysis configuration.
    
    :param config: Analysis configuration container.
    :type config: AnalysisConfig
    :param root_name: Name of the root node.
    :type root_name: str
    :returns: Root of the constructed tree.
    :rtype: TreeNode
    """
    root_node = create_root(root_name)
    add_container_parameters(root_node, config)
    return root_node

def construct_digitizers_trees(config: "DigitizersConfig", root_name: str = "root") -> TreeNode:
    """
    Construct a hierarchical tree of digitizer configurations.
    
    Each digitizer is grouped under its own container node, and each channel
    is represented as a subgroup containing parameter nodes.
    
    :param config: Digitizer configuration container.
    :type config: DigitizersConfig
    :param root_name: Name of the root node.
    :type root_name: str
    :returns: Root node of the digitizer tree.
    :rtype: TreeNode
    """
    root_node = create_root(root_name)
    
    for digitizer in config.digitizers:
        digitizer_group = TreeNode(
            name=digitizer.display_name,
            parent=root_node,
            node_type="container",
        )
        root_node.add_child(digitizer_group)
        
        for channel in digitizer.channels:
            channel_node = TreeNode(
                name=f"Channel {channel.get_value('ch_id')}",
                parent=digitizer_group,
                node_type="group",
            )
            digitizer_group.add_child(channel_node)
            add_container_parameters(channel_node, channel)
    return root_node

def construct_detectors_trees(config: "DetectorsConfig", root_name: str = 'root') -> TreeNode:
    """
    Construct a tree representation of detector configurations.
    
    :param config: Detector configuration container.
    :type config: DetectorsConfig
    :param root_name: Name of the root node.
    :type root_name: str
    :returns: Root node of the detector tree.
    :rtype: TreeNode
    """
    root_node = create_root(root_name)
    
    for detector in config.detectors:
        add_container_parameters(root_node, detector)
    
    return root_node

# =======================================================================
# Configuration builder methods 
# =======================================================================

def build_analysis_config(root_node: "TreeNode") -> dict[str, Any]:
    """
    Extract analysis configuration values from a tree.
    
    :param root_node: Root node of the analysis tree.
    :type root_node: TreeNode
    :returns: Dictionary of analysis parameters.
    :rtype: dict[str, Any]
    """
    return get_branch_values(root_node)

def build_digitizer_config(root_node: "TreeNode") -> "Digitizer":
    """
    Build a digitizer configuration object from a tree.
    
    :param root_node: Root node of the digitizer tree.
    :type root_node: TreeNode
    :returns: Typed digitizer configuration.
    :rtype: Digitizer
    :raises NotImplementedError: If digitizer type is not registered.
    """
    digitizer = find_by_display_name(
        root_node.name,
        DIGITIZER_MAP.values(),
    )
    
    if digitizer is None:
        raise NotImplementedError(
            "This digitizer is not in the DIGITIZER_MAP."
        )
    
    channels = [
        {"values": get_branch_values(child)}
        for child in root_node.children
    ]
    
    return msgspec.convert(
        {
            "tag": digitizer.tag_cls,
            "channels": channels,
        },
        type=digitizer.config_cls,
    )

def build_detectors_config(root_node: "TreeNode") -> List["Detector"]:
    """
    Build detector configuration objects from a tree.
    
    :param root_node: Root node of the detector tree.
    :type root_node: TreeNode
    :returns: List of detector configuration objects.
    :rtype: list[Detector]
    """
    detectors = []
    
    for child in root_node.children:
        info = find_by_display_name(child.display_name(), DETECTOR_MAP.values())
        if info is None:
            continue
        
        config = convert_config(
            info.tag_cls,
            get_branch_values(child),
            info.config_cls,
        )
        detectors.append(config)
    
    return detectors

# =======================================================================
# Other/Test methods 
# =======================================================================

def _make_test_processing_config():
    from flashy.models.processing_config import ProcessingConfig
    from flashy.models.acquisition_config import AcquisitionConfig
    from flashy.digitizers.caen_dt5781.channel import CaenDT5781Channel
    from flashy.digitizers.caen_dt5781.config import CaenDT5781Config
    from flashy.detectors.bergoz_bct.bergoz_bct import BergozBCT
    
    t_bergoz = BergozBCT.create_default()
    t_caen_ch0 = CaenDT5781Channel.create_default()
    t_caen_ch1 = CaenDT5781Channel.create_default()
    t_analysis = _make_test_analysis_config()
    test_config = ProcessingConfig(
        acquisition=AcquisitionConfig(
            digitizer=CaenDT5781Config([
                t_caen_ch0, 
                t_caen_ch1
            ]),
            detectors=[t_bergoz, t_bergoz]
        ),
        analysis=t_analysis
    )
    return test_config

def _make_test_user_config():
    from flashy.models.user.config import UserConfig
    
    test_config = UserConfig()
    return test_config

def _make_test_analysis_config():
    from flashy.models.analysis.config import AnalysisConfig
    return AnalysisConfig.create_default()

if __name__ == '__main__':
    from flashy.models.analysis.config import AnalysisConfig
    #tree = construct_processing_tree(_make_test_processing_config())
    """ print(tree.children)
    print('-'*80)
    print(tree.children[0].children[0].children)
    print(tree.children[0].children[1].children)
    print('-'*80)
    print(tree.children[1].children[0].children[0].children)
    print(tree.children[1].children[1].children[0].children)
    print('-'*80)
    print(tree.children[2].children[0].children[0].children)
    print(tree.children[2].children[0].children[1].children)
    print(tree.children[2].children[0].children[2].children) """
    
    #tree = construct_user_tree(_make_test_user_config())
    test = _make_test_analysis_config()
    tree = construct_analysis_tree(test)
    config = AnalysisConfig.from_tree(tree)
    assert test == config
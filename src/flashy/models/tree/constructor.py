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

def ensure_path(parent_node: TreeNode, path: List[str]) -> TreeNode:
    current = parent_node
    for segment in path:
        next_node = None
        for child in current.children:
            if child.node_type == "group" and child.name == segment:
                next_node = child
                break
        
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

def combine_root_trees(trees: list[TreeNode], root_name: str = 'root') -> TreeNode:
    root_node = TreeNode(
        name=root_name,
        parent=None,
        node_type='root',
        definition=None,
    )
    
    for tree in trees:
        root_node.add_child(tree)
    
    return root_node

# =======================================================================
# Tree constructer methods 
# =======================================================================

def construct_user_tree(config: "UserConfig", root_name: str = 'root') -> TreeNode:
    root_node = TreeNode(
        name=root_name,
        parent=None,
        node_type='root',
        definition=None,
    )
    add_container_parameters(
        parent_node=root_node,
        container=config
    )
    
    return root_node

def construct_analysis_tree(config: "AnalysisConfig", root_name: str = 'root') -> TreeNode:
    root_node = TreeNode(
        name=root_name,
        parent=None,
        node_type='root',
        definition=None,
    )
    add_container_parameters(
        parent_node=root_node,
        container=config
    )
    return root_node

def construct_digitizers_trees(config: "DigitizersConfig", root_name: str = "root") -> TreeNode:
    root_node = TreeNode(
        name=root_name,
        parent=None,
        node_type="root",
        definition=None,
    )
    
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
            add_container_parameters(
                parent_node=channel_node,
                container=channel,
            )
    
    return root_node

def construct_detectors_trees(config: "DetectorsConfig", root_name: str = 'root') -> TreeNode:
    root_node = TreeNode(
        name=root_name,
        parent=None,
        node_type='root',
        definition=None,
    )
    
    for detector in config.detectors:
        add_container_parameters(
            parent_node=root_node,
            container=detector
        )
    
    return root_node

# =======================================================================
# Configuration builder methods 
# =======================================================================

def get_branch_values(node: "TreeNode") -> dict[str, Any]:
    values = {}
    
    for child in node.children:
        if not child.is_parameter:
            values.update(get_branch_values(child))
            continue
        assert child.definition
        values[child.definition.key] = child.get_value()
    
    return values

def build_analysis_config(root_node: "TreeNode") -> dict[str, Any]:
    return get_branch_values(root_node)

def build_digitizer_config(root_node: "TreeNode") -> "Digitizer":
    digitizer_name = root_node.name
    
    correct_digitizer = None
    for dig in DIGITIZER_MAP.values():
        if dig.display_name == digitizer_name:
            correct_digitizer = dig
    if correct_digitizer is None:
        raise NotImplementedError("This digitizer is not in the DIGITIZER_MAP.")
    
    channels = []
    for child in root_node.children:
        val = {
            "values": get_branch_values(child)
        }
        channels.append(val)
    
    digitizer_ch_values = {
        "tag": correct_digitizer.tag_cls,
        "channels": channels
    }
    digitizer = msgspec.convert(digitizer_ch_values, type=correct_digitizer.config_cls)
    
    return digitizer

def build_detectors_config(root_node: "TreeNode") -> List["Detector"]:
    detectors = []
    
    for child in root_node.children:
        display_name = child.display_name()
        for info in DETECTOR_MAP.values():
            if display_name == info.display_name:
                val = {
                    "tag": info.tag_cls,
                    "values": get_branch_values(child)
                }
                config = msgspec.convert(val, type=info.config_cls)
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
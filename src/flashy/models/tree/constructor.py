from typing import TYPE_CHECKING, List

from flashy.models.tree.node import TreeNode
if TYPE_CHECKING:
    from flashy.models.processing_config import ProcessingConfig


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
            path=[param.path]
        )
        node = TreeNode(
            name=param.name,
            parent=parent_node,
            node_type='parameter',
            definition=param,
            container=container
        )
        group_node.add_child(node)

def construct_tree(config: "ProcessingConfig", root_name: str = 'root'):
    
    # Root
    root_node = TreeNode(
        name=root_name,
        parent=None,
        node_type='root',
        definition=None,
    )
    
    # Analysis
    analysis_node = TreeNode(
        name='Analysis',
        parent=root_node,
        node_type='container',
        definition=None,
    )
    add_container_parameters(
        parent_node=analysis_node,
        container=config.analysis
    )
    
    # Detectors
    detector_node = TreeNode(
        name='Detectors',
        parent=root_node,
        node_type='container',
        definition=None
    )
    for assignement in config.acquisition.detector_assignments:
        channel_node = ensure_path(
            parent_node=detector_node,
            path=[f'Channel {assignement.digitizer_channel}']
        )
        add_container_parameters(
            parent_node=channel_node,
            container=assignement.detector
        )
    
    # Digitizers
    digitizer_node = TreeNode(
        name='Digitizer',
        parent=root_node,
        node_type='container',
        definition=None
    )
    for channel in config.acquisition.digitizer.channels:
        channel_node = ensure_path(
            parent_node=digitizer_node,
            path=[f'Channel {channel.channel_id}']
        )
        add_container_parameters(
            parent_node=channel_node,
            container=channel
        )
    
    
    root_node.add_child(analysis_node)
    root_node.add_child(detector_node)
    root_node.add_child(digitizer_node)
    return root_node



def _make_test_config():
    from flashy.models.processing_config import AcquisitionConfig, ProcessingConfig
    from flashy.models.analysis.config import AnalysisConfig
    from flashy.digitizers.caen_dt5781.channel import CaenDT5781Channel
    from flashy.digitizers.caen_dt5781.config import CaenDT5781Config
    from flashy.detectors.detector import DetectorAssignment
    from flashy.detectors.bergoz_bct.bergoz_bct import BergozBCT
    
    t_bergoz = BergozBCT.create_default()
    t_caen_ch0 = CaenDT5781Channel.create_default(channel_id=0)
    t_caen_ch1 = CaenDT5781Channel.create_default(channel_id=1)
    t_analysis = AnalysisConfig.create_default()
    test_config = ProcessingConfig(
        acquisition=AcquisitionConfig(
            digitizer=CaenDT5781Config([
                t_caen_ch0, 
                t_caen_ch1
            ]),
            detector_assignments=[
                DetectorAssignment(
                    detector=t_bergoz,
                    digitizer_channel=0
                    ),
                DetectorAssignment(
                    detector=t_bergoz,
                    digitizer_channel=1
                    ),
            ]
        ),
        analysis=t_analysis
    )
    return test_config

if __name__ == '__main__':
    tree = construct_tree(_make_test_config())
    print(tree.children)
    print('-'*80)
    print(tree.children[0].children[0].children)
    print(tree.children[0].children[1].children)
    print('-'*80)
    print(tree.children[1].children[0].children[0].children)
    print(tree.children[1].children[1].children[0].children)
    print('-'*80)
    print(tree.children[2].children[0].children[0].children)
    print(tree.children[2].children[0].children[1].children)
    print(tree.children[2].children[0].children[2].children)
    #for c in tree.children:
    #    print(c.description())
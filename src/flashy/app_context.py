from flashy.services.data_loader import DataLoader
from flashy.services.export_service import DataExporter
from flashy.services.analysis_service import AnalysisService
from flashy.services.logger.logger_service import setup_logging
from flashy.models.tree.constructor import (
    construct_user_tree,
    construct_analysis_tree,
    construct_digitizers_trees,
    construct_detectors_trees,
    combine_root_trees
)
from flashy.models.processing_config import ProcessingConfig
from flashy.digitizers.map import DIGITIZER_MAP

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flashy.models.tree.node import TreeNode

class AppContext:
    def __init__(self) -> None:
        setup_logging()
        
        self.serv_loader = DataLoader()
        self.serv_exporter = DataExporter()
        self.serv_analysis = AnalysisService()
        
        # Load previous configuration
        configs = self.serv_loader.read_config_json_file()
        self.user_config = configs['user_config']
        self.analysis_config = configs['analysis_config']
        self.digitizers_config = configs['digitizers_config']
        self.detectors_config = configs['detectors_config']
        
        # Construct parameter trees
        self.user_tree = construct_user_tree(self.user_config, root_name='User')
        self.analysis_tree = construct_analysis_tree(self.analysis_config, root_name='Analysis')
        self.digitizers_tree = construct_digitizers_trees(self.digitizers_config, root_name='Digitizers')
        self.detectors_tree = construct_detectors_trees(self.detectors_config, root_name='Detectors')
    
    @property
    def analyser_tree(self) -> "TreeNode":
        return combine_root_trees(
            [
                self.analysis_tree
            ]
        )
    
    @property
    def caendt5781_tree(self) -> "TreeNode":
        root_name = "caen_dt5781"
        dt5781_tree = self.digitizers_tree.find_path(
            DIGITIZER_MAP[root_name].display_name
        )
        if dt5781_tree is None: 
            raise ValueError("Couldn't find specified tree node path.")
        
        return combine_root_trees(
            trees=[
                self.analysis_tree,
                self.detectors_tree,
                dt5781_tree,
            ],
            root_name=root_name
        )
    
    @property
    def caendt5781_processing_config(self) -> ProcessingConfig:
        return ProcessingConfig.from_tree(self.caendt5781_tree)


if __name__ == '__main__':
    context = AppContext()
    print(context.caendt5781_processing_config)
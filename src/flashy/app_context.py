from flashy.services.data_loader import DataLoader
from flashy.services.export_service import DataExporter
from flashy.services.analysis_service import AnalysisService
from flashy.services.logger.logger_service import setup_logging
from flashy.models.tree.constructor import *

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
        return combine_root_trees(
            [
                self.analysis_tree,
                self.digitizers_tree, # TODO: Get only Caen digitizer branch
                self.detectors_tree
            ]
        )


if __name__ == '__main__':
    context = AppContext()
from flashy.services.data_loader import DataLoader
from flashy.services.export_service import DataExporter
from flashy.services.analysis_service import AnalysisService
from flashy.services.logger.logger_service import setup_logging
from flashy.models.tree.constructor import construct_tree


class AppContext:
    def __init__(self) -> None:
        setup_logging()
        
        self.serv_loader = DataLoader()
        self.serv_exporter = DataExporter()
        self.serv_analysis = AnalysisService()
        
        self.user_config, self.processing_config = self.serv_loader.read_config_json_file()
        
        self.root_tree = construct_tree(self.processing_config)
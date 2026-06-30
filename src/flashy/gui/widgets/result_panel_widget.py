import numpy as np

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.gui.ui.ui_result_panel_widget import Ui_ResultPanelWidget
from flashy.gui.widgets.result_table import ResultTableView
from flashy.gui.theme import get_pen

from flashy.services.normalizer import Normalizer
from flashy.services.logger.logger_service import get_logger

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    from flashy.models.analysis.result import AnalysisResult

class ResultPanelWidget(qtw.QWidget, Ui_ResultPanelWidget):
    # NOTE: This is specific to Caen's digitizer's data
    def __init__(
        self, 
        parent=None
    ):
        super().__init__(parent)
        self.setupUi(self)
        self._logger = get_logger()
        self._normalizer = Normalizer()
        
        # Put result table
        self.w_result_table = ResultTableView()
        self.layout_ResultPanel.replaceWidget(self.ResultTablePlaceholder, self.w_result_table)
        self.ResultTablePlaceholder.setParent(None)
        
        self._prepare_plots()
        
        # Connections
        self.w_result_table.pb_save_results.clicked.connect(
            self.save_results
        )
    
    def _prepare_plots(self):
        assert self.graph_top.plotItem
        assert self.graph_bot.plotItem
        assert self.graph_right.plotItem
        
        # Top graph
        self.graph_top.plotItem.setTitle('CH0 - ')
        self.graph_top.plotItem.setLabel('left', 'Voltage', units='V')
        self.graph_top.plotItem.setLabel('bottom', 'Time', units='s')
        self.graph_top.plotItem.showGrid(x=True, y=True, alpha=0.3)
        self.graph_top.plotItem.setMenuEnabled(False)
        
        # Bot graph
        self.graph_bot.plotItem.setTitle('CH1 - ')
        self.graph_bot.plotItem.setLabel('left', 'Voltage', units='V')
        self.graph_bot.plotItem.setLabel('bottom', 'Time', units='s')
        self.graph_bot.plotItem.showGrid(x=True, y=True, alpha=0.3)
        self.graph_bot.plotItem.setMenuEnabled(False)
        
        # Right graph
        self.graph_right.plotItem.setTitle('Relative voltage')
        self.graph_right.plotItem.setLabel('left', 'Relative', units='%')
        self.graph_right.plotItem.setLabel('bottom', 'Time', units='s')
        self.graph_right.plotItem.showGrid(x=True, y=True, alpha=0.3)
        self.graph_right.plotItem.setMenuEnabled(False)
    
    def _change_plot_title(self, title: str, ch: int):
        graph = [
            self.graph_top,
            self.graph_bot,
        ][ch]
        
        assert graph.plotItem
        chx = graph.plotItem.titleLabel.text.split(' - ')[0]
        graph.plotItem.setTitle(f"{chx} - {title}")
    
    @qtc.Slot('AnalysisResult')
    def change_results(
        self,
        analysis_results: "AnalysisResult",
    ) -> None:
        assert self.graph_right.plotItem
        graphs = [
            self.graph_top,
            self.graph_bot,
        ]
        
        config = analysis_results.config
        table_results = None
        
        try:
            sampling_period_ns = config.acquisition.digitizer.sampling_period_ns
            time_scale = float(config.analysis.get_value("time_scale").split(" ")[0])
            scale_factor = time_scale * sampling_period_ns
            time_axis = np.arange(0, len(analysis_results.pulse_batches[0].pulses[0])) * scale_factor
        except IndexError as e:
            self._logger.warning(f"Analysis results are empty!")
            self._logger.debug(f"analysis_results.pulse_batches={analysis_results.pulse_batches}")
            return
        except KeyError as e:
            self._logger.warning(f"{e} is not a parameter in the chosen file. Please disable the 'Use File Parameters' parameter for now.")
            self._logger.debug("Implement fallback!")
            return
        except Exception as e:
            self._logger.exception(f"An error occured: {e}")
            return
        
        self.graph_right.plotItem.clear()
        for i, (graph, batch) in enumerate(zip(graphs, analysis_results.pulse_batches)):
            # Table
            table_batch = np.array([batch.area_under_curves, batch.doses]).T
            if table_results is None:
                table_results = table_batch
            else:
                table_results = self._normalizer.append_to_result_table(table_results, table_batch)
            
            # Graphs
            assert graph.plotItem
            graph.plotItem.clear()
            detector_name = config.acquisition.detectors[i].display_name
            self._change_plot_title(detector_name, i)
            for j, p in enumerate(batch.pulses):
                peak = np.max(p)
                graph.plotItem.plot(time_axis, p, pen=get_pen(j, width=2))
                self.graph_right.plotItem.plot(time_axis, p/peak, pen=get_pen(i))
            graph.plotItem.getViewBox().autoRange()
        self.graph_right.plotItem.getViewBox().autoRange()
        
        assert table_results is not None, self._logger.exception("Table of results shouldn't be None")
        if table_results.shape[-1] == 2:
            patch = np.zeros_like(table_results)
            table_results = np.append(table_results, patch, axis=1)
        self.w_result_table.model.set_rows(table_results)
    
    @qtc.Slot(bool)
    def set_enabled_results(self, enable: bool):
        self.w_result_table.pb_save_results.setEnabled(enable)
    
    @qtc.Slot()
    def save_results(self):
        self._logger.info("Not implemented!")

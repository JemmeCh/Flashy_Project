import numpy as np

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.gui.ui.ui_result_panel_widget import Ui_ResultPanelWidget
from flashy.gui.widgets.result_table import ResultTableView
from flashy.gui.theme import get_pen

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flashy.models.analysis.result import AnalysisResult

class ResultPanelWidget(qtw.QWidget, Ui_ResultPanelWidget):
    # NOTE: This is specific to Caen's digitizer's data
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Put result table
        self.w_result_table = ResultTableView()
        self.layout_ResultPanel.replaceWidget(self.ResultTablePlaceholder, self.w_result_table)
        self.ResultTablePlaceholder.setParent(None)
        
        
        self._prepare_plots()
    
    def _prepare_plots(self):
        assert self.graph_top.plotItem
        assert self.graph_bot.plotItem
        assert self.graph_right.plotItem
        
        # Top graph
        self.graph_top.plotItem.setTitle('CH0')
        self.graph_top.plotItem.setLabel('left', 'Voltage', units='V')
        self.graph_top.plotItem.setLabel('bottom', 'Time', units='s')
        self.graph_top.plotItem.showGrid(x=True, y=True, alpha=0.3)
        self.graph_top.plotItem.setMenuEnabled(False)
        
        # Bot graph
        self.graph_bot.plotItem.setTitle('CH1')
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
        
        # TODO: Parameter for the hard coded value
        scale_factor = 1e-9 * config.acquisition.digitizer.sampling_period_ns
        time_scale = np.arange(0, len(analysis_results.pulse_batches[0].pulses[0])) * scale_factor
        
        self.graph_right.plotItem.clear()
        for i, (graph, batch) in enumerate(zip(graphs, analysis_results.pulse_batches)):
            # Table
            table_batch = np.array([batch.area_under_curves, batch.doses]).T
            if table_results is None:
                table_results = table_batch
            else: 
                table_results = np.append(table_results, table_batch, axis=1)
            
            # Graphs
            assert graph.plotItem
            graph.plotItem.clear()
            for j, p in enumerate(batch.pulses):
                peak = np.max(p)
                graph.plotItem.plot(time_scale, p, pen=get_pen(j))
                self.graph_right.plotItem.plot(time_scale, p/peak, pen=get_pen(i))
            graph.plotItem.getViewBox().autoRange()
        self.graph_right.plotItem.getViewBox().autoRange()
        
        assert table_results is not None
        if table_results.shape[-1] == 2:
            patch = np.zeros_like(table_results)
            table_results = np.append(table_results, patch, axis=1)
        self.w_result_table.model.set_rows(table_results)
    
    @qtc.Slot(bool)
    def set_enabled_results(self, enable: bool):
        self.w_result_table.pb_save_results.setEnabled(enable)

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

import queue
import copy
from typing import TYPE_CHECKING, Any, Literal, List
if TYPE_CHECKING:
    from flashy.models.processing_config import ProcessingConfig

from flashy.digitizers.caen_dt5781.worker import CaenDT5781AcquisitionWorker
from flashy.digitizers.caen_dt5781.acquisition import CaenDT5781Acquisition
from flashy.services.analysis_worker import AnalysisWorker
from flashy.models.analysis.result import AnalysisResult
from flashy.models.batch_pulses import BatchPulses
from flashy.services.normalizer import Normalizer

from flashy.services.logger.logger_service import get_logger
from flashy.debug import thread_name

class AcquisitionService(qtc.QObject):
    """
    Central service responsible for managing acquisition and analysis pipelines.
    
    This class orchestrates:
    - Acquisition worker threads (digitizer-specific)
    - Analysis worker threads (parallel processing)
    - Queue-based communication between acquisition and analysis stages
    
    Each instance spawns multiple :py:class:`AnalysisWorker` threads that process
    incoming data asynchronously.
    
    The ``begin_acquisition`` method starts a new acquisition session using
    the selected digitizer backend.
    
    :inherits: :py:class:`PySide6.QtCore.QObject`
    
    .. todo::
        - Debugging signals
    """
    results_changed = qtc.Signal(list)
    acquisition_finished = qtc.Signal(list)
    
    # Debug
    _acquisition_started = qtc.Signal()
    _stop_requested = qtc.Signal()
    
    def __init__(
        self, 
        processing_config: "ProcessingConfig"
    )-> None:
        """
        Initialize the acquisition service.
        
        :param processing_config: Global processing configuration used for
            acquisition, analysis, and detector setup.
        :type processing_config: ProcessingConfig
        """
        super().__init__()
        self.normalizer = Normalizer()
        self._logger = get_logger()
        
        # Setup internal variables
        self.processing_config: "ProcessingConfig" = processing_config
        
        nbr_of_channels = len(self.processing_config.acquisition.digitizer.channels)
        acquisition_results = []
        for i in range(nbr_of_channels):
            ch_batch = self.normalizer.create_acquisition_result_batch(
                processing_config=self.processing_config,
                channel_id=i
            )
            acquisition_results.append(ch_batch)
        self.acquisition_results: List[BatchPulses] = acquisition_results
        """Accumulated analysis results per channel."""
        
        # Acquisition setup
        self._current_worker = None
        """Active acquisition worker thread."""
        self._current_acquisition = None
        """Active acquisition backend instance."""
        
        # Analysis setup
        self.analysis_todo_queue = queue.Queue(maxsize=50)
        """Queue of raw acquisition batches waiting for analysis."""
        self._analysis_workers: List[AnalysisWorker] = []
        """Pool of analysis worker threads."""
        for _ in range(3):
            worker = AnalysisWorker(
                analysis_queue=self.analysis_todo_queue,
                config=self.processing_config
            )
            worker.analysis_complete.connect(self.analysis_complete)
            self._analysis_workers.append(worker)
            worker.start()
            self._logger.debug(f"Started {worker} (Thread={thread_name()}) (isRunning={worker.isRunning()})")
        
        self._pending_batches = 0
        self._acquisition_finished = False
        
        # Debugging counters
        self.discard_todo = 0
        """Number of discarded batches due to full analysis queue."""
        self.printed_todo_queue = False
        """Flag preventing repeated queue-full warnings."""
        self.discard_comp = 0
        """Number of discarded completed analysis results."""
        self.printed_comp_queue = False
        """Flag preventing repeated completion warnings."""
    
    def get_basic_dig_info(
        self, 
        digitizer: Literal['caen_dt5781']
    ) -> dict[str, Any]:
        """
        Retrieve basic information from the selected digitizer.
        
        This method stops any currently running acquisition worker before
        querying the hardware.
        
        :param digitizer: Digitizer backend identifier.
        :type digitizer: Literal["caen_dt5781"]
        
        :returns: Dictionary containing digitizer metadata.
        :rtype: dict[str, Any]
        
        :raises ValueError: If the digitizer information cannot be retrieved.
        """
        self._stop_current_worker()
        
        match digitizer:
            case 'caen_dt5781':
                dig = CaenDT5781Acquisition()
                basic_info = dig.get_basic_info()
            case _:
                dig = CaenDT5781Acquisition()
                basic_info = dig.get_basic_info()
        if basic_info: return basic_info
        else: raise ValueError("Couldn't retrieve basic info")
    
    def begin_acquisition(
        self, 
        signal_state_changed, 
        digitizer: Literal['caen_dt5781']
    ) -> None:
        """
        Start a new acquisition session in a background worker thread.
        
        Any currently running acquisition is stopped before starting a new one.
        
        :param digitizer: Digitizer backend to use.
        :type digitizer: Literal["caen_dt5781"]
        """
        self._stop_current_worker()
        
        match digitizer:
            case 'caen_dt5781':
                self._current_acquisition = CaenDT5781Acquisition()
                self._current_worker = CaenDT5781AcquisitionWorker(
                    acquisition=self._current_acquisition,
                    config=self.processing_config.acquisition
                )
            case _:
                self._current_acquisition = CaenDT5781Acquisition()
                self._current_worker = CaenDT5781AcquisitionWorker(
                    acquisition=self._current_acquisition,
                    config=acquisition_config
                )
        self._set_state_callback(signal_state_changed)
        
        # Signals
        self._current_worker.event_dump.connect(self.acquisition_event_dump)
        self._current_worker.finished.connect(self._on_worker_finished)
        
        # Start
        self._current_worker.start()
        
        # Debug
        self._acquisition_started.emit()
    
    # =======================================================================
    # Qt Slots
    # =======================================================================
    
    @qtc.Slot(list)
    def acquisition_event_dump(
        self, 
        batch: list
    ) -> None:
        """
        Receive raw acquisition batches and enqueue them for analysis.
        
        :param batch: List of raw pulses.
        :type batch: list
        """
        try:
            self.analysis_todo_queue.put_nowait(batch)
            self._pending_batches += 1
        except queue.Full:
            self._logger.debug("QUEUE FULL")
    
    @qtc.Slot(AnalysisResult)
    def analysis_complete(
        self, 
        analysis_result: "AnalysisResult"
    ) -> None:
        """
        Handle completed analysis results and store them in memory.
        
        :param analysis_result: Processed analysis output.
        :type analysis_result: AnalysisResult
        """
        #self._logger.debug("ANALYSIS COMPLETE")
        change = False
        print(f"Before={self.acquisition_results}")
        for i, pulse_batch in enumerate(analysis_result.pulse_batches):
            if pulse_batch.has_pulses and not pulse_batch.discard_flag:
                change = True
                result_batch = self.acquisition_results[i]
                result_batch.add_pulses(
                    pulse_batch.pulses,
                    pulse_batch.raw_valid_pulses,
                    pulse_batch.area_under_curves,
                    pulse_batch.doses,
                )
                self.acquisition_results[i] = result_batch
        if change: self.results_changed.emit(copy.deepcopy(self.acquisition_results))
        print(f"After={self.acquisition_results}")
        print("----------------------------------")
        self._pending_batches -= 1
        
        if self._acquisition_finished and self._pending_batches == 0:
            self._finalize_shutdown()
    
    @qtc.Slot()
    def stop_acquisition(self) -> None:
        """
        Request the current acquisition worker to stop.
        """
        if self._current_worker:
            self._current_worker.stop()
    
    @qtc.Slot()
    def _on_worker_finished(self) -> None:
        """
        Cleanup acquisition worker after completion.
        """
        self._logger.debug("Acquisition worker finished")
        
        worker = self._current_worker
        self._current_worker = None
        self._current_acquisition = None
        
        if worker:
            worker.deleteLater()
        
        self._acquisition_finished = True
        if self._pending_batches == 0:
            self._finalize_shutdown()
    
    # =======================================================================
    # Helper methods 
    # =======================================================================
    
    def _set_state_callback(self, func):
        if self._current_acquisition:
            try:
                self._current_acquisition.set_state_callback(func)
            except Exception:
                self._logger.exception("The state callback couldn't be set.")
        else:
            self._logger.warning("No current acquisition.")
    
    def _stop_current_worker(self) -> None:
        if self._current_worker and self._current_worker.isRunning():
            self._current_worker.stop()
            self._current_worker.wait(1000)
    
    def _finalize_shutdown(self):
        self.shutdown()
    
    def shutdown(self):
        """
        Gracefully shutdown all acquisition and analysis workers.
        
        This should be called when the application exits or acquisition ends.
        """
        self._logger.debug("Waiting for analysis queue to be empty.")
        self.analysis_todo_queue.join()
        self._logger.debug("Shutting down analysis worker threads")
        for i, worker in enumerate(self._analysis_workers):
            worker.stop()
        for worker in self._analysis_workers:
            worker.wait()
        
        print(f"At shutdown={self.acquisition_results}")
        self.results_changed.emit(copy.deepcopy(self.acquisition_results))
        self.acquisition_finished.emit(copy.deepcopy(self.acquisition_results))
        
        # Debug prints
        #print(f"Discarded to analyse: {self.discard_todo}")
        #print(f"Discarded compleded analysis: {self.discard_comp}")


def main():
    """:meta private:"""
    from flashy.models.processing_config import AcquisitionConfig, ProcessingConfig
    from flashy.models.analysis.config import AnalysisConfig
    from flashy.digitizers.caen_dt5781.channel import CaenDT5781Channel
    from flashy.digitizers.caen_dt5781.config import CaenDT5781Config
    from flashy.detectors.detector import DetectorAssignment
    from flashy.detectors.bergoz_bct.bergoz_bct import BergozBCT
    
    from PySide6.QtWidgets import QApplication
    import keyboard
    
    #####################################################################
    path = 'write_test.tdms'
    #####################################################################
    
    t_bergoz = BergozBCT.create_default()
    t_caen_ch0 = CaenDT5781Channel.create_default(channel_id=0)
    t_caen_ch1 = CaenDT5781Channel.create_default(channel_id=1)
    t_analysis = AnalysisConfig.create_default()
    processing_config = ProcessingConfig(
        acquisition=AcquisitionConfig(
            digitizer=CaenDT5781Config(
                [t_caen_ch0, t_caen_ch1],
            ),
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
    
    app = QApplication()
    acq = AcquisitionService(processing_config)
    keyboard.on_press_key("q", lambda event: acq._stop_requested.emit())
    
    acq.acquisition_finished.connect(app.quit)
    acq._acquisition_started.connect(lambda: print("Acquisition started"))
    acq.acquisition_finished.connect(lambda: print("Acquisition finished"))
    acq._stop_requested.connect(acq.stop_acquisition)
    
    
    acq.begin_acquisition(
        digitizer='caen_dt5781', 
        signal_state_changed=None
    )
    app.exec()
    
    #print("Qt event loop exited")
    keyboard.unhook_all()
    acq.shutdown()
    
    save_results(acq.acquisition_results, path, processing_config)
    show_results(acq.acquisition_results)

def save_results(results: List[BatchPulses], path: str, processing_config):
    """:meta private:"""
    from flashy.services.export_service import DataExporter
    
    exporter = DataExporter()
    exporter.write_post_acquisition_to_tdms(results, path, processing_config, acquisition_type='mock')

def show_results(results: List[BatchPulses]):
    """:meta private:"""
    import numpy as np
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(1,2, figsize=(8, 6))
    tab_size = 80
    tab_col_size = 20
    tab_nbr_decimals = 6
    for j, batch in enumerate(results):
        ax = axes[j]
        ax.set_title(f'CH{j}')
        ax.set_xlabel('Temps (ns)')
        ax.set_ylabel('Voltage (V)')
        ax.grid(True, 'both')
        try:
            temps = np.linspace(0, len(batch.pulses[0]), len(batch.pulses[0]))
        except:
            continue
        print("="*tab_size)
        print(f"Tableau des résultats - CH{j}")
        print("="*tab_size)
        print(f"{'Pulse':<{tab_col_size}} {'Charge (nC)':<{tab_col_size}} {'Dose (cGy)':<{tab_col_size}}")
        print("-"*tab_size)
        for i, p in enumerate(batch.pulses):
            print(
                f"{f'Pulse {i}':<{tab_col_size}} "
                f"{batch.area_under_curves[i]:<{tab_col_size}.{tab_nbr_decimals}f} "
                f"{batch.doses[i]:<{tab_col_size}.{tab_nbr_decimals}f}"
            )
            ax.plot(temps, p)
        
        ax.set_xlim(0, len(batch.pulses[0]))
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
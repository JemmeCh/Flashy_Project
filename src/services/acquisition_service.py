from PySide6.QtCore import QObject, Signal, Slot
import numpy as np
import queue
import copy
from typing import TYPE_CHECKING, Any, Literal, List
if TYPE_CHECKING:
    from src.models.data_config import ProcessingConfig

from src.digitizers.caen_dt5781.worker import CaenCT5781AcquisitionWorker
from src.digitizers.caen_dt5781.acquisition import CaenDT5781Acquisition
from src.services.analysis_worker import AnalysisWorker
from src.models.analysis_result import AnalysisResult
from src.models.batch_pulses import BatchPulses


class AcquisitionService(QObject):
    acquisition_started = Signal()
    acquisition_finished = Signal()
    acquisition_error = Signal(str)
    stop_requested = Signal()
    
    def __init__(self, processing_config: "ProcessingConfig") -> None:
        super().__init__()
        # Setup internal variables
        self.processing_config: "ProcessingConfig" = copy.deepcopy(processing_config)
        
        nbr_of_channels = len(self.processing_config.acquisition.digitizer.channels)
        acquisition_results = []
        for i in range(nbr_of_channels):
            ch_batch = self._create_result_batch(i)
            acquisition_results.append(ch_batch)
        self.acquisition_results: List[BatchPulses] = acquisition_results
        
        # Acquisition setup
        self._current_worker = None
        self._current_acquisition = None
        
        # Analysis setup
        self.analysis_todo_queue = queue.Queue(maxsize=50)
        self.analysis_workers: List[AnalysisWorker] = []
        for _ in range(3):
            worker = AnalysisWorker(
                analysis_queue=self.analysis_todo_queue,
                config=self.processing_config
            )
            worker.analysis_complete.connect(self.analysis_complete)
            self.analysis_workers.append(worker)
            worker.start()
        
        # Debugging stuff
        self.discard_todo = 0
        self.printed_todo_queue = False
        self.discard_comp = 0
        self.printed_comp_queue = False
    
    def get_basic_dig_info(self, digitizer: Literal['caen_dt5781']) -> dict[str, Any]:
        """Get basic info of the digitizer. Will stop current worker"""
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
    
    def begin_acquisition(self, digitizer: Literal['caen_dt5781']) -> None:
        """Starts acquisition in the background with worker. Will stop current worker"""
        self._stop_current_worker()
        
        match digitizer:
            case 'caen_dt5781':
                self._current_acquisition = CaenDT5781Acquisition()
                self._current_worker = CaenCT5781AcquisitionWorker(
                    acquisition=self._current_acquisition,
                    config=self.processing_config.acquisition
                )
            case _:
                self._current_acquisition = CaenDT5781Acquisition()
                self._current_worker = CaenCT5781AcquisitionWorker(
                    acquisition=self._current_acquisition,
                    config=acquisition_config
                )
        
        # Signals
        self._current_worker.event_dump.connect(self.acquisition_event_dump)
        self._current_worker.error.connect(self.acquisition_error)
        self._current_worker.finished.connect(self._on_worker_finished)
        
        # Start
        self._current_worker.start()
        self.acquisition_started.emit()
    
    # =======================================================================
    # Slots
    # =======================================================================
    
    @Slot(list)
    def acquisition_event_dump(self, batch: list):
        try:
            self.analysis_todo_queue.put_nowait(batch)
        except queue.Full:
            if not self.printed_todo_queue:
                #print("Analysis queue is full!!! DISCARDING")
                self.printed_todo_queue = True
            self.discard_todo += 1
            pass
    
    @Slot(AnalysisResult)
    def analysis_complete(self, analysis_result: "AnalysisResult"):
        for i, pulse_batch in enumerate(analysis_result.pulse_batches):
            if pulse_batch.has_pulses and not pulse_batch.discard_flag:
                result_batch = self.acquisition_results[i]
                result_batch.add_pulses(
                    pulse_batch.pulses,
                    pulse_batch.raw_valid_pulses,
                    pulse_batch.area_under_curves,
                    pulse_batch.doses,
                )
                self.acquisition_results[i] = result_batch
    
    @Slot()
    def stop_acquisition(self):
        if self._current_worker:
            self._current_worker.stop()
    
    @Slot()
    def _on_worker_finished(self) -> None:
        #print('deleting worker')
        if self._current_worker:
            self._current_worker.deleteLater()
            self._current_worker = None
            self._current_acquisition = None
        self.acquisition_finished.emit()
    
    # =======================================================================
    # Helper methods 
    # =======================================================================
    
    def _create_result_batch(self, channel_id: int):
        reclen_ns = self.processing_config.acquisition.digitizer.channels[0].rdc_len
        sampling_period_ns = self.processing_config.acquisition.digitizer.sampling_period_ns
        shape = (0, int(reclen_ns / sampling_period_ns))
        pulses = np.zeros(shape=shape)
        batch_pulses = BatchPulses(
            pulses=pulses,
            raw_valid_pulses=pulses,
            analysis_level_method=self.processing_config.analysis.level_method,
            analysis_area_calc_method=self.processing_config.analysis.area_calc_method,
            analysis_nC2cGy_factor=self.processing_config.analysis.nC2cGy_factor,
            digitizer_sampeling_period_ns=self.processing_config.acquisition.digitizer.sampling_period_ns,
            digitizer_ADC2V_factor=self.processing_config.acquisition.digitizer.get_adc_to_volts_factor(channel_id),
            detector_Vns2nC_factor=self.processing_config.acquisition.detector_assignments[channel_id].detector.get_vns_to_nc_factor()
        )
        return batch_pulses
    
    def _stop_current_worker(self) -> None:
        if self._current_worker and self._current_worker.isRunning():
            self._current_worker.stop()
            self._current_worker.wait(1000)
    
    def shutdown(self):
        self._stop_current_worker()
        for worker in self.analysis_workers:
            worker.stop()        
        for worker in self.analysis_workers:
            worker.wait()
        self.analysis_workers.clear()
        
        # Debug prints
        #print(f"Discarded to analyse: {self.discard_todo}")
        #print(f"Discarded compleded analysis: {self.discard_comp}")


def main():
    from src.models.data_config import AcquisitionConfig, AnalysisConfig, ProcessingConfig
    from src.digitizers.caen_dt5781.channel import CaenDT5781Channel
    from src.digitizers.caen_dt5781.config import CaenDT5781Config
    from src.detectors.detector import DetectorAssignment
    from src.detectors.bergoz_bct import BergozBCT
    
    from PySide6.QtWidgets import QApplication
    import keyboard
    
    #####################################################################
    path = 'write_test.tdms'
    #####################################################################
    
    acquisition_config = AcquisitionConfig(
            digitizer=CaenDT5781Config(
                [CaenDT5781Channel(0), CaenDT5781Channel(1)],
            ),
            detector_assignments=[
                DetectorAssignment(
                    detector=BergozBCT(),
                    digitizer_channel=0
                    ),
                DetectorAssignment(
                    detector=BergozBCT(),
                    digitizer_channel=1
                    ),
            ]
        )
    processing_config = ProcessingConfig(
        acquisition=acquisition_config,
        analysis=AnalysisConfig()
    )
    
    app = QApplication()
    acq = AcquisitionService(processing_config)
    keyboard.on_press_key("q", lambda event: acq.stop_requested.emit())
    
    acq.acquisition_finished.connect(app.quit)
    acq.acquisition_started.connect(lambda: print("Acquisition started"))
    acq.acquisition_error.connect(lambda err: print(f"ERROR: {err}"))
    acq.acquisition_finished.connect(lambda: print("Acquisition finished"))
    acq.stop_requested.connect(acq.stop_acquisition)
    
    
    acq.begin_acquisition('caen_dt5781')
    app.exec()
    
    #print("Qt event loop exited")
    keyboard.unhook_all()
    acq.shutdown()
    
    save_results(acq.acquisition_results, path, processing_config)
    show_results(acq.acquisition_results)

def save_results(results: List[BatchPulses], path: str, processing_config):
    from src.services.export_service import DataExporter
    
    exporter = DataExporter()
    exporter.write_post_acquisition_to_tdms(results, path, processing_config, acquisition_type='mock')

def show_results(results: List[BatchPulses]):
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
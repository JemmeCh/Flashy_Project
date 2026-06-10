@echo off
echo Generating ui_*.py files

pyside6-uic feedback_widget.ui -o ui_feedback_widget.py
pyside6-uic result_table.ui -o ui_result_table.py

pyside6-uic analyser_tab.ui -o ui_analyser_tab.py
pyside6-uic dt5781_tab.ui -o ui_dt5781_tab.py
pyside6-uic result_panel_widget.ui -o ui_result_panel_widget.py

pyside6-uic analyser_controls.ui -o ui_analyser_controls.py
pyside6-uic dt5781_controls.ui -o ui_dt5781_controls.py

pyside6-uic flashy_window.ui -o ui_flashy_window.py

echo Finished!
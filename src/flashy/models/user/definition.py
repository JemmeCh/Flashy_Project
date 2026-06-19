from flashy.models.parameters.definition import ParameterDefinition


USER_DEFINITIONS = {
    "project_path": ParameterDefinition(
        key="project_path",
        name="Project's Path",
        description="Root project path where acquisition data will be saved.",
        path="Project",
        value_type=str,
        default='DAQ',
        widget_type='entry'
    ),
    "name_of_shoot": ParameterDefinition(
        key="name_of_shoot",
        name="Acquisition's name",
        description="Name of the acquisition session or 'shoot'.",
        path="Project",
        value_type=str,
        default='default',
        widget_type='entry'
    ),
    "increment": ParameterDefinition(
        key="increment",
        name="Increment",
        description="Number of increments done.",
        path="Project",
        value_type=int,
        default=1,
        widget_type='readonly'
    ),
    "increment_name": ParameterDefinition(
        key="increment_name",
        name="Increment Name",
        description="Acquisition's name followed by the increment.",
        path="Project",
        value_type=str,
        default="default_1",
        widget_type='readonly'
    ),
    "path_of_shoot": ParameterDefinition(
        key="path_of_shoot",
        name="Acquisition's Path",
        description="Full path where the current acquisition data is stored.",
        path="Project",
        value_type=str,
        default="default_1",
        widget_type='readonly'
    ),
    "analyser_root": ParameterDefinition(
        key="analyser_root",
        name="Root Path",
        description="Full path for the analyser's tree view's root.",
        path="Analyser",
        value_type=str,
        default="Please choose a root path",
        widget_type='entry'
    ),
    "path_to_logs": ParameterDefinition(
        key="path_to_logs",
        name="Path to Logs",
        description="Fixed path where logs are stored.",
        path="Application",
        value_type=str,
        default='logs',
        widget_type='entry'
    )
}
"""
Parameter definitions for user.

:meta hide-value:
"""
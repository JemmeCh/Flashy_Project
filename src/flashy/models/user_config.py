import os
import msgspec
from typing import Literal


class UserConfig(msgspec.Struct):
    """
    User configuration container.
    
    :inherits: msgspec.Struct
    
    .. todo::
        - Maybe revamp this when implementing the GUI since the method's names are weird/old/outdated.
    """
    project_path: str = ''
    """Root project path used for loading/saving data."""
    name_of_shoot: str = ''
    """Name of the acquisition session or "shoot"."""
    increment_name: str = ""
    """Suffix used when generating incremented file or run names."""
    path_of_shoot: str = ""
    """Full path where the current shoot data is stored."""
    
    increment: int = 1
    """Increment index used for run/versioning."""
    path_to_logs: Literal['logs'] = "logs"
    """Relative or fixed path where logs are stored."""
    
    def __post_init__(self):
        """
        Ensure all configuration values are initialized with defaults when missing.
        """
        if not self.project_path:
            self.project_path = 'DAQ'
        if not self.name_of_shoot:
            self.name_of_shoot = 'default'
        if not self.increment_name:
            self.increment_name = f"{self.name_of_shoot}_{self.increment}"
        if not self.path_of_shoot:
            self.path_of_shoot = os.path.join(self.project_path, self.increment_name)
    
    def increment_name_of_shoot(self):
        """
        Increment the shoot name and create the corresponding directory.
        
        :raises FileExistsError: If the target directory already exists.
        """
        self.increment += 1
        self.incremented_name = f'{self.name_of_shoot}_{str(self.increment)}'
        self.path_of_shoot = os.path.join(self.project_path, self.incremented_name)
        try:
            os.mkdir(self.path_of_shoot)
        except FileExistsError:
            # TODO: SIGNAL
            print(f"'{self.path_of_shoot}' already exists! You should change the name of the shoot to not override old data")
    
    def set_name_of_shoot(self, name: str):
        """
        Set a new shoot name and initialize its directory.
        
        :param name: New shoot name.
        :type name: str
        :raises FileExistsError: If a directory for this shoot already exists.
        """
        potential_name = f'{name}_{str(1)}'
        try:
            path_of_shoot = os.path.join(self.project_path, potential_name)
            os.mkdir(path_of_shoot) # Check if we can create a directory with the name
            self.path_of_shoot = path_of_shoot
            self.increment = 1
            self.name_of_shoot = f'{name}'.replace(' ', '')
            self.incremented_name = f"{name.replace(' ', '')}_{self.increment}"
        except FileExistsError as e:
            # Failed to create it
            # TODO: SIGNAL
            print(f'The directory {name} already exists')
            raise e
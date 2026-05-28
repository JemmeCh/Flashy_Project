import os
import msgspec
from typing import Literal

# =======================================================================
# User configuration
# =======================================================================

class UserConfig(msgspec.Struct):
    project_path: str = ''
    name_of_shoot: str = ''
    increment_name: str = ""
    path_of_shoot: str = ""
    
    increment: int = 1
    path_to_logs: Literal['logs'] = "logs"
    
    def __post_init__(self):
        if not self.project_path:
            self.project_path = 'DAQ'
        if not self.name_of_shoot:
            self.name_of_shoot = 'default'
        if not self.increment_name:
            self.increment_name = f"{self.name_of_shoot}_{self.increment}"
        if not self.path_of_shoot:
            self.path_of_shoot = os.path.join(self.project_path, self.increment_name)
    
    def increment_name_of_shoot(self):
        self.increment += 1
        self.incremented_name = f'{self.name_of_shoot}_{str(self.increment)}'
        self.path_of_shoot = os.path.join(self.project_path, self.incremented_name)
        try:
            os.mkdir(self.path_of_shoot)
        except FileExistsError:
            # TODO: SIGNAL
            print(f"'{self.path_of_shoot}' already exists! You should change the name of the shoot to not override old data")
    
    def set_name_of_shoot(self, name: str):
        potential_name = f'{name}_{str(1)}'
        try:
            path_of_shoot = os.path.join(self.project_path, potential_name)
            os.mkdir(path_of_shoot) # Check if we can create a directory with the name
            self.path_of_shoot = path_of_shoot
            self.increment = 1
            self.name_of_shoot = f'{name}'.replace(' ', '')
            self.incremented_name = f"{name.replace(' ', '')}_{self.increment}"
        except FileExistsError:
            # Failed to create it
            # TODO: SIGNAL
            print(f'The directory {name} already exists')
            return
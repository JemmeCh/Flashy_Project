import numpy as np

# To install the module: pip install caen-felib
import caen_felib as caen

# Set acces
lib = caen.lib

# Get CAEN FELib path
print(f'CAEN FELib found at: {lib.path} (version={lib.version})')
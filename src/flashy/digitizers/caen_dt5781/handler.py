from functools import wraps
from caen_felib import error

def handle_CAEN_exceptions(func):
    """:meta private:"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except error.Error as ex:
            if ex.code.value == error.ErrorCode.COMMAND_ERROR:
                self._logger.warning(f"Error code {ex.code.value} (COMMAND_ERROR): Couldn't find a digitizer to connect to!")
            else:
                self._logger.exception(f"Error code {ex.code.value}: Unexpected! Raising error (see terminal)")
    return wrapper
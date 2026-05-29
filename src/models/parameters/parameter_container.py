from typing import Any, ClassVar, Mapping
import msgspec

from src.models.parameters.parameter_definition import ParameterDefinition


class ParameterContainer(msgspec.Struct):
    """
    Generic base for any configuration-like object backed by a ParameterDefinition registry.
    """
    # Each subclass must override this
    DEFINITIONS: ClassVar[Mapping[str, ParameterDefinition]]
    values: dict[str, Any] = msgspec.field(default_factory=dict)
    
    @classmethod
    def create_default(cls, **kwargs):
        values = {
            key: definition.default
            for key, definition in cls.DEFINITIONS.items()
        }
        return cls(values=values, **kwargs)
    
    def get_value(self, key: str):
        return self.values[key]
    
    def get_definition(self, key: str) -> ParameterDefinition:
        return self.DEFINITIONS[key]
    
    def set_value(self, key: str, raw_value: Any):
        definition = self.get_definition(key)
        self.values[key] = definition.transform(raw_value)
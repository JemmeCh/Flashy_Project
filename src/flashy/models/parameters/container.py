from typing import Any, ClassVar, Mapping
import msgspec

from flashy.models.parameters.definition import ParameterDefinition


class ParameterContainer(msgspec.Struct):
    """
    Generic base class for configuration-like objects backed by a
    :py:class:`~flashy.models.parameters.definition.ParameterDefinition` registry.
    
    Each subclass must override ``DEFINITIONS`` to describe the available
    parameters, their defaults, validation rules, and optional conversion
    logic.
    
    This class provides a unified dictionary-based storage for parameter
    values, initialized from the registry.
    
    :inherits: :py:class:`msgspec.Struct`
    """
    DEFINITIONS: ClassVar[Mapping[str, ParameterDefinition]]
    """Mapping of parameter keys to their definitions. Must be overridden."""
    values: dict[str, Any] = msgspec.field(default_factory=dict)
    """Runtime storage of parameter values."""
    
    @classmethod
    def create_default(cls, **kwargs):
        """
        Create a new instance using default values defined in ``DEFINITIONS``.
        
        Each parameter is initialized using the ``default`` field of its
        corresponding :py:class:`~flashy.models.parameters.definition.ParameterDefinition`.
        
        Optional keyword arguments can override default values or provide
        additional initialization parameters accepted by the class.
        
        :param kwargs: Optional overrides for default parameter values or
            constructor arguments.
        :type kwargs: Any
        
        :returns: A new instance of the class initialized with default values.
        :rtype: ParameterContainer
        """
        values = {
            key: definition.default
            for key, definition in cls.DEFINITIONS.items()
        }
        return cls(values=values, **kwargs)
    
    def get_value(self, key: str):
        """
        Retrieve the current value of a parameter.
        
        :param key: Name of the parameter to retrieve.
        :type key: str
        
        :returns: The stored value associated with the given key.
        :rtype: Any
        
        :raises KeyError: If the key does not exist in ``values``.
        """
        return self.values[key]
    
    def get_definition(self, key: str) -> ParameterDefinition:
        """
        Retrieve the :py:class:`~flashy.models.parameters.definition.ParameterDefinition` associated with a key.
        
        This gives access to metadata such as default value, validation rules,
        widget type, and transformation logic.
        
        :param key: Name of the parameter.
        :type key: str
        
        :returns: The parameter definition object.
        :rtype: :py:class:`~flashy.models.parameters.definition.ParameterDefinition`
        
        :raises KeyError: If the key is not defined in ``DEFINITIONS``.
        """
        return self.DEFINITIONS[key]

    def set_value(self, key: str, raw_value: Any):
        """
        Set a parameter value using its associated transformation logic.
        
        The raw input value is passed through the parameter's
        ``transform`` method (if defined) before being stored.
        
        :param key: Name of the parameter to set.
        :type key: str
        
        :param raw_value: Input value to be transformed and stored.
        :type raw_value: Any
        
        :returns: None
        :rtype: None
        
        :raises KeyError: If the key is not defined in ``DEFINITIONS``.
        """
        definition = self.get_definition(key)
        self.values[key] = definition.transform(raw_value)
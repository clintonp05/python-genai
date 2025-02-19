from typing import Dict, Type, Any

class DIContainer:
    _dependencies: Dict[Type, Any] = {}

    @classmethod
    def register(cls, interface: Type, implementation: Any):
        cls._dependencies[interface] = implementation

    @classmethod
    def resolve(cls, interface: Type) -> Any:
        return cls._dependencies.get(interface)
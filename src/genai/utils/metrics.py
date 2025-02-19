from abc import ABC, abstractmethod

class MetricsProvider(ABC):
    @abstractmethod
    def log_metric(self, name: str, value: float):
        pass

class GrafanaProvider(MetricsProvider):
    def log_metric(self, name: str, value: float):
        # Integration with Grafana HTTP API
        pass

class AppDynamicsProvider(MetricsProvider):
    def log_metric(self, name: str, value: float):
        # Integration with AppDynamics SDK
        pass
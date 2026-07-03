from typing import Protocol, Dict, Any, TypeVar, Callable

T = TypeVar("T")

class ServiceRegistryProtocol(Protocol):
    """Protocol for interacting with the Discovery server"""

    def register(self, registration_data: Dict[str, Any]) -> bool:
        """Register an instance in the system"""
        ...

    def send_heartbeat(self, heartbeat_data: Dict[str, Any]) -> bool:
        """Send resource metrics and heartbeat signal"""
        ...

    def get_services(self) -> Dict[str, Any]:
        """Get the current map of the microservices network"""
        ...


class ResourceBalancerProtocol(Protocol):
    """Protocol for managing dynamic thread pools"""

    def configure_pool(self, api_name: str, max_workers: int) -> None:
        """Allocate a specific number of threads for a Web-API"""
        ...

    def execute(self, api_name: str, func: Callable[..., T], *args: Any, **kwargs: Any) -> Any:
        """Execute a task in an isolated pool"""
        ...

    def get_allocations(self) -> Dict[str, int]:
        """Get the current allocation of resources for monitoring"""
        ...
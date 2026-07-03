from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime

class ResourceMetricsDTO(BaseModel):
    """Resource metrics for a specific Django instance"""
    cpu_count: int = Field(..., description="Number of logical CPU cores")
    cpu_usage_percent: float = Field(..., description="Current CPU usage in %")
    ram_total_mb: int = Field(..., description="Total RAM on the host in MB")
    ram_used_mb: int = Field(..., description="RAM used by the current process in MB")
    active_threads: int = Field(..., description="Number of active threads")
    pool_allocations: Dict[str, int] = Field(
        default_factory=dict, 
        description="Sizes of dynamic thread pools for specific Web-APIs"
    )

class ServiceRegistrationDTO(BaseModel):
    """Model for initial registration of a microservice in Hecate Discovery"""
    app_name: str = Field(..., description="Name of the Django application (e.g., billing-api)")
    instance_id: str = Field(..., description="Unique ID of the instance (UUID or hostname)")
    host: str = Field(..., description="IP address or hostname of the instance")
    port: int = Field(..., description="Port on which the Django application is listening")
    status: str = Field(default="STARTING", description="Current status of the instance (UP, STARTING, DOWN)")
    metrics: ResourceMetricsDTO = Field(..., description="Initial resource metrics")

class HeartbeatDTO(BaseModel):
    """Model for sending periodic heartbeat updates to the discovery server"""
    instance_id: str
    app_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metrics: ResourceMetricsDTO  # Each heartbeat update refreshes the RAM/CPU/Thread data on the server
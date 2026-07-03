from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, Any
from hecate_discovery.storage import storage

app = FastAPI(
    title="Hecate Discovery Server",
    description="Central registry of microservices and resource orchestrator for hosting",
    version="0.1.0"
)

# Schemas for request validation (simplified versions of our DTOs)
class MetricsSchema(BaseModel):
    cpu_count: int
    cpu_usage_percent: float
    ram_total_mb: int
    ram_used_mb: int
    active_threads: int
    pool_allocations: Dict[str, int] = {}

class RegisterServiceSchema(BaseModel):
    app_name: str
    instance_id: str
    host: str
    port: int
    status: str
    metrics: MetricsSchema

class HeartbeatSchema(BaseModel):
    instance_id: str
    app_name: str
    metrics: MetricsSchema


@app.post("/api/v1/register", status_code=201)
async def register_service(payload: RegisterServiceSchema):
    """Accepts a request for initial registration of a Django service"""
    storage.register_or_update(payload.app_name, payload.instance_id, payload.model_dump())
    print(f"[Hecate Discovery] Registered service: {payload.app_name} [{payload.instance_id}] at {payload.host}:{payload.port}")
    return {"status": "registered", "instance_id": payload.instance_id}


@app.post("/api/v1/heartbeat")
async def process_heartbeat(payload: HeartbeatSchema, background_tasks: BackgroundTasks):
    """Regular heartbeat. Updates CPU/RAM metrics in real-time"""
    # Run the cleanup task in the background to remove expired services
    background_tasks.add_task(storage.clean_expired_services)
    
    # Extract the existing data to avoid overwriting host/port when updating metrics
    all_services = storage.get_all_services()
    existing_info = all_services.get(payload.app_name, {}).get(payload.instance_id, {}).get("info", {})
    
    # Update the metrics and status, but preserve host/port if they exist
    existing_info["metrics"] = payload.metrics.model_dump()
    existing_info["status"] = "UP"
    
    storage.register_or_update(payload.app_name, payload.instance_id, existing_info)
    
    print(f"[Pulse] {payload.app_name} ({payload.instance_id}) -> CPU: {payload.metrics.cpu_usage_percent}%, RAM: {payload.metrics.ram_used_mb}MB, Threads: {payload.metrics.active_threads}")
    return {"status": "acknowledged"}


@app.get("/api/v1/services")
async def get_registry():
    """Endpoint for the dashboard or API Gateway — returns a map of the entire network"""
    return storage.get_all_services()
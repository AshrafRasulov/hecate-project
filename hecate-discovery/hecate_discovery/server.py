from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, Any
from hecate_discovery.storage import storage

app = FastAPI(
    title="Hecate Discovery Server",
    description="Центральный реестр микросервисов и оркестратор ресурсов хостинга",
    version="0.1.0"
)

# Схемы валидации запросов (упрощенные версии наших DTO)
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
    """Принимает запрос на первичную регистрацию Django-сервиса"""
    storage.register_or_update(payload.app_name, payload.instance_id, payload.model_dump())
    print(f"[Hecate Discovery] Registered service: {payload.app_name} [{payload.instance_id}] at {payload.host}:{payload.port}")
    return {"status": "registered", "instance_id": payload.instance_id}


@app.post("/api/v1/heartbeat")
async def process_heartbeat(payload: HeartbeatSchema, background_tasks: BackgroundTasks):
    """Регулярный пульс. Обновляет метрики CPU/RAM в реальном времени"""
    # Запускаем очистку старых записей в фоне, чтобы не тормозить ответ
    background_tasks.add_task(storage.clean_expired_services)
    
    # Извлекаем текущие данные, чтобы не затереть хост/порт при обновлении метрик
    all_services = storage.get_all_services()
    existing_info = all_services.get(payload.app_name, {}).get(payload.instance_id, {}).get("info", {})
    
    # Обновляем только метрики ресурсов
    existing_info["metrics"] = payload.metrics.model_dump()
    existing_info["status"] = "UP"
    
    storage.register_or_update(payload.app_name, payload.instance_id, existing_info)
    
    print(f"[Pulse] {payload.app_name} ({payload.instance_id}) -> CPU: {payload.metrics.cpu_usage_percent}%, RAM: {payload.metrics.ram_used_mb}MB, Threads: {payload.metrics.active_threads}")
    return {"status": "acknowledged"}


@app.get("/api/v1/services")
async def get_registry():
    """Эндпоинт для дашборда или API Gateway — отдает карту всей сети"""
    return storage.get_all_services()
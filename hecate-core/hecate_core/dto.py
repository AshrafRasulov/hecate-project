from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime

class ResourceMetricsDTO(BaseModel):
    """Метрики использования ресурсов конкретного инстанса Django"""
    cpu_count: int = Field(..., description="Количество логических ядер CPU")
    cpu_usage_percent: float = Field(..., description="Текущая загрузка CPU в %")
    ram_total_mb: int = Field(..., description="Всего RAM на хостинге в Мб")
    ram_used_mb: int = Field(..., description="RAM использовано текущим процессом в Мб")
    active_threads: int = Field(..., description="Количество активных потоков")
    pool_allocations: Dict[str, int] = Field(
        default_factory=dict, 
        description="Размеры динамических пулов потоков для конкретных Web-API"
    )

class ServiceRegistrationDTO(BaseModel):
    """Модель для первоначальной регистрации микросервиса в Hecate Discovery"""
    app_name: str = Field(..., description="Имя Django-приложения (например, billing-api)")
    instance_id: str = Field(..., description="Уникальный ID инстанса (UUID или хостнейм)")
    host: str = Field(..., description="IP-адрес или хост инстанса")
    port: int = Field(..., description="Порт, на котором слушает Django")
    status: str = Field(default="STARTING", description="Текущий статус инстанса (UP, STARTING, DOWN)")
    metrics: ResourceMetricsDTO = Field(..., description="Начальные метрики ресурсов")

class HeartbeatDTO(BaseModel):
    """Модель регулярного 'пульса' для поддержания статуса инстанса в реестре"""
    instance_id: str
    app_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metrics: ResourceMetricsDTO  # Каждый пинг обновляет данные по RAM/CPU/Потокам на сервере
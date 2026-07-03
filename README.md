# 🏛️ Hecate Project

<p align="center">
  <img src="https://img.shields.io/github/license/AshrafRasulov/hecate-project?style=for-the-badge&color=blue" alt="License">
  <img src="https://img.shields.io/github/stars/AshrafRasulov/hecate-project?style=for-the-badge&color=gold" alt="Stars">
  <img src="https://img.shields.io/github/v/release/AshrafRasulov/hecate-project?style=for-the-badge&color=green" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Django-4.0%2B-092E20?style=for-the-badge&logo=django" alt="Django">
</p>

---
## 📋 Обзор системы (Overview)
## 📋 System Overview

**Hecate Project** — это легковесный, отказоустойчивый аналог экосистемы *Spring Boot Eureka / Netflix Service Discovery*, адаптированный для инфраструктуры **Python Django** и **FastAPI**. 
**Hecate Project** — It is a lightweight, fault-tolerant alternative to the Spring Boot Eureka / Netflix Service Discovery ecosystem, adapted for the Python Django framework and FastAPI.

Проект разработан для оркестрации микросервисов, мониторинга ресурсов хостинга (CPU, RAM, активные потоки) и умного динамического распределения лимитов непосредственно во время работы высоконагруженных Web-API.
The project is designed for microservice orchestration, monitoring hosting resources (CPU, RAM, active threads), and intelligent dynamic limit allocation directly during the operation of high-load Web APIs.

---

## 🧬 Архитектура Монорепозитория
## 🧬 Monorepository Architecture

Проект организован в виде чистой моноструктуры, разделенной на три ключевых слоя:
The project is organized as a pure monostructure, divided into three key layers:

* **`hecate-core`** — Общие структуры данных (DTO), Pydantic-схемы валидации и интерфейсы (`protocols.py`) взаимодействия.
* **`hecate-core`** — Generic data structures (DTOs), Pydantic validation schemas, and interaction interfaces (`protocols.py`).

* **`hecate-discovery`** — Высокопроизводительный сервер регистрации на базе **FastAPI**. Хранит карту сети в оперативной памяти (In-Memory), отслеживает Heartbeats и предоставляет дашборд.
* **`hecate-discovery`** — A high-performance registration server based on FastAPI. It stores the network map in-memory, monitors heartbeats, and provides a dashboard.

* **`hecate-micro`** — Клиентский агент для интеграции в Django. Автоматически собирает метрики хостинга через `psutil`, управляет изолированными пулами потоков и осуществляет Client-Side Load Balancing.
* **`hecate-micro`** — A client agent for Django integration. Automatically collects hosting metrics via psutil, manages isolated thread pools, and implements client-side load balancing.
---

## 🛠️ Структура конфигурации (`hecate.ini`)
## 🛠️ Configuration structure (`hecate.ini`)

Библиотека поддерживает гибкое переопределение физических параметров хоста без необходимости править код приложений. Вы можете ограничить ресурсы или жестко зафиксировать маски распределения ядер:



```ini
[HECATE]
app_name = payment-service
discovery_url = [http://127.0.0.1:8771](http://127.0.0.1:8771)
port = 8772

[RESOURCES]
# Ручное переопределение метрик для контейнеров / Docker
# Manually overriding metrics for containers / Docker
cpu_count = 8
ram_total_mb = 1024

# Изоляция ядер по классам: Discovery (1), Gateway (1), Django Services (6)
# Isolation of cores by class: Discovery (1), Gateway (1), Django Services (6)
cpu_assignment = 1:1:6


🚀 Быстрый старт (Quick Start)
1. Запуск Сервера Регистрации (Hecate Discovery)
Сервер автоматически резервирует за собой системный порт 8771.
The server automatically reserves system port 8771.

    cd hecate-discovery
    pip install -e .
    python -m hecate_discovery

2. Подключение агента к любому Django Web-API
Установите клиент локально в виртуальное окружение вашего Django-приложения:
Connecting the agent to any Django Web API
Install the client locally in your Django application's virtual environment:

    pip install -e /path/to/hecate-project/hecate-micro

Добавьте библиотеку в settings.py:
Add the library to settings.py:

    Python
    INSTALLED_APPS = [
        # ...
        'hecate_micro',  # Активирует автоматический фоновый сборщик метрик / Enables automatic background metrics collector
    ]

📈 Конвенция Портов Экосистемы
📈 Ports Ecosystem Convention

Для предсказуемости инфраструктуры в Hecate заложена жесткая дефолтная иерархия портов:
To ensure infrastructure predictability, Hecate has a rigid default port hierarchy:

    8770 — Базовый порт инфраструктуры Hecate / Hecate's core infrastructure port
    
    8771 — Hecate Discovery Сервер (Центральный Реестр) / Hecate Discovery Server (Central Registry)
    
    8772 — Первое подключенное Django Web-API приложение / First connected Django Web-API application
    
    877(N) — Последующие реплики и микросервисы (8773, 8774...) / Subsequent replicas and microservices (8773, 8774...)

🤝 Лицензия (License)
Distributed under the MIT License. See LICENSE for more information.
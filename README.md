# MultifuncionalBot

Bot multifuncional para servidores de Discord, desarrollado como proyecto de finalización del CFGS en Desarrollo de Aplicaciones Multiplataforma (DAM).

## Descripción

El proyecto desarrolla un Bot multifuncional autohospedado (*self-hosted*) para Discord. Su objetivo es proporcionar una solución modular y escalable, superando las limitaciones de los bots comerciales (restricciones de pago, publicidad, falta de control de datos). La arquitectura está diseñada para integrar múltiples categorías de comandos (Información, Moderación, Música, Configuración).

## Características principales

*   **Arquitectura Modular:** Organización de comandos, eventos y tareas según responsabilidades.
*   **Motor de Audio:** Integración con [Lavalink](https://lavalink.dev/) mediante [Wavelink](https://wavelink.dev/) para una reproducción de música eficiente y desacoplada de la lógica del bot.
*   **Persistencia de datos:** Uso de [PostgreSQL](https://www.postgresql.org/) y [SQLAlchemy](https://www.sqlalchemy.org/) para gestionar configuraciones por servidor, datos de usuarios, etc.
*   **Internacionalización (i18n):** Respuestas del bot traducibles.
*   **Contenerización:** Despliegue simplificado mediante `docker-compose`.

## Tecnologías utilizadas

*   **Lenguaje:** Python 3.14+
*   **Discord Framework:** [discord.py](https://github.com/Rapptz/discord.py)
*   **Audio:** Lavalink & Wavelink
*   **Base de Datos:** PostgreSQL & SQLAlchemy (async)
*   **Configuración:** Pydantic & pydantic-settings
*   **Despliegue:** Docker & Docker Compose

## Primeros pasos

### Requisitos previos

*   Docker y Docker Compose instalados.
*   Un token de bot de Discord (obtenido desde el Portal de Desarrolladores de Discord).
*   Un servidor Lavalink (o puedes usar el contenedor incluido).

### Instalación y ejecución

1.  Clona el repositorio:
    ```bash
    git clone https://github.com/KevinUrreta/multifuncionalbot.git
    cd MultifuncionalBot
    ```

2.  Crea un archivo `.env` en la raíz del proyecto basándote en un ejemplo (debes definir las variables necesarias para Discord, PostgreSQL y Lavalink).

3.  Inicia el bot y los servicios necesarios:
    ```bash
    docker-compose up -d
    ```

## Estructura del proyecto

```text
.
├── docker/             # Configuración de Docker
├── src/
│   ├── app/            # Lógica del bot (comandos, eventos, tareas)
│   ├── core/           # Configuración, loader y núcleo
│   ├── helpers/        # Utilidades
│   ├── i18n/           # Internacionalización
│   └── infrastructure/ # BD y Lavalink
├── tests/              # Pruebas unitarias e integración
└── main.py             # Punto de entrada
```

## Licencia

Este proyecto se ha desarrollado con fines educativos como parte del CFGS en DAM.

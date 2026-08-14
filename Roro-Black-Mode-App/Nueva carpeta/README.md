# Roro Black Mode — Browser Agent Starter

Este proyecto es una base local para Roro Black Mode.

Incluye:
- interfaz negra futurista;
- control de permisos;
- navegador Chromium controlado por Playwright;
- capturas locales sin límite artificial;
- historial de capturas;
- voz del navegador cuando está disponible;
- acciones básicas: abrir URL, capturar pantalla y cerrar navegador.

## Instalación en Windows

1. Instala Python 3.11+.
2. Abre CMD en esta carpeta.
3. Ejecuta:

    pip install -r requirements.txt
    playwright install chromium
    python app.py

4. Abre http://127.0.0.1:8000

Las capturas se guardan en `captures/`. El programa no establece un límite de cantidad; el límite real es el espacio disponible en el disco.

## Importante
Este starter NO guarda contraseñas ni intenta saltarse autenticaciones. Para sitios con cuenta, el usuario debe iniciar sesión de forma normal y las acciones sensibles deben pasar por confirmación.

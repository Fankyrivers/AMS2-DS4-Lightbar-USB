# AMS2 DS4 Multicolor Shift‑Light (USB Edition)

🎮 **Convierte tu DualShock 4 en un shift‑light realista para Automobilista 2**  
Este script lee la telemetría en tiempo real y enciende la barra de luz del DS4 con los mismos colores y patrones que el tablero del coche.  
Incluye configuraciones listas para todos los GT3 y es totalmente personalizable desde un archivo `coches.json`.

---

## ⚠️ Advertencia importante
- **No modifiques el script `autoluces.py`** a menos que:
  - Tengas conocimientos suficientes de Python y del funcionamiento del HID del DS4.
  - Sea para optimizar o adaptar el código a cambios futuros del juego.
- Toda la personalización de colores, RPM y parpadeos se hace **únicamente** en `coches.json`.
- Si modificas el script sin saber exactamente qué haces, podrías romper la compatibilidad.

---

## ✨ Características
- Soporte para todos los GT3 y fácil de ampliar a otros coches.
- Colores y umbrales de RPM configurables por coche.
- Parpadeo en corte con velocidad ajustable (`parpadeo_ms`).
- Reconexión automática si el mando se desconecta por cable.
- Funciona **solo por USB** para máxima estabilidad y compatibilidad.

---

## 📦 Contenido
- `autoluces.py` → Script principal.
- `coches.json` → Configuración de colores y RPM por coche.
- `autoluces.bat` → Ejecución rápida con doble clic.
- `README.md` → Instrucciones y guía de personalización.
- `README.txt` → Copia en texto plano para usuarios que no abren `.md`.

---

## 🔧 Requisitos
- **Windows 10/11**
- **Python 3.8+**
- Librería `pywinusb` (ver instalación abajo)
- Automobilista 2 con telemetría activada
- DualShock 4 conectado por **USB**
Opcional: DS4Windows
El script funciona de forma independiente, pero es compatible con DS4Windows si lo usas para mapeo o perfiles.
- Mantén desactivada la opción “Ocultar DS4 Controller” (Hide DS4 Controller).
- Desactiva “Habilitar salida de datos al DS4” (Enable output data to DS4) para evitar conflictos con la lightbar.
- No es necesario para la conexión por USB, pero no interfiere si está configurado correctamente.

---

## 📌 Requisito adicional: sim-to-motec

Este proyecto utiliza **[sim-to-motec](https://github.com/GeekyDeaks/sim-to-motec)** como fuente de telemetría para sincronizar la lógica de la lightbar con datos en tiempo real del simulador.

**¿Por qué es necesario?**  
El script no lee la telemetría directamente del simulador. En su lugar, se apoya en _sim-to-motec_ para recibir datos como RPM, velocidad, luces, etc., que luego se usan para controlar la secuencia de colores.

🔗 **Descarga sim-to-motec** desde su repositorio oficial en GitHub:  
[https://github.com/GeekyDeaks/sim-to-motec](https://github.com/GeekyDeaks/sim-to-motec)

> **Nota:** Se recomienda usar la última versión disponible en la sección de *Releases* del repositorio.  
> Si no tienes _sim-to-motec_ instalado y configurado, el script no podrá sincronizar la lightbar con la telemetría.

## 📥 Instalación de dependencias
1. Instala Python desde [python.org](https://www.python.org/downloads/) (marca la casilla **Add to PATH** durante la instalación).
2. Abre la consola de comandos (CMD):
   - Pulsa `Windows + R`, escribe `cmd` y presiona **Enter**.
3. Escribe:
   ```bash
   pip install pywinusb

---

## Formato de configuración (`cars.json`)

Cada coche se define como un objeto con:

- **car_id**: Nombre exacto del coche como lo detecta el simulador.
- **thresholds**:
  - `speed_on`: Velocidad mínima (km/h) para activar color de crucero (0 si no se usa).
  - `rpm_steps`: Lista de RPM donde empieza cada fase.
- **colors**: Colores RGB para cada estado, en formato `[R, G, B]` (0–255).
- **blink**: Frecuencia de parpadeo en Hz para cada estado (0 = fijo).
  - Si no quieres parpadeo, usa 0.
  - Si quieres un parpadeo suave, usa 2–4 Hz.
  - Si quieres que el corte se vea como un “flash fuerte”, usa 6–8 Hz.
  - Si quieres que parezca que la luz tiembla o vibra, sube a 12–15 Hz.
  - **idle**: Color cuando el motor está apagado o el coche detenido.
  - **green**: Color para RPM bajas (crucero).
  - **yellow**: Color para RPM medias (preaviso).
  - **red_cut**: Color para RPM altas (corte).
- **sequence**: Lista de claves de color que se aplican en orden según `rpm_steps`.
- Los colores son completamente personalizables, al igual que `rpm_steps`.
- Puedes poner tantas fases y colores como desees, configura tu experiencia a tu gusto.

### Ejemplo: Audi R8 LMS GT3

```json
{
  "car_id": "Audi R8 LMS GT3",
  "thresholds": {
    "speed_on": 0,
    "rpm_steps": [7500, 7910, 8400]
  },
  "colors": {
    "idle": [0, 0, 0],
    "green": [120, 255, 0],
    "yellow": [255, 255, 0],
    "red_cut": [255, 0, 0]
  },
  "blink": {
    "idle": 0,
    "green": 0,
    "yellow": 0,
    "red_cut": 8
  },
  "sequence": ["green", "yellow", "red_cut"]
}
```

---

📌 Notas y futuro del proyecto
- Diseñado para conexión USB para máxima estabilidad.
- Si Automobilista 2 se actualiza y cambia la telemetría, puede ser necesario ajustar los offsets en el script.
- En futuras versiones se buscará:
	- Añadir todos los coches base del simulador en coches.json.
	- Implementar soporte oficial para conexión por Bluetooth.
- Puedes añadir cualquier coche nuevo al coches.json usando el nombre exacto que detecta el script.

---

📄 Licencia
- Libre para uso personal y modificación. Si lo compartes, por favor incluye este README.

---

## 🖱 Vista previa del `.bat` (ejecución rápida)

```bat
@echo off
cd /d "%~dp0"
python autoluces.py
pause
```
---

## Pasos para armarlo en tu PC

- **Crea la carpeta:** “AMS2-DS4-Lightbar-USB” en tu escritorio.
- **Copia archivos:** pega dentro los cuatro archivos tal cual aparecen arriba.
- **Instala dependencia:** 
  - Abre CMD.
  - Ejecuta: pip install pywinusb
- **Conecta el DS4:** por USB.
- **Ejecuta:** doble clic en autoluces.bat.
- **Abre AMS2:** entra a pista y verifica la lightbar.

---

## Prueba rápida en pista

- **Verifica detección:** en la consola debe aparecer “🎮 DS4 por USB listo…” y “🚗 Detectado: …”.
- **Comprueba colores:** sube RPM y confirma transición por tramos.
- **Parpadeo de corte:** ajusta parpadeo_ms en coches.json y valida el cambio.
- **Desconexión/reconexión:** mueve el cable; la luz debe recuperarse sola.

---



######## Disfruta mucho de este proyecto #######


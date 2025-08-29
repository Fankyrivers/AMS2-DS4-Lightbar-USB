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
- Opcional: DS4Windows
- El script funciona de forma independiente, pero es compatible con DS4Windows si lo usas para mapeo o perfiles.
- Mantén desactivada la opción “Ocultar DS4 Controller” (Hide DS4 Controller).
- Desactiva “Habilitar salida de datos al DS4” (Enable output data to DS4) para evitar conflictos con la lightbar.
- Puedes mantener activa la opcion anterior, no quitara la vibracion pero interfiere ligeramente con el control de la lightbar
- No es necesario para la conexión por USB, pero no interfiere si está configurado correctamente.

---

## ⚙️ Configuración en Automobilista 2
Para que el script funcione correctamente:
1. Abre Automobilista 2.
2. Ve a **Opciones → Sistema**.
3. Activa **Compartir datos de telemetría** (*Shared Memory*).
4. Selecciona **Project CARS 2**
5. En Frecuencia de UDP, se recomienda mantener la opcion en **5**.
6. En la version de protocolo UDP seleccionar **Project CARS 1**.
7. Guarda los cambios y reinicia el juego si es necesario.

--

## 📥 Instalación de dependencias
1. Instala Python desde [python.org](https://www.python.org/downloads/) (marca la casilla **Add to PATH** durante la instalación).
2. Abre la consola de comandos (CMD):
   - Pulsa `Windows + R`, escribe `cmd` y presiona **Enter**.
3. Escribe:
   ```bash
   pip install pywinusb

---

##🎨 Personalización
- Edita coches.json para cambiar:- Umbrales de RPM (verde, amarillo, naranja, azul, rojo, corte)
- Colores RGB (verde_rgb, amarillo_rgb, etc.)
- Velocidad de parpadeo (parpadeo_ms)
Ejemplo:
```json
"McLaren 720S GT3": {
    "verde": 7180,
    "amarillo": 7500,
    "naranja": 7680,
    "corte": 7800,
    "parpadeo_ms": 30,
    "verde_rgb": [0, 255, 0],
    "amarillo_rgb": [255, 255, 0],
    "naranja_rgb": [255, 180, 120],
    "corte_rgb": [0, 0, 255]
}
```

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


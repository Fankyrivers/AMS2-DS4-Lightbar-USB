import sys, os, struct, time, json
sys.path.append(os.path.dirname(__file__))

from pywinusb import hid
from stm.ams2.sampler import AMS2Sampler

OFFSET_CAR_NAME = 6444
CAR_NAME_MAXLEN = 64
OFFSET_RPM = 6852

JSON_FILE = "coches.json"

ds4 = None
color_actual = (0, 0, 0)
toggle = False
ultimo_toggle = time.time()

def get_ds4_device():
    devices = hid.HidDeviceFilter(vendor_id=0x054C).get_devices()
    for dev in devices:
        try:
            # Filtrar solo el mando físico
            if "Wireless Controller" not in dev.product_name:
                continue
            dev.open()
            reports = dev.find_output_reports()
            if reports and len(reports[0].get_raw_data()) >= 9:
                print(f"🎮 DS4 físico encontrado: {dev.product_name}")
                return dev
            dev.close()
        except:
            pass
    return None

def set_lightbar(r, g, b):
    global ds4, color_actual
    color_actual = (r, g, b)  # siempre actualizamos
    try:
        if ds4 is None or not ds4.is_plugged():
            ds4 = get_ds4_device()
            if not ds4:
                return
        report = ds4.find_output_reports()[0]
        data = [0x00] * len(report.get_raw_data())
        data[0], data[1] = 0x05, 0xFF
        data[6], data[7], data[8] = r, g, b
        report.set_raw_data(data)
        report.send()
    except Exception as e:
        print(f"[ERROR Lightbar] {e}")
        if ds4:
            ds4.close()
            ds4 = None

try:
    with open(JSON_FILE, "r") as f:
        coches_db = json.load(f)
except FileNotFoundError:
    print(f"❌ No se encontró {JSON_FILE}")
    coches_db = {}

def logica_multicolor(nombre, rpm, cfg):
    global toggle, ultimo_toggle
    cfg = dict(cfg)
    cfg.setdefault("verde", 0)
    cfg.setdefault("amarillo", cfg.get("rojo", cfg.get("naranja", cfg.get("corte", 99999))))
    cfg.setdefault("rojo", cfg.get("naranja", cfg.get("corte", 99999)))
    cfg.setdefault("parpadeo_ms", 100)

    # Corte con parpadeo usando corte_rgb si existe
    if rpm >= cfg["corte"]:
        intervalo = cfg.get("parpadeo_ms", 100) / 1000.0
        if time.time() - ultimo_toggle >= intervalo:
            toggle = not toggle
            ultimo_toggle = time.time()
        set_lightbar(*(cfg.get("corte_rgb", cfg.get("rojo_rgb", [255, 0, 0])) if toggle else (0, 0, 0)))
        return

    # Colores intermedios
    if "naranja" in cfg and rpm >= cfg["naranja"]:
        set_lightbar(*cfg.get("naranja_rgb", [255, 128, 0]))
        return
    if "azul" in cfg and rpm >= cfg["azul"]:
        set_lightbar(*cfg.get("azul_rgb", [0, 0, 255]))
        return
    if "amarillo" in cfg and rpm >= cfg["amarillo"]:
        set_lightbar(*cfg.get("amarillo_rgb", [255, 255, 0]))
        return
    if rpm >= cfg["verde"]:
        set_lightbar(*cfg.get("verde_rgb", [0, 255, 0]))
        return

    set_lightbar(0, 0, 0)

print("🏎 Shift‑light GT3 multicolor (filtro y reconexión activa) listo…")

sampler = AMS2Sampler(freq=10)
sampler.start()

try:
    coche_cfg = None
    while True:
        timestamp, raw_data = sampler.samples.get()

        coche_raw = raw_data[OFFSET_CAR_NAME:OFFSET_CAR_NAME+CAR_NAME_MAXLEN]
        coche_raw = coche_raw.split(b"\x00", 1)[0].decode('utf-8', errors='ignore').strip()

        rpm = struct.unpack_from("<f", raw_data, OFFSET_RPM)[0]

        if coche_raw in coches_db:
            if coche_cfg is None or coche_raw != coche_cfg.get("nombre"):
                coche_cfg = {"nombre": coche_raw, **coches_db[coche_raw]}
                print(f"🚗 Detectado: {coche_raw} → {coches_db[coche_raw]}")
            logica_multicolor(coche_raw, rpm, coche_cfg)
        else:
            if coche_raw:
                print(f"⚠️ {coche_raw} no está en {JSON_FILE}")
            coche_cfg = None

except KeyboardInterrupt:
    print("\n🛑 Detenido por usuario.")
finally:
    sampler.stop()
    if ds4:
        ds4.close()
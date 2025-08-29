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
    color_actual = (r, g, b)
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

# Cargar configuración
try:
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        coches_db = {c["car_id"]: c for c in json.load(f)}
    print(f"📄 Configuración cargada desde {JSON_FILE}")
except FileNotFoundError:
    print(f"❌ No se encontró {JSON_FILE}")
    coches_db = {}

def _blink_or_solid(color_tuple, hz):
    """Envía color sólido o parpadeo según hz."""
    global toggle, ultimo_toggle
    if hz and hz > 0:
        intervalo = 1.0 / hz / 2.0
        now = time.time()
        if now - ultimo_toggle >= intervalo:
            toggle = not toggle
            ultimo_toggle = now
        set_lightbar(*(color_tuple if toggle else (0, 0, 0)))
    else:
        set_lightbar(*color_tuple)

def logica_unificada(nombre, rpm, speed, pit, cfg):
    thr = cfg["thresholds"]
    cols = cfg["colors"]
    blink_cfg = cfg.get("blink", {})
    seq = cfg.get("sequence", [])
    steps = thr.get("rpm_steps", [])

    # Pit limiter (prioridad máxima)
    if pit:
        color = cols.get("blue", (0, 0, 255))
        _blink_or_solid(color, blink_cfg.get("blue", 0))
        return

    # Si no hay secuencia o pasos, idle
    if not steps or not seq:
        _blink_or_solid(cols.get("idle", (0, 0, 0)), blink_cfg.get("idle", 0))
        return

    # Determinar fase actual
    fase = -1
    for i, step in enumerate(steps):
        if rpm >= step:
            fase = i
        else:
            break

    if fase == -1:
        # Antes de la primera fase
        _blink_or_solid(cols.get("idle", (0, 0, 0)), blink_cfg.get("idle", 0))
        return

    # Si fase >= len(seq), usar última (corte)
    if fase >= len(seq):
        fase = len(seq) - 1

    color_key = seq[fase]
    color = cols.get(color_key, (255, 0, 0))
    hz = blink_cfg.get(color_key, 0)
    _blink_or_solid(color, hz)

print("🏎 Shift‑light multicolor v2.0 (JSON dinámico, reconexión activa) listo…")

sampler = AMS2Sampler(freq=20)  # 20 Hz reenvío constante
sampler.start()

try:
    coche_cfg = None
    coche_actual_id = None
    while True:
        timestamp, raw_data = sampler.samples.get()

        coche_raw = raw_data[OFFSET_CAR_NAME:OFFSET_CAR_NAME+CAR_NAME_MAXLEN]
        coche_raw = coche_raw.split(b"\x00", 1)[0].decode('utf-8', errors='ignore').strip()

        rpm = struct.unpack_from("<f", raw_data, OFFSET_RPM)[0]
        speed = 0.0  # Si luego agregas velocidad real, cámbiala aquí
        pit = False  # Si agregas flag de pit-limiter, cámbialo aquí

        if coche_raw in coches_db:
            if coche_actual_id != coche_raw:
                coche_cfg = coches_db[coche_raw]
                coche_actual_id = coche_raw
                print(f"🚗 Detectado: {coche_raw}")
                print(f"   thresholds: {coche_cfg.get('thresholds', {})}")
                print(f"   sequence: {coche_cfg.get('sequence', [])}")
                print(f"   blink: {coche_cfg.get('blink', {})}")
            logica_unificada(coche_raw, rpm, speed, pit, coche_cfg)
        else:
            if coche_raw:
                print(f"⚠️ {coche_raw} no está en {JSON_FILE}")
            coche_cfg = None
            coche_actual_id = None

except KeyboardInterrupt:
    print("\n🛑 Detenido por usuario.")
finally:
    sampler.stop()
    if ds4:
        ds4.close()
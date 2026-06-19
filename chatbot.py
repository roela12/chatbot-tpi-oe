import csv
from datetime import datetime, timedelta
from enum import Enum, auto

# ---------- Máquina de estados ----------
class Estado(Enum):
    LEGAJO = auto()
    FECHA_INICIO = auto()
    FECHA_FIN = auto()
    PROCESAR = auto()
    FIN = auto()

# ---------- Datos (CSV) ----------
def cargar_csv(archivo):
    with open(archivo, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def guardar_empleados(empleados):
    with open("empleados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["legajo", "nombre", "saldo_dias"])
        for e in empleados:
            w.writerow([e["legajo"], e["nombre"], e["saldo_dias"]])

def guardar_calendario(calendario):
    with open("calendario.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["fecha", "disponible"])
        for fecha, disp in calendario.items():
            w.writerow([fecha, disp])

def registrar_solicitud(legajo, nombre, inicio, fin, dias, estado, motivo):
    with open("solicitudes.csv", "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([legajo, nombre, inicio, fin, dias, estado,
                                 motivo, datetime.now().strftime("%Y-%m-%d %H:%M")])

# ---------- Validaciones ----------
def validar_fecha(texto):
    try:
        return datetime.strptime(texto.strip(), "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        return None

def rango_fechas(inicio, fin):
    d1, d2 = datetime.strptime(inicio, "%Y-%m-%d"), datetime.strptime(fin, "%Y-%m-%d")
    return [(d1 + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((d2 - d1).days + 1)]

# ---------- Bot principal: recorre la máquina de estados ----------
def main():
    empleados = cargar_csv("empleados.csv")
    calendario = {f["fecha"]: f["disponible"] for f in cargar_csv("calendario.csv")}

    estado = Estado.LEGAJO
    empleado, legajo, inicio, fin = None, None, None, None

    print("🤖 Hola! Soy el bot de vacaciones.")

    while estado != Estado.FIN:

        # GW0: validar identidad
        if estado == Estado.LEGAJO:
            legajo = input("🤖 Decime tu legajo:\n👤 ").strip()
            empleado = next((e for e in empleados if e["legajo"] == legajo), None)
            if not empleado:
                print("🤖 No te encontré. Probá de nuevo.")
                continue
            print(f"🤖 Hola {empleado['nombre']}, tu saldo es {empleado['saldo_dias']} días.")
            estado = Estado.FECHA_INICIO

        elif estado == Estado.FECHA_INICIO:
            texto = input("🤖 Fecha de inicio (AAAA-MM-DD):\n👤 ")
            inicio = validar_fecha(texto)
            if not inicio:
                print("🤖 Formato inválido. Usá AAAA-MM-DD.")
                continue
            estado = Estado.FECHA_FIN

        elif estado == Estado.FECHA_FIN:
            texto = input("🤖 Fecha de fin (AAAA-MM-DD):\n👤 ")
            fin = validar_fecha(texto)
            if not fin or fin < inicio:
                print("🤖 Fecha invalida o anterior al inicio. Probá de nuevo.")
                continue
            estado = Estado.PROCESAR

        elif estado == Estado.PROCESAR:
            dias = rango_fechas(inicio, fin)

            # GW1: saldo suficiente?
            if len(dias) > int(empleado["saldo_dias"]):
                registrar_solicitud(legajo, empleado["nombre"], inicio, fin, len(dias),
                                    "RECHAZADA", "saldo insuficiente")
                print("🤖 Solicitud RECHAZADA: no tienes suficientes días.")
                estado = Estado.FIN
                continue

            # GW2: fechas disponibles?
            ocupadas = [d for d in dias if calendario.get(d) != "SI"]
            if ocupadas:
                registrar_solicitud(legajo, empleado["nombre"], inicio, fin, len(dias),
                                    "RECHAZADA", f"fechas ocupadas: {ocupadas}")
                print(f"🤖 Solicitud RECHAZADA: fechas ocupadas {ocupadas}.")
                estado = Estado.FIN
                continue

            # Aprobar
            empleado["saldo_dias"] = int(empleado["saldo_dias"]) - len(dias)
            for d in dias:
                calendario[d] = "NO"
            guardar_empleados(empleados)
            guardar_calendario(calendario)
            registrar_solicitud(legajo, empleado["nombre"], inicio, fin, len(dias),
                                "APROBADA", "ok")
            print(f"🤖 Solicitud APROBADA. Saldo restante: {empleado['saldo_dias']} días.")
            estado = Estado.FIN

if __name__ == "__main__":
    main()

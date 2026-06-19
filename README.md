# Bot de Gestión de Vacaciones (simulación por consola)

TPI - Organización Empresarial - Tecnicatura Universitaria en Programación (UTN, a distancia)

## Descripción

Simulación de un chatbot de gestión de solicitudes de vacaciones, ejecutado
por consola (sin conexión a Telegram, WhatsApp ni ninguna API externa).
El usuario interactúa escribiendo respuestas directamente en la terminal.

El bot sigue el flujo modelado en el diagrama BPMN 2.0 del proceso, e
implementa una **máquina de estados** para recordar en qué paso se
encuentra cada usuario durante la conversación.

## Estructura del proyecto

```
bot_vacaciones/
├── bot_vacaciones.py     # Script principal del bot
├── empleados.csv         # Base de datos simulada: legajo, nombre, saldo de días
├── calendario.csv        # Base de datos simulada: disponibilidad por fecha
├── solicitudes.csv       # Historial de todas las solicitudes procesadas
└── README.md
```

## Cómo ejecutarlo

Requiere Python 3.8 o superior (no necesita librerías externas).

```bash
python3 chatbot.py
```

El bot va a hacer preguntas por consola. Respondé escribiendo y presionando
Enter.

## Flujo del proceso (correspondencia con el BPMN)

| Paso del bot              | Elemento BPMN                   | Validación / Decisión                            |
| ------------------------- | ------------------------------- | ------------------------------------------------ |
| Pedir legajo              | Tarea de usuario                | -                                                |
| Validar legajo            | Compuerta **GW0**               | ¿El legajo existe en `empleados.csv`?            |
| Pedir fecha de inicio/fin | Tarea de usuario                | Valida formato de fecha                          |
| Registrar solicitud       | Tarea de servicio               | Guarda intento en `solicitudes.csv`              |
| Evaluar saldo             | Compuerta **GW1**               | ¿Días solicitados ≤ saldo disponible?            |
| Evaluar disponibilidad    | Compuerta **GW2**               | ¿Todas las fechas están libres en el calendario? |
| Aprobar / Rechazar        | Tarea de servicio (fin proceso) | Actualiza `empleados.csv` y `calendario.csv`     |

## Base de datos simulada (CSV)

### `empleados.csv`

Columnas: `legajo`, `nombre`, `saldo_dias`.
Se actualiza automáticamente: cada vez que se aprueba una solicitud, se
descuentan los días utilizados del saldo del empleado.

### `calendario.csv`

Columnas: `fecha`, `disponible` (`SI` / `NO`).
Cuando se aprueba una solicitud, todas las fechas del rango pasan a `NO`,
simulando que ese período queda "tomado" y no puede ser solicitado de
nuevo por otro empleado.

### `solicitudes.csv`

Columnas: `id_solicitud`, `legajo`, `nombre`, `fecha_inicio`, `fecha_fin`,
`dias_solicitados`, `estado` (`APROBADA` / `RECHAZADA`), `motivo`,
`fecha_registro`.
Funciona como historial: nunca se borra, solo se le agregan filas nuevas
(append) cada vez que se procesa una solicitud, sea aprobada o rechazada.

## Manejo de errores (camino infeliz)

El bot contempla los siguientes casos de entrada inválida:

- **Legajo inexistente**: pide reingresar el dato, hasta un máximo de 3
  intentos; al superarlo, deriva a un agente humano (simulado) y corta la
  sesión.
- **Fecha con formato inválido** (texto en lugar de fecha, o formato no
  reconocido): pide reingresar sin avanzar de estado.
- **Fecha de fin anterior a la fecha de inicio**: pide reingresar la fecha
  de fin.
- **Saldo insuficiente**: rechaza la solicitud y la registra con el
  motivo correspondiente.
- **Conflicto de fechas** (alguna fecha del rango ya está ocupada):
  rechaza la solicitud, indica qué fechas están en conflicto, y sugiere
  elegir otro rango.

## Empleados de prueba incluidos

| Legajo | Nombre          | Saldo inicial |
| ------ | --------------- | ------------- |
| 1001   | Juan Perez      | 14 días       |
| 1002   | Maria Gomez     | 21 días       |
| 1003   | Carlos Diaz     | 5 días        |
| 1004   | Lucia Fernandez | 0 días        |
| 1005   | Andres Romero   | 10 días       |

## Autor

Rodrigo Elias Martinez Jalil

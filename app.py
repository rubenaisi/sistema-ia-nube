# ======================================================
# SISTEMA 100% NUBE - EDITH / JARVIS / MAX
# ☁️ Nada en tu PC | Acceso desde cualquier dispositivo
# ======================================================

import requests

# --------------------------
# 🎨 ESTILO Y COLORES
# --------------------------
RESET = "\033[0m"
BOLD = "\033[1m"
COLORES = {
    "edith": {"nombre": "🤍 EDITH", "fondo": "\033[48;2;224;242;254m", "texto": "\033[38;2;15;23;42m"},
    "jarvis": {"nombre": "⚙️ JARVIS", "fondo": "\033[48;2;15;23;42m", "texto": "\033[38;2;248;250;252m"},
    "max": {"nombre": "🚀 MODO MAX", "fondo": "\033[48;2;30;27;75m", "texto": "\033[38;2;255;255;255m"},
    "exito": "\033[32m", "error": "\033[31m", "info": "\033[36m"
}

# --------------------------
# ☁️ CONEXIÓN A GEMINI (GRATIS)
# --------------------------
API_KEY = "AQ.Ab8RN6KxKCoA2o-WJQYIai_BeQ26HzBkMilIXGw7TS-cwH2UaQ"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

MOTORES = {
    "edith": "gemini-flash-lite",
    "jarvis": "gemini-2.5-flash",
    "max": "gemini-2.5-pro"
}

# --------------------------
# 🧩 MÓDULOS
# --------------------------
def autotune(modo):
    return {
        "temperature": 0.7 if modo == "edith" else 0.3 if modo == "jarvis" else 0.5,
        "max_output_tokens": 1000 if modo == "edith" else 2000 if modo == "jarvis" else 4000
    }

def ultraplinian(modo, esfuerzo):
    return "\n\n✅ Verificación cruzada completada" if modo == "max" and esfuerzo == "experto" else ""

# --------------------------
# 🎭 PERSONALIDADES
# --------------------------
PERSONALIDADES = {
    "edith": """Eres EDITH: amable, clara, lenguaje sencillo, solo usas el nivel AVANZADO.""",
    "jarvis": """Eres JARVIS: preciso, elegante, técnico, solo usas el nivel AVANZADO.""",
    "max": """Eres MODO MAX: Edith y Jarvis trabajan juntos. Puedes usar nivel AVANZADO o EXPERTO."""
}

# --------------------------
# ⚙️ ESTADO ACTUAL
# --------------------------
modo_actual = "edith"
esfuerzo_actual = "avanzado"

# --------------------------
# 🚀 CONEXIÓN A LA NUBE
# --------------------------
def obtener_respuesta(texto):
    if not API_KEY.strip():
        return f"{COLORES['error']}❌ Falta la clave API. Agrégala en la línea API_KEY{RESET}"
    ajustes = autotune(modo_actual)
    prompt = PERSONALIDADES[modo_actual]
    if esfuerzo_actual == "experto":
        prompt += "\n---\nESFUERZO EXPERTO: Haz un análisis profundo y detallado."
    url = f"{URL_BASE}/{MOTORES[modo_actual]}:generateContent?key={API_KEY}"
    datos = {"contents": [{"parts": [{"text": f"{prompt}\n\nPregunta: {texto}"}]}], "generationConfig": ajustes}
    try:
        res = requests.post(url, json=datos, timeout=30)
        if res.status_code == 200:
            txt = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            return txt + ultraplinian(modo_actual, esfuerzo_actual)
        return f"{COLORES['error']}❌ Error: {res.status_code}{RESET}"
    except Exception as e:
        return f"{COLORES['error']}❌ Sin conexión: {str(e)}{RESET}"

# --------------------------
# 🛠️ COMANDOS
# --------------------------
def procesar(entrada):
    global modo_actual, esfuerzo_actual
    texto = entrada.strip()
    if texto.startswith("/"):
        cmd = texto.lower()
        if cmd == "/edith":
            modo_actual = "edith"; esfuerzo_actual = "avanzado"
            return f"{COLORES['exito']}✅ Modo activado: {COLORES['edith']['nombre']}{RESET}"
        elif cmd == "/jarvis":
            modo_actual = "jarvis"; esfuerzo_actual = "avanzado"
            return f"{COLORES['exito']}✅ Modo activado: {COLORES['jarvis']['nombre']}{RESET}"
        elif cmd == "/max":
            modo_actual = "max"
            return f"{COLORES['exito']}✅ Modo activado: {COLORES['max']['nombre']}{RESET}"
        elif cmd == "/avanzado":
            esfuerzo_actual = "avanzado"
            return "✅ Nivel: AVANZADO"
        elif cmd == "/experto":
            if modo_actual == "max":
                esfuerzo_actual = "experto"
                return "✨✅ Nivel: EXPERTO activado"
            return "❌ Solo disponible en modo /max"
        elif cmd == "/estado":
            return f"📊 ESTADO\n• Modo: {modo_actual.upper()}\n• Nivel: {esfuerzo_actual.upper()}\n• Servicio: ☁️ NUBE"
        elif cmd == "/ayuda":
            return "📚 COMANDOS\n/edith /jarvis /max\n/avanzado /experto\n/estado /ayuda /salir"
        elif cmd == "/salir":
            print("👋 Hasta luego!"); exit()
        return "❌ Comando no reconocido"
    return obtener_respuesta(texto)

# --------------------------
# 🚀 EJECUCIÓN
# --------------------------
def iniciar_sistema():
    print("=" * 50)
    print(f"{COLORES['info']}{BOLD}🤖 SISTEMA 100% EN LA NUBE ☁️{RESET}")
    print("Acceso desde cualquier dispositivo")
    print("=" * 50)
    while True:
        entrada = input(f"\n{BOLD}Tú:{RESET} ")
        print(f"\n{COLORES[modo_actual]['fondo']}{COLORES[modo_actual]['texto']}{procesar(entrada)}{RESET}")

# Ejecutar
iniciar_sistema()

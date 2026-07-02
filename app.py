# ======================================================
# SISTEMA 100% NUBE - EDITH / JARVIS / MAX
# ☁️ Nada en tu PC | Acceso desde cualquier dispositivo
# ======================================================

from flask import Flask, render_template_string, request
import requests

# --------------------------
# 🎨 ESTILO Y COLORES WEB
# --------------------------
ESTILOS = {
    "edith": {"nombre": "🤍 EDITH", "fondo": "#E0F2FE", "texto": "#0F172A"},
    "jarvis": {"nombre": "⚙️ JARVIS", "fondo": "#0F172A", "texto": "#F8FAFC"},
    "max": {"nombre": "🚀 MODO MAX", "fondo": "#1E1B4B", "texto": "#FFFFFF"},
    "exito": "#16A34A", "error": "#DC2626", "info": "#2563EB"
}

# --------------------------
# ☁️ CONEXIÓN A GEMINI (GRATIS)
# --------------------------
API_KEY = "AQ.Ab8RN6KxKCoA2o-WJQYIai_BeQ26HzBkMilIXGw7TS-cwH2UaQ"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

MOTORES = {
    "edith": "gemini-1.5-flash-latest",
    "jarvis": "gemini-2.5-flash-preview-05-2025",
    "max": "gemini-2.5-pro-preview-05-2025"
}

# --------------------------
# ⚙️ ESTADO ACTUAL
# --------------------------
modo_actual = "edith"
esfuerzo_actual = "avanzado"

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
# 🚀 CONEXIÓN A LA NUBE
# --------------------------
def obtener_respuesta(texto):
    if not API_KEY.strip():
        return "❌ Falta la clave API. Agrégala en la línea API_KEY"
    ajustes = autotune(modo_actual)
    prompt = PERSONALIDADES[modo_actual]
    if esfuerzo_actual == "experto":
        prompt += "\n---\nESFUERZO EXPERTO: Haz un análisis profundo y detallado."
    url = f"{URL_BASE}/{MOTORES[modo_actual]}:generateContent?key={API_KEY}"
    datos = {
        "contents": [{"parts": [{"text": f"{prompt}\n\nPregunta: {texto}"}]}],
        "generationConfig": ajustes
    }
    try:
        res = requests.post(url, json=datos, timeout=30)
        if res.status_code == 200:
            txt = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            return txt + ultraplinian(modo_actual, esfuerzo_actual)
        return f"❌ Error en la API: Código {res.status_code}"
    except Exception as e:
        return f"❌ Sin conexión: {str(e)}"

# --------------------------
# 🛠️ PROCESAMIENTO DE COMANDOS
# --------------------------
def procesar(entrada):
    global modo_actual, esfuerzo_actual
    texto = entrada.strip()
    if texto.startswith("/"):
        cmd = texto.lower()
        if cmd == "/edith":
            modo_actual = "edith"; esfuerzo_actual = "avanzado"
            return "✅ Modo activado: 🤍 EDITH"
        elif cmd == "/jarvis":
            modo_actual = "jarvis"; esfuerzo_actual = "avanzado"
            return "✅ Modo activado: ⚙️ JARVIS"
        elif cmd == "/max":
            modo_actual = "max"
            return "✅ Modo activado: 🚀 MODO MAX"
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
            return "📚 COMANDOS\n/edith /jarvis /max\n/avanzado /experto\n/estado /ayuda"
        return "❌ Comando no reconocido"
    return obtener_respuesta(texto)

# --------------------------
# 🌐 INTERFAZ WEB
# --------------------------
PAGINA_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema IA en la Nube</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif; }
        body { background: {{fondo}}; color: {{texto}}; padding: 20px; max-width: 900px; margin: 0 auto; transition: all 0.3s ease; }
        h1 { text-align: center; margin-bottom: 20px; color: {{info}}; }
        .estado { padding: 12px; border-radius: 8px; background: rgba(255,255,255,0.15); margin-bottom: 20px; text-align: center; font-weight: bold; }
        #chat { height: 520px; overflow-y: auto; border: 1px solid rgba(255,255,255,0.25); padding: 15px; border-radius: 8px; margin-bottom: 15px; background: rgba(0,0,0,0.1); }
        .mensaje { margin: 12px 0; padding: 10px 14px; border-radius: 6px; line-height: 1.5; }
        .usuario { background: rgba(37, 99, 235, 0.2); text-align: right; margin-left: 20%; }
        .ia { background: rgba(22, 163, 74, 0.2); text-align: left; margin-right: 20%; }
        form { display: flex; gap: 10px; }
        input { flex: 1; padding: 13px; border-radius: 6px; border: none; background: rgba(255,255,255,0.95); color: #111; font-size: 16px; }
        button { padding: 13px 22px; border: none; border-radius: 6px; background: {{exito}}; color: white; cursor: pointer; font-weight: bold; font-size: 16px; }
        button:hover { opacity: 0.9; }
    </style>
</head>
<body>
    <h1>🤖 Sistema IA 100% en la Nube</h1>
    <div class="estado" id="estado">
        Modo: {{modo}} | Nivel: {{esfuerzo}}
    </div>
    <div id="chat"></div>
    <form onsubmit="enviarMensaje(event)">
        <input type="text" id="texto" placeholder="Escribe tu mensaje o comando..." required>
        <button type="submit">Enviar</button>
    </form>

    <script>
        const chat = document.getElementById('chat');
        const estadoDiv = document.getElementById('estado');

        async function enviarMensaje(e) {
            e.preventDefault();
            const input = document.getElementById('texto');
            const texto = input.value.trim();
            if (!texto) return;

            agregarMensaje('Tú', texto, 'usuario');
            input.value = '';

            const respuesta = await fetch('/procesar', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({texto: texto})
            });
            const datos = await respuesta.json();
            agregarMensaje('IA', datos.mensaje, 'ia');

            if (datos.estado) {
                estadoDiv.innerHTML = `Modo: ${datos.modo} | Nivel: ${datos.esfuerzo}`;
                document.body.style.background = datos.fondo;
                document.body.style.color = datos.texto;
            }

            chat.scrollTop = chat.scrollHeight;
        }

        function agregarMensaje(quien, texto, clase) {
            const div = document.createElement('div');
            div.className = `mensaje ${clase}`;
            div.innerHTML = `<strong>${quien}:</strong><br>${texto.replace(/\n/g, '<br>')}`;
            chat.appendChild(div);
        }
    </script>
</body>
</html>
"""

# --------------------------
# 🚀 INICIO DE LA APLICACIÓN
# --------------------------
app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template_string(
        PAGINA_HTML,
        fondo=ESTILOS[modo_actual]["fondo"],
        texto=ESTILOS[modo_actual]["texto"],
        exito=ESTILOS["exito"],
        info=ESTILOS["info"],
        modo=ESTILOS[modo_actual]["nombre"],
        esfuerzo=esfuerzo_actual.upper()
    )

@app.route('/procesar', methods=['POST'])
def ruta_procesar():
    datos = request.get_json()
    respuesta = procesar(datos["texto"])
    return {
        "mensaje": respuesta,
        "estado": True,
        "modo": ESTILOS[modo_actual]["nombre"],
        "esfuerzo": esfuerzo_actual.upper(),
        "fondo": ESTILOS[modo_actual]["fondo"],
        "texto": ESTILOS[modo_actual]["texto"]
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

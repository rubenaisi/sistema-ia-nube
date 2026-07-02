# ======================================================
# SISTEMA IA ESTILO CHATGPT - GEMINI FUNCIONAL
# ======================================================

from flask import Flask, render_template_string, request
import requests

# --------------------------
# ⚠️ CONFIGURACIÓN CORRECTA
# --------------------------
API_KEY = "AIzaSyAb8RNGKbPtKrRmuWtHzRxDU26ZRpQGRGYNhCEbUmcp3iC0zvQ"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

MOTORES = {
    "edith": "gemini-1.5-flash-latest",
    "jarvis": "gemini-1.5-flash-latest",
    "max": "gemini-1.5-pro-latest"
}

modo_actual = "edith"
esfuerzo_actual = "avanzado"

# --------------------------
# 🎭 PERSONALIDADES
# --------------------------
PERSONALIDADES = {
    "edith": """Eres EDITH: amable, clara, sencilla y directa. Responde siempre en español.""",
    "jarvis": """Eres JARVIS: preciso, técnico, ordenado y profesional.""",
    "max": """Eres MODO MAX: haz análisis completos, profundos y detallados."""
}

def autotune(modo):
    return {
        "temperature": 0.7 if modo == "edith" else 0.3 if modo == "jarvis" else 0.5,
        "max_output_tokens": 1000 if modo == "edith" else 2500 if modo == "jarvis" else 6000
    }

# --------------------------
# 🚀 CONEXIÓN CON GEMINI
# --------------------------
def obtener_respuesta(texto):
    if not API_KEY or not API_KEY.startswith("AIzaSy"):
        return "❌ ERROR: Clave API inválida"
    
    ajustes = autotune(modo_actual)
    prompt = PERSONALIDADES[modo_actual]
    if esfuerzo_actual == "experto":
        prompt += "\n---\nNIVEL EXPERTO: Responde con máximo detalle."

    url = f"{URL_BASE}/{MOTORES[modo_actual]}:generateContent?key={API_KEY}"
    datos = {
        "contents": [{"parts": [{"text": f"{prompt}\n\nPregunta: {texto}"}]}],
        "generationConfig": ajustes
    }

    try:
        res = requests.post(url, json=datos, timeout=45)
        if res.status_code == 200:
            return res.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"❌ Error: Código {res.status_code}"
    except Exception as e:
        return f"❌ Sin conexión: {str(e)}"

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
            return "✅ Modo activado: 🤍 EDITH"
        elif cmd == "/jarvis":
            modo_actual = "jarvis"; esfuerzo_actual = "avanzado"
            return "✅ Modo activado: ⚙️ JARVIS"
        elif cmd == "/max":
            modo_actual = "max"; esfuerzo_actual = "avanzado"
            return "✅ Modo activado: 🚀 MODO MAX"
        elif cmd == "/avanzado":
            esfuerzo_actual = "avanzado"
            return "✅ Nivel: AVANZADO"
        elif cmd == "/experto":
            if modo_actual == "max":
                esfuerzo_actual = "experto"
                return "✨✅ Nivel EXPERTO activado"
            return "❌ Solo disponible en modo /max"
        elif cmd == "/estado":
            return f"📊 ESTADO\n• Modo: {modo_actual.upper()}\n• Nivel: {esfuerzo_actual.upper()}"
        elif cmd == "/ayuda":
            return "📚 COMANDOS:\n/edith → Modo amable\n/jarvis → Modo técnico\n/max → Modo completo\n/avanzado /experto\n/estado /ayuda"
        return "❌ Comando no reconocido. Usa /ayuda."
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
    <title>Chat IA - Gemini</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        fondo: '#202123',
                        lateral: '#343541',
                        usuario: '#343541',
                        ia: '#444654',
                        texto: '#ECECF1',
                        acento: '#10A37F',
                        acento_hover: '#15b892'
                    },
                    fontFamily: { inter: ['Inter', 'sans-serif'] }
                }
            }
        }
    </script>
    <style>
        .scrollbar-thin { scrollbar-width: thin; scrollbar-color: #565869 transparent; }
        .scrollbar-thin::-webkit-scrollbar { width: 8px; }
        .scrollbar-thin::-webkit-scrollbar-thumb { background: #565869; border-radius: 4px; }
        .mensaje-animado { animation: entrada 0.3s ease-out forwards; }
        @keyframes entrada { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:translateY(0); } }
        .typing span { display:inline-block; width:6px; height:6px; border-radius:50%; background:#ECECF1; margin:0 2px; animation: parpadeo 1.4s infinite; }
        .typing span:nth-child(2) { animation-delay:0.2s; }
        .typing span:nth-child(3) { animation-delay:0.4s; }
        @keyframes parpadeo { 0%,60%,100% { opacity:0.3; } 30% { opacity:1; } }
    </style>
</head>
<body class="bg-fondo text-texto min-h-screen flex flex-col">
    <aside class="hidden md:flex flex-col w-64 bg-lateral p-4 gap-4">
        <button onclick="nuevoChat()" class="border border-gray-600 rounded-lg p-3 hover:bg-gray-600 transition">
            <i class="fa fa-plus mr-2"></i> Nuevo chat
        </button>
        <div class="mt-auto text-sm opacity-70">
            <p>Modo: <strong id="modo-lateral">EDITH</strong></p>
            <p>Nivel: <strong id="nivel-lateral">AVANZADO</strong></p>
        </div>
    </aside>

    <main class="flex-1 flex flex-col h-screen">
        <header class="border-b border-gray-700 p-4 text-center">
            <h1 class="text-xl font-semibold">🤖 Chat IA - Sistema Gemini</h1>
        </header>

        <div id="chat" class="flex-1 overflow-y-auto scrollbar-thin p-6 space-y-6 max-w-4xl mx-auto w-full">
            <div class="mensaje-animado flex gap-4">
                <div class="w-8 h-8 rounded-full bg-acento flex items-center justify-center">IA</div>
                <div>
                    <p class="text-lg font-medium mb-1">¡Hola! Soy tu asistente con Gemini</p>
                    <p class="opacity-90">Escribe cualquier pregunta o usa <code class="bg-gray-700 px-1 rounded">/ayuda</code></p>
                </div>
            </div>
        </div>

        <form id="formulario" class="p-4 border-t border-gray-700">
            <div class="max-w-4xl mx-auto flex gap-3">
                <input type="text" id="texto" placeholder="Escribe tu mensaje..." required
                    class="flex-1 bg-ia border border-gray-600 rounded-xl px-4 py-3 focus:outline-none focus:ring-1 focus:ring-acento">
                <button type="submit" class="bg-acento hover:bg-acento_hover px-5 py-3 rounded-xl">
                    <i class="fa fa-paper-plane"></i>
                </button>
            </div>
        </form>
    </main>

    <script>
        const chat = document.getElementById('chat');
        const formulario = document.getElementById('formulario');
        const inputTexto = document.getElementById('texto');
        const modoLateral = document.getElementById('modo-lateral');
        const nivelLateral = document.getElementById('nivel-lateral');

        async function enviarMensaje(e) {
            e.preventDefault();
            const texto = inputTexto.value.trim();
            if (!texto) return;

            agregarMensaje('Tú', texto, 'bg-usuario');
            inputTexto.value = '';
            inputTexto.disabled = true;

            const cargando = agregarCargando();

            try {
                const res = await fetch('/procesar', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({texto: texto})
                });
                const datos = await res.json();
                cargando.remove();
                agregarMensaje('IA', datos.mensaje, 'bg-ia');
                if (datos.estado) {
                    modoLateral.textContent = datos.modo;
                    nivelLateral.textContent = datos.nivel;
                }
            } catch {
                cargando.remove();
                agregarMensaje('IA', '❌ Error de conexión. Intenta de nuevo.', 'bg-ia');
            }

            inputTexto.disabled = false;
            inputTexto.focus();
            chat.scrollTop = chat.scrollHeight;
        }

        function agregarMensaje(quien, texto, fondo) {
            const div = document.createElement('div');
            div.className = 'mensaje-animado flex gap-4';
            div.innerHTML = `
                <div class="w-8 h-8 rounded-full ${quien==='IA'?'bg-acento':'bg-gray-500'} flex items-center justify-center shrink-0">${quien==='IA'?'IA':'Tú'}</div>
                <div class="flex-1 ${fondo} p-3 rounded-xl whitespace-pre-wrap">${texto.replace(/\n/g,'<br>')}</div>
            `;
            chat.appendChild(div);
            return div;
        }

        function agregarCargando() {
            const div = document.createElement('div');
            div.className = 'mensaje-animado flex gap-4';
            div.innerHTML = `
                <div class="w-8 h-8 rounded-full bg-acento flex items-center justify-center">IA</div>
                <div class="bg-ia p-3 rounded-xl typing"><span></span><span></span><span></span></div>
            `;
            chat.appendChild(div);
            return div;
        }

        function nuevoChat() {
            chat.innerHTML = `
                <div class="mensaje-animado flex gap-4">
                    <div class="w-8 h-8 rounded-full bg-acento flex items-center justify-center">IA</div>
                    <div>
                        <p class="text-lg font-medium mb-1">¡Hola! Soy tu asistente con Gemini</p>
                        <p class="opacity-90">Escribe cualquier pregunta o usa <code class="bg-gray-700 px-1 rounded">/ayuda</code></p>
                    </div>
                </div>
            `;
        }

        formulario.addEventListener('submit', enviarMensaje);
    </script>
</body>
</html>
"""

# --------------------------
# 🚀 ARRANQUE FINAL
# --------------------------
app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template_string(PAGINA_HTML)

@app.route('/procesar', methods=['POST'])
def ruta_procesar():
    datos = request.get_json()
    respuesta = procesar(datos["texto"])
    return {
        "mensaje": respuesta,
        "estado": True,
        "modo": modo_actual.upper(),
        "nivel": esfuerzo_actual.upper()
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

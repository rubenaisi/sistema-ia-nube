# ======================================================
# SISTEMA IA 100% NUBE - ESTILO CHATGPT CON GEMINI
# ☁️ Acceso desde cualquier dispositivo
# ======================================================

from flask import Flask, render_template_string, request
import requests

# --------------------------
# ⚙️ CONFIGURACIÓN GEMINI
# --------------------------
API_KEY = "AIzaSy_TU_CLAVE_AQUÍ"  # ⚠️ PON AQUÍ TU CLAVE REAL (empieza por AIzaSy...)
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
    "edith": """Eres EDITH: amable, clara, sencilla y directa. Responde en español, con explicaciones fáciles de entender.""",
    "jarvis": """Eres JARVIS: preciso, técnico, ordenado y profesional. Responde estructurado y detallado cuando sea necesario.""",
    "max": """Eres MODO MAX: análisis completo, profundo y detallado. Responde con toda la información posible y explicaciones amplias."""
}

def autotune(modo):
    return {
        "temperature": 0.7 if modo == "edith" else 0.3 if modo == "jarvis" else 0.5,
        "max_output_tokens": 1000 if modo == "edith" else 2500 if modo == "jarvis" else 6000
    }

# --------------------------
# 🚀 CONEXIÓN CON LA IA
# --------------------------
def obtener_respuesta(texto):
    if not API_KEY or not API_KEY.startswith("AIzaSy"):
        return "❌ Error: Clave API inválida o no configurada correctamente."
    
    ajustes = autotune(modo_actual)
    prompt = PERSONALIDADES[modo_actual]
    if esfuerzo_actual == "experto":
        prompt += "\n---\nNIVEL EXPERTO: Haz un análisis muy detallado, completo y profundo."

    url = f"{URL_BASE}/{MOTORES[modo_actual]}:generateContent?key={API_KEY}"
    datos = {
        "contents": [{"parts": [{"text": f"{prompt}\n\nPregunta: {texto}"}]}],
        "generationConfig": ajustes
    }

    try:
        res = requests.post(url, json=datos, timeout=45)
        if res.status_code == 200:
            return res.json()["candidates"][0]["content"]["parts"][0]["text"]
        return f"❌ Error de conexión: Código {res.status_code}. Revisa tu clave o modelo."
    except Exception as e:
        return f"❌ Sin conexión: {str(e)}"

# --------------------------
# 🛠️ PROCESAR COMANDOS
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
            return "📚 COMANDOS DISPONIBLES:\n/edith → Modo amable\n/jarvis → Modo técnico\n/max → Modo completo\n/avanzado /experto → Cambiar nivel\n/estado /ayuda"
        return "❌ Comando no reconocido. Usa /ayuda para ver opciones."
    return obtener_respuesta(texto)

# --------------------------
# 🌐 INTERFAZ WEB ESTILO CHATGPT
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
                    fontFamily: {
                        inter: ['Inter', 'system-ui', 'sans-serif']
                    }
                }
            }
        }
    </script>
    <style type="text/tailwindcss">
        @layer utilities {
            .scrollbar-thin {
                scrollbar-width: thin;
                scrollbar-color: #565869 transparent;
            }
            .scrollbar-thin::-webkit-scrollbar {
                width: 8px;
            }
            .scrollbar-thin::-webkit-scrollbar-track {
                background: transparent;
            }
            .scrollbar-thin::-webkit-scrollbar-thumb {
                background-color: #565869;
                border-radius: 4px;
            }
            .mensaje-animado {
                animation: entrada 0.3s ease-out forwards;
            }
            @keyframes entrada {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .typing {
                display: inline-block;
                width: 6px;
                height: 6px;
                border-radius: 50%;
                background: #ECECF1;
                margin: 0 2px;
                animation: parpadeo 1.4s infinite ease-in-out;
            }
            .typing:nth-child(2) { animation-delay: 0.2s; }
            .typing:nth-child(3) { animation-delay: 0.4s; }
            @keyframes parpadeo {
                0%, 60%, 100% { opacity: 0.3; }
                30% { opacity: 1; }
            }
        }
    </style>
</head>
<body class="bg-fondo text-texto font-inter min-h-screen flex flex-col">
    <!-- Barra lateral -->
    <aside class="hidden md:flex flex-col w-64 bg-lateral p-4 gap-4">
        <button onclick="nuevoChat()" class="border border-gray-600 rounded-lg p-3 text-left hover:bg-gray-600 transition-colors">
            <i class="fa fa-plus mr-2"></i> Nuevo chat
        </button>
        <div class="mt-auto text-sm opacity-70">
            <p>Modo: <strong id="modo-lateral">EDITH</strong></p>
            <p>Nivel: <strong id="nivel-lateral">AVANZADO</strong></p>
        </div>
    </aside>

    <!-- Contenido principal -->
    <main class="flex-1 flex flex-col h-screen">
        <!-- Encabezado -->
        <header class="border-b border-gray-700 p-4 text-center">
            <h1 class="text-xl font-semibold">🤖 Chat IA - Sistema Gemini</h1>
        </header>

        <!-- Área de mensajes -->
        <div id="chat" class="flex-1 overflow-y-auto scrollbar-thin p-6 space-y-6 max-w-4xl mx-auto w-full">
            <div class="mensaje-animado flex gap-4">
                <div class="w-8 h-8 rounded-full bg-acento flex items-center justify-center text-sm">IA</div>
                <div class="flex-1">
                    <p class="text-lg font-medium mb-1">¡Hola! Soy tu asistente con Gemini</p>
                    <p class="opacity-90">Escribe cualquier pregunta o usa <code class="bg-gray-700 px-1 rounded">/ayuda</code> para ver todos los comandos disponibles.</p>
                </div>
            </div>
        </div>

        <!-- Caja de entrada -->
        <form id="formulario" class="p-4 border-t border-gray-700">
            <div class="max-w-4xl mx-auto flex gap-3">
                <input type="text" id="texto" placeholder="Escribe tu mensaje..." required
                    class="flex-1 bg-ia border border-gray-600 rounded-xl px-4 py-3 text-base focus:outline-none focus:ring-1 focus:ring-acento">
                <button type="submit" class="bg-acento hover:bg-acento_hover text-white px-5 py-3 rounded-xl transition-colors">
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

            // Mostrar mensaje del usuario
            agregarMensaje('Tú', texto, 'bg-usuario');
            inputTexto.value = '';
            inputTexto.disabled = true;

            // Indicador de "escribiendo"
            const cargando = agregarIndicadorCargando();

            try {
                const respuesta = await fetch('/procesar', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({texto: texto})
                });
                const datos = await respuesta.json();
                
                cargando.remove();
                agregarMensaje('IA', datos.mensaje, 'bg-ia');

                // Actualizar estado
                if (datos.estado) {
                    modoLateral.textContent = datos.modo;
                    nivelLateral.textContent = datos.nivel;
                }
            } catch (err) {
                cargando.remove();
                agregarMensaje('IA', '❌ Error de conexión. Intenta de nuevo más tarde.', 'bg-ia');
            }

            inputTexto.disabled = false;
            inputTexto.focus();
            chat.scrollTop = chat.scrollHeight;
        }

        function agregarMensaje(quien, texto, fondo) {
            const div = document.createElement('div');
            div.className = `mensaje-animado flex gap-4 max-w-4xl`;
            div.innerHTML = `
                <div class="w-8 h-8 rounded-full ${quien === 'IA' ? 'bg-acento' : 'bg-gray-500'} flex items-center justify-center text-sm shrink-0">
                    ${quien === 'IA' ? 'IA' : 'Tú'}
                </div>
                <div class="flex-1 ${fondo} p-3 rounded-xl whitespace-pre-wrap leading-relaxed">
                    ${texto.replace(/\n/g, '<br>')}
                </div>
            `;
            chat.appendChild(div);
            return div;
        }

        function agregarIndicadorCargando() {
            const div = document.createElement('div');
            div.className = 'mensaje-animado flex gap-4 max-w-4xl';
            div.innerHTML = `
                <div class="w-8 h-8 rounded-full bg-acento flex items-center justify-center text-sm">IA</div>
                <div class="bg-ia p-3 rounded-xl flex items-center">
                    <div class="typing"></div>
                    <div class="typing"></div>
                    <div class="typing"></div>
                </div>
            `;
            chat.appendChild(div);
            return div;
        }

        function nuevoChat() {
            chat.innerHTML = `
                <div class="mensaje-animado flex gap-4">
                    <div class="w-8 h-8 rounded-full bg-acento flex items-center justify-center text-sm">IA</div>
                    <div class="flex-1">
                        <p class="text-lg font-medium mb-1">¡Hola! Soy tu asistente con Gemini</p>
                        <p class="opacity-90">Escribe cualquier pregunta o usa <code class="bg-gray-700 px-1 rounded">/ayuda</code> para ver todos los comandos disponibles.</p>
                    </div>
                </div>
            `;
            inputTexto.focus();
        }

        formulario.addEventListener('submit', enviarMensaje);
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

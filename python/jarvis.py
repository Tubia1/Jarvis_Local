import json
import subprocess
import requests
import whisper
import pyttsx3
import sounddevice as sd
from scipy.io.wavfile import write

AUDIO_PATH = "../audios/live.wav"
MODEL_NAME = "qwen2.5:1.5b"

DURATION = 8
SAMPLE_RATE = 44100


def grabar_audio():

    print("Grabando... hablá ahora")

    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1
    )

    sd.wait()

    write(AUDIO_PATH, SAMPLE_RATE, audio)

    print("Audio guardado.")


def transcribir_audio(model):

    print("Transcribiendo audio...")

    result = model.transcribe(
        AUDIO_PATH,
        language="spanish"
    )

    text = result["text"]

    print("Texto detectado:")
    print(text)

    return text


def obtener_respuesta(text):
 


    prompt = f"""
Sos Jarvis, un asistente de voz local.

Tu tarea es decidir si el usuario quiere ejecutar una acción o conversar.

Respondé SOLO con JSON válido.
No uses markdown.
No uses ```json.

Tipos posibles:
- action
- chat

Acciones permitidas:
- open_vscode
- open_notepad
- open_calculator
- open_chrome
- open_explorer
- open_terminal
- open_smartlot
- exit
- unknown

Reglas:
- Si el usuario pide abrir un programa, usá type "action".
- Si el usuario pregunta algo o quiere conversar, usá type "chat".
- Si el usuario menciona "Visual Studio Code", "VS Code" o "Code", la acción es "open_vscode".
- Si menciona "terminal", "consola" o "PowerShell", la acción es "open_terminal".
- Si dice "salir", "cerrar", "terminar" o "apagar Jarvis", la acción es "exit".

Texto del usuario:
{text}

Ejemplos válidos:

{{
  "type": "action",
  "action": "open_vscode"
}}

{{
  "type": "chat",
  "response": "Estoy funcionando correctamente. ¿En qué puedo ayudarte?"
}}
"""


    print("Enviando texto a Ollama...")

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    ollama_response = (
        data["response"]
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    print("Respuesta de Ollama:")
    print(ollama_response)
   
    action_data = json.loads(ollama_response)
    return action_data["action"].lower()
    
def hablar(texto):
    engine = pyttsx3.init()
    engine.setProperty("volume", 1.0)
    engine.setProperty("rate", 150)
    engine.say(texto)
    engine.runAndWait()

def procesar_respuesta(respuesta):

    tipo = respuesta.get("type")

    if tipo == "action":
        action = respuesta.get("action", "unknown").lower()
        ejecutar_accion(action)

    elif tipo == "chat":
        mensaje = respuesta.get("response", "No tengo una respuesta.")
        print("Jarvis:")
        print(mensaje)
        hablar(mensaje)

    else:
        print("Respuesta desconocida.")
        hablar("No entendí qué tengo que hacer.")


def ejecutar_accion(action): 

    if action == "open_vscode":
        print("Abriendo Visual Studio Code...")
        hablar("Abriendo Visual Studio Code")
        subprocess.Popen("code", shell=True) 

    elif action == "open_notepad":
        print("Abriendo Notepad...")
        hablar("Abriendo Notepad")
        subprocess.Popen("notepad.exe")

    elif action == "open_calculator":
        print("Abriendo Calculadora...")
        hablar("Abriendo Calculadora")
        subprocess.Popen("calc.exe")

    elif action == "open_chrome":
        print("Abriendo Chrome...")
        hablar("Abriendo Chrome")
        subprocess.Popen(
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )

    elif action == "open_explorer":
        print("Abriendo Explorador...")
        hablar("Abriendo Explorador de archivos")
        subprocess.Popen("explorer.exe")

    elif action == "open_smartlot":
        print("Abriendo SmartLot...")
        hablar("Abriendo SmartLot")
        subprocess.Popen(
            ["code", r"C:\Users\Tobias\Downloads\SmartLot"],
            shell=True
        )
    elif action == "open_terminal":
           print("Abriendo terminal...")
           hablar("Abriendo terminal")
           subprocess.Popen("powershell.exe")
    elif action == "exit":
        print("Apagando Jarvis...")
        hablar("Apagando Jarvis")
        exit()

    else:
        print("Acción desconocida.")
        hablar("No entendí la acción")
print("Cargando Whisper...")
model = whisper.load_model("base")

print("Jarvis iniciado.")

while True:
    try:
        grabar_audio()
        text = transcribir_audio(model)
        respuesta = obtener_respuesta(text)
        procesar_respuesta(respuesta)
    except Exception as e:
        print(f"Error: {e}")


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


def obtener_accion(text):
 


    prompt = f"""
Sos el cerebro de un asistente llamado Jarvis.

Respondé SOLO con JSON válido.

Acciones permitidas:
- open_vscode
- open_notepad
- open_calculator
- open_chrome
- open_explorer
- open_smartlot
- exit
- unknown
Reglas:
- Si el usuario menciona "Visual Studio Code" o "VS Code", la acción es "open_vscode".
- Si el usuario menciona "Notepad" o "Bloc de notas", la acción es "open_notepad".
- Si el usuario menciona "Calculator" o "Calculadora", la acción es "open_calculator".
- Si el usuario menciona "Chrome" o "Google Chrome", la acción es "open_chrome".
- Si el usuario menciona "Explorer" o "Explorador de archivos", la acción es "open_explorer".
- Si el usuario menciona "auto", "estacionamiento" o "SmartLot", la acción es "open_smartlot".
- Si el usuario dice salir, cerrar , terminar o apagar Jarvis, la acción es "exit".:
{{
  "action": "exit"
}}

Texto del usuario:
{text}

Formato:
{{
  "action": "open_vscode"
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
    engine.say(texto)
    engine.runAndWait()          



def ejecutar_accion(action):

    if action == "open_vscode":

        print("Abriendo Visual Studio Code...")
        subprocess.Popen("code", shell=True)

    elif action == "open_notepad":

        print("Abriendo Notepad...")
        subprocess.Popen("notepad.exe")

    elif action == "open_calculator":

        print("Abriendo Calculadora...")
        subprocess.Popen("calc.exe")

    elif action == "open_chrome":

        print("Abriendo Chrome...")
        subprocess.Popen(
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )

    elif action == "open_explorer":

        print("Abriendo Explorador...")
        subprocess.Popen("explorer.exe")

    elif action == "open_smartlot":

        print("Abriendo SmartLot...")
        subprocess.Popen(
            ["code", r"C:\Users\Tobias\Downloads\SmartLot"],
            shell=True
        )

    elif action == "exit":

        print("Apagando Jarvis...")
        exit()

    else:

        print("Acción desconocida.")
    if action == "open_vscode":
        print("Abriendo Visual Studio Code...")
        hablar("Abriendo Visual Studio Code")
    elif action == "open_notepad":
        print("Abriendo Notepad...")
        hablar("Abriendo Notepad")
    elif action == "open_calculator":
        print("Abriendo Calculadora...")
        hablar("Abriendo Calculadora")

print("Cargando Whisper...")
model = whisper.load_model("base")

print("Jarvis iniciado.")

while True:
    try:
        grabar_audio()
        text = transcribir_audio(model)
        action = obtener_accion(text)
        ejecutar_accion(action)
    except Exception as e:
        print(f"Error: {e}")


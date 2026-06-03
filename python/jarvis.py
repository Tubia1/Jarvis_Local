import json
import subprocess
import requests
import whisper
import sounddevice as sd
from scipy.io.wavfile import write

AUDIO_PATH = "../audios/live.wav"
MODEL_NAME = "qwen2.5:1.5b"

duration = 8
sample_rate = 44100

def escuchar_y_grabar():

 print("Grabando... hablá ahora")

audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1
)

sd.wait()

write(AUDIO_PATH, sample_rate, audio)

print("Audio guardado.")
print("Cargando Whisper...")

model = whisper.load_model("base")

print("Transcribiendo audio...")

result = model.transcribe(AUDIO_PATH, language="spanish")
text = result["text"]

print("Texto detectado:")
print(text)

prompt = f"""
Sos el cerebro de un asistente llamado Jarvis.
Tu tarea es convertir la orden del usuario en una acción.

Respondé SOLO con JSON válido.

Acciones permitidas:
- open_vscode
- open_notepad
- open_calculator
- open_chrome
- open_explorer
- open_smartLot 
- unknown

Reglas:
- Si el usuario menciona "Visual Studio Code" o "VS Code", la acción es "open_vscode".
- Si el usuario menciona "Notepad" o "Bloc de notas", la acción es "open_notepad".
- Si el usuario menciona "Calculator" o "Calculadora", la acción es "open_calculator".
- Si el usuario menciona "Chrome" o "Google Chrome", la acción es "open_chrome".
- Si el usuario menciona "Explorer" o "Explorador de archivos", la acción es "open_explorer".
- Si el usuario menciona "auto o estacionamiento", la acción es "open_smartLot".
 Si el usuario dice salir, cerrar o terminar:
{
  "action": "exit"
}
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
ollama_response = data["response"]
ollama_response = ollama_response.replace("```json", "").replace("```", "").strip() # Eliminar los backticks si están presentes

print("Respuesta de Ollama:")
print(ollama_response)


action_data = json.loads(ollama_response)
action = action_data["action"]

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

elif action == "open_smartLot":
    print("Abriendo SmartLot...")
    subprocess.Popen(["code", r"C:\Users\Tobias\Downloads\SmartLot"], shell=True)
elif action == "exit":
    print("apagando Jarvis...")
    exit()
else:
    print("Acción desconocida.")

    while True:
        escuchar_y_grabar()
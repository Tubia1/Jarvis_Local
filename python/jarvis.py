import json
import subprocess
import requests
import whisper
import sounddevice as sd
from scipy.io.wavfile import write

AUDIO_PATH = "../audios/live.wav"
MODEL_NAME = "qwen2.5:1.5b"

duration = 5
sample_rate = 44100

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
- unknown

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

else:
    print("Acción desconocida.")
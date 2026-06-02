import whisper
import requests
import json
import subprocess
print ("Loading  whisper model...")
model = whisper.load_model("base")
print ("Model loaded.")
result = model.transcribe("../audios/vs_code.m4a", language="spanish") 
text = result["text"]
print (text)
prompt = f"""
Sos el cerebro de un asistente llamado Jarvis.

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
print ("Sending text to ollama..")
response = requests.post("http://localhost:11434/api/generate", json={
    "model": "qwen2.5:1.5b",
    "prompt": prompt,
    "stream": False
    
})
data = response.json()  
ollama_response = data["response"]
print ("Respuesta de ollama ")
print (ollama_response)
action_data =json.loads(ollama_response)
action = action_data["action"] 
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
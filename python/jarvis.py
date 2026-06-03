import sounddevice as sd
from scipy.io.wavfile import write

duration = 5  # Duración de la grabación en segundos
sample_rate = 44100 # Frecuencia de muestreo (puedes ajustarla según tus necesidades)

print("Grabando... hablá ahora")
audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1) # Graba audio en mono
sd.wait()

write("../audios/live.wav", sample_rate, audio) # Guarda el audio en un archivo WAV

print("Audio guardado en ../audios/live.wav")
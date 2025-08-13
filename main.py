from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment

# Carregar o vídeo e extrair o áudio
video = VideoFileClip("seu_video.mp4")
video.audio.write_audiofile("audio_temp.wav")

# Converter o áudio para formato WAV e carregar com pydub
audio = AudioSegment.from_file("audio_temp.wav")
audio.export("audio_temp.wav", format="wav")

# Inicializar o reconhecedor de fala
recognizer = sr.Recognizer()

# Dividir o áudio em segmentos de 1 minuto
duration = len(audio) // 1000  # duração em segundos
text_result = []

for i in range(0, duration, 60):  # incrementa de 60 em 60 segundos
    segment = audio[i*1000:(i+60)*1000]
    segment.export("temp_segment.wav", format="wav")
    
    with sr.AudioFile("temp_segment.wav") as source:
        audio_data = recognizer.record(source)
        try:
            # Transcrever o segmento de áudio
            texto = recognizer.recognize_google(audio_data, language="pt-BR")
            text_result.append(texto)
        except sr.UnknownValueError:
            print(f"Não foi possível entender o áudio no segmento {i // 60 + 1}.")
        except sr.RequestError:
            print("Erro ao conectar com o serviço de reconhecimento de fala.")
            break  # interrompe se houver erro de conexão

# Juntar todo o texto extraído
texto_final = " ".join(text_result)

# Salvar o texto extraído em um arquivo .txt
with open("resultado.txt", "w", encoding="utf-8") as arquivo_texto:
    arquivo_texto.write(texto_final)
    #print("Texto extraído do vídeo:", texto_final)

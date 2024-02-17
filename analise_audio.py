import sounddevice as sd
import numpy as np
import librosa
from scipy import signal
import speech_recognition as sr
import wavio
from analise_texto import analisar_texto


def preprocessamento_audio(audio, taxa_amostragem):
    # Filtrar o sinal de áudio para enfatizar a faixa de frequência da voz
    nyquist = taxa_amostragem / 2
    # Projetar um filtro passa-baixa com uma frequência de corte de 4 kHz
    fc = 4000 / nyquist
    b, a = signal.butter(6, fc, 'low')
    audio_filtrado = signal.filtfilt(b, a, audio)
    return audio_filtrado


def analisar_caracteristicas_acusticas(audio, taxa_amostragem=44100):
    # Pré-processar o áudio para focar na voz
    audio_preprocessado = preprocessamento_audio(audio, taxa_amostragem)

    # Calcular o pitch usando a transformada rápida de Fourier (FFT)
    fft_data = np.fft.fft(audio_preprocessado)
    freqs = np.fft.fftfreq(len(fft_data))
    freq_in_hertz = abs(freqs[np.argmax(fft_data)])
    pitch = freq_in_hertz * taxa_amostragem

    # Calcular a entonação (desvio padrão das frequências fundamentais)
    tons_medios, _ = librosa.piptrack(
        y=audio_preprocessado, sr=taxa_amostragem)
    entonacao = np.std(np.diff(np.mean(tons_medios, axis=0)))

    return pitch, entonacao


def extrair_texto_audio(audio):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio_data = recognizer.record(source)
        texto = recognizer.recognize_google(audio_data, language='pt-BR')
    return texto


def calcular_taxa_fala(texto, duracao_audio_segundos):
    # Contar o número de palavras no texto
    num_palavras = len(texto.split())

    # Calcular a taxa de fala em palavras por minuto (WPM)
    taxa_fala_wpm = (num_palavras / duracao_audio_segundos) * 60

    return taxa_fala_wpm


def calcular_tempo_medio_pausas_por_palavra(texto_extraido, duracao_audio_segundos):
    # Dividir o texto em palavras
    palavras = texto_extraido.split()

    # Calcular a duração total do áudio menos a duração do tempo de fala
    duracao_fala_total = duracao_audio_segundos - \
        len(palavras) / calcular_taxa_fala(texto_extraido, duracao_audio_segundos)

    # Calcular o número total de pausas entre as palavras
    num_pausas = len(palavras) - 1

    # Calcular o tempo médio de pausas por palavra
    if num_pausas > 0:
        tempo_medio_pausas_por_palavra = duracao_fala_total / num_pausas
    else:
        tempo_medio_pausas_por_palavra = 0

    return tempo_medio_pausas_por_palavra


def gravar_analisar_audio():
    try:
        # Gravar áudio do microfone
        print("Gravando áudio...")
        audio = sd.rec(int(60 * 44100), samplerate=44100,
                       channels=1, dtype='float64')
        sd.wait()

        # Salvar o áudio gravado em um arquivo WAV
        arquivo_audio = "audio_gravado.wav"
        wavio.write(arquivo_audio, audio, 44100, sampwidth=2)

        # Analisar características acústicas do áudio gravado
        pitch_medio, entonacao = analisar_caracteristicas_acusticas(
            audio.squeeze())
        # Calcular a duração do áudio em segundos
        duracao_audio_segundos = len(audio) / 44100
        # Extrair texto do áudio gravado
        texto_extraido = extrair_texto_audio(arquivo_audio)
        # Calcular a taxa de fala
        taxa_fala_wpm = calcular_taxa_fala(
            texto_extraido, duracao_audio_segundos)
        tempo_medio_pausas_por_palavra = calcular_tempo_medio_pausas_por_palavra(
            texto_extraido, duracao_audio_segundos)
        # Imprimir informações sobre as características acústicas
        print("\nCaracterísticas acústicas do áudio gravado:")
        print("Pitch médio (Hz):", pitch_medio)
        print("Entonação:", entonacao)
        print("Taxa de fala:", taxa_fala_wpm, "em 1 minuto")
        print("Tempo médio de pausas por palavra: {:.2f} segundos".format(
            tempo_medio_pausas_por_palavra))

        print("\nTexto extraído do áudio gravado:")
        print(texto_extraido)
        print('\nAnalise do texto')
        print(analisar_texto(texto_extraido))

    except Exception as e:
        print("Ocorreu um erro:", e)

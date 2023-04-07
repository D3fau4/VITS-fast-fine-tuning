import os
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
raw_audio_dir = "./raw_audio/"

def dividir_audio_carpeta(carpeta_entrada, max_duration):
    """
    Función que recibe una carpeta de entrada y una duración máxima para dividir los archivos
    de audio en trozos de máximo max_duration, evitando cortar cuando alguien está hablando.
    Los trozos de audio resultantes se guardan en la misma carpeta que el archivo de audio original,
    con el mismo nombre pero divididos por el número de fragmento.
    """
    # Obtenemos la lista de archivos de audio en formato WAV en la carpeta de entrada
    archivos_de_audio = [archivo for archivo in os.listdir(carpeta_entrada) if archivo.endswith('.wav')]

    # Procesamos cada archivo de audio de la carpeta de entrada
    for archivo in archivos_de_audio:
        print(f"Procesando archivo: {archivo}")

        # Cargamos el archivo de audio
        audio = AudioSegment.from_wav(os.path.join(carpeta_entrada, archivo))
        print("Audio cargado...")
        # Detectamos los segmentos de audio con sonido
        segmentos_de_sonido = detect_nonsilent(audio, min_silence_len=500, silence_thresh=-50)
        print(f"Segmentos de sonido encontrados")
        # Dividimos el archivo de audio en trozos de máximo max_duration, evitando cortar cuando alguien está hablando
        for i, segmento in enumerate(segmentos_de_sonido):
            inicio = segmento[0]
            fin = segmento[1]
            duracion = fin - inicio
            num_fragmento = i + 1

            # Si la duración del segmento es menor o igual a max_duration, lo guardamos tal cual
            if duracion <= max_duration * 1000:
                trozo_de_audio = audio[inicio:fin]
                trozo_de_audio.export(os.path.join(carpeta_entrada, f"{archivo[:-4]}_{num_fragmento}.wav"),
                                      format="wav")

            # Si la duración del segmento es mayor que max_duration, lo dividimos en trozos de máximo max_duration
            else:
                num_trozos = duracion // (max_duration * 1000) + 1
                for j in range(num_trozos):
                    inicio_trozo = inicio + j * max_duration * 1000
                    fin_trozo = min(inicio_trozo + max_duration * 1000, fin)
                    trozo_de_audio = audio[inicio_trozo:fin_trozo]
                    trozo_de_audio.export(os.path.join(carpeta_entrada, f"{archivo[:-4]}_{num_fragmento}_{j + 1}.wav"),
                                          format="wav")

        print(f"Archivo {archivo} procesado correctamente.")
        os.remove(archivo)

dividir_audio_carpeta(raw_audio_dir, 30 * 60)
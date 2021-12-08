import subprocess
import speech_recognition as sr
import soundfile as sf
import time


def get_v_len(file_path_wav) -> int:
    """
    получить продолжительность аудио в секундах
    :return int v_len - длина видео в секундах
    """
    try:
        with sf.SoundFile(file_path_wav) as f:
            v_len = int(len(f) / f.samplerate)
    except RuntimeError:
        time.sleep(3)
        with sf.SoundFile(file_path_wav) as f:
            v_len = int(len(f) / f.samplerate)
    return v_len


def analyser(file_path, language, wav=False):
    """
    перевести аудио в текст
    :param file_path: путь к аудио файлу
    :param language: язык аудио
    :param wav: является ли файл уже нужного формата
    :return: полный текст аудио
    """
    if not wav:
        subprocess.call(f'ffmpeg/bin/ffmpeg.exe -y -i Resource/{file_path}.mp3 -ac 2 -f wav Resource/{file_path}.wav '
                        f'-loglevel quiet')

    file_path_wav = f'Resource/{file_path}.wav'
    v_len = get_v_len(file_path_wav)

    r = sr.Recognizer()
    full_text = ''
    with sr.AudioFile(file_path_wav) as source:
        chunk_range = range(0, v_len)
        output = [chunk_range[i:i + 60] for i in range(0, len(chunk_range), 60)]

        for _ in output:
            try:
                audio_data = r.record(source, duration=60)
                text = r.recognize_google(audio_data, language=language)
                try:
                    full_text += text
                except Exception:
                    pass
            except Exception as e:
                print(e)

    return full_text


if __name__ == '__main__':
    analyser('Resource/test1', language='UK-ua')

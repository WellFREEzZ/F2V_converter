import os
from pydub import AudioSegment


def wav_to_ogg(orig):
    dest = os.path.splitext(orig)[0] + '.oga'
    song = AudioSegment.from_wav(orig)
    song.export(dest, format="oga")
    return dest


def mp3_to_ogg(orig):
    dest = os.path.splitext(orig)[0] + '.oga'
    song = AudioSegment.from_mp3(orig)
    song.export(dest, format="oga")
    return dest


def b_wf(orig):
    bar_count = 64
    db_ceiling = 255
    sound = AudioSegment.from_ogg(orig)
    chunk_length = len(sound) / bar_count

    loudness_of_chunks = [
        sound[i * chunk_length: (i + 1) * chunk_length].rms
        for i in range(bar_count)]

    max_rms = max(loudness_of_chunks)

    return [int((loudness / max_rms) * db_ceiling)
            for loudness in loudness_of_chunks], int(sound.duration_seconds)


if __name__ == '__main__':
    mp3_to_ogg('C:\\Users\\mrtit\\PythonProjects\\PythonMB\\VoiceConverter\\music.mp3')

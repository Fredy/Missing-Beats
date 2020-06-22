#!/usr/bin/env python3
import argparse
import os
import uuid

import ffmpeg
import youtube_dl

from src.main import remove_beats
from src.spotify import get_tempo


def download_song(url: str, output: str):
    """
    Download song from URL and save it in `output`.wav

    :param url: Youtube song URL.
    :param output: path to output file wihtout extension
    """
    ydl_opts = dict(
        format='bestaudio/best',
        outtmpl=f'{output}.%(ext)s',
        postprocessors=[dict(
            key='FFmpegExtractAudio',
            preferredcodec='wav',
        )]
    )
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def file_to_mp3(file: str, extension='.wav'):
    """
    Converts audio `file` with `extension` into mp3 file with the same name.
    """
    ffmpeg.input(f'{file}{extension}').output(f'{file}.mp3').global_args(
        '-loglevel', 'warning').run()


def main(url: str, track_id: str, output_file: str, output_dir: str):
    temp_file = os.path.join(output_dir, uuid.uuid4().hex)
    download_song(url, temp_file)
    temp_file_wav = f'{temp_file}.wav'

    bpm = get_tempo(track_id)
    file_a, file_b = remove_beats(temp_file_wav, bpm, output_dir, output_file)
    file_to_mp3(os.path.splitext(file_a)[0])
    file_to_mp3(os.path.splitext(file_b)[0])

    os.remove(temp_file_wav)
    os.remove(file_a)
    os.remove(file_b)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remove beats from a song')
    parser.add_argument('url', help='song from youtube')
    parser.add_argument('track_id', help='spotify song track id')
    parser.add_argument('output', help='output files base name')
    parser.add_argument(
        '--output-dir', '-d', help='output directory path', default='./output')

    args = parser.parse_args()
    main(args.url, args.track_id, args.output, args.output_dir)

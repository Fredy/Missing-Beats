import os

import numpy as np
from scipy.io import wavfile


def get_file_name(file):
    """Return the file name without its extension"""
    base = os.path.basename(file)
    return os.path.splitext(base)[0]


def _set_values(input_, output, in_idx, out_idx, leap):
    output[out_idx * leap: (out_idx + 1) * leap] = (
        input_[in_idx * leap: (in_idx + 1) * leap])


def remove_beats(
        file: str, bpm: float, output_dir="./output",
        output_file=None) -> (str, str):
    """
    Deletes beats from a song and save two files one with even beats and other
    with odd beats.
    BPM can be retrieved from Spotify API:
    https://developer.spotify.com/console/get-audio-features-track/

    :param file: Path of the input song, it must be a .wav file.
    :param bpm: Beats per minute of the input song.
    :param output_dir: Path where the outputs will be saved.
    :param output_file: Output file name, the default is the input file name.

    :return: Output files dirs.
    """
    rate, data = wavfile.read(file)
    beat_rate = round(rate / (bpm / 60))  # rate / Beats per second
    first_idx_data = np.nonzero(data)[0][0]

    non_silent_data = data[first_idx_data:]
    non_silent_result_even = np.zeros_like(non_silent_data)
    non_silent_result_odd = np.zeros_like(non_silent_data)
    range_to = non_silent_data.shape[0] // beat_rate

    for i, j in enumerate((range(0, range_to, 2))):
        _set_values(non_silent_data, non_silent_result_even, j, i, beat_rate)
    for i, j in enumerate((range(1, range_to, 2))):
        _set_values(non_silent_data, non_silent_result_odd, j, i, beat_rate)

    result = np.zeros_like(data)
    # first_idx_data is to add some silence at the end
    duration = data.shape[0] // 2 + first_idx_data

    os.makedirs(output_dir, exist_ok=True)
    if output_file is None:
        output_file = get_file_name(file)

    result[first_idx_data:] = non_silent_result_even
    output_file_even = os.path.join(output_dir, f'{output_file}_even.wav')
    wavfile.write(output_file_even, rate, result[:duration])

    result[first_idx_data:] = non_silent_result_odd
    output_file_odd = os.path.join(output_dir, f'{output_file}_odd.wav')
    wavfile.write(output_file_odd, rate, result[:duration])

    return output_file_even, output_file_odd

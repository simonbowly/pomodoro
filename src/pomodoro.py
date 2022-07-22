import contextlib
import functools
import os
import pathlib
import time

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from tqdm import trange
from pygame import mixer


__version__ = "0.1.0"


AUDIO = pathlib.Path(__file__).parent / "audio"
SECONDS_PER_MINUTE = 60


@functools.lru_cache()
def get_sound(name):
    return mixer.Sound(str(AUDIO / f"{name}.wav"))


def timer(name, *, minutes, end_sound, ncols=100):
    desc = f"{name:10s} ({minutes:2d} min)"
    for _ in trange(minutes * SECONDS_PER_MINUTE, desc=desc, ncols=ncols):
        time.sleep(1)
    end_sound.play()


@contextlib.contextmanager
def mixer_active():
    mixer.init()
    try:
        yield
    finally:
        # wait for sounds to finish
        while mixer.get_busy():
            time.sleep(1)
        mixer.quit()


def pomodoro_cycle(work_end_sound="success", break_end_sound="ping"):
    timings = [(25, 5)] * 3 + [(25, 15)]
    for work_time, break_time in timings:
        timer("Work", minutes=work_time, end_sound=get_sound(work_end_sound))
        timer("Break", minutes=break_time, end_sound=get_sound(break_end_sound))


def main():
    with mixer_active():
        pomodoro_cycle()

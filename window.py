from scipy.fft import rfft
import numpy as np
import tkinter as tk


class AudioBufferWithLog:
    _MX_LOG_SIZE = 10000

    def __init__(self, buffer_size: int):
        self.buffer_size = buffer_size
        self.buffer = np.ndarray((0,))
        self.sm_log = list()
        self.avg_log = list()

    def append(self, fresh):
        self.buffer = np.append(self.buffer, fresh)
        if self.buffer.size > self.buffer_size:
            self.buffer = self.buffer[-self.buffer_size:]

    def new_snapshot(self, data: np.ndarray) -> list:
        self.append(data.flatten())
        dfft = np.abs(rfft(self.buffer))
        if len(self.sm_log) < AudioBufferWithLog._MX_LOG_SIZE:
            self.sm_log.append(np.sum(dfft))
            self.avg_log.append(np.dot(dfft, np.arange(0, dfft.size)) / self.sm_log[-1])
        return [a for b, c in enumerate(dfft[:64]) for a in [b * 16, c]]


class WindowGraphFft(tk.Frame):

    DEF_COLS = ["blue", "red"]

    def __init__(self, logs: list[AudioBufferWithLog], master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.pic = tk.Canvas(self, width=1024, height=512)
        self.pic.pack()
        self.logs = list(logs)

    def audio_input_callback(self, indata: np.ndarray, _1, _2, _3) -> None:
        self.pic.delete('all')
        for idx, log in enumerate(self.logs):
            self.pic.create_line(log.new_snapshot(indata), fill=WindowGraphFft.DEF_COLS[idx])

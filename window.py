from scipy.fft import fft
import numpy as np
import tkinter as tk

BLOCK_SIZE = 256


class WindowMxVal(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.mxval = 0.0
        self.mxvalL = tk.Label(self, text="awaiting audio")
        self.mxvalL.pack()

    def audio_input_callback(self, indata: np.ndarray, _1, _2, _3) -> None:
        idfft = fft(indata.flatten())
        self.mxval = max(self.mxval, np.max(np.abs(idfft)))
        self.mxvalL['text'] = str(self.mxval)


class AudioBufferWithLog:
    _MX_LOG_SIZE = 10000

    def __init__(self, buffer_size: int):
        self.buffer_size = buffer_size
        self.buffer = np.ndarray((0,))
        self.log = list()

    def append(self, fresh):
        self.buffer = np.append(self.buffer, fresh)
        if self.buffer.shape[0] > self.buffer_size:
            self.buffer = self.buffer[-self.buffer_size:]

    def new_snapshot(self, data: np.ndarray) -> list:
        self.append(data)
        dfft = np.abs(fft(self.buffer)[:64])
        if len(self.log) < self._MX_LOG_SIZE:
            self.log.append(np.max(dfft))
        return [a for b, c in enumerate(dfft) for a in [b * 16, c]]


class WindowGraphFft(tk.Frame):

    def __init__(self, logs: list[AudioBufferWithLog], master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.pics = [(tk.Canvas(self, width=1024, height=512), log) for log in logs]
        for can, _ in self.pics:
            can.pack()

    def audio_input_callback(self, indata: np.ndarray, _1, _2, _3) -> None:
        for pic, log in self.pics:
            pic.delete('all')
            pic.create_line(log.new_snapshot(indata))

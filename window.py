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

    def get_audio_input_callback(self):
        def callback(indata: np.ndarray, _1,
                     _2, _3) -> None:
            idfft = fft(indata.flatten())
            self.mxval = max(self.mxval, np.max(np.abs(idfft)))
            self.mxvalL['text'] = str(self.mxval)
        return callback


class WindowGraphFft(tk.Frame):
    _BUFFER_SIZE = 4096

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.pic = tk.Canvas(self, width=1024, height=512)
        self.pic.pack()
        self.buffer = np.ndarray((0,))

    def _append_to_buffer(self, fresh):
        self.buffer = np.append(self.buffer, fresh)
        if self.buffer.shape[0] > self._BUFFER_SIZE:
            self.buffer = self.buffer[-self._BUFFER_SIZE:]

    def get_audio_input_callback(self):
        def callback(indata: np.ndarray, _1, _2, _3) -> None:
            self._append_to_buffer(indata)
            idfft = (abs(fft(self.buffer)))[:64]
            pic = self.pic
            pic.delete("all")
            pic.create_line(*[a for b, c in enumerate(idfft) for a in [b * 16, c]])
        return callback

from window import WindowGraphFft as Window, BLOCK_SIZE, AudioBufferWithLog as Log
import tkinter as tk
import sounddevice as sd
import matplotlib.pyplot as mp

SAMPLE_RATE = 44100

a = Log(4096)
b = Log(4096 * 2)

root = tk.Tk()
window = Window([a, b], master=root)

stream = sd.InputStream(
    samplerate=SAMPLE_RATE,
    blocksize=BLOCK_SIZE,
    callback=window.audio_input_callback,
    channels=1
)
stream.start()
window.mainloop()
stream.stop()
mp.plot(a.log)
mp.plot(b.log)
mp.show()
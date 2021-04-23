from window import WindowGraphFft as Window, AudioBufferWithLog as Log
import tkinter as tk
import sounddevice as sd
import matplotlib.pyplot as mp
import numpy as np

BLOCK_SIZE = 256
SAMPLE_RATE = 44100

a = Log(2048)
b = Log(4096)

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
fig, (sp, ap) = mp.subplots(2)

sp.set_title('magnitude')
sp.plot(a.sm_log)
sp.plot([t for t in b.sm_log])

ap.set_title('freq')
ap.plot(a.avg_log)
ap.plot([t for t in b.avg_log])

sp.label_outer()
ap.label_outer()

mp.show()
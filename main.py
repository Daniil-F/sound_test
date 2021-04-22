from window import WindowGraphFft as Window, BLOCK_SIZE
import tkinter as tk
import sounddevice as sd

SAMPLE_RATE = 44100

root = tk.Tk()
window = Window(master=root)

stream = sd.InputStream(
    samplerate=SAMPLE_RATE,
    blocksize=BLOCK_SIZE,
    callback=window.get_audio_input_callback(),
    channels=1
)
stream.start()
window.mainloop()
stream.stop()
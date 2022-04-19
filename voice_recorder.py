import sounddevice as sd
from tkinter import *
import queue
import soundfile as sf
import threading
from tkinter import messagebox
from scipy import arange
from scipy.fft import fft
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os

# Define the user interface
voice_rec = Tk()
voice_rec.geometry("360x200")
voice_rec.title("voice recorder")
voice_rec.config(bg="#107dc2")

# Create a queue to contain the audio data
q = queue.Queue()
# Declare variables and initialise them
recording = False
file_exists = False


# Fit data into queue
def callback(indata, frames, time, status):
    q.put(indata.copy())






# Functions to play, stop and record audio
# The recording is done as a thread to prevent it being the main process
def threading_rec(x):
    if x == 1:
        # If recording is selected, then the thread is activated
        t1 = threading.Thread(target=record_audio)
        t1.start()
    elif x == 2:
        # To stop, set the flag to false
        global recording
        recording = False
        messagebox.showinfo(message="Recording finished")
    elif x == 3:
        # To play a recording, it must exist.
        if file_exists:
            # Read the recording if it exists and play it
            data, fs = sf.read("trial.wav", dtype='float32')
            sd.play(data, fs)
            sd.wait()
        else:
            # Display and error if none is found
            messagebox.showerror(message="Record something to play")
    elif x == 4:
        def frequency_spectrum(x, sf):
            """
            Derive frequency spectrum of a signal from time domain
            :param x: signal in the time domain
            :param sf: sampling frequency
            :returns frequencies and their content distribution
            """
            x = x - np.average(x)  # zero-centering

            n = len(x)
            k = arange(n)
            tarr = n / float(sf)
            frqarr = k / float(tarr)  # two sides frequency range

            frqarr = frqarr[range(n // 2)]  # one side frequency range

            x = fft(x) / n  # fft computing and normalization
            x = x[range(n // 2)]

            return frqarr, abs(x)

        # Sine sample with a frequency of 1hz and add some noise
        sr = 32  # sampling rate
        y = np.linspace(0, 2 * np.pi, sr)
        y = np.tile(np.sin(y), 5)
        y += np.random.normal(0, 1, y.shape)
        t = np.arange(len(y)) / float(sr)

        plt.subplot(2, 1, 1)
        plt.plot(t, y)
        plt.xlabel('t')
        plt.ylabel('y')

        frq, X = frequency_spectrum(y, sr)

        plt.subplot(2, 1, 2)
        plt.plot(frq, X, 'b')
        plt.xlabel('Freq (Hz)')
        plt.ylabel('|X(freq)|')
        plt.tight_layout()

        # wav sample from https://freewavesamples.com/files/Alesis-Sanctuary-QCard-Crickets.wav
        here_path = os.path.dirname(os.path.realpath(__file__))
        wav_file_name = 'trial.wav'
        wave_file_path = os.path.join(here_path, wav_file_name)
        sr, signal = wavfile.read(wave_file_path)

        y = signal[:, 0]  # use the first channel (or take their average, alternatively)
        t = np.arange(len(y)) / float(sr)

        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(t, y)
        plt.xlabel('t')
        plt.ylabel('y')

        frq, X = frequency_spectrum(y, sr)

        plt.subplot(2, 1, 2)
        plt.plot(frq, X, 'b')
        plt.xlabel('Freq (Hz)')
        plt.ylabel('|X(freq)|')
        plt.tight_layout()
        plt.show()


# Recording function
def record_audio():
    # Declare global variables
    global recording
    # Set to True to record
    recording = True
    global file_exists
    # Create a file to save the audio
    messagebox.showinfo(message="Recording Audio. Speak into the mic")
    with sf.SoundFile("trial.wav", mode='w', samplerate=44100,
                      channels=2) as file:
        # Create an input stream to record audio without a preset time
        with sd.InputStream(samplerate=44100, channels=2, callback=callback):
            while recording == True:
                # Set the variable to True to allow playing the audio later
                file_exists = True
                # write into file
                file.write(q.get())


# Label to display app title
title_lbl = Label(voice_rec, text="voice recorder", bg="#107dc2").grid(row=0, column=0, columnspan=3)

# Button to record audio
record_btn = Button(voice_rec, text="Record Audio", command=lambda m=1: threading_rec(m))
# Stop button
stop_btn = Button(voice_rec, text="Stop Recording", command=lambda m=2: threading_rec(m))
# Play button
play_btn = Button(voice_rec, text="Play Recording", command=lambda m=3: threading_rec(m))
# show frequency
show_freq = Button(voice_rec, text="Show frequency", command=lambda m=4: threading_rec(m))

# Position buttons
record_btn.grid(row=1, column=1)
stop_btn.grid(row=1, column=0)
play_btn.grid(row=1, column=2)
show_freq.grid(row=3,column=1)
voice_rec.mainloop()


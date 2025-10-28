import sounddevice as sd
import numpy as np
from scipy.signal import find_peaks
from pydub import AudioSegment
from io import BytesIO

DURATION = 5
SAMPLE_RATE = 44100

def record_audio(duration=DURATION, samplerate=SAMPLE_RATE):
    print(f"Recording {duration} seconds of ambient sound...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    print("Recording complete.\n")
    return np.squeeze(recording)

def analyze_audio(data, samplerate=SAMPLE_RATE):
    rms = np.sqrt(np.mean(np.square(data)))
    loudness = 20 * np.log10(rms + 1e-6)
    peaks, _ = find_peaks(np.abs(data), height=0.05, distance=samplerate/20)
    rhythm_score = len(peaks) / DURATION
    return loudness, rhythm_score

def classify_mood(loudness, rhythm_score):
    if loudness < -40:
        return "library at midnight"
    elif loudness > -15 and rhythm_score > 30:
        return "storm of chaos"
    else:
        return "toaster orchestra"

def main():
    audio_data = record_audio()
    loudness, rhythm = analyze_audio(audio_data)
    mood = classify_mood(loudness, rhythm)
    print(f"Loudness: {loudness:.2f} dB")
    print(f"Rhythm score: {rhythm:.2f}")
    print(f"Your environment sounds like: {mood}")

if __name__ == "__main__":
    main()

import time
import whisper

# model = whisper.load_model("base")
# model = whisper.load_model("medium")
model = whisper.load_model("large-v2")

time_start = time.time()
result = model.transcribe("audio.mp3")
print(result["text"])
print(str(time.time()-time_start))

exit(0)

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("audio.mp3")
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio).to(model.device)
time_start = time.time()
# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions()
result = whisper.decode(model, mel, options)

# print the recognized text
print(result.text)
print(str(time.time()-time_start))
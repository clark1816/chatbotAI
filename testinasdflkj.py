import whisper

model = whisper.load_model("base")
out = model.transcribe('myvoice.mp3', language= 'en')
print(out['text'])

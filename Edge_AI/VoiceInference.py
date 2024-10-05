
import os
import time
import threading
from datetime import datetime
import shutil

# Audio Recording
from pydub import AudioSegment
import pyaudio
import wave
from VideoStream import firebase_update
from transformers import pipeline

import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db

classifier = pipeline("audio-classification", model="model")

# firebase_cred = credentials.Certificate("owens-and-minor-inventory-firebase.json")
# firebase_admin.initialize_app(firebase_cred,{
#     'databaseURL': 'https://owens-and-minor-inventory-default-rtdb.asia-southeast1.firebasedatabase.app'
# })

# ref = db.reference('Product_Onboarding/Voice_keyword')


# Set the parameters for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 0.5 # Set the recording duration for each chunk
FILE_NAME_PREFIX = "all_audios/audio_chunk"


def get_extra_audio(audio):
    """
    Takes an audio file, extracts the integer part of the filename, loads the previous and current audio files,
    concatenates specific parts of these audio files, exports the final audio file, and starts a new thread to perform inference on the final audio file.
    """
    
    audio_int = int(audio.lstrip("all_audios/audio_chunk_").rstrip(".wav"))

    if os.path.exists(f"all_audios/audio_chunk_{audio_int - 1}.wav"):
        print('Get Extra Audio............. for audio int',audio_int)
        audio_prev = f"all_audios/audio_chunk_{audio_int - 1}.wav"
        audio_next = audio

        audio_prev = AudioSegment.from_file(audio_prev, format="wav")
        audio_next = AudioSegment.from_file(audio_next, format="wav")

        audio_final = audio_prev[500:] + audio_next[:500]

        filename = f'all_audios/audio_chunk_{audio_int - 1}.5.wav'

        audio_final.export(filename, format="wav")

        t4 = threading.Thread(target=do_infer, args=(filename,))
        t4.start()


def do_infer(audio):
    global classifier
    # global ref

    labs = classifier(audio)

    if labs[0]["score"] > 0.9 and labs[0]['label'] != "unknown":
        
        prediction = labs[0]['label'].upper()
        confidence = int(labs[0]['score'] * 100)
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
        print(f"GB_ prediction :- {prediction} \n confidence :-{confidence}% \n timestamp :- {timestamp}\n",
              f"HB_{audio}")
        print(f'######### PREDICTION : {prediction} ########')
        firebase_update({"status": str(prediction),
                         "client_id": "temp"},"voice_status" )


class AudioRecorder:
    def __init__(self):
        os.makedirs('all_audios', exist_ok=True)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      input=True,
                                      frames_per_buffer=CHUNK)
        self.is_recording = True
        self.record_thread = threading.Thread(target=self.record_audio)
        self.record_thread.start()
        
        self.deletion_thread = threading.Thread(target=self.delete_files_periodically, args=('all_audios', 20))
        self.deletion_thread.start()

    def record_audio(self):
        frames = []
        while self.is_recording:
            data = self.stream.read(CHUNK)
            frames.append(data)

            # Save the audio data every second
            if len(frames) >= int(RATE / CHUNK * RECORD_SECONDS):
                self.save_audio(frames)
                frames = []

    def save_audio(self, frames):
        print('SAVING AUDIO@@@@@@@')
        file_name = f"{FILE_NAME_PREFIX}_{int(time.time())}.wav"
        wave_file = wave.open(file_name, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(self.audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()

        # threading.Thread(target=get_extra_audio, args=(file_name,)).start()

        t1 = threading.Thread(target=do_infer, args=(file_name,))
        t1.start()

    def stop_recording(self):
        self.is_recording = False
        self.record_thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.delete_files_periodically.join()
        shutil.rmtree('all_audios')

    
    def delete_files_periodically(self,folder_path, interval):
        while True:
            files = os.listdir(folder_path)
            if len(files) >= 1:
                files_to_delete = files[:2]
                for file_name in files_to_delete:
                    file_path = os.path.join(folder_path, file_name)
                    os.remove(file_path)
                print(f"Deleted {len(files_to_delete)} file(s) from {folder_path}")
            else:
                print("Folder is empty or has less than 2 files. Nothing to delete.")

            time.sleep(interval)



if __name__ == '__main__':
    try:
        
        audio_recorder = AudioRecorder()
        print('Recording Started.......')
        
        while True:
            audio_recorder.record_audio()

    except KeyboardInterrupt:
        
        audio_recorder.stop_recording()
        print("\nRecording stopped......")
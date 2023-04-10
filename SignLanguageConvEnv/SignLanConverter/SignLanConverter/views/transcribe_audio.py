from io import BytesIO
import json
import math
import time
import speech_recognition as sr
import os
from pydub import AudioSegment
from rest_framework.response import Response
import psutil
from ..status_codes import Status_code

def transcribe_audio_chunk(audio_chunk,used_language):
    # Create a new Speech Recognizer object
    r = sr.Recognizer()
    # Create an AudioFile object for the given audio chunk
    audio = sr.AudioFile(audio_chunk)
    # Use the recognizer object to record the audio from the file
    with audio as source:
        audio_file = r.record(source)
    try:
        # Use the recognizer object to transcribe the recorded audio
        # using the Google Speech Recognition service with the given language code
        # and return the transcribed text and the confidence level  
        text = r.recognize_google(audio_file,language=used_language,with_confidence=True)
        return text[0],text[1]
    except sr.UnknownValueError:
        # If the Speech Recognition service could not understand the audio, print an error message and return an empty string and confidence level 0
        print("Error: Speech Recognition could not understand audio")
        return "",0
    except sr.RequestError as e:
        #If there was an error while requesting results from the Speech Recognition service, print an error message and return an empty string and confidence level 2   
        print(f"Error: Could not request results from Speech Recognition service; {str(e)}")
        return "",2
    
def transcribe_audio(audio_file,used_language):
    start_transcribe_time = time.time()
    confidence=[] #array to store confidence of transcribting every chunk aka accuracy
    chunk_size = 11 # seconds
    output_file = r"media\\transcribed_text.txt"
    
    audio_duration=0
    
    with open(output_file, "w") as f:
        while True:
            chunk = audio_file.read(math.floor(chunk_size * 44100))
            
            if not chunk:
                break   
            chunk_name = os.path.splitext(audio_file.name)[0] + "_" + str(int(audio_file.tell() / (chunk_size * 44100)) + 1)
            if os.path.exists(chunk_name):
                os.remove(chunk_name)
            with open(chunk_name, "wb") as chunk_file:
                chunk_file.write(chunk)
            try:
                audio_segment = AudioSegment.from_file(chunk_name, format=os.path.splitext(audio_file.name)[1][1:],frame_rate=44100)
                #get the total duration of chunks to get the duration of the original audio
                audio_duration+=audio_segment.duration_seconds
                # print("chunk_duration_seconds", len(chunk) / audio_segment.frame_rate)
            except Exception as e:
                print(f"Error: {str(e)}")
                os.remove(chunk_name)
                continue
            compatible_file = os.path.join(r"media\\wav_files",os.path.splitext(chunk_name)[0] + ".wav")
            audio_segment.export(compatible_file, format="wav")
            transcribed_text,chunk_confidence = transcribe_audio_chunk(compatible_file,used_language)
            
            #The value 0 is returned by Speech Recognition when the audio is unintelligible or contains no spoken words 
            # in the given chunk. On the other hand, the value 2 is returned when the Speech Recognition service cannot
            # provide results in response to a request.
            if chunk_confidence not in [0, 2]:  
                confidence.append(chunk_confidence)
            elif chunk_confidence == 2:
                transcribed_text="Speech Recognition service error"
                audio_duration=0
                return transcribed_text, audio_duration
                
            f.write(transcribed_text + "\n")
            os.remove(chunk_name)
            os.remove(compatible_file)
    with open(output_file, "r") as f:
        transcribed_text = f.read()
    os.remove(output_file)
    
    #calculate time and memory used
    end_transcribe_time = time.time()
    total_transcribe_time = end_transcribe_time - start_transcribe_time
    
    print(f"Total transcribe time: {total_transcribe_time:.2f} seconds")
    print(f"transcribe accuracy: {(sum(confidence)/len(confidence))if len(confidence)!=0 else 1 *100} %") 
    print(f"number of chunks: {len(confidence)} ") 
    
    print("TEXT ",transcribed_text)
    
    return transcribed_text,audio_duration

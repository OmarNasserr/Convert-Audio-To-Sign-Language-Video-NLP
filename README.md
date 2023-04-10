# Convert-Audio-To-Sign-Language-Video-NLP
-a django python tool that translates audio files to sign language video through and endpoint request
-this tool uses google speech-to-text to convert audio files to text
-ffmpeg is used to convert audio chunks to accepted audio format by google speech-to-text
-nltk then used to tokenize the transcribted text and remove stop words
-moviepy then used to concatenate the corresponding videos to the tokens and if there's no corresponding word, then the token is displayed letter by letter
-the POST request require two fields "language" and "audio_file" 
-the endpoint is "{{uri}}/convert_audio_to_SL/"

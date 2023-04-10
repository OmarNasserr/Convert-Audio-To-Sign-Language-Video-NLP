import json
import random
import uuid
from django.http import HttpResponse, StreamingHttpResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from ..validations import AudioToTextValidations
from .tokenize_text import tokenize_text
from .animation_generator import convert_tokens_to_mp4
from ..status_codes import Status_code
from rest_framework.response import Response
import os
from .transcribe_audio import transcribe_audio
import time
import psutil


@csrf_exempt
@api_view(['POST'])
def convert_audio_to_SL(request):
    start_process_time = time.time()
    validation = AudioToTextValidations.audio_validation(request)
    if validation.status_code != 200:
        return validation

    audio_file = request.FILES['audio_file']
    used_language = request.POST.get('language')

    transcribed_text, audio_duration = transcribe_audio(
        audio_file, used_language)
    if transcribed_text == "Speech Recognition service error":
        return Response(data={'message': 'There was a failure in retrieving results for a text chunk from the Speech Recognition service. Please resend the request to ensure that no results are missed.',
                              'status': Status_code.service_unavailable,
                              },
                        status=Status_code.service_unavailable)

    elif len(transcribed_text) == 0:
        return Response(data={'message': 'It appears that there is no transcribed text available from the audio file. Kindly verify the file to ensure it is valid.',
                              'status': str(Status_code.bad_request),
                              },
                        status=Status_code.bad_request)

    try:
        tokens = tokenize_text(transcribed_text)
    except:
        return Response(data={'message': 'An issue occurred while attempting to tokenize the transcribed text.',
                              'status': Status_code.internal_server_err,
                              },
                        status=Status_code.internal_server_err)

    try:
        video_url = convert_tokens_to_mp4(
            request, tokens, os.path.splitext(audio_file.name)[0], audio_duration)
    except:
        return Response(data={'message': 'There was a problem during the conversion process of the transcribed text to MP4 format.',
                              'status': Status_code.internal_server_err,
                              },
                        status=Status_code.internal_server_err)

    end_process_time = time.time()
    process_at_the_end = psutil.Process(os.getpid())
    total_process_time = end_process_time - start_process_time
    total_memory_usage = process_at_the_end.memory_info().rss
    print(f"Total process time: {total_process_time:.2f} seconds")
    print(
        f"Total process memory usage: {total_memory_usage / 1024 / 1024:.2f} MB")

    return Response(data={'message': 'The conversion of the audio file to sign language video was successful.',
                          'status': Status_code.created,
                          'video_url': video_url
                          },
                    status=Status_code.created)


#########################################################################################
# this function does the same thing as the above function but the difference is that it returns 
# StreamingHttpResponse so it returns progress percentage as the function is running and returns
# the converted video when the function is over
#########################################################################################

# @csrf_exempt
# @api_view(['POST'])
# def convert_audio_to_SL(request):
#     start_process_time = time.time()
#     def generate():
#         yield {"message": "starting audio conversion...", "conversion_progress": 0}

#         validation = AudioToTextValidations.audio_validation(request)
#         if validation.status_code != 200:
#             yield validation
#             return

#         audio_file = request.FILES['audio_file']
#         used_language = request.POST.get('language')
#         yield {"message": "in progress...", "conversion_progress": {random.randint(1, 10)}}

#         transcribed_text, audio_duration = transcribe_audio(
#             audio_file, used_language)
#         yield {"message": "in progress...", "conversion_progress": {random.randint(11, 20)}}

#         if transcribed_text == "Speech Recognition service error":
#             yield Response(data={'message': 'There was a failure in retrieving results for a text chunk from the Speech Recognition service. Please resend the request to ensure that no results are missed.',
#                                 'status': Status_code.service_unavailable,
#                                 },
#                             status=Status_code.service_unavailable)
#             return

#         elif len(transcribed_text) == 0:
#             yield Response(data={'message': 'It appears that there is no transcribed text available from the audio file. Kindly verify the file to ensure it is valid.',
#                                 'status': str(Status_code.bad_request),
#                                 },
#                             status=Status_code.bad_request)
#             return

#         try:
#             tokens = tokenize_text(transcribed_text)
#             yield {"message": "in progress...", "conversion_progress": {random.randint(21, 40)}}
#         except:
#             yield Response(data={'message': 'An issue occurred while attempting to tokenize the transcribed text.',
#                                 'status': Status_code.internal_server_err,
#                                 },
#                             status=Status_code.internal_server_err)
#             return
#         yield {"message": "in progress...", "conversion_progress": {random.randint(41, 50)}}
#         try:
#             video_url = convert_tokens_to_mp4(
#                 request, tokens, os.path.splitext(audio_file.name)[0], audio_duration)
#             yield {"message": "in progress...", "conversion_progress": {random.randint(51, 90)}}
#         except:
#             yield Response(data={'message': 'There was a problem during the conversion process of the transcribed text to MP4 format.',
#                                 'status': Status_code.internal_server_err,
#                                 },
#                             status=Status_code.internal_server_err)
#             return

#         end_process_time = time.time()
#         process_at_the_end = psutil.Process(os.getpid())
#         total_process_time = end_process_time - start_process_time
#         total_memory_usage = process_at_the_end.memory_info().rss
#         print(f"Total process time: {total_process_time:.2f} seconds")
#         print(
#             f"Total process memory usage: {total_memory_usage / 1024 / 1024:.2f} MB")

#         yield {"message": "Audio conversion complete...", "conversion_progress": 100}

#         yield {"message": "'The conversion of the audio file to sign language video was successful.",
#                'status': Status_code.created,
#                'video_url': video_url
#                }

#     return StreamingHttpResponse(generate(), content_type="application/json")

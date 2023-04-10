import os
from rest_framework.response import Response
import re
from SignLanConverter.status_codes import Status_code


class AudioToTextValidations():
    
    
    
    def audio_validation(request):
    
        language_regex='^[a-z]{2}-[A-Z]{2}$'
        
        if 'language' not in request.data:
            request.data._mutable=True
            request.data['language'] = 'en-US'
        
        if 'audio_file' not in request.data:
            return Response(data={
                'message':'The audio_file field is mandatory and cannot be left empty. Please upload an audio file to proceed with the form submission.','status':Status_code.bad_request
            },status=Status_code.bad_request)
            
        elif os.path.splitext(request.FILES['audio_file'].name)[1] != '.mp3':
            return Response(data={
                'message':'The audio file format must be in mp3 format.','status':Status_code.unsupported_media_type
            },status=Status_code.unsupported_media_type)
        
        elif not re.match(language_regex,request.data['language']) or request.data['language'] not in ['en-US', 'ar-EG']:
            return Response(data={
                'message':'The supported languages are limited to English and Arabic, and only the language codes en-US and ar-EG are currently accepted.',
                'status':Status_code.bad_request
            },status=Status_code.bad_request)
            
        else:
            return Response(status=Status_code.success)
            
       
        
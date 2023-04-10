from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib import admin
from django.urls import include, path, re_path
from .views.transcribe_audio import transcribe_audio    
from .views.tokenize_text import tokenize_text    
from .views.convert_audio_to_SL import convert_audio_to_SL

urlpatterns = [
    path("admin/", admin.site.urls),
    path('convert_audio_to_SL/',convert_audio_to_SL,name='convert_audio_to_SL'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# URL pattern for serving individual video files
urlpatterns += [
    re_path(r'^media/sign_language_videos/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]   


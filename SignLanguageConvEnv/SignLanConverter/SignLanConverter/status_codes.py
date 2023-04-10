from rest_framework import status
class Status_code():
    success=status.HTTP_200_OK
    created=status.HTTP_201_CREATED
    no_content=status.HTTP_204_NO_CONTENT
    internal_server_err=status.HTTP_500_INTERNAL_SERVER_ERROR
    service_unavailable=status.HTTP_503_SERVICE_UNAVAILABLE
    version_err=status.HTTP_306_RESERVED
    bad_request=status.HTTP_400_BAD_REQUEST
    unsupported_media_type=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
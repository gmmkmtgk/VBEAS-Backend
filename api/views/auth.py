from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as googleIdToken

# Register your models here.
@api_view(['POST'])
def authenticate(request):
    try:
        id_token = request.data["id_token"]
    except KeyError:
        return Response({"error": "No id_token provided"}, status=status.HTTP_403_FORBIDDEN)
    
    id_info = googleIdToken.verify_oauth2_token(
        id_token, google_requests.Request())
    if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
        return Response(
            {"error": "Not a valid Google account"}, status=status.HTTP_403_FORBIDDEN
        )    
    email = id_info["email"]
    try:
        first_name = id_info["given_name"]
        last_name = id_info["family_name"]
    except Exception as e:
        return Response({
            'message': e
        })
    
    username, domain = email.split('@')

    if domain != "lnmiit.ac.in":
        return Response(
            {"error": "Can only be accessed by Bits Mail"}, status=status.HTTP_403_FORBIDDEN
        )
    key = "thissisomeveryveryimportantkeywhichcannotbesharedanywheremindthisthingplease"
    encoded = jwt.encode({"some": "payload"}, key, algorithm="HS256")
    print(encoded)

    decoded = jwt.decode(encoded, key, algorithms="HS256")
    print(encoded)



from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .email_po import send_po_email, send_po_cancelled_email
from email_config import send_po
import datetime
import traceback


# Create your views here.
class EmailPO(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request,):
        try:
            if send_po:
                if send_po_email():
                    return Response("SUCCESS", status=status.HTTP_200_OK)
            else:
                if send_po_cancelled_email():
                    return Response("SUCCESS", status=status.HTTP_200_OK)
            return Response("FAILED TO SEND", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                str(datetime.datetime.now()) + ': ' + str(e) + '\n' + traceback.format_exc(),
                status=status.HTTP_400_BAD_REQUEST
            )

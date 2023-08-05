import requests
import logging
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response

from remo_app.remo.use_cases import is_remo_local

logger = logging.getLogger('remo_app')


class ValidateTrial(viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        valid = True
        if is_remo_local():
            try:
                resp = requests.post('https://app.remo.ai/api/v1/ui/validate-uuid/1/trial/',
                                     json={'uuid': settings.REMO_UUID}).json()
                valid = resp.get('valid', False)
            except Exception:
                pass

        return Response({'valid': valid}, status=status.HTTP_200_OK)

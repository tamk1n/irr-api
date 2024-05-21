import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

logger = logging.getLogger('django')


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    # Check if it's a validation error
    if isinstance(exc, ValidationError):
        logger.warning(f"Bad request to {context['request'].path}: {response.data}")
    return response

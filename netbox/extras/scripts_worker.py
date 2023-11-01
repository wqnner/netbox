import logging

import requests
from django.conf import settings
from django_rq import job
from jinja2.exceptions import TemplateError

from .conditions import ConditionSet
from .constants import WEBHOOK_EVENT_TYPES
from .webhooks import generate_signature

logger = logging.getLogger('netbox.webhooks_worker')


def process_script(webhook, model_name, event, data, timestamp, username, request_id=None):
    """
    Make a POST request to the defined Webhook
    """

    pass

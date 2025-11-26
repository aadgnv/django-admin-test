import os
import django
from django.test import Client


def before_all(context):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testproject.settings')
    django.setup()


def before_scenario(context, scenario):
    context.client = Client()
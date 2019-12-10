"""Module to import AppConfig from django and define our app"""
from django.apps import AppConfig


class SubletConfig(AppConfig):
    """Class to represent our app"""
    name = 'sublet'

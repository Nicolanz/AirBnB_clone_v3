#!/usr/bin/python3
"""Module to define the Blueprint"""
from flask import Blueprint
app_views = Blueprint('app_view', __name__)
from api.v1.views.index import *
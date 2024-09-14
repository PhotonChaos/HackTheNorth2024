#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from test import app

CGIHandler().run(app)
#!/bin/bash
gunicorn --config gunicorn_config.py wsgi:app 

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.sites.shortcuts import get_current_site
from urllib import request
from urllib import parse
import random
import urllib
from django.contrib import messages
from django.db import connection
from json import dumps
from typing import ContextManager
import time
import datetime
from datetime import datetime as dt
from django.http import Http404, HttpResponseNotFound
from django.core.mail import message, send_mail
from pathlib import Path
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import re
import os
import pytz

def index(request):
    return render(request, 'index.html')

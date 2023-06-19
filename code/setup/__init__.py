# library imports
import tkinter as tk
import customtkinter as ctk
import os
import sys
import time
import schedule
import webbrowser
from datetime import date
from CTkMessagebox import CTkMessagebox
from plyer import notification
from datetime import datetime
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

# folder imports
from utils import *
from api import *
from health import *
from medicine import *

# setup file imports
from setup.special import Settings, InformationPages
from setup.setup_questions import Questions
from setup.setup import setup_logging, get_information_texts

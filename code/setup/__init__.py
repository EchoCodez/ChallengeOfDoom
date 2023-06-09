# library imports
from datetime import datetime, timedelta, date
from plyer import notification
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from CTkMessagebox import CTkMessagebox
import tkinter as tk
import customtkinter as ctk
import re
import sys, os
import webbrowser
import time, schedule

# folder imports
from utils import *
from api import *
from health import *
from medicine import *

# setup file imports
from setup.special import Settings, InformationPages
from setup.setup_questions import Questions
from setup.setup import setup_logging, get_information_texts

# library imports
import tkinter as tk
import customtkinter as ctk
import sys
import webbrowser
from datetime import date

# file imports
from utils.parse_json import jsonUtils
from CTkMessagebox import CTkMessagebox
from setup.setup import setup_logging
from utils.mcq import MCQbuiler
from utils.data_classes import Question, CustomQuestion
from api.diagnosis import Diagnosis
from log_processes.health_log import SearchForLog, get_previous_month
from utils.config import set_theme, delete_old_diagnosis
from setup.setup_questions import Questions
from log.health_log import Log
from setup.ctkcalender import CTkCalender
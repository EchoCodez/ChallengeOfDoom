# library imports
import tkinter as tk
import customtkinter as ctk
import sys
import webbrowser
from datetime import date
from CTkMessagebox import CTkMessagebox

# file imports
from api.diagnosis import Diagnosis
from log_processes.health_log import SearchForLog, get_previous_month
from log.health_log import Log
from utils import *
from setup import *
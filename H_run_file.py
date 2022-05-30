import re, sys, json,datetime,datetime
import time, random#, testlink
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from random import choice
from pathlib import Path
from datetime import date
from openpyxl import Workbook
import os
import select
import H_function, H_functions, HR_timecard_H, HR_timecard_OT
from H_functions import execution_log, fail_log, error_log, Logging
from simple_colors import *

def MyExecution(domain_name):
    error_menu = []
    error_screenshot = []
    
    try:
        H_functions.access_hr(domain_name)
    except:
        Logging("Cannot continue execution")
        error_menu.append("H_functions.access_hr")
    
    try:
        HR_timecard_H.timecard()
    except:
        Logging("Cannot continue execution")
        error_menu.append("HR_timecard_H.timecard()")

    try:
        HR_timecard_H.time_card()
    except:
        Logging("Cannot continue execution")
        error_menu.append("HR_timecard_H.time_card()")
    
    
    hanh_log = {
        "execution_log": execution_log,
        "fail_log": fail_log,
        "error_log": error_log,
        "error_menu": error_menu
    }

    return hanh_log


def My_Execution(domain_name):
    H_functions.access_hr(domain_name)
    HR_timecard_H.timecard()
    #HR_timecard_H.time_card()
    #HR_timecard_OT.timecard_OT()
    #HR_timecard_OT.timecard_report()

#My_Execution("http:/groupware57.hanbiro.net/nhr/login")
#My_Execution("http:/gw.hanbirolinux.tk/nhr/login")
My_Execution("http:/global3.hanbiro.com/nhr/login")


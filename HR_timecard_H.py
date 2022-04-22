from calendar import timegm
from logging import exception
import re, sys, json#, testlink
import time, random
from selenium import webdriver
from random import randint
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from random import choice
from pathlib import Path
from datetime import datetime
import os.path
import time
import select
from H_functions import driver, data, ValidateFailResultAndSystem,TesCase_LogResult, Logging#, TestlinkResult_Fail, TestlinkResult_Pass
from simple_colors import *

now = datetime.now()
date_time = now.strftime("%Y/%m/%d, %H:%M:%S")

date_id = date_time.replace("/", "").replace(":", "").replace(", ", "")
n = random.randint(1,1000)

now = datetime.now()
date = now.strftime("%m/%d/%y %H:%M:%S")

print_date = now.strftime("%H:%M")

def input_reason_late():
    try:
        tardiness = driver.find_element_by_xpath(data["TIMECARD"]["tardiness"])
        if tardiness.is_displayed():
            driver.find_element_by_xpath(data["TIMECARD"]["input_reason_late"]).send_keys(data["TIMECARD"]["reason_late"])
            Logging("- Input reason late")
            #add_data_in_excel(param_excel["checkin"],"f","Input reason late")
            driver.find_element_by_xpath(data["TIMECARD"]["save"]).click()
            Logging("- Save reason late")
            #add_data_in_excel(param_excel["checkout"],"p","Save reason late")
            time_clock_in()
    except:
        Logging("- Clock-in on time")

def clock_in():
    try:
        #pop up clock-in display
        pop_up = driver.find_element_by_xpath(data["TIMECARD"]["pop_up"])
        time.sleep(1)
        if pop_up.is_displayed():
            try:
                clock_in_but = driver.find_element_by_xpath(data["TIMECARD"]["clock_in_but"])
                clock_in_but.click()
                Logging("- Clock-in")
                time.sleep(5)
                input_reason_late()
            except:
                Logging("- Clock-in already")
            
    except:
        #pop up clock-in don't display
        pop_up_hid = driver.find_element_by_xpath(data["TIMECARD"]["pop_up_hid"])
        pop_up_hid.click()
        Logging("- Click show pop up")
        time.sleep(2)
        pop_up = driver.find_element_by_xpath(data["TIMECARD"]["pop_up"])
        if pop_up.is_displayed():
            try:
                clock_in_but = driver.find_element_by_xpath(data["TIMECARD"]["clock_in_but"])
                clock_in_but.click()
                Logging("- Clock-in")
                time.sleep(5)
                input_reason_late()
            except:
                Logging("- Clock-in already")

def nightwork():
    time.sleep(4)
    try:
        midnight_popup = driver.find_element_by_xpath("//span[contains(.,'Confirm Nightwork')]")
        if midnight_popup.is_displayed():
            Logging("Nightwork popup is display")
            click_confirm = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Yes, confirm it!')]").click()
            click_apply_OT = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_action_apply_ot')]").click()
            input_memo_OT = driver.find_element_by_xpath("//textarea[contains(@class, 'form-control')]")
            input_memo_OT.send_keys("This is a test")
            time.sleep(3)
            scroll_apply_OT = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_action_apply')]")
            scroll_apply_OT.location_once_scrolled_into_view
            time.sleep(2)
            # #Export data
            # approver_data = driver.find_element_by_xpath("//div[contains(@class, 'approver-wrapper ')]//li/div/div[1]").text
            # Logging ("Approver: " + approver_data)
            # referrer_data = driver.find_element_by_xpath("//div[contains(@class, 'referer-wrapper')]//li/div/div[1]").text
            # Logging ("Referrer: " + referrer_data)
            # time.sleep(3)
            apply_OT_confirm = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_action_apply')]/..").click()
            Logging("Apply OT successfully - Approval is submitted successfully")
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["post_OT"]["pass"])
            time.sleep(3)
            #Approval page
            approval_page = driver.find_element_by_xpath("//li//a[contains(@href,'/nhr/hr/timecard/user/approval')]//span[contains(@data-lang-id, 'tc_approval_approval')]").click()            
            status_approve = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
            #Logging (status_approve.text)
            if status_approve.is_displayed():
                # Logging (status_approve.text)
                if status_approve.text == "Over Time":
                    Logging ("Approval is displayed in approval list")
                    # #Reject approve
                    # driver.find_element_by_xpath("//div[contains(@class, 'select-approval-status')]//div").click()
                    # driver.find_element_by_xpath("//div[contains(@data-lang-id, 'tc_action_reject')]").click()
                    # time.sleep(3)
                    # #Scroll to detail
                    # slider = driver.find_element_by_xpath("//div[@ref='eBodyHorizontalScrollViewport']")
                    # horizontal_bar = driver.find_element_by_xpath("//div[@ref='eHorizontalRightSpacer']")
                    # webdriver.ActionChains(driver).click_and_hold(slider).move_to_element(horizontal_bar).perform()
                    # webdriver.ActionChains(driver).release().perform()
                    # #Logging ("Scroll successfully")
                    # #Click view details
                    # driver.find_element_by_xpath("//div[1]/*[@col-id='id']//div[contains(@class, 'btn-view-detail')]").click()

                    # #Print status column
                    # postOT_event_status = driver.find_element_by_xpath("//div[contains(@class, 'avatar-wrapper')]/..//div[contains(@class, 'approval-status')]").text
                    # if postOT_event_status.text == "Pending":
                    #     Logging ("Status is not changed => Approve failed")
                    #     add_data_in_excel(param_excel["approve_status"],"p","Status is not changed => Approve failed")
                    # elif postOT_event_status.text == "Reject":
                    #     Logging ("Status is changed => Approve successfully")
                    #     add_data_in_excel(param_excel["approve_status"],"p","Status is changed => Approve successfully")
                else:
                    Logging ("Approval is not displayed in approval list")
            else: 
                Logging ("Approval is submitted failed")
        else:
            Logging("Apply OT failed - Approval is submitted failed")
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["post_OT"]["fail"])
    except:
        Logging("=> Don't show pop up nightwork")
        clock_in()


def time_clock_in():
    try:
        time.sleep(5)
        driver.find_element_by_xpath(data["TIMECARD"]["my_timesheets"]).click()
        Logging("- Select My timecard: Timesheets")
        format_time = driver.find_element_by_xpath(data["TIMECARD"]["format_time"])
        clock_time = format_time.text[0:2]

        item_clock = driver.find_element_by_xpath(data["TIMECARD"]["item_clock"])
        item_clock.location_once_scrolled_into_view
        time.sleep(2)

        driver.find_element_by_xpath(data["TIMECARD"]["edit_clockin_time"]).click()
        Logging("- Edit Clock-in time")
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["pop_up_edit"])))
        time.sleep(3)

        driver.find_element_by_xpath(data["TIMECARD"]["btn_hour"]).click()
        time.sleep(2)
        hours_time = driver.find_element_by_xpath("//*[starts-with(@id,'btnHours')]//following-sibling::div/button[contains(.,'" + clock_time + "')]")
        hours_time.click()
        Logging("- Select hours clock-in")
        driver.find_element_by_xpath(data["TIMECARD"]["btn_min"]).click()
        time.sleep(2)
        minute_time = driver.find_element_by_xpath(data["TIMECARD"]["minutes"])
        minute_time.click()
        Logging("- Select minutes clock-in")
        time.sleep(2)
        driver.find_element_by_xpath(data["TIMECARD"]["on_time"]).click()
        Logging("- Choose On time")
        driver.find_element_by_xpath(data["TIMECARD"]["save_edit"]).click()
        Logging("=> Save edit time clock-in")
    except:
        Logging("Pass")

def breaktime():
    try:
        #pop up clock-in display
        pop_up = driver.find_element_by_xpath(data["TIMECARD"]["pop_up"])
        time.sleep(1)
        if pop_up.is_displayed():
            try:
                breaktime_but = driver.find_element_by_xpath(data["TIMECARD"]["breaktime_but"])
                breaktime_but.click()
                Logging("- Break time")
                time.sleep(3)
                try:
                    pop_up_breaktime = driver.find_element_by_xpath(data["TIMECARD"]["pop_up_breaktime"])
                    if pop_up_breaktime.is_displayed():
                        Logging("=> Break time successfully")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["breaktime"]["pass"])
                        pop_up_breaktime.click()
                        time.sleep(3)
                        try:
                            pop_up_breaktime = driver.find_element_by_xpath(data["TIMECARD"]["pop_up_breaktime"])
                            if pop_up_breaktime.is_displayed():
                                Logging("- End break time fail")
                                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["end_breaktime"]["fail"])

                            else:
                                Logging("- End break time successfully")
                                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["end_breaktime"]["pass"])
                        except:
                            Logging("- End break time successfully")
                            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["end_breaktime"]["pass"])
                    else:
                        Logging("=> Break time fail")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["breaktime"]["fail"])
                except:
                    driver.refresh()
                    time.sleep(3)
                    pop_up_breaktime = driver.find_element_by_xpath(data["TIMECARD"]["pop_up_breaktime"])
                    if pop_up_breaktime.is_displayed():
                        Logging("=> Break time successfully")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["breaktime"]["pass"])
                        pop_up_breaktime.click()
                        time.sleep(3)
                        try:
                            pop_up_breaktime = driver.find_element_by_xpath(data["TIMECARD"]["pop_up_breaktime"])
                            if pop_up_breaktime.is_displayed():
                                Logging("- End break time fail")
                                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["end_breaktime"]["fail"])
                            else:
                                Logging("- End break time successfully")
                                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["end_breaktime"]["pass"])
                        except:
                            Logging("- End break time successfully")
                            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["end_breaktime"]["pass"])
                    else:
                        Logging("=> Break time fail")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["breaktime"]["fail"])
            except:
                Logging("- Don't show button breaktime")
            
    except:
        #pop up clock-in don't display
        pop_up_hid = driver.find_element_by_xpath(data["TIMECARD"]["pop_up_hid"])
        pop_up_hid.click()
        Logging("- Click show pop up")
        time.sleep(2)
        pop_up = driver.find_element_by_xpath(data["TIMECARD"]["pop_up"])
        if pop_up.is_displayed():
            try:
                breaktime_but = driver.find_element_by_xpath(data["TIMECARD"]["breaktime_but"])
                breaktime_but.click()
                Logging("- Break time")
                time.sleep(3)
                try:
                    pop_up_breaktime = driver.find_element_by_xpath(data["TIMECARD"]["pop_up_breaktime"])
                    if pop_up_breaktime.is_displayed():
                        Logging("=> Break time successfully")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["breaktime"]["pass"])
                        pop_up_breaktime.click()
                        time.sleep(3)
                        try:
                            pop_up_breaktime = driver.find_element_by_xpath(data["TIMECARD"]["pop_up_breaktime"])
                            if pop_up_breaktime.is_displayed():
                                Logging("- End break time fail")
                                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["end_breaktime"]["fail"])
                            else:
                                Logging("- End break time successfully")
                                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["end_breaktime"]["pass"])
                        except:
                            Logging("- End break time successfully")
                            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["end_breaktime"]["pass"])
                    else:
                        Logging("=> Break time fail")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["breaktime"]["fail"])
                except:
                    driver.refresh()
                    time.sleep(3)
                    pop_up_breaktime = driver.find_element_by_xpath(data["TIMECARD"]["pop_up_breaktime"])
                    if pop_up_breaktime.is_displayed():
                        Logging("=> Break time successfully")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["breaktime"]["pass"])
                        pop_up_breaktime.click()
                        time.sleep(3)
                        try:
                            pop_up_breaktime = driver.find_element_by_xpath(data["TIMECARD"]["pop_up_breaktime"])
                            if pop_up_breaktime.is_displayed():
                                Logging("- End break time fail")
                                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["end_breaktime"]["fail"])
                            else:
                                Logging("- End break time successfully")
                                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["end_breaktime"]["pass"])
                        except:
                            Logging("- End break time successfully")
                            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["end_breaktime"]["pass"])
                    else:
                        Logging("=> Break time fail")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["breaktime"]["fail"])
            except:
                Logging("- Don't show button breaktime")

def input_reason_leave_early():
    try:
        leave_early = driver.find_element_by_xpath(data["TIMECARD"]["leave_early"])
        if leave_early.is_displayed():
            driver.find_element_by_xpath(data["TIMECARD"]["input_reason_leave_early"]).send_keys(data["TIMECARD"]["reason_leave_early"])
            Logging("- Input reason")
            time.sleep(2)
            driver.find_element_by_xpath(data["TIMECARD"]["save"]).click()
            Logging("- Save reason")
            time.sleep(3)
            time_clock_out()
    except:
        Logging("- Clock-out on time")

def clock_out():
    try:
        #pop up clock-in display
        pop_up = driver.find_element_by_xpath(data["TIMECARD"]["pop_up"])
        time.sleep(1)
        if pop_up.is_displayed():
            try:
                clock_out_but = driver.find_element_by_xpath(data["TIMECARD"]["clock_out_but"])
                clock_out_but.click()
                Logging("- Clock-out")
                time.sleep(5)
                input_reason_leave_early()
            except:
                Logging("- Clock-out already")
                driver.find_element_by_xpath(data["TIMECARD"]["my_timesheets"]).click()
                Logging("- Select My timecard: Timesheets")
        else:
            Logging("=> Clock-out already")
            
    except:
        #pop up clock-in don't display
        pop_up_hid = driver.find_element_by_xpath(data["TIMECARD"]["pop_up_hid"])
        pop_up_hid.click()
        Logging("- Click show pop up")
        time.sleep(5)
        try:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["OT_popup"])))
            driver.find_element_by_xpath(data["TIMECARD"]["OT_clockout"]).click()
            Logging("- Clock-out")
            time.sleep(2)
            driver.find_element_by_xpath(data["TIMECARD"]["yes_but"][0]).click()
        except:
            pop_up = driver.find_element_by_xpath(data["TIMECARD"]["pop_up"])
            if pop_up.is_displayed():
                try:
                    clock_out_but = driver.find_element_by_xpath(data["TIMECARD"]["clock_out_but"])
                    clock_out_but.click()
                    Logging("- Clock-out")
                    time.sleep(5)
                    input_reason_leave_early()
                except:
                    Logging("- Clock-out already")
                    driver.find_element_by_xpath(data["TIMECARD"]["my_timesheets"]).click()
                    Logging("- Select My timecard: Timesheets")
            else:
                Logging("=> Clock-out already")

def time_clock_out():
    time.sleep(5)
    driver.find_element_by_xpath(data["TIMECARD"]["my_timesheets"]).click()
    Logging("- Select My timecard: Timesheets")
    format_time = driver.find_element_by_xpath(data["TIMECARD"]["format_time"])
    clock_time = format_time.text[0:2]
    work_time = format_time.text[8]
    clock_out_time = int(clock_time) + int(work_time)
    #Logging(clock_out_time)

    if str(clock_out_time) >= "13":
        clock_out_time_update = int(clock_out_time) + 1
        #Logging(clock_out_time_update)
    else:
        Logging( )

    item_clock = driver.find_element_by_xpath(data["TIMECARD"]["item_clock"])
    item_clock.location_once_scrolled_into_view
    time.sleep(2)

    driver.find_element_by_xpath(data["TIMECARD"]["edit_clockout_time"]).click()
    Logging("- Edit Clock-out time")
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["pop_up_edit"])))
    time.sleep(3)

    driver.find_element_by_xpath(data["TIMECARD"]["btn_hour"]).click()
    time.sleep(2)
    hours_time = driver.find_element_by_xpath("//*[starts-with(@id,'btnHours')]//following-sibling::div/button[contains(.,'" + str(clock_out_time_update) + "')]")
    hours_time.click()
    Logging("- Select hours clock-out")
    driver.find_element_by_xpath(data["TIMECARD"]["btn_min"]).click()
    time.sleep(2)
    minute_time = driver.find_element_by_xpath(data["TIMECARD"]["minutes"])
    minute_time.click()
    Logging("- Select minutes clock-out")
    time.sleep(2)
    driver.find_element_by_xpath(data["TIMECARD"]["on_time"]).click()
    Logging("- Choose On time")
    driver.find_element_by_xpath(data["TIMECARD"]["save_edit"]).click()
    Logging("=> Save edit time clock-out")

def check_time():
    time.sleep(5)
    #Print Clockin and Clokout
    today_work = driver.find_element_by_xpath("//*[@id='app']//div[@class='daily-wrapper']//div[@class='react-datepicker-wrapper']//span")
    today_work_date = today_work.text[8:10]
    #Logging(today_work_date)

    format_time = driver.find_element_by_xpath(data["TIMECARD"]["format_time"])
    clock_in_time = format_time.text
    #Logging(clock_in_time)

    work_method = driver.find_element_by_xpath(data["TIMECARD"]["work_method"])
    work_method_up = work_method.text
    #Logging(work_method_up)

    output_clock_in = driver.find_element_by_xpath(data["TIMECARD"]["output_clockin"])
    output_clock_in.location_once_scrolled_into_view
    time.sleep(2)
    Logging(">> Clock-in: " + output_clock_in.text)
    output_clockin = output_clock_in.text

    output_clock_out = driver.find_element_by_xpath(data["TIMECARD"]["output_clockout"])
    Logging(">> Clock-out: " + output_clock_out.text)
    output_clockout = output_clock_out.text

    officetime = driver.find_element_by_xpath(data["TIMECARD"]["officetime"])
    Logging(">> Office Time: " + officetime.text)

    breaktime = driver.find_element_by_xpath(data["TIMECARD"]["breaktime"])
    Logging(">> Break Time: " + breaktime.text)
    break_time = breaktime.text

    workingtime = driver.find_element_by_xpath(data["TIMECARD"]["workingtime"])
    Logging(">> Working Time: " + workingtime.text)
    working_time = workingtime.text

    OT = driver.find_element_by_xpath(data["TIMECARD"]["OT"])
    Logging(">> OT Time: " + OT.text)
    OT_time = OT.text

    return output_clockin,output_clockout,break_time,working_time,clock_in_time,work_method_up,today_work_date, OT_time

def timesheet_list(output_clockin,output_clockout,break_time,working_time, OT_time):
    date_clockin = driver.find_element_by_xpath("//*[@class='admin_status']//div[contains(@class,'daily-wrapper')]/div/div/div/div[2]/div/div[2]/div/div/span")
    #Logging(date_clockin.text)
    date_clock_in = date_clockin.text
    driver.find_element_by_xpath("//*[@id='app']//div[contains(@class,'admin_status')]//a/span[contains(.,'List')]").click()
    Logging("- My Timesheets: List")
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='admin_status']//div[contains(@class,'list-table-wrapper')]//form//div[contains(@ref,'eCenterContainer')]/div")))
    time.sleep(5)
    today = driver.find_element_by_xpath("//*[@class='admin_status']//div[contains(@class,'list-table-wrapper')]//form//div[contains(@ref,'eCenterContainer')]//div[contains(@col-id,'date')]/div[contains(.,'" + date_clock_in + "')]/../..")
    today.location_once_scrolled_into_view
    time.sleep(2)
    if today.is_displayed():
        clockin = driver.find_element_by_xpath("//div[contains(.,'" + date_clock_in + "')]/following-sibling::div[contains(@col-id,'clock_in')]/div/div/div")
        if output_clockin == clockin.text:
            Logging("Clock-in Time is correct")
        else:
            Logging("Clock-in Time is wrong")

        clockout = driver.find_element_by_xpath("//div[contains(.,'" + date_clock_in + "')]/following-sibling::div[contains(@col-id,'clock_out')]/div/div/div")
        if output_clockout == clockout.text:
            Logging("Clock-out Time is correct")
        else:
            Logging("Clock-out Time is wrong")

        breaktime_li = driver.find_element_by_xpath("//div[contains(.,'" + date_clock_in + "')]/following-sibling::div[contains(@col-id,'break_time_label')]/div/div")
        if break_time == breaktime_li.text:
            Logging("Break Time is correct")
        else:
            Logging("Break Time is wrong")

        workingtime_li = driver.find_element_by_xpath("//div[contains(.,'" + date_clock_in + "')]/following-sibling::div[contains(@col-id,'work_time_label')]/div/div")
        if working_time == workingtime_li.text:
            Logging("Working Time is correct")
        else:
            Logging("Working Time is wrong")

        OTtime_li = driver.find_element_by_xpath("//div[contains(.,'" + date_clock_in + "')]/following-sibling::div[contains(@col-id,'over_time_label')]/div/div")
        if OT_time == OTtime_li.text:
            Logging("OT Time is correct")
        elif OTtime_li.text == "-":
            Logging("No OT Time")
        else:
            Logging("OT Time is wrong")

        event_li = driver.find_element_by_xpath("//div[contains(.,'" + date_clock_in + "')]/following-sibling::div[contains(@col-id,'day_name')]/div/div")
        if event_li.text == "Work Day":
            Logging("Today is work day")
        if event_li.text == "Day Off":
            Logging("Today is day off")
        if event_li.text == "Holiday":
            Logging("Today is holiday")
        else:
            Logging("No Event")
                
    else:
        Logging("- Cannot find date")
    #approval_OT()

def add_event2():
    #SELECT APPROVAL SETTING 
    basic = driver.find_element_by_xpath(data["TIMECARD"]["basic"])
    basic.location_once_scrolled_into_view
    basic.click()
    Logging("- Setting: Basic")
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='card-body']//label/span[contains(@data-lang-id,'Use clock in/out pop-up.')]")))
    time.sleep(2)
    driver.find_element_by_xpath(data["TIMECARD"]["setting_approval"]).click()
    Logging("- Setting: Basic_Approval")
    time.sleep(3)
    work_correction_scroll = driver.find_element_by_xpath("//*[@class='basic_setting']//div[@class='card-body']//div[contains(@class,'title-primary') and contains(.,'Events')]")
    work_correction_scroll.location_once_scrolled_into_view
    time.sleep(2)
    EV_list = int(len(driver.find_elements_by_xpath(data["TIMECARD"]["EV_list"])))
    approval_EV_list = []
    i = 0
    for i in range(EV_list):
        i += 1
        approvalEV = driver.find_element_by_xpath(data["TIMECARD"]["approvalEV"] + "[" + str(i) + "]/label")
        approval_EV_list.append(approvalEV.text)

    Logging("- Total of type Approval Event: " + str(len(approval_EV_list)))
    #Logging(approval_EV_list)

    x = random.choice(approval_EV_list)
    time.sleep(1)
    select_approval_EV = driver.find_element_by_xpath(data["TIMECARD"]["EV_list"] + "[contains(.,'" + str(x) + "')]")
    select_approval_EV.click()
    Logging("- Select Approval Event type")
    time.sleep(2)

    if str(x) == "Approval Line":
        Logging("- Approval type: Approval Line")
        time.sleep(3)
        try:
            EV_approver = driver.find_element_by_xpath(data["TIMECARD"]["EV_approver"])
            if EV_approver.text == "No data was found.":
                Logging("- Don't have approval line")
                driver.find_element_by_xpath(data["TIMECARD"]["EV_add_approver"]).click()
                WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["wait_OT"])))
                time.sleep(2)
                EV_approval_line = driver.find_element_by_xpath(data["TIMECARD"]["approval_line"])
                EV_approval_line.send_keys(data["user_name"])
                EV_approval_line.send_keys(Keys.ENTER)
                time.sleep(3)
                driver.find_element_by_xpath(data["TIMECARD"]["select_user"]).click()
                driver.find_element_by_xpath(data["TIMECARD"]["plus_button"]).click()
                driver.find_element_by_xpath(data["TIMECARD"]["save_approver"]).click()
                Logging("- Save approval line")
                # EV_approver_list = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,  data["TIMECARD"]["approver_list"] + data["name_keyword"][1] + "')]")))
                approver_after_save = driver.find_element_by_xpath("//div[contains(@class,'title-note') and contains(.,'Business trip, education, outside work, etc.')]/following-sibling::div//div[contains(.,'Use Fixed approval line')]//label[contains(.,'Approvers')]/following::div[1]")
                if approver_after_save != "No data was found.":
                    Logging("- Save approvers list Successfully")
                    driver.refresh()
                    time.sleep(5)
                    driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Timesheets')]").click()
                    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Break time')] ")))
                    driver.find_element_by_xpath(data["TIMECARD"]["calendar"]).click()
                    Logging("- Select Timesheets: Calendar")
                    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["wait_calendar"])))
                    time.sleep(3)
                    driver.find_element_by_xpath(data["TIMECARD"]["add_event"]).click()
                    driver.find_element_by_xpath(data["TIMECARD"]["event"]).click()
                    time.sleep(2)

                    #Choose Event
                    choose_event = driver.find_element_by_xpath(data["TIMECARD"]["choose_event"])
                    choose_event.click()
                    time.sleep(3)
                    event = driver.find_element_by_xpath(data["TIMECARD"]["select_event"])
                    #event.send_keys(Keys.ARROW_DOWN)
                    event.send_keys(Keys.RETURN)
                    time.sleep(2)

                    # Add title
                    title = driver.find_element_by_xpath(data["TIMECARD"]["title"])
                    title.send_keys(data["TIMECARD"]["title_event"] + str(n))
                    Logging("- Input title")

                    # Add place
                    place = driver.find_element_by_xpath(data["TIMECARD"]["place"])
                    place.send_keys(data["TIMECARD"]["place_event"] + str(n))
                    Logging("- Input location")

                    # Add memo
                    memo = driver.find_element_by_xpath(data["TIMECARD"]["memo"])
                    memo.send_keys(data["TIMECARD"]["memo_event"] + str(n))
                    Logging("- Input memo")

                    #Save
                    driver.find_element_by_xpath(data["TIMECARD"]["save_event"]).click()
                    Logging("- Save")
                    time.sleep(2)
                    try:
                        noty_success = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["pre_OT_noty"])))
                        noty_event_list = [data["TIMECARD"]["noty_event"][0], data["TIMECARD"]["noty_event"][1]]
                        if noty_success.text in noty_event_list:
                            Logging("- Save event Successfully - Approval is submitted successfully")
                            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["add_event"]["pass"])
                            #Approval page
                            approval_page = driver.find_element_by_xpath("//li//a[contains(@href,'/nhr/hr/timecard/user/approval')]//span[contains(@data-lang-id, 'tc_approval_approval')]").click()
                            
                            time.sleep(3)
                            event_status_approve = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
                            # Logging (status_approve.text)
                            if event_status_approve.is_displayed():
                                # Logging(status_approve.text)
                                if event_status_approve.text == "Event":
                                    Logging ("- Event approval is displayed in approval list")
                                    open_approve_status_list = driver.find_element_by_xpath("//div[contains(@class, 'select-approval-status')]//div").click()
                                    #Logging("Open successfully")
                                    time.sleep(5)
                                    #Click random (Reject, Approve)
                                    approve_status_list = (int(len(driver.find_elements_by_xpath("//div[contains(@class,'select-approval-status-content')]/div"))))
                                    list_approve_status = []
                                    i=0
                                    for i in range(approve_status_list):
                                        i += 1
                                        approve_status = driver.find_element_by_xpath("//div[contains(@class,'select-approval-status-content')]/div[" + str(i) + "]/div")
                                        list_approve_status.append(approve_status.text)

                                    x1 = random.choice(list_approve_status)
                                    time.sleep(1)
                                    approve_status1 = driver.find_element_by_xpath("//div[contains(@class,'select-approval-status-content')]/div/div[contains(.,'" + str(x1) + "')]")
                                    approve_status1.click()
                                    Logging("- Select event approve status successfully")
                                    time.sleep(5)
                                    #Scroll to detail
                                    slider = driver.find_element_by_xpath("//div[@ref='eBodyHorizontalScrollViewport']")
                                    horizontal_bar = driver.find_element_by_xpath("//div[@ref='eHorizontalRightSpacer']")
                                    webdriver.ActionChains(driver).click_and_hold(slider).move_to_element(horizontal_bar).perform()
                                    webdriver.ActionChains(driver).release().perform()
                                    time.sleep(5)
                                    #Logging ("Scroll successfully")
                                    #Click view details
                                    driver.find_element_by_xpath("//div[1]/*[@col-id='id']//div[contains(@class, 'btn-view-detail')]").click()
                                    time.sleep(5)
                                    #Print status
                                    status_approve_event = driver.find_element_by_xpath("//div[contains(@class, 'avatar-wrapper')]/..//div[contains(@class, 'approval-status')]").text
                                    Logging ("- Modal is opened successfully")
                                    if status_approve_event == "Pending":
                                        Logging ("- Status is not changed => Approve failed")
                                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["approve_status"]["fail"])
                                    elif status_approve_event != str(x1):
                                        Logging ("- Status is changed => Approve successfully")
                                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["approve_status"]["pass"])
                                        #approval_OT()
                                else:
                                        Logging ("Event approval is not displayed in approval list")
                            else: 
                                    Logging ("Event approval is not displayed in approval list")
                        else:
                            Logging("- Save event Fail")
                            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["add_event"]["fail"])
                    except:
                        Logging("- Save event Fail")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["add_event"]["fail"])
                else:
                    Logging("- Save approvers list Fail")
            else:
                Logging("- Approval line has already")
                driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Timesheets')]").click()
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Break time')] ")))
                driver.find_element_by_xpath(data["TIMECARD"]["calendar"]).click()
                Logging("- Select Timesheets: Calendar")
                WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["wait_calendar"])))
                time.sleep(3)
                driver.find_element_by_xpath(data["TIMECARD"]["add_event"]).click()
                driver.find_element_by_xpath(data["TIMECARD"]["event"]).click()
                time.sleep(2)

                #Choose Event
                choose_event = driver.find_element_by_xpath(data["TIMECARD"]["choose_event"])
                choose_event.click()
                time.sleep(3)
                event = driver.find_element_by_xpath(data["TIMECARD"]["select_event"])
                #event.send_keys(Keys.ARROW_DOWN)
                event.send_keys(Keys.RETURN)
                time.sleep(2)

                # Add title
                title = driver.find_element_by_xpath(data["TIMECARD"]["title"])
                title.send_keys(data["TIMECARD"]["title_event"] + str(n))
                Logging("- Input title")

                # Add place
                place = driver.find_element_by_xpath(data["TIMECARD"]["place"])
                place.send_keys(data["TIMECARD"]["place_event"] + str(n))
                Logging("- Input location")

                # Add memo
                memo = driver.find_element_by_xpath(data["TIMECARD"]["memo"])
                memo.send_keys(data["TIMECARD"]["memo_event"] + str(n))
                Logging("- Input memo")

                #Save
                driver.find_element_by_xpath(data["TIMECARD"]["save_event"]).click()
                Logging("- Save")
                time.sleep(2)
                try:
                    noty_success = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["pre_OT_noty"])))
                    noty_event_list = [data["TIMECARD"]["noty_event"][0], data["TIMECARD"]["noty_event"][1]]
                    if noty_success.text in noty_event_list:
                        Logging("- Save event Successfully - Approval is submitted successfully")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["add_event"]["pass"])
                        #Approval page
                        approval_page = driver.find_element_by_xpath("//a[contains(@href,'/nhr/hr/timecard/company/approval')]").click()
                        
                        time.sleep(3)
                        event_status_approve = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
                        # Logging (status_approve.text)
                        if event_status_approve.is_displayed():
                            # Logging(status_approve.text)
                            if event_status_approve.text == "Event":
                                Logging ("- Event approval is displayed in approval list")
                                open_approve_status_list = driver.find_element_by_xpath("//div[contains(@class, 'select-approval-status')]//div").click()
                                #Logging("Open successfully")
                                time.sleep(5)
                                #Click random (Reject, Approve)
                                approve_status_list = (int(len(driver.find_elements_by_xpath("//div[contains(@class,'select-approval-status-content')]/div"))))
                                list_approve_status = []
                                i=0
                                for i in range(approve_status_list):
                                    i += 1
                                    approve_status = driver.find_element_by_xpath("//div[contains(@class,'select-approval-status-content')]/div[" + str(i) + "]/div")
                                    list_approve_status.append(approve_status.text)

                                x1 = random.choice(list_approve_status)
                                time.sleep(1)
                                approve_status1 = driver.find_element_by_xpath("//div[contains(@class,'select-approval-status-content')]/div/div[contains(.,'" + str(x1) + "')]")
                                approve_status1.click()
                                Logging("- Select event approve status successfully")
                                time.sleep(5)
                                #Scroll to detail
                                slider = driver.find_element_by_xpath("//div[@ref='eBodyHorizontalScrollViewport']")
                                horizontal_bar = driver.find_element_by_xpath("//div[@ref='eHorizontalRightSpacer']")
                                webdriver.ActionChains(driver).click_and_hold(slider).move_to_element(horizontal_bar).perform()
                                webdriver.ActionChains(driver).release().perform()
                                time.sleep(5)
                                #Logging ("Scroll successfully")
                                #Click view details
                                driver.find_element_by_xpath("//div[1]/*[@col-id='id']//div[contains(@class, 'btn-view-detail')]").click()
                                time.sleep(5)
                                #Print status
                                status_approve_event = driver.find_element_by_xpath("//div[contains(@class, 'avatar-wrapper')]/..//div[contains(@class, 'approval-status')]").text
                                Logging ("- Modal is opened successfully")
                                if status_approve_event == "Pending":
                                    Logging ("- Status is not changed => Approve failed")
                                    TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["approve_status"]["fail"])
                                elif status_approve_event != str(x1):
                                    Logging ("- Status is changed => Approve successfully")
                                    TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["approve_status"]["pass"])
                                    #approval_OT()
                                #Click view details
                                driver.find_element_by_xpath("//div[1]/*[@col-id='id']//div[contains(@class, 'btn-view-detail')]").click()
                                time.sleep(5)
                            else:
                                    Logging ("Event approval is not displayed in approval list")
                        else: 
                                Logging ("Event approval is not displayed in approval list")
                    else:
                        Logging("- Save event Fail")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["add_event"]["fail"])
                except:
                    Logging("- Save event Fail")
                    TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["add_event"]["fail"])
        except:
            Logging(" ")
    elif str(x) == "Automatic approval":
        Logging("- Approval type: Automatic approval")
        driver.refresh()
        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Timesheets')]").click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Break time')] ")))
        time.sleep(3)
        driver.find_element_by_xpath(data["TIMECARD"]["calendar"]).click()
        Logging("- Select Timesheets: Calendar")
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["wait_calendar"])))
        time.sleep(3)
        driver.find_element_by_xpath(data["TIMECARD"]["add_event"]).click()
        driver.find_element_by_xpath(data["TIMECARD"]["event"]).click()
        time.sleep(2)

        #Choose Event
        choose_event = driver.find_element_by_xpath(data["TIMECARD"]["choose_event"])
        choose_event.click()
        time.sleep(3)
        event = driver.find_element_by_xpath(data["TIMECARD"]["select_event"])
        #event.send_keys(Keys.ARROW_DOWN)
        event.send_keys(Keys.RETURN)
        time.sleep(2)

        # Add title
        title = driver.find_element_by_xpath(data["TIMECARD"]["title"])
        title.send_keys(data["TIMECARD"]["title_event"] + str(n))
        Logging("- Input title")

        # Add place
        place = driver.find_element_by_xpath(data["TIMECARD"]["place"])
        place.send_keys(data["TIMECARD"]["place_event"] + str(n))
        Logging("- Input location")

        # Add memo
        memo = driver.find_element_by_xpath(data["TIMECARD"]["memo"])
        memo.send_keys(data["TIMECARD"]["memo_event"] + str(n))
        Logging("- Input memo")

        #Save
        driver.find_element_by_xpath(data["TIMECARD"]["save_event"]).click()
        Logging("- Save event successfully - Event approval is submitted successfully")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["add_event"]["pass"])
        
        time.sleep(2)
        #Approval page
        approval_page = driver.find_element_by_xpath("//li//a[contains(@href,'/nhr/hr/timecard/user/approval')]//span[contains(@data-lang-id, 'tc_approval_approval')]").click()
        
        ev_status_approve = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
        #Logging (status_approve.text)
        if ev_status_approve.is_displayed():
            #Logging (ev_status_approve.text)
            if ev_status_approve.text == "Event":
                Logging ("- Event approval is displayed in approval list")
                time.sleep(3)
                #Scroll to detail
                slider = driver.find_element_by_xpath("//div[@ref='eBodyHorizontalScrollViewport']")
                horizontal_bar = driver.find_element_by_xpath("//div[@ref='eHorizontalRightSpacer']")
                webdriver.ActionChains(driver).click_and_hold(slider).move_to_element(horizontal_bar).perform()
                webdriver.ActionChains(driver).release().perform()
                #Logging ("Scroll successfully")
                #Click view details
                driver.find_element_by_xpath("//div[1]/*[@col-id='id']//div[contains(@class, 'btn-view-detail')]").click()
                time.sleep(5)
                #Print status column
                event_status_app = driver.find_element_by_xpath("//div[contains(@class, 'avatar-wrapper')]/..//div[contains(@class, 'approval-status')]")
                ab1 = event_status_app.text
                time.sleep(3)
                if ab1 == "Pending":
                    Logging ("- Status is not changed => Approve failed")
                    TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["approve_status"]["fail"])
                elif ab1 != "Pending":
                    Logging ("- Status is changed => Approve successfully")
                    TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["approve_status"]["pass"])
            else:
                Logging ("- Event approval is not displayed in approval list")
        else: 
            Logging ("- Event approval is submitted failed")
    elif str(x) == "Head Dept.":
        Logging("- Approval type: Head Dept.")
        driver.refresh()
        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Timesheets')]").click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Break time')] ")))
        driver.find_element_by_xpath(data["TIMECARD"]["calendar"]).click()
        Logging("- Select Timesheets: Calendar")
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["wait_calendar"])))
        time.sleep(3)
        driver.find_element_by_xpath(data["TIMECARD"]["add_event"]).click()
        driver.find_element_by_xpath(data["TIMECARD"]["event"]).click()
        time.sleep(2)

        #Choose Event
        choose_event = driver.find_element_by_xpath(data["TIMECARD"]["choose_event"])
        choose_event.click()
        time.sleep(3)
        event = driver.find_element_by_xpath(data["TIMECARD"]["select_event"])
        #event.send_keys(Keys.ARROW_DOWN)
        event.send_keys(Keys.RETURN)
        time.sleep(2)

        # Add title
        title = driver.find_element_by_xpath(data["TIMECARD"]["title"])
        title.send_keys(data["TIMECARD"]["title_event"] + str(n))
        Logging("- Input title")

        # Add place
        place = driver.find_element_by_xpath(data["TIMECARD"]["place"])
        place.send_keys(data["TIMECARD"]["place_event"] + str(n))
        Logging("- Input location")

        # Add memo
        memo = driver.find_element_by_xpath(data["TIMECARD"]["memo"])
        memo.send_keys(data["TIMECARD"]["memo_event"] + str(n))
        Logging("- Input memo")

        #Save
        driver.find_element_by_xpath(data["TIMECARD"]["save_event"]).click()
        Logging("- Save event successfully - Event approval is submitted successfully")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["add_event"]["pass"])

        time.sleep(2) 
        
        #Approval page
        approval_page = driver.find_element_by_xpath("//li//a[contains(@href,'/nhr/hr/timecard/user/approval')]//span[contains(@data-lang-id, 'tc_approval_approval')]").click()
        
        ev_status_approve = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
        #Logging (status_approve.text)
        if ev_status_approve.is_displayed():
            #Logging (ev_status_approve.text)
            if ev_status_approve.text == "Event":
                Logging ("- Event approval is displayed in approval list")
                #Scroll to detail
                slider = driver.find_element_by_xpath("//div[@ref='eBodyHorizontalScrollViewport']")
                horizontal_bar = driver.find_element_by_xpath("//div[@ref='eHorizontalRightSpacer']")
                webdriver.ActionChains(driver).click_and_hold(slider).move_to_element(horizontal_bar).perform()
                webdriver.ActionChains(driver).release().perform()
                time.sleep(5)
                #Click view details
                driver.find_element_by_xpath("//div[1]/*[@col-id='id']//div[contains(@class, 'btn-view-detail')]").click()
                time.sleep(5)
            else:
                Logging ("- Event approval is not displayed in approval list")
        else: 
            Logging ("- Event approval is submitted failed")
    elif str(x) == "Timecard Manager":
        Logging("- Approval type: Timecard Manager")
        driver.refresh()
        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Timesheets')]").click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Break time')] ")))
        driver.find_element_by_xpath(data["TIMECARD"]["calendar"]).click()
        Logging("- Select Timesheets: Calendar")
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["wait_calendar"])))
        time.sleep(3)
        driver.find_element_by_xpath(data["TIMECARD"]["add_event"]).click()
        driver.find_element_by_xpath(data["TIMECARD"]["event"]).click()
        time.sleep(2)

        #Choose Event
        choose_event = driver.find_element_by_xpath(data["TIMECARD"]["choose_event"])
        choose_event.click()
        time.sleep(3)
        event = driver.find_element_by_xpath(data["TIMECARD"]["select_event"])
        #event.send_keys(Keys.ARROW_DOWN)
        event.send_keys(Keys.RETURN)
        time.sleep(2)

        # Add title
        title = driver.find_element_by_xpath(data["TIMECARD"]["title"])
        title.send_keys(data["TIMECARD"]["title_event"] + str(n))
        Logging("- Input title")

        # Add place
        place = driver.find_element_by_xpath(data["TIMECARD"]["place"])
        place.send_keys(data["TIMECARD"]["place_event"] + str(n))
        Logging("- Input location")

        # Add memo
        memo = driver.find_element_by_xpath(data["TIMECARD"]["memo"])
        memo.send_keys(data["TIMECARD"]["memo_event"] + str(n))
        Logging("- Input memo")

        #Save
        driver.find_element_by_xpath(data["TIMECARD"]["save_event"]).click()
        Logging("- Save event successfully - Event approval is submitted successfully")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["add_event"]["pass"])
        time.sleep(3)

        #Approval page
        approval_page = driver.find_element_by_xpath("//li//a[contains(@href,'/nhr/hr/timecard/user/approval')]//span[contains(@data-lang-id, 'tc_approval_approval')]").click()

        ev_status_approve = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
        #Logging (status_approve.text)
        if ev_status_approve.is_displayed():
            #Logging (ev_status_approve.text)
            if ev_status_approve.text == "Event":
                Logging ("- Event approval is displayed in approval list")
                #Scroll to detail
                slider = driver.find_element_by_xpath("//div[@ref='eBodyHorizontalScrollViewport']")
                horizontal_bar = driver.find_element_by_xpath("//div[@ref='eHorizontalRightSpacer']")
                webdriver.ActionChains(driver).click_and_hold(slider).move_to_element(horizontal_bar).perform()
                webdriver.ActionChains(driver).release().perform()
                time.sleep(5)
                #Click view details
                driver.find_element_by_xpath("//div[1]/*[@col-id='id']//div[contains(@class, 'btn-view-detail')]").click()
                time.sleep(5)
            else:
                Logging ("- Event approval is not displayed in approval list")
        else: 
            Logging ("- Event approval is submitted failed")
    elif str(x) == "Dept. Manager":
        Logging("- Approval type: Dept. Manager")
        driver.refresh()
        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Timesheets')]").click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Break time')] ")))
        driver.find_element_by_xpath(data["TIMECARD"]["calendar"]).click()
        Logging("- Select Timesheets: Calendar")
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["wait_calendar"])))
        time.sleep(3)
        driver.find_element_by_xpath(data["TIMECARD"]["add_event"]).click()
        driver.find_element_by_xpath(data["TIMECARD"]["event"]).click()
        time.sleep(2)

        #Choose Event
        choose_event = driver.find_element_by_xpath(data["TIMECARD"]["choose_event"])
        choose_event.click()
        time.sleep(3)
        event = driver.find_element_by_xpath(data["TIMECARD"]["select_event"])
        #event.send_keys(Keys.ARROW_DOWN)
        event.send_keys(Keys.RETURN)
        time.sleep(2)

        # Add title
        title = driver.find_element_by_xpath(data["TIMECARD"]["title"])
        title.send_keys(data["TIMECARD"]["title_event"] + str(n))
        Logging("- Input title")

        # Add place
        place = driver.find_element_by_xpath(data["TIMECARD"]["place"])
        place.send_keys(data["TIMECARD"]["place_event"] + str(n))
        Logging("- Input location")

        # Add memo
        memo = driver.find_element_by_xpath(data["TIMECARD"]["memo"])
        memo.send_keys(data["TIMECARD"]["memo_event"] + str(n))
        Logging("- Input memo")

        #Save
        driver.find_element_by_xpath(data["TIMECARD"]["save_event"]).click()
        Logging("- Save event successfully - Event approval is submitted successfully")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["add_event"]["pass"])
        time.sleep(2)

        #Approval page
        approval_page = driver.find_element_by_xpath("//li//a[contains(@href,'/nhr/hr/timecard/user/approval')]//span[contains(@data-lang-id, 'tc_approval_approval')]").click()
        
        ev_status_approve = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
        #Logging (status_approve.text)
        if ev_status_approve.is_displayed():
            #Logging (ev_status_approve.text)
            if ev_status_approve.text == "Event":
                Logging ("- Event approval is displayed in approval list")
                #Scroll to detail
                slider = driver.find_element_by_xpath("//div[@ref='eBodyHorizontalScrollViewport']")
                horizontal_bar = driver.find_element_by_xpath("//div[@ref='eHorizontalRightSpacer']")
                webdriver.ActionChains(driver).click_and_hold(slider).move_to_element(horizontal_bar).perform()
                webdriver.ActionChains(driver).release().perform()
                time.sleep(5)
                #Click view details
                driver.find_element_by_xpath("//div[1]/*[@col-id='id']//div[contains(@class, 'btn-view-detail')]").click()
                time.sleep(5)
            else:
                Logging ("- Event approval is not displayed in approval list")
        else: 
            Logging ("- Event approval is submitted failed")

    #approval_OT()

def view_details():
    # #Scroll to detail
    # slider = driver.find_element_by_xpath("//div[@ref='eBodyHorizontalScrollViewport']")
    # horizontal_bar = driver.find_element_by_xpath("//div[@ref='eHorizontalRightSpacer']")
    # webdriver.ActionChains(driver).click_and_hold(slider).move_to_element(horizontal_bar).perform()
    # webdriver.ActionChains(driver).release().perform()
    # time.sleep(5)
    # #Logging ("Scroll successfully")
    # #Click view details
    # driver.find_element_by_xpath("//div[1]/*[@col-id='id']//div[contains(@class, 'btn-view-detail')]").click()
    # time.sleep(5)
    #View details data
    try:
        content_add_event_date = driver.find_element_by_xpath("//div[contains(@class, 'sidebar-approval-wrapper')]/div[3]/div[1]")
        if content_add_event_date.is_displayed():
            Logging("- Content is displayed")
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["view_details"]["pass"])
        else:
            Logging("- Content is not displayed")
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["view_details"]["fail"])
    except:
        Logging("- Content empty")

    try:
        route_add_event = driver.find_element_by_xpath("//label[contains(@data-lang-id, 'tc_title_approver')]")
        if route_add_event.is_displayed():
            Logging("- Route is displayed")
        else:
            Logging("- Route is not displayed")
    except:
        Logging("- Route empty")

    try:
        referer_add_event = driver.find_element_by_xpath("//label[contains(@data-lang-id, 'tc_title_referer')]")
        if referer_add_event.is_displayed():
            Logging("- Referrer is displayed")
        else:
            Logging("- Referrer is not displayed")
    except:
        Logging("- Referrer empty")

    try:
        history_scroll = driver.find_element_by_xpath("//div[contains(@class, 'sidebar-approval-wrapper')]/div[3]/div[3]")
        history_scroll.location_once_scrolled_into_view
        time.sleep(5)
        #Logging("Scroll successfully")
    except:
        Logging(" ")

    try:
        history_add_event = driver.find_element_by_xpath("//div[contains(@class, 'sidebar-approval-wrapper')]/div[3]/div[3]")
        if history_add_event.is_displayed():
            Logging("- History is displayed")
        else:
            Logging("- History is not displayed")
    except:
        Logging("- History empty")

    #approval_OT()

def working_status():
    time.sleep(5)
    driver.find_element_by_xpath(data["TIMECARD"]["add_working_status"]).click()
    Logging("- Add working status")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["working_status"])))
    try:
        add_workingstatus = driver.find_element_by_xpath(data["TIMECARD"]["clear_working_status"])
        if add_workingstatus.is_displayed():
            add_workingstatus.click()
            time.sleep(3)
            add_working_status()
            time.sleep(2)
    except:
        add_working_status()
        time.sleep(2)
        Logging(" ")

def add_working_status():
    working_status_list = (int(len(driver.find_elements_by_xpath(data["TIMECARD"]["working_status"]))))

    list_working_status = []
    i=0
    for i in range(working_status_list):
        i += 1
        working_status = driver.find_element_by_xpath("//*[@id='click-out-side-5']//div[contains(@class,'item-header-content')]//div[2]/div/div" + "[" + str(i) + "]/div")
        list_working_status.append(working_status.text)

    x = random.choice(list_working_status)
    time.sleep(1)
    status = driver.find_element_by_xpath("//*[@id='click-out-side-5']//div[contains(@class,'item-header-content')]//div[2]/div/div/div[contains(.,'" + str(x) + "')]")
    status.click()
    Logging("- Select status")

    driver.find_element_by_xpath(data["TIMECARD"]["dropdown_time"]).click()
    time.sleep(3)
    status_time_list = (int(len(driver.find_elements_by_xpath(data["TIMECARD"]["status_time_list"]))))

    list_status_time = []
    y = 0
    for y in range(status_time_list):
        y += 1
        status_time = driver.find_element_by_xpath("//*[starts-with(@id,'dropdown')]/div/button" + "[" + str(y) + "]/div")
        list_status_time.append(status_time.text)

    m = random.choice(list_status_time)
    time.sleep(1)
    time_st = driver.find_element_by_xpath("//*[starts-with(@id,'dropdown')]/div/button/div[contains(.,'" + str(m) + "')]")
    time_st.click()
    time.sleep(3)

    if str(m) != "Select date and time":
        driver.find_element_by_xpath(data["TIMECARD"]["save_working_status"]).click()
        Logging("- Save working status")
    else:
        driver.find_element_by_xpath(data["TIMECARD"]["choose_time"]).click()
        driver.find_element_by_xpath(data["TIMECARD"]["select_time"]).click()
        Logging("- Select time of working status")
        driver.find_element_by_xpath(data["TIMECARD"]["save_working_status"]).click()
        Logging("- Save working status")



def approval_OT():
    basic = driver.find_element_by_xpath(data["TIMECARD"]["basic"])
    basic.location_once_scrolled_into_view
    basic.click()
    Logging("- Setting: Basic")
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='card-body']//label/span[contains(@data-lang-id,'Use clock in/out pop-up.')]")))
    time.sleep(2)
    driver.find_element_by_xpath("//div[@class='card-body']//label/span[contains(@data-lang-id,'Use clock in/out pop-up.')]").click()
    time.sleep(2)
    checkbox = driver.find_element_by_xpath("//div[@class='card-body']//label/span[contains(@data-lang-id,'Use clock in/out pop-up.')]/../../input")
    if checkbox.is_selected():
        Logging("- Turn on clock-in/out pop up")
        driver.refresh()
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='card-body']//label/span[contains(@data-lang-id,'Use clock in/out pop-up.')]")))
        time.sleep(2)
        try:
            pop_up = driver.find_element_by_xpath(data["TIMECARD"]["pop_up"])
            if pop_up.is_displayed():
                Logging("=> Turn on clock-in/out pop up successfully")

        except:
            Logging("=> Turn on clock-in/out pop up fail")
    else:
        Logging("- Turn off clock-in/out pop up")
        driver.refresh()
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='card-body']//label/span[contains(@data-lang-id,'Use clock in/out pop-up.')]")))
        time.sleep(2)
        try:
            pop_up = driver.find_element_by_xpath(data["TIMECARD"]["pop_up"])
            if pop_up.is_displayed():
                Logging("=> Turn off clock-in/out pop up fail")
        except:
            Logging("=> Turn off clock-in/out pop up successfully")

    time.sleep(2)
    driver.find_element_by_xpath(data["TIMECARD"]["setting_approval"]).click()
    Logging("- Setting: Basic_Approval")
    time.sleep(3)
    OT = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["OT_scroll"])))
    OT.location_once_scrolled_into_view
    time.sleep(2)
    OT_list = int(len(driver.find_elements_by_xpath(data["TIMECARD"]["OT_list"])))

    approval_OT_list = []
    i = 0
    for i in range(OT_list):
        i += 1
        approvalOT = driver.find_element_by_xpath(data["TIMECARD"]["approvalOT"] + "[" + str(i) + "]/label")
        approval_OT_list.append(approvalOT.text)
    
    Logging("- Total of type Approval OT: " + str(len(approval_OT_list)))
    #Logging(approval_OT_list)

    x = random.choice(approval_OT_list)
    time.sleep(1)
    select_approval_OT = driver.find_element_by_xpath(data["TIMECARD"]["OT_list"] + "[contains(.,'" + str(x) + "')]")
    select_approval_OT.click()
    Logging("- Select Approval OT type")
    time.sleep(2)

    if str(x) == "Approval Line":
        try:
            approver = driver.find_element_by_xpath(data["TIMECARD"]["approver"])
            if approver.text == "No data was found.":
                Logging("- Don't have approval line")
                driver.find_element_by_xpath(data["TIMECARD"]["add_approver"]).click()
                WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["wait_OT"])))
                time.sleep(2)
                approval_line = driver.find_element_by_xpath(data["TIMECARD"]["approval_line"])
                approval_line.send_keys(data["name_keyword"][1])
                approval_line.send_keys(Keys.ENTER)
                time.sleep(3)
                driver.find_element_by_xpath(data["TIMECARD"]["select_user"]).click()
                driver.find_element_by_xpath(data["TIMECARD"]["plus_button"]).click()
                driver.find_element_by_xpath(data["TIMECARD"]["save_approver"]).click()
                Logging("- Save approval line")
                approver_list = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,  data["TIMECARD"]["approver_list"] + data["name_keyword"][1] + "')]")))
                if approver_list.is_displayed():
                    Logging("- Save approvers list Successfully")
                else:
                    Logging("- Save approvers list Fail")
            else:
                Logging("- Approval line has already")
        except:
            Logging()
         
    driver.find_element_by_xpath(data["TIMECARD"]["my_timesheets"]).click()
    time.sleep(1)
    driver.find_element_by_xpath(data["TIMECARD"]["calendar"]).click()
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["wait_calendar"])))
    time.sleep(3)
    driver.find_element_by_xpath(data["TIMECARD"]["add_event"]).click()
    time.sleep(1)
    driver.find_element_by_xpath(data["TIMECARD"]["add_OT"]).click()
    time.sleep(3)

    driver.find_element_by_xpath(data["TIMECARD"]["filter"]).click()
    filters_OT_list = int(len(driver.find_elements_by_xpath(data["TIMECARD"]["filters_OT_list"])))

    list_filters_OT = []
    y = 0
    for y in range(filters_OT_list):
        y += 1
        filters = driver.find_element_by_xpath("//button[contains(.,'Select Filters')]/following-sibling::div/a[contains(.,'" + str(y) + "')]")
        list_filters_OT.append(filters.text)

    m = random.choice(list_filters_OT)
    filter_time = driver.find_element_by_xpath("//button[contains(.,'Select Filters')]/following-sibling::div/a[contains(.,'" + str(m) + "')]")
    filter_time.click()
    Logging("- Select filters time OT")
    time.sleep(2)

    memo_approval_line = driver.find_element_by_xpath(data["TIMECARD"]["memo_approval_line"])
    memo_approval_line.send_keys("I would like to OT " + str(m) + " after work. Date: " + date)

    driver.find_element_by_xpath(data["TIMECARD"]["save_approval_line"]).click()
    Logging("- Apply Pre OT")
    try:
        noty_success = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["pre_OT_noty"])))
        time.sleep(3)
        noty_list = [data["TIMECARD"]["pre_OT_noty_success"][0], data["TIMECARD"]["pre_OT_noty_success"][1]]
        if noty_success.text in noty_list:
            Logging("- Apply Pre OT Successfully")
            add_data_in_excel(param_excel["pre_OT"],"p","Apply Pre OT Successfully")
        elif noty_success.text == data["TIMECARD"]["pre_OT_noty_error"]:
            Logging("- Apply Pre OT has already")
            add_data_in_excel(param_excel["pre_OT"],"p","Apply Pre OT has already")
            time.sleep(3)
            driver.find_element_by_xpath("//div[@class='modal-header ']//button").click()
            time.sleep(2)
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["exit"]))).click()
        else:
            Logging("- Apply Pre OT Fail")
            add_data_in_excel(param_excel["pre_OT"],"f","Apply Pre OT Fail")
    except:
        Logging("- Apply Pre OT Fail")
        add_data_in_excel(param_excel["pre_OT"],"f","Apply Pre OT Fail")

    time.sleep(5)
    driver.find_element_by_xpath(data["TIMECARD"]["approval"]).click()
    Logging("- My Timecard: Approval")
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["approval_list"])))
    pre_OT = driver.find_element_by_xpath(data["TIMECARD"]["pre_OT"])
    if pre_OT.text == "Over Time (Pre)":
        Logging("- Approval list: Pre OT")
        driver.find_element_by_xpath(data["TIMECARD"]["detail"]).click()
        Logging("- View detail approval")
        time.sleep(2) 
        if str(x) == "Automatic approval":
            status_pre_OT = driver.find_element_by_xpath(data["TIMECARD"]["status_pre_OT"])
            if status_pre_OT.text == "Approved":
                Logging("- Pre OT has been approved automatically")
                driver.find_element_by_xpath(data["TIMECARD"]["turn_off_view"]).click()
                time.sleep(2)
            else:
                Logging("- Pre OT hasn't been approved automatically")
                Logging("=> Fail")
                driver.find_element_by_xpath(data["TIMECARD"]["turn_off_view"]).click()
                time.sleep(2)
        else:
            status_pre_OT = driver.find_element_by_xpath(data["TIMECARD"]["status_pre_OT"])
            time.sleep(2)
            if status_pre_OT.text == "Approved":
                Logging("- Pre OT has been Approved")
                driver.find_element_by_xpath(data["TIMECARD"]["turn_off_view"]).click()
                time.sleep(2)
            elif status_pre_OT == "Cancelled":
                Logging("- Pre OT has been Cancelled")
                driver.find_element_by_xpath(data["TIMECARD"]["turn_off_view"]).click()
                time.sleep(2)
            else:
                status_pre_OT.click()
                Logging("- Cancel Pre OT")
                time.sleep(2)
                driver.find_element_by_xpath(data["TIMECARD"]["yes_but"][1]).click()
                time.sleep(5)
                driver.find_element_by_xpath(data["TIMECARD"]["reload"]).click()
                status_update = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["status_update"])))
                time.sleep(5)
                if status_update.text == "Cancelled":
                    Logging("- Cancel Pre OT successfully")
                else:
                    Logging("- Cancel Pre OT fail")
    else:
        Logging(" ")

def manager():
    manager = driver.find_element_by_xpath(data["TIMECARD"]["manager"])
    manager.location_once_scrolled_into_view
    manager.click()
    Logging("- Settings: Manager")
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='basic_setting']//form//div[1]/div[2]/div[1]")))
    time.sleep(2)
    driver.find_element_by_xpath("//div[@class='permission-setting-wrapper']//button[contains(.,'Add manager')]").click()
    time.sleep(3)
    add_manager = driver.find_element_by_xpath("//*[@id='org-form-search']//input")
    add_manager.send_keys(data["name_keyword"][1])
    add_manager.send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element_by_xpath("//div[@class='org-search']//div[starts-with(@id,'tree')]/ul/li//span[contains(@role,'checkbox')]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//div[@class='card-body']//button[contains(.,'Add')]").click()

    try:
        no_user = driver.find_element_by_xpath("//div[@class='card-body']/div/div[3]//div[contains(@class,'text-opacity') and contains(.,'No data was found.')]")
        if no_user.is_displayed():
            Logging("- Add user from ORG Fail") 
    except:
        Logging("- Add user from ORG successfully")

    permission_list = int(len(driver.find_elements_by_xpath("//*[starts-with(@id,'right-sidebar')]//div[contains(text(),'Select department/user')]/following-sibling::div/div/div")))

    list_permission = []
    i = 0
    for i in range(permission_list):
        i += 1
        permission = driver.find_element_by_xpath("//*[starts-with(@id,'right-sidebar')]//div[contains(text(),'Select department/user')]/following-sibling::div/div/div[" + str(i) + "]//label")
        list_permission.append(permission.text)

    x = random.choice(list_permission)
    select_per = driver.find_element_by_xpath("//*[starts-with(@id,'right-sidebar')]//div[contains(text(),'Select department/user')]/following-sibling::div/div/div//label[contains(.,'" + str(x) + "')]")
    select_per.click()
    Logging("- Select permission")

    if str(x) == "Select Department/User":
        search_dept = driver.find_element_by_xpath("//div[text()='Select department/user']//following::form[@id='org-form-search']//input[contains(@placeholder,'Search')]")
        search_dept.send_keys("Selenium")
        search_dept.send_keys(Keys.ENTER)
        time.sleep(3)
        driver.find_element_by_xpath("//div[text()='Select department/user']//following::div//ul[starts-with(@id,'ft-id')]//span/span[2]").click()
        driver.find_element_by_xpath("//div[text()='Select department/user']//following::button[contains(.,'Add')]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[starts-with(@id,'right-sidebar')]//div[contains(.,'Manager Settings')]//button[contains(.,'Save')]").click()
        Logging("- Save")
        time.sleep(3)
        try:
            error = driver.find_element_by_xpath("//*[starts-with(@id,'noty_bar')]//div[contains(text(),'Duplicate data exists.')]")
            if error.is_displayed():
                Logging("=> Duplicate data exists")
                driver.find_element_by_xpath("//*[starts-with(@id,'right-sidebar')][2]//div[contains(@class,'close-btn')]").click()

                time.sleep(3)
                search = driver.find_element_by_xpath("//div[@class='basic_setting']//div[contains(@class,'input-group')]//input")
                search.send_keys(data["name_keyword"][1])
                search.send_keys(Keys.ENTER)
                time.sleep(2)

                slider = driver.find_element_by_xpath("//div[@ref='eBodyHorizontalScrollViewport']")
                horizontal_bar = driver.find_element_by_xpath("//div[@ref='eHorizontalRightSpacer']")

                webdriver.ActionChains(driver).click_and_hold(slider).move_to_element(horizontal_bar).perform()
                webdriver.ActionChains(driver).release().perform()
                time.sleep(2)
                driver.find_element_by_xpath("//span[contains(@ref,'eCellValue')]//div[contains(@class,'btn-view-detail')][2]").click()
                Logging("- Delete Dept. Manager")
                time.sleep(2)
                driver.find_element_by_xpath("//button/span[contains(@data-lang-id, 'tc_action_delete')]").click()
                Logging("- Click Delete button")
        except:
            Logging("=> Save manager successfully")
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["add_manager"]["pass"])
            time.sleep(3)
            search = driver.find_element_by_xpath("//div[@class='basic_setting']//div[contains(@class,'input-group')]//input")
            search.send_keys(data["name_keyword"][1])
            search.send_keys(Keys.ENTER)
            time.sleep(2)

            slider = driver.find_element_by_xpath("//div[@ref='eBodyHorizontalScrollViewport']")
            horizontal_bar = driver.find_element_by_xpath("//div[@ref='eHorizontalRightSpacer']")

            webdriver.ActionChains(driver).click_and_hold(slider).move_to_element(horizontal_bar).perform()
            webdriver.ActionChains(driver).release().perform()
            time.sleep(2)

            driver.find_element_by_xpath("//span[contains(@ref,'eCellValue')]//div[contains(@class,'btn-view-detail')][1]").click()
            Logging("- View detail")
            time.sleep(2)

            try:
                manager_permission =  driver.find_element_by_xpath("//*[starts-with(@id,'right-sidebar')]//div[contains(.,'Select department/user')]//following-sibling::div//label[contains(.,'" + str(x) + "')]/preceding-sibling::input")
                if manager_permission.is_selected():
                    Logging("=> Correct permission")
            except:
                Logging("=> Wrong permission")

            driver.find_element_by_xpath("//*[starts-with(@id,'right-sidebar')][1]//div[contains(@class,'close-btn')]").click()

            driver.find_element_by_xpath("//span[contains(@ref,'eCellValue')]//div[contains(@class,'btn-view-detail')][2]").click()
            Logging("- Delete Dept. Manager")
            time.sleep(2)
            driver.find_element_by_xpath("//button/span[contains(@data-lang-id, 'tc_action_delete')]").click()
            Logging("- Click Delete button")
    else:
        driver.find_element_by_xpath("//*[starts-with(@id,'right-sidebar')]//div[contains(.,'Manager Settings')]//button[contains(.,'Save')]").click()
        Logging("save")
        time.sleep(3)
        try:
            error = driver.find_element_by_xpath("//*[starts-with(@id,'noty_bar')]//div[contains(text(),'Duplicate data exists.')]")
            if error.is_displayed():
                Logging("=> Duplicate data exists")
                driver.find_element_by_xpath("//*[starts-with(@id,'right-sidebar')][2]//div[contains(@class,'close-btn')]").click()
                time.sleep(3)
                search = driver.find_element_by_xpath("//div[@class='basic_setting']//div[contains(@class,'input-group')]//input")
                search.send_keys(data["name_keyword"][1])
                search.send_keys(Keys.ENTER)
                time.sleep(2)

                slider = driver.find_element_by_xpath("//div[@ref='eBodyHorizontalScrollViewport']")
                horizontal_bar = driver.find_element_by_xpath("//div[@ref='eHorizontalRightSpacer']")

                webdriver.ActionChains(driver).click_and_hold(slider).move_to_element(horizontal_bar).perform()
                webdriver.ActionChains(driver).release().perform()
                time.sleep(2)
                driver.find_element_by_xpath("//span[contains(@ref,'eCellValue')]//div[contains(@class,'btn-view-detail')][2]").click()
                Logging("- Delete Dept. Manager")
                time.sleep(2)
                driver.find_element_by_xpath("//button/span[contains(@data-lang-id, 'tc_action_delete')]").click()
                Logging("- Click Delete button")
        except:
            Logging("=> Save manager successfully")
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["add_manager"]["pass"])
            time.sleep(3)
            search = driver.find_element_by_xpath("//div[@class='basic_setting']//div[contains(@class,'input-group')]//input")
            search.send_keys(data["name_keyword"][1])
            search.send_keys(Keys.ENTER)
            time.sleep(2)

            slider = driver.find_element_by_xpath("//div[@ref='eBodyHorizontalScrollViewport']")
            horizontal_bar = driver.find_element_by_xpath("//div[@ref='eHorizontalRightSpacer']")

            webdriver.ActionChains(driver).click_and_hold(slider).move_to_element(horizontal_bar).perform()
            webdriver.ActionChains(driver).release().perform()
            time.sleep(2)

            driver.find_element_by_xpath("//span[contains(@ref,'eCellValue')]//div[contains(@class,'btn-view-detail')][1]").click()
            Logging("- View detail")
            time.sleep(2)

            try:
                manager_permission =  driver.find_element_by_xpath("//*[starts-with(@id,'right-sidebar')]//div[contains(.,'Select department/user')]//following-sibling::div//label[contains(.,'" + str(x) + "')]/preceding-sibling::input")
                if manager_permission.is_selected():
                    Logging("=> Correct permission")
            except:
                Logging("=> Wrong permission")

            driver.find_element_by_xpath("//*[starts-with(@id,'right-sidebar')][1]//div[contains(@class,'close-btn')]").click()

            driver.find_element_by_xpath("//span[contains(@ref,'eCellValue')]//div[contains(@class,'btn-view-detail')][2]").click()
            Logging("- Delete Dept. Manager")
            time.sleep(2)
            driver.find_element_by_xpath("//button/span[contains(@data-lang-id, 'tc_action_delete')]").click()
            Logging("- Click Delete button")

    time.sleep(2)
    try:
        notice_success =  driver.find_element_by_xpath("//*[starts-with(@id,'noty_bar')]//div[contains(text(),'Delete success')]")
        if notice_success.is_displayed():
            Logging("=> Delete Dept. Manager Successfully")
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["delete_manager"]["pass"])
    except:
        Logging("=> Delete Dept. Manager Fail")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["delete_manager"]["fail"])

    time.sleep(3)

def total_manager():
    manager = driver.find_element_by_xpath(data["TIMECARD"]["manager"])
    manager.location_once_scrolled_into_view
    manager.click()
    Logging("- Settings: Manager")
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='basic_setting']//form//div[1]/div[2]/div[1]")))
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='app']//a[contains(@href,'/nhr/hr/timecard/admin/manager/admin')]/span").click()
    Logging("- Total manager")
    time.sleep(2)

    search_total_manager = driver.find_element_by_xpath("//*[@id='org-form-search']//input[@placeholder='Search Name']")
    search_total_manager.send_keys(data["name_keyword"][1])
    search_total_manager.send_keys(Keys.ENTER)

    time.sleep(5)
    name_manager = driver.find_element_by_xpath("//*[starts-with(@id,'ft-id')]//span/span[@class='fancytree-title']")
    name_manager.click()
    driver.find_element_by_xpath("//*[@data-lang-id='tc_action_add']").click()
    time.sleep(3)

    try:
        notice =  driver.find_element_by_xpath("//*[starts-with(@id,'noty_bar')]//div[contains(@class,'alert-body')]")
        if notice.text == "There is duplicated data, please try again":
            Logging("=> Duplicate data exists")
        elif notice.text == "Data saved successfully.":
            Logging("=> Add Timecard Manager Successfully")
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["add_total_manager"]["pass"])
    except:
        Logging("=> Add Timecard Manager Fail")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["add_total_manager"]["fail"])

    add_name_manager = driver.find_element_by_xpath("//span[text()='Managers']//following::div//ul//li//div[contains(@class,'first-line') and contains(.,'" + str(name_manager.text) + "')]")
    if add_name_manager.is_displayed():
        Logging("- User " + str(name_manager.text) + " display in custom ORG tree")
        add_name_manager.click()
        driver.find_element_by_xpath("//span[text()='Managers']//following::div//ul//li//div[contains(@class,'first-line') and contains(.,'" + str(name_manager.text) + "')]//following::div[2]").click()
        Logging("- Delete Timecard Manager")
        driver.find_element_by_xpath("//button/span[contains(@data-lang-id, 'tc_action_delete')]").click()
        Logging("- Click Delete button")

        time.sleep(2)
        try:
            notice_success =  driver.find_element_by_xpath("//*[starts-with(@id,'noty_bar')]//div[contains(text(),'Data deleted successfully.')]")
            if notice_success.is_displayed():
                Logging("=> Delete Timecard Manager Successfully")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["delete_total_manager"]["pass"])
        except:
            Logging("=> Delete Timecard Manager Fail")
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["delete_total_manager"]["fail"])
    else:
        Logging("- User " + str(name_manager.text) + " don't display in custom ORG tree")

def find_date(today_work_date):
    driver.find_element_by_xpath("//*[starts-with(@id,'left-menu')]//span[contains(@data-lang-id,'tc_schedule_work_schedule')]").click()
    print("- Work schedule")
    time.sleep(3)
    calendar_date = int(len(driver.find_elements_by_xpath("//*[@class='work-schedule-container']//div[@class='row']/div")))

    list_date = []
    i = 0
    for i in range(calendar_date):
        i += 1
        if i % 8 != 0:
            try:
                icon_layer = driver.find_element_by_xpath("//*[@class='row']/div[" + str(i) + "]/div[starts-with(@id,'selectableItem')]/div//div[@class='cursor-pointer']/div/div[1]/*[starts-with(@id,'Layer')]")
                if icon_layer.is_displayed():
                    date_work = driver.find_element_by_xpath("//*[@class='row']/div[" + str(i) + "]/div[starts-with(@id,'selectableItem')]/div/div[1]/span")
                    if date_work.text > str(today_work_date):
                        list_date.append(date_work.text)
                    else:
                        continue
                else:
                    continue
            except:
                pass
        else:
            continue

    print("- Total of date: " + str(len(list_date)))
    #print(list_date)

    if len(list_date) >= 2:
        for x in list_date[0::]:
            date_work_up = driver.find_element_by_xpath("//*[@class='row']/div/div[starts-with(@id,'selectableItem')]/div/div[1]/span[contains(.,'" + str(x) + "')]")
            #print(date_work_up.text)
            date_work_update = int(date_work_up.text)

            for y in list_date[1::]:
                date_work_up1 = driver.find_element_by_xpath("//*[@class='row']/div/div[starts-with(@id,'selectableItem')]/div/div[1]/span[contains(.,'" + str(y) + "')]")
                #print(date_work_up1.text)
                date_work_update1 = int(date_work_up1.text)

                day_list = []
                if date_work_update == date_work_update1 - 1:
                    date_update = driver.find_element_by_xpath("//*[@class='row']/div/div[starts-with(@id,'selectableItem')]/div/div[1]/span[contains(.,'" + str(x) + "')]/../../..")
                    date_update_get = date_update.get_attribute("id")
                    date_update1 = driver.find_element_by_xpath("//*[@class='row']/div/div[starts-with(@id,'selectableItem')]/div/div[1]/span[contains(.,'" + str(y) + "')]/../../..")
                    date_update1_get = date_update1.get_attribute("id")
                    day_list.append(date_update_get)
                    day_list.append(date_update1_get)
                    print("- Find two days in a row")
                    time.sleep(2)
                    date_from = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='row']/div/div[starts-with(@id,'" + str(day_list[0]) + "')]")))
                    editor_to = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='row']/div/div[starts-with(@id,'" + str(day_list[1]) + "')]")))
                    webdriver.ActionChains(driver).drag_and_drop(date_from,editor_to).perform()
                    #print(day_list)
                    return day_list
                    break
                else:
                    print("- No two days in a row")

    elif len(list_date) == 1:
        print("- No two days in a row")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='row']/div/div[starts-with(@id,'" + str(day_list[0]) + "')]"))).click()
        print("- Select date")

    else:
        print("- No more date to selected in this month")
        driver.find_element_by_xpath("//*[@id='app']//div[@class='work-schedule-wrapper']//div[contains(@class,'month-navigation')]//*[contains(@class,'feather-chevron-right')]").click()
        print("- View next month")
        time.sleep(2)
        calendar_date = int(len(driver.find_elements_by_xpath("//*[@class='work-schedule-container']//div[@class='row']/div")))

        list_date = []
        i = 0
        for i in range(calendar_date):
            i += 1
            if i % 8 != 0:
                try:
                    icon_layer = driver.find_element_by_xpath("//*[@class='row']/div[" + str(i) + "]/div[starts-with(@id,'selectableItem')]/div//div[@class='cursor-pointer']/div/div[1]/*[starts-with(@id,'Layer')]")
                    if icon_layer.is_displayed():
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='row']/div[" + str(i) + "]/div[starts-with(@id,'selectableItem')]/div//div[@class='cursor-pointer']/div/div[1]/*[starts-with(@id,'Layer')]"))).click()
                        print("- Select date")
                        break
                    else:
                        continue
                except:
                    pass
            else:
                continue

def work_schedule(day_list):
    clockin_time = driver.find_element_by_xpath("//span[contains(.,'Clock-In Time')]/../following-sibling::div//div[starts-with(@id,'dropTimeWrapper')]//button[starts-with(@id,'btnHours')]")
    clockin_time_num = int(clockin_time.text)
    clockin_time.click()

    clockout_time = driver.find_element_by_xpath("//span[contains(.,'Estimated Clock Out')]/../following-sibling::div/span")
    clockin_time_num = int(clockin_time.text[::1])

    clockin_time_update = clockin_time_num + 1
    driver.find_element_by_xpath("//span[contains(.,'Clock-In Time')]/../following-sibling::div//div[starts-with(@id,'dropTimeWrapper')]//button[starts-with(@id,'btnHours')]/following-sibling::div/button[contains(.,'" + str(clockin_time_update) + "')]").click()

    clockin_time_up = driver.find_element_by_xpath("//span[contains(.,'Clock-In Time')]/../following-sibling::div//div[starts-with(@id,'dropTimeWrapper')]//button[starts-with(@id,'btnHours')]")
    if int(clockin_time_up.text) == clockin_time_update:
        Logging("- Change time clock in successfully")
    else:
        Logging("- Change time clock in fail")

    clockout_time_up = driver.find_element_by_xpath("//span[contains(.,'Estimated Clock Out')]/../following-sibling::div/span")
    clockin_time_num_up = int(clockin_time.text[::1])
    if int(clockin_time_num) + 1 == int(clockin_time_num_up):
        Logging("- Change time successfully")
    else:
        Logging("- Change time fail")

    time.sleep(2)
    driver.find_element_by_xpath("//span[contains(@data-lang-id,'vc_title_request')]").click()
    Logging("- Request Work Schedule")
    time.sleep(3)
    
    try:
        noty_success = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["pre_OT_noty"])))
        noty_event_list = [data["TIMECARD"]["noty_event"][0], data["TIMECARD"]["noty_event"][1]]
        if noty_success.text in noty_event_list:
            Logging("- Request Work Schedule Successfully -> Approval is submitted successfully")
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["work_scheduless"]["pass"])
            time.sleep(2)
            driver.find_element_by_xpath("//*[@id='timecard-tab']//li/a[contains(@href,'/nhr/hr/timecard/company/approval')]").click()
            Logging("- Company timecard: Timecard")
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='table-approval']//div[@ref='eBodyViewport']//div[contains(@col-id,'user_id')]")))
            time.sleep(1)

            driver.find_element_by_xpath("//*[@id='app']//div[@class='company-approval-content']//div[@class='pos-absolute']/div/div[1]/*[1]").click()
            search_user = driver.find_element_by_xpath("//div[@class='company-approval-content']//span[@class='input-group-prepend']/following-sibling::input")
            search_user.send_keys(data["name_keyword"][0])
            search_user.send_keys(Keys.ENTER)
            Logging("- Show ORG successfully")
            time.sleep(1)

            driver.find_element_by_xpath("//*[starts-with(@id,'tree-container')]//ul//li[1]").click()
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='table-approval']//div[@ref='eBodyViewport']//div[contains(@col-id,'user_id')]")))
            time.sleep(2)
            driver.find_element_by_xpath("//*[@id='app']//div[@class='company-approval-content']//div[@class='pos-absolute']/div/div[1]/*[1]").click()
            driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]/following-sibling::div//div[2]//span/following-sibling::div").click()
            type_approval = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]/following-sibling::div//div[contains(text(),'All')]/following-sibling::div//input")
            type_approval.send_keys(Keys.ARROW_DOWN)
            type_approval.send_keys(Keys.ARROW_DOWN)
            type_approval.send_keys(Keys.ARROW_DOWN)
            type_approval.send_keys(Keys.ENTER)
            Logging("- Select Type approval")
            time.sleep(1)

            driver.find_element_by_xpath("//div[contains(@data-lang-id,'vc_title_period')]/following-sibling::div//div[2]//span/following-sibling::div").click()
            period_approval = driver.find_element_by_xpath("//div[contains(@data-lang-id,'vc_title_period')]/following-sibling::div//div[contains(text(),'All-Time')]/following-sibling::div//input")
            period_approval.send_keys(Keys.ARROW_DOWN)
            period_approval.send_keys(Keys.ENTER)
            Logging("- Select Period approval")
            time.sleep(1)

            #view detail
            wp_status_approve = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
            #Logging (status_approve.text)
            if wp_status_approve.is_displayed():
                Logging (wp_status_approve.text)
                if wp_status_approve.text == "Work Plan":
                    Logging ("- Work Schedule approval is displayed in approval list")
                else:
                    Logging ("- Work Schedule approval is not displayed in approval list")
            else: 
                Logging ("- Work Schedule approval is submitted failed")
        else:
            Logging("- Request Work Schedule Fail -> Approval is submitted fail")
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["work_scheduless"]["fail"])

    except:
        Logging("- Request Work Schedule Fail -> Approval is submitted fail")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["work_scheduless"]["fail"])


def work_correction():
    #Logout
    time.sleep(4)
    driver.find_element_by_xpath("//div[contains(@data-tooltip, 'Logout')]").click()
    #Log in to user acc
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "gw_id")))
    userID = driver.find_element_by_name("gw_id")
    #userID.send_keys("luu")
    userID.send_keys("automationtest2")
    Logging("- Input user ID")
    #add_data_in_excel(param_excel["checkin"],"p","Input reason late")
    password = driver.find_element_by_name("gw_pass")
    #password.send_keys("matkhau1!")
    password.send_keys(data["user_password"])
    Logging("- Input user password")
    driver.find_element_by_xpath(data["TIMECARD"]["sign_in"]).click()
    Logging("- Click button Sign in")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["notify"][0])))
    Logging("=> Log in successfully")
    time.sleep(2)
    driver.refresh()

    #Clock-in
    try:
        tardiness = driver.find_element_by_xpath(data["TIMECARD"]["tardiness"])
        if tardiness.is_displayed():
            driver.find_element_by_xpath(data["TIMECARD"]["input_reason_late"]).send_keys(data["TIMECARD"]["reason_late"])
            Logging("- Input reason late")
            #add_data_in_excel(param_excel["checkin"],"f","Input reason late")
            driver.find_element_by_xpath(data["TIMECARD"]["save"]).click()
            Logging("- Save reason late")
            #add_data_in_excel(param_excel["checkout"],"p","Save reason late")
            time_clock_in()
    except:
        Logging("- Clock-in on time")

    try:
        #pop up clock-in display
        pop_up = driver.find_element_by_xpath(data["TIMECARD"]["pop_up"])
        time.sleep(1)
        if pop_up.is_displayed():
            try:
                clock_in_but = driver.find_element_by_xpath(data["TIMECARD"]["clock_in_but"])
                clock_in_but.click()
                Logging("- Clock-in")
                time.sleep(5)
                input_reason_late()
            except:
                Logging("- Clock-in already")
            
    except:
        #pop up clock-in don't display
        pop_up_hid = driver.find_element_by_xpath(data["TIMECARD"]["pop_up_hid"])
        pop_up_hid.click()
        Logging("- Click show pop up")
        time.sleep(2)
        pop_up = driver.find_element_by_xpath(data["TIMECARD"]["pop_up"])
        if pop_up.is_displayed():
            try:
                clock_in_but = driver.find_element_by_xpath(data["TIMECARD"]["clock_in_but"])
                clock_in_but.click()
                Logging("- Clock-in")
                time.sleep(5)
                input_reason_late()
            except:
                Logging("- Clock-in already")


    #Request work correction
    try:
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Timesheets')]").click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Break time')] ")))
    except:
        Logging("")

    clockout_scroll = driver.find_element_by_xpath("//div[contains(@class, 'timeline-item  ')]//div[contains(.,'Clock-In')]//div[contains(@class, 'd-flex ')]//span[contains(.,'Request for correction')]")
    clockout_scroll.location_once_scrolled_into_view
    time.sleep(2)
    try:
        work_correction_status = driver.find_element_by_xpath("//div[contains(@class, 'timeline-item  ')]//div[contains(.,'Clock-In')]//div[contains(@class, 'd-flex ')]//span[contains(.,'Request for correction')]")
        if work_correction_status.is_displayed():
            driver.find_element_by_xpath("//div[contains(@class, 'timeline-item  ')]//div[contains(.,'Clock-In')]//div[contains(@class, 'd-flex ')]//span[contains(.,'Request for correction')]").click()
            time.sleep(3)
            driver.find_element_by_xpath("//div[contains(@data-lang-id, 'tc_title_status')]/..//button").click()
            driver.find_element_by_xpath("//span[contains(@data-lang-id, 'On Time')]").click()
            time_work_correction = driver.find_element_by_xpath("//button[starts-with(@id, 'btnHours')]").click()
            time.sleep(5)
            hour_work_correction = driver.find_element_by_xpath("//div[starts-with(@id, 'dropdown')]//div//button[contains(.,'08')]").click()
            time_work_correction1 = driver.find_element_by_xpath("//button[starts-with(@id, 'btnMin')]").click()
            time.sleep(3)
            minute_work_correction = driver.find_element_by_xpath("//div[starts-with(@id, 'dropdown')]//button[starts-with(@id, 'btnMin')]//following-sibling::div//button[contains(.,'00')]").click()
            #Save
            driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_action_save')]").click()
            Logging("Request work correction succesfully -> Approval is submitted successfullu")
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["work_correction"]["pass"])
            time.sleep(3)
            #Log in to admin acc
            driver.find_element_by_xpath("//div[contains(@data-tooltip, 'Logout')]").click()
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "gw_id")))
            userID = driver.find_element_by_name("gw_id")
            #userID.send_keys("luu")
            userID.send_keys(data["name_keyword"][0])
            print("- Input user ID")
            #add_data_in_excel(param_excel["checkin"],"p","Input reason late")
            password = driver.find_element_by_name("gw_pass")
            #password.send_keys("matkhau1!")
            password.send_keys(data["user_password"])
            print("- Input user password")
            driver.find_element_by_xpath(data["TIMECARD"]["sign_in"]).click()
            print("- Click button Sign in")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["notify"][0])))
            print("=> Log in successfully")
            #add_data_in_excel(param_excel["checkin"],"p","Log in successfully")
            time.sleep(2)
            driver.refresh()
            time.sleep(5)
            #Approval page
            approval_page = driver.find_element_by_xpath("//li//a[contains(@href,'/nhr/hr/timecard/user/approval')]//span[contains(@data-lang-id, 'tc_approval_approval')]").click()
            
            wc_status_approve = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
            #Logging (status_approve.text)
            if wc_status_approve.is_displayed():
                #Logging (wc_status_approve.text)
                if wc_status_approve.text == "Clock in/out":
                    Logging ("- Work corection approval is displayed in approval list")
                    #Scroll to detail
                    slider = driver.find_element_by_xpath("//div[@ref='eBodyHorizontalScrollViewport']")
                    horizontal_bar = driver.find_element_by_xpath("//div[@ref='eHorizontalRightSpacer']")
                    webdriver.ActionChains(driver).click_and_hold(slider).move_to_element(horizontal_bar).perform()
                    webdriver.ActionChains(driver).release().perform()
                    #Logging ("Scroll successfully")
                    #Click view details
                    driver.find_element_by_xpath("//div[1]/*[@col-id='id']//div[contains(@class, 'btn-view-detail')]").click()
                    time.sleep(5)
                    #Print status column
                    work_corection_status_app = driver.find_element_by_xpath("//div[contains(@class, 'avatar-wrapper')]/..//div[contains(@class, 'approval-status')]")
                    ab = work_corection_status_app.text
                    time.sleep(3)
                    if ab == "Pending":
                        Logging ("- Status is not changed => Approve failed")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["approve_status_work"]["fail"])
                    elif ab != "Pending":
                        Logging ("- Status is changed => Approve successfully")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["approve_status_work"]["pass"])
                else:
                    Logging ("- Work corection approval is not displayed in approval list")
            else: 
                Logging ("- Work corection approval is submitted failed")
        else:
            Logging("- Request work correction failed")
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["work_correction"]["fail"])
    except:
        Logging("- Request work correction failed")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["work_correction"]["fail"])







def delete_punch():
    
    driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Timeline')]").click()
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Filters')] ")))
    time.sleep(2)

    filters_input_dashboard_del = driver.find_element_by_xpath("//input[starts-with(@id, 'react-select')]")
    filters_input_dashboard_del.send_keys(Keys.ARROW_DOWN)
    filters_input_dashboard_del.send_keys(Keys.ENTER)
    time.sleep(3)
    driver.find_element_by_xpath("//div[contains(@class, 'timeline-item  ')]//div[contains(.,'Clock-In')]//div[contains(@class, 'd-flex ')]//span[2]//div[contains(@class, 'cursor-pointer')]").click()
    driver.find_element_by_xpath("//button//span[contains(.,'Delete')] ").click()
    Logging("Delete punch-in successfully")
    driver.refresh()

#---------------------------------------------------------------------------------------#

def weekly_status():
    try:
        Logging("")
        #Logging("***Weekly Status - Default***")    
        Logging(yellow('***Weekly Status - Default***', 'bold'))    
        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Weekly Status')]").click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Name')] ")))
        Logging("Access page successfully")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["access_weekly_status_page"]["pass"])
    except:
        Logging("Access page fail")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["access_weekly_status_page"]["fail"])

    try:
        driver.find_element_by_xpath("//div[contains(@class,'company-status-setting')]/div/div[2]/div/div[1]").click()
        ws_search = driver.find_element_by_xpath("//input[contains(@class,'form-control')]")
        ws_search.send_keys(data["name_keyword"][0])
        ws_search.send_keys(Keys.ENTER)
        time.sleep(5)
        driver.find_element_by_xpath("//div[contains(@class,'visible')]//li").click()
        driver.find_element_by_xpath("//div[contains(@class,'company-status-setting')]/div/div[2]/div/div[1]").click()
        time.sleep(3)

        avg_clockin = driver.find_element_by_xpath("//div[contains(@class,'ag-center-cols-viewport')]//span[contains(@class,'td-avg-clock-in')]")
        Logging("avg.clockin: " + avg_clockin.text)

        avg_clockout = driver.find_element_by_xpath("//div[contains(@class,'ag-center-cols-viewport')]//span[contains(@class,'td-avg-clock-out')]")
        Logging("avg_clockout: " + avg_clockout.text)

        avg_working_time = driver.find_element_by_xpath("//div[contains(@class,'ag-center-cols-viewport')]//span[contains(@class,'td-avg-work-hour')]")
        Logging("avg_working time: " + avg_working_time.text)

        time.sleep(5)
        monday = driver.find_element_by_xpath("//*[@col-id='day_0']//div[contains(@class,'cursor-pointer')]/span")
        time.sleep(3)
        Logging("monday before change to decimal: " + monday.text)
        monday_time = monday.text
        time.sleep(3)
        try:
            minute_monday_time = monday_time.split(" ")[1]
            minutes_monday_time = minute_monday_time.split("m")[0]
            minutes_number_monday_time = int(minutes_monday_time)
            #Logging(minutes_number_monday_time)
            hour_monday_time = monday_time.split(" ")[0]
            #Logging(hour_monday_time)
            hours_monday_time = hour_monday_time.split("H")[0]
            hour_number_monday_time = int(hours_monday_time)
            #Logging(hour_number_monday_time)
            monday_time_decimal = ((minutes_number_monday_time) / 60) + (hour_number_monday_time)
            #Logging("monday after change to decimal: " + str(monday_time_decimal))
            Logging("monday after change to decimal: " + str(round(monday_time_decimal, 2)))
        except:
            hour_monday_time = monday_time.split(" ")[0]
            #Logging(hour_monday_time)
            hours_monday_time = hour_monday_time.split("H")[0]
            hour_number_monday_time = int(hours_monday_time)
            #Logging(hour_number_monday_time)
            monday_time_decimal = hour_number_monday_time
            Logging("monday after change to decimal: " + str(monday_time_decimal))

        tuesday = driver.find_element_by_xpath("//*[@col-id='day_1']//div[contains(@class,'cursor-pointer')]/span")
        Logging("tuesday before change to decimal: " + tuesday.text)
        tuesday_time = tuesday.text
        try:
            minute_tuesday_time = tuesday_time.split(" ")[1]
            minutes_tuesday_time = minute_tuesday_time.split("m")[0]
            minutes_number_tuesday_time = int(minutes_tuesday_time)
            #Logging(minutes_number_tuesday_time)
            hour_tuesday_time = tuesday_time.split(" ")[0]
            #Logging(hour_tuesday_time)
            hours_tuesday_time = hour_tuesday_time.split("H")[0]
            hour_number_tuesday_time = int(hours_tuesday_time)
            #Logging(hour_number_tuesday_time)
            tuesday_time_decimal = ((minutes_number_tuesday_time) / 60) + (hour_number_tuesday_time)
            #Logging("tuesday after change to decimal: " + str(tuesday_time_decimal))
            Logging("tuesday after change to decimal: " + str(round(tuesday_time_decimal, 2)))
        except:
            hour_tuesday_time = tuesday_time.split(" ")[0]
            #Logging(hour_tuesday_time)
            hours_tuesday_time = hour_tuesday_time.split("H")[0]
            hour_number_tuesday_time = int(hours_tuesday_time)
            #Logging(hour_number_tuesday_time)
            tuesday_time_decimal = hour_number_tuesday_time
            Logging("tuesday after change to decimal: " + str(tuesday_time_decimal))

        wednesday = driver.find_element_by_xpath("//*[@col-id='day_2']//div[contains(@class,'cursor-pointer')]/span")
        Logging("wednesday before change to decimal: " + wednesday.text)
        wednesday_time = wednesday.text
        try:
            minute_wednesday_time = wednesday_time.split(" ")[1]
            minutes_wednesday_time = minute_wednesday_time.split("m")[0]
            minutes_number_wednesday_time = int(minutes_wednesday_time)
            #Logging(minutes_number_wednesday_time)
            hour_wednesday_time = wednesday_time.split(" ")[0]
            #Logging(hour_wednesday_time)
            hours_wednesday_time = hour_wednesday_time.split("H")[0]
            hour_number_wednesday_time = int(hours_wednesday_time)
            #Logging(hour_number_wednesday_time)
            wednesday_time_decimal = ((minutes_number_wednesday_time) / 60) + (hour_number_wednesday_time)
            #Logging("wednesday after change to decimal: " + str(wednesday_time_decimal))
            Logging("wednesday after change to decimal: " + str(round(wednesday_time_decimal, 2)))
        except:
            hour_wednesday_time = wednesday_time.split(" ")[0]
            #Logging(hour_wednesday_time)
            hours_wednesday_time = hour_wednesday_time.split("H")[0]
            hour_number_wednesday_time = int(hours_wednesday_time)
            #Logging(hour_number_wednesday_time)
            wednesday_time_decimal = hour_number_wednesday_time
            Logging("wednesday after change to decimal: " + str(wednesday_time_decimal))

        thursday = driver.find_element_by_xpath("//*[@col-id='day_3']//div[contains(@class,'cursor-pointer')]/span")
        Logging("thursday before change to decimal: " + thursday.text)
        thursday_time = thursday.text
        try:
            minute_thursday_time = thursday_time.split(" ")[1]
            minutes_thursday_time = minute_thursday_time.split("m")[0]
            minutes_number_thursday_time = int(minutes_thursday_time)
            #Logging(minutes_number_thursday_time)
            hour_thursday_time = thursday_time.split(" ")[0]
            #Logging(hour_thursday_time)
            hours_thursday_time = hour_thursday_time.split("H")[0]
            hour_number_thursday_time = int(hours_thursday_time)
            #Logging(hour_number_thursday_time)
            thursday_time_decimal = ((minutes_number_thursday_time) / 60) + (hour_number_thursday_time)
            #Logging("thursday after change to decimal: " + str(thursday_time_decimal))
            Logging("thursday after change to decimal: " + str(round(thursday_time_decimal, 2)))
        except:
            hour_thursday_time = thursday_time.split(" ")[0]
            #Logging(hour_thursday_time)
            hours_thursday_time = hour_thursday_time.split("H")[0]
            hour_number_thursday_time = int(hours_thursday_time)
            #Logging(hour_number_thursday_time)
            thursday_time_decimal = hour_number_thursday_time
            Logging("thursday after change to decimal: " + str(thursday_time_decimal))

        friday = driver.find_element_by_xpath("//*[@col-id='day_4']//div[contains(@class,'cursor-pointer')]/span")
        Logging("friday before change to decimal: " + friday.text)
        friday_time = friday.text
        try:
            minute_friday_time = friday_time.split(" ")[1]
            minutes_friday_time = minute_friday_time.split("m")[0]
            minutes_number_friday_time = int(minutes_friday_time)
            #Logging(minutes_number_friday_time)
            hour_friday_time = friday_time.split(" ")[0]
            #Logging(hour_friday_time)
            hours_friday_time = hour_friday_time.split("H")[0]
            hour_number_friday_time = int(hours_friday_time)
            #Logging(hour_number_friday_time)
            friday_time_decimal = ((minutes_number_friday_time) / 60) + (hour_number_friday_time)
            #Logging("friday after change to decimal: " + str(friday_time_decimal))
            Logging("friday after change to decimal: " + str(round(friday_time_decimal, 2)))
        except:
            hour_friday_time = friday_time.split(" ")[0]
            #Logging(hour_friday_time)
            hours_friday_time = hour_friday_time.split("H")[0]
            hour_number_friday_time = int(hours_friday_time)
            #Logging(hour_number_friday_time)
            friday_time_decimal = hour_number_friday_time
            Logging("friday after change to decimal: " + str(friday_time_decimal))

        saturday = driver.find_element_by_xpath("//*[@col-id='day_5']//div[contains(@class,'cursor-pointer')]/span")
        Logging("saturday before change to decimal: " + saturday.text)
        saturday_time = saturday.text
        try:
            minute_saturday_time = saturday_time.split(" ")[1]
            minutes_saturday_time = minute_saturday_time.split("m")[0]
            minutes_number_saturday_time = int(minutes_saturday_time)
            #Logging(minutes_number_saturday_time)
            hour_saturday_time = saturday_time.split(" ")[0]
            #Logging(hour_saturday_time)
            hours_saturday_time = hour_saturday_time.split("H")[0]
            hour_number_saturday_time = int(hours_saturday_time)
            #Logging(hour_number_saturday_time)
            saturday_time_decimal = ((minutes_number_saturday_time) / 60) + (hour_number_saturday_time)
            #Logging("saturday after change to decimal: " + str(saturday_time_decimal))
            Logging("saturday after change to decimal: " + str(round(saturday_time_decimal, 2)))
        except:
            hour_saturday_time = saturday_time.split(" ")[0]
            #Logging(hour_saturday_time)
            hours_saturday_time = hour_saturday_time.split("H")[0]
            hour_number_saturday_time = int(hours_saturday_time)
            #Logging(hour_number_saturday_time)
            saturday_time_decimal = hour_number_saturday_time
            Logging("saturday after change to decimal: " + str(saturday_time_decimal))

        sunday = driver.find_element_by_xpath("//*[@col-id='day_6']//div[contains(@class,'cursor-pointer')]/span")
        Logging("sunday: " + sunday.text)

        total = driver.find_element_by_xpath("//span[contains(@class,'td-sum-of-time')]")
        Logging("total: " + total.text)
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["weekly_status_data"]["pass"])
    except:
        #Logging("Check data fail")
        Logging(red('>>>Check data failed', 'bright')) 
        

def daily_status():
    try:
        #Before login
        Logging("")
        #Logging("*** Daily Status - Default***")
        Logging(yellow('***Daily Status - Default***', 'bold')) 

        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Daily Status')]").click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Name')] ")))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["access_daily_status_page"]["pass"])
        try:
            Logging("***Download Excel File***")
            driver.find_element_by_xpath("//div[contains(@class,'han-content-wrapper')]//div[4]//button[contains(@class,'outline-white')]").click()
            time.sleep(10)
            if '2022' in driver.page_source:
                #Logging ("Download file succcessfully")
                Logging(green('>>>Download file succcessfully', 'bright')) 
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["download_excel_file"]["pass"])
            else:
                #Logging ("Download file failed")
                Logging(red('>>>Download file failed', 'bright')) 
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["download_excel_file"]["fail"])
        except:
            #Logging ("Download file failed")
            Logging(red('>>>Download file failed', 'bright')) 
            
        time.sleep(10)
    except:
        Logging("Access page fail")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["access_daily_status_page"]["fail"])

    try:
        Logging("")
        driver.find_element_by_xpath("//div[contains(@class,'company-time-card-real-time')]/div/div[2]/div/div[1]").click()
        search = driver.find_element_by_xpath("//input[contains(@class,'form-control')]")
        search.send_keys(data["name_keyword"][0])
        search.send_keys(Keys.ENTER)
        time.sleep(5)
        driver.find_element_by_xpath("//div[contains(@class,'visible')]//li").click()
        driver.find_element_by_xpath("//div[contains(@class,'company-time-card-real-time')]/div/div[2]/div/div[1]").click()

        time.sleep(5)
        work_status = driver.find_element_by_xpath("//div[contains(@class,'label-rounded')]")
        Logging("work status: " + work_status.text)
        status1 = work_status.text

        dailystatus_clockin = driver.find_element_by_xpath("//div[contains(@class,'ag-center-cols-viewport')]//*[@col-id='clock_in_title']/div[1]")
        Logging("clock-in: " + dailystatus_clockin.text)

        dailystatus_clockout = driver.find_element_by_xpath("//div[contains(@class,'ag-center-cols-viewport')]//*[@col-id='clock_out_title']")
        Logging("clock-out: " + dailystatus_clockout.text)

        dailystatus_breaktime = driver.find_element_by_xpath("//div[contains(@class,'ag-center-cols-viewport')]//*[@col-id='break_time']")
        Logging("break time: " + dailystatus_breaktime.text)

        achievement = driver.find_element_by_xpath("//div[contains(@class,'ag-center-cols-viewport')]//*[@col-id='cumulative_work_time_percent']/div[1]/div")
        Logging("achievement: " + achievement.text)

        estimate = driver.find_element_by_xpath("//div[contains(@class,'ag-center-cols-viewport')]//*[@col-id='over_time_since']/div[1]/div")
        Logging("estimate: " + estimate.text)
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["daily_status_data"]["pass"])

        return status1
    except:
        Logging (">>>Check data fail")
        #Logging(red('>>>Check data failed', 'bright')) 


def report():   
    try:
        time.sleep(3)
        rp =[]
        driver.find_element_by_xpath("//a[contains(@href,'/nhr/hr/timecard/user/statistics')]").click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Working status')] ")))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["access_daily_status_page"]["pass"])
    except:
        Logging (">>>Access page fail")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["access_daily_status_page"]["fail"])

    try:
        Logging("")
        #Logging("*** Report - Default***")
        Logging(yellow('***Report - Default***', 'bold')) 

        #workingtimeUI_number
        Logging("Change working time to decimal")
        time.sleep(5)
        working_time_report = driver.find_element_by_xpath("//span[contains(.,'Working status')]//following-sibling::div//li[1]//span[contains(.,'Working time')]/../../div[2]")
        Logging("working time: " +  working_time_report.text)
        working_time_report1 = working_time_report.text
        try:
            minute_time_report1 = working_time_report1.split(" ")[1]
            #Logging(minute_time_report1)
            minutes_report1 = minute_time_report1.split("m")[0]
            minutes_number_report1 = int(minutes_report1)
            #Logging(minutes_number_report1)

            hour_time_report1 = working_time_report1.split(" ")[0]
            #Logging(hour_time_report1)
            hour_report1 = hour_time_report1.split("H")[0]
            hour_number_report1 = int(hour_report1)
            #Logging(hour_number_report1)

            working_time_report_decimal = ((minutes_number_report1) / 60) + (hour_number_report1)
            rp.append(working_time_report_decimal)
            Logging("working time after change to decimal: " + str(round(working_time_report_decimal, 2)))
            #Logging("working time after change to decimal: " + str(working_time_report_decimal))
        except:
            hour_time_report1 = working_time_report1.split(" ")[0]
            #Logging(hour_time_report1)
            hour_report1 = hour_time_report1.split("H")[0]
            hour_number_report1 = int(hour_report1)
            #Logging(hour_number_report1)

            working_time_report_decimal = hour_number_report1
            rp.append(working_time_report_decimal)
            Logging("working time after change to decimal: " + str(working_time_report_decimal))

        #workedtimeUI_number
        Logging("Change worked time to decimal")
        time.sleep(5)
        worked_time_report = driver.find_element_by_xpath("//span[contains(.,'Working status')]//following-sibling::div//li[2]//span[contains(.,'Worked time')]/../../div[2]")
        Logging("worked time: " + worked_time_report.text)
        worked_time_report1 = worked_time_report.text
        try:
            minute_worked_time_report1 = worked_time_report1.split(" ")[1]
            #Logging(minute_worked_time_report1)
            minutes_worked_report1 = minute_worked_time_report1.split("m")[0]
            minutes_worked_number_report1 = int(minutes_worked_report1)
            #Logging(minutes_worked_number_report1)

            hour_worked_time_report1 = worked_time_report1.split(" ")[0]
            #Logging(hour_worked_time_report1)
            hour_worked_report1 = hour_worked_time_report1.split("H")[0]
            hour_worked_number_report1 = int(hour_worked_report1)
            #Logging(hour_worked_number_report1)

            worked_time_report_decimal = ((minutes_worked_number_report1) / 60) + (hour_worked_number_report1)
            rp.append(worked_time_report_decimal)
            Logging("worked time after change to decimal: " + str(round(worked_time_report_decimal, 2)))
            #Logging("worked time after change to decimal: " +  str(worked_time_report_decimal))
        except:
            hour_worked_time_report1 = worked_time_report1.split(" ")[0]
            #Logging(hour_worked_time_report1)
            hour_worked_report1 = hour_worked_time_report1.split("H")[0]
            hour_worked_number_report1 = int(hour_worked_report1)
            #Logging(hour_worked_number_report1)

            worked_time_report_decimal = hour_worked_number_report1
            rp.append(worked_time_report_decimal)
            Logging("worked time after change to decimal: " +  str(worked_time_report_decimal))

        #breaktimeUI_number
        Logging("Change break time to decimal")
        time.sleep(5)
        break_time_report = driver.find_element_by_xpath("//span[contains(.,'Working status')]//following-sibling::div//li[3]//span[contains(.,'Break time')]/../../div[2]")
        Logging("break time: " + break_time_report.text)
        break_time_report1 = break_time_report.text
        try:
            minute_break_time_report1 = break_time_report1.split(" ")[1]
            #Logging(minute_break_time_report1)
            minutes_break_report1 = minute_break_time_report1.split("m")[0]
            minutes_break_number_report1 = int(minutes_break_report1)
            #Logging(minutes_break_number_report1)

            hour_break_time_report1 = break_time_report1.split(" ")[0]
            #Logging(hour_break_time_report1)
            hour_break_report1 = hour_break_time_report1.split("H")[0]
            hour_break_number_report1 = int(hour_break_report1)
            #Logging(hour_break_number_report1)

            break_time_report_decimal = ((minutes_break_number_report1) / 60)  + (hour_break_number_report1)
            rp.append(break_time_report_decimal)
            Logging("break time after change to decimal: " + str(break_time_report_decimal))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["report_data"]["pass"])
            return rp
        except:
            hour_break_time_report1 = break_time_report1.split(" ")[0]
            #Logging(hour_break_time_report1)
            hour_break_report1 = hour_break_time_report1.split("H")[0]
            hour_break_number_report1 = int(hour_break_report1)
            #Logging(hour_break_number_report1)

            break_time_report_decimal = (hour_break_number_report1)
            rp.append(break_time_report_decimal)
            Logging("break time after change to decimal: " + str(break_time_report_decimal))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["report_data"]["pass"])
            return rp

    except:
        Logging ("Check data fail")
        #Logging(red('>>>Check data fail', 'bright')) 


def clockin():
    try:
        night_work = driver.find_element_by_xpath("//span[contains(.,'Confirm Nightwork')]")
        if night_work.is_displayed():
            driver.find_element_by_xpath("//span[contains(.,'Confirm Nightwork')]/..//button").click()
            time.sleep(3)
    except:
        Logging(" ")

    try:
        driver.find_element_by_xpath("//*[@id='0']").click()
        driver.find_element_by_xpath("//span[contains(.,'Clock-In')]").click()
        time.sleep(3)
        driver.find_element_by_xpath("//div[contains(@class,'modal-content')]//button[contains(@type,'button')]/span").click()
        time.sleep(3)
        Logging(" ")
        #Logging("clock in successfully")
        Logging(green('Clock in successfully', 'bright'))  
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["clockin_through_avatar"]["pass"])

    except:
        #Logging("clock in failed")
        Logging(red('Clock in failed', 'bright')) 
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["clockin_through_avatar"]["fail"])

def timesheet_calendar_check():
    driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Timesheets')]").click()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Break time')] ")))
    time.sleep(1)
    output_clock_in = driver.find_element_by_xpath("//div[contains(@class, 'content-body')]//div[contains(@class, 'header')]//div[contains(@class, 'check-in-status')]")
    Logging(">> Clock-in: " + output_clock_in.text)
    output_clockin = output_clock_in.text
    out_put_status = driver.find_element_by_xpath("//*[@id='app']/div/div[2]/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div[2]/div[4]/div/div/div[2]/nav/div[4]")
    time.sleep(5)
    Logging(">> Status: " + out_put_status.text)
    output_status = out_put_status.text
    time.sleep(1)
    driver.find_element_by_xpath(data["TIMECARD"]["calendar"]).click()
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["wait_calendar"])))
    time.sleep(5)
    #Find today's clockin
    today_clockin = driver.find_element_by_xpath("//span[contains(.,'" + output_status + " " + output_clockin + "')]")
    Logging(today_clockin.text)
    time.sleep(1)
    try:
        if today_clockin.is_displayed():
            today_clockin.click()
            clock_in_UI = driver.find_element_by_xpath("//div[contains(@class, 'content-body')]//div[contains(@class, 'header')]//div[contains(@class, 'check-in-status')]")
            if clock_in_UI.text == output_clockin():
                Logging ("Clock in time is correct")
            else:
                Logging ("Clock in time is wrong")
        else:
            Logging("Can't find date")
    except:
        Logging("Can't find date")
    

def clockout():
    try:
        time.sleep(5)
        driver.find_element_by_xpath("//*[@id='0']").click()
        driver.find_element_by_xpath("//span[contains(.,'Clock-Out')]").click()
        time.sleep(5)
        driver.find_element_by_xpath(data["TIMECARD"]["input_reason_leave_early"]).send_keys(data["TIMECARD"]["reason_leave_early"])
        time.sleep(2)
        driver.find_element_by_xpath(data["TIMECARD"]["save"]).click()
        #Logging("clock out successfully")
        Logging(green('Clock out successfully', 'bright'))  
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["clockout_through_avatar"]["pass"])
    except:
        #Logging("clock out failed")
        Logging(red('Clock out failed', 'bright')) 
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["clockout_through_avatar"]["fail"])


def edit_clockin():
    try:
        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Timesheets')]").click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Break time')] ")))

        Logging(" ")
        Logging("Edit clockin")
        time.sleep(5)
        #Click Edit
        Edit = driver.find_element_by_xpath("//div[contains(@class, 'admin_status')]//div[contains(@class, 'timeline-item  ')]//div[contains(.,'Clock-In')]//div[contains(@class, 'd-flex ')]//span[1]//div[contains(@class, 'cursor-pointer')]").click()
        time.sleep(5)
        Time = driver.find_element_by_xpath("//button[starts-with(@id, 'btnHours')]").click()
        time.sleep(5)
        Hour = driver.find_element_by_xpath("//div[starts-with(@id, 'dropdown')]//div//button[contains(.,'08')]").click()

        Time1 = driver.find_element_by_xpath("//button[starts-with(@id, 'btnMin')]").click()
        time.sleep(3)
        Minute = driver.find_element_by_xpath("//div[starts-with(@id, 'dropdown')]//button[starts-with(@id, 'btnMin')]//following-sibling::div//button[contains(.,'00')]").click()

        #Click On-time
        Status = driver.find_element_by_xpath("//span[contains(.,'On Time')]").click()

        #Input Memo
        Memo = driver.find_element_by_xpath("//div[contains(@class, 'modal-content')]//div[5]//textarea[contains(@name, 'memo')]").send_keys("test")
        #Logging("Input memo")

        #Save
        Save = driver.find_element_by_xpath("//span[contains(.,'Save')]").click()
        #Logging("Edit clockin successfully")    
        Logging(green('Edit clock in successfully', 'bright')) 
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["edit_clockin"]["pass"])

    except:
        #Logging("Edit clockin failed")   
        Logging(red('Edit clock in failed', 'bright')) 
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["edit_clockin"]["fail"])


def edit_clockout():
    try:
        Logging(" ")
        Logging("Edit clockout")
        nb_out=[]
        time.sleep(10)
        #Click Edit
        Edit = driver.find_element_by_xpath("//div[contains(@class, 'admin_status')]//div[contains(@class, 'timeline-item  ')]//div[contains(.,'Clock-Out')]//div[contains(@class, 'd-flex ')]//span[1]//div[contains(@class, 'cursor-pointer')]").click()
        time.sleep(5)
        Time = driver.find_element_by_xpath("//button[starts-with(@id, 'btnHours')]").click()
        time.sleep(5)
        Hour = driver.find_element_by_xpath("//div[starts-with(@id, 'dropdown')]//div//button[contains(.,'17')]").click()

        Time1 = driver.find_element_by_xpath("//button[starts-with(@id, 'btnMin')]").click()
        time.sleep(2)
        Minute = driver.find_element_by_xpath("//div[starts-with(@id, 'dropdown')]//button[starts-with(@id, 'btnMin')]//following-sibling::div//button[contains(.,'00')]").click()

        #Click On-time
        Status = driver.find_element_by_xpath("//span[contains(.,'On Time')]").click()

        #Input Memo
        Memo = driver.find_element_by_xpath("//div[contains(@class, 'modal-content')]//div[5]//textarea[contains(@name, 'memo')]").send_keys("test")
        #Logging("Input memo")

        #Save
        Save = driver.find_element_by_xpath("//span[contains(.,'Save')]").click()
        #Logging("Edit clockout successfully")
        Logging(green('Edit clock out successfully', 'bright')) 
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["edit_clockout"]["pass"])        
        time.sleep(5)
    except:
        Logging("Edit clockout failed")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["edit_clockout"]["fail"])    

#------------------------------------------------------------------------------------------#
    #officetimeUI_timesheet
    Logging(" ")
    Logging("Change timesheet-officetime to decimal")
    office_time = driver.find_element_by_xpath("//*[@id='app']//div[contains(@class, 'admin_status')]//div[contains(@class, 'info-card')]//div[contains(.,'Office time')]//div[2]/div")
    Logging("office time: " +  office_time.text)

    office_time1 = office_time.text

    hour1 = office_time1.split("H")[0]
    hour_number1 = int(hour1)
    nb_out.append(hour_number1)
    Logging("office time after change to decimal: " + str(hour_number1))

    #workingtimeUI_timesheet
    Logging("Change timesheet-working time to decimal")
    working_time = driver.find_element_by_xpath("//*[@id='app']//div[contains(@class, 'admin_status')]//div[contains(@class, 'info-card')]//div[contains(.,'Working time')]//div[2]/div")
    Logging("working time: " + working_time.text)

    working_time1 = working_time.text

    working_hour1 = working_time1.split("H")[0]
    working_number1 = int(working_hour1)
    nb_out.append(working_number1)
    Logging("working time after change to decimal: " + str(working_number1))

    #breaktimeUI_timesheet
    Logging("Change timesheet-break time to decimal")
    break_time = driver.find_element_by_xpath("//*[@id='app']//div[contains(@class, 'admin_status')]//div[contains(@class, 'info-card')]//div[contains(.,'Break time')]//div[2]/div")
    Logging("break time: " + break_time.text)

    break_time1 = break_time.text

    break_hour1 = break_time1.split("H")[0]
    break_number1 = int(break_hour1)
    nb_out.append(break_number1)
    Logging("break time after change to decimal: " + str(break_number1))

    #OTUI_timesheet
    Logging("Change timesheet-OT time to decimal")
    OT_time = driver.find_element_by_xpath("//*[@id='app']//div[contains(@class, 'admin_status')]//div[contains(@class, 'info-card')]/div[5]/div[2]/div[1]")
    Logging("OT time: " + OT_time.text)

    OT_time1 = OT_time.text

    OT_hour1 = OT_time1.split("H")[0]
    OT_number1 = int(OT_hour1)
    nb_out.append(OT_number1)
    Logging("OT time after change to decimal: " + str(OT_number1))
    return nb_out
    #return hour_number1, working_number1, break_number1, OT_number1
  

def report_2nd():
    try:
        time.sleep(5)
        nb_report=[]
        driver.find_element_by_xpath("//a[contains(@href,'/nhr/hr/timecard/user/statistics')]").click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Working status')] ")))

        Logging("")
        #Logging("*** Report - After log in***")
        Logging(yellow('***Report - After log in***', 'bold')) 

        #workingtimeUI_number
        Logging("Change working time to decimal")
        time.sleep(5)
        working_time2nd = driver.find_element_by_xpath("//span[contains(.,'Working status')]//following-sibling::div//li[1]//span[contains(.,'Working time')]/../../div[2]")
        Logging("working time: " + working_time2nd.text)
        working_time2 = working_time2nd.text
        try:
            minute_time2 = working_time2.split(" ")[1]
            #Logging(minute_time2)
            minutes2 = minute_time2.split("m")[0]
            minutes_number2 = int(minutes2)
            #Logging(minutes_number2)

            hour_time2 = working_time2.split(" ")[0]
            #Logging(hour_time2)
            hour2 = hour_time2.split("H")[0]
            hour_number2 = int(hour2)
            #Logging(hour_number2)

            working_time_decimal_2nd = ((minutes_number2) / 60) + (hour_number2)
            nb_report.append(working_time_decimal_2nd)
            Logging("working time after change to decimal: " + str(round(working_time_decimal_2nd, 2)))
            #Logging("working time after change to decimal: " + str(working_time_decimal_2nd))
        except:
            hour_time2 = working_time2.split(" ")[0]
            #Logging(hour_time2)
            hour2 = hour_time2.split("H")[0]
            hour_number2 = int(hour2)
            #Logging(hour_number2)

            working_time_decimal_2nd = hour_number2
            nb_report.append(working_time_decimal_2nd)

            Logging("working time after change to decimal: " + str(working_time_decimal_2nd))

        #workedtimeUI_number
        Logging("Change worked time to decimal")
        time.sleep(5)
        worked_time2nd = driver.find_element_by_xpath("//span[contains(.,'Working status')]//following-sibling::div//li[2]//span[contains(.,'Worked time')]/../../div[2]")
        Logging("worked time: " + worked_time2nd.text)
        worked_time2 = worked_time2nd.text
        try:
            minute_worked_time2 = worked_time2.split(" ")[1]
            #Logging(minute_worked_time2)
            minutes_worked2 = minute_worked_time2.split("m")[0]
            minutes_worked_number2 = int(minutes_worked2)
            #Logging(minutes_worked_number2)

            hour_worked_time2 = worked_time2.split(" ")[0]
            #Logging(hour_worked_time2)
            hour_worked2 = hour_worked_time2.split("H")[0]
            hour_worked_number2 = int(hour_worked2)
            #Logging(hour_worked_number2)

            worked_time_decimal_2nd = ((minutes_worked_number2) / 60) + (hour_worked_number2)
            nb_report.append(worked_time_decimal_2nd)
            Logging("worked time after change to decimal: " + str(round(worked_time_decimal_2nd, 2)))
            #Logging("worked time after change to decimal: " + str(worked_time_decimal_2nd))
        except:
            hour_worked_time2 = worked_time2.split(" ")[0]
            #Logging(hour_worked_time2)
            hour_worked2 = hour_worked_time2.split("H")[0]
            hour_worked_number2 = int(hour_worked2)
            #Logging(hour_worked_number2)

            worked_time_decimal_2nd = hour_worked_number2
            nb_report.append(worked_time_decimal_2nd)
            Logging("worked time after change to decimal: " + str(worked_time_decimal_2nd))

        #breaktimeUI_number
        Logging("Change break time to decimal")
        time.sleep(5)
        break_time2nd = driver.find_element_by_xpath("//span[contains(.,'Working status')]//following-sibling::div//li[3]//span[contains(.,'Break time')]/../../div[2]")
        Logging("break time: " + break_time2nd.text)
        break_time2 = break_time2nd.text
        try:
            minute_break_time_report2 = break_time2nd.split(" ")[1]
            #Logging(minute_break_time_report2)
            minutes_break_report2 = minute_break_time_report2.split("m")[0]
            minutes_break_number_report2 = int(minutes_break_report2)
            #Logging(minutes_break_number_report2)

            hour_break_time2 = break_time2.split(" ")[0]
            #Logging(hour_break_time2)
            hour_break2 = hour_break_time2.split("H")[0]
            hour_break_number2 = int(hour_break2)
            #Logging(hour_break_number2)

            break_time_decimal_2nd = ((minutes_break_number_report2) / 60) + (hour_break_number2)
            nb_report.append(break_time_decimal_2nd)
            Logging("break time after change to decimal: " + str(break_time_decimal_2nd))
            #return working_time_decimal_2nd, worked_time_decimal_2nd, break_time_decimal_2nd
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["after_login_report_data"]["pass"])  
            return nb_report
        except:
            hour_break_time2 = break_time2.split(" ")[0]
            #Logging(hour_break_time2)
            hour_break2 = hour_break_time2.split("H")[0]
            hour_break_number2 = int(hour_break2)
            #Logging(hour_break_number2)

            break_time_decimal_2nd = hour_break_number2
            nb_report.append(break_time_decimal_2nd)
            Logging("break time after change to decimal: " + str(break_time_decimal_2nd))
            #return working_time_decimal_2nd, worked_time_decimal_2nd, break_time_decimal_2nd
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["after_login_report_data"]["pass"])  
            return nb_report
    except:
        #Logging("Check data fail")
        Logging(red('>>>Check data fail', 'bright')) 


def calculation(working_time_report_decimal,worked_time_report_decimal,break_time_report_decimal,hour_number1,working_number1,break_number1,working_time_decimal_2nd,worked_time_decimal_2nd,break_time_decimal_2nd):
    try:
    #Calculation step by step #working time
        Logging("")
        Logging("Compare workingtime - before and after log in")
        if round(working_time_report_decimal) + hour_number1 == round(working_time_decimal_2nd):
            # Logging(working_time_report_decimal)
            # Logging(hour_number1)
            # Logging(working_time_decimal_2nd)
            #Logging("Result was the same - calculation was right")
            Logging(green('>>>Result was the same - calculation was right', 'bright')) 
        else:
            #Logging("Result was different - calculation was wrong")
            Logging(red('>>>Result was different - calculation was wrong', 'bright')) 

        #Calculation step by step #worked time  
        Logging("Compare workedtime - before and after log in")
        if round(worked_time_report_decimal, 2) + working_number1 == round(worked_time_decimal_2nd, 2):
            # Logging(worked_time_report_decimal)
            # Logging(working_number1)
            # Logging(worked_time_decimal_2nd)
            #Logging("Result was the same - calculation was right")
            Logging(green('>>>Result was the same - calculation was right', 'bright')) 
        else:
            #Logging("Result was different - calculation was wrong")
            Logging(red('>>>Result was different - calculation was wrong', 'bright')) 

        #Calculation step by step #break time
        Logging("Compare break time - before and after log in")  
        if round(break_time_report_decimal) + round(break_number1) == round(break_time_decimal_2nd):
            # Logging(break_time_report_decimal)
            # Logging(break_number1)
            # Logging(break_time_decimal_2nd)
            #Logging("Result was the same - calculation was right")
            Logging(green('>>>Result was the same - calculation was right', 'bright')) 
        else:
            #Logging("Result was different - calculation was wrong") 
            Logging(red('>>>Result was different - calculation was wrong', 'bright')) 

        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["compare_time"]["pass"])

    except:
        #Logging("Can't calculation")
        Logging(red('>>>Cant calculate', 'bright')) 
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["compare_time"]["fail"])


def daily_status2(status1,break_number1,working_number1,OT_number1):
    try:
        #After login
        Logging("")
        #Logging("*** Daily Status - After log in***")
        Logging(yellow('***Daily Status - After log in***', 'bold')) 

        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Daily Status')]").click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Name')] ")))

        driver.find_element_by_xpath("//div[contains(@class,'company-time-card-real-time')]/div/div[2]/div/div[1]").click()
        search2 = driver.find_element_by_xpath("//input[contains(@class,'form-control')]")
        search2.send_keys(data["name_keyword"][0])
        search2.send_keys(Keys.ENTER)
        time.sleep(5)
        driver.find_element_by_xpath("//div[contains(@class,'visible')]//li").click()
        driver.find_element_by_xpath("//div[contains(@class,'company-time-card-real-time')]/div/div[2]/div/div[1]").click()

        time.sleep(5)
        work_status2 = driver.find_element_by_xpath("//div[contains(@class,'label-rounded')]")
        Logging(" work status: " + work_status2.text)
        status2 = work_status2.text

        dailystatus_clockin2 = driver.find_element_by_xpath("//div[contains(@class,'ag-center-cols-viewport')]//*[@col-id='clock_in_title']/div[1]")
        Logging(" clock-in: " + dailystatus_clockin2.text[0:5])
        x = dailystatus_clockin2.text[0:5]

        dailystatus_clockout2 = driver.find_element_by_xpath("//div[contains(@class,'ag-center-cols-viewport')]//*[@col-id='clock_out_title']")
        Logging("clock-out: " + dailystatus_clockout2.text[0:5])
        y = dailystatus_clockout2.text[0:5]

        dailystatus_breaktime2 = driver.find_element_by_xpath("//div[contains(@class,'ag-center-cols-viewport')]//*[@col-id='break_time']")
        Logging("break time before change to decimal: " + dailystatus_breaktime2.text)
        breaktime = dailystatus_breaktime2.text
        breaktime_hour = breaktime.split("H")[0]
        breaktime_number = int(breaktime_hour)
        Logging("break time after change to decimal: " + str(breaktime_number))

        achievement2 = driver.find_element_by_xpath("//div[contains(@class,'ag-center-cols-viewport')]//*[@col-id='cumulative_work_time_percent']/div[1]/div")
        Logging("Achievement: " + achievement2.text)

        estimate2 = driver.find_element_by_xpath("//div[contains(@class,'ag-center-cols-viewport')]//*[@col-id='over_time_since']/div[1]/div")
        Logging("Estimate: " + estimate2.text)   

        workingtime = driver.find_element_by_xpath("//div[contains(@class,'ag-center-cols-viewport')]//*[@col-id='cumulative_work_time']/div[1]/div")
        Logging("working time before change to decimal: " + workingtime.text[0:1])
        workingtime_status = workingtime.text[0:1]
        workingtime_status_hour = workingtime_status.split("H")[0]
        workingtime_status_number = int(workingtime_status_hour)
        Logging("working time after change to decimal: " + str(workingtime_status_number))

        OT = driver.find_element_by_xpath("//div[contains(@class,'ag-center-cols-viewport')]//*[@col-id='cumulative_over_time_remain']/div[1]/div/div[1]")
        Logging("OT time before change to decimal: " + OT.text[0:1])
        OT1 = OT.text[0:1]
        OT_hour = OT1.split("H")[0]
        OT_number = int(OT_hour)
        Logging(" OT time after change to decimal: " + str(OT_number))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["after_login_daily_status_data"]["pass"])

        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Timesheets')]").click()
        time.sleep(5)
        clockin_UI = driver.find_element_by_xpath("//div[contains(@class,'check-in-status')]")
        Logging("Clock-in time: " + clockin_UI.text)  
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["clockin_UI"]["pass"])

        clockout_UI = driver.find_element_by_xpath("//div[contains(@class,'check-out-status')]")
        Logging("Clock-out time: " + clockout_UI.text)
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["clockout_UI"]["pass"])
    except: 
        #Logging("Check data fail")
        Logging(red('>>>Check data failed', 'bright')) 

    try:      
        #Compare Clockin
        Logging("")
        Logging("Compare clock-in time and dailystatus-clockin ")  
        if x == clockin_UI.text:
            #Logging ("Result was the same - system is correct")
            Logging(green('>>>Result was the same - system is correct', 'bright'))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["compare_clockin"]["pass"])

        else:
            #Logging("Result was different - system is false")
            Logging(red('>>>Result was different - system is false', 'bright')) 
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["compare_clockin"]["fail"])


        #Compare ClockoutCompare clock-out time and dailystatus-clockout
        Logging("Compare clock-out time and dailystatus-clockout ") 
        if y == clockout_UI.text:
            #Logging ("Result was the same - system is correct")
            Logging(green('>>>Result was the same - system is correct', 'bright'))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["compare_clockout"]["pass"])

        else:
            #Logging("Result was different - system is false")  
            Logging(red('>>>Result was different - system is false', 'bright'))   
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["compare_clockout"]["fail"])

        # #Compare status
        # Logging("Compare status before and after log in") 
        # if status1 == status2:
        #     #Logging ("Result was the same - system is false")
        #     Logging(red('>>>Result was different - system is false', 'bright')) 
        #     add_data_in_excel(param_excel["compare_status"],"f","System is false")
        # else:
        #     #Logging("Result was different - system is correct")
        #     Logging(green('>>>Result was different - system is correct', 'bright'))
        #     add_data_in_excel(param_excel["compare_status"],"p","System is correct")

        #Compare break time
        Logging("Compare daily status-break time and timesheet-break time")
        if breaktime_number == break_number1:
            #Logging ("Result was the same - system is correct")
            Logging(green('>>>Result was the same - system is correct', 'bright'))
        else:
            #Logging("Result was different - system is false")
            Logging(red('>>>Result was different - system is false', 'bright')) 

        #Compare working time
        Logging("Compare daily status-working time and timesheet-working time")
        if working_number1 == workingtime_status_number:
            #Logging ("Result was the same - system is correct")
            Logging(green('>>>Result was the same - system is correct', 'bright'))
        else:
            #Logging("Result was different - system is false")
            Logging(red('>>>Result was different - system is false', 'bright')) 

        #Compare OT
        Logging("Compare daily status-OT time and timesheet-OT time")
        if OT_number == OT_number1:
            #Logging ("Result was the same - system is correct")
            Logging(green('>>>Result was the same - system is correct', 'bright'))
        else:
            #Logging("Result was different - system is false")
            Logging(red('>>>Result was different - system is false', 'bright')) 

        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["compare_time_daily"]["pass"])
    except:
        #Logging("Can't compare")
        Logging(red('>>>Cant compare', 'bright')) 
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["compare_time_daily"]["fail"])


def weekly_status2():
    try:
        #Timesheets
        time.sleep(5)
        e = driver.find_element_by_xpath("//div[contains(@class,'check-in-status')]").text
        f = driver.find_element_by_xpath("//div[contains(@class,'check-out-status')]").text
        a = ws_office_time = driver.find_element_by_xpath("//*[@id='app']//div[contains(@class, 'admin_status')]//div[contains(@class, 'info-card')]//div[contains(.,'Office time')]//div[2]/div").text[0]
        a = int(a)
        b = ws_break_time = driver.find_element_by_xpath("//*[@id='app']//div[contains(@class, 'admin_status')]//div[contains(@class, 'info-card')]//div[contains(.,'Break time')]//div[2]/div").text[0]
        b = int(b)
        c = ws_working_time = driver.find_element_by_xpath("//*[@id='app']//div[contains(@class, 'admin_status')]//div[contains(@class, 'info-card')]//div[contains(.,'Working time')]//div[2]/div").text[0]
        c = int(c)
        d = ws_OT_time = driver.find_element_by_xpath("//div[contains(@class, 'info-card')]/div[5]/div[2]/div[1]").text[0]
        d = int(d)
        
        Logging("")
        #Logging("***Weekly Status - After log in***")
        Logging(yellow('***Weekly Status - After log in***', 'bold')) 

        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Weekly Status')]").click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Name')] ")))

        driver.find_element_by_xpath("//div[contains(@class,'company-status-setting')]/div/div[2]/div/div[1]").click()
        ws_search2 = driver.find_element_by_xpath("//input[contains(@class,'form-control')]")
        ws_search2.send_keys(data["name_keyword"][0])
        ws_search2.send_keys(Keys.ENTER)
        time.sleep(3)
        driver.find_element_by_xpath("//div[contains(@class,'visible')]//li").click()
        driver.find_element_by_xpath("//div[contains(@class,'company-status-setting')]/div/div[2]/div/div[1]").click()

        time.sleep(3)
        monday2 = driver.find_element_by_xpath("//*[@col-id='day_0']//div[contains(@class,'cursor-pointer')]/span")
        Logging("monday before change to decimal: " + monday2.text)
        monday_time2 = monday2.text
        try:
            minute_monday_time2 = monday_time2.split(" ")[1]
            minutes_monday_time2 = minute_monday_time2.split("m")[0]
            minutes_number_monday_time2 = int(minutes_monday_time2)
            #Logging(minutes_number_monday_time)
            hour_monday_time2 = monday_time2.split(" ")[0]
            #Logging(hour_monday_time)
            hours_monday_time2 = hour_monday_time2.split("H")[0]
            hour_number_monday_time2 = int(hours_monday_time2)
            #Logging(hour_number_monday_time)
            monday_time_decimal2 = ((minutes_number_monday_time2) / 60) + (hour_number_monday_time2)
            #Logging("monday after change to decimal: " + str(monday_time_decimal2))
            Logging("monday after change to decimal: " + str(round(monday_time_decimal2, 2)))
        except:
            hour_monday_time2 = monday_time2.split(" ")[0]
            #Logging(hour_monday_time)
            hours_monday_time2 = hour_monday_time2.split("H")[0]
            hour_number_monday_time2 = int(hours_monday_time2)
            #Logging(hour_number_monday_time2)
            monday_time_decimal2 = hour_number_monday_time2
            Logging("monday after change to decimal: " + str(monday_time_decimal2))

        tuesday2 = driver.find_element_by_xpath("//*[@col-id='day_1']//div[contains(@class,'cursor-pointer')]/span")
        Logging("tuesday before change to decimal: " + tuesday2.text)
        tuesday_time2 = tuesday2.text
        try:
            minute_tuesday_time2 = tuesday_time2.split(" ")[1]
            minutes_tuesday_time2 = minute_tuesday_time2.split("m")[0]
            minutes_number_tuesday_time2 = int(minutes_tuesday_time2)
            #Logging(minutes_number_tuesday_time2)
            hour_tuesday_time2 = tuesday_time2.split(" ")[0]
            #Logging(hour_tuesday_time2)
            hours_tuesday_time2 = hour_tuesday_time2.split("H")[0]
            hour_number_tuesday_time2 = int(hours_tuesday_time2)
            #Logging(hour_number_tuesday_time2)
            tuesday_time_decimal2 = ((minutes_number_tuesday_time2) / 60) + (hour_number_tuesday_time2)
            #Logging("tuesday after change to decimal: " + str(tuesday_time_decimal2))
            Logging("tuesday after change to decimal: " + str(round(tuesday_time_decimal2, 2)))
        except:
            hour_tuesday_time2 = tuesday_time2.split(" ")[0]
            #Logging(hour_tuesday_time2)
            hours_tuesday_time2 = hour_tuesday_time2.split("H")[0]
            hour_number_tuesday_time2 = int(hours_tuesday_time2)
            #Logging(hour_number_tuesday_time2)
            tuesday_time_decimal2 = hour_number_tuesday_time2
            Logging("tuesday after change to decimal: " + str(tuesday_time_decimal2))

        wednesday2 = driver.find_element_by_xpath("//*[@col-id='day_2']//div[contains(@class,'cursor-pointer')]/span")
        Logging("wednesday before change to decimal: " + wednesday2.text)
        wednesday_time2 = wednesday2.text
        try:
            minute_wednesday_time2 = wednesday_time2.split(" ")[1]
            minutes_wednesday_time2 = minute_wednesday_time2.split("m")[0]
            minutes_number_wednesday_time2 = int(minutes_wednesday_time2)
            #Logging(minutes_number_wednesday_time2)
            hour_wednesday_time2 = wednesday_time2.split(" ")[0]
            #Logging(hour_wednesday_time2)
            hours_wednesday_time2 = hour_wednesday_time2.split("H")[0]
            hour_number_wednesday_time2 = int(hours_wednesday_time2)
            #Logging(hour_number_wednesday_time2)
            wednesday_time_decimal2 = ((minutes_number_wednesday_time2) / 60) + (hour_number_wednesday_time2)
            #Logging("wednesday after change to decimal: " + str(wednesday_time_decimal2))
            Logging("wednesday after change to decimal: " + str(round(wednesday_time_decimal2, 2)))
        except:
            hour_wednesday_time2 = wednesday_time2.split(" ")[0]
            #Logging(hour_wednesday_time2)
            hours_wednesday_time2 = hour_wednesday_time2.split("H")[0]
            hour_number_wednesday_time2 = int(hours_wednesday_time2)
            #Logging(hour_number_wednesday_time2)
            wednesday_time_decimal2 = hour_number_wednesday_time2
            Logging("wednesday after change to decimal: " + str(wednesday_time_decimal2))

        thursday2 = driver.find_element_by_xpath("//*[@col-id='day_3']//div[contains(@class,'cursor-pointer')]/span")
        Logging("thursday before change to decimal: " + thursday2.text)
        thursday_time2 = thursday2.text
        try:
            minute_thursday_time2 = thursday_time2.split(" ")[1]
            minutes_thursday_time2 = minute_thursday_time2.split("m")[0]
            minutes_number_thursday_time2 = int(minutes_thursday_time2)
            #Logging(minutes_number_thursday_time2)

            hour_thursday_time2 = thursday_time2.split2(" ")[0]
            #Logging(hour_thursday_time2)
            hours_thursday_time2 = hour_thursday_time2.split("H")[0]
            hour_number_thursday_time2 = int(hours_thursday_time2)
            #Logging(hour_number_thursday_time2)
            thursday_time_decimal2 = ((minutes_number_thursday_time2) / 60) + (hour_number_thursday_time2)
            #Logging("thursday after change to decimal: " + str(thursday_time_decimal2))
            Logging("thursday after change to decimal: " + str(round(thursday_time_decimal2, 2)))
        except:
            hour_thursday_time2 = thursday_time2.split(" ")[0]
            #Logging(hour_thursday_time2)
            hours_thursday_time2 = hour_thursday_time2.split("H")[0]
            hour_number_thursday_time2 = int(hours_thursday_time2)
            #Logging(hour_number_thursday_time2)
            thursday_time_decimal2 = hour_number_thursday_time2
            Logging("thursday after change to decimal: " + str(thursday_time_decimal2))

        friday2 = driver.find_element_by_xpath("//*[@col-id='day_4']//div[contains(@class,'cursor-pointer')]/span")
        Logging("friday before change to decimal: " + friday2.text)
        friday_time2 = friday2.text
        try:
            minute_friday_time2 = friday_time2.split(" ")[1]
            minutes_friday_time2 = minute_friday_time2.split("m")[0]
            minutes_number_friday_time2 = int(minutes_friday_time2)
            #Logging(minutes_number_friday_time2)
            hour_friday_time2 = friday_time2.split(" ")[0]
            #Logging(hour_friday_time2)
            hours_friday_time2 = hour_friday_time2.split("H")[0]
            hour_number_friday_time2 = int(hours_friday_time2)
            #Logging(hour_number_friday_time2)
            friday_time_decimal2 = ((minutes_number_friday_time2) / 60) + (hour_number_friday_time2)
            #Logging("friday after change to decimal: " + str(friday_time_decimal2))
            Logging("friday after change to decimal: " + str(round(friday_time_decimal2, 2)))
        except:
            hour_friday_time2 = friday_time2.split(" ")[0]
            #Logging(hour_friday_time2)
            hours_friday_time2 = hour_friday_time2.split("H")[0]
            hour_number_friday_time2 = int(hours_friday_time2)
            #Logging(hour_number_friday_time2)
            friday_time_decimal2 = hour_number_friday_time2
            Logging("friday after change to decimal: " + str(friday_time_decimal2))

        saturday2 = driver.find_element_by_xpath("//*[@col-id='day_5']//div[contains(@class,'cursor-pointer')]/span")
        Logging("saturday before change to decimal: " + saturday2.text)
        saturday_time2 = saturday2.text
        try:
            minute_saturday_time2 = saturday_time2.split(" ")[1]
            minutes_saturday_time2 = minute_saturday_time2.split("m")[0]
            minutes_number_saturday_time2 = int(minutes_saturday_time2)
            #Logging(minutes_number_saturday_time2)
            hour_saturday_time2 = saturday_time2.split(" ")[0]
            #Logging(hour_saturday_time2)
            hours_saturday_time2 = hour_saturday_time2.split("H")[0]
            hour_number_saturday_time2 = int(hours_saturday_time2)
            #Logging(hour_number_saturday_time2)
            saturday_time_decimal2 = ((minutes_number_saturday_time2) / 60) + (hour_number_saturday_time2)
            #Logging("saturday after change to decimal: " + str(saturday_time_decimal2))
            Logging("saturday after change to decimal: " + str(round(saturday_time_decimal2, 2)))
        except:
            hour_saturday_time2 = saturday_time2.split(" ")[0]
            #Logging(hour_saturday_time2)
            hours_saturday_time2 = hour_saturday_time2.split("H")[0]
            hour_number_saturday_time2 = int(hours_saturday_time2)
            #Logging(hour_number_saturday_time2)
            saturday_time_decimal2 = hour_number_saturday_time2
            Logging("saturday after change to decimal: " + str(saturday_time_decimal2))

        sunday2 = driver.find_element_by_xpath("//*[@col-id='day_6']//div[contains(@class,'cursor-pointer')]/span")
        Logging("sunday: " + sunday2.text)

        Logging("")
        total2 = driver.find_element_by_xpath("//span[contains(@class,'td-sum-of-time')]")
        Logging("total before change to decimal: " + total2.text)
        total_time2 = total2.text
        try:
            minute_total_time2 = total_time2.split(" ")[1]
            minutes_total_time2 = minute_total_time2.split("m")[0]
            minutes_number_total_time2 = int(minutes_total_time2)
            #Logging(minutes_number_total_time2)

            hour_total_time2 = total_time2.split(" ")[0]
            #Logging(hour_total_time2)
            hours_total_time2 = hour_total_time2.split("H")[0]
            hour_number_total_time2 = int(hours_total_time2)
            #Logging(hour_number_total_time2)
            total_time_decimal2 = ((minutes_number_total_time2) / 60) + (hour_number_total_time2)
            #Logging("total after change to decimal: " + str(total_time_decimal2))
            Logging("total after change to decimal: " + str(round(total_time_decimal2, 2)))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["after_login_weekly_status_data"]["pass"])

        except:
            hour_total_time2 = total_time2.split(" ")[0]
            #Logging(hour_total_time2)
            hours_total_time2 = hour_total_time2.split("H")[0]
            hour_number_total_time2 = int(hours_total_time2)
            #Logging(hour_number_total_time2)
            total_time_decimal2 = hour_number_total_time2
            Logging("total after change to decimal: " + str(total_time_decimal2))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["after_login_weekly_status_data"]["pass"])

    except: 
        #Logging("Check data fail")
        Logging(red('>>>Check data failed', 'bright')) 

    try:   
        #Calculation #Total working time
        Logging("")
        Logging("Calculation - Total Working time")
        if round(monday_time_decimal2) + round(tuesday_time_decimal2) + round(wednesday_time_decimal2) + round(thursday_time_decimal2) + round(friday_time_decimal2) + round(saturday_time_decimal2) == round(total_time_decimal2):
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - calculation was right', 'bright')) 
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["total_working_time"]["pass"])
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright')) 
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["total_working_time"]["fail"])

        #Click details
        driver.find_element_by_xpath("//*[@col-id='view-detail']//div[contains(@class,'cursor-pointer')]").click()

        Logging("")
        #Clock in time
        time.sleep(5)
        ws_clockin_UI = driver.find_element_by_xpath("//div[contains(@class,'check-in-status')]")
        Logging("Clock-in time: " + ws_clockin_UI.text)  
        
        #Clock out time
        ws_clockout_UI = driver.find_element_by_xpath("//div[contains(@class,'check-out-status')]")
        Logging("Clock-out time: " + ws_clockout_UI.text)

        #officetimeUI_weekly status
        Logging(" ")
        Logging("Change weekly status-officetime to decimal")
        time.sleep(3)
        ws_office_time = driver.find_element_by_xpath("//div[contains(@class, 'info-card')]//div[contains(.,'Office time')]//div[2]/div")
        Logging("office time: " +  ws_office_time.text)

        ws_office_time1 = ws_office_time.text

        ws_hour1 = ws_office_time1.split("H")[0]
        ws_hour_number1 = int(ws_hour1)
        Logging("office time after change to decimal: " + str(ws_hour_number1))

        #breaktimeUI_weekly status
        Logging("Change weekly status-break time to decimal")
        ws_break_time = driver.find_element_by_xpath("//div[contains(@class, 'info-card')]//div[contains(.,'Break time')]//div[2]/div")
        Logging("break time: " + ws_break_time.text)

        ws_break_time1 = ws_break_time.text

        ws_break_hour1 = ws_break_time1.split("H")[0]
        ws_break_number1 = int(ws_break_hour1)
        Logging("break time after change to decimal: " + str(ws_break_number1))

        #workingtimeUI_weekly status
        Logging("Change weekly status-working time to decimal")
        ws_working_time = driver.find_element_by_xpath("//div[contains(@class, 'info-card')]//div[contains(.,'Working time')]//div[2]/div")
        Logging("working time: " + ws_working_time.text)

        ws_working_time1 = ws_working_time.text

        ws_working_hour1 = ws_working_time1.split("H")[0]
        ws_working_number1 = int(ws_working_hour1)
        Logging("working time after change to decimal: " + str(ws_working_number1))

        #OTUI_weekly status
        Logging("Change weekly status-OT time to decimal")
        ws_OT_time = driver.find_element_by_xpath("//div[contains(@class, 'info-card')]/div[5]/div[2]/div[1]")
        Logging("OT time: " + ws_OT_time.text)

        ws_OT_time1 = ws_OT_time.text

        ws_OT_hour1 = ws_OT_time1.split("H")[0]
        ws_OT_number1 = int(ws_OT_hour1)
        Logging("OT time after change to decimal: " + str(ws_OT_number1))
        
        #Compare clock in
        Logging("")
        Logging("***Compare data of timesheets and weekly status***")
        # Logging(ws_clockin_UI.text)
        # Logging(e)
        Logging("Compare timesheets-clockin and weekly status-clockin")
        if ws_clockin_UI.text == e:
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright')) 

        #Compare clock out
        Logging("")
        # Logging(ws_clockout_UI.text)
        # Logging(f)
        Logging("Compare timesheets-clockout and weekly status-clockout")
        if ws_clockout_UI.text == f:
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright')) 

        #Compare officetime
        # Logging(ws_hour_number1)
        # Logging(a)
        Logging("")
        Logging("Compare timesheets-officetime and weekly status-officetime")
        if ws_hour_number1 == a:
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright')) 

        #Compare breaktime
        # Logging(ws_break_number1)
        # Logging(b)
        Logging("")
        Logging("Compare timesheets-breaktime and weekly status-breaktime")
        if ws_break_number1 == b:
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright')) 

        #Compare workingtime
        # Logging(ws_working_number1)
        # Logging(c)
        Logging("")
        Logging("Compare timesheets-workingtime and weekly status-workingtime")
        if ws_working_number1 == c:
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright')) 

        #Compare OTtime
        # Logging(ws_OT_number1)
        # Logging(d)
        Logging("")
        Logging("Compare timesheets-OT time and weekly status-OT time")
        if ws_OT_number1 == d:
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright')) 

        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["view_detail_weekly_status_data"]["pass"])

    except:
        #Logging("Check data fail")
        Logging(red('>>>Check data failed', 'bright')) 


def company_timecard_reports():
    try:
        time.sleep(5)
        company_report_page = driver.find_element_by_xpath(" //a[contains(@href,'/nhr/hr/timecard/company/statistics')]")
        if company_report_page.is_displayed():
            company_report_page.click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Name')]")))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["access_company_report_page"]["pass"])
        else:
            driver.find_element_by_xpath("//li[11]//span[contains(@class, 'text-truncate') and contains(., 'Reports')]").click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Name')] ")))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["access_company_report_page"]["pass"])

        driver.find_element_by_xpath("//div[contains(@class,'company-statistic-setting')]/div/div[2]/div/div[1]").click()
        ws_search2 = driver.find_element_by_xpath("//input[contains(@class,'form-control')]")
        ws_search2.send_keys(data["name_keyword"][0])
        ws_search2.send_keys(Keys.ENTER)
        time.sleep(5)
        driver.find_element_by_xpath("//div[contains(@class,'visible')]//li").click()
        driver.find_element_by_xpath("//div[contains(@class,'company-statistic-setting')]/div/div[2]/div/div[1]").click()

        time.sleep(5)
        Logging("")
        #Logging("***Reports Default***")
        Logging(yellow('***Reports Default***', 'bold')) 

        Logging("Change working day to decimal")
        working_day = driver.find_element_by_xpath("//*[@col-id='weekday']//div[contains(@class,'ag-react-container')]//div//div")
        Logging("working day before change to decimal: " + working_day.text)
        working_day_time = working_day.text
        working_day_hour = working_day_time.split(" ")[0]
        working_day_number = int(working_day_hour)
        Logging("working day after change to decimal: " + str(working_day_number))

        Logging("Change worked day to decimal")
        worked_day = driver.find_element_by_xpath("//*[@col-id='day_work']//div[contains(@class,'ag-react-container')]")
        Logging("worked daybefore change to decimal: " + worked_day.text)
        worked_day_time = worked_day.text
        worked_day_hour = worked_day_time.split(" ")[0]
        worked_day_number = int(worked_day_hour)
        Logging("worked day after change to decimal: " + str(worked_day_number))

        avg_clock_in = driver.find_element_by_xpath("//*[@col-id='avg_clock_in']//div[contains(@class,'ag-react-container')]")
        Logging("avg clock in: " + avg_clock_in.text)
        
        avg_clock_out = driver.find_element_by_xpath("//*[@col-id='avg_clock_out']//div[contains(@class,'ag-react-container')]")
        Logging("avg clock out: " + avg_clock_out.text)
        time.sleep(5)

        Logging("")
        Logging("Change Avg.Worked time per day to decimal")
        avg_worked_time_per_day = driver.find_element_by_xpath("//*[@col-id='avg_daily_work']//div[contains(@class,'ag-react-container')]")
        Logging("Avg.Worked time per day before change to decimal: " + avg_worked_time_per_day.text)
        avg_worked_time_per_day_time = avg_worked_time_per_day.text
        try:
            avg_worked_time_per_day_minute1 = avg_worked_time_per_day_time.split(" ")[1]
            #Logging(avg_worked_time_per_day_minute1)
            avg_worked_time_per_day_minute = avg_worked_time_per_day_minute1.split("m")[0]
            #Logging(avg_worked_time_per_day_minute)
            avg_worked_time_per_day_minute_number = int(avg_worked_time_per_day_minute) 

            avg_worked_time_per_day_hour1 = avg_worked_time_per_day_time.split(" ")[0]
            #Logging(avg_worked_time_per_day_hour1)
            avg_worked_time_per_day_hour = avg_worked_time_per_day_hour1.split("H")[0]
            #Logging(avg_worked_time_per_day_hour)
            avg_worked_time_per_day_hour_number = int(avg_worked_time_per_day_hour)

            avg_worked_time_per_day_decimal = ((avg_worked_time_per_day_minute_number) / 60) + (avg_worked_time_per_day_hour_number)
            Logging("Avg.Worked time per day after change to decimal: " + str(avg_worked_time_per_day_decimal))
        except:
            avg_worked_time_per_day_hour1 = avg_worked_time_per_day_time.split(" ")[0]
            #Logging(avg_worked_time_per_day_hour1)
            avg_worked_time_per_day_hour = avg_worked_time_per_day_hour1.split("H")[0]
            #Logging(avg_worked_time_per_day_hour)
            avg_worked_time_per_day_hour_number = int(avg_worked_time_per_day_hour)

            avg_worked_time_per_day_decimal = avg_worked_time_per_day_hour_number
            Logging("Avg.Worked time per day after change to decimal: " + str(avg_worked_time_per_day_decimal))

        Logging("")
        Logging("Change Avg.Worked time per week to decimal")
        avg_worked_time_per_week = driver.find_element_by_xpath("//*[@col-id='avg_weekly_work']//div[contains(@class,'ag-react-container')]//div//div")
        Logging("Avg.Worked time per week before change to decimal: " + avg_worked_time_per_week.text)
        avg_worked_time_per_week_time = avg_worked_time_per_week.text
        try:
            avg_worked_time_per_week_minute1 = avg_worked_time_per_week_time.split(" ")[1]
            #Logging(avg_worked_time_per_week_minute1)
            avg_worked_time_per_week_minute = avg_worked_time_per_week_minute1.split("m")[0]
            #Logging(avg_worked_time_per_week_minute)
            avg_worked_time_per_week_minute_number = int(avg_worked_time_per_week_minute)

            avg_worked_time_per_week_hour1 = avg_worked_time_per_week_time.split(" ")[0]
            #Logging(avg_worked_time_per_week_hour1)
            avg_worked_time_per_week_hour = avg_worked_time_per_week_hour1.split("H")[0]
            #Logging(avg_worked_time_per_week_hour)
            avg_worked_time_per_week_hour_number = int(avg_worked_time_per_week_hour)

            avg_worked_time_per_week_decimal = ((avg_worked_time_per_week_minute_number) / 60) + (avg_worked_time_per_week_hour_number)
            Logging("Avg.Worked time per week after change to decimal: " + str(avg_worked_time_per_week_decimal))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["work_correction"]["pass"])

        except:
            avg_worked_time_per_week_hour1 = avg_worked_time_per_week_time.split(" ")[0]
            #Logging(avg_worked_time_per_week_hour1)
            avg_worked_time_per_week_hour = avg_worked_time_per_week_hour1.split("H")[0]
            #Logging(avg_worked_time_per_week_hour)
            avg_worked_time_per_week_hour_number = int(avg_worked_time_per_week_hour)

            avg_worked_time_per_week_decimal = avg_worked_time_per_week_hour_number
            Logging("Avg.Worked time per week after change to decimal: " + str(avg_worked_time_per_week_decimal))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["after_login_company_report_data"]["pass"])

    except:
        #Logging("Check data fail")
        Logging(red('>>>Check data failed', 'bright')) 

    try:
        time.sleep(5)
        #Click details
        driver.find_element_by_xpath("//*[@col-id='user_id']//div[contains(@class,'cursor-pointer')]").click()

        time.sleep(5)
        Logging("")
        #Logging("***MONTHLY***")
        Logging(yellow('***MONTHLY***', ['bold', 'underlined'])) 
        #Logging("'''Monthly Scheduled Working'''")
        Logging(yellow('***Monthly Scheduled Working***', 'bold')) 

        #Monthly #Scheduled Working
        scheduled_workingday = driver.find_element_by_xpath("//span[contains(.,'Scheduled working day')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Scheduled working day before change to decimal: " + scheduled_workingday.text)
        working_day_time1 = scheduled_workingday.text
        working_day_hour1 = working_day_time1.split(" ")[0]
        working_day_number1 = int(working_day_hour1)
        Logging("Scheduled working day after change to decimal: " + str(working_day_number1))

        scheduled_worked_day = driver.find_element_by_xpath("//span[contains(.,'Worked day')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Scheduled worked day before change to decimal: " + scheduled_worked_day.text)
        worked_day_time1 = scheduled_worked_day.text
        worked_day_hour1 = worked_day_time1.split(" ")[0]
        worked_day_number1 = int(worked_day_hour1)
        Logging("Scheduled worked day after change to decimal: " + str(worked_day_number1))

        holiday = driver.find_element_by_xpath("//li[3]//span[contains(.,'Holiday')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Holiday before change to decimal: " + holiday.text)
        holiday_time1 = holiday.text
        holiday_hour1 = holiday_time1.split(" ")[0]
        holiday_number1 = int(holiday_hour1)
        Logging("Holiday after change to decimal: " + str(holiday_number1))

        day_off = driver.find_element_by_xpath("//li[4]//span[contains(.,'Day Off')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Day off before change to decimal: " + day_off.text)
        day_off_time1 = day_off.text
        day_off_hour1 = day_off_time1.split(" ")[0]
        day_off_number1 = int(day_off_hour1)
        Logging("Day off after change to decimal: " + str(day_off_number1))

        scheduled_working_vacation = driver.find_element_by_xpath("//li[5]//span[contains(.,'Vacation')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Vacation before change to decimal: " + scheduled_working_vacation.text)
        scheduled_working_vacation_time1 = scheduled_working_vacation.text
        scheduled_working_vacation_hour1 = scheduled_working_vacation_time1.split(" ")[0]
        scheduled_working_vacation_number1 = int(scheduled_working_vacation_hour1)
        Logging("Vacation after change to decimal: " + str(scheduled_working_vacation_number1))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["work_correction"]["pass"])

    except:
        #Logging("Check data fail")
        Logging(red('>>>Check data failed', 'bright')) 

    try:
        Logging("")
        #Logging("'''Monthly Working status'''")
        Logging(yellow('***Monthly Working status***', 'bold')) 

        Logging("Change Avg.Working time per day to decimal")
        #Monthly #Working status
        avg_working_time_per_day = driver.find_element_by_xpath("//span[contains(.,'Avg.Working time per day')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Avg.Working time per day before change to decimal: " + avg_working_time_per_day.text)
        avg_working_time_per_day_time = avg_working_time_per_day.text
        try:
            avg_working_time_per_day_minute1 = avg_working_time_per_day_time.split(" ")[1]
            #Logging(avg_working_time_per_day_minute1)
            avg_working_time_per_day_minute = avg_working_time_per_day_minute1.split("m")[0]
            #Logging(avg_working_time_per_day_minute)
            avg_working_time_per_day_minute_number = int(avg_working_time_per_day_minute)
            
            avg_working_time_per_day_hour1 = avg_working_time_per_day_time.split(" ")[0]
            #Logging(avg_working_time_per_day_hour1)
            avg_working_time_per_day_hour = avg_working_time_per_day_hour1.split("H")[0]
            #Logging(avg_working_time_per_day_hour)
            avg_working_time_per_day_hour_number = int(avg_working_time_per_day_hour)

            avg_working_time_per_day_decimal = ((avg_working_time_per_day_minute_number) / 60) + (avg_working_time_per_day_hour_number)
            Logging("Avg.Working time per day after change to decimal: " + str(avg_working_time_per_day_decimal))
        except:
            avg_working_time_per_day_hour1 = avg_working_time_per_day_time.split(" ")[0]
            #Logging(avg_working_time_per_day_hour1)
            avg_working_time_per_day_hour = avg_working_time_per_day_hour1.split("H")[0]
            #Logging(avg_working_time_per_day_hour)
            avg_working_time_per_day_hour_number = int(avg_working_time_per_day_hour)

            avg_working_time_per_day_decimal = avg_working_time_per_day_hour_number
            Logging("Avg.Working time per day after change to decimal: " + str(avg_working_time_per_day_decimal))

        Logging("")
        Logging("Change Avg.Working time per week to decimal")
        avg_working_time_per_week = driver.find_element_by_xpath("//span[contains(.,'Avg.Working time per week')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Avg.Working time per week beore change to decimal: " + avg_working_time_per_week.text)
        avg_working_time_per_week_time = avg_working_time_per_week.text
        try:
            avg_working_time_per_week_minute1 = avg_working_time_per_week_time.split(" ")[1]
            #Logging(avg_working_time_per_week_minute1)
            avg_working_time_per_week_minute = avg_working_time_per_week_minute1.split("m")[0]
            #Logging(avg_working_time_per_week_minute)
            avg_working_time_per_week_minute_number = int(avg_working_time_per_week_minute)
            
            avg_working_time_per_week_hour1 = avg_working_time_per_week_time.split(" ")[0]
            #Logging(avg_working_time_per_week_hour1)
            avg_working_time_per_week_hour = avg_working_time_per_week_hour1.split("H")[0]
            #Logging(avg_working_time_per_week_hour)
            avg_working_time_per_week_hour_number = int(avg_working_time_per_week_hour)

            avg_working_time_per_week_decimal = ((avg_working_time_per_week_minute_number) / 60) + (avg_working_time_per_week_hour_number)
            Logging("Avg.Working time per week after change to decimal: " + str(avg_working_time_per_week_decimal))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["monthly_working_status"]["pass"])

        except:
            avg_working_time_per_week_hour1 = avg_working_time_per_week_time.split(" ")[0]
            #Logging(avg_working_time_per_week_hour1)
            avg_working_time_per_week_hour = avg_working_time_per_week_hour1.split("H")[0]
            #Logging(avg_working_time_per_week_hour)
            avg_working_time_per_week_hour_number = int(avg_working_time_per_week_hour)

            avg_working_time_per_week_decimal = avg_working_time_per_week_hour_number
            Logging("Avg.Working time per week after change to decimal: " + str(avg_working_time_per_week_decimal))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["monthly_working_status"]["pass"])

    except:
        #Logging("Check data fail")
        Logging(red('>>>Check data failed', 'bright')) 

    try:
        Logging("")
        #Logging("Events")
        Logging(yellow('***Monthly Events***', 'bold')) 

        events_clockin = driver.find_element_by_xpath("//li[1]//span[contains(.,'Clock-In')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Clock-In: " + events_clockin.text)
        events_clockin_day = events_clockin.text
        events_clockin_time = events_clockin_day.split(" ")[0]
        events_clockin_decimal = int(events_clockin_time)
        Logging("Clock-In after change to decimal: " + str(events_clockin_decimal))

        tardiness = driver.find_element_by_xpath("//span[contains(.,'Tardiness')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Tardiness: " + tardiness.text)
        tardiness_day = tardiness.text
        tardiness_time = tardiness_day.split(" ")[0]
        tardiness_decimal = int(tardiness_time)
        Logging("Tardiness after change to decimal: " + str(tardiness_decimal))

        no_clockin = driver.find_element_by_xpath("//span[contains(.,'No Clock-In')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("No Clock-In: " + no_clockin.text)
        no_clockin_day = no_clockin.text
        no_clockin_time = no_clockin_day.split(" ")[0]
        no_clockin_decimal = int(no_clockin_time)
        Logging("No Clock-In after change to decimal: " + str(no_clockin_decimal))

        events_clockout = driver.find_element_by_xpath("//li[4]//span[contains(.,'Clock-Out')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Clock-Out: " + events_clockout.text)
        events_clockout_day = events_clockout.text
        events_clockout_time = events_clockout_day.split(" ")[0]
        events_clockout_decimal = int(events_clockout_time)
        Logging("Clock-Out after change to decimal: " + str(events_clockout_decimal))

        leave_early = driver.find_element_by_xpath("//span[contains(.,'Leave Early')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Leave Early: " + leave_early.text)
        leave_early_day = leave_early.text
        leave_early_time = leave_early_day.split(" ")[0]
        leave_early_decimal = int(leave_early_time)
        Logging("Leave Early after change to decimal: " + str(leave_early_decimal))

        no_clockout = driver.find_element_by_xpath("//span[contains(.,'No Clock-Out')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("No Clock-Out: " + no_clockout.text)
        no_clockout_day = no_clockout.text
        no_clockout_time = no_clockout_day.split(" ")[0]
        no_clockout_decimal = int(no_clockout_time)
        Logging("No Clock-Out after change to decimal: " + str(no_clockout_decimal))

        events_OT = driver.find_element_by_xpath("//li[7]//span[contains(.,'O/T')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("OT: " + events_OT.text)
        events_OT_day = events_OT.text
        events_OT_time = events_OT_day.split(" ")[0]
        events_OT_decimal = int(events_OT_time)
        Logging("OT after change to decimal: " + str(events_OT_decimal))

        night_shift = driver.find_element_by_xpath("//li[8]//span[contains(.,'Night shift')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Night shift: " + night_shift.text)
        night_shift_day = night_shift.text
        night_shift_time = night_shift_day.split(" ")[0]
        night_shift_decimal = int(night_shift_time)
        Logging("Night shift after change to decimal: " + str(night_shift_decimal))

        vacation = driver.find_element_by_xpath("//li[9]//span[contains(.,'Vacation')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Vacation: " + vacation.text)
        vacation_day = vacation.text
        vacation_time = vacation_day.split(" ")[0]
        vacation_decimal = int(vacation_time)
        Logging("Vacation after change to decimal: " + str(vacation_decimal))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["monthly_events"]["pass"])

    except:
        #Logging("Check data fail")
        Logging(red('>>>Check data failed', 'bright')) 

    try:
        Logging("")
        #Logging("List")
        Logging(yellow('***LIST***', 'bold')) 

        driver.find_element_by_xpath("//span[contains(.,'List')]").click()
        time.sleep(5)
        list_clockin = driver.find_element_by_xpath("//div[@class='list-wrapper']/div[2]/div[2]//span[@data-lang-id='Clock-In']/../following-sibling::div")
        Logging("Clock-In: " + list_clockin.text)
        list_clockin_day = list_clockin.text
        list_clockin_time = list_clockin_day.split(" ")[0]
        list_clockin_decimal = int(list_clockin_time)
        Logging("Clock-In after change to decimal: " + str(list_clockin_decimal))

        list_tardiness = driver.find_element_by_xpath("//span[contains(.,'Tardiness')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Tardiness: " + list_tardiness.text)
        list_tardiness_day = list_tardiness.text
        list_tardiness_time = list_tardiness_day.split(" ")[0]
        list_tardiness_decimal = int(list_tardiness_time)
        Logging("Tardiness after change to decimal: " + str(list_tardiness_decimal))


        list_no_clockin = driver.find_element_by_xpath("//span[contains(.,'No Clock-In')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("No Clock-In: " + list_no_clockin.text)
        list_no_clockin_day = list_no_clockin.text
        list_no_clockin_time = list_no_clockin_day.split(" ")[0]
        list_no_clockin_decimal = int(list_no_clockin_time)
        Logging("No Clock-In after change to decimal: " + str(list_no_clockin_decimal))

        list_clockout = driver.find_element_by_xpath("//div[@class='list-wrapper']/div[2]/div[2]//span[@data-lang-id='Clock-Out']/../following-sibling::div")
        Logging("Clock-Out: " + list_clockout.text)
        list_clockout_day = list_clockout.text
        list_clockout_time = list_clockout_day.split(" ")[0]
        list_clockout_decimal = int(list_clockout_time)
        Logging("No Clock-Out after change to decimal: " + str(list_clockout_decimal))


        list_leave_early = driver.find_element_by_xpath("//span[contains(.,'Leave Early')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Leave Early: " + list_leave_early.text)
        list_leave_early_day = list_leave_early.text
        list_leave_early_time = list_leave_early_day.split(" ")[0]
        list_leave_early_decimal = int(list_leave_early_time)
        Logging("Leave Early after change to decimal: " + str(list_leave_early_decimal))

        list_no_clockout = driver.find_element_by_xpath("//span[contains(.,'No Clock-Out')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("No Clock-Out: " + list_no_clockout.text)
        list_no_clockout_day = list_no_clockout.text
        list_no_clockout_time = list_no_clockout_day.split(" ")[0]
        list_no_clockout_decimal = int(list_no_clockout_time)
        Logging("No Clock-Out after change to decimal: " + str(list_no_clockout_decimal))

        list_OT = driver.find_element_by_xpath("//span[contains(.,'O/T')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("OT: " + list_OT.text)
        list_OT_day = list_OT.text
        list_OT_time = list_OT_day.split(" ")[0]
        list_OT_decimal = int(list_OT_time)
        Logging("OT after change to decimal: " + str(list_OT_decimal))

        list_night_shift = driver.find_element_by_xpath("//span[contains(.,'Night shift')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Night shift: " + list_night_shift.text)
        list_night_shift_day = list_night_shift.text
        list_night_shift_time = list_night_shift_day.split(" ")[0]
        list_night_shift_decimal = int(list_night_shift_time)
        Logging("Night shift after change to decimal: " + str(list_night_shift_decimal))

        list_vacation = driver.find_element_by_xpath("//span[contains(.,'Vacation')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Vacation: " + list_vacation.text)
        list_vacation_day = list_vacation.text
        list_vacation_time = list_vacation_day.split(" ")[0]
        list_vacation_decimal = int(list_vacation_time)
        Logging("Vacation after change to decimal: " + str(list_vacation_decimal))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["list_data"]["pass"])

    except:
        #Logging("Check data fail")
        Logging(red('>>>Check data failed', 'bright')) 

    try:
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Dashboard')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@data-lang-id,'tc_dashboard_name')]")))
        settlement = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Settlement')] ")))
        settlement.location_once_scrolled_into_view

        Logging("")
        #Logging("Settlement")
        Logging(yellow('Settlement', 'bold')) 

        settlement_holiday = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_status_day_holiday')]//..//div//span")
        Logging("Holiday: " + settlement_holiday.text)
        settlement_holiday_day = settlement_holiday.text
        settlement_holiday_time = settlement_holiday_day.split(" ")[0]
        settlement_holiday_decimal = int(settlement_holiday_time)
        Logging("Holiday after change to decimal: " + str(settlement_holiday_decimal))

        settlement_day_off = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_work_type_dayoff')]//..//div//span")
        Logging("Day off: " + settlement_day_off.text)
        settlement_day_off_day = settlement_day_off.text
        settlement_day_off_time = settlement_day_off_day.split(" ")[0]
        settlement_day_off_decimal = int(settlement_day_off_time)
        Logging("Day off after change to decimal: " + str(settlement_day_off_decimal))

        settlement_vacation = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_status_vacations')]//..//div//span")
        Logging("Vacation: " + settlement_vacation.text)
        settlement_vacation_day = settlement_vacation.text
        settlement_vacation_time = settlement_vacation_day.split(" ")[0]
        settlement_vacation_decimal = int(settlement_vacation_time)
        Logging("Vacation after change to decimal: " + str(settlement_vacation_decimal))
    

        #Compare
        Logging("")
        Logging("Compare Contractual working day with Scheduled Working")
        if working_day_number == working_day_number1:
            # Logging(working_day_number)
            # Logging(working_day_number1)
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright')) 

        Logging("")
        Logging("Compare Contractual worked day with Scheduled Working")
        if worked_day_number == worked_day_number1:
            # Logging(worked_day_number)
            # Logging(worked_day_number1)
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright')) 

        Logging("")
        Logging("Compare Report - avg worked time per day with Monhtly - Avg.Working time per day")
        if avg_worked_time_per_day_decimal == avg_working_time_per_day_decimal:
            # Logging(avg_worked_time_per_day_decimal)
            # Logging(avg_working_time_per_day_decimal)
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright')) 

        Logging("")
        Logging("Compare Report - avg worked time per week with Monhtly - Avg.Working time per week")
        if avg_worked_time_per_week_decimal == avg_working_time_per_week_decimal:
            # Logging(avg_worked_time_per_week_decimal)
            # Logging(avg_working_time_per_week_decimal)
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")    
            Logging(red('>>>Result was different - System was false', 'bright'))

        Logging("")
        Logging("Compare Events - Clockin with List - Clockin")
        if events_clockin_decimal == list_clockin_decimal:
            # Logging(events_clockin_decimal)
            # Logging(list_clockin_decimal)
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false") 
            Logging(red('>>>Result was different - System was false', 'bright'))

        Logging("")
        Logging("Compare Events - Tardiness with List - Tardiness")
        if tardiness_decimal == list_tardiness_decimal:
            #Logging(tardiness_decimal)
            #Logging(list_tardiness_decimal)
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright'))

        Logging("")
        Logging("Compare Events - No Clockin with List - No Clockin")
        if no_clockin_decimal == list_no_clockin_decimal:
            #Logging(no_clockin_decimal)
            #Logging(list_no_clockin_decimal)
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright'))

        Logging("")
        Logging("Compare Events - Clockout with List - Clockout")
        if events_clockout_decimal == list_clockout_decimal:
            #Logging(events_clockout_decimal)
            #Logging(list_clockout_decimal)
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright'))

        Logging("")
        Logging("Compare Events - Leave Early with List - Leave Early")
        if leave_early_decimal == list_leave_early_decimal:
            #Logging(leave_early_decimal)
            #Logging(list_leave_early_decimal)
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright'))

        Logging("")
        Logging("Compare Events - No Clockout with List - No Clockout")
        if no_clockout_decimal == list_no_clockout_decimal:
            #Logging(no_clockout_decimal)
            #Logging(list_no_clockout_decimal)
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright'))

        Logging("")
        Logging("Compare Events - OT with List - OT")
        if events_OT_decimal == list_OT_decimal:
            #Logging(events_OT_decimal)
            #Logging(list_OT_decimal)
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright'))

        Logging("")
        Logging("Compare Events - Night Shifts with List - Night Shifts")
        if night_shift_decimal == list_night_shift_decimal:
            #Logging(night_shift_decimal)
            #Logging(list_night_shift_decimal)
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright'))

        Logging("")
        Logging("Compare Events - Vacation with List - Vacation")
        if vacation_decimal == list_vacation_decimal:
            #Logging(vacation_decimal)
            #Logging(list_vacation_decimal)
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright'))

        Logging("")
        Logging("Compare Settlement - Holiday with Monthly Scheduled Working - Holiday")
        if settlement_holiday_decimal == holiday_number1:
            #Logging(settlement_holiday_decimal)
            #Logging(holiday_number1)
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright'))

        Logging("")
        Logging("Compare Settlement - Day off with Monthly Scheduled Working - Day off")
        if settlement_day_off_decimal == day_off_number1:
            #Logging(settlement_day_off_decimal)
            #Logging(day_off_number1)
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright'))

        Logging("")
        Logging("Compare Settlement - Vacation with Monthly Scheduled Working - Vacation")
        if settlement_vacation_decimal == scheduled_working_vacation_number1:
            #Logging(settlement_vacation_decimal)
            #Logging(scheduled_working_vacation_number1)
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright')) 
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright'))
    except:
        #Logging("Can't compare")
        Logging(red('>>>Cant compare', 'bright')) 


def timeline():
    try:
        Logging("")
        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Timeline')]").click()
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Filters')] ")))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["access_timeline_page"]["pass"])

        driver.find_element_by_xpath("//div[contains(@class,'main-side-container-history')]/../../div[1]").click()
        time.sleep(5)
        try:
            icon = driver.find_element_by_xpath("//*[@id='popover-tree']")
            if icon.is_displayed():
                Logging("Able to open the organization box")
        except:
            #Logging("False")
            Logging(red('>>>Cant open organization box', 'bright')) 
        
        tl_search2 = driver.find_element_by_xpath("//input[contains(@class,'form-control')]")
        tl_search2.send_keys(data["name_keyword"][0])
        tl_search2.send_keys(Keys.ENTER)

        time.sleep(5)
        driver.find_element_by_xpath("//div[contains(@class,'avatar-wrapper')]//li").click()
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["search_user"]["pass"])
        time.sleep(5)
        driver.find_element_by_xpath("//div[contains(@class,'main-side-container-history')]/../../div[1]").click()

        # try:
        #     icon = driver.find_element_by_xpath("//*[@id='popover-tree']")
        #     if icon.is_displayed():
        #         Logging("Fail to close the organization box")
        # except:
        #     Logging("Success to close the organization box")

        filters_all = driver.find_element_by_xpath("//div[contains(@class,'select-wrapper')]/div")
        time.sleep(3)
        filters_all.click()
        time.sleep(3)
        filters_input = driver.find_element_by_xpath("//input[starts-with(@id, 'react-select')]")
        filters_input.send_keys(Keys.ARROW_DOWN)
        filters_input.send_keys(Keys.ENTER)
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["timeline_filter"]["pass"])

        time.sleep(3)
        delete = driver.find_element_by_xpath("//div[contains(@class, 'timeline-item  ')]//div[contains(.,'Clock-In')]//div[contains(@class, 'd-flex ')]//span[2]//div[contains(@class, 'cursor-pointer')]").click()
        delete1 = driver.find_element_by_xpath("//button//span[contains(.,'Delete')] ").click()
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["delete_login"]["pass"])
    except:
        #Logging("Can't delete login")
        Logging(red('>>>Cant delete login', 'bright')) 

    try:
        time.sleep(3)
        add_schedule = driver.find_element_by_xpath("//div[contains(@class, 'pos-relative')]//button//div[contains(@class, 'cursor-pointer')]").click()
        time.sleep(3)
        add_schedu = driver.find_element_by_xpath("//span[contains(.,'Clock In/Out')] ").click()
        time.sleep(3)

        Logging("")
        time_select = driver.find_element_by_xpath("//button[starts-with(@id, 'btnHours')]").click()
        time.sleep(5)
        hour = driver.find_element_by_xpath("//div[starts-with(@id, 'dropdown')]//div//button[contains(.,'07')]").click()
        save = driver.find_element_by_xpath("//span[contains(.,'Save')]").click()
        #Logging("Clock-in through timeline successfully")  
        Logging(green('>>>Clock-in through timeline successfully', 'bright'))   
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["clockin_through_timeline"]["pass"])
    except:
        #Logging("Can't clock in through timeline")
        Logging(red('>>>Cant clock in through timeline', 'bright')) 
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["clockin_through_timeline"]["fail"])

    try:
        time.sleep(3)
        add_schedule1 = driver.find_element_by_xpath("//div[contains(@class, 'pos-relative')]//button//div[contains(@class, 'cursor-pointer')]").click()
        time.sleep(3)
        add_schedu1 = driver.find_element_by_xpath("//span[contains(.,'Clock In/Out')] ").click()
        time.sleep(5)
        time_select2 = driver.find_element_by_xpath("//button[starts-with(@id, 'btnHours')]").click()
        time.sleep(5)
        hour2 = driver.find_element_by_xpath("//div[starts-with(@id, 'dropdown')]//div//button[contains(.,'16')]").click()
        clock_out = driver.find_element_by_xpath("//div[contains(@class,'custom-control custom-radio')]//span[contains(.,'Clock-Out')]").click()
        time.sleep(5)
        save2 = driver.find_element_by_xpath("//span[contains(.,'Save')]").click()
        #Logging("Clock-out through timeline successfully")
        Logging(green('>>>Clock-out through timeline successfully', 'bright')) 
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["clockout_through_timeline"]["pass"])
    except:
        #Logging("Can't clock out through timeline")
        Logging(red('>>>Cant clock-out through timeline', 'bright'))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["clockout_through_timeline"]["fail"])
    try:
        time.sleep(5)
        clockin_time_a = driver.find_element_by_xpath("//div[contains(@class,'timeline-group')]//div[1]//nav//div[5]")
        Logging("Clockin: " + clockin_time_a.text)
        g = clockin_time_a.text

        filters_all = driver.find_element_by_xpath("//div[contains(@class,'select-wrapper')]/div")
        time.sleep(3)
        filters_all.click()
        time.sleep(3)
        filters_input = driver.find_element_by_xpath("//input[starts-with(@id, 'react-select')]")
        filters_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(2)
        filters_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(2)
        filters_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(2)
        filters_input.send_keys(Keys.ENTER)
        time.sleep(3)


        clockout_time_a = driver.find_element_by_xpath("//div[contains(@class,'timeline-group')]//div[1]//nav//div[5]")
        Logging("Clockout: " + clockout_time_a.text)
        h = clockout_time_a.text


        Logging("")
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Dashboard')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@data-lang-id,'tc_dashboard_name')]")))
        dashboard_clockin = driver.find_element_by_xpath("//div[contains(@class,'check-in-status')]").text
        Logging("Dashboard - Clockin: " + dashboard_clockin)
        dashboard_clockout = driver.find_element_by_xpath("//div[contains(@class,'check-out-status')]").text
        Logging("Dashboard - Clockout: " + dashboard_clockout)

        Logging("")
        Logging("Compare timeline clockin and dashboard clockin")
        # Logging(g)
        # Logging(dashboard_clockin)
        if g == dashboard_clockin:
            #Logging("Result was the same - Data was displayed")
            Logging(green('>>>Result was different - Data was displayed', 'bright'))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["timeline_clockin_data"]["pass"])
        else:
            #Logging("Result was different - Data not displayed")
            Logging(red('>>>Result was different - Data not displayed', 'bright'))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["timeline_clockin_data"]["fail"])
        Logging("Compare timeline clockout and dashboard clockout")
        # Logging(h)
        # Logging(dashboard_clockout)
        if h == dashboard_clockout:
            #Logging("Result was the same - System was correct")
            Logging(green('>>>Result was the same - System was correct', 'bright'))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["timeline_clockout_data"]["pass"])
        else:
            #Logging("Result was different - System was false")
            Logging(red('>>>Result was different - System was false', 'bright'))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["timeline_clockout_data"]["fail"])
    except:
        Logging("Data is not displayed")
        #Logging(red('>>>Data is not displayed', 'bright'))


def work_shift():
    time.sleep(5)
    driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Work Shifts')]").click()
    TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["access_workshift_page"]["pass"])

    time.sleep(5)
    driver.find_element_by_xpath("//div[contains(@class,'working-setting-content')]/../../div[1]").click()
    wss_search2 = driver.find_element_by_xpath("//input[contains(@class,'form-control')]")
    wss_search2.send_keys(data["name_keyword"][0])
    wss_search2.send_keys(Keys.ENTER)
    time.sleep(3)
    driver.find_element_by_xpath("//div[contains(@class,'visible')]//li").click()
    driver.find_element_by_xpath("//div[contains(@class,'working-setting-content')]/../../div[1]").click()

    Logging("")
    Logging("***Work Shift Default***")
    time.sleep(3)
    working_method = driver.find_element_by_xpath("//div[contains(@class,'work-method-name')]")
    Logging("Work method: " + working_method.text)

    star_date = driver.find_element_by_xpath("//*[@col-id='start_date']//div[contains(@class,'ag-react-container')]//div//div")
    Logging("Star date: " + star_date.text)

    work_days = driver.find_element_by_xpath("//*[@col-id='weekday']//div[contains(@class,'ag-react-container')]//div//div")
    Logging("Work days: " + work_days.text)
    work_days_time = work_days.text
    work_days_hour = work_days_time.split(" ")[0]
    work_days_number = int(work_days_hour)
    Logging("Work days after change to decimal: " + str(work_days_number))

    working_time_per_day = driver.find_element_by_xpath("//div[contains(@class,'work-hours')]/../div[1]")
    Logging("Working time per day: " + working_time_per_day.text)
    working_time_per_day_time = working_time_per_day.text
    working_time_per_day_hour = working_time_per_day_time.split(" ")[0]
    working_time_per_day_number = int(working_time_per_day_hour)
    Logging("Working time per day after change to decimal: " + str(working_time_per_day_number))

    max_working_time = driver.find_element_by_xpath("//*[@col-id='max_overtime']//div[contains(@class,'ag-react-container')]//div//div")
    Logging("Max working time per day: " + max_working_time.text)
    max_working_time_time = max_working_time.text
    max_working_time_hour = max_working_time_time.split(" ")[0]
    max_working_time_number = int(max_working_time_hour)
    Logging("Max working time per day after change to decimal: " + str(max_working_time_number))

    working_time_per_week = driver.find_element_by_xpath("//*[@col-id='base_work_week']//div[contains(@class,'ag-react-container')]")
    Logging("Working time per week: " + working_time_per_week.text)
    working_time_per_week_time = working_time_per_week.text
    working_time_per_week_hour = working_time_per_week_time.split(" ")[0]
    working_time_per_week_number = int(working_time_per_week_hour)
    Logging("Working time per week after change to decimal: " + str(working_time_per_week_number))

    time.sleep(3)
    driver.find_element_by_xpath("//*[@col-id='id']//div[contains(@class,'cursor-pointer')]").click()
    time.sleep(3)
    driver.find_element_by_xpath("//button[contains(@type,'button') and contains(.,'Add')]").click()
    time.sleep(3)
    #Select work type
    select_work_type = driver.find_element_by_xpath("//span[contains(.,'Work Type')]/../..//div[contains(@class,'singleValue')]").click()
    select_work_type_input = driver.find_element_by_xpath("//span[contains(.,'Work Type')]/../..//div[contains(@class,'singleValue')]/..//input[starts-with(@id, 'react-select')]")
    select_work_type_input.send_keys(Keys.ENTER)

    #Select work place
    select_work_type = driver.find_element_by_xpath("//span[contains(.,'Work Place')]/../..//div[contains(@class,'placeholder')]").click()
    select_work_type_input = driver.find_element_by_xpath("//span[contains(.,'Work Place')]/../..//div[contains(@class,'placeholder')]/..//input[starts-with(@id, 'react-select')]")
    select_work_type_input.send_keys(Keys.ENTER)

    #Select end date
    select_end_date = driver.find_element_by_xpath("//span[contains(.,'Use')]").click()

    #Select work type2
    select_work_type2 = driver.find_element_by_xpath("//div[contains(@class,'select-wrapper')]//div[contains(@class,'placeholder')]").click()
    select_work_type_input2 = driver.find_element_by_xpath("//div[contains(@class,'placeholder')]/..//input")
    select_work_type_input2.send_keys(Keys.ENTER)
    time.sleep(2)

    #Save
    #driver.find_element_by_xpath("//button[contains(@form,'form-add-shift-id')]").click()
    # Logging("Setup new work type successfully")
    # TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["work_type"]["pass"])


def work_place():
    try:
        time.sleep(7)
        #Before edit work place
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Work Place')]").click()
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//*[@id='form-holiday-setting']")))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["access_workplace_page"]["pass"])

        driver.find_element_by_xpath("//div[contains(@class,'title-section')]//button[contains(@type,'button')]").click()
        #Input name
        input_name = driver.find_element_by_xpath("//*[@id='name']/div/input")
        #input_name.clear()
        input_name.send_keys("test01.06")
        input_name.send_keys(Keys.ENTER)
        time.sleep(3)

        #Input location
        select_location = driver.find_element_by_xpath("//*[@id='nation']/div").click()
        select_location_input = driver.find_element_by_xpath("//span[contains(.,'Location')]/..//input[starts-with(@id, 'states-autocomplete')]")
        select_location_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(2)
        select_location_input.send_keys(Keys.ARROW_DOWN)
        select_location_input.send_keys(Keys.ENTER)

        #Input time zone
        select_timezone = driver.find_element_by_xpath("//*[@id='timezone']/div").click()
        select_timezone_input = driver.find_element_by_xpath("//span[contains(.,'Time Zone')]/..//input[starts-with(@id, 'states-autocomplete')]")
        select_timezone_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(2)
        select_timezone_input.send_keys(Keys.ARROW_DOWN)
        select_timezone_input.send_keys(Keys.ENTER)

        #Add
        time.sleep(3)
        driver.find_element_by_xpath("/html/body/div[4]/div").click()
        add_button = driver.find_element_by_xpath("//span[contains(.,'Add')]/../../button").click()
        Logging("")
        #Logging("Add work place successfully")
        work_place_noti =  driver.find_element_by_xpath("//*[starts-with(@id,'noty_bar')]//div[contains(@class,'alert-body')]")
        if work_place_noti.text == "Duplicated data exists":
            Logging("Duplicated data is available")
        elif work_place_noti.text == "Data inserted successfully.":
            Logging(green('>>>Add work place successfully', 'bright'))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["work_place"]["pass"])
    except:
        #Logging("Add work place fail")
        Logging(red('>>>Add work place failed', 'bright'))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["work_place"]["fail"])

        
    try:
        driver.find_element_by_xpath("//div[contains(@class,'title-section')]//button[contains(@type,'button')]").click()
        time.sleep(3)
        driver.find_element_by_xpath("//div[contains(@class,'list-work-places')]//li[1]/a/div[1]").click()
        work_place_data = driver.find_element_by_xpath("//div[contains(@class,'pos-absolute')]//div/ul/li[1]").text
        Logging("Work place before edit: " + work_place_data)

        #Add holiday
        driver.find_element_by_xpath("//div[contains(@class,'pos-absolute')]//div[2]/div[1]/button").click()

        #Input holiday name
        time.sleep(3)
        holiday_name = "hoiday" + date_id
        driver.find_element_by_xpath("//*[@id='form-holiday-setting']//*[@col-id='name']/div/input").send_keys(holiday_name)
        #Logging("Input Holiday name" )
        time.sleep(3)


        #Select holiday
        holiday_type_list = ["Legal Holiday",  "Company Holiday",  "Substitute Holiday"]
        select_holiday_type = Select(driver.find_element_by_xpath("//*[@id='form-holiday-setting']//select"))
        select_holiday_type.select_by_visible_text(random.choice(holiday_type_list))

        #Save holiday
        Logging("")
        holiday_save = driver.find_element_by_xpath("//button[starts-with(@id, 'btn-submit')]").click()
        #Logging("Add new holiday successfully")
        holiday_noti =  driver.find_element_by_xpath("//*[starts-with(@id,'noty_bar')]//div[contains(@class,'alert-body')]")
        if holiday_noti.text == "There is duplicated data, please try again":
            Logging("Duplicated data is available")
        elif holiday_noti.text == "Data saved successfully.":
            Logging(green('>>>Add work holiday successfully', 'bright'))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["holiday"]["pass"])
    except:
        #Logging("Add new holiday fail")
        Logging(red('>>>Add work holiday failed', 'bright'))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["holiday"]["fail"])

    try:
        time.sleep(5)
        holiday_data_before = driver.find_element_by_xpath("//*[@col-id='name']//span/div/div/div").text
        Logging("Holiday name before edit: " + holiday_data_before)


        #After edit work place
        #Edit work place
        time.sleep(3)
        work_place_edit = driver.find_element_by_xpath("//*[@id='app']//li[1]/span").click()
        
        #Input name
        Logging("")
        input_other_name = driver.find_element_by_xpath("//*[@id='app']//li[1]/input")
        input_other_name.clear()
        input_other_name.send_keys("hanh06")
        driver.find_element_by_xpath("//*[@id='app']//li[1]/span[1]").click()
        time.sleep(5)
        input_other_name1 = driver.find_element_by_xpath("//div[contains(@class,'pos-absolute')]//div/ul/li[1]").text
        Logging("Work place after edit: " + input_other_name1)
        time.sleep(3)

        #Compare before and after edit
        Logging("")
        # Logging(work_place_data)
        # Logging(input_other_name1)
        if work_place_data == input_other_name1:
            #Logging("Edit work place failed")
            Logging(red('>>>Edit work place failed', 'bright'))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["edit_work_place"]["fail"])
        else:
            #Logging("Edit work place successfully")
            Logging(green('>>>Edit work place successfully', 'bright'))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["edit_work_place"]["pass"])
    except:
        #Logging("Edit work place failed")
        Logging(red('>>>Edit work place failed', 'bright'))

    try:
        #Edit holiday
        driver.find_element_by_xpath("//button[starts-with(@id, 'btn-edit')]").click()

        #Edit holiday name
        edit_name = driver.find_element_by_xpath("//*[@col-id='name']/div/input")
        edit_name.clear()
        edit_name.send_keys("test")

        holiday_type_list = ["Legal Holiday",  "Company Holiday",  "Substitute Holiday"]
        select_holiday_type = Select(driver.find_element_by_xpath("//*[@id='form-holiday-setting']//select"))
        select_holiday_type.select_by_visible_text(random.choice(holiday_type_list))

        #Save
        Logging("")
        driver.find_element_by_xpath("//button[starts-with(@id, 'btn-submit')]").click()
        time.sleep(5)
        holiday_data_after = driver.find_element_by_xpath("//*[@col-id='name']//span/div/div/div").text
        Logging("Holiday name after edit: " + holiday_data_after)


        #Compare before and after edit
        Logging("")
        # Logging(holiday_data_before)
        # Logging(holiday_data_after)
        if holiday_data_before == holiday_data_after:
            #Logging("Edit holiday failed")
            Logging(red('>>>Edit holiday failed', 'bright'))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["edit_holiday"]["fail"])
        else:
            #Logging("Edit holiday successfully")
            Logging(green('>>>Edit holiday successfully', 'bright'))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["edit_holiday"]["pass"])
    except:
        #Logging("Edit holiday failed")
        Logging(red('>>>Edit holiday failed', 'bright'))


    try:
        #Delete holiday
        Logging("")
        driver.find_element_by_xpath("//button[starts-with(@id, 'btn-delete')]").click()
        driver.find_element_by_xpath("//button//span[contains(.,'Delete')] ").click()
        #Logging("Delete holiday successfully")
        Logging(green('>>>Delete holiday successfully', 'bright'))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["delete_holiday"]["pass"])
    except:
        #Logging("Delete work place fail")
        Logging(red('>>>Delete holiday failed', 'bright'))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["delete_holiday"]["fail"])
    
    try:
        #Delete work place
        time.sleep(3)
        Logging("")
        driver.find_element_by_xpath("//div[contains(@class,'list-work-places')]//li[contains(@class,'active')]//a/div[2]").click()
        driver.find_element_by_xpath("//button//span[contains(.,'Delete')]").click()
        #Logging("Delete work place successfully")
        Logging(green('>>>Delete work place successfully', 'bright'))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["delete_work_place"]["pass"])
    except:
        #Logging("Delete work place fail")
        Logging(red('>>>Delete work place failed', 'bright'))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["delete_work_place"]["fail"])


def report_weekly():
    Logging(" ")
    Logging(yellow('***REPORTS - WEEKLY***', ['bold', 'underlined']))
    Logging(yellow('***Device', 'bold'))
    time.sleep(4)
    try:
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Dashboard')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@data-lang-id,'tc_dashboard_name')]")))
        #Device - Default
        device_scroll = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Settlement')] ")))
        device_scroll.location_once_scrolled_into_view
        time.sleep(3)

        device_web1 = driver.find_element_by_xpath("//div[contains(@class, 'chart-description-wrapper')]/div[1]/div[2]/div/div").text
        #Logging("Web: " + device_web1.text)
        device_wifi1 = driver.find_element_by_xpath("//div[contains(@class, 'chart-description-wrapper')]/div[2]/div[2]/div/div").text
        #Logging("Wifi: " + device_wifi1.text)
        device_gps1 = driver.find_element_by_xpath("//div[contains(@class, 'chart-description-wrapper')]/div[3]/div[2]/div/div").text
        #Logging("GPS: " + device_gps1.text)
        device_beacon1 = driver.find_element_by_xpath("//div[contains(@class, 'chart-description-wrapper')]/div[4]/div[2]/div/div").text
        #Logging("Beacon: " + device_beacon1.text)
    except:
        Logging(red('>>>Check data fail', 'bright'))

    try:
        driver.find_element_by_xpath("//a[contains(@href,'/nhr/hr/timecard/user/statistics')]").click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Working status')] ")))
        driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_cal_weekly')]").click()
        time.sleep(5)
    except:
        Logging(" ")

    #Check data of device
    try:
        report_web = driver.find_element_by_xpath("//div[contains(@class, 'chart-description-wrapper')]/div[1]/div[2]/div/div").text
        Logging("Web: " + report_web)
        report_wifi = driver.find_element_by_xpath("//div[contains(@class, 'chart-description-wrapper')]/div[2]/div[2]/div/div").text
        Logging("Wifi: " + report_wifi)
        report_gps = driver.find_element_by_xpath("//div[contains(@class, 'chart-description-wrapper')]/div[3]/div[2]/div/div").text
        Logging("GPS: " + report_gps)
        report_beacon = driver.find_element_by_xpath("//div[contains(@class, 'chart-description-wrapper')]/div[4]/div[2]/div/div").text
        Logging("Beacon: " + report_beacon)
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["report_device_data"]["pass"])
    except:
        Logging(red('>>>Data is not displayed', 'bright'))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["report_device_data"]["fail"])

    #Compare Dashboard-Device and Reports-Weekly-Device
    time.sleep(3)
    try:
        try:
            if device_web1 == report_web:
                #Logging("Web - Data is the same")
                Logging(green('>>>Web - Data is the same', 'bright'))
        except:
            #Logging("Web - Data is different")
            Logging(red('>>>Web - Data is the different', 'bright'))

        try:
            if device_wifi1 == report_wifi:
                #Logging("Wifi - Data is the same")
                Logging(green('>>>Wifi - Data is the same', 'bright'))
        except:
            #Logging("Wifi - Data is different")
            Logging(red('>>>Wifi - Data is the different', 'bright'))

        try:
            if device_gps1 == report_gps:
                #Logging("GPS - Data is the same")
                Logging(green('>>>GPS - Data is the same', 'bright'))
        except:
            #Logging("GPS - Data is different")
            Logging(red('>>>GPS - Data is the different', 'bright'))

        try:
            if device_beacon1 == report_beacon:
                #Logging("Beacon - Data is the same")
                Logging(green('>>>Beacon - Data is the same', 'bright'))
        except:
            #Logging("Beacon - Data is different")
            Logging(red('>>>Beacon - Data is the different', 'bright'))
    except:
        #Logging("Can't compare")
        Logging(red('>>>Cant compare', 'bright'))


    Logging(" ")
    # Logging(yellow('***Weekly working time', 'bold'))
    # wwt_chart = driver.find_element_by_xpath("//div[contains(@data-lang-id, 'tc_title_week_schedule_msg')]/..//canvas")
    try:
        Logging(yellow('***Weekly working time', 'bold'))
        wwt_chart = driver.find_element_by_xpath("//div[contains(@data-lang-id, 'tc_title_week_schedule_msg')]/..//canvas")
        if wwt_chart.is_displayed():
            #Logging("Weekly working time - Data is displayed")
            Logging(green('>>>Weekly working time - Data is displayed', 'bright'))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["report_weekly_working_time_data"]["pass"])
    except:
        #Logging("Weekly working time - Data is empty")
        Logging(red('>>>Weekly working time - Data is empty', 'bright'))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["report_weekly_working_time_data"]["fail"])


    Logging(" ")
    #Logging("Average working hour per week")
    Logging(yellow('***Average working hour per week', 'bold'))

    try:
        Logging("1st week")
        #Calculation on 1st week
        time.sleep(3)
        Fst_working_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Working time')]/../../../..//div[contains(.,'1st Week')]//..//../td[2]//div[1]")
        Logging("Working time: " + Fst_working_time.text)
        workingtime_1 = Fst_working_time.text
        try:
            minute_workingtime_1 = workingtime_1.split(" ")[1]
            minutes_workingtime_1 = minute_workingtime_1.split("m")[0]
            minutes_number_workingtime_1 = int(minutes_workingtime_1)
            #Logging(minutes_number_workingtime_1)
            hour_workingtime_1 = workingtime_1.split(" ")[0]
            #Logging(hour_monday_time)
            hours_workingtime_1 = hour_workingtime_1.split("H")[0]
            hour_number_workingtime_1 = int(hours_workingtime_1)
            #Logging(hour_number_workingtime_1)
            workingtime_decimal1 = ((minutes_number_workingtime_1) / 60) + (hour_number_workingtime_1)
            #Logging("monday after change to decimal: " + str(workingtime_decimal))
            #Logging("Working time after change to decimal: " + str(round(workingtime_decimal1, 2)))
        except:
            hour_workingtime_1 = workingtime_1.split(" ")[0]
            #Logging(hour_monday_time)
            hours_workingtime_1 = hour_workingtime_1.split("H")[0]
            hour_number_workingtime_1 = int(hours_workingtime_1)
            #Logging(hour_number_monday_time2)
            workingtime_decimal1 = hour_number_workingtime_1
            #Logging("Working time after change to decimal: " + str(workingtime_decimal1))
        
        Fst_break_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Break Time')]/../../../..//div[contains(.,'1st Week')]//..//../td[3]//div[1]")
        Logging("Break time: " + Fst_break_time.text)
        breaktime_1 = Fst_break_time.text
        try:
            minute_breaktime_1 = breaktime_1.split(" ")[1]
            minutes_breaktime_1 = minute_breaktime_1.split("m")[0]
            minutes_number_breaktime_1 = int(minutes_breaktime_1)
            #Logging(minutes_number_breaktime_1)
            hour_breaktime_1 = breaktime_1.split(" ")[0]
            #Logging(hour_monday_time)
            hours_breaktime_1 = hour_breaktime_1.split("H")[0]
            hour_number_breaktime_1 = int(hours_breaktime_1)
            #Logging(hour_number_breaktime_1)
            breaktime_decimal1 = ((minutes_number_breaktime_1) / 60) + (hour_number_breaktime_1)
            #Logging("monday after change to decimal: " + str(breaktime_decimal))
            #Logging("Break time after change to decimal: " + str(round(breaktime_decimal1, 2)))
        except:
            hour_breaktime_1 = breaktime_1.split(" ")[0]
            #Logging(hour_monday_time)
            hours_breaktime_1 = hour_breaktime_1.split("H")[0]
            hour_number_breaktime_1 = int(hours_breaktime_1)
            #Logging(hour_number_monday_time2)
            breaktime_decimal1 = hour_number_breaktime_1
            #Logging("Break time after change to decimal: " + str(breaktime_decimal1))

        Fst_OT_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'O/T')]/../../../..//div[contains(.,'1st Week')]//..//../td[4]//div[1]")
        Logging("OT time: " + Fst_OT_time.text)
        OTtime_1 = Fst_OT_time.text
        try:
            minute_OTtime_1 = OTtime_1.split(" ")[1]
            minutes_OTtime_1 = minute_OTtime_1.split("m")[0]
            minutes_number_OTtime_1 = int(minutes_OTtime_1)
            #Logging(minutes_number_OTtime_1)
            hour_OTtime_1 = OTtime_1.split(" ")[0]
            #Logging(hour_monday_time)
            hours_OTtime_1 = hour_OTtime_1.split("H")[0]
            hour_number_OTtime_1 = int(hours_OTtime_1)
            #Logging(hour_number_OTtime_1)
            OTtime_decimal1 = ((minutes_number_OTtime_1) / 60) + (hour_number_OTtime_1)
            #Logging("monday after change to decimal: " + str(OTtime_decimal))
            #Logging("OT time after change to decimal: " + str(round(OTtime_decimal1, 2)))
        except:
            hour_OTtime_1 = OTtime_1.split(" ")[0]
            #Logging(hour_monday_time)
            hours_OTtime_1 = hour_OTtime_1.split("H")[0]
            hour_number_OTtime_1 = int(hours_OTtime_1)
            #Logging(hour_number_monday_time2)
            OTtime_decimal1 = hour_number_OTtime_1
            #Logging("OT time after change to decimal: " + str(OTtime_decimal1))

        Fst_total_working_hour_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Total Working hour')]/../../../..//div[contains(.,'1st Week')]//..//../td[5]//div[1]")
        Logging("Total working hour: " + Fst_total_working_hour_time.text)
        total_working_hour_time_1 = Fst_total_working_hour_time.text
        try:
            minute_total_working_hour_time_1 = total_working_hour_time_1.split(" ")[1]
            minutes_total_working_hour_time_1 = minute_total_working_hour_time_1.split("m")[0]
            minutes_number_total_working_hour_time_1 = int(minutes_total_working_hour_time_1)
            #Logging(minutes_number_total_working_hour_time_1)
            hour_total_working_hour_time_1 = total_working_hour_time_1.split(" ")[0]
            #Logging(hour_monday_time)
            hours_total_working_hour_time_1 = hour_total_working_hour_time_1.split("H")[0]
            hour_number_total_working_hour_time_1 = int(hours_total_working_hour_time_1)
            #Logging(hour_number_total_working_hour_time_1)
            total_working_hour_time_decimal1 = ((minutes_number_total_working_hour_time_1) / 60) + (hour_number_total_working_hour_time_1)
            #Logging("monday after change to decimal: " + str(total_working_hour_time_decimal))
            #Logging("Total working hour after change to decimal: " + str(round(total_working_hour_time_decimal1, 2)))
        except:
            hour_total_working_hour_time_1 = total_working_hour_time_1.split(" ")[0]
            #Logging(hour_monday_time)
            hours_total_working_hour_time_1 = hour_total_working_hour_time_1.split("H")[0]
            hour_number_total_working_hour_time_1 = int(hours_total_working_hour_time_1)
            #Logging(hour_number_monday_time2)
            total_working_hour_time_decimal1 = hour_number_total_working_hour_time_1
            #Logging("Total working hour after change to decimal: " + str(total_working_hour_time_decimal1))
    except:
        Logging("1st week - Data is empty")

    try:
        Logging(" ")
        Logging("2nd week")
        #Calculation on 1st week
        time.sleep(3)
        Snd_working_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Working time')]/../../../..//div[contains(.,'2nd Week')]//..//../td[2]//div[1]")
        Logging("Working time: " + Snd_working_time.text)
        workingtime_2 = Snd_working_time.text
        try:
            minute_workingtime_2 = workingtime_2.split(" ")[1]
            minutes_workingtime_2 = minute_workingtime_2.split("m")[0]
            minutes_number_workingtime_2 = int(minutes_workingtime_2)
            #Logging(minutes_number_workingtime_2)
            hour_workingtime_2 = workingtime_2.split(" ")[0]
            #Logging(hour_monday_time)
            hours_workingtime_2 = hour_workingtime_2.split("H")[0]
            hour_number_workingtime_2 = int(hours_workingtime_2)
            #Logging(hour_number_workingtime_2)
            workingtime_decimal2 = ((minutes_number_workingtime_2) / 60) + (hour_number_workingtime_2)
            #Logging("monday after change to decimal: " + str(workingtime_decimal2))
            #Logging("Working time after change to decimal: " + str(round(workingtime_decimal2, 2)))
        except:
            hour_workingtime_2 = workingtime_2.split(" ")[0]
            #Logging(hour_monday_time)
            hours_workingtime_2 = hour_workingtime_2.split("H")[0]
            hour_number_workingtime_2 = int(hours_workingtime_2)
            #Logging(hour_number_monday_time2)
            workingtime_decimal2 = hour_number_workingtime_2
            #Logging("Working time after change to decimal: " + str(workingtime_decimal2))
        
        Snd_break_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Break Time')]/../../../..//div[contains(.,'2nd Week')]//..//../td[3]//div[1]")
        Logging("Break time: " + Snd_break_time.text)
        breaktime_2 = Snd_break_time.text
        try:
            minute_breaktime_2 = breaktime_2.split(" ")[1]
            minutes_breaktime_2 = minute_breaktime_2.split("m")[0]
            minutes_number_breaktime_2 = int(minutes_breaktime_2)
            #Logging(minutes_number_breaktime_2)
            hour_breaktime_2 = breaktime_2.split(" ")[0]
            #Logging(hour_monday_time)
            hours_breaktime_2 = hour_breaktime_2.split("H")[0]
            hour_number_breaktime_2 = int(hours_breaktime_2)
            #Logging(hour_number_breaktime_2)
            breaktime_decimal2 = ((minutes_number_breaktime_2) / 60) + (hour_number_breaktime_2)
            #Logging("monday after change to decimal: " + str(breaktime_decimal2))
            #Logging("Break time after change to decimal: " + str(round(breaktime_decimal2, 2)))
        except:
            hour_breaktime_2 = breaktime_2.split(" ")[0]
            #Logging(hour_monday_time)
            hours_breaktime_2 = hour_breaktime_2.split("H")[0]
            hour_number_breaktime_2 = int(hours_breaktime_2)
            #Logging(hour_number_monday_time2)
            breaktime_decimal2 = hour_number_breaktime_2
            #Logging("Break time after change to decimal: " + str(breaktime_decimal2))

        Snd_OT_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'O/T')]/../../../..//div[contains(.,'2nd Week')]//..//../td[4]//div[1]")
        Logging("OT time: " + Snd_OT_time.text)
        OTtime_2 = Snd_OT_time.text
        try:
            minute_OTtime_2 = OTtime_2.split(" ")[1]
            minutes_OTtime_2 = minute_OTtime_2.split("m")[0]
            minutes_number_OTtime_2 = int(minutes_OTtime_2)
            #Logging(minutes_number_OTtime_2)
            hour_OTtime_2 = OTtime_2.split(" ")[0]
            #Logging(hour_monday_time)
            hours_OTtime_2 = hour_OTtime_2.split("H")[0]
            hour_number_OTtime_2 = int(hours_OTtime_2)
            #Logging(hour_number_OTtime_2)
            OTtime_decimal2 = ((minutes_number_OTtime_2) / 60) + (hour_number_OTtime_2)
            #Logging("monday after change to decimal: " + str(OTtime_decimal2))
            #Logging("OT time after change to decimal: " + str(round(OTtime_decimal2, 2)))
        except:
            hour_OTtime_2 = OTtime_2.split(" ")[0]
            #Logging(hour_monday_time)
            hours_OTtime_2 = hour_OTtime_2.split("H")[0]
            hour_number_OTtime_2 = int(hours_OTtime_2)
            #Logging(hour_number_monday_time2)
            OTtime_decimal2 = hour_number_OTtime_2
            #Logging("OT time after change to decimal: " + str(OTtime_decimal2))

        Snd_total_working_hour_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Total Working hour')]/../../../..//div[contains(.,'2nd Week')]//..//../td[5]//div[1]")
        Logging("Total working hour: " + Snd_total_working_hour_time.text)
        total_working_hour_time_2 = Snd_total_working_hour_time.text
        try:
            minute_total_working_hour_time_2 = total_working_hour_time_2.split(" ")[1]
            minutes_total_working_hour_time_2 = minute_total_working_hour_time_2.split("m")[0]
            minutes_number_total_working_hour_time_2 = int(minutes_total_working_hour_time_2)
            #Logging(minutes_number_total_working_hour_time_2)
            hour_total_working_hour_time_2 = total_working_hour_time_2.split(" ")[0]
            #Logging(hour_monday_time)
            hours_total_working_hour_time_2 = hour_total_working_hour_time_2.split("H")[0]
            hour_number_total_working_hour_time_2 = int(hours_total_working_hour_time_2)
            #Logging(hour_number_total_working_hour_time_2)
            total_working_hour_time_decimal2 = ((minutes_number_total_working_hour_time_2) / 60) + (hour_number_total_working_hour_time_2)
            #Logging("monday after change to decimal: " + str(total_working_hour_time_decimal))
            #Logging("Total working hour after change to decimal: " + str(round(total_working_hour_time_decimal2, 2)))
        except:
            hour_total_working_hour_time_2 = total_working_hour_time_2.split(" ")[0]
            #Logging(hour_monday_time)
            hours_total_working_hour_time_2 = hour_total_working_hour_time_2.split("H")[0]
            hour_number_total_working_hour_time_2 = int(hours_total_working_hour_time_2)
            #Logging(hour_number_monday_time2)
            total_working_hour_time_decimal2 = hour_number_total_working_hour_time_2
            #Logging("Total working hour after change to decimal: " + str(total_working_hour_time_decimal2))
    except:
        Logging("2nd week - Data is empty")

    try:
        Logging(" ")
        Logging("3rd week")
        #Calculation on 1st week
        time.sleep(3)
        Trd_working_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Working time')]/../../../..//div[contains(.,'3rd Week')]//..//../td[2]//div[1]")
        Logging("Working time: " + Trd_working_time.text)
        workingtime_3 = Trd_working_time.text
        try:
            minute_workingtime_3 = workingtime_3.split(" ")[1]
            minutes_workingtime_3 = minute_workingtime_3.split("m")[0]
            minutes_number_workingtime_3 = int(minutes_workingtime_3)
            #Logging(minutes_number_workingtime_3)
            hour_workingtime_3 = workingtime_3.split(" ")[0]
            #Logging(hour_monday_time)
            hours_workingtime_3 = hour_workingtime_3.split("H")[0]
            hour_number_workingtime_3 = int(hours_workingtime_3)
            #Logging(hour_number_workingtime_3)
            workingtime_decimal3 = ((minutes_number_workingtime_3) / 60) + (hour_number_workingtime_3)
            #Logging("monday after change to decimal: " + str(workingtime_decimal3))
            #Logging("Working time after change to decimal: " + str(round(workingtime_decimal3, 2)))
        except:
            hour_workingtime_3 = workingtime_3.split(" ")[0]
            #Logging(hour_monday_time)
            hours_workingtime_3 = hour_workingtime_3.split("H")[0]
            hour_number_workingtime_3 = int(hours_workingtime_3)
            #Logging(hour_number_monday_time3)
            workingtime_decimal3 = hour_number_workingtime_3
            #Logging("Working time after change to decimal: " + str(workingtime_decimal3))
        
        Trd_break_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Break Time')]/../../../..//div[contains(.,'3rd Week')]//..//../td[3]//div[1]")
        Logging("Break time: " + Trd_break_time.text)
        breaktime_3 = Trd_break_time.text
        try:
            minute_breaktime_3 = breaktime_3.split(" ")[1]
            minutes_breaktime_3 = minute_breaktime_3.split("m")[0]
            minutes_number_breaktime_3 = int(minutes_breaktime_3)
            #Logging(minutes_number_breaktime_3)
            hour_breaktime_3 = breaktime_3.split(" ")[0]
            #Logging(hour_monday_time)
            hours_breaktime_3 = hour_breaktime_3.split("H")[0]
            hour_number_breaktime_3 = int(hours_breaktime_3)
            #Logging(hour_number_breaktime_3)
            breaktime_decimal3 = ((minutes_number_breaktime_3) / 60) + (hour_number_breaktime_3)
            #Logging("monday after change to decimal: " + str(breaktime_decimal3))
            #Logging("Break time after change to decimal: " + str(round(breaktime_decimal3, 2)))
        except:
            hour_breaktime_3 = breaktime_3.split(" ")[0]
            #Logging(hour_monday_time)
            hours_breaktime_3 = hour_breaktime_3.split("H")[0]
            hour_number_breaktime_3 = int(hours_breaktime_3)
            #Logging(hour_number_monday_time3)
            breaktime_decimal3 = hour_number_breaktime_3
            #Logging("Break time after change to decimal: " + str(breaktime_decimal3))

        Trd_OT_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'O/T')]/../../../..//div[contains(.,'3rd Week')]//..//../td[4]//div[1]")
        Logging("OT time: " + Trd_OT_time.text)
        OTtime_3 = Trd_OT_time.text
        try:
            minute_OTtime_3 = OTtime_3.split(" ")[1]
            minutes_OTtime_3 = minute_OTtime_3.split("m")[0]
            minutes_number_OTtime_3 = int(minutes_OTtime_3)
            #Logging(minutes_number_OTtime_3)
            hour_OTtime_3 = OTtime_3.split(" ")[0]
            #Logging(hour_monday_time)
            hours_OTtime_3 = hour_OTtime_3.split("H")[0]
            hour_number_OTtime_3 = int(hours_OTtime_3)
            #Logging(hour_number_OTtime_3)
            OTtime_decimal3 = ((minutes_number_OTtime_3) / 60) + (hour_number_OTtime_3)
            #Logging("monday after change to decimal: " + str(OTtime_decimal3))
            #Logging("OT time after change to decimal: " + str(round(OTtime_decimal3, 2)))
        except:
            hour_OTtime_3 = OTtime_3.split(" ")[0]
            #Logging(hour_monday_time)
            hours_OTtime_3 = hour_OTtime_3.split("H")[0]
            hour_number_OTtime_3 = int(hours_OTtime_3)
            #Logging(hour_number_monday_time3)
            OTtime_decimal3 = hour_number_OTtime_3
            #Logging("OT time after change to decimal: " + str(OTtime_decimal3))

        Trd_total_working_hour_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Total Working hour')]/../../../..//div[contains(.,'3rd Week')]//..//../td[5]//div[1]")
        Logging("Total working hour: " + Trd_total_working_hour_time.text)
        total_working_hour_time_3 = Trd_total_working_hour_time.text
        try:
            minute_total_working_hour_time_3 = total_working_hour_time_3.split(" ")[1]
            minutes_total_working_hour_time_3 = minute_total_working_hour_time_3.split("m")[0]
            minutes_number_total_working_hour_time_3 = int(minutes_total_working_hour_time_3)
            #Logging(minutes_number_total_working_hour_time_3)
            hour_total_working_hour_time_3 = total_working_hour_time_3.split(" ")[0]
            #Logging(hour_monday_time)
            hours_total_working_hour_time_3 = hour_total_working_hour_time_3.split("H")[0]
            hour_number_total_working_hour_time_3 = int(hours_total_working_hour_time_3)
            #Logging(hour_number_total_working_hour_time_3)
            total_working_hour_time_decimal3 = ((minutes_number_total_working_hour_time_3) / 60) + (hour_number_total_working_hour_time_3)
            #Logging("monday after change to decimal: " + str(total_working_hour_time_decimal))
            #Logging("Total working hour after change to decimal: " + str(round(total_working_hour_time_decimal3, 2)))
        except:
            hour_total_working_hour_time_3 = total_working_hour_time_3.split(" ")[0]
            #Logging(hour_monday_time)
            hours_total_working_hour_time_3 = hour_total_working_hour_time_3.split("H")[0]
            hour_number_total_working_hour_time_3 = int(hours_total_working_hour_time_3)
            #Logging(hour_number_monday_time3)
            total_working_hour_time_decimal3 = hour_number_total_working_hour_time_3
            #Logging("Total working hour after change to decimal: " + str(total_working_hour_time_decimal3))
    except:
        Logging("3rd week - Data is empty")

    try:
        Logging(" ")
        Logging("4th week")
        #Calculation on 1st week
        time.sleep(3)
        Fth_working_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Working time')]/../../../..//div[contains(.,'4th Week')]//..//../td[2]//div[1]")
        Logging("Working time: " + Fth_working_time.text)
        workingtime_4 = Fth_working_time.text
        try:
            minute_workingtime_4 = workingtime_4.split(" ")[1]
            minutes_workingtime_4 = minute_workingtime_4.split("m")[0]
            minutes_number_workingtime_4 = int(minutes_workingtime_4)
            #Logging(minutes_number_workingtime_4)
            hour_workingtime_4 = workingtime_4.split(" ")[0]
            #Logging(hour_monday_time)
            hours_workingtime_4 = hour_workingtime_4.split("H")[0]
            hour_number_workingtime_4 = int(hours_workingtime_4)
            #Logging(hour_number_workingtime_4)
            workingtime_decimal4 = ((minutes_number_workingtime_4) / 60) + (hour_number_workingtime_4)
            #Logging("monday after change to decimal: " + str(workingtime_decimal4))
            #Logging("Working time after change to decimal: " + str(round(workingtime_decimal4, 2)))
        except:
            hour_workingtime_4 = workingtime_4.split(" ")[0]
            #Logging(hour_monday_time)
            hours_workingtime_4 = hour_workingtime_4.split("H")[0]
            hour_number_workingtime_4 = int(hours_workingtime_4)
            #Logging(hour_number_monday_time4)
            workingtime_decimal4 = hour_number_workingtime_4
            #Logging("Working time after change to decimal: " + str(workingtime_decimal4))
        
        Fth_break_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Break Time')]/../../../..//div[contains(.,'4th Week')]//..//../td[3]//div[1]")
        Logging("Break time: " + Fth_break_time.text)
        breaktime_4 = Fth_break_time.text
        try:
            minute_breaktime_4 = breaktime_4.split(" ")[1]
            minutes_breaktime_4 = minute_breaktime_4.split("m")[0]
            minutes_number_breaktime_4 = int(minutes_breaktime_4)
            #Logging(minutes_number_breaktime_4)
            hour_breaktime_4 = breaktime_4.split(" ")[0]
            #Logging(hour_monday_time)
            hours_breaktime_4 = hour_breaktime_4.split("H")[0]
            hour_number_breaktime_4 = int(hours_breaktime_4)
            #Logging(hour_number_breaktime_4)
            breaktime_decimal4 = ((minutes_number_breaktime_4) / 60) + (hour_number_breaktime_4)
            #Logging("monday after change to decimal: " + str(breaktime_decimal4))
            #Logging("Break time after change to decimal: " + str(round(breaktime_decimal4, 2)))
        except:
            hour_breaktime_4 = breaktime_4.split(" ")[0]
            #Logging(hour_monday_time)
            hours_breaktime_4 = hour_breaktime_4.split("H")[0]
            hour_number_breaktime_4 = int(hours_breaktime_4)
            #Logging(hour_number_monday_time4)
            breaktime_decimal4 = hour_number_breaktime_4
            #Logging("Break time after change to decimal: " + str(breaktime_decimal4))

        Fth_OT_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'O/T')]/../../../..//div[contains(.,'4th Week')]//..//../td[4]//div[1]")
        Logging("OT time: " + Fth_OT_time.text)
        OTtime_4 = Fth_OT_time.text
        try:
            minute_OTtime_4 = OTtime_4.split(" ")[1]
            minutes_OTtime_4 = minute_OTtime_4.split("m")[0]
            minutes_number_OTtime_4 = int(minutes_OTtime_4)
            #Logging(minutes_number_OTtime_4)
            hour_OTtime_4 = OTtime_4.split(" ")[0]
            #Logging(hour_monday_time)
            hours_OTtime_4 = hour_OTtime_4.split("H")[0]
            hour_number_OTtime_4 = int(hours_OTtime_4)
            #Logging(hour_number_OTtime_4)
            OTtime_decimal4 = ((minutes_number_OTtime_4) / 60) + (hour_number_OTtime_4)
            #Logging("monday after change to decimal: " + str(OTtime_decimal4))
            #Logging("OT time after change to decimal: " + str(round(OTtime_decimal4, 2)))
        except:
            hour_OTtime_4 = OTtime_4.split(" ")[0]
            #Logging(hour_monday_time)
            hours_OTtime_4 = hour_OTtime_4.split("H")[0]
            hour_number_OTtime_4 = int(hours_OTtime_4)
            #Logging(hour_number_monday_time4)
            OTtime_decimal4 = hour_number_OTtime_4
            #Logging("OT time after change to decimal: " + str(OTtime_decimal4))

        Fth_total_working_hour_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Total Working hour')]/../../../..//div[contains(.,'4th Week')]//..//../td[5]//div[1]")
        Logging("Total working hour: " + Fth_total_working_hour_time.text)
        total_working_hour_time_4 = Fth_total_working_hour_time.text
        try:
            minute_total_working_hour_time_4 = total_working_hour_time_4.split(" ")[1]
            minutes_total_working_hour_time_4 = minute_total_working_hour_time_4.split("m")[0]
            minutes_number_total_working_hour_time_4 = int(minutes_total_working_hour_time_4)
            #Logging(minutes_number_total_working_hour_time_4)
            hour_total_working_hour_time_4 = total_working_hour_time_4.split(" ")[0]
            #Logging(hour_monday_time)
            hours_total_working_hour_time_4 = hour_total_working_hour_time_4.split("H")[0]
            hour_number_total_working_hour_time_4 = int(hours_total_working_hour_time_4)
            #Logging(hour_number_total_working_hour_time_4)
            total_working_hour_time_decimal4 = ((minutes_number_total_working_hour_time_4) / 60) + (hour_number_total_working_hour_time_4)
            #Logging("monday after change to decimal: " + str(total_working_hour_time_decimal))
            #Logging("Total working hour after change to decimal: " + str(round(total_working_hour_time_decimal4, 2)))
        except:
            hour_total_working_hour_time_4 = total_working_hour_time_4.split(" ")[0]
            #Logging(hour_monday_time)
            hours_total_working_hour_time_4 = hour_total_working_hour_time_4.split("H")[0]
            hour_number_total_working_hour_time_4 = int(hours_total_working_hour_time_4)
            #Logging(hour_number_monday_time4)
            total_working_hour_time_decimal4 = hour_number_total_working_hour_time_4
            #Logging("Total working hour after change to decimal: " + str(total_working_hour_time_decimal4))
    except:
        Logging("4th week - Data is empty")

    try:
        Logging(" ")
        Logging("5th week")
        #Calculation on 1st week
        time.sleep(3)
        Fvth_working_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Working time')]/../../../..//div[contains(.,'5th Week')]//..//../td[2]//div[1]")
        Logging("Working time: " + Fvth_working_time.text)
        workingtime_5 = Fvth_working_time.text
        try:
            minute_workingtime_5 = workingtime_5.split(" ")[1]
            minutes_workingtime_5 = minute_workingtime_5.split("m")[0]
            minutes_number_workingtime_5 = int(minutes_workingtime_5)
            #Logging(minutes_number_workingtime_5)
            hour_workingtime_5 = workingtime_5.split(" ")[0]
            #Logging(hour_monday_time)
            hours_workingtime_5 = hour_workingtime_5.split("H")[0]
            hour_number_workingtime_5 = int(hours_workingtime_5)
            #Logging(hour_number_workingtime_5)
            workingtime_decimal5 = ((minutes_number_workingtime_5) / 60) + (hour_number_workingtime_5)
            #Logging("monday after change to decimal: " + str(workingtime_decimal5))
            #Logging("Working time after change to decimal: " + str(round(workingtime_decimal5, 2)))
        except:
            hour_workingtime_5 = workingtime_5.split(" ")[0]
            #Logging(hour_monday_time)
            hours_workingtime_5 = hour_workingtime_5.split("H")[0]
            hour_number_workingtime_5 = int(hours_workingtime_5)
            #Logging(hour_number_monday_time5)
            workingtime_decimal5 = hour_number_workingtime_5
            #Logging("Working time after change to decimal: " + str(workingtime_decimal5))
        
        Fvth_break_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Break Time')]/../../../..//div[contains(.,'5th Week')]//..//../td[3]//div[1]")
        Logging("Break time: " + Fvth_break_time.text)
        breaktime_5 = Fvth_break_time.text
        try:
            minute_breaktime_5 = breaktime_5.split(" ")[1]
            minutes_breaktime_5 = minute_breaktime_5.split("m")[0]
            minutes_number_breaktime_5 = int(minutes_breaktime_5)
            #Logging(minutes_number_breaktime_5)
            hour_breaktime_5 = breaktime_5.split(" ")[0]
            #Logging(hour_monday_time)
            hours_breaktime_5 = hour_breaktime_5.split("H")[0]
            hour_number_breaktime_5 = int(hours_breaktime_5)
            #Logging(hour_number_breaktime_5)
            breaktime_decimal5 = ((minutes_number_breaktime_5) / 60) + (hour_number_breaktime_5)
            #Logging("monday after change to decimal: " + str(breaktime_decimal5))
            #Logging("Break time after change to decimal: " + str(round(breaktime_decimal5, 2)))
        except:
            hour_breaktime_5 = breaktime_5.split(" ")[0]
            #Logging(hour_monday_time)
            hours_breaktime_5 = hour_breaktime_5.split("H")[0]
            hour_number_breaktime_5 = int(hours_breaktime_5)
            #Logging(hour_number_monday_time5)
            breaktime_decimal5 = hour_number_breaktime_5
            #Logging("Break time after change to decimal: " + str(breaktime_decimal5))

        Fvth_OT_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'O/T')]/../../../..//div[contains(.,'5th Week')]//..//../td[4]//div[1]")
        Logging("OT time: " + Fvth_OT_time.text)
        OTtime_5 = Fvth_OT_time.text
        try:
            minute_OTtime_5 = OTtime_5.split(" ")[1]
            minutes_OTtime_5 = minute_OTtime_5.split("m")[0]
            minutes_number_OTtime_5 = int(minutes_OTtime_5)
            #Logging(minutes_number_OTtime_5)
            hour_OTtime_5 = OTtime_5.split(" ")[0]
            #Logging(hour_monday_time)
            hours_OTtime_5 = hour_OTtime_5.split("H")[0]
            hour_number_OTtime_5 = int(hours_OTtime_5)
            #Logging(hour_number_OTtime_5)
            OTtime_decimal5 = ((minutes_number_OTtime_5) / 60) + (hour_number_OTtime_5)
            #Logging("monday after change to decimal: " + str(OTtime_decimal5))
            #Logging("OT time after change to decimal: " + str(round(OTtime_decimal5, 2)))
        except:
            hour_OTtime_5 = OTtime_5.split(" ")[0]
            #Logging(hour_monday_time)
            hours_OTtime_5 = hour_OTtime_5.split("H")[0]
            hour_number_OTtime_5 = int(hours_OTtime_5)
            #Logging(hour_number_monday_time5)
            OTtime_decimal5 = hour_number_OTtime_5
            #Logging("OT time after change to decimal: " + str(OTtime_decimal5))

        Fvth_total_working_hour_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Total Working hour')]/../../../..//div[contains(.,'5th Week')]//..//../td[5]//div[1]")
        Logging("Total working hour: " + Fvth_total_working_hour_time.text)
        total_working_hour_time_5 = Fvth_total_working_hour_time.text
        try:
            minute_total_working_hour_time_5 = total_working_hour_time_5.split(" ")[1]
            minutes_total_working_hour_time_5 = minute_total_working_hour_time_5.split("m")[0]
            minutes_number_total_working_hour_time_5 = int(minutes_total_working_hour_time_5)
            #Logging(minutes_number_total_working_hour_time_5)
            hour_total_working_hour_time_5 = total_working_hour_time_5.split(" ")[0]
            #Logging(hour_monday_time)
            hours_total_working_hour_time_5 = hour_total_working_hour_time_5.split("H")[0]
            hour_number_total_working_hour_time_5 = int(hours_total_working_hour_time_5)
            #Logging(hour_number_total_working_hour_time_5)
            total_working_hour_time_decimal5 = ((minutes_number_total_working_hour_time_5) / 60) + (hour_number_total_working_hour_time_5)
            #Logging("monday after change to decimal: " + str(total_working_hour_time_decimal))
            #Logging("Total working hour after change to decimal: " + str(round(total_working_hour_time_decimal5, 2)))
        except:
            hour_total_working_hour_time_5 = total_working_hour_time_5.split(" ")[0]
            #Logging(hour_monday_time)
            hours_total_working_hour_time_5 = hour_total_working_hour_time_5.split("H")[0]
            hour_number_total_working_hour_time_5 = int(hours_total_working_hour_time_5)
            #Logging(hour_number_monday_time5)
            total_working_hour_time_decimal5 = hour_number_total_working_hour_time_5
            #Logging("Total working hour after change to decimal: " + str(total_working_hour_time_decimal5))
    except:
        Logging("5th week - Data is empty")

    try:
        Logging(" ")
        Logging("6th week")
        #Calculation on 1st week
        time.sleep(3)
        Sth_working_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Working time')]/../../../..//div[contains(.,'6th Week')]//..//../td[2]//div[1]")
        Logging("Working time: " + Sth_working_time.text)
        workingtime_6 = Sth_working_time.text
        try:
            minute_workingtime_6 = workingtime_6.split(" ")[1]
            minutes_workingtime_6 = minute_workingtime_6.split("m")[0]
            minutes_number_workingtime_6 = int(minutes_workingtime_6)
            #Logging(minutes_number_workingtime_6)
            hour_workingtime_6 = workingtime_6.split(" ")[0]
            #Logging(hour_monday_time)
            hours_workingtime_6 = hour_workingtime_6.split("H")[0]
            hour_number_workingtime_6 = int(hours_workingtime_6)
            #Logging(hour_number_workingtime_6)
            workingtime_decimal6 = ((minutes_number_workingtime_6) / 60) + (hour_number_workingtime_6)
            #Logging("monday after change to decimal: " + str(workingtime_decimal6))
            #Logging("Working time after change to decimal: " + str(round(workingtime_decimal6, 2)))
        except:
            hour_workingtime_6 = workingtime_6.split(" ")[0]
            #Logging(hour_monday_time)
            hours_workingtime_6 = hour_workingtime_6.split("H")[0]
            hour_number_workingtime_6 = int(hours_workingtime_6)
            #Logging(hour_number_monday_time6)
            workingtime_decimal6 = hour_number_workingtime_6
            #Logging("Working time after change to decimal: " + str(workingtime_decimal6))
        
        Sth_break_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Break Time')]/../../../..//div[contains(.,'6th Week')]//..//../td[3]//div[1]")
        Logging("Break time: " + Sth_break_time.text)
        breaktime_6 = Sth_break_time.text
        try:
            minute_breaktime_6 = breaktime_6.split(" ")[1]
            minutes_breaktime_6 = minute_breaktime_6.split("m")[0]
            minutes_number_breaktime_6 = int(minutes_breaktime_6)
            #Logging(minutes_number_breaktime_6)
            hour_breaktime_6 = breaktime_6.split(" ")[0]
            #Logging(hour_monday_time)
            hours_breaktime_6 = hour_breaktime_6.split("H")[0]
            hour_number_breaktime_6 = int(hours_breaktime_6)
            #Logging(hour_number_breaktime_6)
            breaktime_decimal6 = ((minutes_number_breaktime_6) / 60) + (hour_number_breaktime_6)
            #Logging("monday after change to decimal: " + str(breaktime_decimal6))
            #Logging("Break time after change to decimal: " + str(round(breaktime_decimal6, 2)))
        except:
            hour_breaktime_6 = breaktime_6.split(" ")[0]
            #Logging(hour_monday_time)
            hours_breaktime_6 = hour_breaktime_6.split("H")[0]
            hour_number_breaktime_6 = int(hours_breaktime_6)
            #Logging(hour_number_monday_time6)
            breaktime_decimal6 = hour_number_breaktime_6
            #Logging("Break time after change to decimal: " + str(breaktime_decimal6))

        Sth_OT_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'O/T')]/../../../..//div[contains(.,'6th Week')]//..//../td[4]//div[1]")
        Logging("OT time: " + Sth_OT_time.text)
        OTtime_6 = Sth_OT_time.text
        try:
            minute_OTtime_6 = OTtime_6.split(" ")[1]
            minutes_OTtime_6 = minute_OTtime_6.split("m")[0]
            minutes_number_OTtime_6 = int(minutes_OTtime_6)
            #Logging(minutes_number_OTtime_6)
            hour_OTtime_6 = OTtime_6.split(" ")[0]
            #Logging(hour_monday_time)
            hours_OTtime_6 = hour_OTtime_6.split("H")[0]
            hour_number_OTtime_6 = int(hours_OTtime_6)
            #Logging(hour_number_OTtime_6)
            OTtime_decimal6 = ((minutes_number_OTtime_6) / 60) + (hour_number_OTtime_6)
            #Logging("monday after change to decimal: " + str(OTtime_decimal6))
            #Logging("OT time after change to decimal: " + str(round(OTtime_decimal6, 2)))
        except:
            hour_OTtime_6 = OTtime_6.split(" ")[0]
            #Logging(hour_monday_time)
            hours_OTtime_6 = hour_OTtime_6.split("H")[0]
            hour_number_OTtime_6 = int(hours_OTtime_6)
            #Logging(hour_number_monday_time6)
            OTtime_decimal6 = hour_number_OTtime_6
            #Logging("OT time after change to decimal: " + str(OTtime_decimal6))

        Sth_total_working_hour_time = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Total Working hour')]/../../../..//div[contains(.,'6th Week')]//..//../td[5]//div[1]")
        Logging("Total working hour: " + Sth_total_working_hour_time.text)
        total_working_hour_time_6 = Sth_total_working_hour_time.text
        try:
            minute_total_working_hour_time_6 = total_working_hour_time_6.split(" ")[1]
            minutes_total_working_hour_time_6 = minute_total_working_hour_time_6.split("m")[0]
            minutes_number_total_working_hour_time_6 = int(minutes_total_working_hour_time_6)
            #Logging(minutes_number_total_working_hour_time_6)
            hour_total_working_hour_time_6 = total_working_hour_time_6.split(" ")[0]
            #Logging(hour_monday_time)
            hours_total_working_hour_time_6 = hour_total_working_hour_time_6.split("H")[0]
            hour_number_total_working_hour_time_6 = int(hours_total_working_hour_time_6)
            #Logging(hour_number_total_working_hour_time_6)
            total_working_hour_time_decimal6 = ((minutes_number_total_working_hour_time_6) / 60) + (hour_number_total_working_hour_time_6)
            #Logging("monday after change to decimal: " + str(total_working_hour_time_decimal))
            #Logging("Total working hour after change to decimal: " + str(round(total_working_hour_time_decimal6, 2)))
        except:
            hour_total_working_hour_time_6 = total_working_hour_time_6.split(" ")[0]
            #Logging(hour_monday_time)
            hours_total_working_hour_time_6 = hour_total_working_hour_time_6.split("H")[0]
            hour_number_total_working_hour_time_6 = int(hours_total_working_hour_time_6)
            #Logging(hour_number_monday_time6)
            total_working_hour_time_decimal6 = hour_number_total_working_hour_time_6
            #Logging("Total working hour after change to decimal: " + str(total_working_hour_time_decimal6))
    except:
        Logging("6th week - Data is empty")


    #Plus working time, break time and OT time to see if the result is equal to total working hour or not
    try:
        Logging("")
        Logging("Plus working time, break time and OT time to see if the result is equal to total working hour or not")
        try:
            if round(workingtime_decimal1, 2) + round(breaktime_decimal1, 2) + round(OTtime_decimal1, 2) == round(total_working_hour_time_decimal1, 2):
                #Logging ("System is correct")
                Logging(green('>>>1st week - System is correct', 'bright'))
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["calculate_report_weekly"]["pass"])
            else:
                #Logging("System is false")
                Logging(red('>>>1st week - System is false', 'bright'))
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["calculate_report_weekly"]["fail"])
        except:
            Logging("1st week - Data is empty")

        try:
            if round(workingtime_decimal2, 2) + round(breaktime_decimal2, 2) + round(OTtime_decimal2, 2) == round(total_working_hour_time_decimal2, 2):
                #Logging ("System is correct")
                Logging(green('>>>2nd week - System is correct', 'bright'))
            else:
                #Logging("System is false")
                Logging(red('>>>2nd week - System is false', 'bright'))
        except:
            Logging("2nd week - Data is empty")
        
        try:
            if round(workingtime_decimal3, 2) + round(breaktime_decimal3, 2) + round(OTtime_decimal3, 2) == round(total_working_hour_time_decimal3, 2):
                #Logging ("System is correct")
                Logging(green('>>>3rd week - System is correct', 'bright'))
            else:
                #Logging("System is false")
                Logging(red('>>>3rd week - System is false', 'bright'))
        except:
            Logging("3rd week - Data is empty")

        try:
            if round(workingtime_decimal4, 2) + round(breaktime_decimal4, 2) + round(OTtime_decimal4, 2) == round(total_working_hour_time_decimal4, 2):
                #Logging ("System is correct")
                Logging(green('>>>4th week - System is correct', 'bright'))
            else:
                #Logging("System is false")
                Logging(red('>>>4th week - System is false', 'bright'))
        except:
            Logging("4th week - Data is empty")

        try:
            if round(workingtime_decimal5, 2) + round(breaktime_decimal5, 2) + round(OTtime_decimal5, 2) == round(total_working_hour_time_decimal5, 2):
                #Logging ("System is correct")
                Logging(green('>>>5th week - System is correct', 'bright'))
            else:
                #Logging("System is false")
                Logging(red('>>>5th week - System is false', 'bright'))
        except:
            Logging("5th week - Data is empty")

        try:
            if round(workingtime_decimal6, 2) + round(breaktime_decimal6, 2) + round(OTtime_decimal6, 2) == round(total_working_hour_time_decimal6, 2):
                #Logging ("System is correct")
                Logging(green('>>>6th week - System is correct', 'bright'))
            else:
                #Logging("System is false")
                Logging(red('>>>6th week - System is false', 'bright'))
        except:
            Logging("6th week - Data is empty")

    except:
        #Logging("System is false")
        Logging(red('>>>System is false', 'bright'))



    Logging(" ")
    Logging(yellow('***Working hours per day of the week', 'bold'))
    Logging("Weekly average")
    try:
        try:
            Logging("1st week")
            weekly_average1 = driver.find_element_by_xpath("//tr[1]/td[9]/div[contains(@class, 'total-work-hours-label')]")
            if weekly_average1.is_displayed():
                #Logging("Weekly working time - Data is displayed")
                Logging(green('>>>Data is displayed', 'bright'))
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["weekly_average"]["pass"])
        except:
            Logging("Data is empty")

        try:
            Logging(" ")
            Logging("2nd week")
            weekly_average2 = driver.find_element_by_xpath("//tr[2]/td[9]/div[contains(@class, 'total-work-hours-label')]")
            if weekly_average2.is_displayed():
                #Logging("Weekly working time - Data is displayed")
                Logging(green('>>>Data is displayed', 'bright'))
        except:
            Logging("Data is empty")

        try:
            Logging(" ")
            Logging("3rd week")
            weekly_average3 = driver.find_element_by_xpath("//tr[3]/td[9]/div[contains(@class, 'total-work-hours-label')]")
            if weekly_average3.is_displayed():
                #Logging("Weekly working time - Data is displayed")
                Logging(green('>>>Data is displayed', 'bright'))
        except:
            Logging("Data is empty")

        try:
            Logging(" ")
            Logging("4th week")
            weekly_average4 = driver.find_element_by_xpath("//tr[4]/td[9]/div[contains(@class, 'total-work-hours-label')]")
            if weekly_average4.is_displayed():
                #Logging("Weekly working time - Data is displayed")
                Logging(green('>>>Data is displayed', 'bright'))
        except:
            Logging("Data is empty")

        try:
            Logging(" ")
            Logging("5th week")
            weekly_average5 = driver.find_element_by_xpath("//tr[5]/td[9]/div[contains(@class, 'total-work-hours-label')]")
            if weekly_average5.is_displayed():
                #Logging("Weekly working time - Data is displayed")
                Logging(green('>>>Data is displayed', 'bright'))
        except:
            Logging("Data is empty")

        try:
            Logging(" ")
            Logging("6th week")
            weekly_average6 = driver.find_element_by_xpath("//tr[6]/td[9]/div[contains(@class, 'total-work-hours-label')]")
            if weekly_average6.is_displayed():
                #Logging("Weekly working time - Data is displayed")
                Logging(green('>>>Data is displayed', 'bright'))
        except:
            Logging("Data is empty")
    except:
        #Logging("Weekly Average - Check data failed")
        Logging(red('>>>Weekly Average - Check data failed', 'bright'))


    # Logging(" ")
    # Logging("Day of week average")
    # try:
    #     Logging("Monday")
    #     mon = driver.find_element_by_xpath("//tbody[starts-with(@id, 'tbody-scroll-table')]//div[contains(.,'Day of week average')]//..//..//../tr[6]/td[2]//div[2]")
    #     if mon.is_displayed():
    #         #Logging("Weekly working time - Data is displayed")
    #         Logging(green('>>>Data is displayed', 'bright'))
    #         TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["day_week_average"]["pass"])
    # except:
    #     # Logging("Data is not displayed")
    #     Logging(red('>>>Data is not displayed', 'bright'))
    #     TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["day_week_average"]["fail"])

    # try:
    #     Logging("Tuesday")
    #     tue = driver.find_element_by_xpath("//tbody[starts-with(@id, 'tbody-scroll-table')]//div[contains(.,'Day of week average')]//..//..//../tr[6]/td[3]//div[2]")
    #     if tue.is_displayed():
    #         #Logging("Weekly working time - Data is displayed")
    #         Logging(green('>>>Data is displayed', 'bright'))
    # except:
    #     #Logging("Data is not displayed")
    #     Logging(red('>>>Data is not displayed', 'bright'))

    # try:
    #     Logging("Wednesday")
    #     wed = driver.find_element_by_xpath("//tbody[starts-with(@id, 'tbody-scroll-table')]//div[contains(.,'Day of week average')]//..//..//../tr[6]/td[4]//div[2]")
    #     if wed.is_displayed():
    #         #Logging("Weekly working time - Data is displayed")
    #         Logging(green('>>>Data is displayed', 'bright'))
    # except:
    #     #Logging("Data is not displayed")
    #     Logging(red('>>>Data is not displayed', 'bright'))

    # try:
    #     Logging("Thursday")
    #     thur = driver.find_element_by_xpath("//tbody[starts-with(@id, 'tbody-scroll-table')]//div[contains(.,'Day of week average')]//..//..//../tr[6]/td[5]//div[2]")
    #     if thur.is_displayed():
    #         #Logging("Weekly working time - Data is displayed")
    #         Logging(green('>>>Data is displayed', 'bright'))
    # except:
    #     #Logging("Data is not displayed")
    #     Logging(red('>>>Data is not displayed', 'bright'))

    # try:
    #     Logging("Friday")
    #     fri = driver.find_element_by_xpath("//tbody[starts-with(@id, 'tbody-scroll-table')]//div[contains(.,'Day of week average')]//..//..//../tr[6]/td[6]//div[2]")
    #     if fri.is_displayed():
    #         #Logging("Weekly working time - Data is displayed")
    #         Logging(green('>>>Data is displayed', 'bright'))
    # except:
    #     #Logging("Data is not displayed")
    #     Logging(red('>>>Data is not displayed', 'bright'))

    # try:
    #     Logging("Saturday")
    #     sat = driver.find_element_by_xpath("//tbody[starts-with(@id, 'tbody-scroll-table')]//div[contains(.,'Day of week average')]//..//..//../tr[6]/td[7]//div[2]")
    #     if sat.is_displayed():
    #         #Logging("Weekly working time - Data is displayed")
    #         Logging(green('>>>Data is displayed', 'bright'))
    # except:
    #     #Logging("Data is not displayed")
    #     Logging(red('>>>Data is not displayed', 'bright'))

    # try:
    #     Logging("Sunday")
    #     sun = driver.find_element_by_xpath("//tbody[starts-with(@id, 'tbody-scroll-table')]//div[contains(.,'Day of week average')]//..//..//../tr[6]/td[8]//div[2]")
    #     if sun.is_displayed():
    #         #Logging("Weekly working time - Data is displayed")
    #         Logging(green('>>>Data is displayed', 'bright'))
    # except:
    #     #Logging("Data is not displayed")
    #     Logging(red('>>>Data is not displayed', 'bright'))


def report_list():
    Logging(" ")
    Logging(yellow('***REPORTS - LIST***', ['bold', 'underlined']))
    time.sleep(4)
    try:
        try:
            driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_action_list')]").click()
            time.sleep(5)
        except:
            Logging(" ")

        try:
            Logging("Clock-In")
            list_clock_in = driver.find_element_by_xpath("//div[@class='list-wrapper']/div[2]/div[2]//span[@data-lang-id='Clock-In']/../following-sibling::div")
            if list_clock_in.is_displayed():
                #Logging("Data is displayed")
                Logging(green('>>>Data is displayed', 'bright'))
        except:
            #Logging("Data is not displayed")
            Logging(red('>>>Data is not displayed', 'bright'))

        try:
            Logging("Tardiness")
            list_tardinesss = driver.find_element_by_xpath("//span[contains(.,'Tardiness')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
            if list_tardinesss.is_displayed():
                #Logging("Data is displayed")
                Logging(green('>>>Data is displayed', 'bright'))
        except:
            #Logging("Data is not displayed")
            Logging(red('>>>Data is not displayed', 'bright'))

        try:
            Logging("No Clock-In")
            list_no_clock_in = driver.find_element_by_xpath("//span[contains(.,'No Clock-In')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
            if list_no_clock_in.is_displayed():
                #Logging("Data is displayed")
                Logging(green('>>>Data is displayed', 'bright'))
        except:
            #Logging("Data is not displayed")
            Logging(red('>>>Data is not displayed', 'bright'))

        try:
            Logging("Clock-Out")
            list_clock_out = driver.find_element_by_xpath("//div[@class='list-wrapper']/div[2]/div[2]//span[@data-lang-id='Clock-Out']/../following-sibling::div")
            if list_clock_out.is_displayed():
                #Logging("Data is displayed")
                Logging(green('>>>Data is displayed', 'bright'))
        except:
            #Logging("Data is not displayed")
            Logging(red('>>>Data is not displayed', 'bright'))

        try:
            Logging("Leave Early")
            list_leaveearly = driver.find_element_by_xpath("//span[contains(.,'Leave Early')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
            if list_leaveearly.is_displayed():
                #Logging("Data is displayed")
                Logging(green('>>>Data is displayed', 'bright'))
        except:
            #Logging("Data is not displayed")
            Logging(red('>>>Data is not displayed', 'bright'))

        try:
            Logging("No CLock-Out")
            list_no_clock_out = driver.find_element_by_xpath("//span[contains(.,'No Clock-Out')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
            if list_no_clock_out.is_displayed():
                #Logging("Data is displayed")
                Logging(green('>>>Data is displayed', 'bright'))
        except:
            #Logging("Data is not displayed")
            Logging(red('>>>Data is not displayed', 'bright'))

        try:
            Logging("OT")
            list_O_T = driver.find_element_by_xpath("//span[contains(.,'O/T')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
            if list_O_T.is_displayed():
                #Logging("Data is displayed")
                Logging(green('>>>Data is displayed', 'bright'))
        except:
            #Logging("Data is not displayed")
            Logging(red('>>>Data is not displayed', 'bright'))

        try:
            Logging("Night Shift")
            list_nightshift = driver.find_element_by_xpath("//span[contains(.,'Night shift')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
            if list_nightshift.is_displayed():
                #Logging("Data is displayed")
                Logging(green('>>>Data is displayed', 'bright'))
        except:
            #Logging("Data is not displayed")
            Logging(red('>>>Data is not displayed', 'bright'))

        try:
            Logging("Vacation")
            list_vacations = driver.find_element_by_xpath("//span[contains(.,'Vacation')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
            if list_vacations.is_displayed():
                #Logging("Data is displayed")
                Logging(green('>>>Data is displayed', 'bright'))
        except:
            #Logging("Data is not displayed")
            Logging(red('>>>Data is not displayed', 'bright'))

        time.sleep(3)
        #Check the first date of the month is displayed or not
        Logging(" ")
        try:
            list_clock_in = driver.find_element_by_xpath("//*[@id='app']//form//div[3]//div[1]/div[2]//div[contains(@class,'time')]")
            if list_clock_in.is_displayed():
                Logging("Clock-In: " + list_clock_in.text)
        except:
            Logging("No CLock-In")

        try:
            list_clock_out = driver.find_element_by_xpath("//*[@id='app']//form//div[3]//div[1]/div[3]//div[contains(@class,'time')]")
            if list_clock_out.is_displayed():
                Logging("Clock-Out: " + list_clock_out.text)
        except:
            Logging("No CLock-Out")

        Logging(" ")
        try:
            office_times1 = driver.find_element_by_xpath("//li[contains(.,'Office time')]")
            if office_times1.is_displayed():
                Logging("Office Time is displayed")
        except:
            Logging("No Office Time")

        try:
            working_times1 = driver.find_element_by_xpath("//li[contains(.,'Working time')]")
            if working_times1.is_displayed():
                Logging("Working Time is displayed")
                working_times = working_times1.text
        except:
            Logging("No Working Time")

        try:
            break_times1 = driver.find_element_by_xpath("//li[contains(.,'Break Time')]")
            if break_times1.is_displayed():
                Logging("Break Time is displayed")
        except:
            Logging("No Break Time")

        try:
            over_times1 = driver.find_element_by_xpath("//li[contains(.,'O/T')]")
            if over_times1.is_displayed():
                Logging("OT is displayed")
        except:
            Logging("No OT")
    except:
        Logging("Report-List-Check data failed")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["reports_list"]["fail"])


def approval_my_request():
    Logging(" ")
    Logging(yellow('***APPROVAL - MY REQUEST***', ['bold', 'underlined']))
    time.sleep(3)
    try:
        driver.find_element_by_xpath("//a[contains(@href,'/nhr/hr/timecard/user/approval')]").click()
        time.sleep(5)
    except:
        Logging(" ")
    
    try:
        filters_type = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//div[contains(@class,'select-wrapper')]/div")
        time.sleep(3)
        filters_type.click()
        time.sleep(3)
        filters_type_input = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//input[starts-with(@id, 'react-select')]")
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ENTER)
        time.sleep(2)
        #Logging(filters_type.text)
        try:
            type_first_row = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
            if type_first_row.is_displayed():
                try:
                    if filters_type.text == type_first_row.text:
                        Logging("Event - Filter is correct")
                    else:
                        Logging("Event - Filter is false")
                except:
                    Logging("Event - No data")
        except:
            Logging("Event - No data")
    except:
        Logging("Event - Can't check data")

    try:
        filters_type = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//div[contains(@class,'select-wrapper')]/div")
        time.sleep(3)
        filters_type.click()
        time.sleep(3)
        filters_type_input = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//input[starts-with(@id, 'react-select')]")
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ENTER)
        time.sleep(2)
        #Logging(filters_type.text)
        try:
            type_first_row = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
            if type_first_row.is_displayed():
                try:
                    if filters_type.text == type_first_row.text:
                        Logging("Clockin/out - Filter is correct")
                    else:
                        Logging("Clockin/out - Filter is false")
                except:
                    Logging("Clockin/out - No data")
        except:
            Logging("Clockin/out - No data")
    except:
        Logging("Clockin/out - Can't check data")

    try:
        filters_type = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//div[contains(@class,'select-wrapper')]/div")
        time.sleep(3)
        filters_type.click()
        time.sleep(3)
        filters_type_input = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//input[starts-with(@id, 'react-select')]")
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ENTER)
        time.sleep(2)
        #Logging(filters_type.text)
        try:
            type_first_row = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
            if type_first_row.is_displayed():
                try:
                    if filters_type.text == type_first_row.text:
                        Logging("Work Plan - Filter is correct")
                    else:
                        Logging("Work Plan - Filter is false")
                except:
                    Logging("Work Plan - No data")
        except:
            Logging("Work Plan - No data")
    except:
        Logging("Work Plan - Can't check data")

    try:
        filters_type = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//div[contains(@class,'select-wrapper')]/div")
        time.sleep(3)
        filters_type.click()
        time.sleep(3)
        filters_type_input = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//input[starts-with(@id, 'react-select')]")
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ENTER)
        time.sleep(2)
        #Logging(filters_type.text)
        try:
            type_first_row = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
            if type_first_row.is_displayed():
                try:
                    if filters_type.text == type_first_row.text:
                        Logging("Over Time - Filter is correct")
                    else:
                        Logging("Over Time - Filter is false")
                except:
                    Logging("Over Time - No data")
        except:
            Logging("Over Time - No data")
    except:
        Logging("Over Time - Can't check data")

    try:
        filters_type = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//div[contains(@class,'select-wrapper')]/div")
        time.sleep(3)
        filters_type.click()
        time.sleep(3)
        filters_type_input = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//input[starts-with(@id, 'react-select')]")
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ENTER)
        time.sleep(2)
        #Logging(filters_type.text)
        try:
            type_first_row = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
            if type_first_row.is_displayed():
                try:
                    if filters_type.text == type_first_row.text:
                        Logging("Over Time (Pre) - Filter is correct")
                    else:
                        Logging("Over Time (Pre) - Filter is false")
                except:
                    Logging("Over Time (Pre) - No data")
        except:
            Logging("Over Time (Pre) - No data")
    except:
        Logging("Over Time (Pre) - Can't check data")

    Logging(" ")
    Logging(yellow('***APPROVAL - VIEW CC***', ['bold', 'underlined']))
    time.sleep(3)
    try:
        driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_approval_view_cc') and contains(.,'View CC')]").click()
        time.sleep(5)
    except:
        Logging(" ")
    

    try:
        filters_type = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//div[contains(@class,'select-wrapper')]/div")
        time.sleep(3)
        filters_type.click()
        time.sleep(3)
        filters_type_input = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//input[starts-with(@id, 'react-select')]")
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ENTER)
        time.sleep(2)
        #Logging(filters_type.text)
        try:
            type_first_row = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
            if type_first_row.is_displayed():
                try:
                    if filters_type.text == type_first_row.text:
                        Logging("Event - Filter is correct")
                    else:
                        Logging("Event - Filter is false")
                except:
                    Logging("Event - No data")
        except:
            Logging("Event - No data")
    except:
        Logging("Event - Can't check data")

    try:
        filters_type = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//div[contains(@class,'select-wrapper')]/div")
        time.sleep(3)
        filters_type.click()
        time.sleep(3)
        filters_type_input = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//input[starts-with(@id, 'react-select')]")
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ENTER)
        time.sleep(2)
        #Logging(filters_type.text)
        try:
            type_first_row = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
            if type_first_row.is_displayed():
                try:
                    if filters_type.text == type_first_row.text:
                        Logging("Clockin/out - Filter is correct")
                    else:
                        Logging("Clockin/out - Filter is false")
                except:
                    Logging("Clockin/out - No data")
        except:
            Logging("Clockin/out - No data")
    except:
        Logging("Clockin/out - Can't check data")

    try:
        filters_type = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//div[contains(@class,'select-wrapper')]/div")
        time.sleep(3)
        filters_type.click()
        time.sleep(3)
        filters_type_input = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//input[starts-with(@id, 'react-select')]")
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ENTER)
        time.sleep(2)
        #Logging(filters_type.text)
        try:
            type_first_row = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
            if type_first_row.is_displayed():
                try:
                    if filters_type.text == type_first_row.text:
                        Logging("Work Plan - Filter is correct")
                    else:
                        Logging("Work Plan - Filter is false")
                except:
                    Logging("Work Plan - No data")
        except:
            Logging("Work Plan - No data")
    except:
        Logging("Work Plan - Can't check data")

    try:
        filters_type = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//div[contains(@class,'select-wrapper')]/div")
        time.sleep(3)
        filters_type.click()
        time.sleep(3)
        filters_type_input = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//input[starts-with(@id, 'react-select')]")
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ENTER)
        time.sleep(2)
        #Logging(filters_type.text)
        try:
            type_first_row = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
            if type_first_row.is_displayed():
                try:
                    if filters_type.text == type_first_row.text:
                        Logging("Over Time - Filter is correct")
                    else:
                        Logging("Over Time - Filter is false")
                except:
                    Logging("Over Time - No data")
        except:
            Logging("Over Time - No data")
    except:
        Logging("Over Time - Can't check data")

    try:
        filters_type = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//div[contains(@class,'select-wrapper')]/div")
        time.sleep(3)
        filters_type.click()
        time.sleep(3)
        filters_type_input = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_title_type')]//..//input[starts-with(@id, 'react-select')]")
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ARROW_DOWN)
        filters_type_input.send_keys(Keys.ENTER)
        time.sleep(2)
        #Logging(filters_type.text)
        try:
            type_first_row = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
            if type_first_row.is_displayed():
                try:
                    if filters_type.text == type_first_row.text:
                        Logging("Over Time (Pre) - Filter is correct")
                    else:
                        Logging("Over Time (Pre) - Filter is false")
                except:
                    Logging("Over Time (Pre) - No data")
        except:
            Logging("Over Time (Pre) - No data")
    except:
        Logging("Over Time (Pre) - Can't check data")




def dashboard():
    try:
        time.sleep(3)
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Timeline')]").click()
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Filters')] ")))
        time.sleep(2)
        driver.find_element_by_xpath("//div[contains(@class,'main-side-container-history')]/../../div[1]").click()
        time.sleep(5)
        # try:
        #     icon = driver.find_element_by_xpath("//*[@id='popover-tree']")
        #     if icon.is_displayed():
        #         Logging("Success in open the organization box")
        # except:
        #     Logging("False")
        
        tl_search2 = driver.find_element_by_xpath("//input[contains(@class,'form-control')]")
        tl_search2.send_keys(data["name_keyword"][0])
        tl_search2.send_keys(Keys.ENTER)
        time.sleep(5)
        driver.find_element_by_xpath("//div[contains(@class,'avatar-wrapper')]//li").click()
        time.sleep(5)
        driver.find_element_by_xpath("//div[contains(@class,'main-side-container-history')]/../../div[1]").click()

        filters_input_dashboard = driver.find_element_by_xpath("//input[starts-with(@id, 'react-select')]")
        filters_input_dashboard.send_keys(Keys.ARROW_DOWN)
        filters_input_dashboard.send_keys(Keys.ENTER)
        time.sleep(3)
        driver.find_element_by_xpath("//div[contains(@class, 'timeline-item  ')]//div[contains(.,'Clock-In')]//div[contains(@class, 'd-flex ')]//span[2]//div[contains(@class, 'cursor-pointer')]").click()
        driver.find_element_by_xpath("//button//span[contains(.,'Delete')] ").click()

        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Dashboard')]").click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@data-lang-id,'tc_dashboard_my_board')]")))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["access_dashboard_page"]["pass"])
    
        time.sleep(2)
        Logging("")
        Logging("***Today's work - Before log in***")
        dashboard_work_place = driver.find_element_by_xpath("//div[contains(@class,'daily-header-wrapper')]/div[1]/div/div")
        Logging("Work Place: " + dashboard_work_place.text)
        today_work = dashboard_work_place.text 
        today_work1 = today_work.split(" ")[0]
        Logging("Work Place - Country : " + today_work1)

        today_work_timezone = dashboard_work_place.text
        today_work_timezone1 = today_work.split(" ")[1]
        Logging("Work Place - Timezone : " + today_work_timezone1)

        dashboard_clockin = driver.find_element_by_xpath("//div[contains(@class,'check-in-status')]")
        Logging("Clock-In: " + dashboard_clockin.text)

        dashboard_clockout = driver.find_element_by_xpath("//div[contains(@class,'check-out-status')]")
        Logging("Clock-Out: " + dashboard_clockout.text)

        dashboard_work_policy = driver.find_element_by_xpath("//div[contains(@class,'left-content')]")
        Logging("Work Policy: " + dashboard_work_policy.text)

        dashboard_work_policy_time = driver.find_element_by_xpath("//div[contains(@class,'right-content')]")
        Logging("Work Policy Time: " + dashboard_work_policy_time.text)

        dashboard_remaining_working_time = driver.find_element_by_xpath("//div[contains(@class,'daily-container-wrapper')]/div[3]/div[2]")
        Logging("Remaining working time: " + dashboard_remaining_working_time.text)
        dashboard_remaining_working_time1 = dashboard_remaining_working_time.text
        dashboard_remaining_working_time2 = dashboard_remaining_working_time1.split("H")[0] 
        dashboard_remaining_working_time2_decimal = int(dashboard_remaining_working_time2)
        Logging("Remaining working time after change to decimal: " + str(dashboard_remaining_working_time2_decimal))

        dashboard_working_time = driver.find_element_by_xpath("//div[contains(@class,'daily-container-wrapper')]/div[4]/div[2]")
        Logging("Working time: " + dashboard_working_time.text)
        dashboard_working_time1 = dashboard_working_time.text
        dashboard_working_time2 = dashboard_working_time1.split("H")[0] 
        dashboard_working_time2_decimal = int(dashboard_working_time2)
        Logging("Working time after change to decimal: " + str(dashboard_working_time2_decimal))

        dashboard_break_time = driver.find_element_by_xpath("//div[contains(@class,'daily-container-wrapper')]/div[5]/div[2]")
        Logging("Break time: " + dashboard_break_time.text)
        dashboard_break_time1 = dashboard_break_time.text
        dashboard_break_time2 = dashboard_break_time1.split("H")[0] 
        dashboard_break_time2_decimal = int(dashboard_break_time2)
        Logging("Break time after change to decimal: " + str(dashboard_break_time2_decimal))

        dashboard_OT_time = driver.find_element_by_xpath("//div[contains(@class,'daily-container-wrapper')]/div[6]/div[2]")
        Logging("OT time: " + dashboard_OT_time.text)
        dashboard_OT_time1 = dashboard_OT_time.text
        dashboard_OT_time2 = dashboard_OT_time1.split("H")[0] 
        dashboard_OT_time2_decimal = int(dashboard_OT_time2)
        Logging("OT time after change to decimal: " + str(dashboard_OT_time2_decimal))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["user_today_work"]["pass"])
    except:
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["user_today_work"]["pass"])

    try:
        # Check if data is displayed or not
        Logging("")
        driver.find_element_by_xpath("//*[@id='app']//li[2]/a")
        Logging("Check if data of Staff working status is displayed or not")
        try:
            data_SWS = driver.find_element_by_xpath("//*[@id='app']/div/div[2]/div/div/div[1]/div[2]/div/div[3]/div[2]/div[2]/div[2]/div/div/div[1]/form/div/div/div[1]/div[2]/div[3]")
            if data_SWS.is_displayed():
                Logging("Data is displayed")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["user_staff_working_status"]["pass"])
        except:
                Logging("Data is not displayed")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["user_staff_working_status"]["fail"])
    except:
        Logging("Staff working status - Data is not displayed")

    try:
        Logging("")
        time.sleep(3)
        driver.find_element_by_xpath("//div[contains(@class,'icon-user-status down')]").click()
        time.sleep(2)
        working_status_pop_up = driver.find_element_by_xpath("//span[contains(.,'Clear')]")
        if working_status_pop_up.is_displayed():
            Logging("Working status is existed")
            driver.find_element_by_xpath("//span[contains(.,'Clear')]").click()
            time.sleep(3)
            Logging("Clear status successfully")
    except:
        Logging("Don't have working status yet")

    try:
        Logging("")
        Logging("***Staff working status - Before change work status***")
        driver.find_element_by_xpath("//*[@id='app']//div[contains(@class,'input-icon-wrapper')]").click()
        searchname = driver.find_element_by_xpath("//*[@id='app']//div[contains(@class,'input-icon-wrapper')]//input")
        searchname.send_keys(data["name_keyword"][0])
        searchname.send_keys(Keys.ENTER)
        
        time.sleep(5)
        SWS_status = driver.find_element_by_xpath("//div[contains(@class,'body-viewport')]//*[@col-id='work_status']").text
        Logging("Status: " + SWS_status)
        SWS_message = driver.find_element_by_xpath("//div[contains(@class,'body-viewport')]//*[@col-id='work_message']").text
        Logging("Message: " + SWS_message)

        #Add message
        Logging("")
        Logging("***Add status***")
        driver.find_element_by_xpath("//div[contains(@class,'icon-user-status down')]").click()
        time.sleep(3)
        meeting = driver.find_element_by_xpath("//div[contains(@class,'user-status-section')]/div[2]/div/div[2]").click()
        clear_after = driver.find_element_by_xpath("//div[starts-with(@id, 'dropdown')]/button").click()
        always_show = driver.find_element_by_xpath("//div[starts-with(@id, 'dropdown')]/div/button[1]").click()
        driver.find_element_by_xpath("//span[contains(.,'Save')] ").click()
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["add_status"]["pass"])

        driver.find_element_by_xpath("//div[contains(@class,'content-body')]//button[2]").click()
        time.sleep(3)

        SWS_status1 = driver.find_element_by_xpath("//div[contains(@class,'body-viewport')]//*[@col-id='work_status']").text
        # Logging("Status: " + SWS_status1)
        SWS_message1 = driver.find_element_by_xpath("//div[contains(@class,'body-viewport')]//*[@col-id='work_message']/div/div/div[1]").text
        # Logging("Message: " + SWS_message1)

        Logging("")
        Logging("***Compare status before and after add message***")
        # Logging(SWS_status)
        # Logging(SWS_status1)
        if SWS_message == SWS_status1:
            Logging("Edit status failed")
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["edit_status"]["fail"])
        else:
            Logging("Edit status successfully")
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["edit_status"]["pass"])
    except:
        Logging("Edit status failed")

    try:
        #Clear message
        Logging("")
        driver.find_element_by_xpath("//div[contains(@class,'icon-user-status down')]").click()
        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(.,'Clear')] ").click()
        driver.find_element_by_xpath("//div[contains(@class,'icon-user-status down')]").click()
        driver.find_element_by_xpath("//div[contains(@class,'icon-user-status down')]").click()
        #Check if message was already cleared or not
        time.sleep(4)
        try:
            clear_message = driver.find_element_by_xpath("//span[contains(@data-lang-id,'tc_action_clear')]")
            if clear_message.is_displayed():
                Logging("Clear status fail")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["clear_status"]["fail"])
        except:
                Logging("Clear status successfully")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["clear_status"]["pass"])
    except:
        #Logging("Can't clear status")
        Logging(" ")

    try:
        Logging("")
        Logging("***Today's work - After log in***")
        driver.find_element_by_xpath("//*[@id='0']").click()
        time.sleep(5)
        driver.find_element_by_xpath("//span[contains(.,'Clock-In')]").click()
        time.sleep(5)
        driver.find_element_by_xpath("//div[contains(@class,'modal-content')]//button[contains(@type,'button')]/span").click()
        Logging("Clock in successfully")

        time.sleep(5)
        driver.find_element_by_xpath("//*[@id='0']").click()
        driver.find_element_by_xpath("//span[contains(.,'Clock-Out')]").click()
        time.sleep(5)
        driver.find_element_by_xpath(data["TIMECARD"]["input_reason_leave_early"]).send_keys(data["TIMECARD"]["reason_leave_early"])
        time.sleep(2)
        driver.find_element_by_xpath(data["TIMECARD"]["save"]).click()
        Logging("Clock out successfully")

        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Timesheets')]").click()
        Logging(" ")
        Logging("Edit clockin")
        time.sleep(5)
        #Click Edit
        driver.find_element_by_xpath("//div[contains(@class, 'admin_status')]//div[contains(@class, 'timeline-item  ')]//div[contains(.,'Clock-In')]//div[contains(@class, 'd-flex ')]//span[1]//div[contains(@class, 'cursor-pointer')]").click()
        time.sleep(3)
        driver.find_element_by_xpath("//button[starts-with(@id, 'btnHours')]").click()
        time.sleep(3)
        driver.find_element_by_xpath("//div[starts-with(@id, 'dropdown')]//div//button[contains(.,'08')]").click()

        driver.find_element_by_xpath("//button[starts-with(@id, 'btnMin')]").click()
        time.sleep(3)
        driver.find_element_by_xpath("//div[starts-with(@id, 'dropdown')]//button[starts-with(@id, 'btnMin')]//following-sibling::div//button[contains(.,'00')]").click()

        #Click On-time
        driver.find_element_by_xpath("//span[contains(.,'On Time')]").click()

        #Input Memo
        driver.find_element_by_xpath("//div[contains(@class, 'modal-content')]//div[5]//textarea[contains(@name, 'memo')]").send_keys("test")
        Logging("Input memo")

        #Save
        driver.find_element_by_xpath("//form/div[2]/button[2]").click()
        Logging("Edit clockin successfully")    

        Logging("Edit clockout")
        time.sleep(3)
        #Click Edit
        driver.find_element_by_xpath("//div[contains(@class, 'admin_status')]//div[contains(@class, 'timeline-item  ')]//div[contains(.,'Clock-Out')]//div[contains(@class, 'd-flex ')]//span[1]//div[contains(@class, 'cursor-pointer')]").click()
        time.sleep(3)
        driver.find_element_by_xpath("//button[starts-with(@id, 'btnHours')]").click()
        time.sleep(3)
        driver.find_element_by_xpath("//div[starts-with(@id, 'dropdown')]//div//button[contains(.,'14')]").click()

        driver.find_element_by_xpath("//button[starts-with(@id, 'btnMin')]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[starts-with(@id, 'dropdown')]//button[starts-with(@id, 'btnMin')]//following-sibling::div//button[contains(.,'00')]").click()

        #Click On-time
        driver.find_element_by_xpath("//span[contains(.,'On Time')]").click()

        #Input Memo
        driver.find_element_by_xpath("//div[contains(@class, 'modal-content')]//div[5]//textarea[contains(@name, 'memo')]").send_keys("test")

        #Save
        driver.find_element_by_xpath("//form/div[2]/button[2]").click()
        Logging("Edit clockout successfully")
        time.sleep(3)

        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Dashboard')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@data-lang-id,'tc_dashboard_name')]")))
        Logging("")

        Logging("***Today's work - After log in***")
        time.sleep(5)
        dashboard_clockin_after = driver.find_element_by_xpath("//div[contains(@class,'check-in-status')]")
        Logging("Clock-In: " + dashboard_clockin_after.text)

        dashboard_clockout_after = driver.find_element_by_xpath("//div[contains(@class,'check-out-status')]")
        Logging("Clock-Out: " + dashboard_clockout_after.text)

        dashboard_remaining_working_time_after = driver.find_element_by_xpath("//div[contains(@class,'daily-container-wrapper')]/div[3]/div[2]")
        Logging("Remaining working time: " + dashboard_remaining_working_time_after.text)
        dashboard_remaining_working_time_after1 = dashboard_remaining_working_time_after.text
        dashboard_remaining_working_time_after2 = dashboard_remaining_working_time_after1.split("H")[0] 
        dashboard_remaining_working_time_after2_decimal = int(dashboard_remaining_working_time_after2)
        Logging("Remaining working time after change to decimal: " + str(dashboard_remaining_working_time_after2_decimal))

        dashboard_working_time_after = driver.find_element_by_xpath("//div[contains(@class,'daily-container-wrapper')]/div[4]/div[2]/div[1]")
        Logging("Working time: " + dashboard_working_time_after.text)
        dashboard_working_time_after1 = dashboard_working_time_after.text
        dashboard_working_time_after2 = dashboard_working_time_after1.split("H")[0] 
        dashboard_working_time_after2_decimal = int(dashboard_working_time_after2)
        Logging("Working time after change to decimal: " + str(dashboard_working_time_after2_decimal))

        period_working_time = driver.find_element_by_xpath("//div[contains(@class,'daily-container-wrapper')]/div[4]/div[2]/div[2]")
        Logging("Period working time: " + period_working_time.text)

        dashboard_break_time_after = driver.find_element_by_xpath("//div[contains(@class,'daily-container-wrapper')]/div[5]/div[2]/div[1]")
        Logging("Break time: " + dashboard_break_time_after.text)
        dashboard_break_time_after1 = dashboard_break_time_after.text
        dashboard_break_time_after2 = dashboard_break_time_after1.split("H")[0] 
        dashboard_break_time_after2_decimal = int(dashboard_break_time_after2)
        Logging("Break time after change to decimal: " + str(dashboard_break_time_after2_decimal))

        period_break_time = driver.find_element_by_xpath("//div[contains(@class,'daily-container-wrapper')]/div[5]/div[2]/div[2]")
        Logging("Period break time: " + period_break_time.text)

        dashboard_OT_time_after = driver.find_element_by_xpath("//div[contains(@class,'daily-container-wrapper')]/div[6]/div[2]")
        Logging("OT time: " + dashboard_OT_time_after.text)
        dashboard_OT_time_after1 = dashboard_OT_time_after.text
        dashboard_OT_time_after2 = dashboard_OT_time_after1.split("H")[0] 
        dashboard_OT_time_after2_decimal = int(dashboard_OT_time_after2)
        Logging("OT time after change to decimal: " + str(dashboard_OT_time_after2_decimal))

        Logging("")
        Logging("Plus workingtime and remaining working time to see if the result is 8 or not")
        if dashboard_working_time_after2_decimal + dashboard_remaining_working_time_after2_decimal == 8:
            Logging("The result is 8 - System calculation is correct")
        else:
            Logging("The result is not 8 - System calculation is wrong")

        #Avatar small window
        time.sleep(5)       
        driver.find_element_by_xpath("//*[@id='0']").click()
        time.sleep(3)
        avatar_work_place = driver.find_element_by_xpath(" //label[contains(@data-lang-id,'tc_title_work_style')]/..//..//div//div//li[1]")
        Logging("")
        Logging("Work Place - Country: " + avatar_work_place.text)

        avatar_work_place_timezone = driver.find_element_by_xpath("//label[contains(@data-lang-id,'tc_title_work_style')]/..//..//div//div//li[2]")
        Logging("Work Place - Timezone: " + avatar_work_place_timezone.text)
        avatar_work = avatar_work_place_timezone.text 
        avatar_work1 = avatar_work.split("(")[0]
        Logging("Work Place - Timezone: " + avatar_work1)

        avatar_clockin = driver.find_element_by_xpath("//span[contains(.,'Clock-In')]/p[2]")
        Logging("Clock-In: " + avatar_clockin.text)

        avatar_breaktime = driver.find_element_by_xpath("//span[contains(.,'Break Time')]/p[2]")
        Logging("Breaktime: " + avatar_breaktime.text)

        avatar_clockout = driver.find_element_by_xpath("//span[contains(.,'Clock-Out')]/p[2]")
        Logging("Clock-Out: " + avatar_clockout.text)

        avatar_work_policy = driver.find_element_by_xpath("//div[contains(@class,'item-header-content')]//div[2]/div[2]/p[2]")
        Logging("Work Policy: " + avatar_work_policy.text)

        avatar_work_policy_time = driver.find_element_by_xpath("//div[contains(@class,'item-header-content')]//div[2]/div[2]/p[1]")
        Logging("Work Policy Time: " + avatar_work_policy_time.text)

        avatar_working_time = driver.find_element_by_xpath("//div[contains(@class,'item-header-content')]//div[5]//div[1]/p")
        Logging("Working Time: " + avatar_working_time.text)


        Logging("")
        Logging("Compare pop-up clockin and dashboard clockin")
        if dashboard_clockin_after.text == avatar_clockin.text:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")

        Logging("")
        Logging("Compare pop-up clockout and dashboard clockout")
        if dashboard_clockout_after.text == avatar_clockout.text:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")

        Logging("")
        Logging("Compare pop-up working time and dashboard working time")
        if int(avatar_working_time.text) == dashboard_working_time_after2_decimal:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")
    except:
        Logging("Check data fail")

    # try:
    #     #Weekly status - Total
    #     time.sleep(15)
    #     driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Weekly Status')]").click()
    #     time.sleep(10)
    #     driver.find_element_by_xpath("//div[contains(@class,'company-status-setting')]/div/div[2]/div/div[1]").click()
    #     ws_search3 = driver.find_element_by_xpath("//form/div/div/input")
    #     ws_search3.send_keys(data["name_keyword"][0])
    #     ws_search3.send_keys(Keys.ENTER)
    #     time.sleep(5)
    #     driver.find_element_by_xpath("//div[contains(@class,'visible')]//li").click()
    #     driver.find_element_by_xpath("//div[contains(@class,'company-status-setting')]/div/div[2]/div/div[1]").click()

    #     Logging("")
    #     time.sleep(10)
    #     total3 = driver.find_element_by_xpath("//span[contains(@class,'td-sum-of-time')]")
    #     Logging("Total hour before change to decimal: " + total3.text)
    #     total_time3 = total3.text
    #     total_hour3 = total_time3.split("H")[0]
    #     total_number3 = int(total_hour3)
    #     Logging("Total hour after change to decimal: " + str(total_number3))

    #     #Reports - OT + Night shift
    #     driver.find_element_by_xpath("//a[contains(@href,'/nhr/hr/timecard/user/statistics')]").click()
    #     WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Working status')] ")))

    #     Logging("")
    #     OT = driver.find_element_by_xpath("//span[contains(.,'Working status')]//following-sibling::div//li[4]//span[contains(.,'O/T')]/../../div[2]")
    #     Logging("OT before change to decimal: " + OT.text)
    #     OT_time = OT.text
    #     OT_hour = OT_time.split("H")[0]
    #     OT_number = int(OT_hour)
    #     Logging("OT after change to decimal: " + str(OT_number))

    #     reports_night_shift = driver.find_element_by_xpath("//span[contains(.,'Working status')]//following-sibling::div//li[5]//span[contains(.,'Night shift')]/../../div[2]")
    #     Logging("Night shift before change to decimal: " + reports_night_shift.text)
    #     reports_night_shift_time = reports_night_shift.text
    #     reports_night_shift_hour = reports_night_shift_time.split("H")[0]
    #     reports_night_shift_number = int(reports_night_shift_hour)
    #     Logging("Night shift after change to decimal: " + str(reports_night_shift_number))


    #     Logging("")
    #     Logging("***Weekly Working Time***")
    #     time.sleep(5)
    #     driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Dashboard')]").click()
    #     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@data-lang-id,'tc_dashboard_name')]")))
    #     time.sleep(2)
    #     WWT_working_time = driver.find_element_by_xpath("//*[@id='app']//div[contains(@class,'work-hours-color')]")
    #     Logging("Working time before change to decimal: " + WWT_working_time.text)
    #     WWT_working_time_time = WWT_working_time.text
    #     WWT_working_time_time_hour = WWT_working_time_time.split("H")[0]
    #     WWT_working_time_time_number = int(WWT_working_time_time_hour)
    #     Logging("Working time after change to decimal: " + str(WWT_working_time_time_number))

    #     WWT_OT = driver.find_element_by_xpath("//*[@id='app']//div[contains(@class,'over-time-color')]")
    #     Logging("OT time before change to decimal: " + WWT_OT.text)
    #     WWT_OT_time = WWT_OT.text
    #     WWT_OT_hour = WWT_OT_time.split("H")[0]
    #     WWT_OT_time_number = int(WWT_OT_hour)
    #     Logging("OT time after change to decimal: " + str(WWT_OT_time_number))

    #     WWT_night_shift = driver.find_element_by_xpath("//*[@id='app']//div[contains(@class,'night-work-color')]")
    #     Logging("Night shift before change to decimal: " + WWT_night_shift.text)
    #     WWT_night_shift_time = WWT_night_shift.text
    #     WWT_night_shift_hour = WWT_night_shift_time.split("H")[0]
    #     WWT_night_shift_time_number = int(WWT_night_shift_hour)
    #     Logging("Night shift after change to decimal: " + str(WWT_night_shift_time_number))
    #     TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["user_weekly_working_time"]["pass"])

    #     Logging("")
    #     Logging("Compare WWT-Working time and Total working time")
    #     if WWT_working_time_time_number == total_number3:
    #         Logging("Result was the same - System was correct")
    #     else:
    #         Logging("Result was different - System was false")

    #     Logging("")
    #     Logging("Compare WWT-OT and Report-OT")
    #     if WWT_OT_time_number == OT_number:
    #         Logging("Result was the same - System was correct")
    #     else:
    #         Logging("Result was different - System was false")
        
    #     Logging("")
    #     Logging("Compare WWT-Night shift and Report-Night shift")
    #     if WWT_night_shift_time_number == reports_night_shift_number:
    #         Logging("Result was the same - System was correct")
    #     else:
    #         Logging("Result was different - System was false")
    # except:
    #     Logging("Check data fail")

    try:
        #Time clock status
        Logging("")
        Logging("**Time clock status**")
        TCS_clockin = driver.find_element_by_xpath(" //div[contains(@class,'working-status-ad-dash-wrapper')]/div[1]/div[1]/div")
        Logging("Clockin before change to decimal: " + TCS_clockin.text)
        TCS_clockin_time = TCS_clockin.text
        TCS_clockin_hour = TCS_clockin_time.split(" ")[0]
        TCS_clockin_time_number = int(TCS_clockin_hour)
        Logging("Clockin after change to decimal: " + str(TCS_clockin_time_number))

        TCS_tardiness = driver.find_element_by_xpath(" //div[contains(@class,'working-status-ad-dash-wrapper')]/div[1]/div[2]/div")
        Logging("Tardiness before change to decimal: " + TCS_tardiness.text)
        TCS_tardiness_time = TCS_tardiness.text
        TCS_tardiness_hour = TCS_tardiness_time.split(" ")[0]
        TCS_tardiness_time_number = int(TCS_tardiness_hour)
        Logging("Tardiness after change to decimal: " + str(TCS_tardiness_time_number))

        TCS_no_clockin = driver.find_element_by_xpath(" //div[contains(@class,'working-status-ad-dash-wrapper')]/div[1]/div[3]/div")
        Logging("No clockin before change to decimal: " + TCS_no_clockin.text)
        TCS_no_clockin_time = TCS_no_clockin.text
        TCS_no_clockin_hour = TCS_no_clockin_time.split(" ")[0]
        TCS_no_clockin_time_number = int(TCS_no_clockin_hour)
        Logging("No clockin after change to decimal: " + str(TCS_no_clockin_time_number))

        TCS_clockout = driver.find_element_by_xpath(" //div[contains(@class,'working-status-ad-dash-wrapper')]/div[1]/div[4]/div")
        Logging("Clockout before change to decimal: " + TCS_clockout.text)
        TCS_clockout_time = TCS_clockout.text
        TCS_clockout_hour = TCS_clockout_time.split(" ")[0]
        TCS_clockout_time_number = int(TCS_clockout_hour)
        Logging("Clockout after change to decimal: " + str(TCS_clockout_time_number))

        TCS_leave_early = driver.find_element_by_xpath(" //div[contains(@class,'working-status-ad-dash-wrapper')]/div[1]/div[5]/div")
        Logging("Leave early before change to decimal: " + TCS_leave_early.text)
        TCS_leave_early_time = TCS_leave_early.text
        TCS_leave_early_hour = TCS_leave_early_time.split(" ")[0]
        TCS_leave_early_time_number = int(TCS_leave_early_hour)
        Logging("Leave early after change to decimal: " + str(TCS_leave_early_time_number))

        TCS_vacation = driver.find_element_by_xpath(" //div[contains(@class,'working-status-ad-dash-wrapper')]/div[1]/div[6]/div")
        Logging("Vacation before change to decimal: " + TCS_vacation.text)
        TCS_vacation_time = TCS_vacation.text
        TCS_vacation_hour = TCS_vacation_time.split(" ")[0]
        TCS_vacation_time_number = int(TCS_vacation_hour)
        Logging("Vacation after change to decimal: " + str(TCS_vacation_time_number))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["user_time_clock_status"]["pass"])


        time.sleep(3)
        driver.find_element_by_xpath("//a[contains(@href,'/nhr/hr/timecard/user/statistics')]").click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Working status')] ")))

        Logging("")
        Logging("***Reports - Events***")
        events_clockin1 = driver.find_element_by_xpath("//li[1]//span[contains(.,'Clock-In')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Clock-In: " + events_clockin1.text)
        events_clockin_day1 = events_clockin1.text
        events_clockin_time1 = events_clockin_day1.split(" ")[0]
        events_clockin_decimal1 = int(events_clockin_time1)
        Logging("Clock-In after change to decimal: " + str(events_clockin_decimal1))

        tardiness1 = driver.find_element_by_xpath("//span[contains(.,'Tardiness')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Tardiness: " + tardiness1.text)
        tardiness_day1 = tardiness1.text
        tardiness_time1 = tardiness_day1.split(" ")[0]
        tardiness_decimal1 = int(tardiness_time1)
        Logging("Tardiness after change to decimal: " + str(tardiness_decimal1))

        no_clockin1 = driver.find_element_by_xpath("//span[contains(.,'No Clock-In')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("No Clock-In: " + no_clockin1.text)
        no_clockin_day1 = no_clockin1.text
        no_clockin_time1 = no_clockin_day1.split(" ")[0]
        no_clockin_decimal1 = int(no_clockin_time1)
        Logging("No Clock-In after change to decimal: " + str(no_clockin_decimal1))

        events_clockout1 = driver.find_element_by_xpath("//li[4]//span[contains(.,'Clock-Out')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Clock-Out: " + events_clockout1.text)
        events_clockout_day1 = events_clockout1.text
        events_clockout_time1 = events_clockout_day1.split(" ")[0]
        events_clockout_decimal1 = int(events_clockout_time1)
        Logging("Clock-Out after change to decimal: " + str(events_clockout_decimal1))

        leave_early1 = driver.find_element_by_xpath("//span[contains(.,'Leave Early')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Leave Early: " + leave_early1.text)
        leave_early_day1 = leave_early1.text
        leave_early_time1 = leave_early_day1.split(" ")[0]
        leave_early_decimal1 = int(leave_early_time1)
        Logging("Leave Early after change to decimal: " + str(leave_early_decimal1))

        vacation1 = driver.find_element_by_xpath("//li[9]//span[contains(.,'Vacation')]/../..//div[contains(@class,'d-flex ')]/following-sibling::div")
        Logging("Vacation: " + vacation1.text)
        vacation_day1 = vacation1.text
        vacation_time1 = vacation_day1.split(" ")[0]
        vacation_decimal1 = int(vacation_time1)
        Logging("Vacation after change to decimal: " + str(vacation_decimal1))




        Logging("")
        Logging("===Compare data betwween Reports and Time clock status===")
        Logging("Compare Events - Clockin with Time clock status - Clockin")
        # Logging(events_clockin_decimal1)
        # Logging(TCS_clockin_time_number)
        if events_clockin_decimal1 == TCS_clockin_time_number:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false") 

        Logging("")
        Logging("Compare Events - Tardiness with Time clock status - Tardiness")
        # Logging(tardiness_decimal1)
        # Logging(TCS_tardiness_time_number)
        if tardiness_decimal1 == TCS_tardiness_time_number:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")

        Logging("")
        Logging("Compare Events - No Clockin with Time clock status - No Clockin")
        # Logging(no_clockin_decimal1)
        # Logging(TCS_no_clockin_time_number)
        if no_clockin_decimal1 == TCS_no_clockin_time_number:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")

        Logging("")
        Logging("Compare Events - Clockout with Time clock status - Clockout")
        # Logging(events_clockout_decimal1)
        # Logging(TCS_clockout_time_number)
        if events_clockout_decimal1 == TCS_clockout_time_number:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")

        Logging("")
        Logging("Compare Events - Leave Early with Time clock status - Leave Early")
        # Logging(leave_early_decimal1)
        # Logging(TCS_leave_early_time_number)
        if leave_early_decimal1 == TCS_leave_early_time_number:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")

        Logging("")
        Logging("Compare Events - Vacation with Time clock status - Vacation")
        # Logging(vacation_decimal1)
        # Logging(TCS_vacation_time_number)
        if vacation_decimal1 == TCS_vacation_time_number:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")
    except:
        Logging("Check data fail")

    try:
        Logging("")
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Dashboard')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@data-lang-id,'tc_dashboard_name')]")))
        Logging("***Device - Default")
        device_scroll = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Settlement')] ")))
        device_scroll.location_once_scrolled_into_view
        time.sleep(3)

        device_web = driver.find_element_by_xpath("//div[contains(@class, 'chart-description-wrapper')]/div[1]/div[2]/div/div")
        Logging("Web: " + device_web.text)
        device_wifi = driver.find_element_by_xpath("//div[contains(@class, 'chart-description-wrapper')]/div[2]/div[2]/div/div")
        Logging("Wifi: " + device_wifi.text)
        device_gps = driver.find_element_by_xpath("//div[contains(@class, 'chart-description-wrapper')]/div[3]/div[2]/div/div")
        Logging("GPS: " + device_gps.text)
        device_beacon = driver.find_element_by_xpath("//div[contains(@class, 'chart-description-wrapper')]/div[4]/div[2]/div/div")
        Logging("Beacon: " + device_beacon.text)
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["user_device"]["pass"])
    except:
        Logging("Device - Check data fail")

    try:
        #Check if the circle is displayed or not
        Logging("")
        driver.find_element_by_xpath("//span[contains(.,'Device')]/../.. /..//div[contains(@class,'date-picker-field-wrapper')]").click()
        driver.find_element_by_xpath("//div[contains(@class,'react-datepicker')]/div[2]/div[2]/div[1]/div[1]").click()
        time.sleep(2)
        Logging("Check if the chart of Device is displayed or not")
        try:
            chart = driver.find_element_by_xpath("//div[contains(@class, 'chart-wrapper')]")
            if chart.is_displayed():
                Logging("Chart is displayed")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["user_time_clock_status_chart"]["pass"])
        except:
                Logging("Chart is not displayed")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["user_time_clock_status_chart"]["fail"])
    except:
        Logging("Chart is not displayed")

    try:
        #My work
        #Work day
        Logging("")
        Logging("*My work - Work day*")
        WD_worked_days = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_status_actual_working_days')]/..//span")
        Logging("Worked days: " + WD_worked_days.text)
        WD_worked_days_day = WD_worked_days.text
        WD_worked_days_time = WD_worked_days_day.split(" ")[0]
        WD_worked_days_decimal = int(WD_worked_days_time)
        Logging("Worked days after change to decimal: " + str(WD_worked_days_decimal))

        WD_scheduled_working_days = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_dashboard_scheduled_working_days')]/..//span")
        Logging("Scheduled working day: " + WD_scheduled_working_days.text)
        WD_scheduled_working_days_day = WD_scheduled_working_days.text
        WD_scheduled_working_days_time = WD_scheduled_working_days_day.split(" ")[0]
        WD_scheduled_working_days_decimal = int(WD_scheduled_working_days_time)
        Logging("Scheduled working day after change to decimal: " + str(WD_scheduled_working_days_decimal))

        WD_remaining_working_days = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_status_remaining_work_days')]/..//span")
        Logging("Remaining working days: " + WD_remaining_working_days.text)
        WD_remaining_working_days_day = WD_remaining_working_days.text
        WD_remaining_working_days_time = WD_remaining_working_days_day.split(" ")[0]
        WD_remaining_working_days_decimal = int(WD_remaining_working_days_time)
        Logging("Remaining working days after change to decimal: " + str(WD_remaining_working_days_decimal))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["user_mywork_workday"]["pass"])



        Logging("")
        time.sleep(2)
        Logging("*My work - Working time*")
        worked_time_mywork = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_status_analyis_work_time')]/..//span[1]")
        Logging("Worked time: " +  worked_time_mywork.text)
        worked_time_mywork1 = worked_time_mywork.text
        #Logging(worked_time_mywork1)
        try:
            hour_worked_time_mywork = worked_time_mywork1.split(" ")[0]
            #Logging(hour_worked_time_mywork)
            hour_worked_time_mywork = hour_worked_time_mywork.split("H")[0]
            hour_number_worked_time_mywork = int(hour_worked_time_mywork)
            #Logging(hour_number_worked_time_mywork)
            minute_worked_time_mywork = worked_time_mywork1.split(" ")[1]
            minutes_worked_time_mywork = minute_worked_time_mywork.split("M")[0]
            minutes_number_worked_time_mywork = int(minutes_worked_time_mywork)
            #Logging(minutes_number_worked_time_mywork)
            worked_time_mywork_decimal = ((minutes_number_worked_time_mywork) / 60) + (hour_number_worked_time_mywork)
            Logging("Worked time after change to decimal: " + str(worked_time_mywork_decimal))
        except:
            hour_worked_time_mywork = worked_time_mywork1.split(" ")[0]
            #Logging(hour_worked_time_mywork)
            hour_worked_time_mywork = hour_worked_time_mywork.split("H")[0]
            hour_number_worked_time_mywork = int(hour_worked_time_mywork)
            #Logging(hour_number_worked_time_mywork)
            worked_time_mywork_decimal = hour_number_worked_time_mywork
            Logging("Worked time after change to decimal: " + str(worked_time_mywork_decimal))


        remaining_working_time_mywork = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_status_remaining_work_hours')]/..//span[1]")
        Logging("Remaining working time: " +  remaining_working_time_mywork.text)
        remaining_working_time_mywork1 = remaining_working_time_mywork.text
        try:
            hour_remaining_working_time_mywork = remaining_working_time_mywork1.split(" ")[0]
            #Logging(hour_remaining_working_time_mywork)
            hour_remaining_working_time_mywork = hour_remaining_working_time_mywork.split("H")[0]
            hour_number_remaining_working_time_mywork = int(hour_remaining_working_time_mywork)
            #Logging(hour_number_remaining_working_time_mywork)
            minute_remaining_working_time_mywork = remaining_working_time_mywork1.split(" ")[1]
            #Logging(minute_remaining_working_time_mywork)
            minutes_remaining_working_time_mywork = minute_remaining_working_time_mywork.split("M")[0]
            minutes_number_remaining_working_time_mywork = int(minutes_remaining_working_time_mywork)
            #Logging(minutes_number_remaining_working_time_mywork)
            remaining_working_time_mywork_decimal = ((minutes_number_remaining_working_time_mywork) / 60) + (hour_number_remaining_working_time_mywork)
            Logging("Remaining working time after change to decimal: " + str(remaining_working_time_mywork_decimal))
        except:
            hour_remaining_working_time_mywork = remaining_working_time_mywork1.split(" ")[0]
            #Logging(hour_remaining_working_time_mywork)
            hour_remaining_working_time_mywork = hour_remaining_working_time_mywork.split("H")[0]
            hour_number_remaining_working_time_mywork = int(hour_remaining_working_time_mywork)
            #Logging(hour_number_remaining_working_time_mywork)
            remaining_working_time_mywork_decimal =hour_number_remaining_working_time_mywork
            Logging("Remaining working time after change to decimal: " + str(remaining_working_time_mywork_decimal))


        scheduled_working_time_mywork = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_dashboard_scheduled_working_hours')]/..//span[1]")
        Logging("Scheduled working time: " +  scheduled_working_time_mywork.text)
        scheduled_working_time_mywork1 = scheduled_working_time_mywork.text
        try:
            hour_scheduled_working_time_mywork = scheduled_working_time_mywork1.split(" ")[0]
            #Logging(hour_worked_time_mywork)
            hour_scheduled_working_time_mywork = hour_scheduled_working_time_mywork.split("H")[0]
            hour_scheduled_working_time_mywork = int(hour_scheduled_working_time_mywork)
            #Logging(scheduled_working_time_mywork)
            minute_scheduled_working_time_mywork = scheduled_working_time_mywork1.split(" ")[1]
            minutes_scheduled_working_time_mywork = minute_scheduled_working_time_mywork.split("M")[0]
            minutes_number_scheduled_working_time_mywork = int(minutes_scheduled_working_time_mywork)
            #Logging(minutes_numberscheduled_working_time_mywork)
            scheduled_working_time_mywork_decimal = ((minutes_number_scheduled_working_time_mywork) / 60) + (hour_scheduled_working_time_mywork)
            Logging("Scheduled working time after change to decimal: " + str(scheduled_working_time_mywork_decimal))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["user_mywork_workingtime"]["pass"])
        except:
            hour_scheduled_working_time_mywork = scheduled_working_time_mywork1.split(" ")[0]
            #Logging(hour_scheduled_working_time_mywork)
            hour_scheduled_working_time_mywork = hour_scheduled_working_time_mywork.split("H")[0]
            hour_number_scheduled_working_time_mywork = int(hour_scheduled_working_time_mywork)
            #Logging(hour_number_scheduled_working_time_mywork)
            scheduled_working_time_mywork_decimal = hour_number_scheduled_working_time_mywork
            Logging("Scheduled working time after change to decimal: " + str(scheduled_working_time_mywork_decimal))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["user_mywork_workingtime"]["pass"])


        Logging("")
        Logging("*My work - Settlement*")
        worked_time_settlement = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_dashboard_working_hours')]//..//div//span")
        Logging("Working time: " +  worked_time_settlement.text)
        worked_time_settlement1 = worked_time_settlement.text
        try:
            hour_worked_time_settlement = worked_time_settlement1.split(" ")[0]
            #Logging(hour_worked_time_settlement)
            hour_worked_time_settlement = hour_worked_time_settlement.split("H")[0]
            hour_number_worked_time_settlement = int(hour_worked_time_settlement)
            #Logging(hour_number_worked_time_settlement)
            minute_worked_time_settlement = worked_time_settlement1.split(" ")[1]
            #Logging(minute_worked_time_settlement)
            minutes_worked_time_settlement = minute_worked_time_settlement.split("M")[0]
            minutes_number_worked_time_settlement = int(minutes_worked_time_settlement)
            #Logging(minutes_number_worked_time_settlement)
            worked_time_settlement_decimal = ((minutes_number_worked_time_settlement) / 60) + (hour_number_worked_time_settlement)
            Logging("Working time after change to decimal: " + str(worked_time_settlement_decimal))
        except:
            hour_worked_time_settlement = worked_time_settlement1.split(" ")[0]
            #Logging(hour_worked_time_settlement)
            hour_worked_time_settlement = hour_worked_time_settlement.split("H")[0]
            hour_number_worked_time_settlement = int(hour_worked_time_settlement)
            #Logging(hour_number_worked_time_settlement)
            worked_time_settlement_decimal = hour_number_worked_time_settlement
            Logging("Working time after change to decimal: " + str(worked_time_settlement_decimal))


        OT_settlement = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_status_ot')]//..//div//span")
        Logging("OT time: " +  OT_settlement.text)
        OT_settlement1 = OT_settlement.text
        try:
            hour_OT_settlement = OT_settlement1.split(" ")[0]
            #Logging(hour_OT_settlement)
            hour_OT_settlement = hour_OT_settlement.split("H")[0]
            hour_number_OT_settlement = int(hour_OT_settlement)
            #Logging(hour_number_OT_settlement)
            minute_OT_settlement = OT_settlement1.split(" ")[1]
            minutes_OT_settlement = minute_OT_settlement.split("M")[0]
            minutes_number_OT_settlement = int(minutes_OT_settlement)
            #Logging(minutes_OT_settlement)
            OT_settlement_decimal = ((minutes_number_OT_settlement) / 60) + (hour_number_OT_settlement)
            Logging("Worked time after change to decimal: " + str(OT_settlement_decimal))
        except:
            hour_OT_settlement = OT_settlement1.split(" ")[0]
            #Logging(hour_OT_settlement)
            hour_OT_settlement = hour_OT_settlement.split("H")[0]
            hour_number_OT_settlement = int(hour_OT_settlement)
            #Logging(hour_number_OT_settlement)
            OT_settlement_decimal = hour_number_OT_settlement
            Logging("OT time after change to decimal: " + str(OT_settlement_decimal))


        nightshift_settlement = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_dashboard_night_shift')]//..//div//span")
        Logging("Night shift time: " +  nightshift_settlement.text)
        nightshift_settlement1 = nightshift_settlement.text
        try:
            hour_nightshift_settlement = nightshift_settlement1.split(" ")[0]
            #Logging(hour_nightshift_settlement)
            hour_nightshift_settlement = hour_nightshift_settlement.split("H")[0]
            hour_number_nightshift_settlement = int(hour_nightshift_settlement)
            #Logging(hour_number_nightshift_settlement)
            minute_nightshift_settlement1 = nightshift_settlement1.split(" ")[0][1]
            minutes_nightshift_settlement1 = minute_nightshift_settlement1.split("M")[0]
            minutes_nightshift_settlement1 = int(minutes_nightshift_settlement1)
            #Logging(minutes_OT_settlement)
            nightshift_settlement_decimal = ((minutes_nightshift_settlement1) / 60) + (hour_number_nightshift_settlement)
            Logging("Worked time after change to decimal: " + str(nightshift_settlement_decimal))
        except:
            hour_nightshift_settlement = nightshift_settlement1.split(" ")[0]
            #Logging(hour_nightshift_settlement)
            hour_nightshift_settlement = hour_nightshift_settlement.split("H")[0]
            hour_number_nightshift_settlement = int(hour_nightshift_settlement)
            #Logging(hour_number_nightshift_settlement)
            nightshift_settlement_decimal = hour_number_nightshift_settlement
            Logging("Night shift time after change to decimal: " + str(nightshift_settlement_decimal))

        holiday_work_settlement = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_dashboard_holiday_work')]//..//div//span")
        Logging("Holiday work time: " +  holiday_work_settlement.text)
        holiday_work_settlement1 = holiday_work_settlement.text
        try:
            hour_holiday_work_settlement = holiday_work_settlement1.split(" ")[0]
            #Logging(hour_holiday_work_settlement)
            hour_holiday_work_settlement = hour_holiday_work_settlement.split("H")[0]
            hour_number_holiday_work_settlement = int(hour_holiday_work_settlement)
            #Logging(hour_number_holiday_work_settlement)
            minute_holiday_work_settlement = holiday_work_settlement.split(" ")[0][1]
            minutes_holiday_work_settlement = minute_holiday_work_settlement.split("M")[0]
            minutes_holiday_work_settlement = int(minutes_holiday_work_settlement)
            #Logging(minutes_OT_settlement)
            holiday_work_settlement_decimal = ((minutes_holiday_work_settlement) / 60) + (hour_number_holiday_work_settlement)
            Logging("Worked time after change to decimal: " + str(holiday_work_settlement_decimal))
        except:
            hour_holiday_work_settlement = holiday_work_settlement1.split(" ")[0]
            #Logging(hour_holiday_work_settlement)
            hour_holiday_work_settlement = hour_holiday_work_settlement.split("H")[0]
            hour_number_holiday_work_settlement = int(hour_holiday_work_settlement)
            #Logging(hour_number_holiday_work_settlement)
            holiday_work_settlement_decimal = hour_number_holiday_work_settlement
            Logging("Holiday work time after change to decimal: " + str(holiday_work_settlement_decimal))



        holiday_settlement = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_status_day_holiday')]//..//div//span")
        Logging("Holiday: " +  holiday_settlement.text)

        holiday_settlement1 = holiday_settlement.text
        hour_holiday_settlement = holiday_settlement1.split(" ")[0]
        holiday_settlement_decimal = int(hour_holiday_settlement)
        Logging("Holiday after change to decimal: " + str(holiday_settlement_decimal))

        day_off_settlement = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_work_type_dayoff')]//..//div//span")
        Logging("Day off: " +  day_off_settlement.text)

        day_off_settlement1 = day_off_settlement.text
        hour_day_off_settlement = day_off_settlement1.split(" ")[0]
        day_off_settlement_decimal = int(hour_day_off_settlement)
        Logging("Day off after change to decimal: " + str(day_off_settlement_decimal))

        vacation_settlement = driver.find_element_by_xpath("//div[contains(@data-lang-id,'tc_status_vacations')]//..//div//span")
        Logging("Vacation: " +  vacation_settlement.text)

        vacation_settlement1 = vacation_settlement.text
        hour_vacation_settlement = vacation_settlement1.split(" ")[0]
        vacation_settlement_decimal = int(hour_vacation_settlement)
        Logging("Vacation after change to decimal: " + str(vacation_settlement_decimal))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["user_mywork_settlement"]["pass"])


        #Schedules - Working time
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Schedules')]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//span[contains(.,'Work Plan')]")))
        time.sleep(2)
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["access_schedule_page"]["pass"])

        Logging("")
        Logging("***Schedules - Working days***")
        WD_cumulative_days = driver.find_element_by_xpath("//div[contains(@class,'work-hours-wrapper')]/div[2]//div[1]/div[1]/div/span[1]")
        Logging("Cumulative days: " + WD_cumulative_days.text)
        WD_cumulative_days_day = WD_cumulative_days.text
        WD_cumulative_days_time = WD_cumulative_days_day.split(" ")[0]
        WD_cumulative_days_decimal = int(WD_cumulative_days_time)
        Logging("Cumulative days after change to decimal: " + str(WD_cumulative_days_decimal))

        WD_contractual_working_days = driver.find_element_by_xpath("//div[contains(@class,'work-hours-wrapper')]/div[2]//div[1]/div[2]/div/span[1]")
        Logging("Contractual working day: " + WD_contractual_working_days.text)
        WD_contractual_working_days_day = WD_contractual_working_days.text
        WD_contractual_working_days_time = WD_contractual_working_days_day.split(" ")[0]
        WD_contractual_working_days_decimal = int(WD_contractual_working_days_time)
        Logging("Contractual working day after change to decimal: " + str(WD_contractual_working_days_decimal))

        schedules_remaining_working_days = driver.find_element_by_xpath("//div[contains(@class,'work-hours-wrapper')]/div[2]//div[1]/div[3]/div/span[1]")
        Logging("Remaining working days: " + schedules_remaining_working_days.text)
        schedules_remaining_working_days_day = schedules_remaining_working_days.text
        schedules_remaining_working_days_time = schedules_remaining_working_days_day.split(" ")[0]
        schedules_remaining_working_days_decimal = int(schedules_remaining_working_days_time)
        Logging("Remaining working days after change to decimal: " + str(schedules_remaining_working_days_decimal))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["schedule_working_days"]["pass"])



        Logging("")
        Logging("***Schedules - Working time***")
        worked_time_schedules = driver.find_element_by_xpath("//div[contains(@class,'work-hours-wrapper')]/div[1]//div[1]/div[1]/div/span[1]")
        Logging("Worked time: " +  worked_time_schedules.text)
        worked_time_schedules1 = worked_time_schedules.text
        try:
            hour_worked_time_schedules = worked_time_schedules1.split(" ")[0]
            #Logging(hour_worked_time_schedules)
            hour_worked_time_schedules = hour_worked_time_schedules.split("H")[0]
            hour_number_worked_time_schedules = int(hour_worked_time_schedules)
            #Logging(hour_number_worked_time_schedules)
            minute_worked_time_schedules = worked_time_schedules1.split(" ")[1]
            #Logging(minute_worked_time_schedules)
            minutes_worked_time_schedules = minute_worked_time_schedules.split("M")[0]
            minutes_number_worked_time_schedules = int(minutes_worked_time_schedules)
            #Logging(minutes_number_worked_time_schedules)
            worked_time_schedules_decimal = ((minutes_number_worked_time_schedules) / 60) + (hour_number_worked_time_schedules)
            Logging("Worked time after change to decimal: " + str(worked_time_schedules_decimal))
        except:
            hour_worked_time_schedules = worked_time_schedules1.split(" ")[0]
            #Logging(hour_worked_time_schedules)
            hour_worked_time_schedules = hour_worked_time_schedules.split("H")[0]
            hour_number_worked_time_schedules = int(hour_worked_time_schedules)
            #Logging(hour_number_worked_time_schedules)
            worked_time_schedules_decimal = hour_number_worked_time_schedules
            Logging("Worked time after change to decimal: " + str(worked_time_schedules_decimal))

        remaining_working_time_schedules = driver.find_element_by_xpath("//div[contains(@class,'work-hours-wrapper')]/div[1]//div[1]/div[3]/div/span[1]")
        Logging("Remaining working time: " +  remaining_working_time_schedules.text)
        remaining_working_time_schedules1 = remaining_working_time_schedules.text
        try:
            hour_remaining_working_time_schedules = remaining_working_time_schedules1.split(" ")[0]
            #Logging(hour_remaining_working_time_schedules)
            hour_remaining_working_time_schedules = hour_remaining_working_time_schedules.split("H")[0]
            hour_number_remaining_working_time_schedules = int(hour_remaining_working_time_schedules)
            #Logging(hour_number_remaining_working_time_schedules)
            minute_remaining_working_time_schedules = remaining_working_time_schedules1.split(" ")[1]
            #Logging(minute_remaining_working_time_schedules)
            minutes_remaining_working_time_schedules = minute_remaining_working_time_schedules.split("M")[0]
            minutes_number_remaining_working_time_schedules = int(minutes_remaining_working_time_schedules)
            #Logging(minutes_number_remaining_working_time_schedules)
            remaining_working_time_schedules_decimal = ((minutes_number_remaining_working_time_schedules) / 60) + (hour_number_remaining_working_time_schedules)
            Logging("Remaining working time after change to decimal: " + str(remaining_working_time_schedules_decimal))
        except:
            hour_remaining_working_time_schedules = remaining_working_time_schedules1.split(" ")[0]
            #Logging(hour_remaining_working_time_schedules)
            hour_remaining_working_time_schedules = hour_remaining_working_time_schedules.split("H")[0]
            hour_number_remaining_working_time_schedules = int(hour_remaining_working_time_schedules)
            #Logging(hour_number_remaining_working_time_schedules)
            remaining_working_time_schedules_decimal = hour_number_remaining_working_time_schedules
            Logging("Remaining working time after change to decimal: " + str(remaining_working_time_schedules_decimal))


        scheduled_working_time_schedules = driver.find_element_by_xpath("//div[contains(@class,'work-hours-wrapper')]/div[1]//div[1]/div[2]/div/span[1]")
        Logging("Scheduled working time: " +  scheduled_working_time_schedules.text)
        scheduled_working_time_schedules1 = scheduled_working_time_schedules.text
        try:
            hour_scheduled_working_time_schedules = scheduled_working_time_schedules1.split(" ")[0]
            #Logging(hour_scheduled_working_time_schedules)
            hour_scheduled_working_time_schedules = hour_scheduled_working_time_schedules.split("H")[0]
            hour_number_scheduled_working_time_schedules = int(hour_scheduled_working_time_schedules)
            #Logging(hour_number_scheduled_working_time_schedules)
            minute_OT_settlement = OT_settlement1.split(" ")[1]
            minutes_OT_settlement = minute_OT_settlement.split("M")[0]
            minutes_OT_settlement = int(minutes_OT_settlement)
            #Logging(minutes_OT_settlement)
            scheduled_working_time_schedules_decimal = ((minutes_OT_settlement) / 60) + (hour_number_scheduled_working_time_schedules)
            Logging("Worked time after change to decimal: " + str(scheduled_working_time_schedules_decimal))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["schedule_working_time"]["pass"])
        except:
            hour_scheduled_working_time_schedules = scheduled_working_time_schedules1.split(" ")[0]
            #Logging(hour_scheduled_working_time_schedules)
            hour_scheduled_working_time_schedules = hour_scheduled_working_time_schedules.split("H")[0]
            hour_number_scheduled_working_time_schedules = int(hour_scheduled_working_time_schedules)
            #Logging(hour_number_scheduled_working_time_schedules)
            scheduled_working_time_schedules_decimal = hour_number_scheduled_working_time_schedules
            Logging("Scheduled working time after change to decimal: " + str(scheduled_working_time_schedules_decimal))
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["schedule_working_time"]["pass"])


        Logging("")
        Logging("***Schedules - Settlement***")
        schedules_working_time_settlement = driver.find_element_by_xpath("//div[contains(@class,'work-hours-wrapper')]/div[3]//div[1]/div[1]/div/span[1]")
        Logging("Working time: " +  schedules_working_time_settlement.text)
        schedules_working_time_settlement1 = schedules_working_time_settlement.text
        try:
            schedules_hour_working_time_settlement = schedules_working_time_settlement1.split(" ")[0]
            #Logging(schedules_hour_working_time_settlement)
            schedules_hour_working_time_settlement = schedules_hour_working_time_settlement.split("H")[0]
            schedules_hour_number_working_time_settlement = int(schedules_hour_working_time_settlement)
            #Logging(schedules_hour_number_working_time_settlement)
            schedules_minute_working_time_settlement = schedules_working_time_settlement1.split(" ")[1]
            #Logging(schedules_minute_working_time_settlement)
            schedules_minutes_working_time_settlement = schedules_minute_working_time_settlement.split("M")[0]
            schedules_minutes_number_working_time_settlement = int(schedules_minutes_working_time_settlement)
            #Logging(schedules_minutes_number_working_time_settlement)
            schedules_working_time_settlement_decimal = ((schedules_minutes_number_working_time_settlement) / 60) + (schedules_hour_number_working_time_settlement)
            Logging("Working time after change to decimal: " + str(schedules_working_time_settlement_decimal))
        except:
            schedules_hour_working_time_settlement = schedules_working_time_settlement1.split(" ")[0]
            #Logging(schedules_hour_working_time_settlement)
            schedules_hour_working_time_settlement = schedules_hour_working_time_settlement.split("H")[0]
            schedules_hour_number_working_time_settlement = int(schedules_hour_working_time_settlement)
            #Logging(schedules_hour_number_working_time_settlement)
            schedules_working_time_settlement_decimal = schedules_hour_number_working_time_settlement
            Logging("Working time after change to decimal: " + str(schedules_working_time_settlement_decimal))
        

        schedules_OT_settlement = driver.find_element_by_xpath("//div[contains(@class,'work-hours-wrapper')]/div[3]//div[1]/div[2]/div/span[1]")
        Logging("OT time: " +  schedules_OT_settlement.text)
        schedules_OT_settlement1 = schedules_OT_settlement.text
        try:
            schedules_hour_OT_settlement = schedules_OT_settlement1.split(" ")[0]
            #Logging(schedules_hour_OT_settlement)
            schedules_hour_OT_settlement = schedules_hour_OT_settlement.split("H")[0]
            schedules_hour_number_OT_settlement = int(schedules_hour_OT_settlement)
            #Logging(schedules_hour_number_OT_settlement)
            minute_OT_settlement1 = schedules_OT_settlement1.split(" ")[1]
            minutes_OT_settlement1 = minute_OT_settlement1.split("M")[0]
            minutes_number_OT_settlement1 = int(minutes_OT_settlement1)
            #Logging(minutes_number_worked_time_mywork)
            schedules_OT_settlement_decimal = ((minutes_number_OT_settlement1) / 60) + (schedules_hour_number_OT_settlement)
            Logging("Worked time after change to decimal: " + str(schedules_OT_settlement_decimal))
        except:
            schedules_hour_OT_settlement = schedules_OT_settlement1.split(" ")[0]
            #Logging(schedules_hour_OT_settlement)
            schedules_hour_OT_settlement = schedules_hour_OT_settlement.split("H")[0]
            schedules_hour_number_OT_settlement = int(schedules_hour_OT_settlement)
            #Logging(schedules_hour_number_OT_settlement)
            schedules_OT_settlement_decimal = schedules_hour_number_OT_settlement
            Logging("OT time after change to decimal: " + str(schedules_OT_settlement_decimal))

        schedules_nightshift_settlement = driver.find_element_by_xpath("//div[contains(@class,'work-hours-wrapper')]/div[3]//div[1]/div[3]/div/span[1]")
        Logging("Night shift time: " +  schedules_nightshift_settlement.text)

        # schedules_nightshift_settlement1 = schedules_nightshift_settlement.text
        # schedules_hour_nightshift_settlement = schedules_nightshift_settlement1.split(" ")[0]
        # #Logging(schedules_hour_nightshift_settlement)
        # schedules_hour_nightshift_settlement = schedules_hour_nightshift_settlement.split("H")[0]
        # schedules_hour_number_nightshift_settlement = int(schedules_hour_nightshift_settlement)
        # #Logging(schedules_hour_number_nightshift_settlement)

        # schedules_nightshift_settlement_decimal = schedules_hour_number_nightshift_settlement
        # Logging("Night shift time after change to decimal: " + str(schedules_nightshift_settlement_decimal))

        schedules_holiday_work_settlement = driver.find_element_by_xpath("//div[contains(@class,'work-hours-wrapper')]/div[3]/div[2]/div[3]/div[1]/div")
        Logging("Holiday work time: " +  schedules_holiday_work_settlement.text)
        schedules_holiday_work_settlement1 = schedules_holiday_work_settlement.text
        try:
            schedules_hour_holiday_work_settlement = schedules_holiday_work_settlement1.split(" ")[0]
            #Logging(schedules_hour_holiday_work_settlement)
            schedules_hour_holiday_work_settlement = schedules_hour_holiday_work_settlement.split("H")[0]
            schedules_hour_number_holiday_work_settlement = int(schedules_hour_holiday_work_settlement)
            #Logging(schedules_hour_number_holiday_work_settlement)
            minute_holiday_work_settlement1 = schedules_holiday_work_settlement1.split(" ")[1]
            minutes_holiday_work_settlement1 = minute_holiday_work_settlement1.split("M")[0]
            minutes_number_holiday_work_settlement1 = int(minutes_holiday_work_settlement1)
            #Logging(minutes_number_worked_time_mywork)
            schedules_holiday_work_settlement_decimal = ((minutes_number_holiday_work_settlement1) / 60) + (schedules_hour_holiday_work_settlement)
            Logging("Worked time after change to decimal: " + str(schedules_holiday_work_settlement_decimal))
        except:
            schedules_hour_holiday_work_settlement = schedules_holiday_work_settlement1.split(" ")[0]
            #Logging(schedules_hour_holiday_work_settlement)
            schedules_hour_holiday_work_settlement = schedules_hour_holiday_work_settlement.split("H")[0]
            schedules_hour_number_holiday_work_settlement = int(schedules_hour_holiday_work_settlement)
            #Logging(schedules_hour_number_holiday_work_settlement)
            schedules_holiday_work_settlement_decimal = schedules_hour_number_holiday_work_settlement
            Logging("Holiday work time after change to decimal: " + str(schedules_holiday_work_settlement_decimal))


        
        schedules_holiday_settlement = driver.find_element_by_xpath("//div[contains(@class,'work-hours-wrapper')]/div[3]/div[2]/div[3]/div[3]/div")
        Logging("Holiday: " +  schedules_holiday_settlement.text)

        schedules_holiday_settlement1 = schedules_holiday_settlement.text
        schedules_hour_holiday_settlement = schedules_holiday_settlement1.split(" ")[0]
        schedules_holiday_settlement_decimal = int(schedules_hour_holiday_settlement)
        Logging("Holiday after change to decimal: " + str(schedules_holiday_settlement_decimal))

        schedules_day_off_settlement = driver.find_element_by_xpath("//div[contains(@class,'work-hours-wrapper')]/div[3]/div[2]/div[3]/div[4]/div")
        Logging("Day off: " +  schedules_day_off_settlement.text)

        schedules_day_off_settlement1 = schedules_day_off_settlement.text
        schedules_hour_day_off_settlement = schedules_day_off_settlement1.split(" ")[0]
        schedules_day_off_settlement_decimal = int(schedules_hour_day_off_settlement)
        Logging("Day off after change to decimal: " + str(schedules_day_off_settlement_decimal))

        schedules_vacation_settlement = driver.find_element_by_xpath("//div[contains(@class,'work-hours-wrapper')]/div[3]/div[2]/div[3]/div[2]/div")
        Logging("Vacation: " +  schedules_vacation_settlement.text)

        schedules_vacation_settlement1 = schedules_vacation_settlement.text
        schedules_hour_vacation_settlement = schedules_vacation_settlement1.split(" ")[0]
        schedules_vacation_settlement_decimal = int(schedules_hour_vacation_settlement)
        Logging("Vacation after change to decimal: " + str(schedules_vacation_settlement_decimal))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["schedule_settlement"]["pass"])

        #Compare Schedule and Mywork
        Logging("")
        Logging("'''Compare to WORKDAY'''")
        Logging("Compare Schedules - Cumulative days with My work - Worked days")
        # Logging(WD_cumulative_days_decimal)
        # Logging(WD_worked_days_decimal)
        if WD_cumulative_days_decimal == WD_worked_days_decimal:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")

        Logging("")
        Logging("Compare Schedules - Contractual working day with My work - Scheduled working day")
        # Logging(WD_contractual_working_days_decimal)
        # Logging(WD_scheduled_working_days_decimal)
        if WD_contractual_working_days_decimal == WD_scheduled_working_days_decimal:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")

        Logging("")
        Logging("Compare Schedules - Remaining working days with My work - Remaining Working Days")
        # Logging(schedules_remaining_working_days_decimal)
        # Logging(WD_remaining_working_days_decimal)
        if schedules_remaining_working_days_decimal == WD_remaining_working_days_decimal:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")



        Logging("")
        Logging("'''Compare to WORKING TIME'''")
        Logging("Compare Schedules - Cumulative Worked Hours with My work - Worked time")
        # print(scheduled_working_time_schedules_decimal)
        # print(scheduled_working_time_mywork_decimal)
        if scheduled_working_time_schedules_decimal == scheduled_working_time_mywork_decimal:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")

        Logging("")
        Logging("Compare Schedules - Contractual Working Hours with My work - Scheduled working time")
        # print(worked_time_schedules_decimal)
        # print(worked_time_mywork_decimal)
        if worked_time_schedules_decimal == worked_time_mywork_decimal:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")

        Logging("")
        Logging("Compare Schedules -Remaining working time with My work - Remaining working time")
        # print(remaining_working_time_schedules_decimal)
        # print(remaining_working_time_mywork_decimal)
        if remaining_working_time_schedules_decimal == remaining_working_time_mywork_decimal:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")


        Logging("")
        Logging("'''Compare to MY WORK/ SETTLEMENT'''")
        Logging("Compare Schedules - Worked time with My work/ Settlement - Working time")
        # Logging(schedules_working_time_settlement_decimal)
        # Logging(worked_time_settlement_decimal)
        if schedules_working_time_settlement_decimal == worked_time_settlement_decimal:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")

        Logging("")
        Logging("Compare Schedules - OT with My work/ Settlement - O/T")
        # Logging(schedules_OT_settlement_decimal)
        # Logging(OT_settlement_decimal)
        if schedules_OT_settlement_decimal == OT_settlement_decimal:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")

        # Logging("")
        # Logging("Compare Schedules -Night shift with My work/ Settlement - Night shift")
        # # Logging(schedules_nightshift_settlement_decimal)
        # # Logging(nightshift_settlement_decimal)
        # if schedules_nightshift_settlement_decimal == nightshift_settlement_decimal:
        #     Logging("Result was the same - System was correct")
        # else:
        #     Logging("Result was different - System was false")

        Logging("")
        Logging("Compare Schedules - Holiday Work with My work/ Settlement - Holidiay work")
        # Logging(schedules_holiday_work_settlement_decimal)
        # Logging(holiday_work_settlement_decimal)
        if schedules_holiday_work_settlement_decimal == holiday_work_settlement_decimal:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")

        Logging("")
        Logging("Compare Schedules - Holiday with My work/ Settlement - Holiday")
        # Logging(schedules_holiday_settlement_decimal)
        # Logging(holiday_settlement_decimal)
        if schedules_holiday_settlement_decimal == holiday_settlement_decimal:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")

        Logging("")
        Logging("Compare Schedules - Day off with My work/ Settlement - Day off")
        # Logging(schedules_day_off_settlement_decimal)
        # Logging(day_off_settlement_decimal)
        if schedules_day_off_settlement_decimal == day_off_settlement_decimal:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")

        Logging("")
        Logging("Compare Schedules -Vacation with My work/ Settlement - Vacation")
        # Logging(schedules_vacation_settlement_decimal)
        # Logging(vacation_settlement_decimal)
        if schedules_vacation_settlement_decimal == vacation_settlement_decimal:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")



        #Calculation step by step
        Logging("")
        Logging("Plus Worked time and Remaining working time to see if the result is equal to Scheduled working time or not")
        # Logging(WD_worked_days_decimal)
        # Logging(WD_remaining_working_days_decimal)
        # Logging(WD_scheduled_working_days_decimal)
        if WD_worked_days_decimal + WD_remaining_working_days_decimal == WD_scheduled_working_days_decimal:
            Logging("The result is equal to scheduled working day>>> System calculation is correct")
        else:
            Logging("The result is not equal to scheduled working day>>> System calculation is wrong")

        Logging("")
        Logging("Plus Worked days and Remaining working days to see if the result is equal to Scheduled working day or not")
        # Logging(worked_time_mywork_decimal)
        # Logging(remaining_working_time_mywork_decimal)
        # Logging(scheduled_working_time_mywork_decimal)
        if worked_time_mywork_decimal + remaining_working_time_mywork_decimal == scheduled_working_time_mywork_decimal:
            Logging("The result is equal to scheduled working day>>> System calculation is correct")
        else:
            Logging("The result is not equal to scheduled working day>>> System calculation is wrong")
    except:
        Logging("Check data fail")

    try:
        #Swtich to Admin
        Logging("")
        Logging("***ADMIN PAGE***")
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Dashboard')]").click()
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@data-lang-id,'tc_dashboard_name')]")))

        driver.find_element_by_xpath("//span[contains(.,'Switch to Admin')] ").click()
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Missing Time clock')] ")))
        time.sleep(3)

        Logging("***Avg Working Time***")
        open_box = driver.find_element_by_xpath("//span[contains(@data-lang-id,'tc_dashboard_avg_working_hours')]/../../../div[2]//button").text
        Logging("Date before change to next month: " + open_box)

        driver.find_element_by_xpath("//span[contains(@data-lang-id,'tc_dashboard_avg_working_hours')]/../../../div[2]//button").click()
        driver.find_element_by_xpath("//div[contains(@class,'month-header')]//a[2]").click()
        change_date = driver.find_element_by_xpath("//div[contains(@class,'react-datepicker')]/div[2]/div[2]/div[1]/div[1]").click()
        time.sleep(5)

        open_box2 = driver.find_element_by_xpath("//span[contains(@data-lang-id,'tc_dashboard_avg_working_hours')]/../../../div[2]//button").text
        Logging("Date after change to next month: " + open_box2)
        driver.find_element_by_xpath("//span[contains(@data-lang-id,'tc_dashboard_avg_working_hours')]/../../../div[2]//button").click()
        driver.find_element_by_xpath("//div[contains(@class,'react-datepicker__today-button')]").click()

        time.sleep(3)
        today = driver.find_element_by_xpath("//span[contains(@data-lang-id,'tc_dashboard_avg_working_hours')]/../../../div[2]//button").text
        Logging("Today: " + today)
        

        # #Compare
        # Logging("")
        # Logging("Compare Data - Date before change to next month with Date after change to next month")
        # # Logging(open_box)
        # # Logging(open_box2)
        # if open_box == open_box2:
        #     Logging("Result was the same - Changed date failed")
        # else:
        #     Logging("Result was different - Changed date successfully")

        #Compare
        Logging("")
        Logging("Compare Data - Date before change to next month with Today")
        # Logging(open_box)
        # Logging(today)
        if open_box == today:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")

        #Check if data is displayed or not
        Logging("")
        Logging("Check if data of Avg.Working time is displayed or not ")
        try:
            data_avg_working_time = driver.find_element_by_xpath("//span[contains(.,'Working Time')]/../../../..")
            if data_avg_working_time.is_displayed():
                Logging("Data is displayed")
        except:
                Logging("Data is not displayed")
    except:
        Logging("Check data fail")

    try:
        #WORKING TIME
        #Box 1
        Logging("")
        Logging("***Working Time***")
        click_pop_up = driver.find_element_by_xpath("//div[contains(@class,'user-working-hours-wrapper')]/div[2]/div[1]/div[1]/button").click()
        try:
            pop_up = driver.find_element_by_xpath("//div[contains(@class,'user-working-hours-wrapper')]/div[2]//div[contains(@class,'pos-absolute sort-container')]")
            if pop_up.is_displayed():
                Logging("Turn on checkbox successfully")
                try:
                    working_time_check_box = driver.find_element_by_xpath("//label[contains(@class,'custom-control-label') and contains(.,'Working time')]").click()
                    working_time_check_box_input = driver.find_element_by_xpath("//label[contains(@class,'custom-control-label') and contains(.,'Working time')]/../input")
                    if working_time_check_box_input.is_selected():
                        Logging("Check working time successfully")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["check_working_time"]["pass"])
                        try:
                            data_working_time = driver.find_element_by_xpath("//div[contains(@class,'user-working-hours-wrapper')]")
                            if data_working_time.is_displayed():
                                Logging("Working time data is displayed")
                                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["working_time_data"]["pass"])
                        except:
                                Logging("Working tine data is not displayed")
                                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["working_time_data"]["fail"])
                except: 
                        Logging("Check working time failed")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["check_working_time"]["fail"])

                try:
                    OT_check_box = driver.find_element_by_xpath("//label[contains(@class,'custom-control-label') and contains(.,'O/T')]").click()
                    OT_check_box_input = driver.find_element_by_xpath("//label[contains(@class,'custom-control-label') and contains(.,'O/T')]/../input")
                    if OT_check_box_input.is_selected():
                        Logging("")
                        Logging("Check OT successfully")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["check_OT_time"]["pass"])
                        try:
                            data_OT = driver.find_element_by_xpath("//div[contains(@class,'user-working-hours-wrapper')]")
                            if data_OT.is_displayed():
                                Logging("OT data is displayed")
                                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["OT_time_data"]["pass"])
                        except:
                                Logging("OT data is not displayed")
                                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["OT_time_data"]["fail"])
                except: 
                        Logging("Check OT failed")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["check_OT_time"]["fail"])
        except:
                Logging("Turn on check-box fail")

        #Box 2
        click_pop_up2 = driver.find_element_by_xpath("//div[contains(@class,'user-working-hours-wrapper')]/div[2]/div[1]/div[2]/button").click()
        time.sleep(5)
        try:
            pop_up2 = driver.find_element_by_xpath("//div[contains(@class,'user-working-hours-wrapper')]/div[2]//div[contains(@class,'pos-absolute limit-container')]")
            if pop_up2.is_displayed():
                Logging("")
                Logging("Turn on pop up filter successfully")
                try:
                    check_box = driver.find_element_by_xpath("//div[contains(@class,'user-working-hours-wrapper')]/div[2]//div[contains(@class,'pos-absolute limit-container')]/div[1]").click()
                    check_box_check = driver.find_element_by_xpath("//div[contains(@class,'user-working-hours-wrapper')]/div[2]//div[1]/*[contains(@class,'feather-check')]")
                    driver.find_element_by_xpath("//div[contains(@class,'user-working-hours-wrapper')]/div[2]/div[1]/div[2]/button").click()
                    if check_box_check.is_displayed():
                        Logging("Check filter-No.1 successfully")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["number_filter"]["pass"])
                        try:
                            filter_data = driver.find_element_by_xpath("//div[contains(@class,'user-working-hours-wrapper')]")
                            if filter_data.is_displayed():
                                Logging("Data is displayed")
                        except:
                                Logging("Data is not displayed")
                except: 
                        Logging("Check filter-No.1 failed")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["number_filter"]["fail"])
        except:
                Logging("Turn on pop up filter fail")


        #Click next page
        #Check if data is displayed or not
        Logging("")
        driver.find_element_by_xpath("//*[@id='app']//div[2]/ul/li[2]/a").click()
        Logging("Check if data of Admin-Working time is displayed or not after click to next page")
        try:
            data_working_time_next_page = driver.find_element_by_xpath("//div[contains(@class,'user-working-hours-wrapper')]")
            if data_working_time_next_page.is_displayed():
                Logging("Data is displayed")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_working_time_next_pgae"]["pass"])
        except:
                Logging("Data is not displayed")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_working_time_next_pgae"]["fail"])

        Logging("")
        avg_open_box = driver.find_element_by_xpath("//span[contains(@data-lang-id,'tc_status_analysis_total_time')]/../../../div[2]//button").text
        Logging("Date before change to next month: " + avg_open_box)

        driver.find_element_by_xpath("//span[contains(@data-lang-id,'tc_status_analysis_total_time')]/../../../div[2]//button").click()
        driver.find_element_by_xpath("//div[contains(@class,'month-header')]//a[2]").click()
        change_date = driver.find_element_by_xpath("//div[contains(@class,'react-datepicker')]/div[2]/div[2]/div[1]/div[1]").click()
        time.sleep(5)

        avg_open_box2 = driver.find_element_by_xpath("//span[contains(@data-lang-id,'tc_status_analysis_total_time')]/../../../div[2]//button").text
        Logging("Date after change to next month: " + avg_open_box2)
        driver.find_element_by_xpath("//span[contains(@data-lang-id,'tc_status_analysis_total_time')]/../../../div[2]//button").click()
        driver.find_element_by_xpath("//div[contains(@class,'react-datepicker__today-button')]").click()

        time.sleep(3)
        avg_today = driver.find_element_by_xpath("//span[contains(@data-lang-id,'tc_status_analysis_total_time')]/../../../div[2]//button").text
        Logging("Today: " + avg_today)

        #Compare
        # Logging("")
        # Logging("Compare Data - Date before change to next month with Date after change to next month")
        # # Logging(avg_open_box)
        # # Logging(avg_open_box2)
        # if avg_open_box == avg_open_box2:
        #     Logging("Result was the same - Changed date failed")
        # else:
        #     Logging("Result was different - Changed date successfully")

        #Compare
        Logging("")
        Logging("Compare Data - Date before change to next month with Today")
        # Logging(avg_open_box)
        # Logging(avg_today)
        if avg_open_box == avg_today:
            Logging("Result was the same - System was correct")
        else:
            Logging("Result was different - System was false")
    except:
        Logging("Check data fail")

    try:    
        #MISSING TIME CLOCK
        Logging("")
        Logging("***MISSING TIME CLOCK***")
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Timeline')]").click()
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Filters')] ")))
        time.sleep(2)
        driver.find_element_by_xpath("//div[contains(@class,'main-side-container-history')]/../../div[1]").click()
        time.sleep(5)
        try:
            icon = driver.find_element_by_xpath("//*[@id='popover-tree']")
            if icon.is_displayed():
                Logging("Success in open the organization box")
        except:
            Logging("Can't open the organization box")
        
        tl_search2 = driver.find_element_by_xpath("//span[contains(@class,'input-group-prepend')]//..//input")
        tl_search2.send_keys(data["name_keyword"][0])
        tl_search2.send_keys(Keys.ENTER)
        time.sleep(5)
        driver.find_element_by_xpath("//div[contains(@class,'avatar-wrapper')]//li").click()
        time.sleep(5)
        driver.find_element_by_xpath("//div[contains(@class,'main-side-container-history')]/../../div[1]").click()

        filters_input_dashboard = driver.find_element_by_xpath("//input[starts-with(@id, 'react-select')]")
        filters_input_dashboard.send_keys(Keys.ARROW_DOWN)
        filters_input_dashboard.send_keys(Keys.ENTER)
        time.sleep(3)
        driver.find_element_by_xpath("//div[contains(@class, 'timeline-item  ')]//div[contains(.,'Clock-In')]//div[contains(@class, 'd-flex ')]//span[2]//div[contains(@class, 'cursor-pointer')]").click()
        driver.find_element_by_xpath("//button//span[contains(.,'Delete')] ").click()
        #Logging("Delete punch-in successfully")

        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Dashboard')]").click()
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@data-lang-id,'tc_dashboard_missing_timeclock')]")))
        driver.find_element_by_xpath("//div[contains(@class,'missing-from-work-wrapper')]/div[1]//button").click()

        time.sleep(5)
        item_clock1 = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_dashboard_timeclock_status')]")
        item_clock1.location_once_scrolled_into_view
        time.sleep(3)
        #Logging("Scroll successfully")


        driver.find_element_by_xpath("//span[contains(.,'Clock In/Out')] ").click()
        #Select user
        driver.find_element_by_xpath("//button[starts-with(@id, 'contentTree')]").click()
        dashboard_search = driver.find_element_by_xpath("//*[@id='org-form-search']//input")
        dashboard_search.send_keys(data["name_keyword"][0])
        dashboard_search.send_keys(Keys.ENTER)
        time.sleep(2)
        driver.find_element_by_xpath("//span[contains(@class,'fancytree-title')]").click()
        try:
            user = driver.find_element_by_xpath("//button[starts-with(@id, 'contentTree')]/..//span[2]")
            if user.is_displayed():
                Logging("Select user successfully")
        except:
                Logging("Select user failed")

        driver.find_element_by_xpath("//span[contains(@data-lang-id,'tc_component_orgtree')]/../a").click()
        try:
            organization_box = driver.find_element_by_xpath("//div[starts-with(@id, 'contentPopover')]")
            if organization_box.is_displayed():
                Logging("Close organization box failed")
        except:
                Logging("Close organization box successfully")

        #Select clock in 
        driver.find_element_by_xpath("//button[starts-with(@id, 'btnHours')]").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[starts-with(@id, 'dropdown')]//div//button[contains(.,'08')]").click()
        #Input memo
        driver.find_element_by_xpath("//div[contains(@class, 'modal-content')]//div[5]//textarea[contains(@name, 'memo')]").send_keys("test")
        driver.find_element_by_xpath("//div[contains(@class, 'modal-content')]//span[contains(@data-lang-id, 'tc_action_save')]").click()
        time.sleep(2)
        Logging("Clock in through missing time clock successfully")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["clockin_through_missing_time_clock"]["pass"])
    except:
        Logging("Clock in through missing time clock failed")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["clockin_through_missing_time_clock"]["fail"])

    try:
        #TIME CLOCK STATUS
        Logging("")
        Logging("***Time Clock Status***")
        TCS_clock_in = driver.find_element_by_xpath(" //div[contains(@class,'working-status-ad-dash-wrapper')]/div[1]/div[1]")
        TCS_clock_in_time = TCS_clock_in.text
        TCS_clock_in_hour = TCS_clock_in_time.split(" ")[0]
        TCS_clock_in_number = int(TCS_clock_in_hour)
        Logging("Total people - Clock In: " + str(TCS_clock_in_number))

        TCS_tardiness = driver.find_element_by_xpath(" //div[contains(@class,'working-status-ad-dash-wrapper')]/div[1]/div[2]")
        TCS_tardiness_time = TCS_tardiness.text
        TCS_tardiness_hour = TCS_tardiness_time.split(" ")[0]
        TCS_tardiness_number = int(TCS_tardiness_hour)
        Logging("Total people - Tardiness: " + str(TCS_tardiness_number))

        TCS_no_clock_in = driver.find_element_by_xpath(" //div[contains(@class,'working-status-ad-dash-wrapper')]/div[1]/div[3]")
        TCS_no_clock_in_time = TCS_no_clock_in.text
        TCS_no_clock_in_hour = TCS_no_clock_in_time.split(" ")[0]
        TCS_no_clock_in_number = int(TCS_no_clock_in_hour)
        Logging("Total people - No Clock In: " + str(TCS_no_clock_in_number))

        TCS_clock_out = driver.find_element_by_xpath(" //div[contains(@class,'working-status-ad-dash-wrapper')]/div[1]/div[4]")
        TCS_clock_out_time = TCS_clock_out.text
        TCS_clock_out_hour = TCS_clock_out_time.split(" ")[0]
        TCS_clock_out_number = int(TCS_clock_out_hour)
        Logging("Total people - Clock Out: " + str(TCS_clock_out_number))

        TCS_leave_early = driver.find_element_by_xpath(" //div[contains(@class,'working-status-ad-dash-wrapper')]/div[1]/div[5]")
        TCS_leave_early_time = TCS_leave_early.text
        TCS_leave_early_hour = TCS_leave_early_time.split(" ")[0]
        TCS_leave_early_number = int(TCS_leave_early_hour)
        Logging("Total people - Leave Early: " + str(TCS_leave_early_number))

        TCS_vacation = driver.find_element_by_xpath(" //div[contains(@class,'working-status-ad-dash-wrapper')]/div[1]/div[6]")
        TCS_vacation_time = TCS_vacation.text
        TCS_vacation_hour = TCS_vacation_time.split(" ")[0]
        TCS_vacation_number = int(TCS_vacation_hour)
        Logging("Total people - Vacation: " + str(TCS_vacation_number))
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_time_clock_status"]["pass"])
    except:
        Logging("Data is not displayed")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_time_clock_status"]["fail"])

    # try:
    #     #Click to another day to see if data is still displayed or not
    #     Logging("")
    #     TCS_open_date = driver.find_element_by_xpath("//span[contains(.,'Time clock status')]/../../../div[2]//button").text
    #     Logging("Date before change to another day: " + TCS_open_date)
    #     driver.find_element_by_xpath("//span[contains(.,'Time clock status')]/../../../div[2]//button").click()
    #     driver.find_element_by_xpath("//div[contains(@class,'react-datepicker')]/div[2]/div[2]/div[1]/div[5]").click()
    #     time.sleep(2)
    #     TCS_open_date_change = driver.find_element_by_xpath("//span[contains(.,'Time clock status')]/../../../div[2]//button").text
    #     Logging("Date after change to 1st day: " + TCS_open_date_change)

    #     #Compare
    #     Logging("")
    #     Logging("Compare Data - Date before change to next month with Today")
    #     # Logging(avg_open_box)
    #     # Logging(avg_today)
    #     if TCS_open_date == TCS_open_date_change:
    #         Logging("Result was the same - Change date failed")
    #     else:
    #         Logging("Result was different - Change date successfully")

    #     #Check if data of Time Clock Status is displayed or not after click to 1st day
    #     Logging("Check if data of Time Clock Status is displayed or not after click to 1st day")
    #     try:
    #         data_time_clock_status = driver.find_element_by_xpath("//div[contains(@class,'working-status-ad-dash-wrapper')]")
    #         if data_time_clock_status.is_displayed():
    #             Logging("Data is displayed")
    #     except:
    #             Logging("Data is not displayed")
    # except:
    #     Logging("Check data failed")


    try:
        #Dashboard - Admin - Device
        time.sleep(5)
        beacon_admin = driver.find_element_by_xpath("//div[contains(@class,'punch-device-total-col')]//div[1]/div[4]/div[1]")
        beacon_admin.location_once_scrolled_into_view
        time.sleep(5)
        #Logging("Scroll successfully")
        
        Logging("")
        Logging("***DEVICE***")
        admin_device_web = driver.find_element_by_xpath("//div[contains(@class,'punch-device-total-col')]//div[contains(@class,'punch-detail-info')]/div[1]/div[1]/div[2]")
        Logging("Web: " + admin_device_web.text)
        admin_device_wifi = driver.find_element_by_xpath("//div[contains(@class,'punch-device-total-col')]//div[contains(@class,'punch-detail-info')]/div[1]/div[2]/div[2]")
        Logging("Wifi: " + admin_device_wifi.text)
        admin_device_gps = driver.find_element_by_xpath("//div[contains(@class,'punch-device-total-col')]//div[contains(@class,'punch-detail-info')]/div[1]/div[3]/div[2]")
        Logging("GPS: " + admin_device_gps.text)
        admin_device_beacon = driver.find_element_by_xpath("//div[contains(@class,'punch-device-total-col')]//div[contains(@class,'punch-detail-info')]/div[1]/div[4]/div[2]")
        Logging("Beacon: " + admin_device_beacon.text)
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_device"]["pass"])
    except:
        Logging("Device-Data - Check data failed")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_device"]["fail"])

    try:
        #Check if the circle is displayed or not
        Logging("")
        time.sleep(5)
        Logging("Check if the chart of Device is displayed or not")
        try:
            admin_chart_device = driver.find_element_by_xpath("//span[contains(.,'Device')]/../../../..//div[contains(@class, 'chart-wrapper')]")
            if admin_chart_device.is_displayed():
                Logging("Chart is displayed")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_device_chart"]["pass"])
        except:
                Logging("Chart is not displayed")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_device_chart"]["fail"])
    except:
        Logging("Device-Chart - Check data fail")


    try:
        #Dashboard - Admin - Working status
        #Check data
        Logging(" ")
        try:
            ws_no_clock_in = driver.find_element_by_xpath("//div[contains(@class,'icon-description')]/..//div[contains(@class,'text-truncate') and contains(.,'No Clock-In')]")
            if ws_no_clock_in.is_displayed:
                Logging("No Clock-In - Data is displayed")
        except:
            Logging("No Clock-In - No data")

        try:
            ws_clock_out = driver.find_element_by_xpath("//div[contains(@class,'icon-description')]/..//div[contains(@class,'text-truncate') and contains(.,'Clock-Out')]")
            if ws_clock_out.is_displayed:
                Logging("Clock-Out - Data is displayed")
        except:
            Logging("Clock-Out - No data")   
            
        try:
            ws_working = driver.find_element_by_xpath("//div[contains(@class,'icon-description')]/..//div[contains(@class,'text-truncate') and contains(.,'Working')]")
            if ws_working.is_displayed:
                Logging("Working - Data is displayed")
        except:
            Logging("Working - No data")

        try:
            ws_clock_in = driver.find_element_by_xpath("//div[contains(@class,'icon-description')]/..//div[contains(@class,'text-truncate') and contains(.,'Clock-In')]")
            if ws_clock_in.is_displayed:
                Logging("Clock-In - Data is displayed")
        except:
            Logging("Clock-In - No data")

        try:
            ws_tarrdiness = driver.find_element_by_xpath("//div[contains(@class,'icon-description')]/..//div[contains(@class,'text-truncate') and contains(.,'Tardiness')]")
            if ws_tarrdiness.is_displayed:
                Logging("Tardiness - Data is displayed")
        except:
            Logging("Tardiness - No data")

        try:
            ws_vacation = driver.find_element_by_xpath("//div[contains(@class,'icon-description')]/..//div[contains(@class,'text-truncate') and contains(.,'Vacation')]")
            if ws_vacation.is_displayed:
                Logging("Vacation - Data is displayed")
        except:
            Logging("Vacation - No data")

        try:
            ws_day_off = driver.find_element_by_xpath("//div[contains(@class,'icon-description')]/..//div[contains(@class,'text-truncate') and contains(.,'Day Off')]")
            if ws_day_off.is_displayed:
                Logging("Day Off - Data is displayed")
        except:
            Logging("Day Off - No data")

        try:
            ws_holiday = driver.find_element_by_xpath("//div[contains(@class,'icon-description')]/..//div[contains(@class,'text-truncate') and contains(.,'Holiday')]")
            if ws_holiday.is_displayed:
                Logging("Holiday - Data is displayed")
        except:
            Logging("Holiday - No data")

        try:
            ws_ouside = driver.find_element_by_xpath("//div[contains(@class,'icon-description')]/..//div[contains(@class,'text-truncate') and contains(.,'Outside')]")
            if ws_ouside.is_displayed:
                Logging("Outside - Data is displayed")
        except:
            Logging("Outside - No data")

        try:
            ws_meeting = driver.find_element_by_xpath("//div[contains(@class,'icon-description')]/..//div[contains(@class,'text-truncate') and contains(.,'Meeting')]")
            if ws_meeting.is_displayed:
                Logging("Meeting - Data is displayed")
        except:
            Logging("Meeting - No data")

        try:
            ws_education = driver.find_element_by_xpath("//div[contains(@class,'icon-description')]/..//div[contains(@class,'text-truncate') and contains(.,'Education')]")
            if ws_education.is_displayed:
                Logging("Education - Data is displayed")
        except:
            Logging("Education - No data")

        try:
            ws_business_trip = driver.find_element_by_xpath("//div[contains(@class,'icon-description')]/..//div[contains(@class,'text-truncate') and contains(.,'Business Trip')]")
            if ws_business_trip.is_displayed:
                Logging("Business Trip - Data is displayed")
        except:
            Logging("Business Trip - No data")

        try:
            ws_away = driver.find_element_by_xpath("//div[contains(@class,'icon-description')]/..//div[contains(@class,'text-truncate') and contains(.,'Away')]")
            if ws_away.is_displayed:
                Logging("Away - Data is displayed")
        except:
            Logging("Away - No data")

        try:
            ws_leave = driver.find_element_by_xpath("//div[contains(@class,'icon-description')]/..//div[contains(@class,'text-truncate') and contains(.,'Leave')]")
            if ws_leave.is_displayed:
                Logging("Leave - Data is displayed")
        except:
            Logging("Leave - No data")
    except:
        Logging("Data is not displayed")


    try:
        #Check if the circle is displayed or not
        Logging("")
        time.sleep(5)
        Logging("Check if the chart of Working Status is displayed or not")
        try:
            admin_chart_working_status = driver.find_element_by_xpath("//span[contains(.,'Working Status')]/../../../..//div[contains(@class, 'chart-wrapper')]")
            if admin_chart_working_status.is_displayed():
                Logging("Chart is displayed")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_working_status_chart"]["pass"])
        except:
                Logging("Chart is not displayed")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_working_status_chart"]["fail"])
    except:
        Logging("Working status - Chart - Check data fail")

    driver.refresh()
    driver.find_element_by_xpath("//span[contains(.,'Switch to Admin')] ").click()
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Missing Time clock')] ")))
    time.sleep(3)

    try:
        scroll_daily_status = driver.find_element_by_xpath("//span[contains(.,'Timeline')]/../.. /..//span[contains(@data-lang-id,'tc_status_view_more')]")
        scroll_daily_status.location_once_scrolled_into_view
        #Access Daily Status page through Admin-Working status
        Logging("")
        time.sleep(3)
        driver.find_element_by_xpath("//span[contains(.,'Working Status')]/../.. /..//span[contains(@data-lang-id,'tc_status_view_more')]").click()
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Name')] ")))
        time.sleep(5)

        Logging("Check if able to access Daily Status page through Admin - Working status or not")
        try:
            admin_working_status_more = driver.find_element_by_xpath("//*[@id='divMenu']/span")
            if admin_working_status_more.is_displayed():
                Logging("Access Daily Status page successfully")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_working_status_more"]["pass"])
        except:
                Logging("Access Daily Status page failed")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_working_status_more"]["fail"])
    except:
        Logging("Access Daily Status page failed")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_working_status_more"]["fail"])


    try:
        driver.find_element_by_xpath("//span[contains(@class, 'text-truncate') and contains(., 'Dashboard')]").click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@data-lang-id,'tc_dashboard_my_board')]")))
        time.sleep(5)
        beacon_admin = driver.find_element_by_xpath("//div[contains(@class, 'daily-sidebar')]")
        beacon_admin.location_once_scrolled_into_view
        time.sleep(5)
    except:
        Logging(" ")

    try:
        #Check if data is displayed or not
        time.sleep(5)
        Logging("Check if data of Timeline is displayed or not")
        try:
            admin_timeline = driver.find_element_by_xpath("//div[contains(@class, 'daily-sidebar')]")
            if admin_timeline.is_displayed():
                Logging("Data is displayed")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_timeline"]["pass"])
        except:
                Logging("Data is not displayed")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_timeline"]["fail"])
    except:
        Logging("Timelilne - Check data fail")

    driver.refresh()

    try:
        scroll_timeline = driver.find_element_by_xpath("//span[contains(.,'Timeline')]/../.. /..//span[contains(@data-lang-id,'tc_status_view_more')]")
        scroll_timeline.location_once_scrolled_into_view
        #Access Timeline page through Admin-Timeline
        Logging("")
        time.sleep(3)
        driver.find_element_by_xpath("//span[contains(.,'Timeline')]/../.. /..//span[contains(@data-lang-id,'tc_status_view_more')]").click()
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Filters')]")))

        Logging("Check if able to access Timeline page through Admin - Timeline or not")
        try:
            admin_timeline_more = driver.find_element_by_xpath("//span[contains(.,'Filters')]")
            if admin_timeline_more.is_displayed():
                Logging("Access Timeline page successfully")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_timeline_more"]["pass"])
        except:
                Logging("Access Timeline page failed")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_timeline_more"]["fail"])
    except:
        Logging("Access Timeline page failed")
        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["admin_timeline_more"]["fail"])


def basic_gps():
    try:
        driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_menu_basic_settings') and contains(., 'Basic')]").click()
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@data-lang-id, 'tc_general_requeset_setting') and contains(., 'Request Settings')]")))
        time.sleep(2)
        driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_title_clock_in_out') and contains(., 'TimeClock')]").click()
        time.sleep(3)
    except:
        Logging(" ")

    Logging(" ")
    Logging("***ADD GPS***")
    driver.find_element_by_xpath("//button[contains(@keylang, 'tc_action_add')]").click()
    time.sleep(3)
    input_name_gps = driver.find_element_by_xpath("//label[contains(@data-lang-id, 'tc_gps_name')]//..//input")
    input_name_gps.send_keys("hanhtest")

    select_work_place = driver.find_element_by_xpath("//input[starts-with(@id, 'react-select')]")
    select_work_place.click()
    time.sleep(3)
    #select_work_place.send_keys(Keys.ARROW_DOWN)
    select_work_place.send_keys(Keys.ENTER)

    input_address = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_gps_search_location')]//..//input")
    input_address.send_keys("400 Nguyễn Thị Thập")
    time.sleep(3)
    input_address.send_keys(Keys.ENTER)
    time.sleep(3)
    #SAVE GPS
    driver.find_element_by_xpath("//div[contains(@class, 'modal-footer')]//span[contains(@data-lang-id, 'tc_action_save')]").click()
    time.sleep(3)
    try:
        gps_noti = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["pre_OT_noty"])))
        gps_noti_list = [data["TIMECARD"]["gps_noti"][0], data["TIMECARD"]["gps_noti"][1]]
        if gps_noti.text in gps_noti_list:
            Logging("Duplicated data is available")
            click_cancel = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_action_cancel')]").click()
            time.sleep(3)
        else:
            time.sleep(3)
            gps_name = driver.find_element_by_xpath("//form//div[1]/div[1]/div/span[contains(@ref, 'eCellValue')]/div").text
            try:
                if gps_name == "hanhtest":
                    Logging("Add GPS successfully")
                    TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["add_gps"]["pass"])
            except:
                Logging("Add GPS failed")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["add_gps"]["fail"])
    except: 
        Logging(" ")

    time.sleep(5)
    #Edit 
    Logging("")
    Logging("***EDIT GPS")
    try:
        driver.find_element_by_xpath("//form//div[1]/div[5]/div/span[contains(@ref, 'eCellValue')]/div/div/div/div[1]/div").click()
        edit_gps = driver.find_element_by_xpath("//span//span[contains(@data-lang-id, 'tc_action_edit')]")
        if edit_gps.is_displayed():
            try:
                input_name_gps = driver.find_element_by_xpath("//label[contains(@data-lang-id, 'tc_gps_name')]//..//input")
                input_name_gps.clear()
                input_name_gps.send_keys("test edit")
                driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_action_save')]/..").click()
                time.sleep(3)
                gps_name = driver.find_element_by_xpath("//form//div[1]/div[1]/div/span[contains(@ref, 'eCellValue')]/div").text
                try:
                    if gps_name == "test edit":
                        Logging("Edit Name successfully")
                        TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["edit_gps"]["pass"])
                except:
                    Logging("Edit Name failed")
                    TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["edit_gps"]["fail"])
            except:
                Logging("Can't edit Name") 
        else:
            Logging("Can't open edit dialog")
    except:
        Logging("Can't open edit dialog")

    #Check data
    Logging(" ")
    try:
        gps_name = driver.find_element_by_xpath("//form//div[1]/*[@col-id='name']//span[contains(@ref, 'eCellValue')]/div")
        if gps_name.is_displayed():
            Logging("Name - Data is displayed")
    except:
        Logging("Name - Data is not displayed")

    try:
        gps_work_place = driver.find_element_by_xpath("//form//div[1]/*[@col-id='workplace_name']//span[contains(@ref, 'eCellValue')]/div")
        if gps_work_place.is_displayed():
            Logging("Work Place - Data is displayed")
    except:
        Logging("Work Place - Data is not displayed")

    try:
        gps_range = driver.find_element_by_xpath("//form//div[1]/*[@col-id='range']//span[contains(@ref, 'eCellValue')]/div")
        if gps_name.is_displayed():
            Logging("GPS Range - Data is displayed")
    except:
        Logging("GPS Range - Data is not displayed")

    try:
        gps_address = driver.find_element_by_xpath("//form//div[1]/*[@col-id='gps_name']//span[contains(@ref, 'eCellValue')]/div")
        if gps_address.is_displayed():
            Logging("Address - Data is displayed")
    except:
        Logging("Address - Data is not displayed")

    #Research field
    Logging(" ")
    try:
        search_field = driver.find_element_by_xpath("//div[contains(@class, 'input-gps-search')]//input")
        search_field.send_keys("test edit")
        time.sleep(3)
        search_field.send_keys(Keys.ENTER)
        time.sleep(3)
        try:
            gps_name = driver.find_element_by_xpath("//form//div[1]/div[1]/div/span[contains(@ref, 'eCellValue')]/div").text
            if gps_name == "test edit":
                Logging("Search GPS successfully")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["search_gps"]["pass"])
        except:
            Logging("Seach GPS failed")
            TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["search_gps"]["fail"])
    except:
        Logging("Search box empty")


    Logging("")
    Logging("***DELETE GPS")
    try:
        driver.find_element_by_xpath("//form//div[1]/div[5]/div/span[contains(@ref, 'eCellValue')]/div/div/div/div[2]/div").click()
        time.sleep(3)
        delete_gps = driver.find_element_by_xpath("//p[contains(@data-lang-id, 'tc_component_confirm_delete')]")
        if delete_gps.is_displayed():
            #Logging("Open delete dialog succeessfully")
            time.sleep(3)
            driver.find_element_by_xpath("//button//span[contains(@data-lang-id, 'tc_action_delete')]").click()
            time.sleep(1)
            delete_noti = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["pre_OT_noty"])))
            delete_noti_list = [data["TIMECARD"]["delete_noti"][0], data["TIMECARD"]["delete_noti"][1]]
            if delete_noti.text in delete_noti_list:
                Logging("Delete GPS successfully")
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["delete_gps"]["pass"])
            else:
                Logging("Delete GPS failed") 
                TesCase_LogResult(**data["testcase_result"]["HR-Timecard"]["delete_gps"]["fail"])
        else:
            Logging("Can't open delete dialog")
    except:
        Logging("Can't open delete dialog")


def exception_users():
    Logging("")
    Logging("*** ADD EXCEPTION USERS")
    time.sleep(2)
    exception_users = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_title_exception')]").click()
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@data-lang-id, 'tc_select_users_are_invisible')]")))
    time.sleep(2)
    input_exc_user = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_exception_user')]/../../../..//input")
    input_exc_user.send_keys(data["name_keyword"][0])
    time.sleep(2)
    input_exc_user.send_keys(Keys.ENTER)
    time.sleep(3)
    exception_user_name = driver.find_element_by_xpath("//*[starts-with(@id,'ft-id')]//span/span[@class='fancytree-title']")
    exception_user_name.click()
    time.sleep(2)
    exception_users_add = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_exception_user')]/../../../..//label[contains(@data-lang-id, 'tc_action_add')]").click()
    time.sleep(2)
    
    try:
        exc_user_noti =  driver.find_element_by_xpath("//*[starts-with(@id,'noty_bar')]//div[contains(@class,'alert-body')]")
        if exc_user_noti.text == "There is duplicated data, please try again":
            Logging("Duplicated data is available")
        elif exc_user_noti.text == "Data saved successfully.":
            Logging("Add exception user successfully")
    except:
        Logging("Add exception user failed")
    
    Logging(" ")
    Logging("*** DELETE EXCEPTION USER")
    add_name_manager = driver.find_element_by_xpath("//span[text()='Exception Users']//following::div//ul//li//div[contains(@class,'first-line') and contains(.,'" + str(exception_user_name.text) + "')]")
    if add_name_manager.is_displayed():
        Logging("User " + str(exception_user_name.text) + " is display in exception users list")
        add_name_manager.click()
        driver.find_element_by_xpath("//span[text()='Exception Users']//following::div//ul//li//div[contains(@class,'first-line') and contains(.,'" + str(exception_user_name.text) + "')]//following::div[2]").click()
        driver.find_element_by_xpath("//button/span[contains(@data-lang-id, 'tc_action_delete')]").click()
        time.sleep(2)

        try:
            notice_success =  driver.find_element_by_xpath("//*[starts-with(@id,'noty_bar')]//div[contains(text(),'Data deleted successfully.')]")
            if notice_success.is_displayed():
                Logging("Delete exception user successfully")
        except:
            Logging("Delete exception user failed")
    else:
        Logging("- User " + str(exception_user_name.text) + " isn't display in exception users list")


def outside_users():   
    Logging(" ")
    Logging("*** ADD OUTSIDE ATTENDANCE AVAILABLE USERS")

    input_out_user = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_available_user')]/../../../..//input")
    input_out_user.send_keys(data["name_keyword"][0])
    time.sleep(2)
    input_out_user.send_keys(Keys.ENTER)
    time.sleep(3)
    outside_user_name = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_outside_clock_in_out_exception_users')]/../..//span[@class='fancytree-title']")
    outside_user_name.click()
    time.sleep(2)
    outside_users_add = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_outside_clock_in_out_exception_users')]/../..//label[contains(@data-lang-id, 'tc_action_add')]").click()
    time.sleep(2)
    
    try:
        out_user_noti =  driver.find_element_by_xpath("//*[starts-with(@id,'noty_bar')]//div[contains(@class,'alert-body')]")
        if out_user_noti.text == "There is duplicated data, please try again":
            Logging("Duplicated data is available")
        elif out_user_noti.text == "Data saved successfully.":
            Logging("Add outside attendance available user successfully")
    except:
        Logging("Add outside attendance available user failed")

    Logging(" ")
    Logging("*** DELETE OUTSIDE ATTENDANCE AVAILABLE USERS")
    add_outside_name = driver.find_element_by_xpath("//span[text()='Available Users']//following::div//ul//li//div[contains(@class,'first-line') and contains(.,'" + str(outside_user_name.text) + "')]")
    if add_outside_name.is_displayed():
        Logging("User " + str(outside_user_name.text) + " is display in available users list")
        add_outside_name.click()
        driver.find_element_by_xpath("//span[text()='Available Users']//following::div//ul//li//div[contains(@class,'first-line') and contains(.,'" + str(outside_user_name.text) + "')]//following::div[2]").click()
        driver.find_element_by_xpath("//button/span[contains(@data-lang-id, 'tc_action_delete')]").click()
        time.sleep(2)

        try:
            outside_notice =  driver.find_element_by_xpath("//*[starts-with(@id,'noty_bar')]//div[contains(text(),'Data deleted successfully.')]")
            if outside_notice.is_displayed():
                Logging("Delete outside attendance available user successfully")
        except:
            Logging("Delete outside attendance available user failed")
    else:
        Logging("- User " + str(outside_user_name.text) + " isn't display in available users list")


def arbitrary_decision():
    Logging("")
    Logging("*** ADD ARBITRARY DECISION")
    time.sleep(2)
    arbitrary_user = driver.find_element_by_xpath("//a[contains(@href,'/nhr/hr/timecard/admin/basic/approval')]").click()
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@data-lang-id, 'tc_title_arbitrary_decision_setting')]")))
    time.sleep(2)

    arbitrary_user_select = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_general_select_approver')]").click()
    time.sleep(2)
    input_arbitrary_user = driver.find_element_by_xpath("//*[@id='org-form-search']//input")
    input_arbitrary_user.send_keys(data["name_keyword"][0])
    time.sleep(2)
    input_arbitrary_user.send_keys(Keys.ENTER)
    time.sleep(3)
    arbitrary_user_name = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_title_arbitrary_decision')]/../..//span[@class='fancytree-title']")
    arbitrary_user_name.click()
    time.sleep(2)
    arbitrary_users_add = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_title_arbitrary_decision')]/../..//label[contains(@data-lang-id, 'tc_action_add')]").click()
    time.sleep(2)
    try:
        arbitrary_user_noti =  driver.find_element_by_xpath("//*[starts-with(@id,'noty_bar')]//div[contains(@class,'alert-body')]")
        if arbitrary_user_noti.text == "There is duplicated data, please try again":
            Logging("Duplicated data is available")
        elif arbitrary_user_noti.text == "Data saved successfully.":
            Logging("Add arbitrary decision successfully")
    except:
        Logging("Add arbitrary decision failed")
  
    Logging(" ")
    Logging("*** DELETE ARBITRARY DECISION")
    add_arbitrary_name = driver.find_element_by_xpath("//span[text()='Available Users']//following::div//ul//li//div[contains(@class,'first-line') and contains(.,'" + str(arbitrary_user_name.text) + "')]")
    if add_arbitrary_name.is_displayed():
        Logging("User " + str(arbitrary_user_name.text) + " is display in available users list")
        add_arbitrary_name.click()
        driver.find_element_by_xpath("//span[text()='Available Users']//following::div//ul//li//div[contains(@class,'first-line') and contains(.,'" + str(arbitrary_user_name.text) + "')]//following::div[2]").click()
        driver.find_element_by_xpath("//button/span[contains(@data-lang-id, 'tc_action_delete')]").click()
        time.sleep(2)

        try:
            arbitrary_notice =  driver.find_element_by_xpath("//*[starts-with(@id,'noty_bar')]//div[contains(text(),'Data deleted successfully.')]")
            if arbitrary_notice.is_displayed():
                Logging("Delete arbitrary decision successfully")
        except:
            Logging("Delete arbitrary decision failed")
    else:
        Logging("- User " + str(arbitrary_user_name.text) + " isn't display in available users list")


def OT_post_midnight():
    time.sleep(5)
    # midnight_popup = driver.find_element_by_xpath("//span[contains(.,'Confirm Nightwork')]")
    # if midnight_popup.is_displayed():
    #     Logging("Nightwork popup is display")
    #     click_confirm = driver.find_element_by_xpath("//span[contains(.,'Yes, confirm it!')]").click()
    # else:
    #     Logging("No nightwork")

    try:
        midnight_popup = driver.find_element_by_xpath("//span[contains(.,'Confirm Nightwork')]")
        if midnight_popup.is_displayed():
            Logging("Nightwork popup is display")
            click_confirm = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'Yes, confirm it!')]").click()
            click_apply_OT = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_action_apply_ot')]").click()
            input_memo_OT = driver.find_element_by_xpath("//textarea[contains(@class, 'form-control')]")
            input_memo_OT.send_keys("This is a test")
            time.sleep(3)
            scroll_apply_OT = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_action_apply')]")
            scroll_apply_OT.location_once_scrolled_into_view
            time.sleep(2)
            #Export data
            approver_data = driver.find_element_by_xpath("//div[contains(@class, 'approver-wrapper ')]//li/div/div[1]").text
            Logging ("Approver: " + approver_data)
            referrer_data = driver.find_element_by_xpath("//div[contains(@class, 'referer-wrapper')]//li/div/div[1]").text
            Logging ("Referrer: " + referrer_data)
            time.sleep(3)
            apply_OT_confirm = driver.find_element_by_xpath("//span[contains(@data-lang-id, 'tc_action_apply')]/..").click()
            Logging("Apply OT successfully - Approval is submitted successfully")
            time.sleep(3)
            #Approval page
            approval_page = driver.find_element_by_xpath("//li//a[contains(@href,'/nhr/hr/timecard/user/approval')]//span[contains(@data-lang-id, 'tc_approval_approval')]").click()
            
            status_approve = driver.find_element_by_xpath("//form//div[2]/div/div/div[1]/*[@col-id='type_name']")
            #Logging (status_approve.text)
            if status_approve.is_displayed():
                Logging (status_approve.text)
                if status_approve.text == "Over Time":
                    Logging ("Approval is displayed in approval list")
                    #Reject approve
                    driver.find_element_by_xpath("//div[contains(@class, 'select-approval-status')]//div").click()
                    driver.find_element_by_xpath("//div[contains(@data-lang-id, 'tc_action_reject')]").click()
                    time.sleep(3)
                    #Scroll to detail
                    slider = driver.find_element_by_xpath("//div[@ref='eBodyHorizontalScrollViewport']")
                    horizontal_bar = driver.find_element_by_xpath("//div[@ref='eHorizontalRightSpacer']")
                    webdriver.ActionChains(driver).click_and_hold(slider).move_to_element(horizontal_bar).perform()
                    webdriver.ActionChains(driver).release().perform()
                    #Logging ("Scroll successfully")
                    #Click view details
                    driver.find_element_by_xpath("//div[1]/*[@col-id='id']//div[contains(@class, 'btn-view-detail')]").click()

                    #Print status column
                    postOT_event_status = driver.find_element_by_xpath("//div[contains(@class, 'avatar-wrapper')]/..//div[contains(@class, 'approval-status')]").text
                    if postOT_event_status.text == "Pending":
                        Logging ("Status is not changed => Approve failed")
                    elif postOT_event_status.text == "Reject":
                        Logging ("Status is changed => Approve successfully")
                else:
                    Logging ("Approval is not displayed in approval list")
            else: 
                Logging ("Approval is submitted failed")
        else:
            Logging("Apply OT failed - Approval is submitted failed")
    except:
            Logging("No nightwork")
    



def timecard():
    nightwork()
    breaktime()
    clock_out()
    output_clockin,output_clockout,break_time,working_time,clock_in_time,work_method_up,today_work_date, OT_time = check_time()
    timesheet_list(output_clockin,output_clockout,break_time,working_time, OT_time)
    # add_event2()
    # view_details()
    # working_status()

    # # day_list = find_date(today_work_date)
    # #work_schedule(day_list)
    # manager()
    # total_manager()
    # # work_correction()
    # delete_punch()

def time_card():
    # # # # Napproval_OT()
    #weekly_status()
    status1 = daily_status()

    rp=report()
    working_time_report_decimal=rp[0]
    worked_time_report_decimal=rp[1]
    break_time_report_decimal=rp[2]

    clockin()
    timesheet_calendar_check()
    clockout()
    edit_clockin()

    nb_out=edit_clockout()
    hour_number1=nb_out[0]
    working_number1=nb_out[1]
    break_number1=nb_out[2]
    OT_number1=nb_out[3]

    nb_report=report_2nd()
    working_time_decimal_2nd=nb_report[0]
    worked_time_decimal_2nd =nb_report[1]
    break_time_decimal_2nd = nb_report[2]

    calculation(working_time_report_decimal,worked_time_report_decimal,break_time_report_decimal,hour_number1,working_number1,break_number1,working_time_decimal_2nd,worked_time_decimal_2nd,break_time_decimal_2nd)

    daily_status2(status1,break_number1,working_number1,OT_number1)

    #weekly_status2()

    company_timecard_reports()

    timeline()


    work_place()

    report_weekly()

    report_list()


    dashboard()

    basic_gps()

    exception_users()

    outside_users()

    arbitrary_decision()
    
    # # # OT_post_midnight()

    # work_shift()

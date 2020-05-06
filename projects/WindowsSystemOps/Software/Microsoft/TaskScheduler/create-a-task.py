#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:create-a-task.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/2/2
Create Time:            18:33
Description:            create a Microsoft Windows Task with Python
Long Description:       
References:             [Using the Task Scheduler](https://docs.microsoft.com/en-us/windows/win32/taskschd/using-the-task-scheduler)
Prerequisites:          pip install pywin32  # https://www.lfd.uci.edu/~gohlke/pythonlibs/#pywin32
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """
import datetime

import win32com.client

scheduler_service = win32com.client.Dispatch('Schedule.Service')
scheduler_service.Connect()

# https://docs.microsoft.com/en-us/windows/win32/taskschd/taskservice-getfolder
root_folder = scheduler_service.GetFolder('\\')

# https://docs.microsoft.com/en-us/windows/win32/taskschd/taskservice-newtask
flags = 0
task_definition = TaskDefinition = scheduler_service.NewTask(
    flags)  # This parameter is reserved for future use and must be set to 0.

# Creates a new trigger for the task.
# https://docs.microsoft.com/en-us/windows/win32/taskschd/triggercollection
# https://docs.microsoft.com/en-us/windows/win32/taskschd/triggercollection-create
TASK_TRIGGER_TIME = 1  # Triggers the task at a specific time of day.
TASK_TRIGGER_DAILY = 2  # Triggers the task on a daily schedule.
TASK_TRIGGER_WEEKLY = 3  # Triggers the task on a weekly schedule.
TASK_TRIGGER_MONTHLY = 4  # Triggers the task on a monthly schedule.

# time str format: "2006-05-02T08:00:00"
start_time = (datetime.datetime.now() + datetime.timedelta(minutes=15)).isoformat()


def create_task_trigger_time(at_time):
    # Starting an Executable at a Specific Time
    # https://docs.microsoft.com/en-us/windows/win32/taskschd/time-trigger-example--scripting-
    # https://docs.microsoft.com/en-us/windows/win32/taskschd/trigger
    trigger = task_definition.Triggers.Create(TASK_TRIGGER_TIME)  #
    trigger.StartBoundary = at_time


def create_task_trigger_daily(at_time):
    # Starting an Executable Daily
    # https://docs.microsoft.com/en-us/windows/win32/taskschd/daily-trigger-example--scripting-
    # https://docs.microsoft.com/en-us/windows/win32/taskschd/trigger
    trigger = task_definition.Triggers.Create(TASK_TRIGGER_DAILY)  #
    trigger.StartBoundary = at_time
    trigger.DaysInterval = 1  # Task runs every day.


def create_task_trigger_weekly(at_time, day_of_week=1):
    # Starting an Executable Weekly
    # https://docs.microsoft.com/en-us/windows/win32/taskschd/weekly-trigger-example--scripting-
    if day_of_week not in [1, 2, 4, 8, 16, 32, 64]:
        raise RuntimeError("bad parameters: day_of_week")
    # https://docs.microsoft.com/en-us/windows/win32/taskschd/trigger
    trigger = task_definition.Triggers.Create(TASK_TRIGGER_WEEKLY)
    trigger.StartBoundary = at_time
    # https://docs.microsoft.com/en-us/windows/win32/taskschd/weeklytrigger-daysofweek
    trigger.DaysOfWeek = day_of_week  # value can be [1, 2, 4, 8, 16, 32, 64]
    trigger.WeeksInterval = 1  # Task runs every week.
    # https://docs.microsoft.com/en-us/windows/win32/taskschd/trigger-id
    trigger.Id = "PythonTestTaskWeeklyTriggerId"  # used by the Task Scheduler for logging purposes.
    trigger.Enabled = True


# create_task_trigger_time(start_time)
# create_task_trigger_daily(start_time)
create_task_trigger_weekly(start_time, 1)  # 1 means Sunday, 2 means Monday

# Create action
# https://docs.microsoft.com/en-us/windows/win32/taskschd/action
# https://docs.microsoft.com/en-us/windows/win32/taskschd/actioncollection-create
TASK_ACTION_EXEC = 0  # The action performs a command-line operation.
action = task_definition.Actions.Create(TASK_ACTION_EXEC)
# https://docs.microsoft.com/en-us/windows/win32/taskschd/action-id
# The user-defined identifier for the action. This identifier is used by the Task Scheduler for logging purposes.
action.ID = 'PythonTestTaskActionId'  # Gets or sets the identifier of the action.
action.Path = 'cmd.exe'  # Gets or sets the path to an executable file.
action.Arguments = '/c "exit"'  # Gets or sets the arguments associated with the command-line operation.
action.WorkingDirectory = ''  # directory that contains files that are used by the executable file.

# Set parameters for TaskDefinition.Settings  and TaskDefinition.RegistrationInfo
task_definition.RegistrationInfo.Author = 'guodong'
task_definition.RegistrationInfo.Date = datetime.datetime.now().isoformat()
task_definition.RegistrationInfo.Description = 'Python Test Task'
task_definition.Settings.Enabled = True
task_definition.Settings.StopIfGoingOnBatteries = False

# Register task
# If task already exists, it will be updated
# https://docs.microsoft.com/en-us/windows/win32/taskschd/taskfolder-registertaskdefinition
# The Task Scheduler either registers the task as a new task or as an updated version if the task already exists.
TASK_CREATE_OR_UPDATE = 6
TASK_LOGON_NONE = 0  # The logon method is not specified. Used for non-NT credentials.
root_folder.RegisterTaskDefinition(
    Path='Python Test Task',  # Task name
    pDefinition=task_definition,  # taskDefinition, The definition of the task that is registered.
    flags=TASK_CREATE_OR_UPDATE,
    UserId='',  # No user
    password='',  # No password
    LogonType=TASK_LOGON_NONE
)

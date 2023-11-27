import pandas as pd
from src.models.sql_helper import sql_helper
from datetime import datetime, timedelta, date
import uuid
from flask import flash, Flask, session
from email_notif import send_mail
# from flask import Flask, render_template, redirect, session, request
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

con = sql_helper()


class task_model:
    def __init__(self):
        pass

    def get_all_tasks(username):
        query = "SELECT *, Categories.Category_name, DATE(Startdate), DATE(Duedate) FROM Tasks JOIN Categories ON Tasks.Category= Categories.Category_ID WHERE UserID = " + \
            f"'{username}'" + ";"
        print(query)
        result = con.run_query(query)
        result = pd.DataFrame(list(result))
        return result.to_dict('records')

    def get_this_week_tasks(currUserName, current_date=None):
        if (current_date == None):
            current_date = date.today()
        dt = current_date
        start_date = dt - timedelta(days=dt.weekday())
        end_date = start_date + timedelta(days=6)
        query = "SELECT *, Categories.Category_name FROM Tasks JOIN Categories ON Tasks.Category= Categories.Category_ID WHERE (Startdate <='"+str(
            end_date)+"' AND Duedate >='"+str(start_date)+'\' AND UserID = '+"\'"+currUserName+'\')'
        result = con.run_query(query)
        result = pd.DataFrame(list(result))
        return result.to_dict('records')

    def get_todays_tasks(currUserName, current_date=None):
        if (current_date == None):
            current_date = date.today()
        dt = current_date
        start_date = dt - timedelta(days=dt.weekday())
        end_date = start_date + timedelta(hours=23)
        query = "SELECT *, Categories.Category_name FROM Tasks JOIN Categories ON Tasks.Category= Categories.Category_ID WHERE (Startdate <='"+str(
            end_date)+"' AND Duedate >='"+str(start_date)+'\' AND UserID = '+"\'"+currUserName+'\')'
        result = con.run_query(query)
        result = pd.DataFrame(list(result))
        return result.to_dict('records')

    def get_backlog(currUserName, current_date=None):
        if (current_date == None):
            current_date = date.today()
        dt = current_date
        start_date = dt - timedelta(days=dt.weekday())
        query = "SELECT  *, Categories.Category_name, DATE(Duedate) FROM Tasks JOIN Categories ON Tasks.Category= Categories.Category_ID WHERE Duedate <='"+str(
            start_date)+'\' and status <> "Done" AND UserID = '+"\'"+currUserName+"\'"
        result = con.run_query(query)
        result = pd.DataFrame(list(result))
        return result.to_dict('records')

    def get_future_tasks(currUserName, current_date=None):
        if (current_date == None):
            current_date = date.today()
        dt = current_date
        start_date = dt - timedelta(days=dt.weekday())
        end_date = start_date + timedelta(days=6)
        query = "SELECT  *, Categories.Category_name, DATE(Duedate) FROM Tasks JOIN Categories ON Tasks.Category= Categories.Category_ID WHERE Startdate >='"+str(
            end_date)+"' AND UserID = \'"+currUserName+"\'"
        result = con.run_query(query)
        result = pd.DataFrame(list(result))
        return result.to_dict('records')

    def create_tasks(self, data):
        print(data)
        columns = 'TaskID, '
        values = f'\'{uuid.uuid4()}\', '
        for key, value in data.items():
            columns += str(key)+', '
            values += "'"+str(value)+"', "

        query = "INSERT INTO Tasks (" + \
            columns[:-2]+" ) VALUES (" + values[:-2]+" );"
        print(query)
        con.run_query(query)
        return

    def create_subtasks(self, data):
        # print(data)
        # print(taskid)
        columns = 'sTaskID, '
        values = f'\'{uuid.uuid4()}\', '
        for key, value in data.items():
            if key == 'subtaskname[]':
                key = 'TaskName'
            columns += str(key)+', '
            values += "'"+str(value)+"', "

        query = "INSERT INTO Sub_tasks(" + \
            columns[:-2]+" ) VALUES (" + values[:-2]+" );"
        print(query)
        con.run_query(query)

        return

    def delete_task(self, taskid):
        querySub = f"SELECT * from Sub_tasks where TaskID = '{taskid}';"
        try:
            subTasks = con.run_query(querySub)
        except:
            print("ERROR in Subtasks")
            subTasks = ''
        currUserID= session["username"]
        user_email = con.run_query(
            f"SELECT EmailId from User where UserId = '{currUserID}';")
        you = user_email[0][0]
        print("THE CURRENT USER IS:", currUserID)
        print("THE CURRENT USER EMAIL IS:", user_email[0][0])
        if len(subTasks) > 0:
            ids = ""
            for i in subTasks:
                print(i[0])
                ids += f"'{i[0]}', "
            ids = ids[:-2]
            queryDel = f"DELETE from Sub_tasks where STaskID IN ({ids});"
            con.run_query(queryDel)
        query = "DELETE FROM Tasks WHERE Taskid ='" + taskid+"';"
        con.run_query(query)
        print("HEREEE")
        # SOF EMAIL #
        send_mail(you, 'Simplii: Task Deleted!', 'This is an automated email from Simplii to inform you that your task <strong>{}</strong> has been successfully deleted.', 'Name of the Task')

    def get_task_by_id(self, taskid):
        query = "SELECT * FROM tasks WHERE Taskid =" + taskid
        result = con.run_query(query)
        return result.to_dict('records')

    def get_user_by_id(self, userid):
        query = "SELECT * FROM user WHERE Userid =" + userid
        result = con.run_query(query)
        return result.to_dict('records')

    def update_task(self, task_id, data):
        values = ''
        for key, value in data.items():
            values += f"{key} = '{value}', "
        query = f"UPDATE Tasks SET {values[:-2]} WHERE TaskID = '{task_id}';"
        con.run_query(query)
        return

    def get_all_subtasks(self, taskid):
        query = f"SELECT * from Sub_tasks where TaskID = '{taskid}';"
        print(query)
        result = con.run_query(query)
        result = pd.DataFrame(list(result))
        return result.to_dict('records')

    def add_collaborator(self, email, task_name):
        subject = 'Simplii: New Task Alert'
        message = "You have been succesfully added as a collaborator on the following task:<br> <strong>{}</strong>"
        send_mail(email, subject, message, task_name)
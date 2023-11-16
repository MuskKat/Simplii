import pandas as pd
from src.models.sql_helper import sql_helper
from datetime import datetime, timedelta, date
import uuid
from flask import flash, Flask, session
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
        subTasks = con.run_query(querySub)
        currUserName = session["username"]
        user_email = con.run_query(
            f"select EmailId from user where user.UserId = '{currUserName}';")
        you = user_email[0][0]
        print("THE CURRENT USER IS:", currUserName)
        print("THE CURRENT USER EMIAL IS:", user_email[0][0])

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

        # SOF EMAIL #
        me = 'nitinjain0455@gmail.com'
        # you = 'muskyk32@gmail.com'
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'test file'
        msg['From'] = me
        msg['To'] = you

        text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
        html = """\
        <html>
        <head></head>
        <body>
            <p>Hi!<br>
            How are you?<br>
            Here is the <a href="http://www.python.org">link</a> you wanted.
            </p>
        </body>
        </html>
        """

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()

        mail.starttls()

        mail.login('nitinjain0455@gmail.com', 'swjq qzus winm tylx')
        mail.sendmail(me, you, msg.as_string())
        mail.quit()
        return
    # EOF #

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

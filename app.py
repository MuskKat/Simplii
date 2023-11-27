"""
Controller of the app
"""
from flask import Flask, render_template, redirect, session, request
# from flask_apscheduler import APScheduler, scheduler
# from apscheduler.schedulers.background import BackgroundScheduler
import notif_system as notification_system
from src.error_handler.error import handle_err
from src.models.task_model import task_model
from src.models.category_model import category_model
from src.controller.task_controller import tasks
from src.login.login import login

app = Flask(__name__)
app.register_blueprint(handle_err)
app.register_blueprint(tasks)
app.register_blueprint(login)
app.config.from_object(notification_system.Config())
app.config['SECRET_KEY'] = 'SECRET_KEY'

@app.route("/login")
def load_login():
    """This function renders the login page."""
    return render_template("login.html")

@app.route("/")
def home_page():
    """This function renders the home page."""
    current_user_name = None
    if "username" in session.keys():
        current_user_name = session["username"]
    if not current_user_name:
        return redirect("/login")
    this_week_tasks = task_model.get_this_week_tasks(current_user_name)
    backlog_tasks = task_model.get_backlog(current_user_name)
    future_tasks = task_model.get_future_tasks(current_user_name)
    categories = category_model.get_category()
    return render_template('home.html', this_week_tasks=this_week_tasks,
    backlog_tasks=backlog_tasks, future_tasks=future_tasks, categories= categories)

@app.route("/edit_task")
def edit_task():
    """This function renders the edit task page."""
    task_id = request.args.get('task_id')
    return render_template("edit_task.html",task_id = task_id)

@app.route("/view_all_tasks")
def view_all_tasks():
    """This function renders the edit task page."""
    current_user_name = session["username"]
    all_tasks = task_model.get_all_tasks(current_user_name)
    return render_template('view_all_tasks.html', all_tasks=all_tasks)

@app.route("/user_details")
def user_details():
    """This function renders the edit task page."""
    return render_template('view_user_details.html')

@app.route('/clear_session_variable')
def clear_session_variable():
    """This function logs the user out of the system"""
    session.pop('username', None)
    session.pop('email', None)
    session.pop('fullname', None)
    return "Session Cleared"


if __name__ == "__main__":
    #notification_system.scheduler.init_app(app)
    print("Hello")
    #notification_system.scheduler.add_job(
    # func=notification_system.send_test_alerts,
    # trigger="interval",
    # minutes=1)
    #notification_system.scheduler.start()
    app.run(debug=True)

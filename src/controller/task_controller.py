from flask import Blueprint, request, redirect
from src.models.task_model import task_model
from flask import render_template
from flask import flash

tasks = Blueprint('tasks', __name__, url_prefix='/tasks')
task = task_model()

def get_tasks():
    if 'period' not in request.form:
        return 'Need time period to fetch tasks!'
    if request.form['period'] == 'THIS WEEK':
        return task.get_this_week_tasks()
    if request.form['period'] == 'BACKLOG':
        return task.get_backlog()
    if request.form['period'] == 'FUTURE TASKS':
        return task.get_future_tasks()

@tasks.route('', methods=['POST'])
def create_task():
    data = request.form
    print ("data",data)
    task.create_tasks(data)
    return redirect('/')

@tasks.route('', methods=['GET'])
def delete_task():
    taskid = request.args.get('taskid')
    task.delete_task(taskid)
    return redirect('/')


@tasks.route('/update', methods=['POST'])
def update_task():
    task_id = request.form['taskid']
    data = request.form
    task.update_task(task_id, data)
    print(task_id)
    flash('User details have been successfully updated', 'success')
    return redirect('/')

@tasks.route('/sub', methods=['POST'])
def create_subtask():
    data = request.form
    # taskid = request.args.get('taskid')
    print(data)
    independent_dicts = []
    for key, value in data.items():
        print(key)
        if key == 'subtaskname[]':
            key = 'TaskName'
        independent_dicts.append({key: value})
    
    print(independent_dicts)
    task.create_subtasks(data)
    return redirect('/')


@tasks.route('/edit_task', methods=['GET', 'POST'])
def edit_task():
    existing_data = None

    if request.method == 'POST':
        task_id = request.form.get('taskid')
        if not task_id:
            task_id = request.args.get('taskid')
        existing_data = task.get_task_by_id(task_id)

    return render_template('edit_task.html', existing_data=existing_data)

@tasks.route('/get_subtasks',methods=['GET'])
def get_subtasks():
    existing_data = None
    task_id = request.args.get('task_id')
    existing_data = task.get_all_subtasks(task_id)
    return render_template('tasks/view_subtasks.html', existing_data=existing_data)

@tasks.route('/add_collaborator', methods=['POST'])
def add_collaborator():
    email = request.form['email']
    try:
        task.add_collaborator(email, 'You have been added to a task!')
        flash('User has been succesfully emailed', 'success')
    except:
        flash('Could not send email to the user, try again later!', 'failure')
    return redirect('/view_all_tasks')
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for
from flask.ext.mongokit import MongoKit, Document, Connection 
import os

app = Flask(__name__)

class Task(Document):
    __collection__ = 'tasks'
    structure = {
        'title': unicode,
        'text': unicode,
        'creation': datetime,
    }
    required_fields = ['title', 'creation']
    default_values = {'creation': datetime.utcnow()}
    use_dot_notation = True

db = MongoKit(app)
connection = Connection(os.environ['MONGODB_URL']) 
db.register([Task])


@app.route('/')
def show_all():
   try: 
     tasks = db.Task.find()
     return render_template('list.html', tasks=tasks)
   except Exception, e: 
     d = {} 
     d['Error'] = e.message  
     d['URL'] = os.environ['MONGODB_URL']
     return render_template('page_not_found.html',d=d) 

""" 
@app.route('/<ObjectId:task_id>')
def show_task(task_id):
    task = db.Task.get_from_id(task_id)
    return render_template('task.html', task=task)

@app.route('/new', methods=["GET", "POST"])
def new_task():
    if request.method == 'POST':
        try: 
          task = db.Task()
          asdf
        except Exception, e: 
          error = {} 
          error['error'] = e.message
          render_template('except.html', error = error) 
        try:
          task.title = request.form['title']
          task.text = request.form['text']
        except Exception, e:
          error = {} 
          error['error'] = e.message
          render_template('except.html', error = error)
        try:
          task.save()
        except Exception, e:
          error = {} 
          error['error'] = e.message
          render_template('except.html', error = error)
        try: 
           return redirect(url_for('show_all'))
        except Exception, e:
          error = {} 
          error['error'] = e.message
          render_template('except.html', error = error)
        
    return render_template('new.html')

@app.route('/')
def show_all():
    d = {} 
    d['MONGODB_URL'] = os.environ.get('MONGODB_URL')
    #for item in os.environ: 
    #   d[item] = os.environ[item] 

    return render_template('hello.html', tasks = d)
"""

if __name__ == '__main__':
    app.run(debug=True)

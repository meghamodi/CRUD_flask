from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///test.db'
db = SQLAlchemy(app)

# table name should be singular Tasks >> task
# user table
class Task(db.Model):
    # id is always taken as primary key by default, so need to metion arguments
    id = db.Column(db.Integer,primary_key=True)
    # no column should be same as table name task>>name/title
    title = db.Column(db.String(80),nullable=False)
    date_created = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        #Tasks >> task
        return '<Task %r>' % self.title


@app.route('/', methods=['GET','POST'])

def index():
    if request.method == "POST":
        form_title = request.form['title']
        # kwargs --> form_title  assigned to table column name
        # left side is object and right side is value assigned
        new_task = Task(title=form_title)
# kwargs
# args
# def subtract(a,b):
#     return a-b
# a=3
# b=4
# subtract(3,4)# a,b -1
# sum(b=a,a=b)
        try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
        except:
            return "There was a problem adding new task."

    else:
        tasks = Task.query.all()
        # asdaf is used in index.html for iterating/getting elements

        return render_template('index.html', asdaf=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    new_task = Task.query.get_or_404(id)

    try:
        db.session.delete(new_task)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting data."

@app.route('/update/<id>', methods=['GET','POST'])
def update(id):
    # id is always taken as the first column so no need of kwargs
    new_task = Task.query.get_or_404(id)
    if request.method=="POST":
        new_task.title = request.form['title']
        # db.session.commit()
        # print(task)

        try:
            db.session.commit()
            print("hey")
            return redirect('/')
        except:
            return "There was a problem updating data."

    else:
        header = "Update Data"
        return render_template('update.html', header=header, task=new_task)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)

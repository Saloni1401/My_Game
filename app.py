from flask import Flask, render_template ,redirect
from flask.globals import request
from datetime import datetime
# flask sqlalchemy is used 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
#mysql db
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False


db= SQLAlchemy(app)

#class for database having filelds like integer, strings
#db i imported by python
class Mygame(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    game=db.Column(db.String(100),nullable=False)
    desc=db.Column(db.String(400),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.game}"


@app.route("/",methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        game=request.form["game"]
        desc=request.form["desc"]
        todo=Mygame(game=game,desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=Mygame.query.all()
    print(alltodo)
    #using jinja2 for templating
    return render_template('index.html',alltodo=alltodo)
    #return "<p>My Website!</p>"

@app.route("/show")
def games():
    alltodo=Mygame.query.all()
    print(alltodo)
    return "This is page"

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=="POST":
        game=request.form["game"]
        desc=request.form["desc"]
        todo=Mygame.query.filter_by(sno=sno).first()
        todo.game=game
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=Mygame.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Mygame.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True,port=8000)

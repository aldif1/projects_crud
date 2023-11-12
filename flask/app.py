from flask import Flask, redirect,render_template
from flask import url_for
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

import ssl
context = ssl.PROTOCOL_TLSv1_2

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myflask.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize the app with the extension
db.init_app(app)

db.Model
db.session

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String)
    #nama = db.Column(db.String(100))
    #umur = db.Column(db.Integer)
    #alamat = db.Column(db.TEXT)
    #notelepon = db.Column(db.Integer)

with app.app_context():
    db.create_all()


################################################################

@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("user/tampil.html", users=users)
@app.route("/newuser")
def new_user():
    nama = "Satrio Aldi Firmansyah"
    return render_template("user/newuser.html",nama=nama)
@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("/user/index.html")

@app.route("/")
def index():
    return f'''<a href="/home">Go To Home</a>
                <br> 
                http://127.0.0.1:5000/home
                <br>
                <a href="/newuser">Halaman User</a>
                <br> 
                http://127.0.0.1:5000/Satrio_Aldi_Firmansyah
                <br>
                <a href="/data">MyData</a>
                <br> 
                http://127.0.0.1:5000/mydata
                <br>
                <a href="/hello/SatrioAldi">Halaman Tempelate</a>
                <br> 
                <img src="{ url_for('static', filename='monalisa.jpg')}" with="50%"> Monalisa
                <br>
                <img src="{ url_for('static', filename='') }" alt="https://brainly.co.id/tugas/27388479"  >
                <br>
                http://127.0.0.1:5000/hello/satrio
                <br>


                
                '''

@app.route('/home')
def home():
    return 'This is My Home'
           


@app.route('/data')
def data():
    return 'Nama : Satrio Aldi Firmansyah'
            

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('user.html', name=name)

@app.route('/login')
def show_the_login_form():
    return render_template('login.html')

@app.route('/loginput')
def showPut():
    return 'data berhasil  diubah'



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return index()
    else:
        return show_the_login_form()
    

@app.route("/users/<int:id>")
def tampil_user(id):
    userr = db.get_or_404(User,id)
    return render_template("update.html",user=userr)

    
@app.route("/users/update/<int:id>", methods=["POST"])
def update_user(id):
    username=request.form["username"]
    email=request.form["email"]

    user=User.query.get(id)

    user.username=username
    user.email=email

    db.session.add(user)
    db.session.commit()

    return redirect(url_for("user_list"))


@app.route("/users/delete/<int:id>",methods=["DELETE"])
def delete_user(id):
    userr = db.get_or_404(User,id)

    db.session.delete(userr)
    db.session.commit()

    return redirect(url_for("user_list"))



#http://127.0.0.1:5000/users
if __name__ == '__main__':
    app.run(ssl_context='adhoc',host="0.0.0.0",debug=True, port=5000)







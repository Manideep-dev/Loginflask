import sqlalchemy
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
# internal db
# app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://mani:mani76922@@localhost/dbb'
# engine = sqlalchemy.create_engine('mysql+mysqlconnector://mani:mani76922@@localhost/dbb')  # connect to server
# engine.execute("CREATE DATABASE IF NOT EXISTS dbb")  # create db
# engine.execute("USE dbb")
# freemysql expired db
# app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
# app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://sql12374717:XIDKAckd2g@sql12.freemysqlhosting.net:3306/sql12374717'
# engine = sqlalchemy.create_engine('mysql+pymysql://sql12374717:XIDKAckd2g@sql12.freemysqlhosting.net:3306/sql12374717')  # connect to server
# engine.execute("CREATE DATABASE IF NOT EXISTS sql12374717")  # create db
# engine.execute("USE sql12374717")
# freemysqldb.com
# app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://id15531596_manideep:Mani76922@$-@localhost:3306/id15531596_dbb'
# engine = sqlalchemy.create_engine(
#     'mysql+pymysql://id15531596_manideep:Mani76922@$-@localhost:3306/id15531596_dbb')  # connect to server
# engine.execute("CREATE DATABASE IF NOT EXISTS id15531596_dbb")  # create db
# engine.execute("USE id15531596_dbb")
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://sql12378985:VAKf3yzUKz@sql12.freemysqlhosting.net:3306/sql12378985'
engine = sqlalchemy.create_engine('mysql+pymysql://sql12378985:VAKf3yzUKz@sql12.freemysqlhosting.net:3306/sql12378985')  # connect to server
engine.execute("CREATE DATABASE IF NOT EXISTS sql12378985")  # create db
engine.execute("USE sql12378985")
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, email, password):
        # self.User = [User]
        self.username = [username]
        self.email = [email]
        self.password = password


class Table(db.Model):
    __tablename__ = 'Table'
    # ref = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False)
    Phoneno = db.Column(db.String(20), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    Notes = db.Column(db.String(100), nullable=False)
    Address = db.Column(db.String(100), nullable=False)
    City = db.Column(db.String(100), nullable=False)
    IssueType = db.Column(db.String(100), nullable=False)
    ticketId = db.Column(db.String(20), nullable=False)

    # def __init__(self, ref, Name, Phoneno, Email, Notes, City, Address, IssueType, ticketId):
    def __init__(self, Name, Phoneno, Email, Notes, City, Address, IssueType, ticketId):
        # self.ref = ref
        self.Name = Name
        self.Phoneno = Phoneno
        self.Email = Email
        self.Notes = Notes
        self.Address = Address
        self.City = City
        self.IssueType = IssueType
        self.ticketId = ticketId


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    # my_data = [r.username  for r in User.query.with_entities(User.username).all()
    #            ]
    my_data = User.query.all()
    print(my_data)
    print(type(my_data))
    return render_template('dashboard.html', name=current_user.username, my_data=my_data)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/delete/<id>/')
def delete(id):
    my_data = User.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
    return redirect(url_for('dashboard'))


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        print(request.form.get('id'))
        my_data = User.query.get(request.form.get('id'))
        print('%%%%%%%%')
        print(my_data)
        my_data.username = request.form['name']
        my_data.email = request.form['email']
        db.session.commit()
        print(my_data.username)
        flash("Employee Updated Successfully")

    return redirect(url_for('dashboard'))


@app.route('/insert', methods=['POST', 'GET'])
def insert(refid=1000):
    if request.method == 'POST':
        print('rrr')
        # ref = request.form.get('ref')
        Name = request.form['Name']
        print(Name)
        Phoneno = request.form.get('Phone no')
        Email = request.form.get('Email')
        Notes = request.form.get('Notes')
        Address = request.form.get('Address')
        City = request.form.get('City')
        IssueType = request.form.get('Issue Type')
        print(type)
        # ticketId = request.form.get('ticketId')
        # print(type(ticketId))
        # data = [r.ref for r in Table.query.with_entities(Table.ref).all()]
        tdata = [r.ticketId for r in Table.query.with_entities(Table.ticketId).all()]

        print(tdata)
        print(type(tdata))
        # print(data)

        if not tdata:
            refid = 1000
            if IssueType == 'Internet':
                ticketId = 'IO-' + str(refid)
            else:
                ticketId = 'CO-' + str(refid)
        else:
            if IssueType == 'Internet':
                substring = "IO-"

                strings_with_substring = [string for string in tdata if substring in string]
                print(strings_with_substring)
                if not strings_with_substring:
                    print("yess there is no IO")
                    ticketId = 'IO-' + str(refid)
                    ref = refid
                else:
                    a = list(map(lambda x: x.replace('IO-', '').replace('', ''), strings_with_substring))
                    print(a)
                    a = list(map(int, a))
                    print(a)
                    a = max(a) + 1
                    print(a)
                    ticketId = 'IO-' + str(a)
                    ref = a
            else:
                substring = "CO-"

                strings_with_substring = [string for string in tdata if substring in string]
                print(strings_with_substring)
                if not strings_with_substring:
                    print("yess there is no CO")
                    ticketId = 'CO-' + str(refid)
                    ref = refid
                else:
                    a = list(map(lambda x: x.replace('CO-', '').replace('', ''), strings_with_substring))
                    print(a)
                    a = list(map(int, a))
                    print(a)
                    a = max(a) + 1
                    print(a)
                    ticketId = 'CO-' + str(a)
                    ref = a

        exists = db.session.query(Table).filter_by(Name=Name, Email=Email, IssueType=IssueType).scalar() is not None
        if exists:
            d = Table.query.filter_by(Name=Name, Email=Email, IssueType=IssueType).first().ticketId
            print(d)
            print('user already exists')
            return d
        else:
            my_dta = Table(Name, Phoneno, Email, Notes, City, Address, IssueType, ticketId)
            db.session.add(my_dta)
            db.session.commit()
            print('add to database')

        print('inserted')

    else:
        print('failed')
    geticket = Table.query.filter_by(Name=Name, Email=Email, IssueType=IssueType).first().ticketId
    print(geticket)

    return 'Your ticket id is:' + geticket


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

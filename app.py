from flask import Flask, render_template, redirect, session, flash 
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm,LoginForm,FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///hashing_users"
app.config['SQLALCHEMY_TRACK_MODIFICATINOS'] = False
app.config['SQLALCHEMY_ECHO'] = True 
app.config['SECRET_KEY'] = 'this_is_a_secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.debug = True
toolbar = DebugToolbarExtension(app)


connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def homepage():
    return redirect ('/register')

@app.route('/register', methods=['GET','POST'])
def register_user():
    """register user: produce form and handle form submission."""
    form = RegisterForm()
    # form.is_admin.choices = [('True','True'),('False','False')]
    # form.is_admin.default = 'False'
    # form.process()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data 
        email = form.email.data 
        first_name = form.first_name.data 
        last_name = form.last_name.data 
        # is_admin = form.is_admin.data

        new_user = User.register(username,password,email,first_name,last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            # raise
            form.username.errors=('Username taken, please pick another one')
            # form.email.errors=('Email taken, please pick another one')
            return render_template ('registration_form.html',form=form)
        session['username']=new_user.username
        flash("Successfully create your account!")
        return redirect(f'/users/{username}')
    return render_template ('registration_form.html', form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        u = User.authenticate(username, password)
        if u:
            session['username'] = u.username
            return redirect(f'/users/{u.username}')
        else:
            flash('Incorrect username or password, please try again')
            return redirect('/login')
    return render_template('login.html',form=form)

@app.route('/users/<username>')
def secret_page(username):
    user = User.query.filter_by(username=username).first()
    
    if 'username' not in session:
        flash('You must be logged in to view')
        return redirect('/')
    elif session['username'] == username:
        
        return render_template('user_info.html', user=user)
    else:
        flash('You are not allowed to view this info.')
        return redirect('/')

@app.route('/logout')
def logout():
    """logs user out and redirect to homepage"""
    session.pop("username")
    return redirect('/')

@app.route('/users/<username>/delete',methods=['POST'])
def delete_user(username):
    
    if 'username' not in session:
        flash('Please log in to operate')
        return redirect('/')
    elif session['username'] == username:
        user = User.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()
        return redirect('/logout')
    else:
        flash('This is not your account')
        cur_user = session['username']
        return redirect(f'/users/{cur_user}')

@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    form = FeedbackForm()
    
    if 'username' not in session:
        flash('You must be logged in to view')
        return redirect('/')

    elif session['username'] == username:

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            new_feedback = Feedback(title=title,content=content,username=username)
            db.session.add(new_feedback)
            db.session.commit()
            return redirect(f'/users/{username}')
        else:
            return render_template('feedback.html',form=form)
    else:
        f('This is not your account')
        cur_user = session['username']
        return redirect(f'/users/{cur_user}')

@app.route('/feedback/<int:feedback_id>/update', methods=['GET','POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)

    if 'username' not in session:
       flash('You must be logged in to view')
       return redirect('/')
    elif session['username'] == feedback.username:
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
    
            db.session.commit()
            return redirect(f'/users/{feedback.username}')
        else:
            return render_template('feedback.html',form=form)

    else:
        flash('You are not allowed to edit this account')
        cur_user = session['username']
        return redirect(f'/users/{cur_user}')

@app.route('/feedback/<int:feedback_id>/delete',methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.username
    
    if 'username' not in session:
        flash('You must be logged in to view')
        return redirect('/')
    elif session['username'] == username:
        Feedback.query.filter_by(id=feedback_id).delete()
        db.session.commit()
        return redirect(f'/users/{username}')
    else:
        flash('This is not your account')
        cur_user = session['username']
        return redirect(f'users/{cur_user}')

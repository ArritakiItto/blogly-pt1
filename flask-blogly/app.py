from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SECRET_KEY'

# db.init_app(app)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()
    
@app.route('/')
def root():
    """Shows home page"""
    return redirect("/users")

##################################################################### USER ROUTE ###########################################################
@app.route('/users')
def users_index():
    """Show all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Show new user form"""

    return render_template('users/new.html')

@app.route('/users/new', methods=["POST"])
def users_new():
    """Handle new user form"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user details"""

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_edit(user_id):
    """Handle form submission for updating an existing user"""
      
      user = User.query.get_or_404(user_id)
      user.first_name = request.form['first_name']
      user.last_name = request.form['last_name']
      user.image_url = request.form['image_url'] or None
  
      db.session.add(user)
      db.session.commit()
  
      return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

if __name__ == '__main__':
    app.run(debug=True)
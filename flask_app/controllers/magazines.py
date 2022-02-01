from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.magazine import Magazine
from flask_app.models.user import User

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }

    user = User.get_by_id(data)
    magazines = Magazine.show_all_magazines_and_users()
    subscribed = Magazine.get_all_subscribed_magazines(data)

    return render_template("dashboard.html",user=user,magazines=magazines, subscribed = subscribed)


@app.route('/new')
def new():
    if 'user_id' not in session:
        return redirect('/logout')
    
    return render_template ("new.html")


@app.route('/new_magazine/', methods=['POST'])
def new_magazine():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Magazine.validate_magazine(request.form):
        return redirect('/new')

    data = {
        "title": request.form['title'],
        "description": request.form['description'],
        "user_id": session['user_id']
    }
    Magazine.create_magazine(data)
    return redirect('/dashboard')


@app.route('/show/<int:id>')
def show_magazine(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }

    one_magazine = Magazine.get_one_magazine_and_one_user(data)

    subscribers = Magazine.get_all_subscribers_of_one_magazine(data)

    return render_template("show.html", one_magazine = one_magazine, subscribers = subscribers)


@app.route('/user/account/<int:id>')
def edit_one(id):
    if 'user_id' not in session:
        return redirect('/logout')

    user_data = {
        "id": id
    }

    user= User.get_by_id(user_data)

    all_magazines = Magazine.get_magazines_of_user(user_data)

    return render_template("edit.html", all_magazines = all_magazines, user = user)


@app.route('/update/user/<int:id>',methods=['POST'])
def update_user(id):
    if not User.validate_user(request.form):
        return redirect(f'/user/account/{id}')
    
    user_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "id": id
    }

    User.update_user(user_data)
    
    return redirect('/dashboard')


@app.route('/delete/<int:id>')
def delete_one(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        "id":id
    }
    Magazine.destroy_magazine(data)

    return redirect('/dashboard')


@app.route('/subscribe/<int:id>')
def user_subscribe(id):
    data = {
        "user_id": session['user_id'],
        "magazine_id": id
    }

    Magazine.subscribe_to_magazine(data)

    return redirect('/dashboard')


@app.route('/unsubscribe/<int:id>')
def user_unsubscribe(id):
    data = {
        "user_id": session['user_id'],
        "magazine_id": id
    }
    Magazine.remove_subscribe_from_magazine(data)

    return redirect('/dashboard')

from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.user import User
from flask_app.models.chore import Chore

@app.route('/new_chore')
def new_chore():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
        }
    user = User.find_id(data)
    return render_template('new_chore.html', user=user)

@app.route('/add_chore', methods=['POST'])
def add_chore():
    if "user_id" not in session:
        return redirect('/')
    if not Chore.validate_chore(request.form):
        return redirect('/new_chore')
    data = {
        'title' : request.form['title'],
        'description': request.form['description'],
        'location': request.form['location'],
        'user_id': session['user_id']
    }
    Chore.add_chore(data)
    return redirect('/dashboard')

@app.route("/view/<int:chore_id>")
def view_chore(chore_id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
        }
    data2 = {
        "id": chore_id
    }
    user = User.find_id(data)
    chore = Chore.view_chore(data2)
    return render_template("view_chore.html", user=user, chore=chore)

@app.route('/edit/<int:chore_id>')
def edit(chore_id):
    if "user_id" in session:
        data = {
            "id": chore_id
        }
        chore = Chore.view_chore(data)
        return render_template("edit_chore.html", chore=chore)
    return redirect("/")

@app.route('/edit_chore/<int:chore_id>', methods=['POST'])
def edit_chore(chore_id):
    if "user_id" not in session:
        return redirect('/')
    if not Chore.validate_chore(request.form):
        return redirect(f'/edit/{chore_id}')
    data = {
        'id' : chore_id,
        'title' : request.form['title'],
        'description': request.form['description'],
        'location': request.form['location'],
        'user_id': session['user_id']
    }
    Chore.update_chore(data)
    return redirect('/dashboard')

@app.route('/delete/<int:chore_id>')
def delete_chore(chore_id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id': chore_id
        }
    Chore.delete_chore(data)
    return redirect('/dashboard')
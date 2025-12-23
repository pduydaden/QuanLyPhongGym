from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
from flask_login import login_user, current_user, logout_user, login_required

from quanlyphonggym import dao, app, login, admin


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['get', 'post'])
def login_my_user():

    if current_user.is_authenticated:
        return redirect("/")

    err_msg = None

    if request.method.__eq__('POST'):
        email=request.form.get("email")
        pswd=request.form.get("pswd")

        user = dao.auth_user(email,pswd)

        if user:
            login_user(user)
            return redirect("/")
        else:
            err_msg="tai khoan hoac mat khau khong dung"

    return render_template("login.html", err_msg=err_msg)

@app.route("/logout")
def logout_my_user():
    logout_user()
    return redirect("/")

@login.user_loader
def load_user(id):
    return dao.get_user_by_id(id)

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['get', 'post'])
def login():
    err_msg = None
    if request.method.__eq__('POST'):
        email=request.form.get("email")
        pswd=request.form.get("pswd")

        if email=="user@gmail.com" and pswd=="123":
            return redirect("/")
        else:
            err_msg="tai khoan hoac mat khau khong dung"

    return render_template("login.html", err_msg=err_msg)

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
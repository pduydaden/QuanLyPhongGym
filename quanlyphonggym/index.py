import hashlib

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required

from quanlyphonggym import dao, app, login, admin, db
from models import User, HoaDon, GoiTap, UserRole


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

            if user.role == UserRole.HLV:
                return redirect("/hlv")
            elif user.role == UserRole.TN:
                return redirect("/tn")
            elif user.role == UserRole.LT:
                return redirect("/lt")
            elif user.role == UserRole.ADMIN:
                return redirect("/admin")
            elif user.role == UserRole.USER:
                return redirect("/")

        else:
            err_msg="tai khoan hoac mat khau khong dung"

    return render_template("login.html", err_msg=err_msg)

@app.route("/hlv")
@login_required
def hlv_dashboard():
    return render_template("hlv.html")

@app.route("/lt")
@login_required
def letan_dashboard():
    return render_template("letan.html")

@app.route("/tn")
@login_required
def thungan_dashboard():
    return render_template("thungan.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup_my_user():
    err_msg = None

    goitaps = GoiTap.query.filter_by(active=True).all()

    if request.method == 'POST':
        name = request.form.get('name')
        gioitinh = request.form.get('gioitinh')
        sdt = request.form.get('sdt')
        email = request.form.get('email')
        pswd = request.form.get('pswd')
        goitap_id = request.form.get('goitap')

        if name and gioitinh and sdt and email and pswd and goitap_id:
            pswd_hash = hashlib.md5(pswd.encode('utf-8')).hexdigest()

            try:
                user = User(
                    name=name,
                    gioitinh=gioitinh,
                    sdt=sdt,
                    email=email,
                    pswd=pswd_hash,
                    goitap_id=int(goitap_id)
                )
                db.session.add(user)
                db.session.commit()

                goitap = GoiTap.query.get(int(goitap_id))

                if not goitap:
                    err_msg = "Gói tập không tồn tại!"
                else:
                    hoadon = HoaDon(
                        name=f"Hóa đơn của {user.name}",
                        tongtien=goitap.giagoitap,
                        user_id=user.id
                    )
                    db.session.add(hoadon)
                    db.session.commit()

                    return redirect(url_for('index'))

            except Exception as ex:
                db.session.rollback()
                err_msg = "Email đã tồn tại hoặc lỗi hệ thống!"
                print(ex)
        else:
            err_msg = "Vui lòng nhập đầy đủ thông tin!"

    return render_template("signup.html", goitaps=goitaps, err_msg=err_msg)

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
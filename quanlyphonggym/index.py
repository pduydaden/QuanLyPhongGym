import hashlib

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required

from quanlyphonggym import dao, app, login, admin, db
from models import User, HoaDon, GoiTap, UserRole, BaiTap, KeHoachTap
from quanlyphonggym.dao import get_users_by_hlv


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

@app.route("/hlv", methods=['GET', 'POST'])
@login_required
def hlv_dashboard():
    search = request.args.get('search', '')

    # POST: thêm hoặc xóa kế hoạch
    if request.method == 'POST':
        # Thêm kế hoạch
        plan_name = request.form.get('plan_name')
        user_id = request.form.get('user_id')
        baitap_ids = request.form.getlist('add_baitap_id')

        if plan_name:
            plan = KeHoachTap(name=plan_name, hlv_id=current_user.id)
            if user_id:
                plan.user_id = int(user_id)
            db.session.add(plan)
            db.session.commit()

            # Gắn bài tập
            for bt_id in baitap_ids:
                bt = BaiTap.query.get(int(bt_id))
                if bt:
                    plan.baitaps.append(bt)
            db.session.commit()
            flash("Tạo kế hoạch thành công!", "success")
            return redirect(url_for('hlv_dashboard'))

        # Xóa kế hoạch
        delete_plan_id = request.form.get('delete_plan_id')
        if delete_plan_id:
            plan = KeHoachTap.query.get(int(delete_plan_id))
            if plan:
                db.session.delete(plan)
                db.session.commit()
                flash("Xóa kế hoạch thành công!", "success")
            return redirect(url_for('hlv_dashboard'))

    # GET: load dữ liệu
    query = KeHoachTap.query.filter_by(hlv_id=current_user.id)
    if search:
        query = query.filter(KeHoachTap.name.ilike(f"%{search}%"))
    plans = query.order_by(KeHoachTap.id.asc()).all()  # ID từ 1 → hết

    all_baitap = BaiTap.query.all()
    all_users = User.query.filter_by(hlv_id=current_user.id).all()

    return render_template("hlv.html", plans=plans, all_baitap=all_baitap,
                           all_users=all_users, search=search)



@app.route("/hlv/<int:plan_id>", methods=['GET', 'POST'])
@login_required
def hlv_detail(plan_id):
    plan = dao.get_plan(plan_id)
    all_baitap = dao.get_all_baitap()
    all_users = dao.get_users_by_hlv(current_user.id)

    if request.method == 'POST':
        # Cập nhật học viên
        user_id = request.form.get('user_id')
        plan.user_id = int(user_id) if user_id and user_id != 'none' else None

        # Thêm bài tập
        add_baitap_ids = request.form.getlist('add_baitap_ids')
        for bt_id in add_baitap_ids:
            bt = BaiTap.query.get(int(bt_id))
            if bt and bt not in plan.baitaps:
                plan.baitaps.append(bt)

        # Xóa bài tập
        remove_baitap_ids = request.form.getlist('remove_baitap_ids')
        for bt_id in remove_baitap_ids:
            bt = BaiTap.query.get(int(bt_id))
            if bt and bt in plan.baitaps:
                plan.baitaps.remove(bt)

        db.session.commit()
        flash("Cập nhật kế hoạch thành công!", "success")
        return redirect(url_for('hlv_detail', plan_id=plan.id))

    return render_template("hlv_detail.html", plan=plan, all_baitap=all_baitap, all_users=all_users)

@app.route("/goitap", methods=['GET', 'POST'])
def goitap_dashboard():
    return render_template("goitap.html")

@app.route("/baitap", methods=['GET', 'POST'])
def baitap_dashboard():
    return render_template("baitap.html")

@app.route("/quydinh", methods=['GET', 'POST'])
def quydinh_dashboard():
    return render_template("quydinh.html")

@app.route("/tn", methods=['GET', 'POST'])
@login_required
def thungan_dashboard():
    if request.method == 'POST':
        hoadons = dao.get_all_hoadon()
        from datetime import datetime

        for hd in hoadons:
            hd.trangthai = f"trangthai_{hd.id}" in request.form
            hd.ngaythanhtoan = datetime.now() if hd.trangthai else None

        db.session.commit()
        flash("Cập nhật trạng thái hóa đơn thành công!", "success")
        return redirect(url_for('thungan_dashboard'))

    hoadons = dao.get_all_hoadon()
    return render_template("thungan.html", hoadons=hoadons)


@app.route("/lt", methods=['POST', 'GET'])
@login_required
def letan_dashboard():
    if request.method == 'POST':
        users = User.query.filter(User.role != UserRole.HLV).all()
        for user in users:
            hlv_id = request.form.get(f"hlv_{user.id}")
            if hlv_id:
                if hlv_id == 'none':
                    user.hlv = None
                else:
                    hlv = User.query.get(int(hlv_id))
                    if hlv:
                        user.hlv = hlv
        db.session.commit()
        flash("Cập nhật HLV cho các học viên thành công!", "success")
        return redirect(url_for('letan_dashboard'))

    # GET
    search = request.args.get('search')
    status = request.args.get('status')
    users = dao.get_users_by_hlv_status(status, search)
    hlvs = dao.get_all_hlv()

    return render_template("letan.html", users=users, hlvs=hlvs, search=search, status=status)


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
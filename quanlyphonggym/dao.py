import json
from models import User, GoiTap, UserRole, HoaDon, BaiTap, KeHoachTap
from quanlyphonggym import app, db
import hashlib


def get_user_by_id(user_id):
    return User.query.get(int(user_id))

def get_users_by_hlv_status(status=None, search=None):
    query = User.query.filter(User.role == UserRole.USER)  # chỉ lấy học viên

    if status == 'no':
        query = query.filter(User.hlv_id == None)
    elif status == 'yes':
        query = query.filter(User.hlv_id != None)

    if search:
        search_term = f"%{search}%"
        query = query.filter((User.name.ilike(search_term)) | (User.email.ilike(search_term)))

    return query.order_by(User.id).all()


def get_all_hlv():
    return User.query.filter(User.role == UserRole.HLV).all()

def get_all_hoadon():
    return HoaDon.query.all()

def get_all_baitap():
    return BaiTap.query.all()

def search_baitap_by_name(keyword):
    if keyword:
        return BaiTap.query.filter(BaiTap.name.ilike(f"%{keyword}%")).all()
    return BaiTap.query.all()

def get_kehoachtap_by_hlv(hlv_id):
    return KeHoachTap.query.join(User).filter(User.hlv_id==hlv_id).all()

def get_users_by_hlv(hlv_id):
    return User.query.filter(User.hlv_id==hlv_id).all()

def auth_user(email, pswd):
    pswd = hashlib.md5(pswd.encode("utf-8")).hexdigest()
    return User.query.filter(User.email.__eq__(email), User.pswd.__eq__(pswd)).first()

def get_plan(plan_id):
    """Lấy 1 kế hoạch theo id"""
    return KeHoachTap.query.get(plan_id)


def get_users_by_hlv(hlv_id):
    """Lấy tất cả học viên do HLV quản lý"""
    return User.query.filter(User.hlv_id == hlv_id).all()

def get_all_users():
    """Lấy tất cả user có role USER"""
    return User.query.filter_by(role=UserRole.USER).all()

if __name__ == '__main__':
    with app.app_context():
        print(auth_user(email="u1@gmail.com", pswd="123"))
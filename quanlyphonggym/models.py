import json

from quanlyphonggym import db, app
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as RoleEnum
from flask_login import UserMixin


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    active = Column(Boolean, default=True)
    create_time = Column(DateTime, default=datetime.now())

class UserRole(RoleEnum):
    USER = 1
    LT = 2
    TN = 3
    HLV = 4
    ADMIN = 5

class GoiTap(Base):
    giagoitap = Column(Integer, nullable=False)
    nguoidung =relationship('User',lazy=True, back_populates='goitap')

class User(Base, UserMixin):
    gioitinh = Column(String(50), nullable=False)
    sdt = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    pswd = Column(String(50), nullable=False)
    avatar = Column(String(300), default="https://png.pngtree.com/png-vector/20220709/ourmid/pngtree-businessman-user-avatar-wearing-suit-with-red-tie-png-image_5809521.png")
    goitap_id = Column(Integer, ForeignKey(GoiTap.id),nullable=False)
    hlv_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    hoadons = relationship('HoaDon', lazy=True, back_populates='user')
    goitap = relationship('GoiTap', lazy=True, back_populates='nguoidung', overlaps="nguoidung")
    hlv = relationship('User', remote_side='User.id', lazy=True)

class BaiTap(Base):
    __tablename__ = 'baitap'
    mota = Column(String(500), nullable=True)
    avatar = Column(String(300))
    nhomco = Column(String(50), nullable=False)

class KeHoach_BaiTap(db.Model):
    __tablename__ = 'kehoachtap_baitap'
    kehoachtap_id = Column(Integer, ForeignKey('kehoachtap.id'), primary_key=True)
    baitap_id = Column(Integer, ForeignKey('baitap.id'), primary_key=True)
    solan = Column(Integer, nullable=False)

    baitap = relationship("BaiTap")


class KeHoachTap(Base):
    __tablename__ = 'kehoachtap'
    hlv_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    user = relationship('User', foreign_keys=[user_id], lazy=True)
    hlv = relationship('User', foreign_keys=[hlv_id], lazy=True)
    baitaps = relationship('KeHoach_BaiTap', backref='kehoach', lazy=True)


class HoaDon(Base):
    tongtien = Column(Integer, nullable=False)
    trangthai = Column(Boolean, default=False)
    ngaythanhtoan  = Column(DateTime,default= None)
    user_id = Column(Integer, ForeignKey(User.id),nullable=False)
    user = relationship('User', back_populates='hoadons', lazy=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        g1=GoiTap(name='1 thang',giagoitap=90000)
        g2 = GoiTap(name='2 thang', giagoitap=190000)
        g3 = GoiTap(name='12 thang', giagoitap=1190000)
        db.session.add_all([g1, g2, g3])

        import hashlib
        pswd = hashlib.md5("123".encode("utf-8")).hexdigest()
        u1 = User(name="Nguyen Van A", gioitinh="Nam", sdt="0973655534", email="u1", pswd=pswd,goitap_id=1)
        u2 = User(name="HVL", gioitinh="Nam", sdt="0384614424", email="hlv", pswd=pswd,goitap_id=1, role=UserRole.HLV)
        u3 = User(name="ADMIN", gioitinh="Nam", sdt="0747575464", email="admin", pswd=pswd,goitap_id=1, role=UserRole.ADMIN)
        u4 = User(name="LETAN", gioitinh="Nữ", sdt="012356675777", email="letan", pswd=pswd,goitap_id=1, role=UserRole.LT)
        u5 = User(name="THUNGAN", gioitinh="Nữ", sdt="09736485762", email="thungan", pswd=pswd,goitap_id=1, role=UserRole.TN)
        u6 = User(name="Nguyen Van A", gioitinh="Nam", sdt="0485762674957", email="u6", pswd=pswd, goitap_id=1)
        u7 = User(name="Nguyen Van B", gioitinh="Nam", sdt="023834612534", email="u7", pswd=pswd, goitap_id=2)
        u8 = User(name="Nguyen Van C", gioitinh="Nữ", sdt="012346897", email="u8", pswd=pswd, goitap_id=3)

        db.session.add_all([u1, u2, u3, u4, u5, u6, u7, u8])

        hd1 = HoaDon(name="Hóa đơn của Nguyen Van A",tongtien=90000, trangthai=False,ngaythanhtoan=None,user_id=1)
        hd2 = HoaDon(name="Hóa đơn của Nguyen Van A",tongtien=90000, trangthai=True,ngaythanhtoan=datetime.now(),user_id=1)

        db.session.add_all([hd1, hd2])

        bt1 = BaiTap(name="Chống đẩy", nhomco="Vai, Tay sau", mota="Chống tay xuống sàn, giữ lưng thẳng", avatar = "https://png.pngtree.com/png-vector/20190120/ourmid/pngtree-push-ups-fitness-work-out-gym-png-image_483557.png")
        bt2 = BaiTap(name="Ngồi xổm", nhomco="Mông", mota="Chân rộng ngang vai, hạ người xuống",avatar = "https://png.pngtree.com/png-vector/20190120/ourmid/pngtree-push-ups-fitness-work-out-gym-png-image_483557.png")
        bt3 = BaiTap(name="Tấm ván", nhomco="Lưng", mota="Chống khuỷu tay, giữ thân người thẳng",avatar = "https://png.pngtree.com/png-vector/20190120/ourmid/pngtree-push-ups-fitness-work-out-gym-png-image_483557.png")
        bt4 = BaiTap(name="Cuộn tạ tay", nhomco="Tay trước", mota="Cuộn tạ lên xuống chậm rãi",avatar = "https://png.pngtree.com/png-vector/20190120/ourmid/pngtree-push-ups-fitness-work-out-gym-png-image_483557.png")
        bt5 = BaiTap(name="Gập bụng", nhomco="Bụng", mota="Nằm ngửa, co gối và gập thân trên lên",avatar = "https://png.pngtree.com/png-vector/20190120/ourmid/pngtree-push-ups-fitness-work-out-gym-png-image_483557.png")
        bt6 = BaiTap(name="Nâng chân", nhomco="Bụng dưới", mota="Nằm ngửa, nâng hai chân lên rồi hạ xuống chậm",avatar = "https://png.pngtree.com/png-vector/20190120/ourmid/pngtree-push-ups-fitness-work-out-gym-png-image_483557.png")
        bt7 = BaiTap(name="Hít xà đơn", nhomco="Lưng, Tay trước", mota="Treo người trên xà và kéo thân lên",avatar = "https://png.pngtree.com/png-vector/20190120/ourmid/pngtree-push-ups-fitness-work-out-gym-png-image_483557.png")
        bt8 = BaiTap(name="Đẩy ngực với tạ", nhomco="Ngực", mota="Nằm ghế, đẩy tạ lên cao rồi hạ xuống",avatar = "https://png.pngtree.com/png-vector/20190120/ourmid/pngtree-push-ups-fitness-work-out-gym-png-image_483557.png")
        bt9 = BaiTap(name="Deadlift", nhomco="Lưng dưới, Đùi sau", mota="Gập người nâng tạ từ sàn lên đứng thẳng",avatar = "https://png.pngtree.com/png-vector/20190120/ourmid/pngtree-push-ups-fitness-work-out-gym-png-image_483557.png")
        bt10 = BaiTap(name="Chạy bộ", nhomco="Toàn thân", mota="Chạy tại chỗ hoặc trên máy để tăng sức bền",avatar = "https://png.pngtree.com/png-vector/20190120/ourmid/pngtree-push-ups-fitness-work-out-gym-png-image_483557.png")
        bt11 = BaiTap(name="Nhảy dây", nhomco="Toàn thân", mota="Nhảy liên tục với dây để đốt mỡ",avatar = "https://png.pngtree.com/png-vector/20190120/ourmid/pngtree-push-ups-fitness-work-out-gym-png-image_483557.png")
        bt12 = BaiTap(name="Plank nghiêng", nhomco="Bụng xiên", mota="Chống một tay, giữ thân người nghiêng thẳng",avatar = "https://png.pngtree.com/png-vector/20190120/ourmid/pngtree-push-ups-fitness-work-out-gym-png-image_483557.png")
        bt13 = BaiTap(name="Đá chân sau", nhomco="Mông, Đùi sau", mota="Đứng bám tường, đá chân ra sau",avatar = "https://png.pngtree.com/png-vector/20190120/ourmid/pngtree-push-ups-fitness-work-out-gym-png-image_483557.png")
        bt14 = BaiTap(name="Nâng vai", nhomco="Vai", mota="Cầm tạ, nâng vai lên rồi hạ xuống",avatar = "https://png.pngtree.com/png-vector/20190120/ourmid/pngtree-push-ups-fitness-work-out-gym-png-image_483557.png")

        db.session.add_all([bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9, bt10, bt11, bt12, bt13, bt14])

        db.session.commit()
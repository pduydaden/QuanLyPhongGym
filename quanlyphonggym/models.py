import json

from quanlyphonggym import db, app
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class GoiTap(db.Model):
    magoitap = Column(Integer, primary_key=True, autoincrement=True)
    tengoitap = Column(String(50),unique=True, nullable=False)
    giagoitap = Column(Integer, nullable=False)
    nguoidung =relationship('NguoiDung',lazy=True)

class NguoiDung(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    hoten = Column(String(50))
    gioitinh = Column(String(50))
    namsinh = Column(Integer)
    sdt = Column(String(50))
    email = Column(String(50))
    pswd = Column(String(50))
    vaitro = Column(String(50))
    goitap_id = Column(Integer, ForeignKey(GoiTap.magoitap),nullable=False)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # g1=GoiTap(tengoitap='1 thang',giagoitap=90000)
        # g2 = GoiTap(tengoitap='2 thang', giagoitap=190000)
        # g3 = GoiTap(tengoitap='12 thang', giagoitap=1190000)
        #
        # db.session.add_all([g1,g2,g3])
        with open("data/nguoidung.json", encoding="utf-8") as f:
            nguoidung = json.load(f)
            for p in nguoidung:
                db.session.add(NguoiDung(**p))

        db.session.commit()
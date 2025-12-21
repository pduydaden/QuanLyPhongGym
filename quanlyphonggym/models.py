from quanlyphonggym import db, app
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class GoiTap(db.Model):
    magoitap = Column(Integer, primary_key=True, autoincrement=True)
    tengoitap = Column(String(50),unique=True, nullable=False)
    giagoitap = Column(Integer, nullable=False)



if __name__ == "__main__":
    with app.app_context():
        g1=GoiTap(tengoitap='1 thang',giagoitap=90000)
        g2 = GoiTap(tengoitap='2 thang', giagoitap=190000)
        g3 = GoiTap(tengoitap='12 thang', giagoitap=1190000)

        db.session.add_all([g1,g2,g3])
        db.session.commit()
import json
from models import User, GoiTap
from quanlyphonggym import app
import hashlib


def load_goitap():
    with open('data/goitap.json', encoding='utf-8') as f:
        return json.load(f)

def get_user_by_id(user_id):
    return User.query.get(int(user_id))

def auth_user(email, pswd):
    pswd = hashlib.md5(pswd.encode("utf-8")).hexdigest()
    return User.query.filter(User.email.__eq__(email), User.pswd.__eq__(pswd)).first()

if __name__ == '__main__':
    with app.app_context():
        print(auth_user(email="u1@gmail.com", pswd="123"))
import json


def load_goitap():
    with open('data/goitap.json', encoding='utf-8') as f:
        return json.load(f)

if __name__ == '__main__':
    print(load_goitap())
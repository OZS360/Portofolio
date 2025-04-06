from flask_sqlalchemy import SQLAlchemy
import pytz
from datetime import datetime  # 日付と時刻を扱うために必要

# SQLAlchemy インスタンスの作成
db = SQLAlchemy()

# 日本時間 (JST) で現在時刻を取得
def jst_now():
    return datetime.now(pytz.timezone('Asia/Tokyo'))

# --- データベースのテーブル定義 ---
class SyaroushiTable(db.Model):
    __tablename__ = 'SyaroushiTable'  # テーブル名
    id = db.Column(db.Integer, primary_key=True)  # 主キー
    name = db.Column(db.String(50), nullable=False)  # 名前
    office = db.Column(db.String(50), nullable=False) 
    address = db.Column(db.String(50), nullable=False) 
    phone = db.Column(db.String(50), nullable=False) 
    url = db.Column(db.String(50), nullable=False) 
    region = db.Column(db.String(50), nullable=False) 
    
    def __repr__(self):
        return f'<SyaroushiTable {self.name} - {self.office}>'

class InquiryTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 送信日時の追加
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(128))
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=jst_now)  # JST で現在時刻を保存

    def __repr__(self):
        return f'<InquiryTable {self.name} - {self.created_at}>'

    


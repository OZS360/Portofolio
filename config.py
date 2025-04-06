import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # メール設定
    MAIL_SERVER = 'smtp.gmail.com'  # GmailのSMTPサーバー
    MAIL_PORT = 587  # ポート番号
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'MAIL_USERNAME'  # 自分のメールアドレス
    MAIL_PASSWORD = 'MAIL_PASSWORD'  # アプリパスワード（Gmailの場合）
    MAIL_DEFAULT_SENDER = ('Flask Contact', 'MAIL_USERNAME')  # 送信者名

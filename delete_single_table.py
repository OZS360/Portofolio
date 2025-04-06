from app import db, app
from sqlalchemy import text  # `sqlalchemy.text` を正しくインポート

with app.app_context():
    db.session.execute(text("DROP TABLE IF EXISTS inquiry;"))  # `inquiry` テーブルを削除
    db.session.commit()
    print("不要な `inquiry` テーブルを削除しました。")

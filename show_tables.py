from app import db, app
from sqlalchemy import inspect  # SQLAlchemy の `inspect` をインポート

with app.app_context():
    inspector = inspect(db.engine)  # インスペクターを作成
    tables = inspector.get_table_names()  # 既存のテーブル一覧を取得
    print("現在のデータベースに存在するテーブル:")
    for table in tables:
        print(f"- {table}")

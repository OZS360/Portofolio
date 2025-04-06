from app import db, SyaroushiTable, app
#変数(データの集まり)

with app.app_context():#接続情報を保持
    db.session.query(SyaroushiTable).delete()
    db.session.commit()
    print("すべてのデータを削除しました。")

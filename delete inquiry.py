from app import db, InquiryTable, app
#変数(データの集まり)

with app.app_context():#接続情報を保持
    db.session.query(InquiryTable).delete()
    db.session.commit()
    print("すべてのデータを削除しました。")

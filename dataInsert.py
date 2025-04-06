import os
import pandas as pd
from app import db, SyaroushiTable  # Flaskアプリからdbとモデルをインポート

def insert_csv_data():
    """CSVデータをデータベースに追加する関数"""
    script_dir = os.path.dirname(os.path.abspath(__file__))  # スクリプトのあるディレクトリos.path.abspath() は、指定されたファイルパスの 絶対パス を取得
    csv_path = os.path.join(script_dir, "syaroushi_sample.csv")  # CSV のパス

    print("CSV Path:", csv_path)  # 確認用

    # --- CSVファイルが存在しない場合の処理 ---
    if not os.path.exists(csv_path):
        print("Error: CSV file not found!")
        return

    try:
        # --- CSV をデータフレームとして読み込む ---
        df = pd.read_csv(csv_path)
        print(df.head())  # 確認用に最初の数行を表示

        # --- データベースにデータを追加 ---
        #with app.app_context():
        for _, row in df.iterrows():
            exists = SyaroushiTable.query.filter_by(name=row["社労士の名前"],office=row['事務所名']).first()
            if not exists:
                record = SyaroushiTable(
                    name=row["社労士の名前"],
                    office=row["事務所名"],
                    address=row["住所"],
                    phone=row["電話番号"],
                    url=row["詳細ページのURL"],
                    region=row["地域 (検索用)"]
                )
                db.session.add(record)
            db.session.commit()
        print("CSVデータの挿入が完了しました！")
    
    except Exception as e:
        print(f"Error while inserting CSV data: {e}")

if __name__ == "__main__":
    insert_csv_data()

import os
from config import Config
from flask import Flask,render_template,redirect, url_for, flash, request, send_file
from models import db,SyaroushiTable, InquiryTable # models.pyからインポート
from forms import ContactForm
from flask_mail import Mail, Message
from xml.etree.ElementTree import Element, SubElement, ElementTree
import subprocess
import pandas as pd
import random

# --- カレントディレクトリの確認 ---
print("Current Working Directory:", os.getcwd())

app = Flask(__name__)
app.config.from_object(Config)


# SQLite3 データベースのパスを修正（instance フォルダ内）
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance", "database.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- データベース初期化 ---
db.init_app(app)

# Flask-Mail の設定
mail = Mail(app)
    

# --- データベースとテーブルの作成（初回実行時） ---
with app.app_context():
    db.create_all()
    

@app.route('/')
def home():
        return render_template('Top.html')

def send_confirmation_email(inquiry):
    subject = f'お問い合わせありがとうございます - {inquiry.title}'
    body = f'''
    {inquiry.name} 様,

    以下の内容でお問い合わせを受け付けました。

    ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    【お名前】 {inquiry.name}
    【メールアドレス】 {inquiry.email}
    【件名】 {inquiry.title}
    【メッセージ内容】
    {inquiry.text}
    ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

    担当者より後ほどご連絡いたしますので、今しばらくお待ちください。

    送信日時: {inquiry.created_at.strftime('%Y-%m-%d %H:%M:%S')}
    
    ---------------
    Flask Contact Team
    '''

    msg = Message(
        subject=subject,
        recipients=[inquiry.email],
        body=body
    )
    mail.send(msg)
    
# お問い合わせページ
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        inquiry = InquiryTable(
            name=form.name.data,
            email=form.email.data,
            title=form.title.data,
            text=form.text.data
        )
        db.session.add(inquiry)
        db.session.commit()

        # 送信完了メッセージ
        flash('送信が完了しました。ありがとうございます！')

        # 確認メールの送信
        send_confirmation_email(inquiry)

        # 結果ページにリダイレクト
        return redirect(url_for('result', inquiry_id=inquiry.id))
    return render_template('contact.html', form=form)

# お問い合わせ完了ページ
@app.route('/result/<int:inquiry_id>')
def result(inquiry_id):
    inquiry = InquiryTable.query.get_or_404(inquiry_id)  # データベースから ID で取得
    return render_template('result.html', inquiry=inquiry)

@app.route('/SyaroushiItiran.html', methods=['GET'])
def syaroushi_list():
    query = request.args.get('query', '')  # 検索キーワードを取得
    if query:
        # 名前または事務所名に部分一致するデータを取得
        results = SyaroushiTable.query.filter(
            (SyaroushiTable.name.ilike(f"%{query}%")) |
            (SyaroushiTable.office.ilike(f"%{query}%"))
        ).all()
    else:
        results = SyaroushiTable.query.all()
    print("検索ワード",query)
    print("ーーーーーーーーーーーーーーーーーーーー")
    print("検索結果",results)
    return render_template('SyaroushiItiran.html', data=results, query=query)

@app.route("/search")
def search_query():
    query = request.args.get("query","")
    print(query)
    if query:
    # 名前または事務所名に部分一致するデータを取得
        results = SyaroushiTable.query.filter(
            (SyaroushiTable.name.ilike(f"%{query}%")) |
            (SyaroushiTable.office.ilike(f"%{query}%"))
        ).all()[0].name
    else:

        results = "検索結果がありません"
    print(results)
    return str(results)+"がヒットしました。<strong>これは強調される文字です</strong>"

# フォームから受け取ったデータをXMLに変換
def generate_xml(data, output_path="data.xml"):
    root = Element("標準報酬決定通知書")

    SubElement(root, "宛名").text = data["宛名"]
    SubElement(root, "発行日").text = data["発行日"]

    被保険者 = SubElement(root, "被保険者")
    SubElement(被保険者, "整理番号").text = data["整理番号"]
    SubElement(被保険者, "氏名").text = data["氏名"]
    SubElement(被保険者, "生年月日").text = data["生年月日"]
    SubElement(被保険者, "性別").text = data["性別"]
    SubElement(被保険者, "資格取得年月日").text = data["資格取得年月日"]
    SubElement(被保険者, "決定年月日").text = data["決定年月日"]
    SubElement(被保険者, "決定等級").text = data["決定等級"]
    SubElement(被保険者, "標準報酬月額").text = data["標準報酬月額"]

    tree = ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    return output_path

# フォーム画面
@app.route("/form")
def form():
    return render_template("form.html")

# PDF出力処理
@app.route("/generate", methods=["POST"])
@app.route("/generate", methods=["POST"])
def generate():
    data = request.form
    base_dir = os.path.dirname(__file__)
    
    xml_path = generate_xml(data, os.path.join(base_dir, "data.xml"))
    xsl_path = os.path.join(base_dir, "notice_style.xsl")
    pdf_path = os.path.join(base_dir, "output.pdf")

    result = subprocess.run([
        "C:/fop-2.10/fop/fop.bat",
        "-c", "C:/fop-2.10/fop/conf/fop.xconf",
        "-xml", xml_path,
        "-xsl", xsl_path,
        "-pdf", pdf_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print(result.stdout)
    print(result.stderr)

    if not os.path.exists(pdf_path):
        return "❌ PDF出力に失敗しました。", 500

    # ✅ PDFをブラウザでそのまま表示！
    return send_file(pdf_path, mimetype="application/pdf", as_attachment=False)

@app.route("/check")
def check_view():
    return render_template("check.html")

@app.route('/numbers3')
def index():
    # CSV読み込み
    csv_path = os.path.join(os.path.dirname(__file__), 'numbers3_with_box_history.csv')
    
    df = pd.read_csv(csv_path, dtype={
    '当せん番号': str,
    'BOX': str
})

    # 抽せん日をdatetime型に
    df['抽せん日'] = pd.to_datetime(df['抽せん日'])
    
    # 並べ替え（古い順にする）
    df = df.sort_values('抽せん日').reset_index(drop=True)
    
    # 最新30件を抽選日が新しい順で取得
    latest_30 = df.sort_values('抽せん日', ascending=False).head(30).copy()

    # 各BOXの過去3件を取得
    box_matches = []
    for _, row in latest_30.iterrows():
        box = row['BOX']
        date = row['抽せん日']
        past = df[(df['BOX'] == box) & (df['抽せん日'] < date)]
        matched = past.sort_values('抽せん日', ascending=False).head(3)
        box_matches.append(', '.join(matched['回号'].tolist()) if not matched.empty else '')

    latest_30['直近BOX3回'] = box_matches
    latest_30 = latest_30.sort_values('抽せん日', ascending=False)

    return render_template('numbers3.html', table=latest_30.to_dict(orient='records'))

@app.route('/numbers4')
def index2():
    # CSV読み込み
    csv_path = os.path.join(os.path.dirname(__file__), 'numbers4_with_box_history.csv')
    
    df = pd.read_csv(csv_path, dtype={
    '当せん番号': str,
    'BOX': str
})

    # 抽せん日をdatetime型に
    df['抽せん日'] = pd.to_datetime(df['抽せん日'])
    
    # 並べ替え（古い順にする）
    df = df.sort_values('抽せん日').reset_index(drop=True)
    
    # 最新30件を抽選日が新しい順で取得
    latest_30 = df.sort_values('抽せん日', ascending=False).head(30).copy()

    # 各BOXの過去3件を取得
    box_matches = []
    for _, row in latest_30.iterrows():
        box = row['BOX']
        date = row['抽せん日']
        past = df[(df['BOX'] == box) & (df['抽せん日'] < date)]
        matched = past.sort_values('抽せん日', ascending=False).head(3)
        box_matches.append(', '.join(matched['回号'].tolist()) if not matched.empty else '')

    latest_30['直近BOX3回'] = box_matches
    latest_30 = latest_30.sort_values('抽せん日', ascending=False)

    return render_template('numbers4.html', table=latest_30.to_dict(orient='records'))

def load_latest_10_draws(csv_path):
    df = pd.read_csv(csv_path)
    df['抽せん日'] = pd.to_datetime(df['抽せん日'])
    df = df.sort_values('抽せん日', ascending=False).reset_index(drop=True)
    return df.head(10)

def generate_combinations(latest_draws, num_sets=5):
    # 本数字6列からすべての数字を抽出
    numbers = []
    for i in range(1, 7):
        numbers += latest_draws[f'本数字{i}'].tolist()

    numbers = list(map(int, numbers))  # 念のためint変換
    candidates = []

    for _ in range(num_sets):
        picked = random.sample(numbers, 6)
        picked.sort()
        candidates.append(picked)

    return candidates

@app.route('/lotto6', methods=['GET', 'POST'])
def index3():
    csv_path = os.path.join(os.path.dirname(__file__), 'loto6_results.csv')
    latest_draws = load_latest_10_draws(csv_path)

    generated = []
    if request.method == 'POST':
        generated = generate_combinations(latest_draws)

    return render_template('lotto6.html',
    latest_draws=latest_draws.to_dict(orient='records'),
    generated=generated)

if __name__ == "__main__":
    app.run(debug=True)
    


document.addEventListener('DOMContentLoaded', () => {
    // 🌙 ダークモード切り替え
    const toggleBtn = document.querySelector('.btn-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        toggleBtn.textContent = document.body.classList.contains('dark-mode')
          ? '☀️ ライトモード'
          : '🌙 ダークモード';
      });
    }

  // 📊 月額チェックの入力処理（存在すれば実行）
  const inputs = ['prevSalary', 'month1', 'month2', 'month3'];
  const allExist = inputs.every(id => document.getElementById(id));


  if (allExist) {
// グレード判定テーブル
const gradeTable = [
    { min: 0, max: 63000, grade: 1 },
    { min: 63000, max: 73000, grade: 2 },
    { min: 73000, max: 83000, grade: 3 },
    { min: 83000, max: 93000, grade: 4 },
    { min: 93000, max: 101000, grade: 5 },
    { min: 101000, max: 107000, grade: 6 },
    { min: 107000, max: 114000, grade: 7 },
    { min: 114000, max: 122000, grade: 8 },
    { min: 122000, max: 130000, grade: 9 },
    { min: 130000, max: 138000, grade: 10 },
    { min: 138000, max: 146000, grade: 11 },
    { min: 146000, max: 155000, grade: 12 },
    { min: 155000, max: 165000, grade: 13 },
    { min: 165000, max: 175000, grade: 14 },
    { min: 175000, max: 185000, grade: 15 },
    { min: 185000, max: 195000, grade: 16 },
    { min: 195000, max: 210000, grade: 17 },
    { min: 210000, max: 230000, grade: 18 },
    { min: 230000, max: 250000, grade: 19 },
    { min: 250000, max: 270000, grade: 20 },
    { min: 270000, max: 290000, grade: 21 },
    { min: 290000, max: 310000, grade: 22 },
    { min: 310000, max: 330000, grade: 23 },
    { min: 330000, max: 350000, grade: 24 },
    { min: 350000, max: 370000, grade: 25 },
    { min: 370000, max: 395000, grade: 26 },
    { min: 395000, max: 425000, grade: 27 },
    { min: 425000, max: 455000, grade: 28 },
    { min: 455000, max: 485000, grade: 29 },
    { min: 485000, max: 515000, grade: 30 },
    { min: 515000, max: 545000, grade: 31 },
    { min: 545000, max: 575000, grade: 32 },
    { min: 575000, max: 605000, grade: 33 },
    { min: 605000, max: 635000, grade: 34 },
    { min: 635000, max: 665000, grade: 35 },
    { min: 665000, max: 695000, grade: 36 },
    { min: 695000, max: 730000, grade: 37 },
    { min: 730000, max: 770000, grade: 38 },
    { min: 770000, max: 810000, grade: 39 },
    { min: 810000, max: 855000, grade: 40 },
    { min: 855000, max: 905000, grade: 41 },
    { min: 905000, max: 955000, grade: 42 },
    { min: 955000, max: 1005000, grade: 43 },
    { min: 1005000, max: 1055000, grade: 44 },
    { min: 1055000, max: 1115000, grade: 45 },
    { min: 1115000, max: 1175000, grade: 46 },
    { min: 1175000, max: 1235000, grade: 47 },
    { min: 1235000, max: 1295000, grade: 48 },
    { min: 1295000, max: 1355000, grade: 49 },
    { min: 1355000, max: Infinity, grade: 50 },
];

function getGrade(value) {
    if (isNaN(value) || value === '') return null;
    const match = gradeTable.find(g => value >= g.min && value < g.max);
    return match ? match.grade : null;
}
function update() {
    const prevSalary = parseFloat(document.getElementById('prevSalary').value);
    const month1 = parseFloat(document.getElementById('month1').value);
    const month2 = parseFloat(document.getElementById('month2').value);
    const month3 = parseFloat(document.getElementById('month3').value);

    const avgSalary = (month1 + month2 + month3) / 3;
    document.getElementById('avgSalary').value = isNaN(avgSalary) ? "" : Math.round(avgSalary);

    const prevGrade = getGrade(prevSalary);
    const avgGrade = getGrade(avgSalary);

    document.getElementById('prevGrade').textContent = prevGrade ? `等級 ${prevGrade}` : "";
    document.getElementById('avgGrade').textContent = avgGrade ? `等級 ${avgGrade}` : "";

    if (prevGrade && avgGrade && Math.abs(prevGrade - avgGrade) >= 2) {
        document.getElementById('warning').classList.remove('d-none');
    } else {
        document.getElementById('warning').classList.add('d-none');
    }

}

//イベント登録
document.querySelectorAll('input').forEach(input => { input.addEventListener('input', update) });

// フォーカス移動の順序指定
const inputOrder = [
    'prevSalary',
    'month1',
    'month2',
    'month3'
];

// Enterキーで次のinputに移動
inputOrder.forEach((id, index) => {
    const input = document.getElementById(id);
    input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault(); // Enterでフォーム送信されるのを防ぐ
            const nextId = inputOrder[index + 1];
            if (nextId) {
                document.getElementById(nextId).focus();
            }
        }
    });
});
}
});
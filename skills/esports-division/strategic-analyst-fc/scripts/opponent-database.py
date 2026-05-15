import json
from datetime import datetime

DB_FILE = "fc_opponents_db.json"

def load_db():
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"المنافسون": {}}

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_opponent():
    db = load_db()
    print("=== إضافة منافس ===")
    name = input("اسم اللاعب/المنافس: ").strip()
    
    opponent = {
        "المنطقة": input("المنطقة: ").strip(),
        "الترتيب": input("الترتيب: ").strip(),
        "التشكيلة_المفضلة": input("التشكيلة المفضلة: ").strip(),
        "أسلوب_اللعب": input("أسلوب اللعب (هجومي/متوازن/دفاعي): ").strip(),
        "بناء_الهجوم": input("بناء الهجوم (سريع/بطيء/مختلط): ").strip(),
        "أسلوب_الدفاع": input("أسلوب الدفاع (ضغط عالي/كتلة وسطى/دفاعي): ").strip(),
        "نقاط_القوة": [],
        "نقاط_الضعف": [],
        "سجل_المواجهات": {"فوز": 0, "تعادل": 0, "خسارة": 0},
        "ملاحظات": input("ملاحظات عامة: ").strip(),
        "آخر_تحديث": datetime.now().strftime("%Y-%m-%d")
    }
    
    print("نقاط القوة (اكتب 'تم' للإنهاء):")
    while True:
        s = input("- ").strip()
        if s == "تم" or not s:
            break
        opponent["نقاط_القوة"].append(s)
    
    print("نقاط الضعف (اكتب 'تم' للإنهاء):")
    while True:
        w = input("- ").strip()
        if w == "تم" or not w:
            break
        opponent["نقاط_الضعف"].append(w)
    
    db["المنافسون"][name] = opponent
    save_db(db)
    print(f"تم إضافة/تحديث المنافس: {name}")

def list_opponents():
    db = load_db()
    opponents = db["المنافسون"]
    if not opponents:
        print("لا يوجد منافسون في قاعدة البيانات")
        return
    print(f"\n=== قائمة المنافسين ({len(opponents)}) ===")
    for name, info in opponents.items():
        record = info["سجل_المواجهات"]
        total = record["فوز"] + record["تعادل"] + record["خسارة"]
        wr = (record["فوز"] / total * 100) if total > 0 else 0
        print(f"  {name} | {info['التشكيلة_المفضلة']} | {info['أسلوب_اللعب']} | سجل: {record['فوز']}و{record['تعادل']}ت{record['خسارة']}خ | فوز: {wr:.0f}%")

def update_result():
    db = load_db()
    list_opponents()
    name = input("\nاسم المنافس: ").strip()
    if name not in db["المنافسون"]:
        print("المنافس غير موجود")
        return
    result = input("النتيجة (فوز/تعادل/خسارة): ").strip()
    if result in db["المنافسون"][name]["سجل_المواجهات"]:
        db["المنافسون"][name]["سجل_المواجهات"][result] += 1
        db["المنافسون"][name]["آخر_تحديث"] = datetime.now().strftime("%Y-%m-%d")
        save_db(db)
        print(f"تم تحديث السجل: {name}")

if __name__ == "__main__":
    print("1. إضافة منافس\n2. عرض المنافسين\n3. تحديث نتيجة")
    choice = input("اختر: ").strip()
    if choice == "1":
        add_opponent()
    elif choice == "2":
        list_opponents()
    elif choice == "3":
        update_result()

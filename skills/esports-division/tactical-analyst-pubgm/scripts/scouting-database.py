import json
from datetime import datetime

DB_FILE = "scouting_database.json"

def load_db():
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"الفرق_المنافسة": {}}

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_team():
    db = load_db()
    print("=== إضافة فريق منافس ===")
    name = input("اسم الفريق: ").strip()
    
    team = {
        "المنطقة": input("المنطقة: ").strip(),
        "الترتيب": input("الترتيب الحالي: ").strip(),
        "أسلوب_اللعب": input("أسلوب اللعب (هجومي/دفاعي/متوازن): ").strip(),
        "نقاط_الهبوط": {
            "Erangel": input("نقطة هبوط Erangel: ").strip(),
            "Miramar": input("نقطة هبوط Miramar: ").strip(),
            "Sanhok": input("نقطة هبوط Sanhok: ").strip(),
        },
        "نقاط_القوة": [],
        "نقاط_الضعف": [],
        "اللاعبون": [],
        "آخر_تحديث": datetime.now().strftime("%Y-%m-%d"),
        "سجل_المواجهات": {"فوز": 0, "خسارة": 0}
    }
    
    print("أدخل نقاط القوة (اكتب 'تم' للإنهاء):")
    while True:
        s = input("- ").strip()
        if s == "تم" or not s:
            break
        team["نقاط_القوة"].append(s)
    
    print("أدخل نقاط الضعف (اكتب 'تم' للإنهاء):")
    while True:
        w = input("- ").strip()
        if w == "تم" or not w:
            break
        team["نقاط_الضعف"].append(w)
    
    db["الفرق_المنافسة"][name] = team
    save_db(db)
    print(f"تم إضافة/تحديث الفريق: {name}")

def list_teams():
    db = load_db()
    teams = db["الفرق_المنافسة"]
    if not teams:
        print("لا توجد فرق في قاعدة البيانات")
        return
    print(f"\n=== الفرق المنافسة ({len(teams)}) ===")
    for name, info in teams.items():
        print(f"  {name} | {info['المنطقة']} | أسلوب: {info['أسلوب_اللعب']} | آخر تحديث: {info['آخر_تحديث']}")

def update_match_result():
    db = load_db()
    list_teams()
    name = input("\nاسم الفريق: ").strip()
    if name not in db["الفرق_المنافسة"]:
        print("الفريق غير موجود")
        return
    result = input("النتيجة (فوز/خسارة): ").strip()
    db["الفرق_المنافسة"][name]["سجل_المواجهات"][result] += 1
    db["الفرق_المنافسة"][name]["آخر_تحديث"] = datetime.now().strftime("%Y-%m-%d")
    save_db(db)
    print(f"تم تحديث السجل: {name}")

if __name__ == "__main__":
    print("1. إضافة فريق\n2. عرض الفرق\n3. تحديث نتيجة مواجهة")
    choice = input("اختر: ").strip()
    if choice == "1":
        add_team()
    elif choice == "2":
        list_teams()
    elif choice == "3":
        update_match_result()

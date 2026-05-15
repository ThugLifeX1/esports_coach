import json
from datetime import datetime

DB_FILE = "academy_prospects.json"

def load_db():
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"الناشئون": {}}

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_prospect():
    db = load_db()
    print("=== إضافة ناشئ جديد ===")
    name = input("الاسم: ").strip()
    
    prospect = {
        "العمر": int(input("العمر: ").strip() or "0"),
        "اللعبة": input("اللعبة (PUBGM/FC): ").strip(),
        "IGN": input("اسم في اللعبة: ").strip(),
        "المستوى": "تأسيسي",
        "تاريخ_الانضمام": datetime.now().strftime("%Y-%m-%d"),
        "الحالة": "نشط",
        "تقييمات": [],
        "سجل_الحضور": {"حاضر": 0, "متأخر": 0, "غائب": 0, "معذور": 0},
        "ملاحظات": input("ملاحظات أولية: ").strip()
    }
    
    db["الناشئون"][name] = prospect
    save_db(db)
    print(f"تم إضافة الناشئ: {name}")

def add_evaluation():
    db = load_db()
    name = input("اسم الناشئ: ").strip()
    if name not in db["الناشئون"]:
        print("الناشئ غير موجود")
        return
    
    print("=== تقييم شهري ===")
    eval_data = {
        "التاريخ": datetime.now().strftime("%Y-%m-%d"),
        "مهارات_فنية": int(input("المهارات الفنية (1-10): ").strip() or "5"),
        "التزام": int(input("الالتزام والسلوك (1-10): ").strip() or "5"),
        "لياقة_ذهنية": int(input("اللياقة الذهنية (1-10): ").strip() or "5"),
        "ملاحظات": input("ملاحظات: ").strip()
    }
    
    total = (eval_data["مهارات_فنية"] * 0.4 +
             eval_data["التزام"] * 0.3 +
             eval_data["لياقة_ذهنية"] * 0.3)
    eval_data["المعدل_الكلي"] = round(total, 1)
    
    if total >= 8:
        eval_data["التوصية"] = "ترقية مستوى"
    elif total >= 6:
        eval_data["التوصية"] = "استمرار"
    elif total >= 4:
        eval_data["التوصية"] = "تحذير"
    else:
        eval_data["التوصية"] = "مراجعة استمرارية"
    
    db["الناشئون"][name]["تقييمات"].append(eval_data)
    save_db(db)
    print(f"المعدل الكلي: {eval_data['المعدل_الكلي']}")
    print(f"التوصية: {eval_data['التوصية']}")

def list_prospects():
    db = load_db()
    prospects = db["الناشئون"]
    if not prospects:
        print("لا يوجد ناشئون")
        return
    
    print(f"\n=== الناشئون ({len(prospects)}) ===")
    print(f"{'الاسم':<15} {'العمر':<6} {'اللعبة':<8} {'المستوى':<10} {'آخر تقييم':<12} {'الحالة'}")
    print("-" * 65)
    for name, info in prospects.items():
        last_eval = info["تقييمات"][-1]["المعدل_الكلي"] if info["تقييمات"] else "لا يوجد"
        print(f"{name:<15} {info['العمر']:<6} {info['اللعبة']:<8} {info['المستوى']:<10} {str(last_eval):<12} {info['الحالة']}")

if __name__ == "__main__":
    print("1. إضافة ناشئ\n2. تقييم ناشئ\n3. عرض الناشئين")
    choice = input("اختر: ").strip()
    if choice == "1":
        add_prospect()
    elif choice == "2":
        add_evaluation()
    elif choice == "3":
        list_prospects()

import json
from datetime import datetime, timedelta

TRACKER_FILE = "team_ops.json"

def load_data():
    try:
        with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"لاعبون": {}, "طلبات": [], "مخالفات": []}

def save_data(data):
    with open(TRACKER_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_player():
    data = load_data()
    name = input("اسم اللاعب: ").strip()
    data["لاعبون"][name] = {
        "اللعبة": input("اللعبة (PUBGM/FC): ").strip(),
        "الدور": input("الدور (أساسي/بديل): ").strip(),
        "تاريخ_التوقيع": input("تاريخ التوقيع (YYYY-MM-DD): ").strip(),
        "تاريخ_انتهاء_العقد": input("تاريخ انتهاء العقد (YYYY-MM-DD): ").strip(),
        "الحالة": "نشط",
        "ملاحظات": input("ملاحظات: ").strip()
    }
    save_data(data)
    print(f"تم إضافة اللاعب: {name}")

def add_request():
    data = load_data()
    req = {
        "التاريخ": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "اللاعب": input("اسم اللاعب: ").strip(),
        "النوع": input("النوع (معدات/سفر/إداري/أخرى): ").strip(),
        "التفاصيل": input("التفاصيل: ").strip(),
        "الأولوية": input("الأولوية (طوارئ/عاجل/عادي/منخفض): ").strip(),
        "الحالة": "مفتوح"
    }
    data["طلبات"].append(req)
    save_data(data)
    print("تم تسجيل الطلب")

def show_roster():
    data = load_data()
    players = data["لاعبون"]
    if not players:
        print("لا يوجد لاعبون")
        return
    print(f"\n=== قائمة اللاعبين ({len(players)}) ===\n")
    for name, info in players.items():
        print(f" {name} | {info['اللعبة']} | {info['الدور']} | عقد حتى: {info['تاريخ_انتهاء_العقد']} | {info['الحالة']}")

def check_contracts():
    data = load_data()
    threshold = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
    print("\n=== عقود قريبة الانتهاء (60 يوم) ===")
    found = False
    for name, info in data["لاعبون"].items():
        if info["تاريخ_انتهاء_العقد"] <= threshold and info["الحالة"] == "نشط":
            print(f" ⚠️ {name} | ينتهي: {info['تاريخ_انتهاء_العقد']}")
            found = True
    if not found:
        print("لا توجد عقود قريبة الانتهاء")

def show_open_requests():
    data = load_data()
    open_reqs = [r for r in data["طلبات"] if r["الحالة"] == "مفتوح"]
    if not open_reqs:
        print("لا توجد طلبات مفتوحة")
        return
    print(f"\n=== الطلبات المفتوحة ({len(open_reqs)}) ===\n")
    for r in open_reqs:
        print(f" [{r['الأولوية']}] {r['اللاعب']} - {r['النوع']}: {r['التفاصيل']} ({r['التاريخ']})")

def close_request():
    data = load_data()
    show_open_requests()
    idx = int(input("رقم الطلب (1-based): ").strip()) - 1
    open_reqs = [i for i, r in enumerate(data["طلبات"]) if r["الحالة"] == "مفتوح"]
    if 0 <= idx < len(open_reqs):
        data["طلبات"][open_reqs[idx]]["الحالة"] = "مغلق"
        save_data(data)
        print("تم إغلاق الطلب")

if __name__ == "__main__":
    print("1. إضافة لاعب\n2. تسجيل طلب\n3. عرض القائمة\n4. فحص العقود\n5. الطلبات المفتوحة\n6. إغلاق طلب")
    choice = input("اختر: ").strip()
    if choice == "1": add_player()
    elif choice == "2": add_request()
    elif choice == "3": show_roster()
    elif choice == "4": check_contracts()
    elif choice == "5": show_open_requests()
    elif choice == "6": close_request()

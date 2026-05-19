import json
from datetime import datetime

ROSTER_FILE = "roster_data.json"

MIN_PLAYERS = 4
MAX_PLAYERS = 6

FIELDS = {
    "الاسم_الكامل": "الاسم الكامل",
    "IGN": "الاسم داخل اللعبة (IGN)",
    "UID": "UID",
    "الجنس": "الجنس (ذكر/أنثى)",
    "الجنسية": "الجنسية",
    "رقم_الهاتف": "رقم الهاتف",
    "رقم_واتساب": "رقم واتساب",
    "البريد_الإلكتروني": "البريد الإلكتروني",
    "تاريخ_الميلاد": "تاريخ الميلاد (YYYY-MM-DD)",
    "الدور_في_الفريق": "الدور (IGL/Fragger/Support/Sniper/Flex/Sub)",
    "الجهاز": "الجهاز",
    "FPS": "FPS",
    "ملاحظات": "ملاحظات إضافية"
}

def load_data():
    try:
        with open(ROSTER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"لاعبون": {}, "طلبات_مستندات": [], "تسجيلات": []}

def save_data(data):
    with open(ROSTER_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_player():
    data = load_data()
    count = len(data["لاعبون"])
    if count >= MAX_PLAYERS:
        print(f"القائمة ممتلئة ({count}/{MAX_PLAYERS}). لا يمكن إضافة لاعب جديد.")
        return
    ign = input("الاسم داخل اللعبة (IGN): ").strip()
    if ign in data["لاعبون"]:
        print("هذا اللاعب موجود بالفعل")
        return
    player = {}
    for key, prompt in FIELDS.items():
        if key == "IGN":
            player[key] = ign
            continue
        if key == "UID":
            player[key] = input(f"{prompt}: ").strip()
        elif key == "FPS":
            player[key] = int(input(f"{prompt}: ").strip() or "0")
        else:
            player[key] = input(f"{prompt}: ").strip()
    player["الحالة"] = "نشط"
    player["تاريخ_الانضمام"] = datetime.now().strftime("%Y-%m-%d")
    player["المستندات"] = {
        "صورة_رسمية": "✗",
        "صورة_فوتو": "✗",
        "جواز_سفر": "✗",
        "هوية_وطنية": "✗",
        "UID_مؤكد": "✗"
    }
    data["لاعبون"][ign] = player
    save_data(data)
    print(f"تم إضافة {ign} ({count+1}/{MAX_PLAYERS})")

def show_roster():
    data = load_data()
    players = data["لاعبون"]
    if not players:
        print("القائمة فارغة")
        return
    print(f"\n{'='*60}")
    print(f"  قائمة الفريق ({len(players)}/{MAX_PLAYERS})")
    print(f"{'='*60}")
    for ign, p in players.items():
        print(f"\n  🎮 {ign} ({p.get('الدور_في_الفريق','')})")
        print(f"     الاسم: {p.get('الاسم_الكامل','')} | {p.get('الجنس','')} | {p.get('الجنسية','')}")
        print(f"     UID: {p.get('UID','')} | الجهاز: {p.get('الجهاز','')} | FPS: {p.get('FPS','')}")
        print(f"     هاتف: {p.get('رقم_الهاتف','')} | واتساب: {p.get('رقم_واتساب','')}")
        print(f"     بريد: {p.get('البريد_الإلكتروني','')}")
        print(f"     الحالة: {p.get('الحالة','')} | ملاحظات: {p.get('ملاحظات','')}")

def update_player():
    data = load_data()
    ign = input("IGN اللاعب: ").strip()
    if ign not in data["لاعبون"]:
        print("اللاعب غير موجود")
        return
    print("الحقل المراد تحديثه:")
    for i, (key, prompt) in enumerate(FIELDS.items(), 1):
        print(f"  {i}. {prompt} ({key})")
    print(f"  {len(FIELDS)+1}. الحالة")
    idx = int(input("الرقم: ").strip()) - 1
    keys = list(FIELDS.keys())
    if 0 <= idx < len(keys):
        key = keys[idx]
        data["لاعبون"][ign][key] = input(f"القيمة الجديدة: ").strip()
    elif idx == len(keys):
        data["لاعبون"][ign]["الحالة"] = input("الحالة (نشط/إصابة/غائب/معار): ").strip()
    else:
        print("خيار غير صحيح")
        return
    save_data(data)
    print(f"تم تحديث بيانات {ign}")

def check_documents():
    data = load_data()
    print(f"\n{'='*50}")
    print("  حالة المستندات")
    print(f"{'='*50}")
    for ign, p in data["لاعبون"].items():
        docs = p.get("المستندات", {})
        missing = [k for k, v in docs.items() if v == "✗"]
        status = "✅ مكتمل" if not missing else f"⚠️ ينقص {len(missing)}"
        print(f"\n  {ign}: {status}")
        for doc, val in docs.items():
            print(f"    {doc}: {val}")

def update_document():
    data = load_data()
    ign = input("IGN اللاعب: ").strip()
    if ign not in data["لاعبون"]:
        print("اللاعب غير موجود")
        return
    docs = data["لاعبون"][ign].get("المستندات", {})
    print("المستندات:")
    for i, (doc, val) in enumerate(docs.items(), 1):
        print(f"  {i}. {doc}: {val}")
    idx = int(input("رقم المستند: ").strip()) - 1
    doc_keys = list(docs.keys())
    if 0 <= idx < len(doc_keys):
        data["لاعبون"][ign]["المستندات"][doc_keys[idx]] = "✓"
        save_data(data)
        print(f"تم تحديث {doc_keys[idx]} لـ {ign}")

def prepare_registration():
    data = load_data()
    tournament = input("اسم البطولة: ").strip()
    print(f"\nتحضير تسجيل: {tournament}")
    print(f"اللاعبون المتاحون ({len(data['لاعبون'])}):")
    available = []
    for ign, p in data["لاعبون"].items():
        if p.get("الحالة") == "نشط":
            docs_ok = all(v == "✓" for v in p.get("المستندات", {}).values())
            status = "✅" if docs_ok else "⚠️ مستندات ناقصة"
            available.append(ign)
            print(f"  {ign} ({p.get('الدور_في_الفريق','')}) - {status}")
    selected = input("\nأسماء اللاعبين المشاركين (مفصولة بفاصلة): ").strip()
    selected_list = [x.strip() for x in selected.split(",") if x.strip()]
    if len(selected_list) < MIN_PLAYERS:
        print(f"يجب اختيار {MIN_PLAYERS} لاعبين على الأقل")
        return
    if len(selected_list) > MAX_PLAYERS:
        print(f"الحد الأقصى {MAX_PLAYERS} لاعبين")
        return
    reg = {
        "البطولة": tournament,
        "التاريخ": datetime.now().strftime("%Y-%m-%d"),
        "اللاعبون": selected_list,
        "الحالة": "جاهز للتسجيل"
    }
    data["تسجيلات"].append(reg)
    save_data(data)
    print(f"\nتم تحضير تسجيل {tournament} بـ {len(selected_list)} لاعبين")
    for ign in selected_list:
        p = data["لاعبون"].get(ign, {})
        print(f"  {ign} | UID: {p.get('UID','')} | {p.get('الدور_في_الفريق','')}")

def send_instruction():
    data = load_data()
    if not data["لاعبون"]:
        print("لا يوجد لاعبون")
        return
    print("إرسال توجيه للاعبين:")
    instruction = input("نص التوجيه: ").strip()
    source = input("المصدر (المدرب الرئيسي/المساعد/أخرى): ").strip()
    channel = input("القناة (واتساب/تليجرام/بريد/الكل): ").strip()
    print(f"\n{'='*40}")
    print(f"  📢 توجيه من {source}")
    print(f"{'='*40}")
    print(f"  {instruction}")
    print(f"  القناة: {channel}")
    print(f"  المرسل إليهم:")
    for ign, p in data["لاعبون"].items():
        print(f"    - {ign} ({p.get('رقم_واتساب','')}) | {p.get('البريد_الإلكتروني','')}")
    print(f"\n  ⚠️ يرجى تأكيد الاستلام بالرد ✓")

if __name__ == "__main__":
    print("=== مدير القائمة ===")
    print("1. إضافة لاعب\n2. عرض القائمة\n3. تحديث بيانات لاعب")
    print("4. فحص المستندات\n5. تحديث مستند\n6. تحضير تسجيل بطولة")
    print("7. إرسال توجيه")
    choice = input("اختر: ").strip()
    if choice == "1": add_player()
    elif choice == "2": show_roster()
    elif choice == "3": update_player()
    elif choice == "4": check_documents()
    elif choice == "5": update_document()
    elif choice == "6": prepare_registration()
    elif choice == "7": send_instruction()

import json
from datetime import datetime

TRACKER_FILE = "design_requests.json"

def load_tracker():
    try:
        with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"طلبات": []}

def save_tracker(data):
    with open(TRACKER_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_request():
    data = load_tracker()
    print("=== طلب تصميم جديد ===")
    
    request = {
        "id": f"D{datetime.now().strftime('%Y%m%d%H%M')}",
        "التاريخ": datetime.now().strftime("%Y-%m-%d"),
        "الجهة_الطالبة": input("الجهة الطالبة: ").strip(),
        "النوع": input("النوع (سوشيال/بث/مطبوعات/ميرتش): ").strip(),
        "التفاصيل": input("تفاصيل الطلب: ").strip(),
        "الموعد_النهائي": input("الموعد النهائي (YYYY-MM-DD): ").strip(),
        "الأولوية": input("الأولوية (عاجل/عالي/عادي/منخفض): ").strip(),
        "الحالة": "جديد",
        "المصمم": "",
        "ملاحظات": ""
    }
    
    data["طلبات"].append(request)
    save_tracker(data)
    print(f"تم تسجيل الطلب: {request['id']} | الموعد: {request['الموعد_النهائي']}")

def update_status():
    data = load_tracker()
    req_id = input("رقم الطلب: ").strip()
    statuses = ["جديد", "قيد_العمل", "مراجعة", "تعديل", "مكتمل", "ملغي"]
    
    for req in data["طلبات"]:
        if req["id"] == req_id:
            print(f"الحالة الحالية: {req['الحالة']}")
            print(f"الخيارات: {' / '.join(statuses)}")
            new_status = input("الحالة الجديدة: ").strip()
            req["الحالة"] = new_status
            req["ملاحظات"] = input("ملاحظات: ").strip()
            save_tracker(data)
            print(f"تم تحديث الطلب: {req_id} → {new_status}")
            return
    
    print("الطلب غير موجود")

def show_pending():
    data = load_tracker()
    pending = [r for r in data["طلبات"] if r["الحالة"] not in ["مكتمل", "ملغي"]]
    
    if not pending:
        print("لا توجد طلبات معلقة")
        return
    
    print(f"\n=== الطلبات المعلقة ({len(pending)}) ===")
    for r in sorted(pending, key=lambda x: x["الموعد_النهائي"]):
        print(f"  {r['id']} | {r['النوع']} | {r['الجهة_الطالبة']} | موعد: {r['الموعد_النهائي']} | {r['الأولوية']} | {r['الحالة']}")

if __name__ == "__main__":
    print("1. طلب جديد\n2. تحديث حالة\n3. عرض المعلق")
    choice = input("اختر: ").strip()
    if choice == "1":
        add_request()
    elif choice == "2":
        update_status()
    elif choice == "3":
        show_pending()

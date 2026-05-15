import json
from datetime import datetime

TRACKER_FILE = "video_projects.json"

def load_projects():
    try:
        with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"مشاريع": []}

def save_projects(data):
    with open(TRACKER_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_project():
    data = load_projects()
    print("=== مشروع فيديو جديد ===")
    
    project = {
        "id": f"V{datetime.now().strftime('%Y%m%d%H%M')}",
        "التاريخ": datetime.now().strftime("%Y-%m-%d"),
        "العنوان": input("عنوان المشروع: ").strip(),
        "النوع": input("النوع (ملخص/ريلز/وثائقي/كواليس/إعلان): ").strip(),
        "المنصة_المستهدفة": input("المنصة (YouTube/TikTok/Instagram/Twitter): ").strip(),
        "المدة_المستهدفة": input("المدة المستهدفة: ").strip(),
        "الموعد_النهائي": input("الموعد النهائي (YYYY-MM-DD): ").strip(),
        "الحالة": "جديد",
        "اللقطات_المتاحة": input("اللقطات متاحة؟ (نعم/لا/جزئياً): ").strip(),
        "ملاحظات": input("ملاحظات: ").strip()
    }
    
    data["مشاريع"].append(project)
    save_projects(data)
    print(f"تم إنشاء المشروع: {project['id']}")

def update_project():
    data = load_projects()
    proj_id = input("رقم المشروع: ").strip()
    
    for proj in data["مشاريع"]:
        if proj["id"] == proj_id:
            print(f"الحالة الحالية: {proj['الحالة']}")
            new_status = input("الحالة الجديدة (جديد/مونتاج/مراجعة/تعديل/مكتمل/منشور): ").strip()
            proj["الحالة"] = new_status
            proj["ملاحظات"] = input("ملاحظات: ").strip()
            save_projects(data)
            print(f"تم التحديث: {proj_id} → {new_status}")
            return
    
    print("المشروع غير موجود")

def show_active():
    data = load_projects()
    active = [p for p in data["مشاريع"] if p["الحالة"] not in ["مكتمل", "منشور"]]
    
    if not active:
        print("لا توجد مشاريع نشطة")
        return
    
    print(f"\n=== المشاريع النشطة ({len(active)}) ===")
    for p in sorted(active, key=lambda x: x["الموعد_النهائي"]):
        print(f"  {p['id']} | {p['العنوان'][:30]} | {p['النوع']} | {p['المنصة_المستهدفة']} | موعد: {p['الموعد_النهائي']} | {p['الحالة']}")

if __name__ == "__main__":
    print("1. مشروع جديد\n2. تحديث حالة\n3. عرض النشطة")
    choice = input("اختر: ").strip()
    if choice == "1":
        add_project()
    elif choice == "2":
        update_project()
    elif choice == "3":
        show_active()

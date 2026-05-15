import json
from datetime import datetime

QUEUE_FILE = "content_queue.json"

def load_queue():
    try:
        with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"طوابير": []}

def save_queue(data):
    with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_content():
    data = load_queue()
    print("=== إضافة محتوى للطابور ===")
    
    item = {
        "id": f"C{datetime.now().strftime('%Y%m%d%H%M')}",
        "التاريخ": datetime.now().strftime("%Y-%m-%d"),
        "العنوان": input("العنوان: ").strip(),
        "النوع": input("النوع (تغريدة/سيناريو/مقال/بيان_صحفي/وصف_فيديو): ").strip(),
        "المنصة": input("المنصة المستهدفة: ").strip(),
        "الجهة_الطالبة": input("الجهة الطالبة: ").strip(),
        "الموعد_النهائي": input("الموعد النهائي (YYYY-MM-DD): ").strip(),
        "الأولوية": input("الأولوية (عاجل/عالي/عادي): ").strip(),
        "الحالة": "قيد_الكتابة",
        "عدد_الكلمات": 0,
        "ملاحظات": input("ملاحظات: ").strip()
    }
    
    data["طوابير"].append(item)
    save_queue(data)
    print(f"تم الإضافة: {item['id']} | موعد: {item['الموعد_النهائي']}")

def update_content():
    data = load_queue()
    item_id = input("رقم المحتوى: ").strip()
    
    for item in data["طوابير"]:
        if item["id"] == item_id:
            print(f"الحالة: {item['الحالة']} | كلمات: {item['عدد_الكلمات']}")
            item["الحالة"] = input("الحالة الجديدة (قيد_الكتابة/مراجعة/مكتمل/منشور): ").strip()
            words = input("عدد الكلمات (اتركه فارغاً إذا لم يتغير): ").strip()
            if words:
                item["عدد_الكلمات"] = int(words)
            save_queue(data)
            print(f"تم التحديث: {item_id}")
            return
    
    print("غير موجود")

def show_queue():
    data = load_queue()
    active = [i for i in data["طوابير"] if i["الحالة"] not in ["منشور", "ملغي"]]
    
    if not active:
        print("الطابور فارغ")
        return
    
    print(f"\n=== طابور المحتوى ({len(active)}) ===")
    for i in sorted(active, key=lambda x: x["الموعد_النهائي"]):
        print(f"  {i['id']} | {i['النوع']} | {i['العنوان'][:25]} | {i['المنصة']} | موعد: {i['الموعد_النهائي']} | {i['الحالة']}")

if __name__ == "__main__":
    print("1. إضافة محتوى\n2. تحديث حالة\n3. عرض الطابور")
    choice = input("اختر: ").strip()
    if choice == "1":
        add_content()
    elif choice == "2":
        update_content()
    elif choice == "3":
        show_queue()

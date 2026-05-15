import json
from datetime import datetime, timedelta

SCHEDULE_FILE = "content_schedule.json"

def load_schedule():
    try:
        with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"المنشورات": []}

def save_schedule(data):
    with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_post():
    data = load_schedule()
    print("=== إضافة منشور مجدول ===")
    
    post = {
        "id": f"P{datetime.now().strftime('%Y%m%d%H%M')}",
        "التاريخ": input("تاريخ النشر (YYYY-MM-DD): ").strip(),
        "الوقت": input("وقت النشر (HH:MM): ").strip(),
        "المنصة": input("المنصة (Twitter/Instagram/TikTok/YouTube/LinkedIn): ").strip(),
        "النوع": input("النوع (خبر/ترفيهي/كواليس/تعليمي/علامة تجارية/مجتمعي): ").strip(),
        "العنوان": input("العنوان: ").strip(),
        "النص": input("النص: ").strip(),
        "الوسائط": input("نوع الوسائط (صورة/فيديو/ستوري/ريلز): ").strip(),
        "الحالة": "مجدول",
        "Hashtags": input("Hashtags: ").strip(),
        "ملاحظات": input("ملاحظات: ").strip()
    }
    
    data["المنشورات"].append(post)
    save_schedule(data)
    print(f"تم جدولة المنشور: {post['id']} | {post['التاريخ']} {post['الوقت']} | {post['المنصة']}")

def view_week():
    data = load_schedule()
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    
    print(f"\n=== جدول الأسبوع ({week_start.strftime('%Y-%m-%d')}) ===")
    
    for i in range(7):
        day = week_start + timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        day_name = ["الاثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت","الأحد"][i]
        
        posts = [p for p in data["المنشورات"] if p["التاريخ"] == day_str]
        print(f"\n{day_name} ({day_str}):")
        
        if not posts:
            print("  لا توجد منشورات")
        for p in posts:
            print(f"  {p['الوقت']} | {p['المنصة']} | {p['النوع']} | {p['العنوان']} | {p['الحالة']}")

def mark_published():
    data = load_schedule()
    post_id = input("رقم المنشور: ").strip()
    
    for post in data["المنشورات"]:
        if post["id"] == post_id:
            post["الحالة"] = "منشور"
            save_schedule(data)
            print(f"تم تحديث: {post_id} → منشور")
            return
    
    print("المنشور غير موجود")

if __name__ == "__main__":
    print("1. إضافة منشور\n2. عرض الأسبوع\n3. تحديث كمنشور")
    choice = input("اختر: ").strip()
    if choice == "1":
        add_post()
    elif choice == "2":
        view_week()
    elif choice == "3":
        mark_published()

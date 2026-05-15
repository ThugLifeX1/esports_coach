import json
from datetime import datetime, timedelta

def generate_tournament_calendar(months_ahead=3):
    start_date = datetime.now()
    end_date = start_date + timedelta(days=30 * months_ahead)
    
    calendar = {
        "التقويم_التنافسي": {
            "الفريق": "PUBGM_TEAM",
            "تاريخ_الإنشاء": datetime.now().strftime("%Y-%m-%d"),
            "الفترة": {
                "من": start_date.strftime("%Y-%m-%d"),
                "إلى": end_date.strftime("%Y-%m-%d")
            },
            "البطولات": [],
            "المواعيد_المهمة": []
        }
    }
    
    print(f"=== إنشاء تقويم تنافسي ({months_ahead} أشهر) ===")
    print(f"الفترة: {start_date.strftime('%Y-%m-%d')} إلى {end_date.strftime('%Y-%m-%d')}")
    
    while True:
        print("\n--- إضافة بطولة ---")
        name = input("اسم البطولة (أو 'تم' للإنهاء): ").strip()
        if name == "تم" or not name:
            break
        
        tournament = {
            "الاسم": name,
            "المنظم": input("المنظم: ").strip(),
            "تاريخ_البداية": input("تاريخ البداية (YYYY-MM-DD): ").strip(),
            "تاريخ_النهاية": input("تاريخ النهاية (YYYY-MM-DD): ").strip(),
            "الموقع": input("الموقع (مدينة/دولة/أونلاين): ").strip(),
            "الجائزة": input("إجمالي الجائزة: ").strip(),
            "الأولوية": input("الأولوية (S/A/B/C/D): ").strip().upper(),
            "موعد_التسجيل_النهائي": input("موعد التسجيل النهائي: ").strip(),
            "الحالة": "مخطط",
            "ملاحظات": input("ملاحظات: ").strip()
        }
        
        calendar["التقويم_التنافسي"]["البطولات"].append(tournament)
    
    filename = f"tournament_calendar_{start_date.strftime('%Y%m%d')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(calendar, f, ensure_ascii=False, indent=2)
    
    print(f"\nتم إنشاء التقويم: {filename}")
    print(f"عدد البطولات: {len(calendar['التقويم_التنافسي']['البطولات'])}")

if __name__ == "__main__":
    generate_tournament_calendar()

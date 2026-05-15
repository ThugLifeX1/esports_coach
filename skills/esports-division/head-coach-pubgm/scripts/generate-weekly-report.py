import json
from datetime import datetime, timedelta

def generate_weekly_report(team_name, week_start=None):
    if not week_start:
        week_start = datetime.now()
    
    week_end = week_start + timedelta(days=6)
    
    report = {
        "تقرير_أسبوعي": {
            "الفريق": team_name,
            "الفترة": {
                "من": week_start.strftime("%Y-%m-%d"),
                "إلى": week_end.strftime("%Y-%m-%d")
            },
            "المدرب": "",
            "ملخص_الأداء": {
                "سجل_السكريمات": {"فوز": 0, "خسارة": 0},
                "نتائج_البطولات": [],
                "مؤشرات_الفريق": {
                    "متوسط_KD": 0.0,
                    "متوسط_الضرر": 0,
                    "نسبة_البقاء": "0%",
                    "متوسط_الترتيب": 0
                }
            },
            "تقييم_اللاعبين": [],
            "الإنجازات": [],
            "التحديات": [],
            "خطة_الأسبوع_القادم": {
                "الأهداف": [],
                "التركيز_التكتيكي": "",
                "البطولات_القادمة": []
            },
            "ملاحظات_المدرب": "",
            "التوقيع": "",
            "التاريخ": datetime.now().strftime("%Y-%m-%d")
        }
    }
    
    filename = f"weekly_report_{team_name}_{week_start.strftime('%Y%m%d')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"تم إنشاء التقرير: {filename}")
    return report

if __name__ == "__main__":
    import sys
    team = sys.argv[1] if len(sys.argv) > 1 else "PUBGM_TEAM"
    generate_weekly_report(team)

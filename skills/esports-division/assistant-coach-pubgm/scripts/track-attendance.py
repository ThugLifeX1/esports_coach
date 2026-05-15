import json
from datetime import datetime

def track_attendance(team_name, date=None):
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    players = []
    print(f"=== تتبع حضور فريق {team_name} - {date} ===")
    print("أدخل أسماء اللاعبين (اكتب 'تم' للإنهاء):")
    
    while True:
        name = input("اسم اللاعب: ").strip()
        if name == "تم" or not name:
            break
        
        status = input("الحالة (حاضر/متأخر/غائب/معذور): ").strip()
        notes = input("ملاحظات (اختياري): ").strip()
        
        players.append({
            "الاسم": name,
            "الحالة": status,
            "ملاحظات": notes
        })
    
    record = {
        "الفريق": team_name,
        "التاريخ": date,
        "اللاعبون": players,
        "ملخص": {
            "حاضر": sum(1 for p in players if p["الحالة"] == "حاضر"),
            "متأخر": sum(1 for p in players if p["الحالة"] == "متأخر"),
            "غائب": sum(1 for p in players if p["الحالة"] == "غائب"),
            "معذور": sum(1 for p in players if p["الحالة"] == "معذور")
        }
    }
    
    filename = f"attendance_{team_name}_{date.replace('-', '')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    
    print(f"\nملخص الحضور:")
    print(f"  حاضر: {record['ملخص']['حاضر']}")
    print(f"  متأخر: {record['ملخص']['متأخر']}")
    print(f"  غائب: {record['ملخص']['غائب']}")
    print(f"  معذور: {record['ملخص']['معذور']}")
    print(f"\nتم حفظ السجل: {filename}")

if __name__ == "__main__":
    import sys
    team = sys.argv[1] if len(sys.argv) > 1 else "PUBGM_TEAM"
    track_attendance(team)

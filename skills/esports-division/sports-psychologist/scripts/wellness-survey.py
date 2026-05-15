import json
from datetime import datetime

SURVEY_FILE = "wellness_surveys.json"

def load_surveys():
    try:
        with open(SURVEY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"استبيانات": {}}

def save_surveys(data):
    with open(SURVEY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def take_survey():
    data = load_surveys()
    print("=== استبيان الرفاهية الأسبوعي ===\n")
    
    name = input("اسم اللاعب: ").strip()
    date = datetime.now().strftime("%Y-%m-%d")
    
    questions = [
        ("مستوى الطاقة العام", "1-10 (1=منهك, 10=مفعم)"),
        ("جودة النوم", "1-10 (1=سيئ جداً, 10=ممتاز)"),
        ("مستوى التوتر", "1-10 (1=مرتاح, 10=شديد التوتر)"),
        ("الحماس للتدريب", "1-10 (1=لا رغبة, 10=متحمس جداً)"),
        ("الرضا عن الأداء", "1-10 (1=غير راضٍ, 10=راضٍ جداً)"),
        ("جودة التواصل مع الفريق", "1-10 (1=سيئ, 10=ممتاز)"),
        ("الشعور بالإرهاق", "1-10 (1=لا إرهاق, 10=احتراق)"),
        ("الثقة بالنفس", "1-10 (1=منخفضة, 10=عالية جداً)"),
        ("التوازن بين اللعب والحياة", "1-10 (1=لا توازن, 10=متوازن)"),
        ("الحالة المزاجية العامة", "1-10 (1=كئيب, 10=ممتاز)")
    ]
    
    survey = {
        "التاريخ": date,
        "الإجابات": {},
        "المعدل_الكلي": 0,
        "مستوى_الخطر": "",
        "ملاحظات": ""
    }
    
    total = 0
    for question, scale in questions:
        answer = int(input(f"{question} ({scale}): ").strip() or "5")
        answer = max(1, min(10, answer))
        survey["الإجابات"][question] = answer
        total += answer
    
    avg = total / len(questions)
    survey["المعدل_الكلي"] = round(avg, 1)
    
    if avg >= 7.5:
        survey["مستوى_الخطر"] = "طبيعي"
    elif avg >= 5.5:
        survey["مستوى_الخطر"] = "انتباه"
    elif avg >= 4.0:
        survey["مستوى_الخطر"] = "تنبيه"
    else:
        survey["مستوى_الخطر"] = "خطر - تدخل فوري"
    
    survey["ملاحظات"] = input("ملاحظات إضافية (اختياري): ").strip()
    
    if name not in data["استبيانات"]:
        data["استبيانات"][name] = []
    data["استبيانات"][name].append(survey)
    save_surveys(data)
    
    print(f"\nالمعدل الكلي: {survey['المعدل_الكلي']}/10")
    print(f"مستوى الخطر: {survey['مستوى_الخطر']}")

def show_trends():
    data = load_surveys()
    if not data["استبيانات"]:
        print("لا توجد بيانات")
        return
    
    print("\n=== اتجاهات الرفاهية ===")
    for name, surveys in data["استبيانات"].items():
        if len(surveys) >= 2:
            latest = surveys[-1]["المعدل_الكلي"]
            previous = surveys[-2]["المعدل_الكلي"]
            trend = "▲" if latest > previous else ("▼" if latest < previous else "→")
            print(f"  {name}: {latest}/10 {trend} (سابق: {previous}) | مستوى: {surveys[-1]['مستوى_الخطر']}")
        else:
            print(f"  {name}: {surveys[0]['المعدل_الكلي']}/10 | مستوى: {surveys[0]['مستوى_الخطر']}")

if __name__ == "__main__":
    print("1. إجراء استبيان\n2. عرض الاتجاهات")
    choice = input("اختر: ").strip()
    if choice == "1":
        take_survey()
    elif choice == "2":
        show_trends()

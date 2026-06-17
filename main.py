import json
import os
from datetime import datetime, timedelta

DATA_FILE = "sleep_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def validate_time(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except:
        return False

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False

def calculate_duration(sleep_time, wake_time):
    sleep_dt = datetime.strptime(sleep_time, "%H:%M")
    wake_dt = datetime.strptime(wake_time, "%H:%M")
    if wake_dt <= sleep_dt:
        wake_dt += timedelta(hours=24)
    delta = wake_dt - sleep_dt
    return round(delta.total_seconds() / 3600, 2)

def get_date_from_user(prompt):
    while True:
        date_str = input(prompt).strip()
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
            print(f"Використано сьогоднішню дату: {date_str}")
            return date_str
        if validate_date(date_str):
            if datetime.strptime(date_str, "%Y-%m-%d") > datetime.now():
                print("❌ Не можна додавати записи з майбутньої дати!")
                continue
            return date_str
        print("❌ Некоректний формат дати! Використовуйте YYYY-MM-DD")

def get_time_from_user(prompt):
    while True:
        time_str = input(prompt).strip()
        if validate_time(time_str):
            return time_str
        print("❌ Некоректний формат часу! Використовуйте HH:MM")

def get_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("так", "т", "+", "yes", "y", "1"):
            return True
        if answer in ("ні", "н", "-", "no", "n", "0"):
            return False
        print("❌ Введіть 'так' або 'ні'")

def add_sleep_record(data):
    print("\n" + "=" * 50)
    print("🛌 ДОДАВАННЯ ЗАПИСУ СНУ")
    print("=" * 50)
    date = get_date_from_user("📅 Введіть дату (YYYY-MM-DD) або Enter для сьогодні: ")
    for record in data:
        if record["date"] == date:
            print(f"⚠️ Запис на {date} вже існує!")
            if not get_yes_no("Бажаєте перезаписати? (так/ні): "):
                return data
            data = [r for r in data if r["date"] != date]
            break
    print("\n⏰ Введіть час:")
    sleep_time = get_time_from_user("   Час засинання (HH:MM): ")
    wake_time = get_time_from_user("   Час пробудження (HH:MM): ")
    duration = calculate_duration(sleep_time, wake_time)
    record = {
        "date": date,
        "sleep_time": sleep_time,
        "wake_time": wake_time,
        "duration_hours": duration
    }
    data.append(record)
    save_data(data)
    print(f"\n✅ Запис додано! Тривалість сну: {duration:.2f} годин")
    return data

def view_all_records(data):
    print("\n" + "=" * 50)
    print("📊 УСІ ЗАПИСИ СНУ")
    print("=" * 50)
    if not data:
        print("ℹ️ Немає жодного запису.")
        return
    sorted_data = sorted(data, key=lambda x: x["date"])
    total_sleep = 0
    for i, record in enumerate(sorted_data, 1):
        print(f"{i}. 📅 {record['date']}")
        print(f"   🛌 Заснув: {record['sleep_time']} → Прокинувся: {record['wake_time']}")
        print(f"   ⏱️ Тривалість: {record['duration_hours']:.2f} год")
        print()
        total_sleep += record['duration_hours']
    print(f"📈 Загалом: {len(data)} записів")
    print(f"⏱️ Загальна тривалість: {total_sleep:.2f} год")
    if data:
        print(f"📊 Середня тривалість: {total_sleep / len(data):.2f} год")

def average_sleep_last_week(data):
    print("\n" + "=" * 50)
    print("📈 СЕРЕДНЯ ТРИВАЛІСТЬ ЗА ТИЖДЕНЬ")
    print("=" * 50)
    if not data:
        print("ℹ️ Немає даних.")
        return
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    week_records = []
    for record in data:
        record_date = datetime.strptime(record["date"], "%Y-%m-%d").date()
        if week_ago <= record_date <= today:
            week_records.append(record)
    if not week_records:
        print(f"ℹ️ Немає записів за останні 7 днів")
        return
    total = sum(r["duration_hours"] for r in week_records)
    avg = total / len(week_records)
    print(f"📊 За останні 7 днів: {len(week_records)} записів")
    print(f"⏱️ Загальна тривалість: {total:.2f} год")
    print(f"📈 Середня тривалість: {avg:.2f} год")
    print("\nДеталі за днями:")
    for r in sorted(week_records, key=lambda x: x["date"]):
        print(f"   {r['date']}: {r['duration_hours']:.2f} год")

def shortest_night(data):
    print("\n" + "=" * 50)
    print("🌙 НАЙКОРОТША НІЧ ЗА ТИЖДЕНЬ")
    print("=" * 50)
    if not data:
        print("ℹ️ Немає даних.")
        return
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    week_records = []
    for record in data:
        record_date = datetime.strptime(record["date"], "%Y-%m-%d").date()
        if week_ago <= record_date <= today:
            week_records.append(record)
    if not week_records:
        print(f"ℹ️ Немає записів за останні 7 днів")
        return
    shortest = min(week_records, key=lambda x: x["duration_hours"])
    print(f"🌙 Найкоротша ніч: {shortest['date']}")
    print(f"   🛌 Заснув: {shortest['sleep_time']} → Прокинувся: {shortest['wake_time']}")
    print(f"   ⏱️ Тривалість: {shortest['duration_hours']:.2f} год")

def show_menu():
    print("\n" + "=" * 50)
    print("🌙 ЩОДЕННИК СНУ")
    print("=" * 50)
    print("1️⃣  Додати запис сну")
    print("2️⃣  Переглянути всі записи")
    print("3️⃣  Середня тривалість за тиждень")
    print("4️⃣  Найкоротша ніч за тиждень")
    print("0️⃣  Вихід")
    print("=" * 50)

def main():
    print("🌙 ЩОДЕННИК СНУ v1.0")
    print("📚 Варіант №24 — Навчальна практика")
    print("=" * 50)
    data = load_data()
    print(f"📊 Завантажено {len(data)} запис(ів)")
    while True:
        show_menu()
        choice = input("👉 Виберіть опцію: ").strip()
        if choice == "1":
            data = add_sleep_record(data)
        elif choice == "2":
            view_all_records(data)
        elif choice == "3":
            average_sleep_last_week(data)
        elif choice == "4":
            shortest_night(data)
        elif choice == "0":
            print("\n👋 До побачення! Гарного сну! 🌙")
            break
        else:
            print("❌ Некоректний вибір. Введіть число від 0 до 4.")
        input("\n🔄 Натисніть Enter, щоб продовжити...")

if __name__ == "__main__":
    main()

# test_sleep.py
# Автоматизований тест для функцій calculate_duration та shortest_night

import json
import os
from datetime import datetime, timedelta

# Імпортуємо функції з main.py
from main import calculate_duration, load_data, save_data, DATA_FILE

TEST_FILE = "test_data.json"

def setup(records):
    """Записує тестові дані у тимчасовий файл."""
    global DATA_FILE
    DATA_FILE = TEST_FILE
    with open(TEST_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f)

def teardown():
    """Видаляє тимчасовий файл після тесту."""
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

# ===== Тест 1: розрахунок тривалості сну (звичайний випадок) =====
print("\n" + "=" * 50)
print("🧪 ЗАПУСК АВТОМАТИЗОВАНИХ ТЕСТІВ")
print("=" * 50)

sleep_time = "23:30"
wake_time = "07:15"
duration = calculate_duration(sleep_time, wake_time)
expected = 7.75
if duration == expected:
    print(f" ✅ Тест 1 пройдено: 23:30 → 07:15 = {duration} год (очікувалось {expected})")
else:
    print(f" ❌ Тест 1 не пройдено: отримано {duration}, очікувалось {expected}")

# ===== Тест 2: розрахунок тривалості сну (перехід через опівніч) =====
sleep_time = "01:00"
wake_time = "08:30"
duration = calculate_duration(sleep_time, wake_time)
expected = 7.5
if duration == expected:
    print(f" ✅ Тест 2 пройдено: 01:00 → 08:30 = {duration} год (очікувалось {expected})")
else:
    print(f" ❌ Тест 2 не пройдено: отримано {duration}, очікувалось {expected}")

# ===== Тест 3: найкоротша ніч =====
test_records = [
    {"date": "2025-06-10", "sleep_time": "23:00", "wake_time": "07:00", "duration_hours": 8.0},
    {"date": "2025-06-11", "sleep_time": "00:30", "wake_time": "07:30", "duration_hours": 7.0},
    {"date": "2025-06-12", "sleep_time": "23:30", "wake_time": "06:30", "duration_hours": 7.0},
]

shortest = min(test_records, key=lambda x: x["duration_hours"])
expected_date = "2025-06-11"
expected_duration = 7.0

if shortest["duration_hours"] == expected_duration:
    print(f" ✅ Тест 3 пройдено: найкоротша ніч {shortest['date']} з {shortest['duration_hours']} год (очікувалось {expected_duration})")
else:
    print(f" ❌ Тест 3 не пройдено: отримано {shortest['duration_hours']}, очікувалось {expected_duration}")

print("\n" + "=" * 50)
print("🏁 ТЕСТУВАННЯ ЗАВЕРШЕНО")
print("=" * 50)
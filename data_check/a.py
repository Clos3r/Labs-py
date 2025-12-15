import pandas as pd
from pathlib import Path
import unittest

BASE_DIR = Path(__file__).parent  
files = {
    "users": BASE_DIR / "users.csv",
    "orders": BASE_DIR / "orders.csv"
}


def load_data(files):
    return {name: pd.read_csv(str(path)) for name, path in files.items()}


def check_foreign_key(df_left, df_right, left_key, right_key):
    invalid = df_left[~df_left[left_key].isin(df_right[right_key])]
    report = []
    for _, row in invalid.iterrows():
        report.append({
            "type": "foreign_key",
            "column": left_key,
            "value": row[left_key],
            "message": f"{left_key} не знайдено в {right_key}"
        })
    return report

def generate_report(issues):
    return pd.DataFrame(issues)


class TestDataCheck(unittest.TestCase):
    def test_foreign_key(self):
        users = pd.DataFrame({"id": [1,2]})
        orders = pd.DataFrame({"user_id": [1,3]})
        issues = check_foreign_key(orders, users, "user_id", "id")
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["value"], 3)

if __name__ == "__main__":
    print("Поточна робоча директорія:", Path().resolve())
    data = load_data(files)
    issues = check_foreign_key(data["orders"], data["users"], "user_id", "id")


    report = generate_report(issues)
    report_path = BASE_DIR / "report.csv"
    report.to_csv(report_path, index=False)

    print("✔ Перевірка виконана")
    print(f"✔ Звіт збережено у {report_path}")

    unittest.main(argv=[""], exit=False)

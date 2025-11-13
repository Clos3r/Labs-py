class JunkItem:
    def __init__(self, name: str, quantity: int, value: float):
        self.name = name
        self.quantity = quantity
        self.value = value

    def __repr__(self):
        return f"JunkItem(name='{self.name}', quantity={self.quantity}, value={self.value})"


class JunkStorage:
    @staticmethod
    def serialize(items: list, filename: str):
        with open(filename, "w", encoding="utf-8") as file:
            for item in items:
                value_str = str(item.value).replace('.', ',')
                line = f"{item.name}|{item.quantity}|{value_str}\n"
                file.write(line)

    @staticmethod
    def parse(filename: str) -> list:
        items = []
        with open(filename, "r", encoding="utf-8") as file:
            for i, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    print(f"[УВАГА] Рядок {i} пошкоджений — пропущено: {line}")
                    continue
                name, quantity_str, value_str = parts
                value_str = value_str.replace(',', '.')
                try:
                    quantity = int(quantity_str)
                    value = float(value_str)
                except ValueError:
                    print(f"[УВАГА] Рядок {i} має некоректні дані — пропущено: {line}")
                    continue
                items.append(JunkItem(name, quantity, value))
        return items


items = [
    JunkItem("Бляшанка", 5, 2.5),
    JunkItem("Стара плата", 3, 7.8),
    JunkItem("Купка дротів", 10, 1.2),
]

filename = "junk_storage.txt"
JunkStorage.serialize(items, filename)
print(f"Дані записано у файл: {filename}")

with open(filename, "a", encoding="utf-8") as f:
    f.write("поганий|рядок\n")
    f.write("Ще один|abc|1,5\n")

parsed_items = JunkStorage.parse(filename)

print("\nВміст після зчитування:")
for obj in parsed_items:
    print(obj)

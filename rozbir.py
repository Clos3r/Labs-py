from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import csv

@dataclass(order=True)
class Item:
    category: str
    value: float
    name: str = field(compare=False)
    quantity: int = field(compare=False)
    condition: str = field(compare=False)
    location: str = field(compare=False)
    added_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"), compare=False)

    def total_value(self) -> float:
        return self.quantity * self.value

    def __str__(self) -> str:
        return f"[{self.category}] {self.name} ({self.quantity} шт.) — {self.value} грн/шт, стан: {self.condition}"

@dataclass
class Inventory:
    items: List[Item] = field(default_factory=list)

    def add_item(self, item: Item):
        self.items.append(item)
        self.items.sort()

    def remove_item(self, name: str):
        self.items = [item for item in self.items if item.name != name]

    def find_by_category(self, category: str) -> List[Item]:
        return [item for item in self.items if item.category == category]

    def total_inventory_value(self) -> float:
        return sum(item.total_value() for item in self.items)

    def save_to_csv(self, filename: str):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "category", "quantity", "value", "condition", "location", "added_date"])
            for item in self.items:
                writer.writerow([item.name, item.category, item.quantity, item.value, item.condition, item.location, item.added_date])

    def load_from_csv(self, filename: str):
        with open(filename, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.items = []
            for row in reader:
                self.items.append(Item(
                    name=row["name"],
                    category=row["category"],
                    quantity=int(row["quantity"]),
                    value=float(row["value"]),
                    condition=row["condition"],
                    location=row["location"],
                    added_date=row.get("added_date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                ))
        self.items.sort()

    def export_summary(self):
        summary = {}
        for item in self.items:
            summary[item.category] = summary.get(item.category, 0) + item.quantity
        print("Короткий звіт по категоріях:")
        for cat, qty in summary.items():
            print(f"{cat}: {qty} шт.")

    def filter_items(self, 
                     name: Optional[str] = None,
                     category: Optional[str] = None,
                     min_quantity: Optional[int] = None,
                     max_quantity: Optional[int] = None,
                     min_value: Optional[float] = None,
                     max_value: Optional[float] = None,
                     condition: Optional[str] = None,
                     location: Optional[str] = None) -> List[Item]:
        result = self.items
        if name is not None:
            result = [i for i in result if name.lower() in i.name.lower()]
        if category is not None:
            result = [i for i in result if i.category == category]
        if min_quantity is not None:
            result = [i for i in result if i.quantity >= min_quantity]
        if max_quantity is not None:
            result = [i for i in result if i.quantity <= max_quantity]
        if min_value is not None:
            result = [i for i in result if i.value >= min_value]
        if max_value is not None:
            result = [i for i in result if i.value <= max_value]
        if condition is not None:
            result = [i for i in result if i.condition == condition]
        if location is not None:
            result = [i for i in result if i.location == location]
        return sorted(result)

if __name__ == "__main__":
    inv = Inventory()

    inv.add_item(Item(name="Гаєчний ключ", category="інструменти", quantity=3, value=5.0, condition="уживаний", location="гараж"))
    inv.add_item(Item(name="Старий ноутбук", category="електроніка", quantity=1, value=2000.0, condition="зламаний", location="комора"))
    inv.add_item(Item(name="Молоток", category="інструменти", quantity=2, value=10.0, condition="новий", location="гараж"))

    print("=== Весь інвентар ===")
    for item in inv.items:
        print(item)

    print("\n=== Короткий звіт ===")
    inv.export_summary()

    print(f"\nЗагальна вартість: {inv.total_inventory_value()} грн")

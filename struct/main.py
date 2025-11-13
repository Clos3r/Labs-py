from models import Antibiotic, Vitamin, Vaccine


def show_info(medicines):
    """Поліморфна функція — жодних if!"""
    for med in medicines:
        print(med.info())


if __name__ == "__main__":
    medicines = [
        Antibiotic("Амоксицилін", 20, 5.5),
        Vitamin("Вітамін C", 50, 1.2),
        Vaccine("Щеплення від грипу", 10, 15.0),
    ]

    show_info(medicines)

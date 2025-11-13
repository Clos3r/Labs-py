from abc import ABC, abstractmethod


class Medicine(ABC):
    def __init__(self, name: str, quantity: int, price: float):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not isinstance(quantity, int):
            raise TypeError("quantity must be an integer")
        if not isinstance(price, (float, int)):
            raise TypeError("price must be a number")

        self.name = name
        self.quantity = quantity
        self.price = float(price)

    @abstractmethod
    def requires_prescription(self) -> bool:
        """Чи потрібен рецепт"""
        pass

    @abstractmethod
    def storage_requirements(self) -> str:
        """Умови зберігання"""
        pass

    def total_price(self) -> float:
        """Загальна вартість"""
        return self.quantity * self.price

    @abstractmethod
    def info(self) -> str:
        """Інформація про препарат"""
        pass


class Antibiotic(Medicine):
    def requires_prescription(self) -> bool:
        return True

    def storage_requirements(self) -> str:
        return "8–15°C, темне місце"

    def info(self) -> str:
        return (f"[Антибіотик] {self.name}: кількість={self.quantity}, ціна={self.price:.2f}, "
                f"загальна={self.total_price():.2f}, рецепт потрібен={self.requires_prescription()}, "
                f"зберігати: {self.storage_requirements()}")


class Vitamin(Medicine):
    def requires_prescription(self) -> bool:
        return False

    def storage_requirements(self) -> str:
        return "15–25°C, сухо"

    def info(self) -> str:
        return (f"[Вітамін] {self.name}: кількість={self.quantity}, ціна={self.price:.2f}, "
                f"загальна={self.total_price():.2f}, рецепт потрібен={self.requires_prescription()}, "
                f"зберігати: {self.storage_requirements()}")


class Vaccine(Medicine):
    def requires_prescription(self) -> bool:
        return True

    def storage_requirements(self) -> str:
        return "2–8°C, холодильник"

    def total_price(self) -> float:
        """Вакцина має +10% до вартості"""
        base_total = super().total_price()
        return base_total * 1.10

    def info(self) -> str:
        return (f"[Вакцина] {self.name}: кількість={self.quantity}, ціна={self.price:.2f}, "
                f"загальна={self.total_price():.2f}, рецепт потрібен={self.requires_prescription()}, "
                f"зберігати: {self.storage_requirements()}")

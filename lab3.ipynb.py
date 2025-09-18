def calculator():
    num1 = float(input("Введіть перше число: "))
    operator = input("Введіть оператор (+, -, *, /): ")
    
    num2 = float(input("Введіть друге число: "))
    
    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1 * num2
    elif operator == '/':
        if num2 != 0:
            result = num1 / num2
        else:
            result = "Помилка: ділення на нуль!"
    else:
        result = "Невідомий оператор!"
    
    print(f"Результат: {result}")

calculator()

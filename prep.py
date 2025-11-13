def check_medicines(medicines):
    for medicine in medicines:
        if type(medicine['quantity']) != int:
            print(medicine['name'] + ": Data error")
            continue
        
        if type(medicine['temperature']) != float:
            print(medicine['name'] + ": Data error")
            continue
        
        if medicine['temperature'] < 5:
            temperature_status = "Too cold"
        elif medicine['temperature'] > 25:
            temperature_status = "Too hot"
        else:
            temperature_status = "Normal"
        
        match medicine['category']:
            case 'antibiotic':
                category_status = "Prescription drug"
            case 'vitamin':
                category_status = "Over-the-counter"
            case 'vaccine':
                category_status = "Requires special storage"
            case _:
                category_status = "Unknown category"
        
        print(medicine['name'] + ": " + category_status + ", " + temperature_status)


medicines = [
    {"name": "Amoxicillin", "quantity": 100, "category": "antibiotic", "temperature": 4.0},
    {"name": "Vitamin C", "quantity": 200, "category": "vitamin", "temperature": 10.5},
    {"name": "Flu Vaccine", "quantity": 50, "category": "vaccine", "temperature": 2.0},

    {"name": "Biotin", "quantity": "not specified", "category": "vitamin", "temperature": 22.0},
    {"name": "Unknown Drug", "quantity": 30, "category": "unknown", "temperature": 30.0}
]

check_medicines(medicines)

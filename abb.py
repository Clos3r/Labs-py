def shadow(limit=200):
    def decorator(gen_func):
        def wrapper(*args, **kwargs):
            total = 0
            triggered = False

            for event in gen_func(*args, **kwargs):
                print(event)


                parts = event.split()
                if len(parts) != 2:
                    continue
                try:
                    amount = float(parts[1])
                except ValueError:
                    continue

                total += amount

                if not triggered and total > limit:
                    print("Тіньовий ліміт перевищено. Активую схему")
                    triggered = True

                yield event

            return total
        return wrapper
    return decorator


@shadow(limit=200)
def transactions():
    yield from [
        "payment 120",
        "refund 50",
        "junk data",
        "transfer 300",
        "bad xx",
    ]


g = transactions()

try:
    for _ in g:
        pass
except StopIteration as e:
    print("Фінальна сума:", e.value)

price = float(input("Введите цену: "))
discount_percent = float(input("Введите скидку (%): "))

final_price = price * (1 - discount_percent / 100)

print(f"Цена со скидкой: {final_price:.2f} ру276б.")
price = 1000
discount_percent = 25

final_price = price * (1 - discount_percent / 100)
print(f"Цена со скидкой: {final_price:.2f} руб.")

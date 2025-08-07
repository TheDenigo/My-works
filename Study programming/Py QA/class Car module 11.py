class Car:
    def __init__(self, model, year, engine_volume, price, mileage):
        self.model = model
        self.year = year
        self.engine_volume = engine_volume
        self.price = price
        self.mileage = mileage
        self.wheels = 4

    def description(self):
        return (f"Модель: {self.model}, "
                f"Год выпуска: {self.year}, "
                f"Объем двигателя: {self.engine_volume} л, "
                f"Цена: {self.price} руб., "
                f"Пробег: {self.mileage} км, "
                f"Количество колес: {self.wheels}")

car_instance = Car("Toyota Camry", 2020, 2.5, 2000000, 15000)

print(car_instance.description())


class Truck(Car):
    def __init__(self, model, year, engine_volume, price, mileage):
        super().__init__(model, year, engine_volume, price, mileage)
        self.wheels = 8

truck_instance = Truck("Kamaz", 2018, 7.0, 3500000, 30000)

print(truck_instance.description())
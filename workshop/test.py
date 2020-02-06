from models import HousePricingPrediction

model = HousePricingPrediction()
house_data = [4.0, 2.25, 2410.0, 4250.0, 1.5, 1460.0, 950.0, 1929.0]

print(model.predict(house_data))

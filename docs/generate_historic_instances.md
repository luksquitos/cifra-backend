# Code to generate historic instances

```python
from datetime import datetime, timedelta
from random import uniform, random
import json


def generate_price(price: float):
    # Will generate a random price based on
    price = float(price)
    lower = 0.6 * price
    higher = 1.6 * price

    number = uniform(lower, higher)

    return round(number, 2)

def generate_datetime(min_year=2019, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random()


file = open("products.json")
products = json.load(file)
file.close()


model = "stores.priceproducthistory"
instances = []
pk = 1

for product in products:
    p_pk = product["pk"]
    p_price = product["fields"]["price"]
    for _ in range(10): # Quantidade de instâncias de histórico
        instances.append(
            {
                "model": model,
                "pk": pk,
                "fields": {
                    "product": p_pk,
                    "price": str(generate_price(p_price)),
                    "created_at": f"{str(generate_datetime())}-03:00"
                }
            }
        )
        pk += 1


with open("historic.json", "w") as historic_json:
    json.dump(instances, historic_json)

```

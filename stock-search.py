import requests as r
import lxml.html
import json
import urllib
import csv
import sys
from time import time
import concurrent.futures
from dataclasses import dataclass, asdict
import itertools


STATES_ROOT='https://www.vw.com/app/dccsearch/vw-us/en/Detailed%20information%20about%20the%20selected%20Volkswagen%20dealer'
INVENTORY_ROOT='https://prod.services.ngw6apps.io/sdl'
WORKER_COUNT=15

@dataclass(frozen=True)
class Dealer:
    id: str
    name: str
    address: dict
    contact: dict
    lat: float
    lon: float

@dataclass(frozen=True)
class Vehicle:
    model: str
    year: str
    vin: str
    trim: str
    exteriorColor: str
    interiorColor: str
    msrp: str
    adjustedPrice: str
    type: str
    factoryOrderDate: str
    sold: bool

@dataclass(frozen=True)
class Inventory:
    dealer: Dealer
    vehicles: list

def get_serialized_states(url):
    response = r.get(STATES_ROOT)
    doc = lxml.html.fromstring(response.content)
    
    states = doc.xpath('//script[@type="x-feature-hub/serialized-states"]')[0].text
    statesDecoded = urllib.parse.unquote(states)

    js = json.loads(statesDecoded)
    return json.loads(
        urllib.parse.unquote(js['dccsearch'])
    )

def dealers_from_state(state):
    return [
        Dealer(
            id=d['id'],
            name=d['name'],
            address=d['address'],
            contact=d['contact'],
            lat=d['geoPosition']['coordinates'][0],
            lon=d['geoPosition']['coordinates'][0]
        )
        for d in state['dealers']['all'].values()
    ]
    

def inventory_for_dealer(dealer):
    start = time()
    params = {
        'language': 'en',
        'countryCode': 'US',
        'currency': 'USD',
        'sdlPath': f'/vwsdl/rest/product/dealers/inventory/{dealer.id}.json',
        'serviceConfigsServiceConfig': json.dumps({
            "key": "service-config",
            "urlOrigin": "https://www.vw.com",
            "urlPath":"/en.service-config.json",
            "tenantCommercial": None,
            "tenantPrivate": None,
            "customConfig": None,
            "homePath": None,
            "credentials": {
                "username":"",
                "password":"",
            }
        })
    }

    response = r.get(INVENTORY_ROOT, params=params)
    js = response.json()

    vehicles = [
        Vehicle(
            model = item['model'],
            year = item['modelYear'],
            vin = item['vin'],
            trim = item['trimLevel'],
            exteriorColor = item['exteriorColorDescription'],
            interiorColor = item['interiorColorBaseColor'],
            msrp = item['msrp'],
            adjustedPrice = item['adjustedListPrice'],
            type = item['type'],
            factoryOrderDate = item['factoryOrderDate'],
            sold = item['sold']
        )
        for item in js
    ]

    end = time()
    print(f'GET dealer/{dealer.id} ({round(end-start, 2)}s)')
    return Inventory(dealer, vehicles)

def get_inventory(dealers):
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKER_COUNT) as executor:
        return [
            r.result()
            for r in [
                executor.submit(inventory_for_dealer, d)
                for d in dealers
            ]
        ]

def sort_output(x):
    (v, inventory) = x
    return (
        inventory.dealer.address['province'],
        inventory.dealer.address['city'],
        inventory.dealer.name,
        v.model,
        v.trim,
        v.exteriorColor,
        v.interiorColor,
        v.msrp
    )

def run():
    dealers = dealers_from_state(
        get_serialized_states(STATES_ROOT))

    print(f'found {len(dealers)} dealers')

    results = get_inventory(dealers)
    filtered = [
        (v, inventory)
        for inventory in results
        for v in inventory.vehicles
        if v.model == 'ID.4'
    ]

    filtered.sort(key=sort_output)

    writer = csv.writer(sys.stdout)

    for (v, inventory) in filtered:
        writer.writerow([
            inventory.dealer.id,
            inventory.dealer.name,
            inventory.dealer.address['province'],
            inventory.dealer.address['city'],
            inventory.dealer.contact['website'] if 'website' in inventory.dealer.contact else '?',
            v.model,
            v.trim,
            v.exteriorColor,
            v.interiorColor,
            v.msrp,
            v.adjustedPrice,
            v.type,
            v.factoryOrderDate,
            v.sold,
        ])

if __name__ == '__main__':
    run()

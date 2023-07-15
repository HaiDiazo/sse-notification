import json

from service.consume import ConsumeService

with open("test.txt", 'r', newline="") as file:
    reader = file.read().splitlines()
    broker = ConsumeService()
    for data in reader:
        broker.produce(message=json.loads(data))

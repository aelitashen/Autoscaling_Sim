class Packet():
    def __init__(self, payload=1):
        self.arrival_timestamp = None
        self.departure_timestamp = None
        self.payload = payload

    def mark_arrival(self, timestamp):
        self.arrival_timestamp = timestamp

    def mark_departure(self, timestamp):
        self.departure_timestamp = timestamp

    def process(self, time_budget):
        amount = min(time_budget, self.payload)
        self.payload -= amount
        return amount
    
import numpy as np

from packet import Packet
from request_generator import BaseRequestGenerator

class VariableRequestGenerator(BaseRequestGenerator):
    def __init__(self, request_frequency=0.1, fixed_payload=1):
        self.request_frequency = request_frequency
        self.payload = fixed_payload

    def generate_requests(self):
        """Generates a batch of requests
        """
        num_requests_to_generate = np.random.poisson(self.request_frequency)
        return [Packet(self.payload) for _ in range(num_requests_to_generate)]

    
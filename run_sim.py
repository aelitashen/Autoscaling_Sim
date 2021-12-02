from system import AutoScaleSystem
from policy import BasePolicy
from request_generator import BaseRequestGenerator

def sim():
    """Main simulation routine
    """
    # Create policy object for autoscale, evaluation, etc
    policy = BasePolicy()

    # Create request generator object for customizing different request amounts
    # that may or may not change with time
    request_generator = BaseRequestGenerator(0.1, 1)

    # Our main system containing multiple nodes for processing requests
    system = AutoScaleSystem(policy, 4)

    # How long to simulate the system
    time_length = 1000

    while system.timestamp <= time_length:
        # For each step
        # Generate new requests using the generator
        new_requests = request_generator.generate_requests()
        # Step our simulation system
        system.step(new_requests, 1)

    # Report score
    print(system.score)


if __name__ == "__main__":
    sim()
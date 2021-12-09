from system import AutoScaleSystem
from policy import BasePolicy
from no_autoscaling import BaselinePolicy
from threshold_based_policy import ThresholdBasedPolicy
from queueing_based_policy import QueueingBasedPolicy
from prediction_based_policy import PredictionBasedPolicy
from request_generator import BaseRequestGenerator
from variable_request_generator import VariableRequestGenerator

def sim():
    """Main simulation routine
    """
    # Create policy object for autoscale, evaluation, etc
    # policy = BaselinePolicy()
    # policy = ThresholdBasedPolicy()
    # policy = QueueingBasedPolicy()
    policy = PredictionBasedPolicy()

    # Create request generator object for customizing different request amounts
    # that may or may not change with time
    request_generator = VariableRequestGenerator(20, 1)

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
    print(policy.get_total_score())

    policy.plot()


if __name__ == "__main__":
    sim()
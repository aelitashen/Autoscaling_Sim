import numpy as np
from policy import BasePolicy

class ThresholdBasedPolicy(BasePolicy):
    def __init__(self):
        pass

    def evaluate_score(self, evaluation_dict):
        """Defines the policy for evaluating the score of the system state
        """
        score = len(evaluation_dict["completed_requests"])
        score -= evaluation_dict["num_nodes"]

        return score

    def autoscale(self, metrics_dict):
        """Defines the autoscale policy
        """
        new_num_nodes = metrics_dict["num_nodes"]
        print(metrics_dict["usages"])
        
        if np.mean(metrics_dict["usages"]) > 0.8:
            new_num_nodes *= 2

        if np.mean(metrics_dict["usages"]) < 0.6:
            new_num_nodes /= 2

        if new_num_nodes < 1:
            new_num_nodes = 1

        return int(new_num_nodes)

    def get_overhead(self, old_num_nodes, new_num_nodes):
        """Defines the overhead for scaling up/down
        """
        return 0
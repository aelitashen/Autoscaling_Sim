from matplotlib import pyplot as plt
import numpy as np
from policy import BasePolicy

class BaselinePolicy(BasePolicy):
    def __init__(self):
        self.num_nodes = []
        self.completed_throughputs = []
    
    def update_metric(self, evaluation_dict):
        """Defines the policy for evaluating the score of the system state
        """
        self.num_nodes.append(evaluation_dict["num_nodes"])
        self.completed_throughputs.append(len(evaluation_dict["completed_requests"]))

    def autoscale(self, metrics_dict):
        """Defines the autoscale policy, it's fake, does nothing 
        """
        return int(metrics_dict["num_nodes"])

    def get_overhead(self, old_num_nodes, new_num_nodes):
        """Defines the overhead for scaling up/down
        """
        overhead = 0

        # if old_num_nodes > new_num_nodes:
        #     overhead = 0.2

        # if old_num_nodes < new_num_nodes:
        #     overhead = 0.2

        return overhead   
    def get_total_score(self):

        return np.mean(np.array(self.completed_throughputs) / np.array(self.num_nodes))
    def plot(self):
        pass
class BasePolicy():
    def __init__(self):
        pass

    def evaluate_score(self, evaluation_dict):
        """Defines the policy for evaluating the score of the system state
        """
        return len(evaluation_dict["completed_requests"])

    def autoscale(self, metrics_dict):
        """Defines the autoscale policy
        """
        return metrics_dict["num_nodes"]

    def get_overhead(self, old_num_nodes, new_num_nodes):
        """Defines the overhead for scaling up/down
        """
        return max(5, new_num_nodes - old_num_nodes)
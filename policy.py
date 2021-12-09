class BasePolicy():
    def __init__(self):
        pass

    def update_metric(self, evaluation_dict):
        """Defines the policy for evaluating the score of the system state
        """
        pass

    def autoscale(self, metrics_dict):
        """Defines the autoscale policy
        """
        pass

    def get_overhead(self, old_num_nodes, new_num_nodes):
        """Defines the overhead for scaling up/down
        """
        pass

    def get_total_score(self):
        pass
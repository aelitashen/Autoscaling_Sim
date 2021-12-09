from matplotlib import pyplot as plt
import numpy as np
from policy import BasePolicy

class PredictionBasedPolicy(BasePolicy):
    def __init__(self):
        self.num_nodes = []
        self.completed_throughputs = []
        self.queue_length_history = []
        self.num_new_requests = []
        self.cooldown = 5

    def update_metric(self, evaluation_dict):
        """Defines the policy for evaluating the score of the system state
        """
        self.num_nodes.append(evaluation_dict["num_nodes"])
        self.completed_throughputs.append(len(evaluation_dict["completed_requests"]))
        self.num_new_requests.append(evaluation_dict["num_new_incoming_requests"])


    def autoscale(self, metrics_dict):
        new_num_nodes = metrics_dict["num_nodes"]
        avg_queue_length = np.mean(metrics_dict['outstanding_requests'])
        self.queue_length_history.append(avg_queue_length)
        self.queue_length_history = self.queue_length_history[-20:]
        print(self.queue_length_history)

        trend = [self.queue_length_history[i + 1] - self.queue_length_history[i] for i in range(len(self.queue_length_history) - 1)]
        is_upward_trend = np.all(np.array(trend) >= 0)
        if self.cooldown == 0:
            if is_upward_trend:
                self.cooldown = 15
                new_num_nodes *= 2

            is_downward_trend = np.all(np.array(trend) <= 0)
            if is_downward_trend:
                self.cooldown = 15
                new_num_nodes /= 2
            
            if new_num_nodes < 1:
                new_num_nodes = 1
        else:
            self.cooldown -= 1

        return int(new_num_nodes)  

    def get_overhead(self, old_num_nodes, new_num_nodes):
        """Defines the overhead for scaling up/down
        """
        overhead = 0

        if old_num_nodes > new_num_nodes:
            overhead = 2

        if old_num_nodes < new_num_nodes:
            overhead = 2

        return overhead   

    def get_total_score(self):
        return np.mean(np.array(self.completed_throughputs) / np.array(self.num_nodes))

    def plot(self):
        print("PREDICTION_BASED")
        plt.figure()
        num_nodes = self.num_nodes
        num_nodes = [sum(self.num_nodes[i:i+10])// 10 for i in range(0,len(self.num_nodes),10)]
        plt.plot(self.num_nodes, label="#Nodes", color='r')
        for n in num_nodes:
            print(n)
        plt.xlabel('Timestep')
        plt.legend()
        # plt.figure()
        # x_labels = range(0,1000,10)
        # completed_throughputs = self.completed_throughputs 
        # completed_throughputs = [sum(self.completed_throughputs[i:i+10])// 10 for i in range(0,len(self.completed_throughputs),10)]
        # for cthru in completed_throughputs:
        #     print(cthru)
        # plt.plot(x_labels, completed_throughputs[:-1], label="Throughputs", color='b')
        # plt.xlabel('Timestep')
        # plt.legend()
        # plt.show()
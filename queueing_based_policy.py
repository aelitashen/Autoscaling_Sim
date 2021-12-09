from matplotlib import pyplot as plt
import numpy as np
from policy import BasePolicy

class QueueingBasedPolicy(BasePolicy):
    def __init__(self):
        self.num_nodes = []
        self.completed_throughputs = []
        self.num_new_requests = []
        self.cooldown = 5

    def update_metric(self, evaluation_dict):
        """Defines the policy for evaluating the score of the system state
        """
        self.num_nodes.append(evaluation_dict["num_nodes"])
        self.completed_throughputs.append(len(evaluation_dict["completed_requests"]))
        self.num_new_requests.append(evaluation_dict["num_new_incoming_requests"])

    def autoscale(self, metric_dict):
        """Defines the autoscale policy
        """
        new_num_nodes = metric_dict['num_nodes']
        if self.cooldown == 0:
            if np.mean(metric_dict['outstanding_requests']) >= 15:
                self.cooldown = 15
                new_num_nodes *= 2
            elif np.mean(metric_dict['outstanding_requests']) <= 5:
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
        print("QUEUEING_BASED")
        # plt.figure()
        # num_nodes = self.num_nodes
        # num_nodes = [sum(self.num_nodes[i:i+10])// 10 for i in range(0,len(self.num_nodes),10)]
        # plt.plot(self.num_nodes, label="#Nodes", color='r')
        # for n in num_nodes:
        #     print(n)
        # plt.xlabel('Timestep')
        # plt.legend()
        plt.figure()
        x_labels = range(0,1000,10)
        completed_throughputs = self.completed_throughputs 
        completed_throughputs = [sum(self.completed_throughputs[i:i+10])// 10 for i in range(0,len(self.completed_throughputs),10)]
        for cthru in completed_throughputs:
            print(cthru)
        plt.plot(x_labels, completed_throughputs[:-1], label="Throughputs", color='b')
        plt.xlabel('Timestep')
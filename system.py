from node import Node
from math import ceil

class AutoScaleSystem():
    def __init__(self, policy, num_nodes=4):
        """Initialize the system
        """
        # Create the initial nodes and store our policy
        self.nodes = [Node() for _ in range(num_nodes)]
        self.policy = policy
        # Set the current total score to zero
        self.score = 0
        # Set the current system time to zero
        self.timestamp = 0


    @property
    def num_nodes(self):
        """Helper property for getting the number of nodes
        """
        return len(self.nodes)


    def rebalance_requests(self, request_list, num_nodes):
        """Rebalaces requests on each node

        params:
            request_list: a list of requests to be distributed
            num_nodes: the number of nodes available
        """
        rebalanced_list = []

        for i in range(num_nodes):
            # Each node will get num_req_per_node requests
            requests_for_node = [req for req in request_list[i::num_nodes]]
            rebalanced_list.append(requests_for_node)

        return rebalanced_list


    def distribute_requests_to_nodes(self, request_list):
        """Distributes requests to the node
        """
        # This is equivalent to rebalancing new requests to each node
        # and thus we are calling rebalance_requests here
        for index, new_request_list in enumerate(self.rebalance_requests(request_list, self.num_nodes)):
            self.nodes[index].receive(new_request_list, self.timestamp)


    def process_requests(self, time_budget):
        """Runs each node to process the request for a given time budget
        """
        completion_list = []

        for i in range(self.num_nodes):
            completed_requests = self.nodes[i].process(self.timestamp, time_budget)
            completion_list.extend(completed_requests)

        return completion_list

    
    def scale(self, new_node_number):
        """Scales the number of nodes in the system
        """
        # First, destroy all nodes and put their outstanding requests in a pool
        request_list = []
        for i in range(self.num_nodes):
            remaining_request_list = self.nodes[i].destruct()
            request_list.extend(remaining_request_list)

        # Then, we re-distribute all outstanding requests to the new nodes
        self.nodes = []
        for new_request_list in self.rebalance_requests(request_list, new_node_number):
            node = Node()
            node.receive(new_request_list, self.timestamp)
            self.nodes.append(node)


    def step(self, request_list, time_budget):
        """Steps the simulation for a given time budget
        """
        # First, distribute new requests to nodes
        self.distribute_requests_to_nodes(request_list)

        # Next, ask the nodes to process all the requests as much as possible
        # under the time budget
        completed_requests = self.process_requests(time_budget)
        print(f"At timestamp {self.timestamp}: processed {len(completed_requests)} requests")

        # Evaluates the score here using a set of metrics
        metrics = {
            "completed_requests": completed_requests
        }
        score = self.policy.evaluate_score(metrics)
        self.score += score

        # Autoscale here using a set of metrics
        metrics = {
            "num_nodes": self.num_nodes
        }
        new_node_num = self.policy.autoscale(metrics)

        # Scale the system using the result of the autoscale policy
        # and increment the system time
        if new_node_num != self.num_nodes:
            self.scale(new_node_num)
            scale_overhead = self.policy.get_overhead(self.num_nodes, new_node_num)
            self.timestamp += scale_overhead + time_budget
        else:
            self.timestamp += time_budget
        
        


        
        
        

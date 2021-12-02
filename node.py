class Node():
    def __init__(self):
        # The request pool stores all requests that have not yet been processed
        self.request_pool = []

    def process(self, timestamp, time_budget):
        """Processes pending requests in the pool using a given time budget
        """
        remaining_time = time_budget
        completion_pool = []

        for index, req in enumerate(self.request_pool):
            # Process the request
            remaining_time -= req.process(remaining_time)

            # Increment the current time
            timestamp += req.payload

            if req.payload == 0:
                # Mark the departure timestamp on the request
                req.mark_departure(timestamp)
                # Append the completed request to the completion pool
                completion_pool.append(req)

            # If the remaining time if not enough to process the next request,
            # exit the loop
            if remaining_time == 0:
                break

        # Remove requests that have been processed
        self.request_pool = self.request_pool[len(completion_pool):]
        return completion_pool

    def receive(self, request_list, timestamp):
        """Leaves an arrival timestamp on each request
        """
        for req in request_list:
            # Only stamp requests that do not have a timestamp already
            # This is because we may rebalance requests in case of autoscaling
            if not req.arrival_timestamp:
                req.mark_arrival(timestamp)

        # Add new requests to the request pool
        self.request_pool.extend(request_list)

    def destruct(self):
        """Destruct the node in case of autoscaling
        """
        return self.request_pool




            

import heapq

class AirportScheduler:
    def __init__(self, max_landings, max_gates, max_takeoffs):
        self.max_landings = max_landings
        self.max_gates = max_gates
        self.max_takeoffs = max_takeoffs
        self.landing_times = []  # Min heap to store available landing times
        self.gate_free_times = [0] * max_gates  # Keep track of gate availability
        self.takeoff_times = []  # Min heap to store available takeoff times

    def schedule_planes(self, planes):
        # Sort planes based on remaining fuel and distance from gate
        planes.sort(key=lambda x: (x[0], -x[1]))

        arrangements = []  # To store assigned landing and takeoff times for each plane

        for plane in planes:
            remaining_fuel, gate_distance, service_time, takeoff_time, max_complaint_time = plane
            # Assign landing time
            landing_time = max(0, self.find_landing_time(remaining_fuel))
            heapq.heappush(self.landing_times, landing_time)

            # Assign gate and takeoff time
            gate, gate_time = self.find_gate_and_takeoff_time(landing_time, service_time, takeoff_time, max_complaint_time)
            arrangements.append((landing_time, gate_time))
            self.gate_free_times[gate] = gate_time + service_time

        return arrangements

    def find_landing_time(self, remaining_fuel):
        if len(self.landing_times) < self.max_landings:
            return 0
        else:
            return heapq.heappop(self.landing_times) + 1

    def find_gate_and_takeoff_time(self, landing_time, service_time, takeoff_time, max_complaint_time):
        # Find the earliest available gate
        min_gate_time = min(self.gate_free_times)
        gate = self.gate_free_times.index(min_gate_time)

        # Ensure the plane doesn't exceed the maximum complaint time
        if min_gate_time - landing_time < max_complaint_time:
            takeoff_time += max_complaint_time - (min_gate_time - landing_time)

        gate_time = max(min_gate_time, landing_time) + service_time

        # Ensure the gate time doesn't exceed the takeoff time
        takeoff_time = max(takeoff_time, gate_time)

        # Ensure the number of planes taking off doesn't exceed the limit
        if len(self.takeoff_times) >= self.max_takeoffs:
            takeoff_time = max(takeoff_time, heapq.heappop(self.takeoff_times) + 1)

        heapq.heappush(self.takeoff_times, takeoff_time)

        return gate, gate_time

# Sample input
airport_info = (3, 2, 3)  # Maximum landings, gates, and takeoffs
planes_info = [
    (15, 30, 65, 70, 65),
    (10, 75, 60, 80, 80),
    (50, 15, 10, 15, 80),
    (65, 40, 65, 70, 75)
]

# Parse input
num_planes = len(planes_info)
planes = [tuple(plane_info) for plane_info in planes_info]

# Initialize scheduler
scheduler = AirportScheduler(*airport_info)

# Schedule planes
arrangements = scheduler.schedule_planes(planes)

# Output
for arrangement in arrangements:
    print(*arrangement)

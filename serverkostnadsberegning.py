import matplotlib.pyplot as plt
import math


# Constants
concurrent_users_peak_hours = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
storage_costs = 20 # dollars for 1TB

costs_per_GB_bandwidth = 0.1 # GB
traffic_per_request = 0.01 # 10KB

prompts_per_userminute = 6                                              # Amount of requests generated by each user per minute
prompts_per_instance_minute = [300, 400, 500, 600, 700, 800, 900, 1000, 2000] # Amount of requests that can be handled by an instance per minute

number_peak_hours = 10
number_off_peak_hours = 14

instance_cost_hourly = 1.5 # dollars

# Calculations
required_instances_peak = [] 
required_instances_off_peak = []
for i in range(len(concurrent_users_peak_hours)):
    peak_hours_instances = []
    off_peak_hours_instances = []
    for j in range(len(prompts_per_instance_minute)):
        min_required_instances = concurrent_users_peak_hours[i] * prompts_per_userminute / prompts_per_instance_minute[j]
        peak_hours_instances.append(math.ceil(min_required_instances))
        off_peak_hours_instances.append(math.ceil(min_required_instances/10))
    required_instances_peak.append(peak_hours_instances)
    required_instances_off_peak.append(off_peak_hours_instances)

cost_graphs = []
for i in range(len(prompts_per_instance_minute)):
    cost_graph = []
    for j in range(len(concurrent_users_peak_hours)):
        cost = instance_cost_hourly * (required_instances_peak[j][i] * number_peak_hours + required_instances_off_peak[j][i] * number_off_peak_hours) * 30
        cost += storage_costs
        cost += costs_per_GB_bandwidth * traffic_per_request * prompts_per_userminute * (concurrent_users_peak_hours[j] * number_peak_hours + concurrent_users_peak_hours[j] * number_off_peak_hours) * 30
        cost_graph.append(cost)
    cost_graphs.append(cost_graph)


# Plotting
for i in range(len(cost_graphs)):
    plt.plot(concurrent_users_peak_hours, cost_graphs[i], label=str(prompts_per_instance_minute[i]))
plt.xlabel('Concurrent Users (Peak Hours)')
plt.ylabel('Cost')
plt.title('Cost vs Concurrent Users (Peak Hours)')
plt.legend(title='Prompts per\ninstance minute')
plt.show()

for i in range(len(cost_graphs)-5, len(cost_graphs)):
    plt.plot(concurrent_users_peak_hours, cost_graphs[i], label=str(prompts_per_instance_minute[i]))
plt.xlabel('Concurrent Users (Peak Hours)')
plt.ylabel('Cost')
plt.title('Cost vs Concurrent Users (Peak Hours)')
plt.legend(title='Prompts per\ninstance minute')
plt.show()

#Todo plot cost per user

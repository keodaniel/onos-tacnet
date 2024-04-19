import matplotlib.pyplot as plt 
import numpy as np
import statistics
import datetime
import os
from time import sleep

output = ([21.4, 19.6, 23.2, 24.4, 21.5, 22.2, 23.3, 19. , 24. , 24.6], 
          [24.7, 23.3, 23.9, 23.2, 23.2, 23.8, 23.7, 23.2, 25.1, 25. ], 
          [8.69, 8.05, 8.68, 9.27, 8.33, 8.47, 9.17, 7.82, 9.19, 9.51], 
          [9.34, 8.86, 9.21, 8.94, 8.93, 8.99, 8.96, 9.16, 9.36, 9.55], 
          [-3.3, -3.7, -0.7,  1.2, -1.7, -1.6, -0.4, -4.2, -1.1, -0.4], 
          [-0.65, -0.81, -0.53,  0.33, -0.6 , -0.52,  0.21, -1.34, -0.17, -0.04])
output = (([24.5, 25.2, 24.7, 20.9, 22.5, 24. , 23.4, 22.6, 21.5, 24.2]), ([24.3, 25.9, 23.2, 23.6, 23.4, 22.8, 23.8, 24.2, 23. , 24.3]), ([9.5 , 9.55, 9.48, 8.03, 8.63, 9.05, 9.06, 8.37, 8.23, 9.29]), ([9.35, 9.54, 8.96, 8.98, 8.99, 8.69, 9.11, 9.24, 8.93, 9.01]), ([ 0.2, -0.7,  1.5, -2.7, -0.9,  1.2, -0.4, -1.6, -1.5, -0.1]), ([ 0.15,  0.01,  0.52, -0.95, -0.36,  0.36, -0.05, -0.87, -0.7 ,
        0.28]))
output = ([36.7, 25.2], [28.4, 26.8], [9.33, 6.04], [6.49, 6.12], [8.3, -1.6], [2.84, -0.08])
start_time = datetime.datetime.now()
elapsed_time = (datetime.datetime.now() - start_time)


baseline_capacity_data = output[0]
failover_capacity_data = output[1]
baseline_throughput_data = output[2]
failover_throughput_data = output[3]
capacity_diff_data = output[4]
throughput_diff_data = output[5]

# boxplot
fig, ax = plt.subplots(1, 2)
fig.set_size_inches(10, 5)
ax[0].boxplot([baseline_capacity_data, failover_capacity_data], widths=0.4, labels=["Baseline", "Single Link Failover"])
ax[0].set_title("Capacity of 20s iPerf Test")
m = min(min(baseline_capacity_data), min(failover_capacity_data))
M = max(max(baseline_capacity_data), max(failover_capacity_data))
M = M + 10 - M % 10

ticks = np.arange(0, M+2, 2)
ax[0].set_yticks(ticks)
ax[0].set_ylabel("MBytes")
failover_median = statistics.median(failover_capacity_data)
baseline_median = statistics.median(baseline_capacity_data)
diff_median = (failover_median - baseline_median) / baseline_median * 100
# ax[0].text(1.65, failover_median, f"{diff_median:.2f}%", ha='center', va='center', color='red')
ax[0].text(1.6, failover_median, f"{'+' if diff_median >= 0 else '-'}{diff_median:.2f}% ", ha='center', va='center', color='red')


ax[0].text(1.5, 0, "Median % Difference from Baseline", ha='center', va='bottom', color='red')

ax[1].boxplot([baseline_throughput_data, failover_throughput_data], widths=0.4, labels=["Baseline", "Single Link Failover"])
ax[1].set_title("Throughput of 20s iPerf Test")
ax[1].set_ylabel("Mbits/sec")
m = min(min(baseline_throughput_data), min(failover_throughput_data))
M = max(max(baseline_throughput_data), max(failover_throughput_data))
M = M + 10 - M % 10
ticks = np.arange(0, M+1, 1)
ax[1].set_yticks(ticks)
failover_median = statistics.median(failover_throughput_data)
baseline_median = statistics.median(baseline_throughput_data)
diff_median = (failover_median - baseline_median) / baseline_median * 100
ax[1].text(1.6, failover_median, f"{'+' if diff_median >= 0 else '-'}{diff_median:.2f}% ", ha='center', va='center', color='red')
ax[1].text(1.5, 0, "Median % Difference from Baseline", ha='center', va='bottom', color='red')

plt.show()

# date = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
# if not os.path.exists('logs'):
#     os.makedirs('logs')
# fig.savefig(f"logs/boxplot-{date}.png")

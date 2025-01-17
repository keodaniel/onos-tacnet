import matplotlib.pyplot as plt 
import numpy as np
import statistics
import datetime
import os
from time import sleep

# output = ([21.4, 19.6, 23.2, 24.4, 21.5, 22.2, 23.3, 19. , 24. , 24.6], 
#           [24.7, 23.3, 23.9, 23.2, 23.2, 23.8, 23.7, 23.2, 25.1, 25. ], 
#           [8.69, 8.05, 8.68, 9.27, 8.33, 8.47, 9.17, 7.82, 9.19, 9.51], 
#           [9.34, 8.86, 9.21, 8.94, 8.93, 8.99, 8.96, 9.16, 9.36, 9.55], 
#           [-3.3, -3.7, -0.7,  1.2, -1.7, -1.6, -0.4, -4.2, -1.1, -0.4], 
#           [-0.65, -0.81, -0.53,  0.33, -0.6 , -0.52,  0.21, -1.34, -0.17, -0.04])
# output = (([24.5, 25.2, 24.7, 20.9, 22.5, 24. , 23.4, 22.6, 21.5, 24.2]), ([24.3, 25.9, 23.2, 23.6, 23.4, 22.8, 23.8, 24.2, 23. , 24.3]), ([9.5 , 9.55, 9.48, 8.03, 8.63, 9.05, 9.06, 8.37, 8.23, 9.29]), ([9.35, 9.54, 8.96, 8.98, 8.99, 8.69, 9.11, 9.24, 8.93, 9.01]), ([ 0.2, -0.7,  1.5, -2.7, -0.9,  1.2, -0.4, -1.6, -1.5, -0.1]), ([ 0.15,  0.01,  0.52, -0.95, -0.36,  0.36, -0.05, -0.87, -0.7 ,
#         0.28]))
# output = ([36.7, 25.2], [28.4, 26.8], [9.33, 6.04], [6.49, 6.12], [8.3, -1.6], [2.84, -0.08])
output_reactiveforwarding = ([35.9, 36.3, 35.0, 36.2, 24.5, 36.3, 35.8, 32.7, 35.6, 36.5, 36.3, 36.5, 36.8, 36.6, 36.6, 36.7, 36.8, 36.7, 36.2, 36.2], [28.6, 28.4, 24.6, 28.1, 27.7, 28.0, 27.9, 27.9, 27.7, 28.0, 28.6, 28.6, 28.4, 28.7, 28.4, 28.4, 28.0, 28.3, 28.4, 28.5], [8.99, 8.94, 8.67, 8.93, 8.92, 8.92, 9.1, 8.57, 8.88, 9.17, 9.22, 9.1, 9.34, 9.26, 9.06, 9.17, 9.31, 9.28, 9.22, 8.99], [6.63, 6.62, 7.04, 6.53, 6.42, 6.39, 6.55, 6.49, 6.53, 6.51, 6.64, 6.62, 6.57, 6.71, 6.59, 6.57, 6.49, 6.61, 6.6, 6.64], [7.3, 7.9, 10.4, 8.1, -3.2, 8.3, 7.9, 4.8, 7.9, 8.5, 7.7, 7.9, 8.4, 7.9, 8.2, 8.3, 8.8, 8.4, 7.8, 7.7], [2.36, 2.32, 1.63, 2.4, 2.5, 2.53, 2.55, 2.08, 2.35, 2.66, 2.58, 2.48, 2.77, 2.55, 2.47, 2.6, 2.82, 2.67, 2.62, 2.35])
output_hostintents = ([37.1, 35.4, 36.7, 36.5, 36.4, 36.9, 36.5, 35.8, 36.3, 36.5, 36.0, 36.4, 36.7, 36.5, 29.6, 36.7, 36.6, 36.8, 36.5, 36.5], [28.4, 27.5, 28.8, 28.8, 28.7, 28.1, 28.9, 28.4, 28.7, 29.0, 28.0, 28.3, 28.8, 28.6, 28.7, 28.4, 28.5, 28.4, 28.7, 28.4], [9.4, 8.81, 9.16, 9.23, 9.0, 9.23, 8.96, 9.15, 9.05, 9.16, 9.12, 9.22, 9.08, 9.01, 9.23, 9.08, 9.32, 9.37, 9.27, 9.12], [6.5, 6.36, 6.65, 6.65, 6.65, 6.56, 6.65, 6.54, 6.58, 6.68, 6.48, 6.56, 6.65, 6.58, 6.63, 6.54, 6.55, 6.49, 6.58, 6.58], [8.7, 7.9, 7.9, 7.7, 7.7, 8.8, 7.6, 7.4, 7.6, 7.5, 8.0, 8.1, 7.9, 7.9, 0.9, 8.3, 8.1, 8.4, 7.8, 8.1], [2.9, 2.45, 2.51, 2.58, 2.35, 2.67, 2.31, 2.61, 2.47, 2.48, 2.64, 2.66, 2.43, 2.43, 2.6, 2.54, 2.77, 2.88, 2.69, 2.54])

# separate each output into 6 lists named baseline capacity, failover capacity, baseline throughput, failover throughput, capacity difference, throughput difference, report means median and std for each, then report p-values for the difference in statistics between the two outputs for statistical significance
baseline_capacity_data_reactiveforwarding = output_reactiveforwarding[0]
failover_capacity_data_reactiveforwarding = output_reactiveforwarding[1]
baseline_throughput_data_reactiveforwarding = output_reactiveforwarding[2]
failover_throughput_data_reactiveforwarding = output_reactiveforwarding[3]
capacity_diff_data_reactiveforwarding = output_reactiveforwarding[4]
throughput_diff_data_reactiveforwarding = output_reactiveforwarding[5]

baseline_capacity_data_hostintents = output_hostintents[0]
failover_capacity_data_hostintents = output_hostintents[1]
baseline_throughput_data_hostintents = output_hostintents[2]
failover_throughput_data_hostintents = output_hostintents[3]
capacity_diff_data_hostintents = output_hostintents[4]
throughput_diff_data_hostintents = output_hostintents[5]


# print statistics in one line per output
print("Reactive Forwarding")
print("Baseline Capacity")
print(f"Mean: {statistics.mean(baseline_capacity_data_reactiveforwarding)}, Median: {statistics.median(baseline_capacity_data_reactiveforwarding)}, Std: {statistics.stdev(baseline_capacity_data_reactiveforwarding)}")
print("Failover Capacity")
print(f"Mean: {statistics.mean(failover_capacity_data_reactiveforwarding)}, Median: {statistics.median(failover_capacity_data_reactiveforwarding)}, Std: {statistics.stdev(failover_capacity_data_reactiveforwarding)}")
print("Capacity Difference")
print(f"Mean: {statistics.mean(baseline_capacity_data_reactiveforwarding)-statistics.mean(failover_capacity_data_reactiveforwarding)}, Median: {statistics.median(baseline_capacity_data_reactiveforwarding)-statistics.median(failover_capacity_data_reactiveforwarding)}, Std: {statistics.stdev(baseline_capacity_data_reactiveforwarding)-statistics.stdev(failover_capacity_data_reactiveforwarding)}")

print("Baseline Throughput")
print(f"Mean: {statistics.mean(baseline_throughput_data_reactiveforwarding)}, Median: {statistics.median(baseline_throughput_data_reactiveforwarding)}, Std: {statistics.stdev(baseline_throughput_data_reactiveforwarding)}")
print("Failover Throughput")
print(f"Mean: {statistics.mean(failover_throughput_data_reactiveforwarding)}, Median: {statistics.median(failover_throughput_data_reactiveforwarding)}, Std: {statistics.stdev(failover_throughput_data_reactiveforwarding)}")
print("Throughput Difference")
print(f"Mean: {statistics.mean(baseline_throughput_data_reactiveforwarding)-statistics.mean(failover_throughput_data_reactiveforwarding)}, Median: {statistics.median(baseline_throughput_data_reactiveforwarding)-statistics.median(failover_throughput_data_reactiveforwarding)}, Std: {statistics.stdev(baseline_throughput_data_reactiveforwarding)-statistics.stdev(failover_throughput_data_reactiveforwarding)}")

print("Host Intents")
print("Baseline Capacity")
print(f"Mean: {statistics.mean(baseline_capacity_data_hostintents)}, Median: {statistics.median(baseline_capacity_data_hostintents)}, Std: {statistics.stdev(baseline_capacity_data_hostintents)}")
print("Failover Capacity")
print(f"Mean: {statistics.mean(failover_capacity_data_hostintents)}, Median: {statistics.median(failover_capacity_data_hostintents)}, Std: {statistics.stdev(failover_capacity_data_hostintents)}")
print("Capacity Difference")
print(f"Mean: {statistics.mean(baseline_capacity_data_hostintents)-statistics.mean(failover_capacity_data_hostintents)}, Median: {statistics.median(baseline_capacity_data_hostintents)-statistics.median(failover_capacity_data_hostintents)}, Std: {statistics.stdev(baseline_capacity_data_hostintents)-statistics.stdev(failover_capacity_data_hostintents)}")

print("Baseline Throughput")
print(f"Mean: {statistics.mean(baseline_throughput_data_hostintents)}, Median: {statistics.median(baseline_throughput_data_hostintents)}, Std: {statistics.stdev(baseline_throughput_data_hostintents)}")
print("Failover Throughput")
print(f"Mean: {statistics.mean(failover_throughput_data_hostintents)}, Median: {statistics.median(failover_throughput_data_hostintents)}, Std: {statistics.stdev(failover_throughput_data_hostintents)}")
print("Throughput Difference")
print(f"Mean: {statistics.mean(baseline_throughput_data_hostintents)-statistics.mean(failover_throughput_data_hostintents)}, Median: {statistics.median(baseline_throughput_data_hostintents)-statistics.median(failover_throughput_data_hostintents)}, Std: {statistics.stdev(baseline_throughput_data_hostintents)-statistics.stdev(failover_throughput_data_hostintents)}")

# print p-values for statistical significance
from scipy.stats import ttest_ind
print("Baseline Capacity")
print(ttest_ind(baseline_capacity_data_reactiveforwarding, baseline_capacity_data_hostintents))
print("Baseline Throughput")
print(ttest_ind(baseline_throughput_data_reactiveforwarding, baseline_throughput_data_hostintents))
print("Failover Capacity")
print(ttest_ind(failover_capacity_data_reactiveforwarding, failover_capacity_data_hostintents))
print("Failover Throughput")
print(ttest_ind(failover_throughput_data_reactiveforwarding, failover_throughput_data_hostintents))
print("Capacity Difference")
print(ttest_ind(capacity_diff_data_reactiveforwarding, capacity_diff_data_hostintents))
print("Throughput Difference")
print(ttest_ind(throughput_diff_data_reactiveforwarding, throughput_diff_data_hostintents))

def plot(input):
        output = input
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
        print("MEDIAN CALCULATION", baseline_median, failover_median - baseline_median, diff_median)
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

plot(output_reactiveforwarding)
plot(output_hostintents)
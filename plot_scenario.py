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
# output_reactiveforwarding = ([35.9, 36.3, 35.0, 36.2, 24.5, 36.3, 35.8, 32.7, 35.6, 36.5, 36.3, 36.5, 36.8, 36.6, 36.6, 36.7, 36.8, 36.7, 36.2, 36.2], [28.6, 28.4, 24.6, 28.1, 27.7, 28.0, 27.9, 27.9, 27.7, 28.0, 28.6, 28.6, 28.4, 28.7, 28.4, 28.4, 28.0, 28.3, 28.4, 28.5], [8.99, 8.94, 8.67, 8.93, 8.92, 8.92, 9.1, 8.57, 8.88, 9.17, 9.22, 9.1, 9.34, 9.26, 9.06, 9.17, 9.31, 9.28, 9.22, 8.99], [6.63, 6.62, 7.04, 6.53, 6.42, 6.39, 6.55, 6.49, 6.53, 6.51, 6.64, 6.62, 6.57, 6.71, 6.59, 6.57, 6.49, 6.61, 6.6, 6.64], [7.3, 7.9, 10.4, 8.1, -3.2, 8.3, 7.9, 4.8, 7.9, 8.5, 7.7, 7.9, 8.4, 7.9, 8.2, 8.3, 8.8, 8.4, 7.8, 7.7], [2.36, 2.32, 1.63, 2.4, 2.5, 2.53, 2.55, 2.08, 2.35, 2.66, 2.58, 2.48, 2.77, 2.55, 2.47, 2.6, 2.82, 2.67, 2.62, 2.35])
# output_hostintents = ([37.1, 35.4, 36.7, 36.5, 36.4, 36.9, 36.5, 35.8, 36.3, 36.5, 36.0, 36.4, 36.7, 36.5, 29.6, 36.7, 36.6, 36.8, 36.5, 36.5], [28.4, 27.5, 28.8, 28.8, 28.7, 28.1, 28.9, 28.4, 28.7, 29.0, 28.0, 28.3, 28.8, 28.6, 28.7, 28.4, 28.5, 28.4, 28.7, 28.4], [9.4, 8.81, 9.16, 9.23, 9.0, 9.23, 8.96, 9.15, 9.05, 9.16, 9.12, 9.22, 9.08, 9.01, 9.23, 9.08, 9.32, 9.37, 9.27, 9.12], [6.5, 6.36, 6.65, 6.65, 6.65, 6.56, 6.65, 6.54, 6.58, 6.68, 6.48, 6.56, 6.65, 6.58, 6.63, 6.54, 6.55, 6.49, 6.58, 6.58], [8.7, 7.9, 7.9, 7.7, 7.7, 8.8, 7.6, 7.4, 7.6, 7.5, 8.0, 8.1, 7.9, 7.9, 0.9, 8.3, 8.1, 8.4, 7.8, 8.1], [2.9, 2.45, 2.51, 2.58, 2.35, 2.67, 2.31, 2.61, 2.47, 2.48, 2.64, 2.66, 2.43, 2.43, 2.6, 2.54, 2.77, 2.88, 2.69, 2.54])

def parse_and_print(file_path, parallel_connections=False):
        baseline_capacity_data = []
        failover_capacity_data = []
        baseline_throughput_data = []
        failover_throughput_data = []
        baseline_jitter_data = []
        failover_jitter_data = []
        baseline_datagram_loss_data = []
        failover_datagram_loss_data = []

        capacity_list = None
        throughput_list = None
        jitter_list = None
        datagram_loss_list = None

        if "UDP" in file_path or "udp" in file_path:
                search_term = "receiver"
        else:
                search_term = "sender"

        with open(file_path, "r") as file:
                for line in file:
                        line.strip("\n")
                        if "SUM" in line:
                                parallel_connections = True
                        if "Baseline Output:" in line:
                                capacity_list = baseline_capacity_data
                                throughput_list = baseline_throughput_data
                                jitter_list = baseline_jitter_data
                                datagram_loss_list = baseline_datagram_loss_data
                                
                        if "Failover Output:" in line:
                                capacity_list = failover_capacity_data
                                throughput_list = failover_throughput_data
                                jitter_list = failover_jitter_data
                                datagram_loss_list = failover_datagram_loss_data

                        if capacity_list is not None and throughput_list is not None and search_term in line:
                                if parallel_connections:
                                        if "SUM" in line:
                                                for part in line.split("  "):
                                                        if "MBytes" in part:
                                                                capacity_list.append(float(part.split(" ")[0]))
                                                        if "Mbits/sec" in part:
                                                                throughput_list.append(float(part.split(" ")[0]))
                                                        if "ms" in part:
                                                                jitter_list.append(float(part.split(" ")[0]))
                                                        if "%" in part:
                                                                fraction_str = part.split(" ")[0]
                                                                lost_datagram = int(fraction_str.split("/")[0])
                                                                # total_datagram = int(fraction_str.split("/")[1])
                                                                datagram_loss_list.append(lost_datagram)
                                else:
                                        for part in line.split("  "):
                                                if "Bytes" in part:
                                                        for i in part.split(" "):
                                                                if i and "Bytes" not in i:
                                                                        capacity_list.append(float(i.split(" ")[0]))
                                                        # capacity_list.append(float(part.split(" ")[0]))
                                                if "bits/sec" in part:
                                                        throughput_list.append(float(part.split(" ")[0]))
                                                if "ms" in part:
                                                        jitter_list.append(float(part.split(" ")[0]))
                                                if "%" in part:
                                                        fraction_str = part.split(" ")[0]
                                                        lost_datagram = int(fraction_str.split("/")[0])
                                                        # total_datagram = int(fraction_str.split("/")[1])
                                                        datagram_loss_list.append(lost_datagram)

        for i in zip(("Baseline Capacity", "Failover Capacity", "Baseline Throughput", "Failover Throughput"), (baseline_capacity_data, failover_capacity_data, baseline_throughput_data, failover_throughput_data)):
                print(f"{i[0]} Data: {i[1]}")

        if search_term == "receiver":
                print(f"Jitter Data: Baseline: {baseline_jitter_data}, Failover: {failover_jitter_data}")
        # print(f"Datagram Loss Data: Baseline: {baseline_datagram_loss_data}, Failover: {failover_datagram_loss_data}")

        # print statistics in one line per output
        print(f"Baseline Capacity Mean: {round(statistics.mean(baseline_capacity_data), 4)}, Median: {round(statistics.median(baseline_capacity_data), 4)}, Std: {round(statistics.stdev(baseline_capacity_data), 4)}")
        print(f"Failover Capacity Mean: {round(statistics.mean(failover_capacity_data), 4)}, Median: {round(statistics.median(failover_capacity_data), 4)}, Std: {round(statistics.stdev(failover_capacity_data), 4)}")
        print(f"Capacity Difference Mean: {round(statistics.mean(baseline_capacity_data)-statistics.mean(failover_capacity_data), 4)}, Median: {round(statistics.median(baseline_capacity_data)-statistics.median(failover_capacity_data), 4)}, Std: {round(statistics.stdev(baseline_capacity_data)-statistics.stdev(failover_capacity_data), 4)}")
        print(f"Baseline Throughput Mean: {round(statistics.mean(baseline_throughput_data), 4)}, Median: {round(statistics.median(baseline_throughput_data), 4)}, Std: {round(statistics.stdev(baseline_throughput_data), 4)}")
        print(f"Failover Throughput Mean: {round(statistics.mean(failover_throughput_data), 4)}, Median: {round(statistics.median(failover_throughput_data), 4)}, Std: {round(statistics.stdev(failover_throughput_data), 4)}")
        print(f"Throughput Difference Mean: {round(statistics.mean(baseline_throughput_data)-statistics.mean(failover_throughput_data), 4)}, Median: {round(statistics.median(baseline_throughput_data)-statistics.median(failover_throughput_data), 4)}, Std: {round(statistics.stdev(baseline_throughput_data)-statistics.stdev(failover_throughput_data), 4)}")
        
        if search_term == "receiver":
                print(f"Baseline Jitter Mean: {round(statistics.mean(baseline_jitter_data), 4)}, Median: {round(statistics.median(baseline_jitter_data), 4)}, Std: {round(statistics.stdev(baseline_jitter_data), 4)}")
                print(f"Failover Jitter Mean: {round(statistics.mean(failover_jitter_data), 4)}, Median: {round(statistics.median(failover_jitter_data), 4)}, Std: {round(statistics.stdev(failover_jitter_data), 4)}")
                print(f"Jitter Difference Mean: {round(statistics.mean(baseline_jitter_data)-statistics.mean(failover_jitter_data), 4)}, Median: {round(statistics.median(baseline_jitter_data)-statistics.median(failover_jitter_data), 4)}, Std: {round(statistics.stdev(baseline_jitter_data)-statistics.stdev(failover_jitter_data), 4)}")
                print(f"Baseline Datagram Loss Mean: {round(statistics.mean(baseline_datagram_loss_data), 4)}, Median: {round(statistics.median(baseline_datagram_loss_data), 4)}, Std: {round(statistics.stdev(baseline_datagram_loss_data), 4)}")
                print(f"Failover Datagram Loss Mean: {round(statistics.mean(failover_datagram_loss_data), 4)}, Median: {round(statistics.median(failover_datagram_loss_data), 4)}, Std: {round(statistics.stdev(failover_datagram_loss_data), 4)}")
                print(f"Datagram Loss Difference Mean: {round(statistics.mean(baseline_datagram_loss_data)-statistics.mean(failover_datagram_loss_data), 4)}, Median: {round(statistics.median(baseline_datagram_loss_data)-statistics.median(failover_datagram_loss_data), 4)}, Std: {round(statistics.stdev(baseline_datagram_loss_data)-statistics.stdev(failover_datagram_loss_data), 4)}")

        return (baseline_capacity_data, failover_capacity_data, baseline_throughput_data, failover_throughput_data, baseline_jitter_data, failover_jitter_data, baseline_datagram_loss_data, failover_datagram_loss_data)

def plot(input, title):
        baseline_capacity_data = input[0]
        failover_capacity_data = input[1]
        baseline_throughput_data = input[2]
        failover_throughput_data = input[3]
        baseline_jitter_data = input[4]
        failover_jitter_data = input[5]
        baseline_datagram_loss_data = input[6]
        failover_datagram_loss_data = input[7]

        # boxplot
        fig, ax = plt.subplots(1, 2)
        fig.set_size_inches(10, 5)
        ax[0].boxplot([baseline_capacity_data, failover_capacity_data], widths=0.4, labels=["Baseline", "Single Link Failover"])
        ax[0].set_title(title[0])
        m = min(min(baseline_capacity_data), min(failover_capacity_data))
        M = max(max(baseline_capacity_data), max(failover_capacity_data))
        M = M + 10 - M % 10

        ticks = np.arange(0, M+2, 2)
        ax[0].set_yticks(ticks)
        ax[0].set_ylabel("MBytes")
        failover_median = statistics.median(failover_capacity_data)
        baseline_median = statistics.median(baseline_capacity_data)
        diff_median = (failover_median - baseline_median) / baseline_median * 100
        ax[0].text(1.6, failover_median, f"{'+' if diff_median >= 0 else '-'}{diff_median:.2f}% ", ha='center', va='center', color='red')
        ax[0].text(1.5, 0, "Median % Difference from Baseline", ha='center', va='bottom', color='red')

        ax[1].boxplot([baseline_throughput_data, failover_throughput_data], widths=0.4, labels=["Baseline", "Single Link Failover"])
        ax[1].set_title(title[1])
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

        if baseline_jitter_data and failover_jitter_data and baseline_datagram_loss_data and failover_datagram_loss_data:
                # boxplot jitter data
                fig, ax = plt.subplots(1, 2)
                fig.set_size_inches(10, 5)

                ax[0].boxplot([baseline_jitter_data, failover_jitter_data], widths=0.4, labels=["Baseline", "Single Link Failover"])
                ax[0].set_title("Jitter")
                ax[0].set_ylabel("ms (Log Scale)")
                ax[0].set_yscale('log')  # Set y-axis to log scale
                m = min(min(baseline_jitter_data), min(failover_jitter_data))
                M = max(max(baseline_jitter_data), max(failover_jitter_data))
                # M = M + 10 - M % 10
                # ticks = np.arange(0, M+1, 5)
                # ax[0].set_yticks(ticks)
                # set max y to 100
                ax[0].set_ylim([0, 100000])
                failover_median = statistics.median(failover_jitter_data)
                baseline_median = statistics.median(baseline_jitter_data)
                diff_median = (failover_median - baseline_median) / baseline_median * 100
                ax[0].text(1.6, failover_median, f"{'+' if diff_median >= 0 else '-'}{diff_median:.2f}% ", ha='center', va='center', color='red')
                ax[0].text(1.5, ax[0].get_ylim()[1] - 10000, "Median % Difference from Baseline", ha='center', va='top', color='red')
                
                ax[1].boxplot([baseline_datagram_loss_data, failover_datagram_loss_data], widths=0.4, labels=["Baseline", "Single Link Failover"])
                ax[1].set_title("Datagram Loss")
                ax[1].set_ylabel("Quantity")
                m = min(min(baseline_datagram_loss_data), min(failover_datagram_loss_data))
                M = max(max(baseline_datagram_loss_data), max(failover_datagram_loss_data))
                # ax[1].set_ylim([0, 10])
                # M = M + 10 - M % 10
                ticks = np.arange(0, 11, 1)
                ax[1].set_yticks(ticks)
                
                plt.show()


# output_reactiveforwarding = (baseline_capacity_data, failover_capacity_data, baseline_throughput_data, failover_throughput_data, capacity_diff_data_reactiveforwarding, throughput_diff_data_reactiveforwarding)

# file_path = r"for_thesis\2024-04-29-2040_test.log" # iperf3 reactive forwarding 20 seconds 20 trials single TCP
# file_path = r"logs\2024-04-30-1508_output -t 10 -P 3 2 trials.log"
# file_path = r"for_thesis\2024-04-30-2202 fwd-TC-t20-P3-20runs_output.log"
# file_path = r"for_thesis\2024-04-30-2308 fwd-TC-t20-P1-20runs_output.log"

# file_path = r"for_thesis\2024-05-01-0051 fwd-TC-t20-P3-20runs_output.log"
# file_path = r"logs\2024-05-01-1018 fwd-UDP-TC-t20-P1-20runs_output.log"
# file_path = r"logs\2024-05-01-1628 fwd-TC-udp-t20-P1-b1M-20runs_output.log"
# file_path = r"logs\2024-05-01-1702 fwd-TC-udp-t20-P3-b1M-20runs_output.log"
# file_path = r"logs\2024-05-01-1818 fwd-TC-udp-t20-P1-b10M-20runs_output.log"
# file_path = r"logs\2024-05-02-1522 fwd-TC-udp-t20-P1-b0M-20runs_output.log"
file_path = r"logs\2024-05-02-1549 fwd-TC-udp-t20-P3-b0M-20runs_output.log"


output = parse_and_print(file_path)
plot(output, ("Capacity of 20s iPerf Test", "Throughput of 20s iPerf Test"))
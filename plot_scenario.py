import matplotlib.pyplot as plt 
import numpy as np
import statistics
import datetime
import os
from time import sleep

def parse_and_print(file_path):
        parallel_connections = False
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
        units = ["Bytes", "bits/sec"]

        if "udp" in file_path:
                search_term = "receiver"
        else:
                search_term = "sender"

        if "P3" in file_path:
                parallel_connections = True

        with open(file_path, "r") as file:
                for line in file:
                        line.strip("\n")
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

                        if search_term in line:
                                if parallel_connections:
                                        if "SUM" in line:
                                                for i in line.split("   "):
                                                        for j in i.split("  "):
                                                                if "Bytes" in j:
                                                                        units[0] = j.split(" ")[1]
                                                                        capacity_list.append(float(j.split(" ")[0]))
                                                                if "bits/sec" in j:
                                                                        units[1] = j.split(" ")[1]
                                                                        throughput_list.append(float(j.split(" ")[0]))
                                                                if "ms" in j:
                                                                        jitter_list.append(float(j.split(" ")[0]))
                                                                if "%" in j:
                                                                        datagram_loss_list.append(float(j.split()[1].strip("(").strip(")").strip("%")))
                                else:
                                        for i in line.split("   "):
                                                for j in i.split("  "):
                                                        if "Bytes" in j:
                                                                units[0] = j.split(" ")[1]
                                                                capacity_list.append(float(j.split(" ")[0]))
                                                        if "bits/sec" in j:
                                                                units[1] = j.split(" ")[1]
                                                                throughput_list.append(float(j.split(" ")[0]))
                                                        if "ms" in j:
                                                                jitter_list.append(float(j.split(" ")[0]))
                                                        if "%" in j:
                                                                datagram_loss_list.append(float(j.split()[1].strip("(").strip(")").strip("%")))
                                                                # fraction_str = j.split(" ")[0]
                                                                # lost_datagram = int(fraction_str.split("/")[0])
                                                                # datagram_loss_list.append(lost_datagram)


        for i in zip(("Baseline Capacity", "Failover Capacity", "Baseline Throughput", "Failover Throughput"), (baseline_capacity_data, failover_capacity_data, baseline_throughput_data, failover_throughput_data)):
                print(f"{i[0]} Data: {i[1]}")

        if "udp" in file_path:
                for i in zip(("Baseline Jitter", "Failover Jitter", "Baseline Datagram Loss", "Failover Datagram Loss"), (baseline_jitter_data, failover_jitter_data, baseline_datagram_loss_data, failover_datagram_loss_data)):
                        print(f"{i[0]} Data: {i[1]}")
                # print(f"Jitter Data: Baseline: {baseline_jitter_data}\nFailover: {failover_jitter_data}")
                # print(f"Datagram Loss Data: Baseline: {baseline_datagram_loss_data}\nFailover: {failover_datagram_loss_data}")

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

        return (units, baseline_capacity_data, failover_capacity_data, baseline_throughput_data, failover_throughput_data, baseline_jitter_data, failover_jitter_data, baseline_datagram_loss_data, failover_datagram_loss_data)

def plot(input, title, filename="plot"):
        units, baseline_capacity_data, failover_capacity_data, baseline_throughput_data, failover_throughput_data, baseline_jitter_data, failover_jitter_data, baseline_datagram_loss_data, failover_datagram_loss_data = input

        # boxplot
        fig, ax = plt.subplots(1, 2)
        fig.set_size_inches(10, 5)
        ax[0].boxplot([baseline_capacity_data, failover_capacity_data], widths=0.4, labels=["Baseline", "Single Link Failover"])
        ax[0].set_title(title[0])
        m = min(min(baseline_capacity_data), min(failover_capacity_data))
        M = max(max(baseline_capacity_data), max(failover_capacity_data))
        M = M + 10 - M % 10

        ticks = np.arange(0, 42, 2)
        ax[0].set_yticks(ticks)

        ax[0].set_ylabel(units[0])
        failover_median = statistics.median(failover_capacity_data)
        baseline_median = statistics.median(baseline_capacity_data)
        diff_median = (failover_median - baseline_median) / baseline_median * 100
        ax[0].text(1.6, failover_median, f"{'+' if diff_median >= 0 else '-'}{diff_median:.2f}% ", ha='center', va='center', color='red')
        ax[0].text(1.5, 0, "Median % Difference from Baseline", ha='center', va='bottom', color='red')

        ax[1].boxplot([baseline_throughput_data, failover_throughput_data], widths=0.4, labels=["Baseline", "Single Link Failover"])
        ax[1].set_title(title[1])
        ax[1].set_ylabel(units[1])
        m = min(min(baseline_throughput_data), min(failover_throughput_data))
        M = max(max(baseline_throughput_data), max(failover_throughput_data))
        M = M + 10 - M % 10

        ticks = np.arange(0, 21, 1)
        ax[1].set_yticks(ticks)
        
        failover_median = statistics.median(failover_throughput_data)
        baseline_median = statistics.median(baseline_throughput_data)
        diff_median = (failover_median - baseline_median) / baseline_median * 100
        ax[1].text(1.6, failover_median, f"{'+' if diff_median >= 0 else '-'}{diff_median:.2f}% ", ha='center', va='center', color='red')
        ax[1].text(1.5, 0, "Median % Difference from Baseline", ha='center', va='bottom', color='red')

        plt.show()

        # save fig as name
        # fig.savefig(f"{filename}_plot1.png")

        if baseline_jitter_data and failover_jitter_data and baseline_datagram_loss_data and failover_datagram_loss_data:
                # boxplot jitter data
                fig, ax = plt.subplots(1, 2)
                fig.set_size_inches(10, 5)

                ax[0].boxplot([baseline_jitter_data, failover_jitter_data], widths=0.4, labels=["Baseline", "Single Link Failover"])
                ax[0].set_title("Jitter")
                ax[0].set_ylabel("ms")
                # ax[0].set_yscale('log')  # Set y-axis to log scale
                m = min(min(baseline_jitter_data), min(failover_jitter_data))
                M = max(max(baseline_jitter_data), max(failover_jitter_data))
                # M = M + 10 - M % 10

                ticks = np.arange(0, 60, 5)
                ax[0].set_yticks(ticks)

                failover_median = statistics.median(failover_jitter_data)
                baseline_median = statistics.median(baseline_jitter_data)
                diff_median = (failover_median - baseline_median) / baseline_median * 100
                ax[0].text(1.6, failover_median, f"{'+' if diff_median >= 0 else '-'}{diff_median:.2f}% ", ha='center', va='center', color='red')
                ax[0].text(1.5, ax[0].get_ylim()[1] - 1, "Median % Difference from Baseline", ha='center', va='top', color='red')
                
                ax[1].boxplot([baseline_datagram_loss_data, failover_datagram_loss_data], widths=0.4, labels=["Baseline", "Single Link Failover"])
                ax[1].set_title("Datagram Loss")
                ax[1].set_ylabel("%")
                m = min(min(baseline_datagram_loss_data), min(failover_datagram_loss_data))
                M = max(max(baseline_datagram_loss_data), max(failover_datagram_loss_data))
                # ax[1].set_ylim([0, 10])
                # M = M + 10 - M % 10

                ticks = np.arange(0, 1.1, .1)
                ax[1].set_yticks(ticks)
                # ax[1].text(1.5, ax[1].get_ylim()[1] - 10, "Median % Difference from Baseline", ha='center', va='top', color='red')

                plt.show()
                # fig.savefig(f"{filename}_plot2.png")



# output_reactiveforwarding = (baseline_capacity_data, failover_capacity_data, baseline_throughput_data, failover_throughput_data, capacity_diff_data_reactiveforwarding, throughput_diff_data_reactiveforwarding)
# 

# TCP TESTS
# file_path = r"for_thesis\2024-04-29-2040_test.log" # SCENARIO 1
# file_path = r"for_thesis\2024-04-30-2308 fwd-TC-t20-P1-20runs_output.log" # SCENARIO 1 v2
# file_path = r"for_thesis\2024-04-30-2202 fwd-TC-t20-P3-20runs_output.log" # SCENARIO 2
# file_path = r"for_thesis\2024-05-01-0051 fwd-TC-t20-P3-20runs_output.log" # SCENARIO 2 v2

# UDP TESTS
# file_path = r"logs\2024-05-02-1522 fwd-TC-udp-t20-P1-b0M-20runs_output.log" # SCENARIO 3
# file_path = r"logs\2024-05-02-1549 fwd-TC-udp-t20-P3-b0M-20runs_output.log" # SCENARIO 4
# file_path = r"logs\2024-05-03-1049 fwd-TC-udp-t20-P1-b3M-20runs_output.log" # SCENARIO 5 . . . replace with P1-b2m

# file_path = r"logs\2024-05-03-1229 fwd-TC-udp-t20-P3-b1M-20runs_output.log" # UDP 1Mbps x 3


# file_path = r"old logs\2024-05-05-0307 fwd-TC-t20-P1-20runs_output SUCCESS.log" # SCENARIO 1 FWD
# file_path = r"logs\2024-05-06-2031 fwd-TC-t20-P1-20runs_output SUCCESS.log" # SCENARIO 1 FWD
# file_path = r"old logs\2024-05-05-0356 intent-TC-t20-P1-20runs_output SUCCESS.log" # SCENARIO 1 INTENT
# file_path = r"logs\2024-05-06-2108 intent-TC-t20-P1-20runs_output SUCCESS.log" # SCENARIO 1 INTENT

# file_path = r"logs\2024-05-08-2024 fwd-TC-t20-P1-20runs_output.log" # SCENARIO 1 FWD v3 not that different
# file_path = r"logs\2024-05-08-2100 intent-TC-t20-P1-20runs_output.log" # SCENARIO 1 INTENT v3 not that difference

# max cap 40, mbps 16
# file_path = r"logs\2024-05-05-1707 fwd-TC-t20-P3-20runs_output SUCCESS.log" # SCENARIO 2 FWD
# file_path = r"logs\2024-05-05-1429 intent-TC-t20-P3-20runs_output 14 SUCCESSFUL RUNS.log" # SCENARIO 2 INTENT ONLY 14 RUNS
# file_path = r"logs\2024-05-06-1003 intent-TC-t20-P3-6runs_output.log" # SCENARIO 2 INTENT ONLY 6 RUNS
# file_path = r"logs\2024-05-05-1429 intent-TC-t20-P3-20runs_output COMBINED 20.log" # SCENARIO 2 INTENT
# file_path = r"logs\2024-05-07-1223 intent-TC-t20-P3-20runs_output SUCCESS.log" # SCENARIO 2 INTENT v2
# file_path = r"logs\2024-05-07-0014 fwd-TC-t20-P3-20runs_output SUCCESS.log" # SCENARIO 2 FWD FULL 20 RUNS

# 325 160 4.5 1.1
# file_path = r"old logs\2024-05-05-0808 fwd-TC-udp-t20-P1-b0M-20runs_output SUCCESS.log" # SCENARIO 3 FWD
# file_path = r"logs\2024-05-07-2215 fwd-TC-udp-t20-P1-b0M-20runs_output SUCCESS.log" # SCENARIO 3 FWD v2
# file_path = r"logs\2024-05-06-1024 intent-TC-udp-t20-P1-b0M-20runs_output SUCCESS.log" # SCENARIO 3 INTENT

# 825, 310, 100, 10
# file_path = r"old logs\2024-05-05-1013 fwd-TC-udp-t20-P3-b0M-20runs_output SUCCESS.log" # SCENARIO 4 FWD
# # file_path = # SCENARIO 4 INTENT

# 825, 310, 6, 110
# file_path = r"logs\2024-05-06-2308 fwd-TC-udp-t20-P3-b0M-20runs_output SUCCESS.log" # SCENARIO 4 FWD
# file_path = r"logs\2024-05-06-2339 intent-TC-udp-t20-P3-b0M-20runs_output SUCCESS.log" # SCENARIO 4 INTENT

# 10, 5, 1000, 100
# file_path = r"logs\2024-05-05-2049 fwd-TC-udp-t20-P1-b2M-20runs_output SUCCESS.log" # SCENARIO 5 FWD
# file_path = r"logs/2024-05-06-1513 intent-TC-udp-t20-P1-b2M-20runs_output SUCCESS.log" # SCENARIO 5 INTENT

10, 5, 200, 1
# file_path = r"logs\2024-05-05-2117 fwd-TC-udp-t20-P2-b2M-20runs_output SUCCESS.log" # SCENARIO 6 FWD old
# file_path = r"logs\2024-05-06-1919 fwd-TC-udp-t20-P2-b2M-20runs_output SUCCESS.log" # SCENARIO 6 FWD
# file_path = r"logs\2024-05-06-1950 intent-TC-udp-t20-P2-b2M-20runs_output SUCCESS.log" # SCENARIO 6 INTENT

output = parse_and_print(file_path)
plot(output, ("Capacity of 20s iPerf Test", "Throughput of 20s iPerf Test"), "scenario1")
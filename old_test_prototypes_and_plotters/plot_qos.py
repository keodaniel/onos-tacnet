import matplotlib.pyplot as plt 
import numpy as np
import statistics
import datetime
import os
from time import sleep

def parse_and_print(file_path):
        throughput_list = []
        datagram_loss_list = []

        with open(file_path, "r") as file:
                for line in file:
                        line.strip("\n")
                        if "receiver" in line:
                                for i in line.split("   "):
                                        for j in i.split("  "):
                                                if "bits/sec" in j:
                                                        units = j.split(" ")[1]
                                                        if units == "Mbits/sec":
                                                                throughput_list.append(float(j.split(" ")[0]))
                                                        elif units == "Kbits/sec":
                                                                throughput_list.append(float(j.split(" ")[0]) / 1000)
                                                if "%" in j:
                                                        datagram_loss_list.append(float(j.split()[1].strip("(").strip(")").strip("%")))

        print("Throughput List: ", throughput_list)
        print(f"Throughput Mean: {round(statistics.mean(throughput_list), 4)}, Median: {round(statistics.median(throughput_list), 4)}, Std: {round(statistics.stdev(throughput_list), 4)}")
        if datagram_loss_list:
                print("Datagram Loss List: ", datagram_loss_list)
                print(f"Datagram Loss Mean: {round(statistics.mean(datagram_loss_list), 4)}, Median: {round(statistics.median(datagram_loss_list), 4)}, Std: {round(statistics.stdev(datagram_loss_list), 4)}")

        # print(f"Baseline Throughput Mean: {round(statistics.mean(throughput_list), 4)}, Median: {round(statistics.median(throughput_list), 4)}, Std: {round(statistics.stdev(throughput_list), 4)}")
        # if datagram_loss_list:
        #         print(f"Baseline Datagram Loss Mean: {round(statistics.mean(datagram_loss_list), 4)}, Median: {round(statistics.median(datagram_loss_list), 4)}, Std: {round(statistics.stdev(datagram_loss_list), 4)}")
        
        return (units, throughput_list, datagram_loss_list)

def plot(input, title):
        host_vlan_output, voip_vlan_output, vtc_vlan_output = input
        UNITS = 0
        THROUGHPUT = 1
        DATAGRAM_LOSS = 2

        # Figure 1
        fig1, ax1 = plt.subplots(figsize=(7, 5))
        # PLOT THROUGHPUTS
        ax1.boxplot([host_vlan_output[THROUGHPUT], voip_vlan_output[THROUGHPUT], vtc_vlan_output[THROUGHPUT]])
        ax1.set_title(title[0])
        ax1.set_ylabel(f"Throughput ({host_vlan_output[UNITS][0]}bps)")
        ax1.set_xticklabels(["H1 to H4 Host", "H2 to H5 VOIP", "H3 to H6 VTC"])
        ax1.set_yticks(np.arange(0, 4.5, .25))

        # set meter line at y=3 from at x=1
        ax1.axhline(y=2, xmin=0, xmax=1/3, color='r', linestyle='dashed', label="2Mbps Meter")
        ax1.axhline(y=1, xmin=1/3, xmax=2/3, color='r', linestyle='solid', label="1Mbps Meter")
        ax1.axhline(y=3, xmin=2/3, xmax=1, color='r', linestyle='dotted', label="3Mbps Meter")
        ax1.legend()

        plt.show()

        # save fig as name
        fig1.savefig(f"vlan_plot_throughput.png")
        # fig2.savefig(f"bwplot_packetloss.png")

# No Burst set
# host_vlan = parse_and_print(r"logs\2024-06-02-2111 bw_control_test_host_vlan.log")
# voip_vlan = parse_and_print(r"logs\2024-06-02-2111 bw_control_test_voip_vlan.log")
# vtc_vlan = parse_and_print(r"logs\2024-06-02-2111 bw_control_test_vtc_vlan.log")

# Burst Size 100
host_vlan = parse_and_print(r"logs\2024-06-05-1513_hostvlan.log")
voip_vlan = parse_and_print(r"logs\2024-06-05-1513_voipvlan.log")
vtc_vlan = parse_and_print(r"logs\2024-06-05-1513_vtcvlan.log")

plot_input = [host_vlan, voip_vlan, vtc_vlan]
plot(plot_input, ("Metered Throughput of 5Mbps iPerf Test", "Metered Packet Loss of 10Mbps iPerf Test"))
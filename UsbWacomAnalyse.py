import os
import sys
import matplotlib.pyplot as plt


def analyse_usb_data(data_file, data_type,pcapFilePath):
    os.system(f"tshark -r {pcapFilePath} -T fields -e usb{data_type}.data > {data_file}")
    with open(data_file) as f:
        data = [line.strip() for line in f.readlines() if line.strip()]
    wacom_list = list(set([d[:4] for d in data]))
    for wacom in wacom_list:
        tmp_data = [(int(d[4:6], 16) + int(d[6:8], 16) * 256, int(d[8:10], 16) + int(d[10:12], 16) * 256) for d in data if d[:4] == wacom]
        plt.figure()
        plt.title(f"{data_file}-{wacom}")
        plt.scatter(*zip(*tmp_data),s =5, c='black')
        plt.show()
    os.remove(data_file)


def main():
    if len(sys.argv) != 2:
        print("Wrong! Try:python UsbWacomAnalyse.py pcapfile.pcap")
        exit()
    pcapFilePath = sys.argv[1]
    analyse_usb_data("usb.capdata", "",pcapFilePath)
    analyse_usb_data("usbhid.data", "hid",pcapFilePath)


if __name__ == "__main__":
    main()

import binascii
import itertools
import sys
import zipfile


def crc_brust(zipf_path, mode):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    number = "0123456789"
    allchar = "-_{}"
    if mode == "-a":
        wordlist = alphabet
    elif mode == "-n":
        wordlist = number
    elif mode == "-m":
        wordlist = alphabet + number
    elif mode == "-z":
        wordlist = alphabet + number + allchar
    out = ""

    zipf = zipfile.ZipFile(zipf_path)
    file_list = zipf.namelist()

    for file in file_list:
        count = 0
        zipinfo = zipf.getinfo(file)
        zipf_crc = zipinfo.CRC
        file_size = zipinfo.file_size

        data_list = itertools.product(wordlist, repeat=file_size)

        for data in data_list:
            data = "".join(data)
            data_crc = binascii.crc32(data.encode())

            if data_crc == zipf_crc:
                count += 1
                print(f"filename:{file} crc:{hex(zipf_crc)} data:{data}")
                out += data
        if count == 0:
            print(f"filename:{file} crc:{hex(zipf_crc)} data:Not found")
    return out


def main():
    if len(sys.argv) != 3 or sys.argv[2][-3:] != "zip" or sys.argv[1] == "-h" or (
            sys.argv[1] not in ["-a", "-n", "-m", "-z"]):
        print(
            "Please:\tpython ZipCRCAnlyse.py -a example.zip\n\t[-a] Use alphabet\n\t[-n] Use number\n\t[-m] Use alphabet and number\n\t[-z] Use all")
        exit()

    mode = sys.argv[1]
    zipf_path = sys.argv[2]
    print(crc_brust(zipf_path, mode))


if __name__ == "__main__":
    main()

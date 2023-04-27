import binascii
import struct
import math
import sys
import os


def png_save(file_path, x, y):
    path = os.path.split(file_path)[0]
    file_name = os.path.split(file_path)[1]

    with open(file_path, "rb") as f:
        data_png = f.read()
        out_data = data_png[:16] + struct.pack('>i', x) + struct.pack('>i', y) + data_png[24:]

    with open(path + "\\" + file_name[:-4] + "_fix" + file_name[-4:], "wb") as out_png:
        out_png.write(out_data)


def png_crc_brust(file_path):
    with open(file_path, "rb") as f:
        data_png = f.read()
        crc_data = data_png[12:29]
        crc_origin = binascii.crc32(crc_data)

        crc_bytes = data_png[29:33]
        crc = int(crc_bytes.hex(), 16)

        if crc_origin == crc:
            print("This picture size is right")
            exit()

    for y in range(4095):
        for x in range(4095):
            data = data_png[12:16] + struct.pack('>i', x) + struct.pack('>i', y) + data_png[24:29]
            if binascii.crc32(data) == crc:
                print(f"[Filepath]:{file_path}\n[Width]:{x}\n[Heught]:{y}\n")
                png_save(file_path, x, y)
                exit()


def bmp_save(file_path, pixel_size):
    path = os.path.split(file_path)[0]
    file_name = os.path.split(file_path)[1]

    with open(file_path, "rb") as f:
        data_bmp = f.read()
        width = int.from_bytes(data_bmp[18:22], byteorder="little")
        height = int.from_bytes(data_bmp[22:26], byteorder="little")

    print(f"[Filepath]:{file_path}")
    # mode one: fix_height
    width_tmp = width
    height_tmp = pixel_size // width
    print(f"[Fix_height]:[Width]:{width_tmp}[Height]:{height_tmp}")
    with open(path + "\\" + file_name[:-4] + "_fix_height" + file_name[-4:], "wb") as out_bmp:
        out_data = data_bmp[:18] + struct.pack("<i", width_tmp) + struct.pack("<i", height_tmp) + data_bmp[26:]
        out_bmp.write(out_data)

    # mode two: fix_width
    width_tmp = pixel_size // height
    height_tmp = height
    print(f"[Fix_width]:[Width]:{width_tmp}[Height]:{height_tmp}")
    with open(path + "\\" + file_name[:-4] + "_fix_width" + file_name[-4:], "wb") as out_bmp:
        out_data = data_bmp[:18] + struct.pack("<i", width_tmp) + struct.pack("<i", height_tmp) + data_bmp[26:]
        out_bmp.write(out_data)

    # mode three: sqrt
    width_tmp = height_tmp = int(math.sqrt(pixel_size))
    print(f"[Fix_sqrt]:[Width]:{width_tmp}[Height]:{height_tmp}")
    with open(path + "\\" + file_name[:-4] + "_fix_sqrt" + file_name[-4:], "wb") as out_bmp:
        out_data = data_bmp[:18] + struct.pack("<i", width_tmp) + struct.pack("<i", height_tmp) + data_bmp[26:]
        out_bmp.write(out_data)


def bmp_crc_brust(file_path):
    with open(file_path, "rb") as f:
        data_bmp = f.read()
        bfsize = int.from_bytes(data_bmp[2:6], byteorder="little")
        bfoffbits = int.from_bytes(data_bmp[10:14], byteorder="little")
        bibitcount = int.from_bytes(data_bmp[28:30], byteorder="little")
        pixelsize = (bfsize - bfoffbits) // (bibitcount // 8)
    bmp_save(file_path, pixelsize)


def main():
    if len(sys.argv) != 3 or sys.argv[1] == "-h" or sys.argv[2][-3:].lower() not in ("png", "bmp") or sys.argv[
        1] not in ("-a", "-b", "-p"):
        print(
            "[Wrong!]Please: python PictureSizeAnalyse.py -a picture_file_path\n[Wrong!]Support: PNG BMP\n\t[-a]Auto select\n\t[-b]Select bmp mode\n\t[-p]Select png mode")
        exit()

    file_path = sys.argv[2]
    file_type = sys.argv[2][-3:].lower()

    if sys.argv[1] == "-p":
        png_crc_brust(file_path)
    elif sys.argv[1] == "-b":
        bmp_crc_brust(file_path)
    elif sys.argv[1] == "-a":
        if file_type == "png":
            png_crc_brust(file_path)
        elif file_type == "bmp":
            bmp_crc_brust(file_path)


if __name__ == "__main__":
    main()

import sys
import os

normalKeys = {"04":"a", "05":"b", "06":"c", "07":"d", "08":"e", "09":"f", "0a":"g", "0b":"h", "0c":"i", "0d":"j", "0e":"k", "0f":"l", "10":"m", "11":"n", "12":"o", "13":"p", "14":"q", "15":"r", "16":"s", "17":"t", "18":"u", "19":"v", "1a":"w", "1b":"x", "1c":"y", "1d":"z","1e":"1", "1f":"2", "20":"3", "21":"4", "22":"5", "23":"6","24":"7","25":"8","26":"9","27":"0","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"\t","2c":"<SPACE>","2d":"-","2e":"=","2f":"[","30":"]","31":"\\","32":"<NON>","33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}
shiftKeys = {"04":"A", "05":"B", "06":"C", "07":"D", "08":"E", "09":"F", "0a":"G", "0b":"H", "0c":"I", "0d":"J", "0e":"K", "0f":"L", "10":"M", "11":"N", "12":"O", "13":"P", "14":"Q", "15":"R", "16":"S", "17":"T", "18":"U", "19":"V", "1a":"W", "1b":"X", "1c":"Y", "1d":"Z","1e":"!", "1f":"@", "20":"#", "21":"$", "22":"%", "23":"^","24":"&","25":"*","26":"(","27":")","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"\t","2c":"<SPACE>","2d":"_","2e":"+","2f":"{","30":"}","31":"|","32":"<NON>","33":"\"","34":":","35":"<GA>","36":"<","37":">","38":"?","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}

# 获取 usbhid.data 列表
def analyse_usbhid_data(pcapFilePath,src,argument):
    usbhid_data = []
    os.system("tshark -r {} -T fields -e usbhid.data \"usb.data_len == 8 && usb.src == {}\" > usbhid.data".format(pcapFilePath,src))
    with open("usbhid.data") as f:
         for line in f:
             usbhid_data.append(line.strip())
    result(usbhid_data,src,argument,"usbhid.data")
    os.remove("usbhid.data")

# 获取 usb.capdata 列表
def analyse_usb_capdata(pcapFilePath,src,argument):
    usb_capdata = []
    os.system("tshark -r {} -T fields -a usb.capdata \"usb.data_len == 8 && usb.src == {}\" > usb.capdata".format(pcapFilePath,src))
    with open("usb.capdata") as f:
        for line in f:
            usb_capdata.append(line.strip())
    result(usb_capdata,src,argument,"usb.capdata")
    os.remove("usb.capdata")

# 获取 usb流量分析
def result(presses,src,argument,path):
    result = ""

    for press in presses:
        if press == '':
            continue
        if ':' in press:
            Bytes = press.split(":")
        else:
            Bytes = [press[i:i+2] for i in range(0, len(press), 2)]
        if Bytes[0] == "00":
            if Bytes[2] != "00" and normalKeys.get(Bytes[2]):
                result += normalKeys[Bytes[2]]
        elif int(Bytes[0],16) & 0b10 or int(Bytes[0],16) & 0b100000: # shift key is pressed.
            if Bytes[2] != "00" and normalKeys.get(Bytes[2]):
                result += shiftKeys[Bytes[2]]

        if argument == "-b":
            result = result.replace("<RET>","").replace("<ESC>","").replace("<DEL>","").replace("<SPACE>","").replace("<GA>","").replace("<CAP>","").replace("\t","").replace("F1","").replace("F2","").replace("F3","").replace("F4","").replace("F5","").replace("F6","").replace("F7","").replace("F8","").replace("F9","").replace("F10","").replace("F11","").replace("F12","")

    if result != "":
        print("[",src,path,"]",result,"\n")

def error():
    #输入 -a 则全部输出，输入 -b 则将过滤 <DEL> <ESC> 之类的符号
    print("Example:\n\tpython UsbKeyboardDataAnalyse.py -a  data.pcapng\nArgument:\n\t[-a]:Output all data.\n\t[-b]:Output only common characters.")
    exit()
    
def main():
    # 判断输入参数
    if len(sys.argv) != 3 or (sys.argv[1] not in ["-a", "-b", "-h"]):
        error()
        
    # 获取流量文件路径 // 获取 usb.src 列表
    argument = sys.argv[1]
    pcapFilePath = sys.argv[2]
    usb_src = []
    os.system("tshark -r {} -T fields -e usb.src > usb.src".format(pcapFilePath))
    with open("usb.src") as f:
        for line in f:
            if line.strip() not in usb_src:
                usb_src.append(line.strip())
    os.remove("usb.src")

    for src in usb_src:
        analyse_usbhid_data(pcapFilePath, src, argument)
        analyse_usb_capdata(pcapFilePath, src, argument)

if __name__ == '__main__':
    main()

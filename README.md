### CTF-misc-script

---

| 脚本 | 作用 | 文件类型 |
| --- | --- | --- |
| PictureSizeAnalyse | 计算图片正确宽高 | bmp图片，png图片 |
| ZipCRCAnlyse | 多文件压缩包CRC爆破 | zip，rar，7z |
| UsbKeyboardDataAnalyse | USB键盘流量分析 | pcap，pcapng |
| UsbWacomAnalyse | USB数位板流量分析 | pcap，pcapng |

### PictureSizeAnalyse

---

```
适用平台：Windows/Kali
参数：
	-h 查看help
	-a 自动选择模式
	-b 使用 bmp 模式分析正确宽高
	-p 使用 png 模式分析宽高
使用：
	python 模式 文件路径
	python PictureSizeAnalyse.py -a test.png
```
### ZipCRCAnlyse

---

```
适用平台：Windows/Kali
参数：
	-h 查看help
	-a 使用字母字符集碰撞
	-n 使用数字字符集碰撞
	-m 使用字母字符集碰撞 和 数字字符集碰撞
	-z 尝试 chr(1~128) 字符集碰撞
使用：
	python 模式 文件路径
	python PictureSizeAnalyse.py -a test.zip
```
### UsbKeyboardDataAnalyse

---

```
适用平台：Kali
参数：
	-h 查看help
	-a 结果输出完整内容
	-b 结果只输出字符
使用：
	python 模式 文件路径
	python PictureSizeAnalyse.py -a test.pcapng
```
### UsbWacomAnalyse

---

```
适用平台：Kali
使用：
	python 文件路径
	python UsbWacomAnalyse.py test.pcapng
```

#
# import smtplib
#
# from email.mime.text import MIMEText
#
#
# msg = MIMEText('content') # 文本内容
# msg['Subject'] = "title" # 文本标题
# msg['From'] = 'lanmszhang@163.com' # 写邮件的人的网址
# msg['To'] = '1367000465@qq.com' # 收邮件的地址
#
# s = smtplib.SMTP('location') # 也可以下远程主机的 IP 让远程主机发送邮件
# s.send_message(msg)
# s.quit()

#
#
# import smtplib
# import time
# from email.mime.text import MIMEText
#
# from urllib.request import urlopen
# from bs4 import BeautifulSoup
#
#
# def sendMail(subject, body):
#     msg = MIMEText(body)
#     msg['Subject'] = subject
#     msg['From'] = ''
#     msg['To'] = ''
#
#     s = smtplib.SMTP('location')
#     s.send_message(msg)
#     s.quit()
#
#
# bsObj = BeautifulSoup(urlopen('https://isitchirstms.com、'))
# while (bsObj.find('a', {'id', 'answer'}).attrs['title'] == 'NO'):
#     print('不是 需要的页面')
#     time.sleep(100)
# bsObj = BeautifulSoup(urlopen('https://isitchristmas.com/'))
# sendMail("It's Christmas!", 'body')


from io import StringIO

from urllib.request import urlopen, Request
import csv

# req = Request('http:/pythonscraping.com/files/MontyPythonAlbums.csv')
# data = urlopen('http:/pythonscraping.com/files/MontyPythonAlbums.csv').read().decode('ascii', 'ignore')
# dataFile = StringIO(data)

# with open('./file/MontyPythonAlbums.csv', 'r') as f:
#     with open('test.csv', 'w') as t:
#
#         csvReader = csv.reader(f) # 读取文件
#         for row in csvReader:
#             print(row)
#             writer = csv.writer(t)
#             # 写入文件  注意的是这里的 row 是一个列表， 里面是一行所有字段的信息
#             writer.writerow(row)
#             # 写入多行
            # writer.writerows(row1, row2, row3)



# from urllib.request import urlopen
# from pdfminer.pdfinterp import PDFResourceManager, process_pdf
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from io import StringIO
#
#
# def readPDF(pdfFile):
#     rsrcmgr = PDFResourceManager()
#     retstr = StringIO()
#     laparams = LAParams()
#     device = TextConverter(rsrcmgr=rsrcmgr, outfp=retstr, laparams=laparams)
#
#     process_pdf(rsrcmgr=rsrcmgr, device=device, fp=pdfFile)
#
#     device.close()
#     content = retstr.getvalue()
#     retstr.close()
#     return content


# 第一步从文件读取 XML:

import re
from zipfile import ZipFile
from io import BytesIO, StringIO


def readDocx(wordFile):
    """
    读取 .docx 文件的内容
    :param wordFile:  目标文件
    :return: 文档的文字内容
    """
    content = StringIO()
    # 获取网络文档
    wordFile = BytesIO(wordFile)
    # 因为所有的 .docx 文件都是经过压缩的， 所以需要进行解压
    document = ZipFile(wordFile)
    # 读取文件， 指定文件的格式为 xml
    xml_content = document.read('word/document.xml')

    # wordObj = BeautifulSoup(xml_content.decode('utf-8'), 'lxml')
    # 所有的正文内容都在 <w:t> 标签中， 标题也是一样， 标题只是在外面套了一层标签
    # textStrings = wordObj.findAll("w:t")

    # # 通过 etree 获取  传入 bytes 对象即可
    # wordObj = etree.HTML(xml_content)
    # textStrings = wordObj.xpath('//*w:t')

    # 正则匹配
    content = xml_content.decode('utf-8')
    pattern = re.compile(r'<w:t[>](.*?)</w:t>', re.S)
    textStrings = re.findall(pattern, content)
    print(textStrings)
    for textElem in textStrings:
        c = textElem
        print(c)

    # return content


with open('./file/AWordDocument.docx', 'rb') as f:
    c = readDocx(f.read())
    # print(c)


"""
内容  content 

r'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" mc:Ignorable="w14 w15 wp14"><w:body><w:p w:rsidR="00764658" w:rsidRDefault="00764658" w:rsidP="00764658"><w:pPr><w:pStyle w:val="Title"/></w:pPr><w:r><w:t>A Word Document on a Website</w:t></w:r><w:bookmarkStart w:id="0" w:name="_GoBack"/><w:bookmarkEnd w:id="0"/></w:p><w:p w:rsidR="00764658" w:rsidRDefault="00764658" w:rsidP="00764658"/><w:p w:rsidR="00764658" w:rsidRPr="00764658" w:rsidRDefault="00764658" w:rsidP="00764658"><w:r><w:t>This is a Word document, full of content that you want very much. Unfortunately, it’s difficult to access because I’m putting it on my website as a .</w:t></w:r><w:proofErr w:type="spellStart"/><w:r><w:t>docx</w:t></w:r><w:proofErr w:type="spellEnd"/><w:r><w:t xml:space="preserve"> file, rather than just publishing it as HTML</w:t></w:r></w:p><w:sectPr w:rsidR="00764658" w:rsidRPr="00764658"><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/><w:cols w:space="720"/><w:docGrid w:linePitch="360"/></w:sectPr></w:body></w:document>'

"""
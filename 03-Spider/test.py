#
# from io import StringIO
#
#
# s = StringIO()
# s.write('www.baidu.com\n')
# s.write('abc\n')
# s.write('zhang')
#
#
# o = s.getvalue()
# print(o)
#
#
# s.seek(0)  # 指定开始读取的位置
# while True:
#     strBuf = s.readline()
#     if not strBuf:
#         break
#     print(strBuf, end='')
#
# s.close()
#
#


# class Test():
#
#     def __init__(self):
#         self.name = 'test'
#         self.num = 12
#
#     def __str__(self):
#         return self.name
#
#
# t = Test()
# assert(t == 'test')
# print(type(t))

import re


s = r"""
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n
    <w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" mc:Ignorable="w14 w15 wp14"><w:body><w:p w:rsidR="00764658" w:rsidRDefault="00764658" w:rsidP="00764658">
    <w:pPr><w:pStyle w:val="Title"/></w:pPr><w:r><w:t>A Word Document on a Website</w:t></w:r>
    <w:bookmarkStart w:id="0" w:name="_GoBack"/><w:bookmarkEnd w:id="0"/></w:p>
    <w:p w:rsidR="00764658" w:rsidRDefault="00764658" w:rsidP="00764658"/>
    <w:p w:rsidR="00764658" w:rsidRPr="00764658" w:rsidRDefault="00764658" w:rsidP="00764658"><w:r>
    <w:t>This is a Word document, full of content that you want very much. 
    Unfortunately, it’s difficult to access because I’m putting it on my website as a .</w:t>
    </w:r><w:proofErr w:type="spellStart"/><w:r>
    
    <w:t>docx</w:t>
    
    </w:r><w:proofErr w:type="spellEnd"/>
    <w:r>
    
    <w:t xml:space="preserve"> file, rather than just publishing it as HTML</w:t>
    
    </w:r></w:p><w:sectPr w:rsidR="00764658" w:rsidRPr="00764658"><w:pgSz w:w="12240" w:h="15840"/>
    
    <w:t>hello</w:t>
    
    <w:t tetrs>test<w:t>
    <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" 
    w:footer="720" w:gutter="0"/><w:cols w:space="720"/><w:docGrid w:linePitch="360"/>
    </w:sectPr></w:body>
    </w:document>

    """

# pattern = re.compile(r'<w:t[>](.*?)</w:t>', re.S)
#
# result = re.findall(pattern, s)
#
# print(result)



import re
from zipfile import ZipFile
from io import BytesIO, StringIO


def readDocx(filePath):
    """
    读取 .docx 文件

    :param filePath: 文件路径
    :return:  文件内所有内容的列表
    """
    with open(filePath, 'rb',) as f:
        wordFile = f.read()
        # 二进制文件
        wordFile = BytesIO(wordFile)
        # 因为所有的 .docx 文件都是经过压缩的， 所以需要进行解压
        document = ZipFile(wordFile)
        # 读取文件， 指定文件的格式为 xml
        xml_content = document.read('word/document.xml')
        # 正则匹配 需要的内容
        content_str = xml_content.decode('utf-8')
        pattern = re.compile(r'<w:t[>](.*?)</w:t>', re.S)
        content_list = re.findall(pattern, content_str)
        return content_list


p = r'./AWordDocument.docx'
c = readDocx(p)
print(c)



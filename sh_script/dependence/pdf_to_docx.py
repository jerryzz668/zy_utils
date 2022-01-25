"""
@Description: 
@Author     : zhangyan
@Time       : 2022/1/25 下午5:24
"""
import sys
from pdf2docx import Converter

pdf_file = sys.argv[1]
docx_file = pdf_file.replace('.pdf', '.docx')

# convert pdf to docx
cv = Converter(pdf_file)
cv.convert(docx_file, start=0, end=None)
cv.close()
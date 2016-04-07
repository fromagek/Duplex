# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 11:46:57 2016

@author: florian
"""
from pyPdf import PdfFileWriter, PdfFileReader
import easygui
import os
import tkFileDialog

def append_pdf(input,output):
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

def interleave(a,b):
    c=a+b
#    print c,"\n\n"
#    print c[::2]
    c[::2] = a
    c[1::2] = b
    return c
            
#user_input_first_PDF=easygui.fileopenbox("PDF mit erster seite angeben (Vorderseite)")
#user_input_second_PDF=easygui.fileopenbox("PDF mit zweiter seite angeben (R)")

user_input_first_PDF=tkFileDialog.askopenfilename()
user_input_second_PDF=tkFileDialog.askopenfilename()

work_dir=os.path.dirname(user_input_first_PDF)

os.chdir(work_dir)
print user_input_first_PDF
print os.path.dirname(user_input_first_PDF)
#print user_input_first_PDF.index('/')
#print os.path.basename(user_input_first_PDF)[:-4]

inputpdf1 = PdfFileReader(open(user_input_first_PDF, "rb"))
inputpdf2 = PdfFileReader(open(user_input_second_PDF, "rb"))

inputpdf_list=[inputpdf1,inputpdf2]
#print inputpdf1

pdfs=[os.path.basename(user_input_first_PDF)[:-4],os.path.basename(user_input_second_PDF)[:-4]]

pdf_list=[]
pdf_list2=[]
for j,pdf in enumerate(pdfs):
    for i in xrange(inputpdf1.numPages):
#        print "j=",j
        output = PdfFileWriter()
        output.addPage(inputpdf_list[j].getPage(i))
        with open(pdf+"_einzeln_%s.pdf" % i, "wb") as outputStream:
            output.write(outputStream)
        pdf_list.append(pdf+"_einzeln_%s.pdf" % i)
        

#print "jajajajjajaj",pdf_list,inputpdf1.numPages,"\n\n"

pdf_list1=pdf_list[:inputpdf1.numPages]
pdf_list2=pdf_list[inputpdf1.numPages:]
pdf_list2.reverse()

#print pdf_list[:inputpdf1.numPages]

pdf_list_final= interleave(pdf_list1,pdf_list2)


output = PdfFileWriter()
for page in pdf_list_final:
#    print page
    append_pdf(PdfFileReader(file(page,"rb")),output)
    os.remove(page)

#print os.getcwd()
output_path=os.path.join(work_dir,"combined.pdf")
#output_path=os.path.join(os.path.dirname(user_input_first_PDF),"combined.pdf")

output.write(file(output_path,"wb"))


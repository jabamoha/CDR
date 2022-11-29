
# import the CDR processes...
from Components.PPTProcessor import DisableLinks as PPTLinks,DisableMacro as PPTMacro
from Components.PDFprocessor import Clean_Pdf_From_ClickAbles as PDFLinks,ANALYZE_AND_DISARM as PDF_JS
from Components.DocumentProcessor import DisableLinks as DOCLinks,DisableMacros as DOCMAcros
from Components.ExcelProcessor import DisableLinks as EXCELLinks,DisableMacros as EXCELMacros
from Components.imageProcess import clean_jpeg,clean_png 
from Components.CompressedProcessor import ZipEncrypted


# import the python packages

from threading import Thread




# declare a class to work with multi emails in same time(sync.)
class EmailProcess:
    
    def __init__(self,files : list[str]):
        """_summary_

        Args:
            files (list[str]): list of paths
        """
        self.Processes = {
            "pptm":[PPTMacro,PPTLinks],
            "ppt":[PPTLinks],
            "pdf":[PDFLinks,PDF_JS],
            "docx":[DOCLinks],
            "docm":[DOCMAcros,DOCLinks],
            "xlsx":[EXCELLinks],
            "xlsm":[EXCELMacros],
            "jpeg":[clean_jpeg],
            "jpg":[clean_jpeg],
            "png":[clean_png],
            "zip":[ZipEncrypted]
        }
        self._files = files
        self.Extensions = {}
        for file in files:
            extension = file.split('.')[-1]
            if extension in self.Processes:
                if extension not in self.Extensions:
                    self.Extensions[extension] = [file]
                else:
                    self.Extensions[extension].append(file)
        
        
    def CDR(self):
        for ext in self.Extensions:
            print(self.Extensions[ext])
            for filepath in self.Extensions[ext]:
                print(filepath)
                for CDR_func in self.Processes[ext]:
                    CDR_func(filepath)        
            
        print('----------------CDR-----------------')
            



from PDFprocessor import ANALYZE_AND_DISARM as jsClean,Clean_Pdf_From_ClickAbles as DisableClickAbles
import os

import PPTProcessor
import DocumentProcessor
import imageProcess as ImageProcessor
from macpath import dirname


images_processing = {'png':ImageProcessor.clean_png , 'jpeg':ImageProcessor.clean_jpeg , 'jpg':ImageProcessor.clean_jpeg}


class PDFProcess:
    
    def __init__(self,filepath):
        self._file = filepath
        self._dirpath = os.path.dirname(filepath)
        self._filename = os.path.basename(filepath)
    
    def processor(self):
        print('----------------Starting cleaning PDF-----------------')
        logs = DisableClickAbles(self._file)
        jsClean(self._file)
        print('----------------The PDF is Safe-----------------')
        return logs

    
class PPTProcess:
    
    def __init__(self,filepath):
        self._filename = os.path.basename(filepath)
        self._dirpath = os.path.dirname(filepath)
        self._file= filepath
        
    def processor(self):
        print('-----------------Starting cleaning Power Point------------')
        macro_logs,filename=PPTProcessor.DisableMacro(self._file)
        self._filename = filename
        self._file = self._dirpath + '\\' + self._filename
        links_logs = PPTProcessor.DisableLinks(self._file)
        del filename

        print('----------------The Power Point File is Safe-----------------')
        
        return macro_logs if links_logs is None else links_logs if macro_logs is None else macro_logs + links_logs 


class DocumentProcess:
    
    def __init__(self,filepath):
        self._file = filepath
        self._filename = os.path.basename(filepath)
        self._dirpath = os.path.dirname(filepath)
    
    def processor(self):
        print('---------------Starting Cleaning Word File--------------')
        macro_logs,filename = DocumentProcessor.DisableMacros(self._file,self._filename)
        self._filename = filename
        self._file = self._dirpath + '\\' + self._filename
        del filename
        links_logs = DocumentProcessor.DisableLinks(self._file)
        print('---------------The Word file is safe now--------------')

        return macro_logs if links_logs is None else links_logs if macro_logs is None else macro_logs + links_logs 
                
                       
class ImageProcess:
    
    def __init__(self,filepath):
        self._file = filepath
        self._filename = str(os.path.basename(filepath))
        self._type = self._filename.split('.')[-1]
        self._dirpath = os.path.dirname(filepath)
    
    def processor(self):
        if self._type in images_processing.keys():
            print('-------------Starting Cleaning Image-------------')
            images_processing[self._type](self._file)
            print('-------------The Image file is safe now-----------')                    
        else:
            print('------------Image type not supported--------------')


import ExcelProcessor

class ExcelProcess:
    def __init__(self,filepath):
        self._file = filepath
        self._filename = str(os.path.basename(filepath))
        self._type = self._filename.split('.')[-1]
        self._dirpath = os.path.dirname(filepath)
    
    def processor(self):
        macro_logs = ExcelProcessor.DisableMacros(self._file)
        links_logs = ExcelProcessor.DisableLinks(self._file)
        return macro_logs + links_logs
    


import SpamProcessor

class SpamProcess:
    
    def __init__(self,message):
        self._message = message
        
    def processor(self):
        return SpamProcessor.Analyze_Message(message=self._message)

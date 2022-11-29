import pprint
import pdfrw
from pdfid import pdfid
import os 

pp = pprint.PrettyPrinter(indent=4)

TEST_FILENAME = "pdf.pdf"

def Name_analyze(filenames):
    options = pdfid.get_fake_options()
    options.scan = True
    options.json = True
    
    list_of_dict = pdfid.PDFiDMain(filenames, options)

    return list_of_dict

def Buffer_analyze(filenames, file_buffers):
    options = pdfid.get_fake_options()
    options.scan = True
    options.json = True

    list_of_dict = pdfid.PDFiDMain(filenames, options, file_buffers)
    return list_of_dict

def disarm_pdfs_by_buffer(filenames, file_buffers):
    options = pdfid.get_fake_options()

    options.disarm = True
    
    options.return_disarmed_buffer = True

    # disarm
    disarmed_pdf_buffers = pdfid.PDFiDMain(filenames, options, file_buffers)
    return disarmed_pdf_buffers




def Clean_Pdf_From_ClickAbles(filepath):
    """_summary_

    Args:
        dirpath (str): Directory path of the file that need to clean
        filename (str): file name with extension

    Returns:
        str,list[str] : the new name of the safe file , list of logs 
    """
    
    pdf = pdfrw.PdfReader(filepath)
    new_pdf = pdfrw.PdfWriter()  
    logs = []
    print('----------Starting Clean PDF from ClickAbles-----------')
    for page in pdf.pages:  

        for annot in page.Annots or []:
            old_url = annot.A.URI
            log = f'[-]Remove {old_url}'
            print(log)
            logs.append(log)
            new_url = pdfrw.objects.pdfstring.PdfString("#")
            annot.A.URI = new_url

        new_pdf.addpage(page)   
    new_pdf.write(filepath)
    del new_pdf,pdf
    print('----------Successfully Clean PDF from ClickAbles-----------')
    return logs




def ANALYZE_AND_DISARM(fileDST):
    filenames = [fileDST]
    file_buffers = []
    for filename in filenames:
        with open(filename, "rb") as f:
            file_buffers.append(f.read())
            f.close()
    print("analyzing file by name ,")
    results_1 = Name_analyze(filenames)
    pp.pprint(results_1)

    print("initiating buffer analyzing")
    results_2 = Buffer_analyze(filenames, file_buffers)
    pp.pprint(results_2)

    print("STARTING DISARM")
    disarmed_pdf_buffers = disarm_pdfs_by_buffer(filenames, file_buffers)

    print("STARTING DISARMED ANALYSIS")
    results_3 = Buffer_analyze(filenames, disarmed_pdf_buffers['buffers'])
    pp.pprint(results_3)
 





# if __name__ == "__main__":
#     # Clean_Pdf_From_ClickAbles()
#     my_input="./pdf.pdf"
#     my_output="new.pdf"
#     ANALYZE_AND_DISARM('pdf.pdf')
#     print("ok")
    

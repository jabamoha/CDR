from zipfile import ZipFile
import PDFprocessor as pdf,DocumentProcessor as doc,imageProcess as img,ExcelProcessor as excel,PPTProcessor as ppt
# the exe extensions which we will delete them from any archive file 
import os
EXE_EXTENSIONS = (
                  '.bms','.msi','.ahk','.apk','.jar','.ipa','.run','.cmd','.xbe','.0xe',
                  '.exe','.workflow','.bin','.elf','.8ck','.bat','.sk','.air',
                  '.gadget','.xap','.ac','.widget','.app','.u3p','.pif','.fpa',
                  '.rbf','.mcr','.com','.sh','.tpk','.out','.x86','.73k','.ex_',
                  '.rxe','.command','.xex','.x86_64','.ebs2','.a7r','.plx','.nexe',
                  '.exe1','.pyc','.e_e','.spr','.uvm','.osx','.vexe','.upx','.ore','.ezt'
                  )





# files_processes[(dot)extension:str] = List[CDR Functions] 
files_processes= {
                  '.pdf':[pdf.ANALYZE_AND_DISARM,pdf.Clean_Pdf_From_ClickAbles],
                  '.docx':[doc.DisableLinks],'.docm':[doc.DisableMacros,doc.DisableLinks],
                  '.pptx':[ppt.DisableLinks],'.pptm':[ppt.DisableMacro,ppt.DisableLinks],
                  '.jpeg':[img.clean_jpeg],'.jpg':[img.clean_jpeg],'.png':[img.clean_png],
                  '.xlsx':[excel.DisableLinks],'.xlsm':[excel.DisableMacros]
                  }





def ZipEncrypted(file):
        """Check if the archive file(zip) has a password

        Args:
            file (str): path to the archive file (.zip)

        Returns:
            bool: True if the file has password, else False
        """
        zf = ZipFile(file)
        for zinfo in zf.infolist():
            is_encrypted = zinfo.flag_bits & 0x1
            if is_encrypted:
                zf.close()
                os.remove(file)
                return True
        return False
        
    
    
    
    
    


# import os

# def CleanZip(filepath):
#     dirpath = os.path.dirname(filepath)
#     filename = 'CDR_'+os.path.basename(filepath)
#     z_in = ZipFile(filepath,'r')
#     z_out = ZipFile(dirpath+'\\'+filename,'w')
#     logs = {}
    
#     return ZipProcessor(z_in,z_out,logs=logs,dirpath=os.path.dirname(filepath))
    
# def ZipProcessor(z_in : ZipFile, z_out : ZipFile , dirpath : str, logs : dict):
#     if z_in is None:
#         return z_out
#     infolist = z_in.infolist()
#     # print(infolist)
#     for item in infolist:
#         filename = item.filename
#         print(filename)
#         file_extension ='.'+ filename.split('.')[-1]
#         if file_extension in EXE_EXTENSIONS:
#             continue
#         elif file_extension in files_processes:
#             # extract the file to the dirpath
#             z_in.extract(filename, path=dirpath)
#             file_to_process = dirpath + '\\' + filename
#             for obj in files_processes.get(file_extension):
#                 file_logs = obj(file_to_process)
#                 if file_logs is not None:
#                     if filename in logs:
#                         logs[filename] = logs[filename] + file_logs
#                     else:
#                         logs[filename] = file_logs 
#             z_out.write(filename,file_to_process)
#         elif file_extension[1:] in archive_processes:
#             z_in.extract(filename,path=dirpath)
#             archive_to_process = dirpath+'//'+filename
#             archive_processes[file_extension[1:]](archive_to_process)
#             z_out.write(archive_to_process,filename)
#         else:
#             buffer = z_in.read(filename)
#             z_out.writestr(item,buffer)
#             del buffer
#     z_in.close()
#     z_out.close()
#     return z_in,logs
        





# def Clean_gz(filepath):
#     pass

# def Clean_7z(filepath):
#     pass

# def Clean_rar(filepath):
#     pass

# def Clean_z(filepath):
#     pass


# archive_processes = {'gz':Clean_gz,
#                      '7z':Clean_7z,
#                      'rar':Clean_rar,
#                      'z':Clean_z,
#                      'zip':CleanZip
#                      }



# # CleanZip('C:\\temp\\NAC\\FinalProject\\CDRFP\\CDRFinal\\CDR_Processor\\Mohammad_Jabareen_Resume.zip')
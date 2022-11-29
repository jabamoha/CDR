from fileinput import filename
from PIL import Image
import numpy as np
# import sys 


def clean_png(file):
    print('Cleanning starting')

    im = Image.open(file)                                     

    na = np.array(im)                                                                       
    print('format Converted')                                                                      
    # Create new image from the Numpy array
    result = Image.fromarray(na)

    # Copy forward the palette, if any
    palette = im.getpalette()
    if palette != None:
        result.putpalette(palette)

    result.save(file)
    print('File cleaned successfully')



# Load image
def clean_jpeg(file):

    print('Cleanning starting')
    imJP = Image.open(file)                                     

    # Convert to format that cannot store IPTC/EXIF or comments, i.e. Numpy array
    naJP= np.array(imJP) 
    print('format Converted')                                                                      

    # Create new image from the Numpy array and save
    result = Image.fromarray(naJP).save(file)
    print('File cleaned successfully')




# filename=sys.argv[1]

# if filename[-3:] == 'png':
#     clean_png(filename)
# elif filename[-3:] == 'jpg':
#     clean_jpeg(filename)
# elif filename[-4:] == 'jpeg':
#     clean_jpeg(filename)
# else :
#     print('File type not supported')
# yolo keras label format row : image_file_path box1 box2 ... boxN
#                         box : x_min,y_min,x_max,y_max,class_id

from xml.dom import minidom
import os
import glob

path = os.getcwd()
class_id = {'apple' : 1, 'banana' : 2, 'orange' : 3}

def convert_xml2yolo():
    #xml name + txt
    fname_out = ('test'+'.txt')

    #get number of xml file
    for fname in glob.glob("*.xml"):
        
        #parsing
        xmldoc = minidom.parse(fname)
        
        with open(fname_out, "a") as f:

            itemlist = xmldoc.getElementsByTagName('object')

            for item in itemlist:
                # get class label
                class_name =  (item.getElementsByTagName('name')[0]).firstChild.data

                # get bbox coordinates
                xmin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
                ymin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
                xmax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
                ymax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data

                fname_txt = os.path.splitext(fname)

                print(fname_txt)
                f.write(str(path) + "/" + str(fname_txt[0]) + ".jpg " + str(xmin) + "," + str(ymin) + "," + str(xmax) + "," + str(ymax)  + "," + str(class_id[class_name]) + '\n')

    print ("wrote %s" % fname_out)

convert_xml2yolo()

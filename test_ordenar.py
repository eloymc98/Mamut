
import os
import glob
import shutil

if __name__ == '__main__':
    count = int(input('count = ?'))
    path = r'E:\Residus\Marro'
    images = glob.glob(os.path.join(path,'*','*.jpg'))
    print(images)

    for image in images:
        print(image)
        #filename = 'brown' + str(count)
        #new_name = image.replace(image.split(os.sep)[-1],filename)
        #os.rename(image,image.replace(image.split(os.sep)[-1],filename))
        shutil.copy(image,path)


    #images = glob.glob(os.path.join(path,'*.jpg'))
    #for image in images:
    #    filename = 'brown' + str(count)
     #   os.rename(image,image.replace(image.split(os.sep)[-1],filename))
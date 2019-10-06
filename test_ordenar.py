import os
import glob
import random
import shutil

if __name__ == '__main__':
    count = int(input('count = ?'))
    path = r'/Users/eloymarinciudad/Downloads/dataset-resized/brown'
    images = glob.glob(os.path.join(path, '*.jpg'))
    print(images)
    #random.shuffle(images)
    for image in images:
        #print(image)
        filename = 'brown' + str(count)+'.jpg'
        #filename = str(count)+'.jpg'

        #new_name = image.replace(image.split(os.sep)[-1],filename)
        #os.remove(image)
        os.rename(image, image.replace(os.path.basename(image), filename))
        count += 1

    # images = glob.glob(os.path.join(path,'*.jpg'))
    # for image in images:
    #    filename = 'brown' + str(count)
    #   os.rename(image,image.replace(image.split(os.sep)[-1],filename))

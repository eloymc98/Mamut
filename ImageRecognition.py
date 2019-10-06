from fastai.vision import *


class CNN:

    def __init__(self):
        self.prediction_recycle = {"plastic": "yellow dumper", "paper": "blue dumper", "metal": "yellow dumper",
                                   "green_point": "green point", "glass": "green dumper", "cardboard": "blue dumper",
                                   "brown": "brown dumper"}
        self.learn = load_learner(r'C:\Users\Mephistopheles\Documents\Mamut\model2')

    def predict_image(self, img_path):
        img = open_image(img_path)
        pred_class, pred_idx, outputs = self.learn.predict(img)
        print(pred_class)
        return self.predict_to_recycle(str(pred_class))

    def predict_to_recycle(self, prediction):
        recycle_string = f'This is {prediction if prediction != "green_point" else "special"}, you ought to throw into the ' \
                         f'{self.prediction_recycle[prediction]}'
        #recycle_string = f'You ought to throw into the {self.prediction_recycle[prediction]}'
        return recycle_string


if __name__ == '__main__':
    predict = CNN()
    predict.predict_image()

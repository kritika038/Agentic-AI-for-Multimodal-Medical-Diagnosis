import pickle
import cv2
import os
import numpy as np
from sklearn.metrics import classification_report

model = pickle.load(open("models/xray_model.pkl","rb"))

data=[]
labels=[]

path="dataset/pneumonia/test"
classes=["NORMAL","PNEUMONIA"]

for c in classes:
    folder=os.path.join(path,c)
    label=classes.index(c)

    for img in os.listdir(folder)[:100]:
        img_path=os.path.join(folder,img)

        image=cv2.imread(img_path,0)
        image=cv2.resize(image,(64,64))

        data.append(image.flatten())
        labels.append(label)

X=np.array(data)

pred=model.predict(X)

print(classification_report(labels,pred))

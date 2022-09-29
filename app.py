
from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import cv2
import PIL 
from PIL import Image
import subprocess
import torch
from matplotlib import pyplot as plt
import pickle
import shutil
from OCRdataextract import ocr_extract
from maketable import table1
# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'model_vgg16.h5'

# Load your trained model
model = load_model(MODEL_PATH)
model.make_predict_function()          # Necessary


def png_to_jpg(file_name):
    source = r"C:\Users\User\Documents\Semester 8-A\CodeFest3\uploads"
    slash = '//'
    source = source + slash + file_name
    if '.png' in file_name:
        path = r"C:\Users\User\Documents\Semester 8-A\CodeFest3\uploads"
        os. chdir(path)
        image = cv2.imread(source)
        cv2.imwrite('abc.jpg', image)
        path1 = r"C:\Users\User\Documents\Semester 8-A\CodeFest3"
        os.chdir(path1)

        
        #fil = file_name.replace('.png', '.jpg')
        #dest = r"C:\Users\User\Documents\Semester 8-A\CodeFest\uploads"
        #dest = dest + slash + fil
        
        #img_png = Image.open(source)
        #rgb_im = img_png.convert('RGB')
        #rgb_im.save(dest)"""
    elif '.jpeg' in image:
        fil = image.replace('.jpeg', '.jpg')
        dest = r"C:\Users\User\Documents\Semester 8-A\CodeFest3\uploads"
        dest = dest + slash + fil
        
        img_jpeg = Image.open(source)
        rgb_im = img_jpeg.convert('RGB')
        rgb_im.save(dest)
               


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    x= x/255
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    # x = preprocess_input(x)

    preds = model.predict(x)
    return preds

def classify(arg):
    a=np.argmax(arg, axis=1)
    class1 = []
    if a == 0:
        class_name = "Grouped Horizontal Bar chart"
        class1.append(class_name)
    #class_visualize(path, class_name)

    if a == 1:
        class_name = "Grouped Vertical Bar chart"
        class1.append(class_name)
    #class_visualize(path, class_name)

    if a == 2:
        class_name = "Stacked Horizontal Bar Chart"
        class1.append(class_name)
    #class_visualize(path, class_name)

    if a == 3:
        class_name = "Stacked Vertical Bar Chart"
        class1.append(class_name)
    #class_visualize(path, class_name)

    return class_name

def class_visualize(path, class_name,filename):
    image = cv2.imread(path)
    cv2.putText(image, class_name, (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), thickness=4, bottomLeftOrigin=False)
    
    basepath = os.path.dirname(__file__)
    file_path1 = os.path.join(basepath,'static','classify')
    os.chdir(file_path1)
    cv2.imwrite(filename, image)
    os.chdir(basepath)


data = (('empty','empty','empty','empty','empty','empty','empty','empty','empty'),
        ('empty','empty','empty','empty','empty','empty','empty','empty','empty'),
        ('empty','empty','empty','empty','empty','empty','empty','empty','empty'))



@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html', data=data)


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_p = os.path.join(basepath, 'uploads', 'abc.png')
        f.save(file_p)
        file_name = os.path.basename(r'C:\Users\User\Documents\Semester 8-A\CodeFest3\uploads\abc.png')
        print(file_name)
        print("Converting from image to jpg")
        png_to_jpg(file_name)
        file_name = os.path.basename(r'C:\Users\User\Documents\Semester 8-A\CodeFest3\uploads\abc.jpg')
        print(file_name)
        file_path = os.path.join(basepath, 'uploads', file_name)

        # Make prediction
        preds = model_predict(file_path, model)

        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
        result = classify(preds)
        class_visualize(file_path, result, file_name)
        basepath = os.path.dirname(__file__)
        file_path1 = os.path.join(basepath,'classify')
        return result
    return none
    

@app.route('/classify', methods=["GET","POST"])
def preview_classification():
    if request.method == "POST":
        f = request.files['file']
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_p = os.path.join(basepath, 'uploads', 'abc.png')
        f.save(file_p)
        file_name = os.path.basename(r'C:\Users\User\Desktop\Final Year Project\FlaskClassifier\uploads\abc.png')
        print(file_name)
        print("Converting from image to jpg")
        png_to_jpg(file_name)
        file_name = os.path.basename(r'C:\Users\User\Desktop\Final Year Project\FlaskClassifier\uploads\abc.jpg')
        print(file_name)
        file_path = os.path.join(basepath, 'uploads', file_name)

        # Make prediction
        preds = model_predict(file_path, model)

        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
        result = classify(preds)
        class_visualize(file_path, result, file_name)
        return result
    return none

@app.route('/detection', methods=["GET","POST"])
def preview_detection():
    if request.method == "POST":
        global data
        basepath = os.path.dirname(__file__)
        weight_path = os.path.join(basepath,'best.pt')
        #subprocess.run(['python', 'detect.py','--weights',weight_path,'--img', '640','--conf','0.40','--source', file_path])
        """"
        model = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True, classes=6)
        checkpoint_ = torch.load(basepath,'best.pt')['model']
        model.load_state_dict(checkpoint_.state_dict())

        model = model.fuse().autoshape()
        """
        file_name = os.path.basename(r'C:\Users\User\Documents\Semester 8-A\CodeFest3\uploads\abc.png')
        print(file_name)
        file_path = os.path.join(basepath, 'uploads', file_name)
        file_p = os.path.join(basepath, 'uploads')
        #src_dir1 = file_path
        #dst_dir1 = r'C:\Users\User\Documents\Semester 8-A\CodeFest\LR'
        #for file in glob.iglob(os.path.join(src_dir1, "*.jpg")):
         #   shutil.copy(file, dst_dir1)
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=weight_path)
        image1 = cv2.imread(file_path, cv2.IMREAD_COLOR)
        image = cv2.imread(file_path)
        results = model(image, size=640)  # includes NMS
        file_path1 = os.path.join(basepath,'static','detection')
        results.save()
        src_dir = basepath + "/runs/detect/exp"
        dst_dir = file_path1

        for jpgfile1 in glob.iglob(os.path.join(src_dir, "*.jpg")):
            shutil.copy(jpgfile1, dst_dir)
        dir = "runs"
        path = os.path.join(basepath, dir)
        # removing directory
        shutil.rmtree(path)
        pd = results.pandas().xyxy[0]
        print(pd)
        classn = upload()
        result1 = "Detection Done!..."
        result = ocr_extract(pd,image1,classn)
        data = table1(result, pd,classn)
        print(data)
        #result1 = 'success'
        """
        output = model(image)
        file_path1 = os.path.join(basepath,'static','detection')
        os.chdir(file_path1)
        cv2.imwrite(abc.jpg, output)
        """
        return data


@app.route('/table', methods=["GET","POST"])
def table(pd, image1, classn):
    result = ocr_extract(pd, image1, classn)
    data = table1(result, pd, classn)
    print(data)
    return data



if __name__ == '__main__':
    app.run(debug=True)

import easyocr
import os
import collections
from tabulate import tabulate
import cv2
import pytesseract
import re
from pandas.plotting import table
import pandas as pd
from io import StringIO
from flask import Flask, redirect, url_for, request, render_template
from matplotlib import pyplot as plt
import dataframe_image as dfi
import test
from test import super_resolution
from test import load_resolution_model

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def ocr_extract(pd,image, classn):
    # Apply ROI filtering and OCR

    #w = image.shape[1]
    #h = image.shape[0]
    #if w<571 and h<601:
        #model = load_resolution_model()
        #image = super_resolution(image,model)
    #file_p1 = r"C:\Users\User\Documents\Semester 8-A\CodeFest\results\abc.jpg"
    #file_p2 = r"C:\Users\User\Documents\Semester 8-A\CodeFest\results\abc.png"
    #image = cv2.imread(file_p1)
    a_dict = collections.defaultdict(list)
    df = pd
    reader = easyocr.Reader(['en'], gpu=False)  # this needs to run only once to load the model into memory
    path12 = r"C:\Users\User\Documents\Semester 8-A\CodeFest\ROI"
    os.chdir(path12)
    cv2.imwrite('123.jpg', image)
    if classn == "Stacked Vertical Bar Chart" or classn == "Grouped Vertical Bar chart":
        for idx, row in df.iterrows():
            basepath = os.path.dirname(__file__)
            path1 = os.path.join(basepath, 'uploads', 'abc.jpg')
            print(idx)
            roi = [row['xmin'], row['ymin'], row['xmax'], row['ymax']]
            print(roi)
            roi = image[int(roi[1]):int(roi[3]), int(roi[0]):int(roi[2])]
            string = "{}.{}".format(idx+1, 'abc.png')
            basepath = os.path.dirname(__file__)
            if row['name'] != 'bar':
                if row['name'] != 'chart_title':
                    roi = resize(roi)
                    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                    cv2.imwrite(string, roi)
                    if row['name'] == 'x-axis':
                        roi = cv2.rotate(roi, cv2.cv2.ROTATE_90_CLOCKWISE)
                    if row['name'] == 'axis_title':
                        if row['ymax'] < 620:
                            roi = cv2.rotate(roi, cv2.cv2.ROTATE_90_CLOCKWISE)

                text = reader.readtext(roi, detail=0, paragraph=True, contrast_ths=0.08, adjust_contrast=0.6)
                # text = pytesseract.image_to_string(roi, lang = 'eng',config='--psm 1 --dpi 400 --oem 1')
                if text:
                    text = text.pop()
                # basic preprocessing of the text
                """
                text = text.replace('\t',' ')
                text= text.rstrip()
                text= text.lstrip()
                text = text.replace(' +',' ')
                text = text.replace('\n+','\n')
                text = text.replace('\n+ +',' ')
                text = text.replace('\n',' ')
                
                if row['name'] != 'legend_label':
                    if text:
                        c = d.check(text)
                        if not c:
                            a = set(d.suggest(text))
                            best_words = []
                            best_ratio = 0
                            for b in a:
                                tmp = difflib.SequenceMatcher(None, text, b).ratio()
                                if tmp > best_ratio:
                                    best_words = [b]
                                    best_ratio = tmp
                                elif tmp == best_ratio:
                                    best_words.append(b)
                            if best_words:
                                text = best_words.pop()
                """
                print(text)
                a_dict[row['name']].append(text)

    elif classn == "Stacked Horizontal Bar Chart" or "Grouped Horizontal Bar chart":
        for idx, row in df.iterrows():
            basepath = os.path.dirname(__file__)
            path1 = os.path.join(basepath, 'uploads', 'abc.jpg')
            print(idx)
            roi = [row['xmin'], row['ymin'], row['xmax'], row['ymax']]
            print(roi)
            roi = image[int(roi[1]):int(roi[3]), int(roi[0]):int(roi[2])]
            string = "{}.{}".format(idx + 1, 'abc.png')
            basepath = os.path.dirname(__file__)
            if row['name'] != 'bar':
                if row['name'] != 'chart_title':
                    roi = resize(roi)
                    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                    cv2.imwrite(string, roi)
                    if row['name'] == 'y-axis':
                        roi = cv2.rotate(roi, cv2.cv2.ROTATE_90_CLOCKWISE)
                    if row['name'] == 'axis_title':
                        if row['ymax'] < 620:
                            roi = cv2.rotate(roi, cv2.cv2.ROTATE_90_CLOCKWISE)

                text = reader.readtext(roi, detail=0, paragraph=True, contrast_ths=0.08, adjust_contrast=0.6)
                # text = pytesseract.image_to_string(roi, lang = 'eng',config='--psm 1 --dpi 400 --oem 1')
                if text:
                    text = text.pop()
                # basic preprocessing of the text
                """
                text = text.replace('\t',' ')
                text= text.rstrip()
                text= text.lstrip()
                text = text.replace(' +',' ')
                text = text.replace('\n+','\n')
                text = text.replace('\n+ +',' ')
                text = text.replace('\n',' ')
                
                if row['name'] != 'legend_label':
                    if text:
                        c = d.check(text)
                        if not c:
                            a = set(d.suggest(text))
                            best_words = []
                            best_ratio = 0
                            for b in a:
                                tmp = difflib.SequenceMatcher(None, text, b).ratio()
                                if tmp > best_ratio:
                                    best_words = [b]
                                    best_ratio = tmp
                                elif tmp == best_ratio:
                                    best_words.append(b)
                            if best_words:
                                text = best_words.pop()
                """
                print(text)
                a_dict[row['name']].append(text)

    print(a_dict)
    # df1 = pd.DataFrame.from_records( a_dict, columns=a_dict.keys())

    df = tabulate(a_dict, headers='keys', tablefmt='github', showindex=True)
    print(df)
    return a_dict


def resize(image):
    scale_percent = 260  # percent of original size
    print(image.shape[1], image.shape[0])
    width = int(image.shape[1] * scale_percent / 80)
    height = int(image.shape[0] * scale_percent / 80)
    dim = (width, height)
    print(dim)
    # resize image
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized




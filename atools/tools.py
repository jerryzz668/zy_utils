import os 
import json
import pickle
import numpy as np 
import matplotlib.pyplot as plt 
import cv2 
def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def read_json(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

def save_json(json_path, json_file):
    with open(json_path, 'w') as f:
        json.dump(json_file, f, indent=4)

def read_pkl(pkl_path):
    with open(pkl_path, 'rb') as f:
        return pickle.load(f)

def read_txt(txt_path):
    with open(txt_path, 'r') as f:
        txt_file = f.readlines()
    return txt_file

def getContoursBinary(blimg):
    # print(blimg.shape)
    ret, binary = cv2.threshold(blimg, 0.5, 255, cv2.THRESH_BINARY)
    # print(binary.shape)
    #ret, binary = cv2.threshold(blimg, 127, 255, cv2.THRESH_BINARY)
    #_, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    return contours  

def plot_hist(np_array, step, title):
    bins = int((np.max(np_array) - np.min(np_array)) / step)
    plt.hist(np_array, bins=bins, facecolor='blue', edgecolor='black')
    plt.xlabel('section')
    plt.ylabel('frequency')
    plt.title('{} distribution'.format(title))
    plt.show()

def rotate_anti_clock_wise90(img):
    trans_img = cv2.transpose(img)
    new_img = cv2.flip(trans_img, 0)
    return new_img 
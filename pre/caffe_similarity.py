
# coding: utf-8

import sys

import cv2
import numpy as np
caffe_root = '/home/workspace/libworkspace/caffe/python'
sys.path.insert(0, caffe_root)
import caffe
import helpfunc
import os


global_data_path = '/opt/poetry/data/army/Similarity_data/'

def write_feature():
    """
    Give the path of image samples, Extract the vgg face features of every image,
    and write the features in the path of data
    :param list_path: the path of images
    :return: NULL
    """
    list_path = global_data_path + 'face'
    image_path = helpfunc.listdir(list_path)
    list_image = []
    data_path = []
    for img_path in image_path:
        face = cv2.imread(img_path)
        #face = helpfunc.get_face_dlib(img_path)
        process_face = PreProcess(face)
        list_image.append(process_face)

        file_name = img_path.split('/')[-1]

        portion = os.path.splitext(file_name)
        if portion[1] == '.png' or portion[1] == '.jpeg' or portion[1] == '.jpg':
            new_name = global_data_path + 'facedata/' + portion[0] + '.txt'
            data_path.append(new_name)

    list_feature = get_caffe_features(list_image)

    for i in range(len(data_path)):
        with open(data_path[i], 'w') as f:
            for name in list_feature[i]:
                f.write(str(name))
                f.write('\n')

def process(image_path):
    """
    Give an image, extract its vgg face features;
    Load the samples image features;
    Calculate the image features with every sample features;
    """
    face_data_path = global_data_path + 'facedata'
    feature_path = helpfunc.listdir(face_data_path)
    dict_data = {}
    for i in range(len(feature_path)):
        with open(feature_path[i], 'r') as f:
            lines = f.readlines()
            for j in range(len(lines)):
                lines[j] = float(lines[j])

            # key = feature_path[i].split('/')[-1].split('z')[0]
            key = feature_path[i].split('_')[-1].split('.')[0]
            dict_data[key] = lines


    input_face = helpfunc.get_face_dlib(image_path)
    # input_face = cv2.imread(image_path)
    process_face = PreProcess(input_face)
    input_feature = get_caffe_features([process_face])

    max_similarity = 0.0
    str_key = ''
    for key in dict_data:
        similarity = helpfunc.cosine_distance(input_feature[0], dict_data[key])
        if similarity > max_similarity:
            max_similarity = similarity
            str_key = key

    print str_key, max_similarity

    return {'name': str_key, 'score': max_similarity}


def PreProcess(image):
    """
    Before feed the image to Caffe Model, We need process the input image,
    make it suitable for the Caffe Model
    """
    img = cv2.resize(image, (224, 224), interpolation=cv2.INTER_CUBIC)
    img = img[:, :, ::-1] * 1.0  # convert RGB->BGR
    avg = np.array([129.1863, 104.7624, 93.5940])
    img = img - avg  # subtract mean (numpy takes care of dimensions :)

    img = img.transpose((2, 0, 1))
    img = img[None, :]

    return img


def get_caffe_features(list_image):
    """
    Feed the list of images,
    Return the corresponding feature lists
    """
    caffe.set_mode_cpu()

    pwd = os.getcwd()
    face_prototxt = global_data_path + 'model/VGG_FACE_deploy.prototxt'
    face_model = global_data_path + 'model/VGG_FACE.caffemodel'
    net = caffe.Net(face_prototxt, face_model, caffe.TEST)

    feature_list = []
    for image in list_image:
        out = net.forward(data=image)
        feature = np.float64(net.blobs['fc7'].data)
        feature = feature[0]

        feature_list.append(feature)
        print feature
    return feature_list


def test_similarity(imagepath1, imagepath2):
    """
    test two images similarity
    """
    face1 = helpfunc.get_face(imagepath1)
    face2 = helpfunc.get_face(imagepath2)

    process_face1 = PreProcess(face1)
    process_face2 = PreProcess(face2)

    list_face = [process_face1, process_face2]
    features = get_caffe_features(list_face)
    similarity = helpfunc.cosine_distance(features[0], features[1])

    print similarity


def test_datas():
    list_path = global_data_path + 'testdata'
    image_path = helpfunc.listdir(list_path)

    parent_path = global_data_path + '军旅素材/'
    for path in image_path:
        dict = process(path)
        print dict
        key, = dict
        child_path = key.split('_')
        similarity_image_path = parent_path + child_path[0] + '/' + child_path[1] + '.png'
        similarity_image = cv2.imread(similarity_image_path)
        cv2.imshow('similarity_image', similarity_image)

        origin_image = cv2.imread(path)
        cv2.imshow('origin_image', origin_image)
        cv2.waitKey(0)

# test_datas()

image_path = global_data_path + 'testdata/100.jpg'
process(image_path)


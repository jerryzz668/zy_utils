'''
@Description: TODO
@author: lijianqing
@date: 2020/11/18 17:12
@return
'''
import logging
import math
import time
from collections import namedtuple

import multiprocessing as mp
import cv2
import mmcv
import numpy as np
import pycocotools.mask as maskUtils
import service_pb2
from skimage import morphology


class FeatureParameterize(object):
    """
    FeatureParameterize
    """

    def __init__(self, single_inference_replies, image_np, nofp_defects=(), limit_scale=100):
        self.single_inference_replies = single_inference_replies
        self.image_np = image_np
        self.nofp_defects = nofp_defects
        self.limit_scale = limit_scale
    def extract_reply_feature(self,item):
        bbox = [int(item.xmin), int(item.ymin), int(item.xmin) + int(item.bb_width),int(item.ymin) + int(item.bb_height), item.score]
        label = item.class_name
        points=item.points
        mask = np.asarray(bytearray(item.mask), dtype="uint8")
        if np.all(mask == 0):
            mask = None
        else:
            mask = mask.reshape((item.mask_height, item.mask_width))
                #TODO 
                #logging.debug("mask info is {}".format(mask)) 
                #mask=mask*255
                #logging.debug("mask info is {}".format(mask)) 

            if label in self.nofp_defects or mask is None:
                feature = self._empty_feat()
            else:
                feature = self._extract_feat(bbox, mask, limit_scale=self.limit_scale)
        return {result:(bbox,label,feature,points)}
    def __call__(self):
        """

        :return:
        """
        bboxes, labels, features,points = [], [], [],[]
        #pool = mp.Pool(16)
        #results = [pool.apply_async(self.extract_reply_feature, args=(item)) for item in self.single_inference_replies]
        #for p in results:
        #    bbox,label,feature=p.get()['result']
        #    bboxs.append(bbox)
        #    labels.append(label)
        #    features.append(feature)
        for i, item in enumerate(self.single_inference_replies):
            points.append(item.points)
             
            bbox = [int(item.xmin), int(item.ymin), int(item.xmin) + int(item.bb_width),
                    int(item.ymin) + int(item.bb_height), item.score]
            label = item.class_name
            if label=='heidian' or label=='baisezaodian':
                if item.bb_height==0 or item.bb_width==0 or item.score==0.331:
                    continue
            mask = np.asarray(bytearray(item.mask), dtype="uint8")
            if np.all(mask == 0):
                mask = None
            else:
                mask = mask.reshape((item.mask_height, item.mask_width))
                #TODO 
                #logging.debug("mask info is {}".format(mask)) 
                #mask=mask*255
                #logging.debug("mask info is {}".format(mask)) 

            bboxes.append(bbox)
            labels.append(label)
            if label in self.nofp_defects or mask is None:
                feature = self._empty_feat()
            else:
                feature = self._extract_feat(bbox, mask, limit_scale=self.limit_scale)
            features.append(feature)
            #points.append(self._trans_list2points(point_list))
        Result = namedtuple('Result', ['bboxes', 'labels', 'features','points'])
        self.result = Result(bboxes=bboxes, labels=labels, features=features,points=points)
        return self.result
    def _trans_list2points(self,point_list):
        """
        transform a point list to proto Point list
        """
        return map(lambda p:service_pb2.Point(x=p[0],y=p[1]),point_list)

    def _empty_feat(self):
        """
        为不需要做fp的类别生成空feature
        Returns:

        """
        feature_result = {'length': 0,
                          'width': 0,
                          'pixel_area': 0,
                          'brightness': 0,
                          'max20brightness': 0,
                          'min20brightness': 0,
                          'gradients': 0,
                          'contrast': 0
                          }
        return feature_result

    def _get_closest_defect(self):
        """

        Returns:

        """
        center_point = []
        for bbox in self.result.bboxes:
            pointx = (bbox[0] + bbox[2]) // 2
            pointy = (bbox[1] + bbox[3]) // 2
            center_point.append((pointx, pointy))
        point_num = len(center_point)
        min_distances = np.full(point_num, np.inf)
        for i in range(point_num):
            for j in range(i + 1, point_num):
                if self.result.labels[i] != self.result.labels[j]:
                    continue
                distance = np.sqrt(
                    np.power((center_point[i][0] - center_point[j][0]), 2) + np.power(
                        (center_point[i][1] - center_point[j][1]), 2))
                min_distances[i] = min(min_distances[i], distance)
                min_distances[j] = min(min_distances[j], distance)
        for i in range(point_num):
            self.result.features[i]['min_distance'] = min_distances[i]

    def _extract_feat(self, bbox, mask, limit_scale=100):
        """
        extract_feat
        :param image: image crop, list
        :param mask: mask of target, np.ndarray
        :limit_scale: mask的宽或高超过这个值就会做resize, int
        :return: features of the feature, dict
        """
        image = self.image_np[bbox[1]: bbox[1] + mask.shape[0], bbox[0]: bbox[0] + mask.shape[1]]
        scale = 1
        if mask.shape[0] >= limit_scale or mask.shape[1] >= limit_scale:
            scale = limit_scale / max(mask.shape[0], mask.shape[1])
            new_w, new_h = int(image.shape[1] * scale), int(image.shape[0] * scale)
            image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
            mask = cv2.resize(mask, (new_w, new_h), interpolation=cv2.INTER_AREA)
            mask = mask.astype(np.bool)
            length, width = self._extract_length_width_minarea(mask)

        else:
            mask = mask.astype(np.bool)
            length, width = self._extract_length_width_bydt(mask)
        length /= scale
        width /= scale
        pixel_area = self._extract_pixel_area(mask)
        pixel_area = pixel_area / scale / scale
        brightness, max20brightness, min20brightness = self._extract_brightness(mask, image)
        gradients = self._extract_gradients(mask, image)
        contrast = self._extract_contrast(mask, image)

        feature_result = {'length': length,
                          'width': width,
                          'pixel_area': pixel_area,
                          'brightness': brightness,
                          'max20brightness': max20brightness,
                          'min20brightness': min20brightness,
                          'gradients': gradients,
                          'contrast': contrast
                          }
        return feature_result

    def _extract_length_width_bydt(self, mask):
        """extract_length and width by distance transform"""
        height, width = mask.shape[0], mask.shape[1]
        # 使用骨架算法
        skeleton = morphology.skeletonize(mask)
        length = sum(skeleton.flatten())
        if length < min(height, width):
            length = min(height, width)  # 圆形缺陷的skeleton会被提取为一个点

        # distance transform
        dist_img = cv2.distanceTransform(mask.astype('uint8'), cv2.DIST_L2, cv2.DIST_MASK_3)
        width = np.median(dist_img[skeleton]) * 2

        return length, width

    def _extract_length_width_skeleton(self, mask):
        """extract_length and width using skeleton algorithm"""
        skeleton, distance = morphology.medial_axis(mask, return_distance=True)

        # 计算length
        height, width = mask.shape[0], mask.shape[1]
        length = sum(skeleton.flatten())
        if length < min(height, width):
            length = min(height, width)  # 圆形缺陷的skeleton会被提取为一个点

        # 计算width
        distance[morphology.skeletonize(mask) == 0] = 0
        distance_values = distance[distance != 0]
        if len(distance_values) == 0:
            return 1, 1
        width = np.mean(distance_values) * 2

        return length, width

    def _extract_length_width_minarea(self, mask):
        """extract_length and width using minarea algorithm"""
        """extract_length and width"""
        # opencv的旧版，返回三个参数，要想返回三个参数: pip install opencv-python==3.4.3.18,或者采用新版本
        # image, cnts, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        mask = mask.astype(np.uint8)
        cnts, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        areas = []
        for cnt in cnts:
            areas.append(cv2.contourArea(cnt))
        index = np.argmax(areas)
        cnt = cnts[index]
        rect = cv2.minAreaRect(cnt)  # 最小外接矩形
        return rect[1][0], rect[1][1]

    def _extract_length(self, mask, by_skeleton=True):
        """
        extract_length
        :param by_skeleton:
        :param mask: mask of target
        :return: length of the image _crop
        """
        height, width = mask.shape[0], mask.shape[1]
        if by_skeleton:
            # 使用骨架算法
            skeleton = morphology.skeletonize(mask)
            length = sum(skeleton.flatten())
            if length < min(height, width):
                length = min(height, width)  # 圆形缺陷的skeleton会被提取为一个点
            return length

        else:
            contours, _ = cv2.findContours(mask.astype(np.uint8) * 255, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
            xs = contours[0][0][:, 0]
            ys = contours[0][0][:, 1]
            xmin, xmax = min(xs), max(xs)
            ymin, ymax = min(ys), max(ys)
            # 计算目标区域中心点
            center_point = ((xmin + xmax) // 2, (ymax + ymin) // 2)
            # 找离中心点最远的点
            max_distance = 0
            for row in range(height):
                for col in range(width):
                    if mask[row, col] == 0:
                        continue
                    else:
                        distance = math.sqrt(
                            ((row - center_point[1]) ** 2) + ((col - center_point[0]) ** 2))
                        if distance > max_distance:
                            max_distance = distance
                            p1 = (row, col)
            # 找离p1最远的点
            length = 0
            for row in range(height):
                for col in range(width):
                    if mask[row, col] == 0:
                        continue
                    else:
                        distance_top1 = math.sqrt(((row - p1[1]) ** 2) + ((col - p1[0]) ** 2))
                        if distance_top1 > length:
                            length = distance_top1
                            p2 = (row, col)
        return length

    def _extract_width(self, mask):
        """
        extract_width
        :param image:
        :param mask:
        :return:
        """
        # TODO: 圆形mask会被提取成一个点
        _, distance = morphology.medial_axis(mask, return_distance=True)
        distance[morphology.skeletonize(mask) == 0] = 0
        distance_values = distance[distance != 0]
        if len(distance_values) == 0:
            return 1
        width = sum(distance_values) / len(distance_values) * 2
        return width

    def _extract_pixel_area(self, mask):
        """
        extract_pixel_area
        :param mask:
        :return:
        """
        return sum(sum(mask))

    def _extract_brightness(self, mask, image):
        """
        extract_brightness
        :param mask:
        :param image:
        :return:
        """
        try:
            segm_pixels = image[mask == 1].flatten().tolist()
        except Exception as e:
            logging.debug('Mask shape: {}, image_shape: {}'.format(mask.shape, image.shape))
            return 0, 0, 0
        if len(segm_pixels) == 0:
            return 0, 0, 0

        # return np.median(segm_pixels), np.percentile(segm_pixels, 80), \
        #        np.percentile(segm_pixels, 20)

        top_k = max(1, int(len(segm_pixels) * 0.2))
        top_k_idx = sorted(segm_pixels, reverse=True)[0:top_k]
        low_k_idx = sorted(segm_pixels)[0:top_k]
        return sum(segm_pixels) / len(segm_pixels), sum(top_k_idx) / len(top_k_idx), sum(
            low_k_idx) / len(low_k_idx)

    def _extract_gradients(self, mask, image):
        """
        extract_gradients
        :param mask:
        :param image:
        :return:
        """
        gray_x = cv2.Sobel(image, cv2.CV_32F, 1, 0)  # x方向一阶导数
        gray_y = cv2.Sobel(image, cv2.CV_32F, 0, 1)  # y方向一阶导数
        gradx = cv2.convertScaleAbs(gray_x)  # 转回原来的uint8形式
        grady = cv2.convertScaleAbs(gray_y)
        grad = cv2.addWeighted(gradx, 0.5, grady, 0.5, 0)  # 图像融合
        # 提取mask边缘点的梯度值
        contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
        # 提取边缘点
        edge_points = []
        for contour in contours:
            for i in range(contour.shape[0]):
                edge_point = contour[i, 0, :]
                edge_points.append(edge_point)

        # 计算边缘点梯度均值
        grad_sum = 0
        for ep in edge_points:
            x, y = ep[0], ep[1]
            grad_sum += grad[y, x]
        return grad_sum if len(edge_points) == 0 else grad_sum / len(edge_points)

    def _extract_contrast(self, mask, image, up_scale=100):
        """
        extract_contrast
        :param mask:
        :param image:
        :param up_scale:
        :return:
        """
        image_norm = image / 255
        fgs = image[mask != 0].flatten()
        bgs = image[mask == 0].flatten()
        if len(fgs) == 0:
            fg_mean = 0
        else:
            fg_mean = sum(fgs) / len(fgs)
        if len(bgs) == 0:
            bg_mean = 0
        else:
            bg_mean = sum(bgs) / len(bgs)

        contrast = abs(fg_mean - bg_mean)

        return contrast * up_scale

    def _generate_mask(self, img_np):
        """

        :param img_np:
        :return:
        """
        threshold = cv2.adaptiveThreshold(img_np, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV, 49, 25)
        return threshold

    def _get_mask_from_bbox(self):
        """

        :return:
        """
        img_nps, masks, bboxes, labels = [], [], [], []
        for result, mask in zip(self.result, self.masks):
            x, y, w, h = result[0], result[1], result[2], result[3]
            img_np = self.image_np[y: y + h, x: x + w]
            img_nps.append(img_np)
            masks.append(mask)
            bboxes.append([x, y, x + w, y + h, 1])
            labels.append(4)

        bboxes = np.array(bboxes)
        Result = namedtuple('Result', ['img_nps', 'masks', 'bboxes', 'labels'])
        result = Result(img_nps=img_nps, masks=masks, bboxes=bboxes, labels=labels)
        return result

    def _get_mask_from_result(self):
        """

        :return:
        """
        img_nps, masks = [], []
        bbox_result, segm_result = self.result
        labels = [
            np.full(bbox.shape[0], i, dtype=np.int32)
            for i, bbox in enumerate(bbox_result)
        ]
        labels = np.concatenate(labels)
        segms = mmcv.concat_list(segm_result)
        bboxes = np.vstack(bbox_result)

        for i in range(len(bboxes)):
            mask = maskUtils.decode(segms[i]).astype(np.bool).astype(np.uint8) * 255
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for index, cnt in enumerate(contours[::-1]):
                rect = cv2.boundingRect(cnt)
                img_np = self.image_np[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]
                mask_np = mask[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]
                img_nps.append(img_np)
                masks.append(mask_np)
                break
        Result = namedtuple('Result', ['img_nps', 'masks', 'bboxes', 'labels'])
        result = Result(img_nps=img_nps, masks=masks, bboxes=bboxes, labels=labels)
        return result


if __name__ == '__main__':
    image_np = cv2.imread('../redis_demo/2-D-95-D3.jpg', 0)
    mask = np.zeros((100, 100), dtype=np.uint8)
    mask[0:80, 0:80] = 1
    mask[60:50, 30:50] = 1
    mask = mask.tobytes()
    image = np.asarray(bytearray(mask))

    singleInferenceReply = service_pb2.SingleInferenceReply(
        class_name='huashang', xmin=0.0, ymin=0.0, bb_width=100.0, bb_height=100.0, score=0.99,
        mask=mask, mask_width=100, mask_height=100)
    single_inference_replies = service_pb2.InferenceReply(
        photo_id=1, product_id=1, channel_id=1, num_detections=1, singleInferenceReply=[])
    single_inference_replies.singleInferenceReply.append(singleInferenceReply)
    fp = FeatureParameterize(single_inference_replies.singleInferenceReply, image_np,
                             limit_scale=100)
    result = fp()


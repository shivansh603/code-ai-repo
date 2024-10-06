# Improved and De-Cluttered Import Sections

import numpy as np
import cv2, os, skimage, random, requests, json, operator, math
from glob import glob
from PIL import Image
from functools import reduce



def json_creater(inputs, closed):
    data = []
    count = 1
    highContrastingColors = ['rgba(0,255,81,1)', 'rgba(255,219,0,1)', 'rgba(255,0,0,1)', 'rgba(0,4,255,1)',
                             'rgba(227,0,255,1)']
    for index, input in enumerate(inputs):
        color = random.sample(highContrastingColors, 1)[0]
        json_id = count
        sub_json_data = {}
        sub_json_data['id'] = json_id
        sub_json_data['name'] = json_id
        sub_json_data['color'] = color
        sub_json_data['isClosed'] = closed
        sub_json_data['selectedOptions'] = [{"id": "0", "value": "root"},
                                            {"id": str(random.randint(10, 20)), "value": inputs[input]}]
        points = eval(input)
        if len(points) > 0:
            center = tuple(
                map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), points), [len(points)] * 2))
            sorted_coords = sorted(points, key=lambda coord: (-135 - math.degrees(
                math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360)
        else:
            sorted_coords = []
        vertices = []
        is_first = True
        for vertex in sorted_coords:
            vertex_json = {}
            if is_first:
                vertex_json['id'] = json_id
                vertex_json['name'] = json_id
                is_first = False
            else:
                json_id = count
                vertex_json['id'] = json_id
                vertex_json['name'] = json_id
            vertex_json['x'] = vertex[1]
            vertex_json['y'] = vertex[0]
            vertices.append(vertex_json)
            count += 1
        sub_json_data['vertices'] = vertices
        data.append(sub_json_data)
    return json.dumps(data)
    
def send_to_rlef(img_path, annotation, labels, model_id, tag='testing', confidence_score=100, label='RGB', prediction='predicted'):
    print("Sending")
    
    li = {}
    for labeld, an in zip(labels, annotation):
        li[f"{an}"] = labeld
    
    annotations = json_creater(li, True)
    
    url = "https://autoai-backend-exjsxe2nda-uc.a.run.app/resource"
    payload = {
        'model': model_id,
        'status': 'backlog',
        'csv': 'csv',
        'label': 'RGB',
        'tag': tag,
        'model_type': 'imageAnnotation',
        'prediction': prediction,
        'confidence_score': confidence_score,
        'imageAnnotations': str(annotations)
    }
    files = [('resource', (f'{img_path}', open((img_path), 'rb'), 'image/png'))]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print('code: ', response.status_code)

def transform(image,
              translation=(0, 0, 0),
              rotation=(0, 0, 0),
              scaling=(1, 1, 1),
              shearing=(0, 0, 0)):
    
    # get the values on each axis
    t_x, t_y, t_z = translation
    r_x, r_y, r_z = rotation
    sc_x, sc_y, sc_z = scaling
    sh_x, sh_y, sh_z = shearing
    
    # convert degree angles to rad
    theta_rx = np.deg2rad(r_x)
    theta_ry = np.deg2rad(r_y)
    theta_rz = np.deg2rad(r_z)
    theta_shx = np.deg2rad(sh_x)
    theta_shy = np.deg2rad(sh_y)
    theta_shz = np.deg2rad(sh_z)
    
    # get the height and the width of the image
    h, w = image.shape[:2]
    # compute its diagonal
    diag = (h ** 2 + w ** 2) ** 0.5
    # compute the focal length
    f = diag
    if np.sin(theta_rz) != 0:
        f /= 2 * np.sin(theta_rz)
        
    # set the image from cartesian to projective dimension
    H_M = np.array([[1, 0, -w / 2],
                    [0, 1, -h / 2],
                    [0, 0,      1],
                    [0, 0,      1]])
    # set the image projective to carrtesian dimension
    Hp_M = np.array([[f, 0, w / 2, 0],
                     [0, f, h / 2, 0],
                     [0, 0,     1, 0]])


    # adjust the translation on z
    t_z = (f - t_z) / sc_z ** 2
    # translation matrix to translate the image
    T_M = np.array([[1, 0, 0, t_x],
                    [0, 1, 0, t_y],
                    [0, 0, 1, t_z],
                    [0, 0, 0,  1]])

    # calculate cos and sin of angles
    sin_rx, cos_rx = np.sin(theta_rx), np.cos(theta_rx)
    sin_ry, cos_ry = np.sin(theta_ry), np.cos(theta_ry)
    sin_rz, cos_rz = np.sin(theta_rz), np.cos(theta_rz)
    # get the rotation matrix on x axis
    R_Mx = np.array([[1,      0,       0, 0],
                     [0, cos_rx, -sin_rx, 0],
                     [0, sin_rx,  cos_rx, 0],
                     [0,      0,       0, 1]])
    # get the rotation matrix on y axis
    R_My = np.array([[cos_ry, 0, -sin_ry, 0],
                     [     0, 1,       0, 0],
                     [sin_ry, 0,  cos_ry, 0],
                     [     0, 0,       0, 1]])
    # get the rotation matrix on z axis
    R_Mz = np.array([[cos_rz, -sin_rz, 0, 0],
                     [sin_rz,  cos_rz, 0, 0],
                     [     0,       0, 1, 0],
                     [     0,       0, 0, 1]])
    # compute the full rotation matrix
    R_M = np.dot(np.dot(R_Mx, R_My), R_Mz)


    # get the scaling matrix
    Sc_M = np.array([[sc_x,     0,    0, 0],
                     [   0,  sc_y,    0, 0],
                     [   0,     0, sc_z, 0],
                     [   0,     0,    0, 1]])
    
        # get the tan of angles
    tan_shx = np.tan(theta_shx)
    tan_shy = np.tan(theta_shy)
    tan_shz = np.tan(theta_shz)
    # get the shearing matrix on x axis
    Sh_Mx = np.array([[      1, 0, 0, 0],
                      [tan_shy, 1, 0, 0],
                      [tan_shz, 0, 1, 0],
                      [      0, 0, 0, 1]])
    # get the shearing matrix on y axis
    Sh_My = np.array([[1, tan_shx, 0, 0],
                      [0,       1, 0, 0],
                      [0, tan_shz, 1, 0],
                      [0,       0, 0, 1]])
    # get the shearing matrix on z axis
    Sh_Mz = np.array([[1, 0, tan_shx, 0],
                      [0, 1, tan_shy, 0],
                      [0, 0,       1, 0],
                      [0, 0,       0, 1]])
    # compute the full shearing matrix
    Sh_M = np.dot(np.dot(Sh_Mx, Sh_My), Sh_Mz)



    Identity = np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])
    
    # compute the full transform matrix
    M = Identity
    M = np.dot(T_M,  M)
    M = np.dot(R_M,  M)
    M = np.dot(Sc_M, M)
    M = np.dot(Sh_M, M)
    M = np.dot(Hp_M, np.dot(M, H_M))
    # apply the transformation
    corners = np.array([
    [0, 0],
    [0, h - 1],
    [w - 1, h - 1],
    [w - 1, 0]
    ])
    corners = cv2.perspectiveTransform(np.float32([corners]), M)[0]
    bx, by, bw, bh = cv2.boundingRect(corners)
    bx2 = bx+bw
    by2 = by+bh
    bx = max(0, bx)
    by = max(0, by)
    bx2 = max(0, bx2)
    by2 = max(0, by2)
    
    image = cv2.warpPerspective(image, M, (5000, 5000))
    # cv2.rectangle(image,(bx,by),(bx+bw,by+bh),(255,0,0),3)
    image = image[by:by2, bx:bx2, :]
    return image


def calculate_iou(box1, box2):

    # Edge Case Handling Added for the Function Defined
    
    if box1.width <= 0 or box2.width <= 0:
        raise ValueError('Bounding box dimensions must be positive')

    # Convert (x, y, w, h) to (x1, y1, x2, y2) format
    x1_box1, y1_box1, w_box1, h_box1 = box1
    x2_box1, y2_box1 = x1_box1 + w_box1, y1_box1 + h_box1

    x1_box2, y1_box2, w_box2, h_box2 = box2
    x2_box2, y2_box2 = x1_box2 + w_box2, y1_box2 + h_box2

    # Calculate coordinates of the intersection rectangle
    x1_intersection = max(x1_box1, x1_box2)
    y1_intersection = max(y1_box1, y1_box2)
    x2_intersection = min(x2_box1, x2_box2)
    y2_intersection = min(y2_box1, y2_box2)

    # Check if there is an intersection (non-negative width and height)
    if x1_intersection < x2_intersection and y1_intersection < y2_intersection:
        # Calculate area of intersection
        intersection_area = (x2_intersection - x1_intersection) * (y2_intersection - y1_intersection)

        # Calculate areas of both boxes
        area_box1 = w_box1 * h_box1
        area_box2 = w_box2 * h_box2

        # Calculate IoU
        iou = intersection_area / (area_box1 + area_box2 - intersection_area)
        return iou
    else:
        return 0.0  # No intersection, IoU is 0


def generate_annotation(item_list, back, over, lab_list, single):
    box_list = []
    a_l = []
    a_l_temp = []
    l_list = []
    l = 0
    w, h = len(back[0]), len(back)
    main_mask = np.zeros((h, w), dtype = np.uint8)
    pass_check = 0
    if single:
        rand_gen = 1
    else:
        rand_gen = random.randint(0,4)
    k = 0
    while l < len(item_list):
        v = item_list[l]
        lab = lab_list[l]
        tx = 0 #np.random.uniform(-w//8, w//8)
        ty = 0 #np.random.uniform(-h//8, h//8)
        tz = 0 #np.random.uniform(- 2, 2)
        rx = np.random.uniform(-5, 5)
        ry = np.random.uniform(-5, 5)
        rz = np.random.uniform(-180, 180)
        scx = np.random.uniform(0.5, 1.5)
        scy = np.random.uniform(0.5, 1.5)
        scz = np.random.uniform(0.5, 1.5)
        shx = np.random.uniform(-5, 5)
        shy = np.random.uniform(-5, 5)
        shz = np.random.uniform(-5, 5)
        
        trans = (tx, ty, tz)
        rot = (rx, ry, rz)
        scale = (scx, scy, scz)
        shear = (shx, shy, shz)
        
        v = transform(v, trans, rot, scale, shear)
        
        width , height = len(v[0]), len(v)
        if width> w:
            width = w-10
        if height> h:
            height = h-10
        x1, y1 = np.random.randint(0, w - width), np.random.randint(0, h - height)
        flag = 0
        for box in box_list:
            iou = calculate_iou((x1, y1, width, height), box)
            # print(iou)
            if iou > over:
                flag = 1
        
        if flag == 1:
            pass_check = pass_check + 1
            if pass_check >= 5:
                l = l + 1
            continue
        
        pass_check = 0
        if rand_gen:
            rand_gen = rand_gen - 1
        else:
            if single:
                rand_gen = 1
            else:
                rand_gen = random.randint(0,4)
            l = l + 1
        k = k + 1 
        mask = np.zeros((h, w), dtype = int)
        v_sum = np.sum(v, axis=2)
        for i in range(height):
            for j in range(width):
                if v_sum[i, j]:
                    main_mask[i+y1, j+x1] = k
                    mask[i+y1, j+x1] = 1
                    back[i+y1, j+x1] =  v[i, j]

        mask = (mask*255).astype(np.uint8)
        # kernel = np.ones((3, 3), np.uint8)
        # mask = cv2.erode(mask, kernel, iterations=1)
        temp_edge = cv2.Canny(image=mask, threshold1=100, threshold2=200)
        a_p = np.transpose(np.where(temp_edge > 0))
        simplified_contour = cv2.approxPolyDP(a_p, 5, True)
        if simplified_contour is not None and simplified_contour.shape[0] > 1:
            simplified_contour = simplified_contour.squeeze()
            a_p = simplified_contour.tolist()

        a_l_temp.append(a_p)
        box_list.append((x1, y1, width, height))
        l_list.append(lab)
    
    l = 0
    while l < len(a_l_temp):
        a_p = a_l_temp[l]
        l = l + 1
        mask = (main_mask == l).astype(np.uint8)
        mask = (mask*255).astype(np.uint8)
        _, count = skimage.measure.label(mask, return_num=True)
        if count > 1:
            a_l.append(a_p)
        else:
            temp_edge = cv2.Canny(image=mask, threshold1=100, threshold2=200)
            a_p = np.transpose(np.where(temp_edge > 0))
            simplified_contour = cv2.approxPolyDP(a_p, 5, True)
            if simplified_contour.shape[0] > 1:
                simplified_contour = simplified_contour.squeeze()
                a_p = simplified_contour.tolist()

            a_l.append(a_p)

    return back, a_l, l_list

def generate_data(trials, back, model_id, over, single, product_name):
    item_list = []
    labels_list = []
    for f in glob('cropped_out/*'):
        labels_list.append(product_name)
        obj_image = Image.open(f)
        img = np.array(obj_image).astype(np.uint8)
        item_list.append(img)
        os.remove(f)
    
    for i in range(trials):
        img_path = 'gen_images/' + str(i+1) + '.png'
        b = back.copy()
        generated_image, annotation_points, lab_list = generate_annotation(item_list, b, over, labels_list, single)
        skimage.io.imsave(img_path, generated_image)
        # model ID: 650af825ebe70f61bd79c083
        send_to_rlef(img_path, annotation_points, lab_list, model_id)
        os.remove(img_path)
        
def run_shuffle(trials = 10, image_path = None, model_id = "650af825ebe70f61bd79c083", over = 0.3, single = True, product_name = 'Object'):
    # # 4608 × 3456 pixels
    im = Image.open(image_path)
    h, w = im.size
    print('h--------------------------------w', h, w)
    if h > w:
        w = h
    else:
        h = w
    if single:
        back = np.zeros((h, h, 3), dtype = np.uint8)
    else:
        h = int(h*1.5)
        back = np.zeros((h, h, 3), dtype = np.uint8)

    os.remove(image_path)
    generate_data(trials, back, model_id, over, single, product_name)
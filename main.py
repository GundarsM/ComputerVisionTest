# #
# #
# # img_name = "sveki mansi ' draugu ' "
# # img = [[[0,255,0],[1,255,0],[2,255,0],[0,255,5],[2,255,0],[8,255,0],[4,255,0]],
# #         [[5,255,0],[6,255,0],[2,255,8],[0,255,9],[9,255,0],[5,255,0],[4,255,7]],
# #         [[6,255,0],[1,255,7],[6,255,0],[5,255,5],[2,255,1],[8,255,4],[1,255,0]]]
# #
# # int_m = 1
# # float_m = 4.525
# # saraksts = [5,4,2,2]
# # bool_m = True
# #
# #
# # #print(img_name, img, int_m,float_m,saraksts,bool_m)
# # # for i in img_name:
# # #    print(i)
# #
# # # print(img)
# # #
# # for j in range(0,len(img)):
# #     for k in range(0,len(img[j])):
# #         print(img[j][k])
# # print(img)
# #
# #
# import random
#
# import cv2
# import numpy
# import matplotlib
# import glob
#
# img_name1 = "glorija.jpeg"
# img_name2 = "bilde.jpeg"
# img_name3 = "bildes\DSC03203(18).jpg"
#
# # img_name4 = glob.glob("bildes\*18*")
#
# # print(img_name4)
#
# img = cv2.imread(img_name1)
# #print(img[0][0][0])
#
# for j in range(0,len(img)):
#     for k in range(0,len(img[j])):
#         #print(random.uniform(0,2))
#         img[j][k][0] = 0#255 - img[j][k][0]
#         img[j][k][1] = 0#255 - img[j][k][1]
#         if img[j][k][2] <150:
#             img[j][k][2] = 0#255 - img[j][k][2]
#         else:
#             img[j][k][2] = 255
#
# #cv2.namedWindow("image",cv2.WINDOW_NORMAL)
# cv2.imshow("image",img)
# cv2.waitKey()
#

import cv2
import numpy
import matplotlib
import glob
import os
import random
from numba import jit
import time

@jit(nopython=True)
def process_frame(img):

    for j in range(0, len(img)):  # iekrāsojam attēlus par 20% zilākus
        for k in range(0, len(img[j])):
            if img[j][k][0] * 1.2 > 255:
                img[j][k][0] = 255
            else:
                img[j][k][0] = img[j][k][0] * 1.2
    return img


dati = "DATA/seq0/seq0.txt"
people_rec = []
people_rec_dic = {}
centre_list = []

with open(dati,"r") as f:
    lines = f.readlines()
    for line in lines:
        img_nr = line.split(",")[0]
        hmn_id = line.split(",")[1]
        pt1 = [int(line.split(",")[2].split(".")[0]),int(line.split(",")[3].split(".")[0])]
        pt2 = [int(line.split(",")[4].split(".")[0]),int(line.split(",")[5].split(".")[0])]
        people_rec.append([img_nr,hmn_id,pt1,pt2])

        if img_nr in people_rec_dic:
            people_rec_dic[img_nr].append([hmn_id,pt1,pt2])
        else:
            people_rec_dic[img_nr]=[]
            people_rec_dic[img_nr].append([hmn_id, pt1, pt2])

#print(people_rec)
#print(people_rec_dic)

img_name = glob.glob("DATA\seq0\*.jpg")
#(img_name)

cv2.namedWindow("image",cv2.WINDOW_AUTOSIZE)
colour_dic = {}
people_count = 0
count_left = 0
count_right = 0
for i in img_name:
    curr_time = time.time()

    new_image = cv2.imread(i)
    height, width, channels = new_image.shape
    img = process_frame(new_image) #paralelizēta funkcija - tipa

    img_nr = str(int(os.path.basename(i).split(".")[0]))
    if img_nr in people_rec_dic:                    #ja dictionarijā ir attēla numurs
        # print("IMG nr. {}".format(img_nr))
        for people in people_rec_dic[img_nr]:       #tad katram cilvēkam ar atbilstošo numuru
            #print(people)
            if people[0] in colour_dic:             #ja ir cilvēks krāsu dictionarijā
                rec_color = colour_dic[people[0]]
            else:                                   #ja nav cilvēks krāsu diktionarijā
                colour_dic[people[0]] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                rec_color = colour_dic[people[0]]

            x1 = 1
            y1 = 1
            x2 = 1920
            y2 = 1080
            #x3 = 544

            m = (y2-y1)/(x2-x1)
            b = y1 - m * x1

            y3 = b + m*people[1][0] + people[2][0] // 2

            if y3<people[1][1] + people[2][1]//2:
                count_left += 1
            else:
                count_right += 1

            #print("{} {} {}".format(m,b,y3))
            #cv2.line(img, (0,0), (people[1][0] + people[2][0] // 2,int(y3)), (0,255,255), 5)
            # if people[1][0] + people[2][0] // 2 < width // 2:
            #     count_left += 1
            # else:
            #     count_right += 1

            #cv2.putText(img, "{}".format(count_left), (50, 100), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 3)
            #print("cilvēks: {}".format(people[0]))
            # pt1 = people[1]
            # pt2 = people[2]
            pt1 = (people[1][0], people[1][1])
            pt2 = (people[1][0] + people[2][0], people[1][1] + people[2][1])

            pt3 = ((people[1][0] + people[2][0]//2-2), (people[1][1] + people[2][1]//2-2))
            pt4 = ((people[1][0] + people[2][0]//2+2), (people[1][1] + people[2][1]//2+2))

            centre_list.append((people[0],pt3,pt4))
            #print(centre_list)
            cv2.rectangle(img, pt1, pt2, rec_color, 2)



            #print("{} {} {}".format(height, width, channels))
            for centre_point in centre_list:
                #print("cilveks {} un centra pukts {} ".format(people[0],centre_point[0]))
                if centre_point[0] == people[0]:
                    cv2.rectangle(img, centre_point[1], centre_point[2], rec_color, 2)

            # print("People id: {} rec: {} {}".format(people[0],people[1],people[2]))
    cv2.putText(img, "{}".format(count_left), (50, 100), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 3)
    cv2.putText(img, "{}".format(count_right), (150, 100), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 3)
    cv2.line(img, (0,0), (width,height), (255,0,0), 2)
    cv2.imshow("image", img)
    count_left =0
    count_right =0
    curr_time2 = time.time()
    #print("Laiks {} cilvēku skaits {}".format(curr_time2 - curr_time,people_count))

    cv2.waitKey(1)
    #print(i)
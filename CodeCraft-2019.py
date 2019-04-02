import logging
import sys
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')
class CROSS(object):
    def __init__(self,ID,road1,road2,road3,road4):
        self.ID = ID
        self.road1 = road1
        self.road2 = road2
        self.road3 = road3
        self.road4 = road4
        
class ROAD(object):
    left_road = None
    right_road = None
    stright_road = None
    back_left = None
    back_right = None
    back_stright = None
    all_right = 1
    def __init__(self,ID,length,speed_lim,channels,cross_begin,cross_end,isDuplex):
        self.ID = ID
        self.length = length
        self.speed_lim = speed_lim
        self.channels = channels
        self.cross_begin = cross_begin
        self.cross_end = cross_end
        self.isDuplex = isDuplex
        
class CAR(object):
    now_posi = None
    def __init__(self,ID,start_loc,dest_loc,speed,start_time):
        self.ID = ID
        self.start_loc = start_loc
        self.dest_loc = dest_loc
        self.speed = speed
        self.start_time = start_time
        

def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

#    car_path = '../config/car.txt'
#    road_path = '../config/road.txt'
#    cross_path = '../config/cross.txt'
#    answer_path = '../config/answer.txt'
    
    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

    cars = pd.read_csv(car_path,skipinitialspace = True)
    roads = pd.read_csv(road_path,skipinitialspace = True)
    crosses = pd.read_csv(cross_path,skipinitialspace = True)

    car_dict = {}
    for car_info in cars.iterrows():
        car_dict[car_info[1][0].replace("(","")] = CAR(car_info[1][0].replace("(",""),car_info[1][1],car_info[1][2],car_info[1][3],car_info[1][4].replace(")",""))

    road_dict = {}
    for road_info in roads.iterrows():
        road_dict[road_info[1][0].replace("(","")] = ROAD(road_info[1][0].replace("(",""),road_info[1][1],road_info[1][2],road_info[1][3],road_info[1][4],road_info[1][5],road_info[1][6].replace(")",""))
        
    cross_dict = {}
    for cross_info in crosses.iterrows():
        the_cross = cross_info[1][0].replace("(","")
        fir = str(int(cross_info[1][1]))
        sec = str(int(cross_info[1][2]))
        thi = str(int(cross_info[1][3]))
        fot = str(int(cross_info[1][4].replace(")","")))
        if fir != "-1":
            if cross_info[1][0].replace("(","") == str(road_dict[fir].cross_begin):
                if (road_dict[fir].isDuplex == "1"):
                    road_dict[fir].back_left = road_dict[sec] if sec != "-1" and ((road_dict[sec].isDuplex == "1") or str(road_dict[sec].cross_begin) == the_cross) else None
                    road_dict[fir].back_stright = road_dict[thi] if thi != "-1" and ((road_dict[thi].isDuplex == "1") or str(road_dict[thi].cross_begin) == the_cross) else None
                    road_dict[fir].back_right = road_dict[fot] if fot != "-1" and ((road_dict[fot].isDuplex == "1") or str(road_dict[fot].cross_begin) == the_cross) else None
                    
                else:
                    road_dict[fir].back_left = None
                    road_dict[fir].back_stright = None
                    road_dict[fir].back_right = None
            else:
                road_dict[fir].left_road = road_dict[sec] if sec != "-1" and ((road_dict[sec].isDuplex == "1") or str(road_dict[sec].cross_begin) == the_cross) else None
                road_dict[fir].stright_road = road_dict[thi] if thi != "-1" and ((road_dict[thi].isDuplex == "1") or str(road_dict[thi].cross_begin) == the_cross) else None
                road_dict[fir].right_road = road_dict[fot] if fot != "-1"  and ((road_dict[fot].isDuplex == "1") or str(road_dict[fot].cross_begin) == the_cross) else None
            
        if sec != "-1":
            if cross_info[1][0].replace("(","") == str(road_dict[sec].cross_begin):
                if (road_dict[sec].isDuplex == "1"):
                    road_dict[sec].back_left = road_dict[thi] if thi != "-1" and ((road_dict[thi].isDuplex == "1") or str(road_dict[thi].cross_begin) == the_cross) else None
                    road_dict[sec].back_stright = road_dict[fot] if fot != "-1" and ((road_dict[fot].isDuplex == "1") or str(road_dict[fot].cross_begin) == the_cross) else None
                    road_dict[sec].back_right = road_dict[fir] if fir != "-1"  and ((road_dict[fir].isDuplex == "1") or str(road_dict[fir].cross_begin) == the_cross) else None
                else:
                    road_dict[sec].back_left = None
                    road_dict[sec].back_stright = None
                    road_dict[sec].back_right = None
            else:
                road_dict[sec].left_road = road_dict[thi] if thi != "-1"  and ((road_dict[thi].isDuplex == "1") or str(road_dict[thi].cross_begin) == the_cross) else None
                road_dict[sec].stright_road = road_dict[fot] if fot != "-1" and ((road_dict[fot].isDuplex == "1") or str(road_dict[fot].cross_begin) == the_cross) else None
                road_dict[sec].right_road = road_dict[fir] if fir != "-1" and ((road_dict[fir].isDuplex == "1") or str(road_dict[fir].cross_begin) == the_cross) else None
                
            
        if thi != "-1":
            if cross_info[1][0].replace("(","") == str(road_dict[thi].cross_begin):
                if (road_dict[thi].isDuplex == "1"):
                    road_dict[thi].back_left = road_dict[fot] if fot != "-1" and ((road_dict[fot].isDuplex == "1") or str(road_dict[fot].cross_begin) == the_cross) else None
                    road_dict[thi].back_stright = road_dict[fir] if fir != "-1" and ((road_dict[fir].isDuplex == "1") or str(road_dict[fir].cross_begin) == the_cross) else None
                    road_dict[thi].back_right = road_dict[sec] if sec != "-1"  and ((road_dict[sec].isDuplex == "1") or str(road_dict[sec].cross_begin) == the_cross) else None
                else:
                    road_dict[thi].back_left = None
                    road_dict[thi].back_stright = None
                    road_dict[thi].back_right = None
            else:
                road_dict[thi].left_road = road_dict[fot] if fot != "-1"  and ((road_dict[fot].isDuplex == "1") or str(road_dict[fot].cross_begin) == the_cross) else None
                road_dict[thi].stright_road = road_dict[fir] if fir != "-1" and ((road_dict[fir].isDuplex == "1") or str(road_dict[fir].cross_begin) == the_cross)  else None
                road_dict[thi].right_road = road_dict[sec] if sec != "-1" and ((road_dict[sec].isDuplex == "1") or str(road_dict[sec].cross_begin) == the_cross)  else None
            
        if fot != "-1":
            if cross_info[1][0].replace("(","") == str(road_dict[fot].cross_begin):
                if (road_dict[fot].isDuplex == "1"):
                    road_dict[fot].back_left = road_dict[fir] if fir != "-1" and ((road_dict[fir].isDuplex == "1") or str(road_dict[fir].cross_begin) == the_cross) else None
                    road_dict[fot].back_stright = road_dict[sec] if sec != "-1" and ((road_dict[sec].isDuplex == "1") or str(road_dict[sec].cross_begin) == the_cross) else None
                    road_dict[fot].back_right = road_dict[thi] if thi != "-1"  and ((road_dict[thi].isDuplex == "1") or str(road_dict[thi].cross_begin) == the_cross) else None
                else:
                    road_dict[fot].back_left = None
                    road_dict[fot].back_stright = None
                    road_dict[fot].back_right = None
            else:
                road_dict[fot].left_road = road_dict[fir] if fir != "-1"  and ((road_dict[fir].isDuplex == "1") or str(road_dict[fir].cross_begin) == the_cross) else None
                road_dict[fot].stright_road = road_dict[sec] if sec != "-1"and ((road_dict[sec].isDuplex == "1") or str(road_dict[sec].cross_begin) == the_cross)  else None
                road_dict[fot].right_road = road_dict[thi] if thi != "-1"  and ((road_dict[thi].isDuplex == "1") or str(road_dict[thi].cross_begin) == the_cross)  else None
            
        cross_dict[cross_info[1][0].replace("(","")] = CROSS(cross_info[1][0].replace("(",""),road_dict[fir] if fir in road_dict else None,road_dict[sec] if sec in road_dict else None,\
                                                            road_dict[thi] if thi in road_dict else None,road_dict[fot] if fot in road_dict else None)
        '''
    for index,item in road_dict.items():    #以列表返回可遍历的(键, 值) 元组数组
        print("当前道路:",item.ID,"\t直行:",item.stright_road.ID if item.stright_road != None else None,"\t左转:",item.left_road.ID if item.left_road != None else None,"\t右转:",item.right_road.ID if item.right_road != None else None,\
            "\t反直:",item.back_stright.ID if item.back_stright != None else None,"\t反左:",item.back_left.ID if item.back_left != None else None,"\t反右:",item.back_right.ID if item.back_right != None else None)
        '''

    road_bas = int(roads["#(id"][0].replace("(",""))
    all_car_driving_track = []
    sum_car = 0
    add = lambda x : x.cross_begin + x.cross_end
    for index,car in car_dict.items():
        #print("new car")
        start_pos = []
        car_point = []
        delta = car.dest_loc - car.start_loc
        car_point.append(car.start_loc)
        #print("起点：",car.start_loc,"终点：",car.dest_loc)
        if (delta > 0):
            if len(roads[roads['from'] == car.start_loc]["#(id"].index[:]) > 0:
                for i in roads[roads['from'] == car.start_loc]["#(id"].index[:]:
                    start_pos.append(road_dict[str(i + road_bas)].ID)
                #car_point.append(car.now_posi.cross_begin)
            #print("car start positions list:",start_pos)
            #print("begin road:",max(start_pos))
            else:
                for i in roads[(roads['to'] == car.start_loc)]["#(id"].index[:]:
                # 多个起点目前取最后一个起点
                    if road_dict[str(i+road_bas)].isDuplex == "1":
                        
                        start_pos.append(road_dict[str(i + road_bas)].ID) 
        else :
            if len(roads[(roads['to'] == car.start_loc)]["#(id"].index[:]) > 0:
                         
                for i in roads[(roads['to'] == car.start_loc)]["#(id"].index[:]:
                # 多个起点目前取最后一个起点
                    if road_dict[str(i+road_bas)].isDuplex == "1":
                        
                        start_pos.append(road_dict[str(i + road_bas)].ID)
            else:       
                for i in roads[roads['from'] == car.start_loc]["#(id"].index[:]:
                    start_pos.append(road_dict[str(i + road_bas)].ID)    
                    #print("car start positions list:",start_pos)
                    #print("begin road:",min(start_pos))
            #driving_track = [min(start_pos)]
            #car.now_posi = road_dict[str(min(start_pos))]
            #car_point.append(road_dict[str(min(start_pos))].cross_end)
        #driving_track = [car.now_posi.ID]
        #print("car start positions list:",start_pos)
        #print("begin road:",min(start_pos))
        
        for i in range(len(start_pos)):
            driving_track = [start_pos[i]]
            sign = 0
            car.now_posi = road_dict[str(start_pos[i])]
            if int(car.now_posi.cross_end) == int(car.start_loc):
                car_point.append(car.now_posi.cross_begin)
                isStright = [0,]
            else:
                car_point.append(car.now_posi.cross_end)
                isStright = [1,]
            tmp_car = []
            while 1 :
                if car_point[-1] == car.start_loc:
                    break
                if isStright[-1] and car.now_posi.cross_end == car.dest_loc:
                    for road in tmp_car:
                        road.all_right = 1
                    sign = 1
                    break
                elif car.now_posi.cross_begin == car.dest_loc:
                    for road in tmp_car:
                        road.all_right = 1
                    sign = 1
                    break
                #dis = [left_end,right_end,stright_end,b_left_end,b_right_end,b_stright_end]
                #car_next = [car.now_posi.left_road,car.now_posi.right_road,car.now_posi.stright_road,car.now_posi.back_left,car.now_posi.back_right,car.now_posi.back_stright,]
                #print("dis:",dis)
                #print(dis.index(min(dis)))
                #print(car_point)
                
                if car_point[-1] in car_point[:-2] and len(car_point) > 2 :
                #if len(car_point) % 10 == 9:
                    #print("陷入循环！",car.now_posi.ID)
                    car.now_posi.all_right = 0
                    tmp_car.append(car.now_posi)
                    
                    #print("tmp car:",tmp_car,car.now_posi.all_right)
                    if isStright[-1]:
                        car_next = [car.now_posi.left_road,car.now_posi.right_road,car.now_posi.stright_road]
                        try:
                            left_end = abs(add(car.now_posi.left_road) - car_point[-1] - car.dest_loc) if car.now_posi.left_road != None and car.now_posi.left_road.all_right == 1 else 999# / car.now_posi.left_road.length
                        except:
                            left_end = 999
                        try:
                            right_end = abs(add(car.now_posi.right_road) - car_point[-1] - car.dest_loc) if car.now_posi.right_road != None and car.now_posi.right_road.all_right == 1 else 999# / car.now_posi.right_road.length 
                        except:
                            right_end = 999
                        try:
                            stright_end = abs(add(car.now_posi.stright_road) - car_point[-1] - car.dest_loc) if car.now_posi.stright_road != None and car.now_posi.stright_road.all_right == 1 else 999# / car.now_posi.stright_road.length
                        except:
                            stright_end = 999
                        
                    else:
                        car_next = [car.now_posi.back_left,car.now_posi.back_right,car.now_posi.back_stright,]
                        try:
                            left_end = abs(add(car.now_posi.back_left) - car_point[-1] - car.dest_loc) if car.now_posi.back_left != None and car.now_posi.back_left.all_right == 1 else 999# / car.now_posi.back_left.length
                        except:
                            left_end = 999
                        try:
                            right_end = abs(add(car.now_posi.back_right)- car_point[-1]  - car.dest_loc) if car.now_posi.back_right != None and car.now_posi.back_right.all_right == 1 else 999# / car.now_posi.back_right.length
                        except:
                            right_end = 999
                        try:
                            stright_end = abs(add(car.now_posi.back_stright)- car_point[-1] - car.dest_loc) if car.now_posi.back_stright != None and car.now_posi.back_stright.all_right == 1 else 999 #/ car.now_posi.back_stright.length
                        except:
                            stright_end = 999
                    dis = [left_end,right_end,stright_end]
                    if min(dis)==999:
                        car.now_posi.all_right = 0
                        tmp_car.append(car.now_posi)
                        driving_track.pop()
                        car.now_posi = road_dict[str(driving_track[-1])]
                        car_point.pop()
                        isStright.pop()
                        continue
                        #car_point = [tmp_car_point]
                        #car.now_posi = tmp_start_pos
                        #driving_track = [tmp_start]
                        #continue
                    #print("asdas:",dis.index(min(dis)),car.now_posi.ID)
#                    if len(driving_track) >= 2 and car_next[dis.index(min(dis))].ID == driving_track[-2]:
#                    
#                        tmp = dis.copy()
#                        car.now_posi = car_next[dis.index(min(tmp.remove(min(dis))))]
#                        driving_track.append(car_next[dis.index(min(tmp.remove(min(dis))))].ID)
#                        car_point.append(add(car_next[dis.index(min(tmp.remove(min(dis))))])-car_point[-1])
#                    else:
                    car.now_posi = car_next[dis.index(min(dis))]
                    driving_track.append(car_next[dis.index(min(dis))].ID)
                    car_point.append(add(car_next[dis.index(min(dis))])-car_point[-1])
                    if car_point[-1] > car_point[-2]:
                        isStright.append(1)
                    else:
                        isStright.append(0)
                    #print("轨迹：",driving_track)
                    '''
                    del car_next[dis.index(min(dis))]
                    del dis[dis.index(min(dis))]
                    car.now_position = car_next[dis.index(min(dis))]
                    driving_track.append(car_next[dis.index(min(dis))].ID)
                    print(driving_track)
                    '''
                else:
                    if isStright[-1]:
                        car_next = [car.now_posi.left_road,car.now_posi.right_road,car.now_posi.stright_road]
                        try:
                            left_end = abs(add(car.now_posi.left_road) - car_point[-1] - car.dest_loc) if car.now_posi.left_road != None and car.now_posi.left_road.all_right == 1 else 999# / car.now_posi.left_road.length
                        except:
                            left_end = 999
                        try:
                            right_end = abs(add(car.now_posi.right_road) - car_point[-1] - car.dest_loc) if car.now_posi.right_road != None and car.now_posi.right_road.all_right == 1 else 999# / car.now_posi.right_road.length 
                        except:
                            right_end = 999
                        try:
                            stright_end = abs(add(car.now_posi.stright_road) - car_point[-1] - car.dest_loc) if car.now_posi.stright_road != None and car.now_posi.stright_road.all_right == 1 else 999# / car.now_posi.stright_road.length
                        except:
                            stright_end = 999
                        
                    else:
                        car_next = [car.now_posi.back_left,car.now_posi.back_right,car.now_posi.back_stright]
                        try:
                            left_end = abs(add(car.now_posi.back_left) - car_point[-1] - car.dest_loc) if car.now_posi.back_left != None and car.now_posi.back_left.all_right == 1 else 999# / car.now_posi.back_left.length
                        except:
                            left_end = 999
                        try:
                            right_end = abs(add(car.now_posi.back_right)- car_point[-1]  - car.dest_loc) if car.now_posi.back_right != None and car.now_posi.back_right.all_right == 1 else 999# / car.now_posi.back_right.length
                        except:
                            right_end = 999
                        try:
                            stright_end = abs(add(car.now_posi.back_stright)- car_point[-1] - car.dest_loc) if car.now_posi.back_stright != None and car.now_posi.back_stright.all_right == 1 else 999 #/ car.now_posi.back_stright.length
                        except:
                            stright_end = 999
                            
                    dis = [left_end,right_end,stright_end]
                    
                    if min(dis)==999:
                        car.now_posi.all_right = 0
                        tmp_car.append(car.now_posi)
                        driving_track.pop()
                        car.now_posi = road_dict[str(driving_track[-1])]
                        car_point.pop()
                        isStright.pop()
                        #print("dead_road")
                        continue
                        #car_point = [tmp_car_point]
                        #car.now_posi = tmp_start_pos
                        #driving_track = [tmp_start]
                        #continue

#                    if len(driving_track) >= 2 and car_next[dis.index(min(dis))].ID == driving_track[-2]:
#                    
#                        tmp = dis.copy()
#                        car.now_posi = car_next[dis.index(min(tmp.remove(min(dis))))]
#                        driving_track.append(car_next[dis.index(min(tmp.remove(min(dis))))].ID)
#                        car_point.append(add(car_next[dis.index(min(tmp.remove(min(dis))))])-car_point[-1])
#                    else:
                    car.now_posi = car_next[dis.index(min(dis))]
                    driving_track.append(car_next[dis.index(min(dis))].ID)
                    car_point.append(add(car_next[dis.index(min(dis))])-car_point[-1])
                    if car_point[-1] > car_point[-2]:
                        isStright.append(1)
                    else:
                        isStright.append(0)
                    #print("轨迹：",driving_track)
            if sign:
                break
            for road in tmp_car:
                road.all_right = 1
        tmp_track = []
        is_repeat = 0
        while(1):
            for i in driving_track:
                if i in tmp_track:
                    fir_l = driving_track.index(i)
                    sec_l = driving_track[fir_l+1:].index(i)
                    if driving_track[fir_l+1] == driving_track[fir_l+sec_l+2]:
                        
                        driving_track = driving_track[:fir_l]+driving_track[fir_l+sec_l+1:]
                        is_repeat = 1
                        tmp_track = []
                        break
                    right_l = sec_l+fir_l+1
                    if driving_track[fir_l-1] == driving_track[right_l +1]:
                        fir_l -= 1
                        right_l += 1
                        while driving_track[fir_l-1] == driving_track[right_l +1]:
                            fir_l -= 1
                            right_l += 1
                        driving_track = driving_track[:fir_l]+driving_track[right_l+1:]
                        is_repeat = 1
                        tmp_track = []
                        break
                tmp_track.append(i)
                is_repeat = 0
            if not is_repeat:
                break
        sum_car += 1
        times = sum_car//10
        tmp = [car.ID,int(car.start_time)+np.random.randint(int(0.083*len(car_dict))),driving_track]
        all_car_driving_track.append(tmp)
#    tmp = []
#    times = 0
#    while(car_dict):
#        dist = {}
#        car_id = ""
#        start = 0
#        dest = 0
#        if len(car_dict) < 10:
#            for car in car_dict.items():
#                tmp.append([car.ID,np.random.randint(10)*times])
#            break
#        count = 0
#        for index,car in car_dict.items():
#            if count ==0:
#                car_id = car.ID
#                start = car.start_loc
#                dest = car.dest_loc
#                tmp_car = car
#                count += 1
#                continue
#            dist[car.ID] = (abs(start - car.start_loc)+abs(dest - car.dest_loc))
#        sorted_values = sorted(dist.items(),key = lambda item:item[1],reverse = True)
#        tmp.append([car_id,np.random.randint(10)*times]) #every 5 seconds ,lanuch 10 cars
#        car_dict.pop(car_id)
#        for Id in sorted_values[:10]:
#            
#            car_dict.pop(Id[0])
#            tmp.append([Id[0],np.random.randint(10)*times])
#        times += 1
#    for driving_track in tmp:
#        all_car_driving_track[all_car_driving_track[:][0] == driving_track[0]][1] += driving_track[1]
    with open(answer_path,"a+") as f:
        for ct in all_car_driving_track:
            new_context = "(" + str(ct[0]) + "," + str(ct[1])
            for j in range(0,len(ct[2])):
                new_context += "," + ct[2][j]
            new_context += ")\n" 
            f.write(new_context)

if __name__ == "__main__":
    main()
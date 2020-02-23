# -*- coding: gbk -*-

import math
import datetime
from numpy import *

def Init_graph_time(options):
    print "Initing the user_item graph G................."
    G = [[0 for i in range(NUM_USERS + NUM_ITEMS + NUM_TYPE)] for i in range(NUM_USERS + NUM_ITEMS + NUM_TYPE)]
    #[��ֵ,����]
    u2t = [[[0.0,0] for i in range(NUM_USERS + NUM_ITEMS + NUM_TYPE)] for i in range(NUM_USERS + NUM_ITEMS + NUM_TYPE)]
    i2t = [[[0.0,0] for i in range(NUM_USERS + NUM_ITEMS + NUM_TYPE)] for i in range(NUM_USERS + NUM_ITEMS + NUM_TYPE)]
    fileReader = open(options.csvfile,'r')
    fileReader2 = open(options.csvfile2,'r')
    file2 = fileReader2.readlines()
    for line in fileReader.readlines():
        line = line.replace("\n","")
        line = line.replace("\r","")
        line = line.split(" ")
        '''
        #ѵ������ֻȡ�û�ϲ������Ϊ
        if int(line[9]) == 0:
            continue
        '''
        user = int(line[0])
        item = int(line[1]) + NUM_USERS
        length = len(line)
        score = float(line[length-1])
        #score = float(line[2])
        #score = 1
        G[user-1][item-1] = score
        G[item-1][user-1] = score
        #����Ʒ����
        info = file2[item - NUM_USERS - 1]
        info = info.replace("\n","")
        info = info.replace("\r","")
        info = info.split(",")
        type_info = info[1].split("|")[0:-1]
        type_number = len(type_info)
        for i in range(type_number):
            if type_info[i] == "1":
                u2t[user-1][i + NUM_USERS + NUM_ITEMS][0] += score
                u2t[user-1][i + NUM_USERS + NUM_ITEMS][1] += 1
                i2t[item-1][i + NUM_USERS + NUM_ITEMS][0] += score
                i2t[item-1][i + NUM_USERS + NUM_ITEMS][1] += 1

    fileReader.close()
    fileReader2.close()


    '''
    max_u2t = [0 for i in range(NUM_USERS)]
    for i in range(NUM_USERS):
        for j in range(NUM_USERS + NUM_ITEMS,NUM_USERS + NUM_ITEMS + NUM_TYPE):
            if max_u2t[i] < u2t[i][j][0]:
                max_u2t[i] = u2t[i][j][0]
    print max_u2t
    '''
    for i in range(NUM_USERS):
        for j in range(NUM_USERS + NUM_ITEMS,NUM_USERS + NUM_ITEMS + NUM_TYPE):
            if u2t[i][j][1] != 0:
                '''
                G[i][j] = (float(u2t[i][j][0]) * 5) / max_u2t[i]
                G[j][i] = G[i][j]
                #print G[j][i]
                '''

                G[i][j] = float(u2t[i][j][0]) / u2t[i][j][1]
                G[j][i] = G[i][j]


    for i in range(NUM_USERS,NUM_USERS + NUM_ITEMS):
        for j in range(NUM_USERS + NUM_ITEMS,NUM_USERS + NUM_ITEMS + NUM_TYPE):
            if i2t[i][j][1] != 0:
                G[i][j] = float(i2t[i][j][0]) / i2t[i][j][1]
                G[j][i] = G[i][j]

    return G


def PersonalRank(alpha, steps, trasMatrix, type):

    M = mat(trasMatrix)
    MT = M.T
    #r�ǽڵ����ƶȾ���
    #q�ǲ�ѯ����
    query ="query"+"_type"+str(type)+".csv"
    out1 = open(query,'w')
    q = zeros((NUM_ITEMS+NUM_USERS+NUM_TYPE, NUM_USERS), float)
    for user in range(NUM_USERS):
        q[user][user] = 0.2
        q[NUM_USERS+NUM_ITEMS+type-1][user] = 0.8
    for i in range(NUM_USERS+NUM_ITEMS+NUM_TYPE):
        for j in range(NUM_USERS):
            temp = q[i][j]
            out1.write(str(temp) + ", ")
        out1.write("\n")
    out1.close()
    r =q
    for i in range(steps):
        r = alpha * MT * r + (1-alpha)*q
    r = r.tolist()
    #���ڵ����ƶȾ�����к�ֵ���к�ֵд���ļ�
    out1 = "sum_colum"+str(type)+".csv"
    file1 = open(out1,"w")
    for i in range(len(r[0])):
        sum_colum = 0
        for j in range(len(r)):
            sum_colum += r[j][i]
        file1.write(str(sum_colum)+"\n")

    return r

def RemAndEva(time,nrofRecommendList,user_rank,user_items,options,nrofAll_items):
    user_recommendList = Recommend(time,nrofRecommendList,user_rank,user_items,options)
    print "write into rem" + str(time) + ".csv......."
    out = options.outfile2[:-4] + "_type" +  str(time) + ".csv"
    fileWrite = open(out, 'w')
    for user in range(len(user_recommendList)):
        fileWrite.write("u" + str(user+1) + " ")
        for i in range(len(user_recommendList[user])):
            #print user_recommendList[user][i]
            fileWrite.write("i" + str(user_recommendList[user][i][0]) + ":" + str(user_recommendList[user][i][1]) + " ")
        fileWrite.write("\n")
    fileWrite.close()

    Evaluate(time,user_recommendList,nrofAll_items,options)  
    
def Recommend(time,nrofRecommendList,user_rank,user_items,options):
    print "Start to recommend................."
    print "nrofRecommendList: " + str(nrofRecommendList)
    #user_recommendList��һ������ÿ�д�������û��ķ��ʸ��ʷֲ�
    user_recommendList = [[[0 for i in range(2)] for i in range(nrofRecommendList)] for i in range(NUM_USERS)]
    fileReader2 = open(options.csvfile2,'r')
    file2 = fileReader2.readlines()
    for user in range(NUM_USERS):
        for item in range(NUM_ITEMS):
            if user_items[user][item] == 1:
                continue                #�û��ѶԸõ�Ӱ������
                #���item�ǲ��ǵ�ǰ�Ƽ�����
            info = file2[item]
            info = info.split(",")
            type_info = info[1].split("|")[0:-1]
            if type_info[time-1] != "1":            #��ǰitem���ǵ�ǰ�Ƽ�����
                continue
            if user_rank[item+NUM_USERS][user] < user_recommendList[user][nrofRecommendList-1][1]:
                continue                        #�ȵ�ǰ�Ƽ��б����һ��Ԫ�ص���ضȵͣ��޷������Ƽ��б�
            #����ǰ��Ӱ����(���򣩵��Ƽ��б���
            for i in range(nrofRecommendList-2,-1,-1):
                if user_recommendList[user][i][1] < user_rank[item+NUM_USERS][user]:
                    user_recommendList[user][i+1][1] = user_recommendList[user][i][1]
                    user_recommendList[user][i+1][0] = user_recommendList[user][i][0]
                    if i == 0:
                        user_recommendList[user][0][1] = user_rank[item+NUM_USERS][user]
                        user_recommendList[user][0][0] = item+1
                else:
                    user_recommendList[user][i+1][1] = user_rank[item+NUM_USERS][user]
                    user_recommendList[user][i+1][0] = item + 1
                    break
    fileReader2.close()
    return user_recommendList

def Evaluate(time,user_recommendList,nrofAll_items,options):
    print "Start to evaluate................."
    nrofTu = 0
    nrofRu = 0
    nrofCommonElements = 0
    RecommendedList = set()

    test_user_items = [[0 for i in range(NUM_ITEMS)] for i in range(NUM_USERS)]
    #ӵ������time����Ʒ
    fileReader = open(options.csvfile2,'r')
    item_HasTime = set()
    for line in fileReader.readlines():
        line = line.replace("\n","")
        line = line.replace("\r","")
        info = line.split(",")
        item = int(info[0])
        type_info = info[1].split("|")[0:-1]
        if type_info[time - 1] == "1":
            item_HasTime.add(item)
    fileReader.close()
    
    fileReader = open(options.csvfile3,'r')
    for line in fileReader.readlines():
        line = line.replace("\n","")
        line = line.replace("\r","")
        line = line.split(" ")
        '''
        #ѵ������ֻȡ�û�ϲ������Ϊ
        if int(line[9]) == 0:
            continue
        '''
        item = int(line[1])
        #ֻʹ�õ�ǰ���͵Ĳ��Լ�
        if item not in item_HasTime:
            continue
        user = int(line[0])
        item = int(line[1])
        test_user_items[user-1][item-1] = 1
    fileReader.close()
    
    
    for user in range(len(test_user_items)):
        for item in range(len(test_user_items[user])):
            if test_user_items[user][item] == 1:
                nrofTu += 1
    for user in range(len(user_recommendList)):
        for x in range(len(user_recommendList[user])):
            nrofRu += 1
            itemID = user_recommendList[user][x][0]
            RecommendedList.add(itemID)
            if test_user_items[user][itemID-1] == 1:
                nrofCommonElements += 1
    
    print "nrofCommonElements: " + str(nrofCommonElements)
    print "nrofTu: " + str(nrofTu) 
    print "nrofRu: " + str(nrofRu)
    print "nrofAll_items: " + str(nrofAll_items)
    print "RecommendedList: " + str(len(RecommendedList))
    
    #�����ʣ�׼ȷ�ʣ������ʣ����ж�
    if nrofTu == 0:
        Recall = 0.0
    else:
        Recall = float(nrofCommonElements) / nrofTu
    r = Recall
    print "Recall: " + str(Recall)
    Recall = str("%.2f"%(Recall * 100)) + "%"
    Precision = float(nrofCommonElements) / nrofRu
    p = Precision
    print "Precision: " + str(Precision)
    Precision = str("%.2f"%(Precision * 100)) + "%"
    Coverage = float(len(RecommendedList)) / nrofAll_items
    print "Coverage: " + str(Coverage)
    Coverage = str("%.2f"%(Coverage * 100)) + "%"
    if (p + r) > 0:
        f = float(2 * p * r) / (p + r)
    else:
        f = 0.0

    out = options.outfile[:-4] + "_type" + str(time) + ".csv"
    fileWrite = open(out, 'w')
    fileWrite.write("׼ȷ��    �ٻ���    ������    F�ع�" + "\n")
    fileWrite.write(Precision + "    " + Recall + "    " + Coverage + "    " + str(f) + "\n")
    fileWrite.write("���и���: " + str(nrofCommonElements) + "\n")
    fileWrite.write("nrofRu: " + str(nrofRu) + "\n")
    fileWrite.write("nrofTu: " + str(nrofTu) + "\n")
    fileWrite.close()


def Factor(trasMatrix,alpha):
    factor = mat(trasMatrix)
    factor = factor.T
    e = eye(NUM_USERS + NUM_ITEMS)
    factor = e - alpha * factor
    factor = factor.I
    return factor

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-c", "--csvfile", dest="csvfile", default="",
                      action="store", type="string", metavar="FILE",
                      help="CSV file contains imdb top movies' list")
    parser.add_option("-e", "--csvfile2", dest="csvfile2", default="",
                      action="store", type="string", metavar="FILE",
                      help="CSV file contains imdb top movies' list")
    parser.add_option("-n", "--outfile2", dest="outfile2", default="",
                      action="store", type="string", metavar="FILE",
                      help="CSV file contains imdb top movies' list")
    parser.add_option("-l", "--csvfile3", dest="csvfile3", action="store",
                      type="string", default="", metavar="FILE",
                      help="search languages: en--englis, zh-simplified chinese")
    parser.add_option("-o", "--outfile", dest="outfile", default="",
                      action="store", type="string", metavar="FILE",
                      help="search results of given movie list")
    parser.add_option("-p", "--outfile3", dest="outfile3", default="",
                      action="store", type="string", metavar="FILE",
                      help="search results of given movie list")
    (options, args) = parser.parse_args()
    # -c TimeDecay_0.9.csv -e item.csv -l test.csv -o eva_TD_MDR.csv -n rem_TD_MDR.csv
    if options.csvfile and options.csvfile3 and options.outfile and options.outfile2:
        starttime = datetime.datetime.now()
        trainusers = set()
        trainitems = set()
        allitems = set()
        allusers = set()
                   
        #ͳ��ѵ�����е���������Ʒ��
        fileReader = open(options.csvfile,'r')
        for line in fileReader.readlines():
            line = line.replace("\n","")
            line = line.replace("\r","")
            line = line.split(" ")
            user = line[0]
            item = line[1]
            if user not in trainusers:
                trainusers.add(user)
            if item not in trainitems:
                trainitems.add(item)
        fileReader.close()

        allitems = trainitems
        allusers = trainusers
        test_user_items = []
        #ͳ�Ʋ��Լ��е���������Ʒ��
        fileReader = open(options.csvfile3,'r')
        for line in fileReader.readlines():
            line = line.replace("\n","")
            line = line.replace("\r","")
            line = line.split(" ")
            user = line[0]
            item = line[1]
            if user not in allusers:
                allusers.add(user)
            if item not in allitems:
                allitems.add(item)
        fileReader.close()
        
        global NUM_USERS
        NUM_USERS = len(allusers)
        global NUM_ITEMS
        NUM_ITEMS = len(allitems)
        global NUM_TYPE
        NUM_TYPE = 31
        print "Nrof users in trainning set: " + str(len(trainusers))
        print "Nrof items in trainning set: " + str(len(trainitems))
        print "Nrof users in all set: " + str(len(allusers))
        print "Nrof items in all set: " + str(len(allitems))
                   
        #�ҳ��û���ѵ�������Ѿ����ʹ�����Ʒ
        user_items = [[0 for i in range(NUM_ITEMS)] for i in range(NUM_USERS)]
        fileReader = open(options.csvfile,'r')
        for line in fileReader.readlines():
            line = line.replace("\n","")
            line = line.replace("\r","")
            line = line.split(" ")
            user = int(line[0])
            item = int(line[1])
            user_items[user-1][item-1] = 1
        fileReader.close()

        '''
        #�ҳ��û��ڲ��Լ���ѡ�����Ʒ
        test_user_items = [[0 for i in range(NUM_USERS + NUM_ITEMS)] for i in range(NUM_USERS + NUM_ITEMS)]
        fileReader = open(options.csvfile3,'r')
        for line in fileReader.readlines():
            line = line.replace("\n","")
            line = line.replace("\r","")
            line = line.split()
            user = int(line[0])
            item = int(line[1]) + NUM_USERS
            test_user_items[user-1][item-1] = 1
        fileReader.close()
        '''
        
        #��ʼ��ͼG
        starttime1 = datetime.datetime.now()
        G = Init_graph_time(options)
        print "Graph G has " + str(len(G)) + " nodes"
        endtime1 = datetime.datetime.now()
        print  unicode(endtime1)
        timeUse1 = unicode((endtime1-starttime1).seconds)
        print timeUse1
        #Hammock��ͼ,wͨ��ʵ��õ�
        '''
        uw = 115
        G = Hammock(G,uw)
        '''
        #����������������ָ��,ѵ����ѵ��
        alpha = 0.8
        #ͨ��ʵ��õ���������
        steps = 45
                   
        #����G1ת�ƾ���
        print "Init G1 trasMatrix....."
        trasMatrixFile = open("transMatrix.csv",'w')

        trasMatrix = [[0 for i in range(NUM_USERS + NUM_ITEMS + NUM_TYPE)] for i in range(NUM_USERS + NUM_ITEMS + NUM_TYPE)]
        for i in range(NUM_USERS + NUM_ITEMS + NUM_TYPE):
            sum_raw = 0
            sum_ij = 0
            for j in range(NUM_USERS + NUM_ITEMS + NUM_TYPE):
                sum_ij += float(G[i][j])
            if sum_ij == 0:
                continue
            for j in range(NUM_USERS + NUM_ITEMS + NUM_TYPE):
                trasMatrix[i][j] = float(G[i][j]) / sum_ij
                sum_raw += trasMatrix[i][j]
            trasMatrixFile.write(str(sum_raw)+ "\n")
        #����(1-alpha*MT)����
        #factor = Factor(trasMatrix,alpha)
                   
        #user_rankÿһ�д�����е�һ��Ԫ���µ�rankֵ���п��Դ���������ڲ�ͬ��㿪ʼ�����µı�����ֵ�����Կ�����Ҫ�ԡ�
        #user_rank = PersonalRank(G,alpha,steps,trasMatrix)
        
        #�Ƽ�����ָ������ʼ�Ƽ�������¼�Ƽ����
        nrofRecommendList = 15
        #user_recommendList��һ�� �û���*�Ƽ����� �ľ���ÿ�д�������û��ķ��ʸ��ʷֲ�
        #�ֱ����NUM_TYPE���Ƽ��Ͳ���

        nrofAll_items = len(allitems)
        type_list=[14,18,21,19,15,9,27,25,8,10,26,11]    #��Ӱ�������
        for type in type_list:
            user_rank = PersonalRank(alpha,steps,trasMatrix,type)
            RemAndEva(type,nrofRecommendList,user_rank,user_items,options,nrofAll_items)
            print

        #��¼ʱ��
        endtime = datetime.datetime.now()
        print  unicode(endtime)
        timeUse = unicode((endtime-starttime).seconds)
        print timeUse
        
        
    else:
        parser.error("need to specify -c -e -o parameter")




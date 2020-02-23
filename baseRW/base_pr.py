# -*- coding: gbk -*-

import math
import datetime
from numpy import *

def Init_graph_time(options):
    print "Initing the user_item graph G................."
    G = [[0 for i in range(NUM_USERS + NUM_ITEMS)] for i in range(NUM_USERS + NUM_ITEMS)]
    #[��ֵ,����]
    '''
    u2t = [[[0.0,0] for i in range(NUM_USERS + NUM_ITEMS)] for i in range(NUM_USERS + NUM_ITEMS )]
    i2t = [[[0.0,0] for i in range(NUM_USERS + NUM_ITEMS)] for i in range(NUM_USERS + NUM_ITEMS )]
    '''
    fileReader = open(options.csvfile,'r')
    #fileReader2 = open(options.csvfile2,'r')
   # file2 = fileReader2.readlines()
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
        score = float(line[2])
        #score = float(line[2])
        #score = 1
        G[user-1][item-1] = score
        G[item-1][user-1] = score
        #����Ʒ����
        '''
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
    '''
    fileReader.close()


    return G



def PersonalRank(G,alpha,steps,trasMatrix):
    print "Start to Rank..............."
    #user_rankÿһ�д�����е�һ��Ԫ���µ�rankֵ
    #r0�ǵ�λ����e

    r0 = eye(NUM_USERS + NUM_ITEMS )
    user_rank = r0
    M = mat(trasMatrix)
    MT = M.T

    f = (r0 - alpha * MT)
    f = f.I
    user_rank  = (1 - alpha) * f * r0
    user_rank = user_rank.tolist()

    user_rank_file1 = open("sum_colum.csv",'w')

    for i in range(len(user_rank)):
        sum_colum = 0
        for j in range(len(user_rank)):
            sum_colum += user_rank[j][i]
        user_rank_file1.write(str(sum_colum)+"\n")


    #����ÿ��
    '''
    for step in range(steps):
        print "SETP " + str(step+1) + " personal rank....."
        user_rank = (1 - alpha) * r0 + alpha * MT * user_rank
        
        #��ӡÿ�ε����Ĳ��ֽ����ȷ����������
        temp = user_rank.tolist()
        p = 0
        print "step: " + str(step)
        for k in range(NUM_USERS + NUM_ITEMS):
            print "number " + str(k) + ": " + str(temp[k][0])
            p += 1
            if p >= 10:
                break
       # print

    user_rank = user_rank.tolist()
    for i in range(len(user_rank)):
        sum_colum = 0
        sum_raw = 0
        for j in range(len(user_rank)):
            sum_colum += user_rank[j][i]
            sum_raw += user_rank[i][j]
        user_rank_file1.write(str(sum_colum)+"\n")
        user_rank_file2.write(str(sum_raw)+"\n")
    '''
    return user_rank


def RemAndEva(nrofRecommendList,user_rank,user_items,options,nrofAll_items):
    user_recommendList = Recommend(nrofRecommendList,user_rank,user_items,options)
    out = options.outfile2[:-4] + ".csv"
    fileWrite = open(out, 'w')
    for user in range(len(user_recommendList)):
        fileWrite.write("u" + str(user+1) + " ")
        for i in range(len(user_recommendList[user])):
            #print user_recommendList[user][i]
            fileWrite.write("i" + str(user_recommendList[user][i][0]) + ":" + str(user_recommendList[user][i][1]) + " ")
        fileWrite.write("\n")
    fileWrite.close()

    Evaluate(user_recommendList,nrofAll_items,options)
    
def Recommend(nrofRecommendList,user_rank,user_items,options):
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
            
            if user_rank[item+NUM_USERS][user] < user_recommendList[user][nrofRecommendList-1][1]:
                continue                        #�ȵ�ǰ�Ƽ��б����һ��Ԫ�ص���ضȵͣ��޷������Ƽ��б�
            #����ǰ��Ӱ����(���򣩵��Ƽ��б���
            for i in range(nrofRecommendList-2,-1,-1):
                if user_recommendList[user][i][1] < user_rank[item+NUM_USERS][user] :
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

def Evaluate(user_recommendList,nrofAll_items,options):
    print "Start to evaluate................."
    nrofTu = 0
    nrofRu = 0
    nrofCommonElements = 0
    RecommendedList = set()

    test_user_items = [[0 for i in range(NUM_ITEMS)] for i in range(NUM_USERS)]
    
    fileReader = open(options.csvfile3,'r')
    for line in fileReader.readlines():
        line = line.replace("\n","")
        line = line.replace("\r","")
        line = line.split(" ")
       
        
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

    out = options.outfile[:-4] +".csv"
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
    #  -c train.csv -e item.csv -l test.csv -o eva_base_PR.csv -n rem_base_PR.csv
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

        trasMatrix = [[0 for i in range(NUM_USERS + NUM_ITEMS )] for i in range(NUM_USERS + NUM_ITEMS)]
        for i in range(NUM_USERS + NUM_ITEMS):
            sum_raw = 0
            sum_ij = 0
            for j in range(NUM_USERS + NUM_ITEMS ):
                sum_ij += float(G[i][j])
            if sum_ij == 0:
                for j in range(NUM_USERS + NUM_ITEMS ):
                    trasMatrix[i][j] = float(1) / (NUM_USERS + NUM_ITEMS)
                continue
            for j in range(NUM_USERS + NUM_ITEMS ):
                trasMatrix[i][j] = float(G[i][j]) / sum_ij
                sum_raw += trasMatrix[i][j]
            trasMatrixFile.write(str(sum_raw)+ "\n")
        #����(1-alpha*MT)����
        #factor = Factor(trasMatrix,alpha)
                   
        #user_rankÿһ�д�����е�һ��Ԫ���µ�rankֵ���п��Դ���������ڲ�ͬ��㿪ʼ�����µı�����ֵ�����Կ�����Ҫ�ԡ�
        user_rank = PersonalRank(G,alpha,steps,trasMatrix)
        
        #�Ƽ�����ָ������ʼ�Ƽ�������¼�Ƽ����
        nrofRecommendList = 15
        #user_recommendList��һ�� �û���*�Ƽ����� �ľ���ÿ�д�������û��ķ��ʸ��ʷֲ�
        #�ֱ����NUM_TYPE���Ƽ��Ͳ���

        nrofAll_items = len(allitems)
        
         
        RemAndEva(nrofRecommendList,user_rank,user_items,options,nrofAll_items)


        
        

        
        





# -*- coding: gbk -*-


import time
import math
'''���û�����Ϊ����ʱ��˥��
'''
def TimeDecay(score,t0,t,tmax,Theta):
    """
    :param score:   ��ʼ���
    :param t0:      ��ʼʱ��
    :param t:       ���ʱ��
    :param tmax:    ����ʱ��
    :param Theta:   ��������
    :return:       ����ʱ��˥����Ĵ��
    """
    if tmax == t0:
        tmax = tmax + 1
    ft = (1 - Theta) + Theta * ((float((t - t0)) / (tmax-t0)) * (float((t - t0)) / (tmax-t0)))
    return score * ft
    
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
    parser.add_option("-l", "--lang", dest="lang", action="store",
                      type="string", default="en", metavar="LANG",
                      help="search languages: en--englis, zh-simplified chinese")
    parser.add_option("-o", "--outfile", dest="outfile", default="",
                      action="store", type="string", metavar="FILE",
                      help="search results of given movie list")
    (options, args) = parser.parse_args()
    print options.csvfile
    print options.outfile
    #-c train.csv  -o TimeDecay.csv
    if options.csvfile and options.outfile:
        #��С-���淶��ʱ������
        user_items = dict()
        r = open(options.csvfile,'r')
        for line in r.readlines():
            line = line.replace("\n","")
            line = line.replace("\r","")  #str����
            info = line.split(" ")        #list����
            user = info[0]
            if user not in user_items:
                user_items[user] = list()
            #user_items[user]��ʾ�û�user��������Ϊ
            user_items[user].append(line)
        r.close()
        new_max = 100
        new_min = 0
        new_span_time = new_max - new_min
        w = open(options.outfile,'w')           #�����˥��ֵ֮������ݼ�
        for user,lines in user_items.items():
            num = len(lines)                #�û�����Ϊ��
            max_time = int(lines[num-1].split(" ")[3])      #��ǰ�û���Ϊʱ������ֵ
            min_time = int(lines[0].split(" ")[3])          #��ǰ�û���Ϊʱ�����Сֵ
            span_time = max_time - min_time
            for i in range(num):
                curr_time = int(lines[i].split(" ")[3])     #��һ��֮ǰ���û���Ϊʱ��

                new_time = ((curr_time - min_time) * new_span_time / (span_time+1) )+ new_min       #��һ��֮�����Ϊʱ��
                new_line = lines[i]+" "+str(new_time)
                w.write(new_line+"\n")                      #�µ���Ϊ���ݣ�ʱ���һ����д���ļ�
                user_items[user][i] = new_line              #�����û���Ϊ�ֵ�
        w.close()

        #����˥��
        theta_list = [0.15,0.3,0.45,0.6,0.75,0.9]
        for theta in theta_list:
            out = options.outfile[:-4] +"_"+str(theta)+".csv"
            w = open(out,'w')
            for user,lines in user_items.items():
                num = len(lines)                            #��ǰ�û���Ϊ��
                first_info = lines[0].split(" ")            #��ǰ�û���һ����Ϊ
                last_info = lines[num-1].split(" ")         #��ǰ�û����һ����Ϊ
                length = len(first_info)                    #�û���Ϊ��Ϣ����
                t0 = int(first_info[length-1])                   #��һ���û���Ϊ��Ӧ��ʱ��
                tmax = int(last_info[length-1])                  #���һ���û���Ϊ��Ӧ��ʱ��
                for i in range(num):
                    curr_info = lines[i].split(" ")             #��i���û���Ϊ
                    t = int(curr_info[length-1])                 #��ǰ�û���Ϊ��ʱ��
                    score = int(curr_info[2])                    #��ǰ�û��Ĵ��

                    new_score = TimeDecay(score,t0,t,tmax,theta)
                    #print user,t0,t,tmax,score,theta,new_score
                    new_line = lines[i]+" "+str(new_score)
                    w.write(new_line + "\n")
            w.close()
    else:
        print "need right param -c ... -o ..."

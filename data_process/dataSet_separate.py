# -*- coding: gbk -*-

import random

#���ݼ�����

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-c", "--csvfile", dest="csvfile", default="",
                      action="store", type="string", metavar="FILE",
                      help="remList")
    parser.add_option("-e", "--csvfile2", dest="csvfile2", default="",
                      action="store", type="string", metavar="FILE",
                      help="u.test")
    parser.add_option("-n", "--csvfile3", dest="csvfile3", default="",
                      action="store", type="string", metavar="FILE",
                      help="P")
    parser.add_option("-l", "--outfile2", dest="outfile2", action="store",
                      type="string", default="", metavar="FILE",
                      help="Q")
    parser.add_option("-o", "--outfile", dest="outfile", default="",
                      action="store", type="string", metavar="FILE",
                      help="search results of given movie list")
    (options, args) = parser.parse_args()
    #-c douban_new.csv -o train.csv -l test.csv
    if options.csvfile and options.outfile2 and options.outfile:
        fileReader = open(options.csvfile,'r')
        w1 = open(options.outfile,'w')
        w2 = open(options.outfile2,'w')
        user_dict = dict()                  #ͳ�����ݼ���ÿ���û�����Ϊ��
        for line in fileReader.readlines():
            line = line.replace("\n", "")
            line = line.split(",")
            user = line[0]
            if user not in user_dict:
                user_dict[user] = 1
            else:
                user_dict[user]  += 1
        fileReader.close()
        user_set = set()                    #��¼�Ѿ����������֣����û�
        fileReader = open(options.csvfile,'r')
        for line in fileReader.readlines():
            line = line.replace("\n","")
            line = line.split(",")
            user = line[0]
            if user not in user_set:        #ÿ����һ�����û�������n=0��ʼ��������
                user_set.add(user)
                n = 0
            if n < user_dict[user] * 0.8:
                line = " ".join(line)       #listת��Ϊ�ַ�������","����
                w1.write(line + "\n")
                n = n + 1
            else:
                line = " ".join(line)
                w2.write(line + "\n")
        fileReader.close()
        w1.close()
        w2.close()





    '''
    if options.csvfile and options.outfile2 and options.outfile:
        #��ȡ�Ƽ��б�����
        flag = 0
        fileReader = open(options.csvfile,'r')
        w1 = open(options.outfile,'w')
        w2 = open(options.outfile2,'w')
        for line in fileReader.readlines():
            line = line.replace("\n","")
            flag = random.random()
            print flag
            #С��0.8�ķ���ѵ������0.8���ĺ�Ϳ��Ե�������
            if flag <=0.8:
                w1.write(line + "\n")
            else:
                w2.write(line + "\n")
        fileReader.close()
        w1.close()
        w2.close()
        
    else:
        parser.error("need to specify -c -e -o parameter")
    '''




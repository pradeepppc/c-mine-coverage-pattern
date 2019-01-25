import time
import sys


class cmine():
    def __init__(self, minRF, minCS, maxOR, inpfile, outfile):
        self.minRF = minRF
        self.minCS = minCS
        self.maxOR = maxOR
        self.inpfile = inpfile
        self.outfile = outfile
        self.nots = self.getlines(inpfile)
        self.fout = open(outfile, 'w')
        self.NOk = []
        self.items = self.dbscan(inpfile)

        print(self.outfile)
        print(self.items)

        sorteditems = sorted(self.items.items(), key = lambda a: (-a[1], a[0]))
        print(sorteditems)
        mintracs = self.minRF * 1.0 * self.nots
        freqitems = filter(lambda x: (x[1] >= mintracs), sorteditems)
        print(freqitems)
        one_size_coverage = filter(lambda x: (x[1] >= minCS*self.nots), freqitems)
        print(one_size_coverage)
        self.freqitems = map(lambda x: x[0], freqitems)

        for i in self.freqitems:
            self.NOk.append([i])
        for i in one_size_coverage:
            self.fout.write("['"+str(i[0])+"']\n")
        
    def get_overlapratio_cs(self, pattern):
        ovr_nume_1=set()
        for i in pattern[:-1]:
            for j in range(len(self.database)):
                if i in self.database[j]:
                    ovr_nume_1.add(j)
        ovr_deno = set()
        for j in range(len(self.database)):
            if pattern[-1] in self.database[j]:
                ovr_deno.add(j)
        cs_nume = ovr_nume_1.union(ovr_deno)
        ovr_nume = ovr_nume_1.intersection(ovr_deno)
        # print ovr_nume,ovr_deno,ovr_nume_1
        return len(ovr_nume)*1.0/len(ovr_deno),len(cs_nume)*1.0/self.nots

    def prune(self,patterns):
        f = open(self.inpfile,'r')
        for row in f:
            row = row.rstrip('\n')
            row = row.split(",")
            if len(row[-1]) == 0:
                row.pop()
            for i in range(len(patterns)):
                ovr_flag = False
                for item in patterns[i][0][:-1]:
                    if item in row:
                        patterns[i][1] += 1
                        ovr_flag = True
                        break
                if(patterns[i][0][-1] in row):
                    patterns[i][3] += 1
                    if ovr_flag == True:
                        patterns[i][2] += 1
                    else:
                        patterns[i][1] += 1
            # print row,patterns

        NOk = []
        coverage_patterns = []
        for i in patterns:
            if i[2]*1.0/i[3] <= self.maxOR:
                NOk.append(i[0])
                if i[1]*1.0/self.nots >= self.minCS:
                    coverage_patterns.append(i)
        return NOk,coverage_patterns




    def expand(self):
        cnt = 0
        cnt1 = 0
        length = 1
        while len(self.NOk)>0:
            print("length",length,len(self.NOk))
            C_k=[]
            for i in range(len(self.NOk)):
                for j in range(i+1,len(self.NOk)):
                    cnt += 1
                    if(self.NOk[i][:-1] == self.NOk[j][:-1]):
                        cnt1 += 1
                        newpattern = self.NOk[i] + [self.NOk[j][-1]]
                        C_k.append([newpattern,0,0,0])
                    else:
                        break
            length += 1
            # print "C_k",C_k
            self.NOk, coverage_patterns = self.prune(C_k)
            # print "NOk",self.NOk
            # print "coverage patterns",coverage_patterns 
            for i in coverage_patterns:
                self.fout.write('['+str(i[0])+']'+"\n")
        return cnt1       
    # def expand(self):
    #     cnt = 0
    #     cnt1 = 0
    #     length = 1;
    #     while len(self.NOk)>0:
    #         print "length",length,len(self.NOk)
    #         temp_NOk = self.NOk
    #         self.NOk = []
    #         for i in range(len(temp_NOk)):
    #             for j in range(i+1, len(temp_NOk)):
    #                 cnt += 1
    #                 if temp_NOk[i][:-1] == temp_NOk[j][:-1]:
    #                     cnt1 += 1
    #                     newpattern = temp_NOk[i] + [temp_NOk[j][-1]]
    #                     # print "newpattern",newpattern
    #                     overlapratio,cs = self.get_overlapratio_cs(newpattern)
    #                     # print newpattern,overlapratio,cs
    #                     if overlapratio <= maxOR:
    #                         self.NOk.append(newpattern)
    #                         if cs >= minCS:
    #                             # print "This is coverage pattern",newpattern,cs,overlapratio
    #                             self.fout.write(str(newpattern)+"\n")
    #                 else:
    #                     break
    #         length += 1
    #     print "total read, total calculate_or_cs",cnt,cnt1
    #     self.fout.close()
        # return cnt1

    def dbscan(self, inputfile):
        f = open(inputfile, 'r')
        a = {}
        # database = []
        for row in f:
            row = row.rstrip('\n')
            row = row.split(",")
            if len(row[-1]) == 0:
                row.pop()
            # database.append(row)
            for j in row:
                if j in a:
                    a[j] += 1
                else:
                    a[j] = 1
        return a

    def getlines(self, filename):
        with open(filename, "r") as f:
            return sum(1 for _ in f)

t1 = time.time()
minRF = float(sys.argv[1])
minCS = float(sys.argv[2])
maxOR = float(sys.argv[3])
inpfile = sys.argv[4]
outfile = sys.argv[5]
# splitted = inpfile.split("/")
# filepath = sys.argv[6]
# outfile = filepath+"./outputs/"+splitted[2]+"_"+str(minRF)+"_"+str(minCS)+"_"+str(maxOR)+"_"+sys.argv[5]
# inpfile = filepath+inpfile
obj = cmine(minRF, minCS, maxOR, inpfile, outfile)
# t3 = time.time()
# print("data read", str(t3-t1))
# candidate_patterns = obj.expand()
# t2 = time.time()
# print("process done", str(t2-t1))
# excel = open(filepath+"./times_new.csv", 'a')
# excel.write("cmine"+","+str(minRF)+","+str(minCS)+","+str(maxOR)+","+inpfile+","+outfile+","+str(t3-t1)+","+str(candidate_patterns)+","+str(t2-t1)+"\n")
# excel.close()

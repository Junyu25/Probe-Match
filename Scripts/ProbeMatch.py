## by jinhui tang
##set up ls -R data/*.fna >seq.txt
## usage   nohup python /home/jhtang/probe/script/probeMatch.py -p probe.fasta -s seq.txt & 
from __future__ import print_function
import glob,os,re,argparse,time,math
import pandas as pd
from Bio import SeqIO
from multiprocessing import Pool 


def probe_match(probeFile,seqFile,misMatchNum):
    file = open('%s' % (seqFile),'r')
    #out_file = open('result.txt','w')
    cwd = os.getcwd()
    count = 0
    for i in file:
        rootName = i.rstrip()
        rawprobe_iterator = SeqIO.parse("%s/%s" % (cwd,probeFile),"fasta")
        rawseq_iterator = SeqIO.parse("%s/%s" % (cwd,rootName),"fasta")
        seqBase = pd.DataFrame(columns = ('typeName','seq'))
        rawseq = {}
        j = 0
        
        for each in rawseq_iterator:
            j += 1
            rawseq[j]=each
            
        rawprobe={}
        i = 0
        probeBase = pd.DataFrame(columns = ('proId','proSeq'))
        for each in rawprobe_iterator:
            i += 1
            rawprobe[i]=each    
        #print(rawdata[i])
        for i in range(1,len(rawprobe)+1):
            probeBase = probeBase.append({'proId':i,'proSeq':str(rawprobe[i].seq.reverse_complement())},ignore_index= True,sort = False)
        
        
        record0 = pd.DataFrame(columns=('proId','locId','MM_position','MM_No','typeName'))
        record = record0
        recordAll = pd.DataFrame(columns=('proId','locId','MM_position','MM_No','typeName'))
        recordAll['typeName'].astype(str)
        jj=0
        for ii in range(1,len(rawseq)+1):   # if there are 2 or more seq
            seq = str(rawseq[ii].seq)
            seqName =rawseq[ii].name
            for z in range(0,len(rawprobe)):    # for num of probe
                probe = probeBase.iloc[z]['proSeq']
                proId = probeBase.iloc[z]['proId']
                record0 = pd.DataFrame(columns=('proId','locId','MM_position','MM_No','typeName','rootName'))
                for j in range(0,len(seq)-len(probe)):    # make sure the tail is intact  
                    
                    seqTest=seq[j:j+len(probe)]   
                    MM_No = 0
                    MM_position = []
                    for i in range (0,len(seqTest)):   # check each position if they are the same 
                        if seqTest[i] != probe[i]:
                            MM_position.append(i)
                            MM_No += 1
                        i += 1
                    if j != 0:                       # only find the min num for each probe when matching to a seq
                        if MM_No <= misMatchNum:
                            record0=record0.append(pd.DataFrame({'proId':proId,'locId': [j],
                                                         'MM_position':[MM_position],'MM_No':[MM_No],'typeName':[seqName],
                                                                'rootName':[rootName]}),sort=False)                
                recordAll= recordAll.append(record0,sort= False)
        if count==0:
            out_data = recordAll
            count += 1
        else:
            out_data = out_data.append(recordAll,sort=False)
    out_data.to_excel('result.xlsx')
    #out_file.close()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--probe', dest='probe', type=str, required=True,
                        help="the probe file needed for match-test")
    parser.add_argument('-s', '--seqfile', dest='seqFile', type=str, required=True,
                        help="the file *.txt containing the name of seq")
    parser.add_argument('-um', '--misMatchNum', dest='misMatchNum', type=int, required=False,default=4,
                        help="the mismatch number between probe and seq, smaller or equal to the setting will be output")
    args = parser.parse_args()
    probeFile = args.probe
    seqFile = args.seqFile
    misMatchNum = args.misMatchNum
    probe_match(probeFile,seqFile,misMatchNum)
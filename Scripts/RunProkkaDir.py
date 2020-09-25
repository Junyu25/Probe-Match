import os
import argparse
import subprocess
from Bio import SeqIO
from shutil import copyfile
from itertools import repeat
from multiprocessing import Pool, freeze_support

#Run on Dir    
def RunProkkaDir(Dir):
    prefixList = []
    fileList = []
    outFileList = []
    for run in os.listdir(Dir):
        if os.path.exists(os.path.join(Dir, run)):
            prefixList.append(run.replace(".fasta", ""))
            fileList.append(os.path.join(Dir, run))
            outFileList.append(os.path.join(ouputDir, run.replace(".fasta", "")))
    RunProkkaParallel(fileList, outFileList, prefixList)



#Run Prokka in parallel
def RunProkkaParallel(fileList, outFileList, prefixList):
    #numOfprocess = len(R1List)
    #pool = Pool(processes=numOfprocess)
    pool = Pool(processes=4)
    pool.starmap(RunProkka, zip(fileList, outFileList, prefixList))
    pool.close()
    pool.join()
    pool.terminate()

def RunProkka(fasta, outDir, prefix):
    cmd = "prokka --kingdom Bacteria --addgenes --prefix " + prefix + " --outdir " + outDir + " --force " + fasta
    print(cmd)
    subprocess.call(cmd, shell=True)


parser = argparse.ArgumentParser(description='Run Prokka in Dir')
parser.add_argument('-i', '--input', dest='fileDir', type=str, required=True,
                    help="the path of the reads")
parser.add_argument('-o', '--output', dest='OpDir', type=str, required=True,
                    help="the output path of reads")
parser.add_argument('-j', '--jobs', dest='jobs', type=str,  required=False, default='4',
                    help="the number of jobs run in parallel")
parser.add_argument('-t', '--threads', dest='threads', type=str, required=False, default='6',
                    help="the number of threads run for a job")
args = parser.parse_args()

inputDir = os.path.abspath(args.fileDir)
ouputDir = os.path.abspath(args.OpDir)
jobs = int(args.jobs)
threads = int(args.threads)

RunProkkaDir(inputDir)
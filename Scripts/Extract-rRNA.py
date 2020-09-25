# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 09:52:16 2019

@author: Junyu
"""

import os
import argparse
from BCBio import GFF
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation



limit_info = dict(gff_type = ["rRNA"])
        
def FindrRNA(path, tempFile):
    
    in_handle = open(path)
    for record in GFF.parse(in_handle, limit_info=limit_info):
        if len(record.features) != 0:
            for i in range(len(record.features)):
                if '23S ribosomal RNA' in record.features[i].qualifiers["product"][0]:
                    '''
                    seq_23S = SeqRecord(record.features[i].location.extract(record.seq),\
                                    id=record.features[i].id,\
                                    description=str(record.id +'-'+ record.features[i].qualifiers["product"][0]))
                    '''
                    seq_23S = SeqRecord(record.features[i].location.extract(record.seq),\
                                    id=tempFile[:-4],\
                                    description=str(record.id +'-'+record.features[i].id+'-'+ record.features[i].qualifiers["product"][0]+'-'+str(len(record.seq))))
                    #print(seq_23S)
                    #SeqIO.write(seq_23S, path[:-4]+"_23S_rRNA.fasta", "fasta")
                    SeqIO.write(seq_23S, os.path.join(ouputDir, tempFile[:-4]+"_23S_rRNA.fasta"), "fasta")
                elif '16S ribosomal RNA' in record.features[i].qualifiers["product"][0]:
                    #print(record.features[i])
                    #print(record.id)
                    seq_16S = SeqRecord(record.features[i].location.extract(record.seq),\
                                    id=tempFile[:-4],\
                                    description=str(record.id +'-'+record.features[i].id+'-'+ record.features[i].qualifiers["product"][0]+'-'+str(len(record.seq))))
                    #SeqIO.write(seq_16S, path[:-4]+"_16S_rRNA.fasta", "fasta")
                    SeqIO.write(seq_16S, os.path.join(ouputDir, tempFile[:-4]+"_16S_rRNA.fasta"), "fasta")
                    #print(seq_16S)

    in_handle.close()


parser = argparse.ArgumentParser(description='FindrRNA')
parser.add_argument('-i', '--input', dest='fileDir', type=str, required=True,
                    help="the path of the prokka output file Dir")
parser.add_argument('-o', '--output', dest='OpDir', type=str, required=True,
                    help="the out Dir")               
args = parser.parse_args()

inputDir = os.path.abspath(args.fileDir)
ouputDir = os.path.abspath(args.OpDir)

for root,dirs,files in os.walk(inputDir):
    for tempFile in files:
        if "gff" in tempFile:
            path = os.path.join(root,tempFile)
            FindrRNA(path, tempFile)
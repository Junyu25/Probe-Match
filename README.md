# Probe Match

## Prokka - Contigs annotation

https://github.com/tseemann/prokka

#### Basic usage:

`prokka --outdir mydir --prefix mygenome contigs.fa`

`prokka --outdir Root11 --prefix Root11 Root11.fna`

```shell
for fasta in `ls | grep .fna`
do
    prokka --outdir /home/junyuchen/Lab/Probe-Match/Root-WGS-Annotated/${fasta:0:-4} --prefix ${fasta:0:-4} $fasta
done
```


```python
!python ./Scripts/RunProkkaDir.py -h
```

    usage: RunProkkaDir.py [-h] -i FILEDIR -o OPDIR [-j JOBS] [-t THREADS]
    
    Run Prokka in Dir
    
    optional arguments:
      -h, --help            show this help message and exit
      -i FILEDIR, --input FILEDIR
                            the path of the reads
      -o OPDIR, --output OPDIR
                            the output path of reads
      -j JOBS, --jobs JOBS  the number of jobs run in parallel
      -t THREADS, --threads THREADS
                            the number of threads run for a job


## Extract rRNA

#### bcbio-gff
https://biopython.org/wiki/GFF_Parsing   
`conda install -c bioconda bcbio-gff` #Bug


```python
pip install bcbio-gff
```

```shell
python /home/junyuchen/Lab/Probe-Match/Probe-Match/Scripts/Extract-rRNA.py -i /home/junyuchen/Lab/Probe-Match/Probe-Match/demo/data -o /home/junyuchen/Lab/Probe-Match/Probe-Match/demo/result
```

## Probe Match


```python
!python ./Scripts/ProbeMatch.py -h
```

    usage: ProbeMatch.py [-h] -p PROBE -s SEQFILE [-um MISMATCHNUM]
    
    optional arguments:
      -h, --help            show this help message and exit
      -p PROBE, --probe PROBE
                            the probe file needed for match-test
      -s SEQFILE, --seqfile SEQFILE
                            the file *.txt containing the name of seq
      -um MISMATCHNUM, --misMatchNum MISMATCHNUM
                            the mismatch number between probe and seq, smaller or
                            equal to the setting will be output


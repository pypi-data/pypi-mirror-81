# Copyright (c) 2020, Renesh Bedre (see LICENSE)

from sklearn.decomposition import PCA
import pandas as pd
import re
import os
import numpy as np
from bioinfokit.visuz import screeplot, pcaplot, general
from itertools import groupby, chain, combinations
import string
import sys
import csv
import matplotlib.pyplot as plt
import scipy.stats as stats
from tabulate import tabulate
from statsmodels.graphics.mosaicplot import mosaic
from textwrap3 import wrap
from statsmodels.formula.api import ols
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from decimal import Decimal
from pathlib import Path
from sklearn.metrics import mean_squared_error
from collections import defaultdict
from shutil import which
from subprocess import check_output, STDOUT, CalledProcessError
from statsmodels.stats.libqsturng import psturng, qsturng


def seqcov(file="fastq_file", gs="genome_size"):
    general.depr_mes("bioinfokit.analys.fastq.seqcov")


def mergevcf(file="vcf_file_com_sep"):
    general.depr_mes("bioinfokit.analys.marker.mergevcf")


def pca(table="p_df"):
    print("This function is deprecated")


def extract_seq(file="fasta_file", id="id_file"):
    # extract seq from fasta file based on id match
    id_list = []
    id_file = open(id, "rU")
    out_file = open("output.fasta", 'w')
    for line in id_file:
        id_name = line.rstrip('\n')
        id_list.append(id_name)
    list_len = len(id_list)
    value = [1] * list_len
    # id_list converted to dict for faster search
    dict_list = dict(zip(id_list, value))
    fasta_iter = fasta_reader(file)
    for record in fasta_iter:
        fasta_header, seq = record
        if fasta_header.strip() in dict_list.keys():
            out_file.write(">"+fasta_header+"\n"+seq+"\n")
    out_file.close()
    id_file.close()


# remove seqs which match to ids in id file
def extract_seq_nomatch(file="fasta_file", id="id_file"):
    # extract seq from fasta file based on id match
    id_list = []
    id_file = open(id, "rU")
    out_file = open("output.fasta", 'w')
    for line in id_file:
        id_name = line.rstrip('\n')
        id_list.append(id_name)
    list_len = len(id_list)
    value = [1] * list_len
    # id_list converted to dict for faster search
    dict_list = dict(zip(id_list, value))
    fasta_iter = fasta_reader(file)
    for record in fasta_iter:
        fasta_header, seq = record
        if fasta_header.strip() not in dict_list.keys():
            out_file.write(">"+fasta_header+"\n"+seq+"\n")
    out_file.close()
    id_file.close()


def fqreadcounter(file="fastq_file"):
    general.depr_mes("bioinfokit.analys.fastq.fqreadcounter")


def fasta_reader(file="fasta_file"):
    general.depr_mes("bioinfokit.analys.fasta.fasta_reader")


def rev_com(seq=None, file=None):
    general.depr_mes("bioinfokit.analys.fasta.rev_com")


# extract subseq from genome sequence
def ext_subseq(file="fasta_file", id="chr", st="start", end="end", strand="plus"):
    fasta_iter = fasta_reader(file)
    for record in fasta_iter:
        fasta_header, seq = record
        if id == fasta_header.strip() and strand == "plus":
            # -1 is necessary as it counts from 0
            sub_seq = seq[int(st-1):int(end)]
            print(sub_seq)
        elif id == fasta_header.strip() and strand == "minus":
            seq = rev_com(seq)
            sub_seq = seq[int(st-1):int(end)]
            print(sub_seq)


def fastq_format_check(file="fastq_file"):
    general.depr_mes("bioinfokit.analys.fastq.fastq_format_check")


def tcsv(file="tab_file"):
    tab_file = csv.reader(open(file, 'r'), dialect=csv.excel_tab)
    csv_file = csv.writer(open('out.csv', 'w', newline=''), dialect=csv.excel)

    for record in tab_file:
        csv_file.writerow(record)


def ttsam(df='dataframe', xfac=None, res=None, evar=True):
    general.depr_mes("bioinfokit.visuz.stat.ttsam")


def chisq(table="table"):
    general.depr_mes("bioinfokit.visuz.stat.chisq")


class fasta:
    def __init__(self):
        pass

    # adapted from https://www.biostars.org/p/710/
    def fasta_reader(file="fasta_file"):
        read_file = open(file, "rU")
        fasta_iter = (rec[1] for rec in groupby(read_file, lambda line: line[0] == ">"))
        for record in fasta_iter:
            fasta_header = record.__next__()[1:].strip()
            fasta_header = re.split("\s+", fasta_header)[0]
            seq = "".join(s.strip() for s in fasta_iter.__next__())
            yield fasta_header, seq

    def rev_com(seq=None, file=None):
        if seq is not None:
            rev_seq = seq[::-1]
            rev_seq = rev_seq.translate(str.maketrans("ATGCUN", "TACGAN"))
            return rev_seq
        elif file is not None:
            out_file = open("output_revcom.fasta", 'w')
            fasta_iter = fasta_reader(file)
            for record in fasta_iter:
                fasta_header, seq = record
                rev_seq = seq[::-1]
                rev_seq = rev_seq.translate(str.maketrans("ATGCUN", "TACGAN"))
                out_file.write(">" + fasta_header + "\n" + rev_seq + "\n")
            out_file.close()

    def ext_subseq(file="fasta_file", id="chr", st="start", end="end", strand="plus"):
        fasta_iter = fasta.fasta_reader(file)
        for record in fasta_iter:
            fasta_header, seq = record
            if id == fasta_header.strip() and strand == "plus":
                # -1 is necessary as it counts from 0
                sub_seq = seq[int(st - 1):int(end)]
                print(sub_seq)
            elif id == fasta_header.strip() and strand == "minus":
                sub_seq = seq[int(st - 1):int(end)]
                sub_seq_rc = fasta.rev_com(seq=sub_seq)
                print(sub_seq_rc)


class fastq:
    def __init__(self):
        pass

    def fastq_reader(file="fastq_file"):
        fastq_file = open(file, "r")
        for line in fastq_file:
            header_1 = line.rstrip()
            read = next(fastq_file).rstrip()
            header_2 = next(fastq_file).rstrip()
            read_qual_asc = next(fastq_file).rstrip()
            yield header_1, read, header_2, read_qual_asc

    def fqreadcounter(file="fastq_file"):
        read_file = open(file, "rU")
        num_lines = 0
        total_len = 0
        for line in read_file:
            num_lines += 1
            header_1 = line.rstrip()
            read = next(read_file).rstrip()
            len_read = len(read)
            total_len += len_read
            header_2 = next(read_file).rstrip()
            read_qual = next(read_file).rstrip()
        read_file.close()
        num_reads = num_lines / 4
        return num_reads, total_len

    def fastq_format_check(file="fastq_file"):
        read_file = open(file, 'r')
        x = 0
        for line in read_file:
            header = line.rstrip()
            if not header.startswith('@'):
                x = 1
            else:
                x = 0
            break
        return x

    def detect_fastq_variant(file="fastq_file"):
        count = 0
        check = []
        fastq_file = open(file, 'rU')

        for line in fastq_file:
            header_1 = line.rstrip()
            read = next(fastq_file).rstrip()
            header_2 = next(fastq_file).rstrip()
            read_qual_asc = next(fastq_file).rstrip()
            asc_list = list(read_qual_asc)
            asc_list = list(map(ord, asc_list))
            min_q = min(asc_list)
            max_q = max(asc_list)
            check.append(min_q)
            check.append(max_q)
            count += 1
            if count == 40000:
                break
        fastq_file.close()
        min_q = min(check)
        max_q = max(check)
        if 64 > min_q >= 33 and max_q == 74:
            return 1
        elif min_q >= 64 and 74 < max_q <= 104:
            return 2
        elif 64 > min_q >= 33 and max_q <= 73:
            return 3

    def split_fastq(file="fastq_file"):
        x = fastq.fastq_format_check(file)
        if x == 1:
            print("Error: Sequences are not in sanger fastq format")
            sys.exit(1)
        fastq_iter = fastq.fastq_reader(file)
        out_file_name_1 = open(Path(file).stem+'_1.fastq', 'w')
        out_file_name_2 = open(Path(file).stem+'_2.fastq', 'w')
        i = 1
        for record in fastq_iter:
            header_1, read, header_2, read_qual_asc = record
            if (i % 2) == 0:
                out_file_name_2.write(header_1+'\n'+read+'\n'+header_2+'\n'+read_qual_asc+'\n')
            else:
                out_file_name_1.write(header_1+'\n'+read+'\n'+header_2+'\n'+read_qual_asc+'\n')
            i += 1

        out_file_name_1.close()
        out_file_name_2.close()

    def sra_bd(file='sra_list_in_file', paired=False, prog='fasterq-dump', t=4, other_opts=None):
        if which(prog) is None:
            raise Exception(prog + ' does not exist. Please install sra toolkit and add to system path')
        if prog not in 'fasterq-dump':
            raise Exception('Only fasterq-dump program supported')
        read_f = open(file, 'r')
        for sra in read_f:
            print('Donwloading ' + sra.strip() + '\n')
            if paired:
                try:
                    if other_opts:
                        cmd = [prog, '-e', str(t), '--split-files']
                        cmd.extend(other_opts.split())
                        cmd.extend(sra.strip())
                        check_output(cmd, stderr=STDOUT)
                    else:
                        check_output([prog, '-e', str(t), '--split-files', sra.strip()], stderr=STDOUT)
                except CalledProcessError as e:
                    print('Error: there is something wrong with the subprocess command or input fastq already '
                          'available\n See detaled error \n')
                    print(e.returncode, e.output, '\n')
            else:
                try:
                    if other_opts:
                        cmd = [prog, '-e', str(t)]
                        cmd.extend(other_opts.split())
                        cmd.extend([sra.strip()])
                        check_output(cmd, stderr=STDOUT)
                    else:
                        check_output([prog, '-e', str(t), sra.strip()], stderr=STDOUT)
                except CalledProcessError as e:
                    print('Error: there is something wrong with the subprocess command or input fastq already '
                          'available\n See detaled error \n' )
                    print(e.returncode, e.output, '\n')

        read_f.close()

    def seqcov(file="fastq_file", gs="genome_size"):
        x = fastq.fastq_format_check(file)
        if x == 1:
            print("Error: Sequences are not in fastq format")
            sys.exit(1)
        num_reads, total_len = fastq.fqreadcounter(file)
        # haploid genome_size must be in Mbp; convert in bp
        gs = gs * 1e6
        cov = round(float(total_len / gs), 2)
        print("Sequence coverage for", file, "is", cov)


class marker:

    def __init__(self):
        pass

    def mergevcf(file="vcf_file_com_sep"):
        print('mergevcf renamed to concatvcf')

    def concatvcf(file="vcf_file_com_sep"):
        vcf_files = file.split(",")
        merge_vcf = open("concat_vcf.vcf", "w+")
        file_count = 0
        print("concatenating vcf files...")
        for f in vcf_files:
            if file_count == 0:
                read_file = open(f, "rU")
                for line in read_file:
                    merge_vcf.write(line)
                read_file.close()
            elif file_count > 0:
                read_file = open(f, "rU")
                for line in read_file:
                    if not line.startswith("#"):
                        merge_vcf.write(line)
                read_file.close()
            file_count += 1
        merge_vcf.close()

    def splitvcf(file='vcf_file', id='#CHROM'):
        read_vcf_file = open(file, 'r')
        info_lines, headers = [], []
        for line in read_vcf_file:
            if line.startswith(id):
                headers = line.strip().split('\t')
            elif line.startswith('##'):
                info_lines.append(line.strip())
        read_vcf_file.close()
        assert len(headers) != 0, "Non matching id parameter"
        read_vcf_file_df = pd.read_csv(file, sep='\t', comment='#', header=None)
        read_vcf_file_df.columns = headers
        chrom_ids = read_vcf_file_df[id].unique()
        for r in range(len(chrom_ids)):
            sub_df = read_vcf_file_df[read_vcf_file_df[id]==chrom_ids[r]]
            # out_vcf_file = open(chrom_ids[r]+'.vcf'
            with open(chrom_ids[r]+'.vcf', 'w') as out_vcf_file:
                for l in info_lines:
                    out_vcf_file.write(l+'\n')
            sub_df.to_csv(chrom_ids[r]+'.vcf', mode='a', sep='\t', index=False)
            out_vcf_file.close()

    def vcfreader(file='vcf_file', id='#CHROM'):
        read_vcf_file = open(file, 'r')
        info_lines, headers = [], []
        for line in read_vcf_file:
            if line.startswith(id):
                headers = line.strip().split('\t')
            elif line.startswith('##'):
                info_lines.append(line.strip())
            else:
                var_lines = line.strip().split('\t')
                yield headers, info_lines, var_lines
        read_vcf_file.close()
        assert len(headers) != 0, "Non matching id parameter"


    def vcf_anot(file='vcf_file', gff_file='gff_file', id='#CHROM', anot_attr=None):
        gff_iter = gff.gffreader(gff_file)
        gene_cord = defaultdict(list)
        cds_cord = defaultdict(list)
        exon_cord = defaultdict(list)
        ftr_cord = defaultdict(list)
        ttr_cord = defaultdict(list)
        sc_cord = defaultdict(list)
        st_cord = defaultdict(list)
        igenic_cord = defaultdict(list)
        intragenic_cord = defaultdict(list)
        # also for introns between the exons
        intragenic_cord_exon = defaultdict(list)
        gene_id_dict = dict()
        transcript_name_dict = dict()
        transcript_strand_dict = dict()
        chr_list = set([])
        for record in gff_iter:
            chr, gene_id, gene_name, transcript_id, source, feature_type, st, ende, strand, attr = record
            if feature_type == 'gene':
                if chr not in chr_list:
                    gene_number_1 = 1
                chr_list.add(chr)
                gene_cord[(chr, gene_id, gene_number_1)]=[st, ende]
                gene_id_dict[(chr, gene_number_1)] = gene_id
                gene_number_1 += 1
            elif feature_type == 'mRNA' or feature_type == 'transcript':
                cds_cord[(chr, transcript_id)] = []
                exon_cord[(chr, transcript_id)] = []
                ftr_cord[transcript_id] = []
                ttr_cord[transcript_id] = []
                sc_cord[transcript_id] = []
                st_cord[transcript_id] = []
                transcript_strand_dict[transcript_id] = strand
                if anot_attr:
                    transcript_name_dict[transcript_id] = re.search(anot_attr+'=(.+?)(;|$)',  attr).group(1)
            elif feature_type == 'CDS':
                cds_cord[(chr, transcript_id)].append([st, ende])
            elif feature_type == 'exon':
                exon_cord[(chr, transcript_id)].append([st, ende])
            elif feature_type == 'five_prime_UTR':
                ftr_cord[(chr, transcript_id)].append([st, ende])
            elif feature_type == 'three_prime_UTR':
                ttr_cord[(chr, transcript_id)].append([st, ende])
            elif feature_type == 'start_codon':
                sc_cord[(chr, transcript_id)].append([st, ende])
            elif feature_type == 'stop_codon':
                st_cord[(chr, transcript_id)].append([st, ende])

        # get intergenic regions
        for gene, cord in gene_cord.items():
            chr, gene_id, gene_number = gene[0], gene[1], gene[2]
            for x in chr_list:
                if x == chr and gene_number == 1:
                    igenic_cord[(chr, gene_id)] = [1, int(cord[0])-1]
                elif x == chr and gene_number != 1:
                    igenic_cord[(chr, gene_id)] = \
                        [int(gene_cord[(chr, gene_id_dict[(chr, int(gene_number)-1)], int(gene_number)-1)][1])+1, int(cord[0])-1]

        # get intragenic regions based on CDS
        for transcript, cord in cds_cord.items():
            chr, transcript_id = transcript[0], transcript[1]
            intragenic_cord[(chr, transcript_id)] = []
            for x in chr_list:
                if x == chr:
                    cord.sort(key=lambda k: k[0])
                    if len(cord) > 1:
                        for y in range(len(cord)-1):
                            intragenic_cord[(chr, transcript_id)].append([int(cord[y][1])+1, int(cord[y+1][0])-1])

        # get intragenic regions based on exon
        for transcript, cord in exon_cord.items():
            chr, transcript_id = transcript[0], transcript[1]
            intragenic_cord_exon[(chr, transcript_id)] = []
            for x in chr_list:
                if x == chr:
                    cord.sort(key=lambda k: k[0])
                    if len(cord) > 1:
                        for y in range(len(cord) - 1):
                            intragenic_cord_exon[(chr, transcript_id)].append([int(cord[y][1]) + 1, int(cord[y + 1][0]) - 1])

        def var_region_check(_dict, _chr,  _region, _anot_attr, _transcript_name_dict, _var_region, _transcript_name,
                             _transcript_id, _transcript_strand):
            for transcript, cord in _dict.items():
                for i in range(len(cord)):
                    if transcript[0] == chr and int(cord[i][0]) <= int(var_pos) <= int(cord[i][1]):
                        _var_region = _region
                        _transcript_id = transcript[1]
                        _transcript_strand = transcript_strand_dict[_transcript_id]
                        if anot_attr:
                            _transcript_name = transcript_name_dict[_transcript_id]
                        break
                if _var_region:
                    break
            return _var_region, _transcript_name, _transcript_id, _transcript_strand

        vcf_iter = marker.vcfreader(file, id)
        try:
            # os.remove(Path(file).stem+'_anot.vcf')
            os.remove(Path(file).stem + '_anot.txt')
        except OSError:
            pass
        # vcf_out_anot = open(Path(file).stem+'_anot.vcf', 'a')
        vcf_out_anot = open(Path(file).stem + '_anot.txt', 'a')
        for_info_lines = 1
        transcript_id=None
        transcript_name=None
        transcript_strand=None
        transcript_name_return=transcript_name
        transcript_id_return=transcript_id
        transcript_strand_return=transcript_strand
        for record in vcf_iter:
            headers, info_lines, chr, var_pos = record[0], record[1], record[2][0], record[2][1]
            if for_info_lines == 1:
                for_info_lines = 0
                # for l in info_lines:
                #    vcf_out_anot.write(l+'\n')
                headers.extend(['genomic region', 'transcript ID', 'transcript name', 'strand'])
                vcf_out_anot.write('\t'.join(x for x in headers) + '\n')

            var_region = None
            if var_region is None:
                for transcript, cord in igenic_cord.items():
                    if transcript[0] == chr and int(cord[0]) <= int(var_pos) <= int(cord[1]):
                        var_region = 'Intergenic'
                        transcript_id_return = None
                        transcript_strand_return = None
                        if anot_attr:
                            transcript_name_return = None
                        break
            if var_region is None:
                var_region, transcript_name_return, transcript_id_return, transcript_strand_return = var_region_check(cds_cord, chr, 'CDS',
                    anot_attr, transcript_name_dict, var_region, transcript_name, transcript_id, transcript_strand)
            if var_region is None:
                var_region, transcript_name_return, transcript_id_return, transcript_strand_return = var_region_check(ftr_cord, chr,
                    'five_prime_UTR', anot_attr, transcript_name_dict, var_region, transcript_name, transcript_id, transcript_strand)
            if var_region is None:
                var_region, transcript_name_return, transcript_id_return, transcript_strand_return = var_region_check(ttr_cord, chr,
                    'three_prime_UTR', anot_attr, transcript_name_dict, var_region, transcript_name, transcript_id, transcript_strand)
            if var_region is None:
                var_region, transcript_name_return, transcript_id_return, transcript_strand_return = var_region_check(sc_cord, chr,
                    'start_codon', anot_attr, transcript_name_dict, var_region, transcript_name, transcript_id, transcript_strand)
            if var_region is None:
                var_region, transcript_name_return, transcript_id_return, transcript_strand_return = var_region_check(st_cord, chr,
                    'stop_codon', anot_attr, transcript_name_dict, var_region, transcript_name, transcript_id, transcript_strand)
            if var_region is None:
                var_region, transcript_name_return, transcript_id_return, transcript_strand_return = var_region_check(exon_cord, chr,
                    'exon', anot_attr, transcript_name_dict, var_region, transcript_name, transcript_id, transcript_strand)

            '''
            if var_region is None:
                for transcript, cord in cds_cord.items():
                    for i in range(len(cord)):
                        if transcript[0] == chr and int(cord[i][0]) <= int(var_pos) <= int(cord[i][1]):
                            var_region = 'CDS'
                            transcript_id = transcript[1]
                            if anot_attr:
                                transcript_name = transcript_name_dict[transcript_id]
                            break
                    if var_region:
                        break
            
            if var_region is None:
                for transcript, cord in ftr_cord.items():
                    for i in range(len(cord)):
                        if transcript[0] == chr and int(cord[i][0]) <= int(var_pos) <= int(cord[i][1]):
                            var_region = 'five_prime_UTR'
                            break
                    if var_region:
                        break
                        
            if var_region is None:
                for transcript, cord in ttr_cord.items():
                    for i in range(len(cord)):
                        if transcript[0] == chr and int(cord[i][0]) <= int(var_pos) <= int(cord[i][1]):
                            var_region = 'three_prime_UTR'
                            break
                    if var_region:
                        break
                        
            if var_region is None:
                for transcript, cord in sc_cord.items():
                    for i in range(len(cord)):
                        if transcript[0] == chr and int(cord[i][0]) <= int(var_pos) <= int(cord[i][1]):
                            var_region = 'start_codon'
                            break
                    if var_region:
                        break
            if var_region is None:
                for transcript, cord in st_cord.items():
                    for i in range(len(cord)):
                        if transcript[0] == chr and int(cord[i][0]) <= int(var_pos) <= int(cord[i][1]):
                            var_region = 'stop_codon'
                            break
                    if var_region:
                        break            
            # keep exons at end as it also contains UTR part
            if var_region is None:
                for transcript, cord in exon_cord.items():
                    for i in range(len(cord)):
                        if transcript[0] == chr and int(cord[i][0]) <= int(var_pos) <= int(cord[i][1]):
                            var_region = 'exon'
                            break
                    if var_region:
                        break            
            '''
            if var_region is None:
                for transcript, cord in intragenic_cord.items():
                    transcript_strand_return = transcript_strand_dict[transcript[1]]
                    transcript_id_return = transcript[1]
                    if len(cord) >= 1:
                        for i in range(len(cord)):
                            if transcript[0] == chr and int(cord[i][0]) <= int(var_pos) <= int(cord[i][1]):
                                var_region = 'Introns'
                                break
                    if var_region:
                        break

            if var_region is None:
                for transcript, cord in intragenic_cord_exon.items():
                    transcript_strand_return = transcript_strand_dict[transcript[1]]
                    transcript_id_return = transcript[1]
                    if len(cord) >= 1:
                        for i in range(len(cord)):
                            if transcript[0] == chr and int(cord[i][0]) <= int(var_pos) <= int(cord[i][1]):
                                var_region = 'Introns'
                                break
                    if var_region:
                        break

            vcf_out_anot.write('\t'.join(str(x) for x in record[2])+'\t'+str(var_region)+'\t'+str(transcript_id_return)+
                               '\t'+str(transcript_name_return)+'\t'+str(transcript_strand_return)+'\n')


class format:
    def __init__(self):
        pass

    def fqtofa(file="fastq_file"):
        x = fastq.fastq_format_check(file)
        if x == 1:
            print("Error: Sequences are not in sanger fastq format")
            sys.exit(1)

        read_file = open(file, "rU")
        out_file = open("output.fasta", 'w')
        for line in read_file:
            header_1 = line.rstrip()
            read = next(read_file).rstrip()
            header_2 = next(read_file).rstrip()
            read_qual = next(read_file).rstrip()
            out_file.write(header_1+"\n"+'\n'.join(wrap(read, 60))+"\n")
        read_file.close()

    def tabtocsv(file="tab_file"):
        tab_file = csv.reader(open(file, 'r'), dialect=csv.excel_tab)
        csv_file = csv.writer(open('output.csv', 'w', newline=''), dialect=csv.excel)

        for record in tab_file:
            csv_file.writerow(record)

    def csvtotab(file="csv_file"):
        csv_file = csv.reader(open(file, 'r'), dialect=csv.excel)
        tab_file = csv.writer(open('output.txt', 'w', newline=''), dialect=csv.excel_tab)

        for record in csv_file:
            tab_file.writerow(record)

    def hmmtocsv(file="hmm_file"):
        hmm_file = open(file, "rU")
        csv_file = open("ouput_hmm.csv", "w")

        for line in hmm_file:
            line = line.strip()
            if not line.startswith("#"):
                data = re.split(' +', line)
                if len(data) == 19:
                    data[18] = data[18].replace(',', ' ')
                    csv_file.write(str.join(',', data))
                    csv_file.write("\n")
                elif len(data) > 19:
                    ele = list(range(18, len(data)))
                    data[18] = " ".join([e for i, e in enumerate(data) if i in ele])
                    data[18] = data[18].replace(',', '')
                    csv_file.write(str.join(',', data[0:19]))
                    csv_file.write("\n")
        hmm_file.close()
        csv_file.close()

    # find sanger fastq phred quality encoding format
    def fq_qual_var(file=None):
        if file is None:
            print("Error: No sanger fastq file provided")
            sys.exit(1)
        x = fastq.fastq_format_check(file)
        if x == 1:
            print("Error: Sequences are not in sanger fastq format")
            sys.exit(1)

        qual_format = fastq.detect_fastq_variant(file)

        if qual_format == 1:
            print("The fastq quality format is illumina 1.8+ (Offset +33)")
        elif qual_format == 2:
            print("The fastq quality format is illumina 1.3/1.4 (Offset +64)")
        elif qual_format == 3:
            print("The fastq quality format is Sanger (Offset +33)")
        else:
            print("\nError: Wrong quality format\n")
            sys.exit(1)


class stat:
    def __init__(self):
        self.anova_summary = None
        self.data_summary = None
        self.tukey_summary = None
        self.tukey_groups = None

    '''
    def anova(self, df='dataframe', xfac=None, res=None):
        # drop NaN
        df = df.dropna()
        df = df[[xfac[0], res]]
        assert xfac and res is not None, "xfac or res variable is missing"
        grand_mean = df[res].mean()
        total_obs = df.count()[0]

        if len(xfac) == 1:
            levels = df[xfac[0]].unique()
            assert len(levels) > 2, 'levels must be more than 2; use two-sample t-test for two levels'
            levels.sort()
            ss_trt_between = np.sum(df.groupby(xfac).count() * (df.groupby(xfac).mean()-grand_mean)**2)[0]
            ss_err_within = 0
            for name, group in df.groupby(xfac):
                ss_err_within = ss_err_within + np.sum((group[res]-group[res].mean()) ** 2)
            ss_total = ss_trt_between + ss_err_within
            df_trt_between = len(levels)-1
            df_err_within = total_obs-len(levels)
            df_total = df_trt_between + df_err_within
            ms_trt_between = ss_trt_between / df_trt_between
            ms_err_within = ss_err_within / df_err_within
            f_value = ms_trt_between / ms_err_within
            p_value = '%.4E' % Decimal(stats.f.sf(f_value, df_trt_between, df_err_within))
            anova_table = []
            anova_table.append(
                ["Model", df_trt_between, ss_trt_between, round(ms_trt_between, 4), round(f_value, 4), p_value])
            anova_table.append(["Error", df_err_within, ss_err_within, round(ms_err_within, 4), "", ""])
            anova_table.append(["Total", df_total, ss_total, "", "", ""])
            print("\nANOVA Summary:\n")
            print(tabulate(anova_table, headers=["Source", "Df", "Sum Squares", "Mean Squares", "F", "Pr(>F)"]),
                  "\n")
    '''
    @staticmethod
    def _data_summary(df='dataframe', xfac_var=None, res_var=None):
        data_summary_dict = dict()
        data_summary_dict['Group'] = []
        data_summary_dict['Count'] = []
        data_summary_dict['Mean'] = []
        data_summary_dict['Std Dev'] = []
        data_summary_dict['Min'] = []
        data_summary_dict['25%'] = []
        data_summary_dict['50%'] = []
        data_summary_dict['75%'] = []
        data_summary_dict['Max'] = []
        levels = df[xfac_var].unique()
        for i in levels:
            temp = df.loc[df[xfac_var] == i, res_var]
            data_summary_dict['Group'].append(i)
            data_summary_dict['Count'].append(temp.describe().to_numpy()[0])
            data_summary_dict['Mean'].append(temp.describe().to_numpy()[1])
            data_summary_dict['Std Dev'].append(temp.describe().to_numpy()[2])
            data_summary_dict['Min'].append(temp.describe().to_numpy()[3])
            data_summary_dict['25%'].append(temp.describe().to_numpy()[4])
            data_summary_dict['50%'].append(temp.describe().to_numpy()[5])
            data_summary_dict['75%'].append(temp.describe().to_numpy()[6])
            data_summary_dict['Max'].append(temp.describe().to_numpy()[7])
        return pd.DataFrame(data_summary_dict)

    def tukey_hsd(self, df="dataframe", res_var=None, xfac_var=None, anova_xfac_var=None, phalpha=0.05):
        df = df.dropna()
        if xfac_var is None or anova_xfac_var is None:
            raise ValueError('Invalid value for xfac_var or anova_xfac_var')
        tukey_phoc = dict()
        tukey_phoc['group1'] = []
        tukey_phoc['group2'] = []
        tukey_phoc['Diff'] = []
        tukey_phoc['Lower'] = []
        tukey_phoc['Upper'] = []
        # tukey_phoc['Significant'] = []
        tukey_phoc['q-value'] = []
        tukey_phoc['p-value'] = []
        # group_letter = dict()
        group_pval = dict()
        # group_let = dict()
        # share_let = dict()
        levels = df[xfac_var].unique()

        self.anova_stat(df, res_var, anova_xfac_var)
        df_res = self.anova_summary.df.Residual
        mse = self.anova_summary.sum_sq.Residual / df_res
        self.data_summary = stat._data_summary(df, xfac_var, res_var)

        # q critical
        q_crit = qsturng(1 - phalpha, len(levels), df_res)
        # t critical tcrit = qcrit /\sqrt 2.
        # t_crit = q_crit / np.sqrt(2)
        tuke_hsd_crit = q_crit * np.sqrt(mse / len(levels))
        # let_num = 97
        # let_num_list = []
        # sharing_letter = dict()

        for i in range(len(levels)):
            for j in range(len(levels)):
                if i < len(levels)-1 and j < len(levels)-1 and levels[i] != levels[j+1] and j+1 > i:
                    mean_diff = max(self.data_summary.loc[self.data_summary['Group'] == levels[j+1], 'Mean'].to_numpy()[0],
                                    self.data_summary.loc[self.data_summary['Group'] == levels[i], 'Mean'].to_numpy()[0]) - \
                                min(self.data_summary.loc[
                                        self.data_summary['Group'] == levels[j + 1], 'Mean'].to_numpy()[0],
                                    self.data_summary.loc[self.data_summary['Group'] == levels[i], 'Mean'].to_numpy()[
                                        0])
                    t_val = mean_diff / np.sqrt(2 * (mse / len(levels) ) )
                    # count for groups; this is useful when sample size not equal -- Tukey-Kramer
                    group1_count = self.data_summary.loc[self.data_summary['Group'] == levels[i], 'Count'].to_numpy()[0]
                    group2_count = self.data_summary.loc[self.data_summary['Group'] == levels[j+1], 'Count'].to_numpy()[
                        0]
                    # https://www.uvm.edu/~statdhtx/StatPages/MultipleComparisons/unequal_ns_and_mult_comp.html
                    # also for considering unequal sample size
                    mse_factor = np.sqrt(np.divide(mse, group1_count) + np.divide(mse, group2_count))
                    q_val = mean_diff / np.divide(mse_factor, np.sqrt(2))
                    tukey_phoc['group1'].append(levels[i])
                    tukey_phoc['group2'].append(levels[j+1])
                    tukey_phoc['Diff'].append(mean_diff)
                    # when equal sample size
                    tukey_phoc['Lower'].append(mean_diff - (q_crit * np.sqrt(np.divide(mse, 2) *
                                                                             (np.divide(1, group1_count) +
                                                                              np.divide(1, group2_count)) ) ) )
                    tukey_phoc['Upper'].append(mean_diff + (q_crit * np.sqrt(np.divide(mse, 2) *
                                                                             (np.divide(1, group1_count) +
                                                                              np.divide(1, group2_count))) ) )
                    # tukey_phoc['Significant'].append(np.abs(mean_diff) > tuke_hsd_crit)
                    # t test related to qvalue as q = sqrt(2) t
                    # ref https://www.real-statistics.com/one-way-analysis-of-variance-anova/unplanned-comparisons/tukey-hsd/
                    tukey_phoc['q-value'].append(q_val)
                    if isinstance(psturng(np.abs(q_val), len(levels), df_res), np.ndarray):
                        group_pval[(levels[i], levels[j+1])] = psturng(np.abs(q_val), len(levels), df_res)[0]
                        tukey_phoc['p-value'].append(psturng(np.abs(q_val), len(levels), df_res)[0])
                    else:
                        group_pval[(levels[i], levels[j + 1])] = psturng(np.abs(q_val), len(levels), df_res)
                        tukey_phoc['p-value'].append(psturng(np.abs(q_val), len(levels), df_res))

                    '''
                    if psturng(np.abs(q_val), len(levels), df_res) < 0.05:
                        if levels[i] not in group_letter and levels[j+1] not in group_letter:
                            assigned = 1
                            group_letter[levels[i]] = let_num
                            let_num_list.append(let_num)
                            group_letter[levels[j + 1]] = let_num_list[-1] + 1
                            let_num_list.append(let_num_list[-1] + 1)
                            print(let_num_list, 'a')
                        elif levels[j+1] not in group_letter:
                            assigned = 1
                            group_letter[levels[j + 1]] = let_num_list[-1] + 1
                            let_num_list.append(let_num_list[-1] + 1)
                            print(levels[i], levels[j + 1], let_num_list, 'b')
                        elif levels[j+1] in group_letter:
                            if assigned == 1:
                                group_letter[levels[j + 1]] = let_num_list[-1] + 1
                                let_num_list.append(let_num_list[-1] + 1)
                                assigned = 0
                                print(levels[i], levels[j + 1], let_num_list, 'd')

                    else:
                        if levels[i] not in group_letter and levels[j+1] not in group_letter:
                            assigned = 1
                            group_letter[levels[i]] = let_num
                            let_num_list.append(let_num)
                            group_letter[levels[j + 1]] = let_num
                            let_num_list.append(let_num)
                            sharing_letter[levels[i]] = 0
                            sharing_letter[levels[j+1]] = 0
                            print(levels[i], levels[j+1], let_num_list, 'e')
                        elif levels[j + 1] in group_letter:
                            assigned = 1
                            print(levels[i], levels[j+1], sharing_letter, 'g')
                            if levels[j + 1] in sharing_letter:
                                group_letter[levels[i]] = [group_letter[levels[i]], group_letter[levels[j+1]]]
                                let_num_list.append(group_letter[levels[i]])
                                print(let_num_list, 'f')
                            else:
                                group_letter[levels[j + 1]] = group_letter[levels[i]]
                                let_num_list.append(group_letter[levels[i]])
                                print(let_num_list, 'c')
                        elif levels[j + 1] not in group_letter:
                            assigned = 1
                            group_letter[levels[j + 1]] = group_letter[levels[i]]
                            let_num_list.append(group_letter[levels[i]])
                            print(levels[i], levels[j+1], let_num_list, 'h')
                    '''
        '''
        # print(group_letter)
        # group_letter_chars = {m: chr(n) for m, n in group_letter.items()}
        let_list = []
        for k, v in group_pval.items():
            # print(k)
            if v <= phalpha:
                if k[0] in group_let and k[1] not in group_let:
                    group_let[k[1]] = [let_num]
                    let_list.append(let_num)
                    print(group_let, let_list, 'a')
                    let_num += 1
                elif k[0] in group_let and k[1] in group_let:
                    if any(ele in group_let[k[0]] for ele in group_let[k[1]]):
                    # if group_let[k[0]] == group_let[k[1]]:
                        group_let[k[1]] = [let_num]
                        # share_let[(k[0], k[1])] = let_num
                        let_num += 1
                        for k1, v1 in share_let.items():
                            if k[0] in k1:
                                if group_pval[(k1[0], k[1])] <= phalpha:
                                    pass
                                elif group_pval[(k1[0], k[1])] > phalpha:
                                    group_let[k1[0]].extend(group_let[k[1]])
                        print(group_let, 'i')
                    else:
                        print(group_let, 'j')
                        pass
                elif k[0] not in group_let and k[1] not in group_let:
                    group_let[k[0]] = [let_num]
                    let_list.append(let_num)
                    let_num += 1
                    group_let[k[1]] = [let_num]
                    let_list.append(let_num)
                    let_num += 1
                    print(group_let, let_list, 'e')
            elif v > phalpha:
                if k[0] not in group_let and k[1] not in group_let:
                    group_let[k[0]] = [let_num]
                    group_let[k[1]] = [let_num]
                    # share_let[let_num] = [k[0], k[1]]
                    share_let[(k[0], k[1])] = let_num
                    let_num += 1
                    print(group_let, 'b')
                elif k[0] in group_let and k[1] not in group_let:
                    group_let[k[1]] = group_let[k[0]]
                    share_let[(k[0], k[1])] = [group_let[k[0]]]
                    print(group_let, 'd')
                elif k[0] in group_let and k[1] in group_let:
                    if any(ele in group_let[k[0]] for ele in group_let[k[1]]):
                        pass
                    elif any(k[0] in ele for ele in share_let):
                        for k1, v1 in share_let.items():
                            # print(k[0], k1)
                            if k[0] in k1:
                                # if group_let[k[1]] not in
                                group_let[k[1]].extend(group_let[k[0]])
                                # group_let[k[1]] = group_let[k[0]]
                                print(group_let, 'cd')
                    else:
                        group_let[k[1]] = group_let[k[0]]
                        share_let[(k[0], k[1])] = group_let[k[0]]
                        print(group_let, 'c')
        '''

        # group_letter_chars = {m: ''.join(list(map(chr, n))) for m, n in group_let.items()}

        self.tukey_summary = pd.DataFrame(tukey_phoc)
        # self.tukey_groups = pd.DataFrame({'': list(group_letter_chars.keys()), 'groups':
        #    list(group_letter_chars.values())})

    def anova_stat(self, df="dataframe", res_var=None, xfac_var=None, phalpha=0.05):
        # x = '{} ~ '
        x = res_var + '~'
        # y = 'C({})'
        z = '+'
        if isinstance(xfac_var, list) and len(xfac_var) > 1:
            for i in range(len(xfac_var)):
                x += 'C({})'.format(xfac_var[i])
                if i < len(xfac_var) - 1:
                    x += z
            model = ols(x, data=df).fit()
        elif isinstance(xfac_var, str):
            # create and run model
            # model = ols('{} ~ C({})'.format(res_var, xfac_var), data=df).fit()
            x += 'C({})'.format(xfac_var)
            model = ols(x, data=df).fit()
        else:
            raise TypeError('xfac_var in anova must be string or list')
        anova_table = sm.stats.anova_lm(model, typ=2)

        # treatments
        # this is for bartlett test
        # levels = df[xfac_var].unique()
        # self.data_summary = stat._data_summary(df, xfac_var, res_var)

        # check assumptions
        # Shapiro-Wilk  data is drawn from normal distribution.
        # w, pvalue1 = stats.shapiro(model.resid)
        # w, pvalue2 = stats.bartlett(*fac_list)
        # if pvalue1 < 0.05:
        #    print("Warning: Data is not drawn from normal distribution")
        # else:
            # samples from populations have equal variances.
        #    if pvalue2 < 0.05:
        #        print("Warning: treatments do not have equal variances")

        self.anova_summary = anova_table

        '''
        if ph:
            # perform multiple pairwise comparison (Tukey HSD)
            m_comp = pairwise_tukeyhsd(endog=df[res], groups=df[xfac], alpha=phalpha)
            print("\nPost-hoc Tukey HSD test\n")
            print(m_comp, "\n")
        '''
        # print("ANOVA Assumption tests\n")
        # print("Shapiro-Wilk (P-value):", pvalue1, "\n")
        # print("Bartlett (P-value):", pvalue2, "\n")

    def lin_reg(self, df="dataframe", y=None, x=None):
        df = df.dropna()
        assert x and y is not None, "Provide proper column names for X and Y variables"
        assert type(x) is list or type(y) is list, "X or Y column names should be list"
        # min data should be 4 or more
        assert df.shape[0] >= 4, "Very few data"
        self.X = df[x].to_numpy()
        self.Y = df[y].to_numpy()
        # number of independent variables
        p = len(x)
        # number of parameter estimates (+1 for intercept and slopes)
        e = p+1
        # number of samples/observations
        n = len(df[y])

        # run regression
        reg_out = LinearRegression().fit(self.X, self.Y)
        # coefficient  of determination
        r_sq = round(reg_out.score(self.X, self.Y), 4)
        # Correlation coefficient (r)
        # Adjusted r-Squared
        r_sq_adj = round(1 - (1 - r_sq) * ((n - 1)/(n-p-1)), 4)
        # RMSE
        # RMSE = standard deviation of the residuals
        rmse = round(np.sqrt(1-r_sq) * np.std(self.Y), 4)
        # intercept and slopes
        reg_intercept = reg_out.intercept_
        reg_slopes = reg_out.coef_
        # predicted values
        self.y_hat = reg_out.predict(self.X)
        # residuals
        self.residuals = self.Y - self.y_hat
        # sum of squares
        regSS = np.sum((self.y_hat - np.mean(self.Y)) ** 2)  # variation explained by linear model
        residual_sse = np.sum((self.Y - self.y_hat) ** 2)  # remaining variation
        sst = np.sum((self.Y - np.mean(self.Y)) ** 2)  # total variation

        eq = ""
        for i in range(p):
            eq = eq+' + '+ '(' + str(round(reg_slopes[0][i], 4))+'*'+x[i] + ')'

        self.reg_eq = str(round(reg_intercept[0], 4)) + eq

        # variance and std error
        # Residual variance = MSE and sqrt of MSE is res stnd error
        sigma_sq_hat = round(residual_sse/(n-e), 4)
        # residual std dev
        res_stdev = round(np.sqrt(sigma_sq_hat))
        # standardized residuals
        self.std_residuals = self.residuals/res_stdev

        # https://stackoverflow.com/questions/22381497/python-scikit-learn-linear-model-parameter-standard-error
        # std error
        X_mat = np.empty(shape=(n, e), dtype=np.float)
        X_mat[:, 0] = 1
        X_mat[:, 1:e] = self.X
        var_hat = np.linalg.inv(X_mat.T @ X_mat) * sigma_sq_hat
        standard_error = []
        for param in range(e):
            standard_error.append(round(np.sqrt(var_hat[param, param]), 4))

        # t = b1 / SE
        params = list(chain(*[["Intercept"], x]))
        estimates = list(chain(*[[reg_intercept[0]], reg_slopes[0]]))
        tabulate_list = []
        for param in range(e):
            tabulate_list.append([params[param], estimates[param], standard_error[param],
                                  estimates[param]/standard_error[param],
                                  '%.4E' % Decimal(stats.t.sf(np.abs(estimates[param]/standard_error[param]), n-e)*2)   ])

        # anova
        anova_table = []
        anova_table.append(["Model", p, regSS, round(regSS/p, 4), round((regSS/p)/(residual_sse/(n-e)), 4),
                            '%.4E' % Decimal(stats.f.sf((regSS/p)/(residual_sse/(n-e)), p, n-e))])
        anova_table.append(["Error", n-e, residual_sse, round(residual_sse/(n-e), 4), "", ""])
        anova_table.append(["Total", n-1, sst, "", "", ""])


        print("\nRegression equation:\n")
        print(self.reg_eq)
        print("\nRegression Summary:")
        print(tabulate([["Dependent variables", x], ["Independent variables", y],
                        ["Coefficient of determination (r-squared)", r_sq], ["Adjusted r-squared", r_sq_adj],
                        ["Root Mean Square Error (RMSE)", rmse],
                        ["Mean of Y", round(np.mean(self.Y), 4)], ["Residual standard error", round(np.sqrt(sigma_sq_hat), 4)],
                        ["No. of Observations", n]], "\n"))
        print("\nRegression Coefficients:\n")
        print(tabulate(tabulate_list, headers=["Parameter", "Estimate", "Std Error", "t-value", "P-value Pr(>|t|)"]), "\n")
        print("\nANOVA Summary:\n")
        print(tabulate(anova_table, headers=["Source", "Df", "Sum Squares", "Mean Squares", "F", "Pr(>F)"]),
              "\n")

        # VIF for MLR
        # VIF computed as regressing X on remaining X
        # using correlation
        if p > 1:
            vif_table = []
            vif_df = df[x]
            df_corr = vif_df.corr()
            vif_mat = np.linalg.inv(df_corr)
            self.vif = vif_mat.diagonal()
            for i in range(len(self.vif)):
                vif_table.append([x[i], self.vif[i]])
            print("\nVariance inflation factor (VIF)\n")
            print(tabulate(vif_table, headers=["Variable", "VIF"]),
                  "\n")

        '''
        vif = []
        for i in range(len(x)):
            temp = x[:]
            print(i, x, temp)
            vif_y = x[i]
            del temp[i]
            vif_x = temp
            y_mat = df[vif_y]
            x_mat = df[vif_x]
            print(y_mat, '\n', x_mat, '\n')
            vif_reg_out = LinearRegression().fit(x_mat, y_mat)
            vif.append(1 / (1-vif_reg_out.score(x_mat, y_mat)))

        print(vif)
        '''

    def ttest(self, df='dataframe', xfac=None, res=None, evar=True, alpha=0.05, test_type=None, mu=None):
        # drop NaN
        df = df.dropna()
        if df.shape[0] < 2:
            raise Exception("Very few observations to run t-test")
        if alpha < 0 or alpha > 1:
            raise Exception("alpha value must be in between 0 and 1")
        if test_type == 1:
            if res and mu is None:
                raise ValueError("res or mu parameter value is missing")
            if res not in df.columns:
                raise ValueError("res column is not in dataframe")
            a_val = df[res].to_numpy()
            res_out = stats.ttest_1samp(a=a_val, popmean=mu, nan_policy='omit')
            sem = df[res].sem()
            if sem == 0:
                print("\nWarning: the data is constant\n")
            ci = (1 - alpha) * 100
            tcritvar = stats.t.ppf((1 + (1 - alpha)) / 2, len(a_val)-1)
            # print results
            self.summary = "\nOne Sample t-test \n" + "\n" + \
                           tabulate([["Sample size", len(a_val)], ["Mean", df[res].mean()], ["t", res_out[0]],
                                     ["Df", len(a_val)-1], ["P-value (one-tail)", res_out[1]/2],
                                     ["P-value (two-tail)", res_out[1]],
                                     ["Lower " + str(ci) + "%", df[res].mean() - (tcritvar * sem)],
                                     ["Upper " + str(ci) + "%", df[res].mean() + (tcritvar * sem)]])
        elif test_type == 2:
            if xfac and res is None:
                raise Exception("xfac or res variable is missing")
            if res not in df.columns or xfac not in df.columns:
                raise ValueError("res or xfac column is not in dataframe")
            levels = df[xfac].unique()
            levels.sort()
            if len(levels) != 2:
                raise Exception("there must be only two levels")
            a_val = df.loc[df[xfac] == levels[0], res].to_numpy()
            b_val = df.loc[df[xfac] == levels[1], res].to_numpy()
            a_count, b_count = len(a_val), len(b_val)
            count = [a_count, b_count]
            mean = [df.loc[df[xfac] == levels[0], res].mean(), df.loc[df[xfac] == levels[1], res].mean()]
            sem = [df.loc[df[xfac] == levels[0], res].sem(), df.loc[df[xfac] == levels[1], res].sem()]
            sd = [df.loc[df[xfac] == levels[0], res].std(), df.loc[df[xfac] == levels[1], res].std()]
            ci = (1-alpha)*100
            # degree of freedom
            # a_count, b_count = np.split(count, 2)
            dfa = a_count - 1
            dfb = b_count - 1
            # sample variance
            with np.errstate(invalid='ignore'):
                var_a = np.nan_to_num(np.var(a_val, ddof=1))
                var_b = np.nan_to_num(np.var(b_val, ddof=1))
            mean_diff = mean[0] - mean[1]
            # variable 95% CI
            varci_low = []
            varci_up = []
            tcritvar = [(stats.t.ppf((1 + (1-alpha)) / 2, dfa)), (stats.t.ppf((1 + (1-alpha)) / 2, dfb))]
            for i in range(len(levels)):
                varci_low.append(mean[i] - (tcritvar[i] * sem[i]))
                varci_up.append(mean[i] + (tcritvar[i] * sem[i]))

            var_test = 'equal'
            # perform levene to check for equal variances
            w, pvalue = stats.levene(a_val, b_val)
            if pvalue < alpha:
                print("\nWarning: the two group variance are not equal. Rerun the test with evar=False\n")

            if evar is True:
                # pooled variance
                message = 'Two sample t-test with equal variance'
                p_var = (dfa * var_a + dfb * var_b) / (dfa + dfb)
                # std error
                se = np.sqrt(p_var * (1.0 / a_count + 1.0 / b_count))
                dfr = dfa + dfb
            else:
                # Welch's t-test for unequal variance
                # calculate se
                message = 'Two sample t-test with unequal variance (Welch\'s t-test)'
                if a_count == 1 or b_count == 1:
                    raise Exception('Not enough observation for either levels. The observations should be > 1 for both levels')
                a_temp = var_a / a_count
                b_temp = var_b / b_count
                dfr = ((a_temp + b_temp) ** 2) / ((a_temp ** 2) / (a_count - 1) + (b_temp ** 2) / (b_count - 1))
                se = np.sqrt(a_temp + b_temp)
                var_test = 'unequal'

            tval = np.divide(mean_diff, se)
            oneside_pval = stats.t.sf(np.abs(tval), dfr)
            twoside_pval = oneside_pval * 2
            # 95% CI for diff
            # 2.306 t critical at 0.05
            tcritdiff = stats.t.ppf((1 + (1-alpha)) / 2, dfr)
            diffci_low = mean_diff - (tcritdiff * se)
            diffci_up = mean_diff + (tcritdiff * se)

            # print results
            self.summary = '\n' + message + '\n\n' + tabulate([["Mean diff", mean_diff], ["t", tval], ["Std Error", se], ["df", dfr],
                                     ["P-value (one-tail)", oneside_pval], ["P-value (two-tail)", twoside_pval],
                                     ["Lower "+str(ci)+"%", diffci_low], ["Upper "+str(ci)+"%", diffci_up]]) + '\n\n' + \
                'Parameter estimates\n\n' + tabulate([[levels[0], count[0], mean[0], sd[0], sem[0], varci_low[0],
                                      varci_up[0]], [levels[1], count[1], mean[1], sd[1], sem[1],
                                                     varci_low[1], varci_up[1]]],
                                    headers=["Level", "Number", "Mean", "Std Dev", "Std Error",
                                             "Lower "+str(ci)+"%", "Upper "+str(ci)+"%"]) + '\n'
            '''
            fig = plt.figure()
            df.boxplot(column=res, by=xfac, grid=False)
            plt.ylabel(res)
            plt.savefig('ttsam_boxplot.png', format='png', bbox_inches='tight', dpi=300)
            '''
        elif test_type == 3:
            if not isinstance(res, (tuple, list)) and len(res) != 2:
                raise Exception("res should be either list of tuple of length 2")
            if sorted(res) != sorted(df.columns):
                raise ValueError("one or all of res columns are not in dataframe")
            df = df.drop(['diff_betw_res'], axis=1, errors='ignore')
            df['diff_betw_res'] = df[res[0]]-df[res[1]]
            a_val = df['diff_betw_res'].to_numpy()
            res_out = stats.ttest_1samp(a=a_val, popmean=0, nan_policy='omit')
            sem = df['diff_betw_res'].sem()
            ci = (1 - alpha) * 100
            tcritvar = stats.t.ppf((1 + (1 - alpha)) / 2, len(a_val)-1)
            # print results
            self.summary = "\nPaired t-test \n" + "\n" + \
                           tabulate([["Sample size", len(a_val)], ["Difference Mean", df['diff_betw_res'].mean()], ["t", res_out[0]],
                                     ["Df", len(a_val)-1], ["P-value (one-tail)", res_out[1]/2],
                                     ["P-value (two-tail)", res_out[1]],
                                     ["Lower " + str(ci) + "%", df['diff_betw_res'].mean() - (tcritvar * sem)],
                                     ["Upper " + str(ci) + "%", df['diff_betw_res'].mean() + (tcritvar * sem)]])
        else:
            raise ValueError("Provide a value to test_type parameter for appropriate t-test")

    def chisq(self, df='dataframe', p=None):
        # d = pd.read_csv(table, index_col=0)
        tabulate_list = []
        if all(i < 0 for i in df.values.flatten()):
            raise ValueError("The observation counts for each group must be non-negative number")
        if p is None:
            # assert df.shape[1] == 2, 'dataframe must 2-dimensional contingency table of observed counts'
            chi_ps, p_ps, dof_ps, expctd_ps = stats.chi2_contingency(df.to_dict('split')['data'])
            tabulate_list.append(["Pearson", dof_ps, chi_ps, p_ps])
            chi_ll, p_ll, dof_ll, expctd_ll = stats.chi2_contingency(df.to_dict('split')['data'], lambda_="log-likelihood")
            tabulate_list.append(["Log-likelihood", dof_ll, chi_ll, p_ll])

            mosaic_dict = dict()
            m = df.to_dict('split')

            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    mosaic_dict[(m['index'][i], m['columns'][j])] = m['data'][i][j]

            # print("\nChi-squared test\n")
            # print(tabulate(tabulate_list, headers=["Test", "Df", "Chi-square", "P-value"]))
            self.summary = '\nChi-squared test for independence\n' + '\n' + \
                           tabulate(tabulate_list, headers=["Test", "Df", "Chi-square", "P-value"]) + '\n'

            # print("\nExpected frequency counts\n")
            # print(tabulate(expctd_ps, headers=df.to_dict('split')['columns'], showindex="always"))
            self.expected_df = '\nExpected frequency counts\n' + '\n' + \
                               tabulate(expctd_ps, headers=df.to_dict('split')['columns'], showindex="always") + '\n'

            # labels = lambda k: "" if mosaic_dict[k] != 0 else ""
            # mosaic(mosaic_dict, labelizer=labels)
            # plt.savefig('mosaic.png', format='png', bbox_inches='tight', dpi=300)

        # goodness of fit test
        if p:
            df = df.drop(['expected_counts'], axis=1, errors='ignore')
            assert df.shape[1] == 1, 'dataframe must one-dimensional contingency table of observed counts'
            assert len(p) == df.shape[0], 'probability values should be equal to observations'
            assert isinstance(p, (tuple, list)) and round(sum(p), 10) == 1, 'probabilities must be list or tuple and ' \
                                                                            'sum to 1'
            df['expected_counts'] = [df.sum()[0] * i for i in p]
            if (df['expected_counts'] < 5).any():
                print('Warning: Chi-squared may not be valid as some of expected counts are < 5')
            if all(i < 0 for i in p):
                raise ValueError("The probabilities for each group must be non-negative number")
            dof = df.shape[0] - 1
            chi_gf, p_gf = stats.chisquare(f_obs=df[df.columns[0]].to_numpy(), f_exp=df[df.columns[1]].to_numpy())
            tabulate_list.append([chi_gf, dof, p_gf, df[df.columns[0]].sum()])
            # print('\nChi-squared goodness of fit test\n')
            # print(tabulate(tabulate_list, headers=["Chi-Square", "Df", "P-value", "Sample size"]), '\n')
            self.summary = '\nChi-squared goodness of fit test\n' + '\n' + \
                           tabulate(tabulate_list, headers=["Chi-Square", "Df", "P-value", "Sample size"]) + '\n'
            self.expected_df = df


class gff:
    def __init__(self):
        pass

    def gff_to_gtf(file='gff_file', mrna_feature_name=None):
        read_gff_file_cds = open(file, 'r')
        cds_dict_st, cds_dict_st_phase  = dict(), dict()
        cds_dict_end, cds_dict_end_phase = dict(), dict()
        cds_ct = 0

        for line in read_gff_file_cds:
            if not line.startswith('#'):
                line = re.split('\s+', line.strip())
                if line[2] == 'mRNA' or line[2] == 'transcript' or line[2] == mrna_feature_name:
                    # attr = re.split(';', line[8])
                    # transcript_id = attr[0].split('=')[1]
                    if 'ID=' in line[8]:
                        transcript_id = re.search('ID=(.+?)(;|$)', line[8]).group(1)
                    else:
                        raise Exception(
                                "ID required in GFF3 file in attribute field for mRNA/transcript"
                                " feature type")
                    cds_dict_st[transcript_id] = []
                    cds_dict_end[transcript_id] = []
                elif line[2] == 'CDS':
                    if 'Parent=' in line[8]:
                        transcript_id_cds = re.search('Parent=(.+?)(;|$)', line[8]).group(1)
                    else:
                        raise Exception(
                            "Parent field required in GFF3 file in attribute field for CDS"
                            " feature type")
                    cds_ct += 1
                    cds_dict_st[transcript_id_cds].append(line[3])
                    cds_dict_end[transcript_id_cds].append(line[4])
                    cds_dict_st_phase[(transcript_id_cds, line[3])] = line[7]
                    cds_dict_end_phase[(transcript_id_cds, line[4])] = line[7]

        read_gff_file_cds.close()

        # check if CDS feature present in GFF3 file
        if cds_ct == 0:
            print ("Warning: No CDS feature type found in given GFF3 file. GTF file requires CDS feature type\n")
        read_gff_file = open(file, 'r')
        out_gtf_file = open(Path(file).stem+'.gtf', 'w')
        gene_id = ''
        transcript_id = ''
        gene_name = ''
        first_cds_present, last_cds_present, start_codon_present, end_codon_present = 0, 0, 0, 0
        gene_trn = dict()
        ttr_i, cds_i, exon_i, ftr_i = dict(), dict(), dict(), dict()

        for line in read_gff_file:
            if not line.startswith('#'):
                line = re.split('\s+', line.strip())
                if line[2] == 'gene':
                    # attr = re.split(';', line[8])
                    if 'ID=' in line[8]:
                        gene_id = re.search('ID=(.+?)(;|$)',  line[8]).group(1)

                    if 'Name=' in line[8]:
                        gene_name = re.search('Name=(.+?)(;|$)',  line[8]).group(1)
                    elif 'gene_name=' in line[8]:
                        gene_name = re.search('gene_name=(.+?)(;|$)',  line[8]).group(1)
                    elif 'gene_id=' in line[8]:
                        gene_name = re.search('gene_id=(.+?)(;|$)',  line[8]).group(1)

                    if 'ID=' not in line[8]:
                        raise Exception("ID field required in GFF3 file in attribute field for gene feature type")

                    gene_trn[gene_id] = []
                    # gene_id = attr[0].split('=')[1]
                    # gene_attr_gtf = 'gene_id "'+gene_id+'"; gene_name "'+attr[1].split('=')[1]+'"; gene_source "'+\
                    #                line[1]+'";'
                    gene_attr_gtf = 'gene_id "' + gene_id + '"; gene_name "' + gene_name + '"; gene_source "' + line[1]+'";'
                    out_gtf_file.write('\t'.join(line[0:8])+'\t'+gene_attr_gtf+'\n')
                elif line[2] == 'mRNA' or line[2] == 'transcript' or line[2] == mrna_feature_name:
                    # cds_i, exon_i, ftr_i, ttr_i = 1, 1, 1, 1
                    exon_i_int, cds_i_int, ftr_i_int, ttr_i_int = 0, 0, 0, 0
                    if 'ID=' in line[8]:
                        transcript_id = re.search('ID=(.+?)(;|$)', line[8]).group(1)
                    # if 'Parent=' in line[8]:
                    #    gene_id = re.search('Parent=(.*);', line[8]).group(1)

                    if 'ID=' not in line[8]:
                        raise Exception("ID field required in GFF3 file in attribute field for mRNA/transcript"
                                        " feature type")

                    # transcript_id = attr[0].split('=')[1]
                    # replace mRNA with transcript for gtf file
                    if line[2] == 'mRNA' or line[2] == mrna_feature_name:
                        line[2] = 'transcript'

                    gene_trn[gene_id].append(transcript_id)
                    ttr_i[transcript_id] = 0
                    cds_i[transcript_id] = 0
                    exon_i[transcript_id] = 0
                    ftr_i[transcript_id] = 0

                    gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id + \
                                    '"; gene_source "' + line[1] + '";'
                    out_gtf_file.write('\t'.join(line[0:8])+'\t'+gene_attr_gtf+'\n')
                elif line[2] == 'CDS':
                    # attr = re.split(';', line[8])
                    if 'Parent=' in line[8]:
                        transcript_id_temp = re.search('Parent=(.+?)(;|$)', line[8]).group(1)

                    if 'Parent=' not in line[8]:
                        raise Exception(
                            "Parent field required in GFF3 file in attribute field for CDS"
                            " feature type")

                    if line[3] == min(cds_dict_st[transcript_id_temp], key=int):
                        first_cds_present = 1
                    if line[4] == max(cds_dict_end[transcript_id_temp], key=int):
                        last_cds_present = 1

                    if transcript_id_temp in gene_trn[gene_id]:
                        cds_i[transcript_id_temp] += 1
                        gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id_temp + \
                                        '"; cds_number "' + str(cds_i[transcript_id_temp]) + '"; gene_name "' + \
                                        gene_name + '"; gene_source "' + line[1] + '";'
                    # for transcripts with shared CDS
                    elif ',' in transcript_id_temp:
                        gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id_temp + \
                                        '"; cds_number "' + '""' + '"; gene_name "' + \
                                        gene_name + '"; gene_source "' + line[1] + '";'
                        # cds_i += 1

                    out_gtf_file.write('\t'.join(line[0:8])+'\t'+gene_attr_gtf+'\n')
                elif line[2] == 'exon':
                    if 'Parent=' in line[8]:
                        transcript_id_temp = re.search('Parent=(.+?)(;|$)', line[8]).group(1)

                    if 'Parent=' not in line[8]:
                        raise Exception(
                            "Parent field required in GFF3 file in attribute field for exon"
                            " feature type")

                    if transcript_id_temp in gene_trn[gene_id]:
                        exon_i[transcript_id_temp] += 1
                        gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id_temp + \
                                        '"; exon_number "' + str(exon_i[transcript_id_temp]) + '"; gene_name "' + \
                                        gene_name + '"; gene_source "' + line[1] + '";'
                    # for transcripts with shared exons
                    elif ',' in transcript_id_temp:
                        gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id_temp + \
                                        '"; exon_number "' + '""' + '"; gene_name "' + gene_name + \
                                        '"; gene_source "' + line[1] + '";'

                    out_gtf_file.write('\t'.join(line[0:8])+'\t'+gene_attr_gtf+'\n')
                elif line[2] == 'five_prime_UTR':
                    if 'Parent=' in line[8]:
                        transcript_id_temp = re.search('Parent=(.+?)(;|$)', line[8]).group(1)

                    if 'Parent=' not in line[8]:
                        raise Exception(
                            "Parent field required in GFF3 file in attribute field for five_prime_UTR"
                            " feature type")

                    if transcript_id_temp in gene_trn[gene_id]:
                        ftr_i[transcript_id_temp] += 1
                        gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id_temp + \
                                        '"; five_prime_UTR_number "' + str(ftr_i[transcript_id_temp]) + \
                                        '"; gene_name "'+ gene_name + '"; gene_source "' + line[1] + '";'
                    # for transcripts with shared five_prime_UTR
                    elif ',' in transcript_id_temp:
                        gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id_temp + \
                                        '"; three_prime_UTR_number "' + '""' + \
                                        '"; gene_name "' + gene_name + '"; gene_source "' + line[1] + '";'

                    out_gtf_file.write('\t'.join(line[0:8])+'\t'+gene_attr_gtf+'\n')
                elif line[2] == 'three_prime_UTR':
                    if 'Parent=' in line[8]:
                        transcript_id_temp = re.search('Parent=(.+?)(;|$)', line[8]).group(1)

                    if 'Parent=' not in line[8]:
                        raise Exception(
                            "Parent field required in GFF3 file in attribute field for three_prime_UTR"
                            " feature type")

                    if transcript_id_temp in gene_trn[gene_id]:
                        ttr_i[transcript_id_temp] += 1
                        gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id_temp + \
                                        '"; three_prime_UTR_number "' + str(ttr_i[transcript_id_temp]) + \
                                        '"; gene_name "' + gene_name + '"; gene_source "' + line[1] + '";'
                    # for transcripts with shared three_prime_UTR
                    elif ',' in transcript_id_temp:
                        gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id_temp + \
                                        '"; three_prime_UTR_number "' + "" + '"; gene_name "' + \
                                        gene_name + '"; gene_source "' + line[1] + '";'

                    out_gtf_file.write('\t'.join(line[0:8])+'\t'+gene_attr_gtf+'\n')
                elif line[2] == 'start_codon':
                    start_codon_present = 1
                    if 'Parent=' in line[8]:
                        transcript_id_temp = re.search('Parent=(.+?)(;|$)', line[8]).group(1)

                    if 'Parent=' not in line[8]:
                        raise Exception(
                            "Parent field required in GFF3 file in attribute field for three_prime_UTR"
                            " feature type")
                    if transcript_id_temp == transcript_id:
                        gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id + '"; gene_name "' + \
                                            gene_name+ '"; gene_source "' + line[1] + '";'
                    out_gtf_file.write('\t'.join(line[0:8])+'\t'+gene_attr_gtf+'\n')
                elif line[2] == 'stop_codon':
                    end_codon_present = 1
                    if 'Parent=' in line[8]:
                        transcript_id_temp = re.search('Parent=(.+?)(;|$)', line[8]).group(1)

                    if 'Parent=' not in line[8]:
                        raise Exception(
                            "Parent field required in GFF3 file in attribute field for three_prime_UTR"
                            " feature type")
                    if transcript_id_temp == transcript_id:
                        gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id + '"; gene_name "' + \
                                            gene_name+ '"; gene_source "' + line[1] + '";'
                    out_gtf_file.write('\t'.join(line[0:8])+'\t'+gene_attr_gtf+'\n')

                if first_cds_present == 1 and start_codon_present == 0:
                    first_cds_present = 0
                    if 'Parent=' in line[8]:
                        transcript_id_temp = re.search('Parent=(.+?)(;|$)', line[8]).group(1)

                    if 'Parent=' not in line[8]:
                        raise Exception(
                            "Parent field required in GFF3 file in attribute field for CDS"
                            " feature type")

                    for k in gene_trn[gene_id]:
                        if k == transcript_id_temp:
                            if line[6] == '+':
                                codon_min_cord = int(min(cds_dict_st[transcript_id_temp], key=int))
                                cds_phase = int(
                                    cds_dict_st_phase[
                                        (transcript_id_temp, min(cds_dict_st[transcript_id_temp], key=int))])
                                line[2], line[3], line[4] = 'start_codon', codon_min_cord + cds_phase, \
                                                            codon_min_cord + cds_phase + 2
                            elif line[6] == '-':
                                codon_max_cord = int(max(cds_dict_end[transcript_id_temp], key=int))
                                cds_phase = int(
                                    cds_dict_end_phase[
                                        (transcript_id_temp, max(cds_dict_end[transcript_id_temp], key=int))])
                                line[2], line[3], line[4] = 'start_codon', codon_max_cord - 2 - cds_phase, \
                                                            codon_max_cord - cds_phase
                            gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id_temp + '"; gene_name "' + \
                                            gene_name + '"; gene_source "' + line[1] + '";'
                            out_gtf_file.write('\t'.join(str(x) for x in line[0:8]) + '\t' + gene_attr_gtf + '\n')

                        '''
                        if transcript_id in gene_trn[k] or gene_id_temp == k:
                            print(transcript_id, 'e')
                            if line[6] == '+':
                                codon_min_cord = int(min(cds_dict_st[transcript_id_temp], key=int))
                                cds_phase = int(
                                    cds_dict_st_phase[(transcript_id_temp, min(cds_dict_st[transcript_id_temp], key=int))])
                                line[2], line[3], line[4] = 'start_codon', codon_min_cord + cds_phase, \
                                                        codon_min_cord + cds_phase + 2
                            elif line[6] == '-':
                                codon_max_cord = int(max(cds_dict_end[transcript_id_temp], key=int))
                                cds_phase = int(
                                    cds_dict_end_phase[(transcript_id_temp, max(cds_dict_end[transcript_id_temp], key=int))])
                                line[2], line[3], line[4] = 'start_codon', codon_max_cord - 2 - cds_phase, \
                                                        codon_max_cord - cds_phase
                            gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id + '"; gene_name "' + \
                                            gene_name + '"; gene_source "' + line[1] + '";'
                            out_gtf_file.write('\t'.join(str(x) for x in line[0:8]) + '\t' + gene_attr_gtf + '\n')
                        '''
                if last_cds_present == 1 and end_codon_present == 0:
                    last_cds_present = 0
                    if 'Parent=' in line[8]:
                        transcript_id_temp = re.search('Parent=(.+?)(;|$)', line[8]).group(1)

                    if 'Parent=' not in line[8]:
                        raise Exception(
                            "Parent field required in GFF3 file in attribute field for CDS"
                            " feature type")

                    for k in gene_trn[gene_id]:
                        if k == transcript_id_temp:
                            if line[6] == '+':
                                codon_max_cord = int(max(cds_dict_end[transcript_id_temp], key=int))
                                line[2], line[3], line[4] = 'stop_codon', codon_max_cord - 2, codon_max_cord
                            elif line[6] == '-':
                                codon_min_cord = int(min(cds_dict_st[transcript_id_temp], key=int))
                                line[2], line[3], line[4] = 'stop_codon', codon_min_cord, codon_min_cord + 2
                            gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id_temp + \
                                            '"; gene_name "' + gene_name + '"; gene_source "' + line[1] + '";'
                            out_gtf_file.write('\t'.join(str(x) for x in line[0:8]) + '\t' + gene_attr_gtf + '\n')
                    '''
                    if transcript_id_temp == transcript_id or gene_id_temp == gene_id:
                        if line[6] == '+':
                            codon_max_cord = int(max(cds_dict_end[transcript_id_temp], key=int))
                            cds_phase = int(cds_dict_end_phase[(transcript_id_temp, max(cds_dict_end[transcript_id_temp], key=int))])
                            line[2], line[3], line[4] = 'stop_codon', codon_max_cord - 2, codon_max_cord
                        elif line[6] == '-':
                            codon_min_cord = int(min(cds_dict_st[transcript_id_temp], key=int))
                            cds_phase = int(cds_dict_st_phase[(transcript_id_temp, max(cds_dict_st[transcript_id_temp], key=int))])
                            line[2], line[3], line[4] = 'stop_codon', codon_min_cord, codon_min_cord + 2
                        gene_attr_gtf = 'gene_id "' + gene_id + '"; transcript_id "' + transcript_id + '"; gene_name "' + \
                                            gene_name + '"; gene_source "' + line[1] + '";'
                        out_gtf_file.write('\t'.join(str(x) for x in line[0:8]) + '\t' + gene_attr_gtf + '\n')
                    '''
        read_gff_file.close()
        out_gtf_file.close()

    def gffreader(file='gff_file'):
        read_gff_file = open(file, 'r')
        transcript_id = ''
        for line in read_gff_file:
            if not line.startswith('#'):
                line = re.split('\t', line.strip())
                if line[2]=='gene':
                    if 'ID=' in line[8]:
                        gene_id = re.search('ID=(.+?)(;|$)',  line[8]).group(1)

                    if 'Name=' in line[8]:
                        gene_name = re.search('Name=(.+?)(;|$)',  line[8]).group(1)
                    elif 'gene_name=' in line[8]:
                        gene_name = re.search('gene_name=(.+?)(;|$)',  line[8]).group(1)
                    elif 'gene_id=' in line[8]:
                        gene_name = re.search('gene_id=(.+?)(;|$)',  line[8]).group(1)

                    if 'ID=' not in line[8]:
                        raise Exception("ID field required in GFF3 file in attribute field for gene feature type")
                    yield (line[0], gene_id, gene_name, transcript_id, line[1], line[2], line[3], line[4], line[6], line[8])
                elif line[2] == 'mRNA' or line[2] == 'transcript':
                    if 'ID=' in line[8]:
                        transcript_id = re.search('ID=(.+?)(;|$)', line[8]).group(1)
                    else:
                        raise Exception("ID field required in GFF3 file in attribute field for mRNA/transcript"
                                        " feature type")
                    yield (line[0], gene_id, gene_name, transcript_id, line[1], line[2], line[3], line[4], line[6], line[8])
                elif line[2]=='CDS':
                    if 'Parent=' in line[8]:
                        transcript_id_temp = re.search('Parent=(.+?)(;|$)', line[8]).group(1)
                    else:
                        raise Exception(
                            "Parent field required in GFF3 file in attribute field for CDS"
                            " feature type")
                    if transcript_id_temp == transcript_id:
                        yield (line[0], gene_id, gene_name, transcript_id, line[1], line[2], line[3], line[4], line[6], line[8])
                elif line[2]=='exon':
                    if 'Parent=' in line[8]:
                        transcript_id_temp = re.search('Parent=(.+?)(;|$)', line[8]).group(1)
                    else:
                        raise Exception(
                            "Parent field required in GFF3 file in attribute field for exon"
                            " feature type")
                    if transcript_id_temp == transcript_id:
                        yield (line[0], gene_id, gene_name, transcript_id, line[1], line[2], line[3], line[4], line[6], line[8])
                elif line[2]=='five_prime_UTR':
                    if 'Parent=' in line[8]:
                        transcript_id_temp = re.search('Parent=(.+?)(;|$)', line[8]).group(1)
                    else:
                        raise Exception(
                            "Parent field required in GFF3 file in attribute field for five_prime_UTR"
                            " feature type")
                    if transcript_id_temp == transcript_id:
                        yield (line[0], gene_id, gene_name, transcript_id, line[1], line[2], line[3], line[4], line[6], line[8])
                elif line[2]=='three_prime_UTR':
                    if 'Parent=' in line[8]:
                        transcript_id_temp = re.search('Parent=(.+?)(;|$)', line[8]).group(1)
                    else:
                        raise Exception(
                            "Parent field required in GFF3 file in attribute field for three_prime_UTR"
                            " feature type")
                    if transcript_id_temp == transcript_id:
                        yield (line[0], gene_id, gene_name, transcript_id, line[1], line[2], line[3], line[4], line[6], line[8])
                elif line[2]=='start_codon':
                    if 'Parent=' in line[8]:
                        transcript_id_temp = re.search('Parent=(.+?)(;|$)', line[8]).group(1)
                    else:
                        raise Exception(
                            "Parent field required in GFF3 file in attribute field for three_prime_UTR"
                            " feature type")
                    if transcript_id_temp == transcript_id:
                        yield (line[0], gene_id, gene_name, transcript_id, line[1], line[2], line[3], line[4], line[6], line[8])

                elif line[2]=='stop_codon':
                    if 'Parent=' in line[8]:
                        transcript_id_temp = re.search('Parent=(.+?)(;|$)', line[8]).group(1)
                    else:
                        raise Exception(
                            "Parent field required in GFF3 file in attribute field for three_prime_UTR"
                            " feature type")
                    if transcript_id_temp == transcript_id:
                        yield (line[0], gene_id, gene_name, transcript_id, line[1], line[2], line[3], line[4], line[6], line[8])
        read_gff_file.close()


class norm:
    def __init__(self):
        pass

    def cpm(self, df='dataframe'):
        df = df.dropna()
        # check for non-numeric values
        for i in df.columns:
            assert general.check_for_nonnumeric(df[i]) == 0, \
                'dataframe contains non-numeric values in {} column'.format(i)
        self.lib_size = df.sum()
        self.cpm_norm = (df * 1e6) / df.sum()

    def rpkm(self, df='dataframe', gl=None):
        df = df.dropna()
        assert gl is not None, "Provide column name for gene length in bp"
        # check for non-numeric values
        for i in df.columns:
            assert general.check_for_nonnumeric(df[i]) == 0, \
                'dataframe contains non-numeric values in {} column'.format(i)
        self.rpkm_norm = (df.div(df[gl], axis=0) * 1e9) / df.sum()
        self.rpkm_norm = self.rpkm_norm.drop([gl], axis=1)

    def tpm(self, df='dataframe', gl=None):
        df = df.dropna()
        assert gl is not None, "Provide column name for gene length in bp"
        # check for non-numeric values
        for i in df.columns:
            assert general.check_for_nonnumeric(df[i]) == 0, \
                'dataframe contains non-numeric values in {} column'.format(i)
        # gene length must be in bp
        self.a = df.div(df[gl], axis=0) * 1e3
        self.tpm_norm = (self.a * 1e6) / self.a.sum()
        self.tpm_norm = self.tpm_norm.drop([gl], axis=1)


class assembly:
    def sizdist(self, file='fasta', n=50):
        fasta_iter = fasta.fasta_reader(file)
        seq_len = []
        total_len_sum = 0
        for record in fasta_iter:
            header, sequence = record
            seq_len.append(len(sequence))
            total_len_sum += len(sequence)
        seq_len.sort(reverse=True)


class lncrna:
    def lincrna_types(gff_file='gff_file_with_lincrna', map_factor=200):
        read_gff_file = open(gff_file, 'r')
        out_file = open('same_conv_out.txt', 'w')
        out_file_2 = open('dive_out.txt', 'w')
        out_file_3 = open('lincrna_types.txt', 'w')
        transcript_id = ''
        lincrna_dict = dict()
        mrna_dict = dict()
        lincrna_dict_1 = dict()
        mrna_dict_1 = dict()
        line_num = 0
        for line in read_gff_file:
            if not line.startswith('#'):
                line = re.split('\t', line.strip())
                line_num += 1
                line.extend([line_num])
                if line[1] == 'Evolinc':
                    lincrna_trn_id = re.search('transcript_id (.+?)(;|$)', line[8]).group(1)
                    lincrna_dict[(line[0], int(line[3]), int(line[4]), line[6], line[9])] = lincrna_trn_id.strip('"')
                    lincrna_dict_1[line_num] = [line[0], int(line[3]), int(line[4]), line[6], line[9], lincrna_trn_id.strip('"')]

                if line[2] == 'mRNA':
                    mrna_id = re.search('gene_id (.+?)(;|$)', line[8]).group(1)
                    mrna_dict[(line[0], int(line[3]), int(line[4]), line[6], line[9])] = mrna_id.strip('"')
                    mrna_dict_1[line_num] = [line[0], int(line[3]), int(line[4]), line[6], line[9],
                                                mrna_id.strip('"')]

        read_gff_file.close()

        checked = dict()
        checked_2 = dict()

        # for same and convergent
        for k in lincrna_dict_1:
            if lincrna_dict_1[k][3] == '+':
                k1 = k
                for i in range(map_factor):
                    if k1 in mrna_dict_1:
                        linc_st = lincrna_dict_1[k][1]
                        mrna_st = mrna_dict_1[k1][1]
                        diff = mrna_st - linc_st + 1
                        mrna_id = mrna_dict_1[k1][5]
                        if 'PGSC' in mrna_dict_1[k1][5] and mrna_dict_1[k1][3] == '+' and lincrna_dict_1[k][5] not in \
                                checked and mrna_dict_1[k1][0] == lincrna_dict_1[k][0]:
                            checked[lincrna_dict_1[k][5]] = [diff, mrna_id, 'same']
                            out_file.write(lincrna_dict_1[k][5]+'\t'+mrna_dict_1[k1][5]+'\t'+str(diff)+'\t'+'same'+'\n')
                        elif 'PGSC' in mrna_dict_1[k1][5] and mrna_dict_1[k1][3] == '-' and lincrna_dict_1[k][5] not \
                                in checked and mrna_dict_1[k1][0] == lincrna_dict_1[k][0]:
                            checked[lincrna_dict_1[k][5]] = [diff, mrna_id, 'convergent']
                            out_file.write(lincrna_dict_1[k][5]+'\t'+mrna_dict_1[k1][5]+'\t'+str(diff)+'\t'+'convergent'+'\n')
                    else:
                        k1 += 1
            elif lincrna_dict_1[k][3] == '-':
                k1 = k
                for i in range(map_factor):
                    if k1 in mrna_dict_1:
                        linc_st = lincrna_dict_1[k][1]
                        mrna_st = mrna_dict_1[k1][1]
                        diff = linc_st - mrna_st + 1
                        mrna_id = mrna_dict_1[k1][5]
                        if 'PGSC' in mrna_dict_1[k1][5] and mrna_dict_1[k1][3] == '-' and lincrna_dict_1[k][
                            5] not in checked and mrna_dict_1[k1][0] == lincrna_dict_1[k][0]:
                            checked[lincrna_dict_1[k][5]] = [diff, mrna_id, 'same']
                            out_file.write(lincrna_dict_1[k][5]+'\t'+mrna_dict_1[k1][5]+'\t'+str(diff)+'\t'+'same'+'\n')
                        elif 'PGSC' in mrna_dict_1[k1][5] and mrna_dict_1[k1][3] == '+' and lincrna_dict_1[k][
                            5] not in checked and mrna_dict_1[k1][0] == lincrna_dict_1[k][0]:
                            checked[lincrna_dict_1[k][5]] = [diff, mrna_id, 'convergent']
                            out_file.write(lincrna_dict_1[k][5]+'\t'+mrna_dict_1[k1][5]+'\t'+str(diff)+'\t'+'convergent'+'\n')
                    else:
                        k1 -= 1

        # for divergent only
        for k in lincrna_dict_1:
            if lincrna_dict_1[k][3] == '+':
                k1 = k
                for i in range(map_factor):
                    if k1 in mrna_dict_1:
                        linc_st = lincrna_dict_1[k][1]
                        mrna_st = mrna_dict_1[k1][1]
                        diff = linc_st - mrna_st + 1
                        mrna_id = mrna_dict_1[k1][5]
                        if 'PGSC' in mrna_dict_1[k1][5] and mrna_dict_1[k1][3] == '-' and lincrna_dict_1[k][5] not in \
                                checked_2 and mrna_dict_1[k1][0] == lincrna_dict_1[k][0]:
                            checked_2[lincrna_dict_1[k][5]] = [diff, mrna_id, 'divergent']
                            out_file_2.write(lincrna_dict_1[k][5]+'\t'+mrna_dict_1[k1][5]+'\t'+str(diff)+'\t'+'divergent'+'\n')
                    else:
                        k1 -= 1
            elif lincrna_dict_1[k][3] == '-':
                k1 = k
                for i in range(map_factor):
                    if k1 in mrna_dict_1:
                        linc_st = lincrna_dict_1[k][1]
                        mrna_st = mrna_dict_1[k1][1]
                        diff = mrna_st - linc_st + 1
                        mrna_id = mrna_dict_1[k1][5]
                        if 'PGSC' in mrna_dict_1[k1][5] and mrna_dict_1[k1][3] == '+' and lincrna_dict_1[k][
                            5] not in checked_2 and mrna_dict_1[k1][0] == lincrna_dict_1[k][0]:
                            checked_2[lincrna_dict_1[k][5]] = [diff, mrna_id, 'divergent']
                            out_file_2.write(lincrna_dict_1[k][5]+'\t'+mrna_dict_1[k1][5]+'\t'+str(diff)+'\t'+'divergent'+'\n')
                    else:
                        k1 += 1

        for k in lincrna_dict_1:
            if lincrna_dict_1[k][5] not in checked:
                print(lincrna_dict_1[k][5])

        for k in checked:
            x = 0
            for k1 in checked_2:
                if k == k1 and checked[k][2] == 'same':
                    x = 1
                    out_file_3.write(k + '\t' + checked[k][1] + '\t' + checked[k][2] + '\t' + str(checked[k][0]) + '\n')
                elif k == k1 and checked[k][2] == 'convergent' and checked_2[k][2] == 'divergent':
                    if checked[k][0] <= checked_2[k][0]:
                        x = 1
                        out_file_3.write(k + '\t' + checked[k][1] + '\t' + checked[k][2] + '\t' + str(checked[k][0]) + '\n')
                    else:
                        x = 1
                        out_file_3.write(
                            k + '\t' + checked_2[k1][1] + '\t' + checked_2[k1][2] + '\t' + str(checked_2[k1][0]) + '\n')
            if x == 0:
                out_file_3.write(k + '\t' + checked[k][1] + '\t' + checked[k][2] + '\t' + str(checked[k][0]) + '\n')


class get_data:
    def __init__(self, data=None):
        if data=='mlr':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/reg/test_reg.csv")
        elif data=='boston':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/reg/boston.csv")
        elif data=='volcano':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/volcano/testvolcano.csv")
        elif data=='ma':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/ma/ma.csv")
        elif data=='hmap':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/heatmap/hm_cot.csv")
        elif data=='mhat':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/mhat/gwas_res_sim.csv")
        elif data=='bdot':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/bardot/bardot.txt", sep="\t")
        elif data=='corr':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/corr/corr_dataset.csv")
        elif data=='slr':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/reg/test_reg_uni.csv")
        elif data=='t_ind_samp':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/ttest/genotype.csv")
        elif data=='gexp':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/pca/cot_pca.csv")
        elif data=='iris':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/pca/iris.csv")
        elif data=='digits':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/tsne/digits.csv")
        elif data=='pbmc':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/tsne/pbmc_seurat_processes.csv")
        elif data=='ath_root':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/tsne/ath_root_sub_seurat_processes.csv")
        elif data=='sc_exp':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/gexp/df_sc.csv")
        elif data=='drugdata':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/chisq/drugdata.csv")
        elif data=='t_one_samp':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/ttest/t_one_samp.csv")
        elif data=='t_pair':
            self.data = pd.read_csv("https://reneshbedre.github.io/assets/posts/ttest/t_pair.csv")
        else:
            print("Error: Provide correct parameter for data\n")



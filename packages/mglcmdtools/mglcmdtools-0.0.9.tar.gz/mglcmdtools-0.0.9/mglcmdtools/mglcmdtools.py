#!/usr/bin/env python3
import subprocess
import sys
import os
import time
import re
import pandas as pd
from Bio import Seq
from itertools import product
from random import randint
import numpy as np
import collections
import logging


def rm_and_mkdir(directory, force=False):
    '''
    create the `directory`.

    If it already exists, when `force=True`, will forcely delete the `directory` and recreate it, otherwise, do nothing and return `None`.

    '''

    if os.path.exists(directory):
        if force:
            cmd = 'rm -rf {0}'.format(directory)
            subprocess.check_output(cmd, shell=True)
        else:
            print(directory, 'already exists!', file=sys.stderr)
            return None

    os.mkdir(directory)

    return directory


def runcmd(command, verbose=False):
    '''
    Run `command`. if `verbose`, print time, and command content to stdout.

    '''
    try:
        if verbose:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.localtime(time.time()))
            print(current_time, "\n", command, "\n", sep="", flush=True)
        subprocess.check_output(command, shell=True)

    except Exception as e:
        print(e, file=sys.stderr)
        raise RuntimeError(
            "Error occured when running command:\n{0}".format(command))

    return command


def longStrings_not_match_shortStrings(Long_strings, Short_strings, reverse=False):
    '''
    Long_strings: the long element list, e.g., ['AABB', 'CCDD', 'EEFF']
    Short_strings: the short element list, e.g., ['AA', 'EE']

    Excluding the elements of Long_strings whose substring is element of Short_strings.

    In the example above, the return is ['CCDD'].

    If reverse=True, the return will be ['AABB', 'EEFF'].

    Return: A list if the result contains one or more elements, or None if no element found.
    '''

    res = []
    for long_string in Long_strings:
        in_SS = any(
            short_string in long_string for short_string in Short_strings)
        if not in_SS and not reverse:
            res.append(long_string)
        elif in_SS and reverse:
            res.append(long_string)

    if len(res) == 0:
        return False

    return res


def read_fastaLike(file, startswith='>', maxrecords=-1):
    '''
    Every time return one record using the 'yield' function,
    the return record is a list, containing the 'seqid' line,
    and 'sequence' lines.

    By default, the 'seqid' line starts with '>',while the 'sequence'
    lines don't. Change this behavior with 'startswith' option.

    Usage:
    >>>records = read_fastaLike('myFastaLikefile')
    >>>for rec in records:
    >>>    print('seqid:', rec[0])
    >>>    print('first seq line:', rec[1])

    '''

    with open(file, 'r') as fh:
        firstline = True
        count = 0
        rec = []
        for i in fh:
            i = i.rstrip()
            if i.startswith(startswith):
                if firstline:
                    firstline = False
                else:
                    yield rec

                count += 1
                if (maxrecords > 0) and (count > maxrecords):
                    raise StopIteration

                rec = []
                rec.append(i)

            else:
                rec.append(i)

        yield rec

        raise StopIteration


def read_fastaLike2(file, seqid_pattern='^>', maxrecords=-1):
    '''
    Every time return one record using the 'yield' function,
    the return record is a list, containing the 'seqid' line,
    and 'sequence' lines.

    By default, the 'seqid' line has regular pattern '^>',while the 'sequence'
    lines don't. Change this behavior with 'seqid_pattern' option.

    Usage:
    >>>records = read_fastaLike2('myFastaLikefile')
    >>>for rec in records:
    >>>    print('seqid:', rec[0])
    >>>    print('first seq line:', rec[1])

    '''

    with open(file, 'r') as fh:
        firstline = True
        count = 0
        rec = []
        for i in fh:
            i = i.rstrip()
            if re.search(seqid_pattern, i):
                if firstline:
                    firstline = False
                else:
                    yield rec

                count += 1
                if (maxrecords > 0) and (count > maxrecords):
                    raise StopIteration

                rec = []
                rec.append(i)

            else:
                rec.append(i)

        yield rec

        raise StopIteration



def get_all_key_to_all(triu_dict=None):
    '''
    by default, the lengthes of different sub-dictionaries returned by `csv2dict` function are different.

    this function is to make sure each sub-dictionary has the same length.
    '''
    new_dict = collections.OrderedDict()
    for key1 in triu_dict:
        new_dict.setdefault(key1, {})
        for key2 in triu_dict[key1]:
            val = triu_dict[key1][key2]
            new_dict[key1][key2] = val

            if key2 not in new_dict:
                new_dict.setdefault(key2, {})
            new_dict[key2][key1] = val

    return new_dict


def csv2dict(file=None, header=None, nrows=None, index_col=0, rm_self=True, all_key_to_all=False, **kwargs):
    '''
    targeted file: a csv file containing a matrix.

    by default, assuming the csv file does not have header row, and the first column (index 0) is the row names.

    you may specify how many rows to be read. otherwise, whole file will be
    read.

    1. read data from a csv file into a pandas Dataframe;
    2. change the up triangular and low triangular to dictionary 'triu_dict' and 'tril_dict', respectively.

    Parameter:
        rm_self: remove the pair of self-to-self, default True.
        all_key_to_all: make sure each sub-dictionary has the same length.


    Return:
        (triu_dict, tril_dict)

    '''

    if nrows:
        # raise ValueError('You must specify how many rows to be read!')
        df = pd.read_csv(file, header=header, nrows=nrows,
                         index_col=index_col, **kwargs)
    else:
        df = pd.read_csv(file, header=header, index_col=index_col, **kwargs)

    for index, row_name in enumerate(df.index):
        df = df.rename(index=str, columns={df.columns[index]: row_name})

    df_up = df.where(np.triu(np.ones(df.shape)).astype(np.bool)).stack()
    df_low = df.where(np.tril(np.ones(df.shape)).astype(np.bool)).stack()

    triu_dict = collections.OrderedDict()
    tril_dict = collections.OrderedDict()

    for index, val in df_up.iteritems():
        key1, key2 = index
        if rm_self and key1 == key2:
            continue

        if key1 not in triu_dict:
            triu_dict.setdefault(key1, {})
        triu_dict[key1][key2] = val

    for index, val in df_low.iteritems():
        key1, key2 = index
        if rm_self and key1 == key2:
            continue

        if key1 not in tril_dict:
            tril_dict.setdefault(key1, {})
        tril_dict[key1][key2] = val

    if all_key_to_all:
        new_triu_dict = get_all_key_to_all(triu_dict)
        new_tril_dict = get_all_key_to_all(tril_dict)
        return new_triu_dict, new_tril_dict
    else:
        return triu_dict, tril_dict


def csv2tupe(file=None, header=None, nrows=None, index_col=0, rm_self=True, **kwargs):
    '''
    targeted file: a csv file containing a matrix.

    by default, assuming the csv file does not have header row, and the first column (index 0) is the row names.

    you must specify how many rows to be read.

    1. read data from a csv file into a pandas Dataframe;
    2. change the up triangular and low triangular to LIST of tupes 'triu' and 'tril', respectively.

    Parameter:
        rm_self: remove the pair of self-to-self, default True.


    Return:
        (triu, tril)

    '''
    #if not nrows:
    #    raise ValueError('You must specify how many rows to be read!')

    if nrows:
        # raise ValueError('You must specify how many rows to be read!')
        df = pd.read_csv(file, header=header, nrows=nrows,
                         index_col=index_col, **kwargs)
    else:
        df = pd.read_csv(file, header=header, index_col=index_col, **kwargs)

    for index, row_name in enumerate(df.index):
        df = df.rename(index=str, columns={df.columns[index]: row_name})

    df_up = df.where(np.triu(np.ones(df.shape)).astype(np.bool)).stack()
    df_low = df.where(np.tril(np.ones(df.shape)).astype(np.bool)).stack()

    triu = []
    tril = []

    for index, val in df_up.iteritems():
        key1, key2 = index
        if rm_self and key1 == key2:
            continue

        triu.append((key1, key2, val))

    for index, val in df_low.iteritems():
        key1, key2 = index
        if rm_self and key1 == key2:
            continue

        tril.append((key1, key2, val))

    return triu, tril


def split_fasta_to_equal_size(fastafile=None, tot_file_num=10, outdir='./'):
    '''
    Split a fasta file to `tot_file_num` subfiles, and all subfiles have
    appropximately equal size.

    Return:
    A list of the subfiles' abspath

    '''

    seqid_seqsize = {}
    for rec in read_fastaLike(fastafile):
        seqid = rec[0].split()[0]
        seqsize = len("".join(rec[1:]))
        seqid_seqsize[seqid] = seqsize

    avg_seqsize = sum(seqid_seqsize.values()) / tot_file_num

    sub_tot_seqsize = 0

    subfiles = []
    count = 1
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    subfile = os.path.join(os.path.abspath(outdir), os.path.basename(fastafile)+'.'+str(count))
    subfiles.append(subfile)
    fhout = open(subfile, 'w')
    for rec in read_fastaLike(fastafile):
        seqid = rec[0].split()[0]
        seqsize = len("".join(rec[1:]))
        sub_tot_seqsize += seqsize

        if sub_tot_seqsize > avg_seqsize and count < tot_file_num:
            print("\n".join(rec), file=fhout)
            fhout.close()
            count += 1
            subfile = os.path.join(os.path.abspath(outdir), os.path.basename(fastafile)+'.'+str(count))
            subfiles.append(subfile)
            fhout = open(subfile, 'w')
            sub_tot_seqsize = 0
        else:
            print("\n".join(rec), file=fhout)

    fhout.close()

    return subfiles


def extend_ambiguous_dna(seq=None, get_a_random_seq=False, get_first_seq=False):
    """
    return a `map` iterator of all possible sequences given an ambiguous
    DNA input.

    if `get_a_random_seq=True`, return a randomly chosen sequence. Beware, if the seq is too long, and there are too many ambiguous sites,this can take
    a lot of memory. It is at your own risk to use `get_a_random_seq=True`. I
    would suggest you use `get_first_seq=True` instead.

    if `get_first_seq=True`, return only the first sequence of the `map`
    iterator. the result should always be the same for one input DNA.

    if `get_a_random_seq=True` and `get_first_seq=True` at the same time,
    only `get_first_seq=True` will work.

    cannot deal with 'U' in RNA sequences.

    the lower case or upper case of each base will be the same with input DNA.

    modified from:
    https://stackoverflow.com/questions/27551921/how-to-extend-ambiguous-dna-sequence

    """

    d = Seq.IUPAC.IUPACData.ambiguous_dna_values
    keys = list(d.keys())
    for k in keys:
        if k.isupper():
            low_k = k.lower()
            d[low_k] = d[k].lower()

    all_possible_seqs_iterator = map("".join, product(*map(d.get, seq)))

    if get_a_random_seq and not get_first_seq:
        all_possible_seqs = list(all_possible_seqs_iterator)
        index = randint(0, len(all_possible_seqs)-1)
        return all_possible_seqs[index]

    if get_first_seq:
        return next(all_possible_seqs_iterator)

    return all_possible_seqs_iterator


def extend_ambiguous_dna_randomly(seq=None):
    """
    return one sequence by randomly extending the input ambiguous DNA.

    the lower case or upper case of each base will be the same with input DNA.

    cannot deal with 'U' in RNA sequences.

    """

    d = Seq.IUPAC.IUPACData.ambiguous_dna_values
    keys = list(d.keys())
    for k in keys:
        if k.isupper():
            low_k = k.lower()
            d[low_k] = d[k].lower()

    new_seq = []
    for bases in map(d.get, seq):
        index = randint(0, len(bases)-1)
        new_seq.append(bases[index])

    return ''.join(new_seq)


def get_logger(debug=False):
    # 级别排序:CRITICAL > ERROR > WARNING > INFO > DEBUG
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - \n%(message)s\n")

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # must be DEBUG, then 'ch' below works.
    # logger.setFormatter(formatter)

    fh = logging.FileHandler(os.path.basename(sys.argv[0]) + '.log')
    if debug:
        fh.setLevel(logging.DEBUG)
    else:
        fh.setLevel(logging.INFO)  # INFO level goes to the log file
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    if debug:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.WARNING)  # only WARNING level will output on screen
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger

from glob import iglob
import ROOT
import rootpy
from rootpy.tree import Cut
from root_numpy import tree2rec
import pandas as pd
from time import time


def expander(
        dtype='cf',
        tree='rrqDir/calibzip1',
        base='/tera2/data3/cdmsbatsProd/R133/dataReleases/Prodv5-3_June2013/merged/',
        data='all',
        productions=['all'],
        cut='',
        cutrev=''):

    pbase = base + data + '/' + cutrev + dtype + '/' + cut

    if 'rrqDir/calib' in tree:
        fname = 'calib_Prodv5-3_{}_??.root'
    elif 'rqDir' in tree:
        fname = 'merge_Prodv5-3_{}_??.root'
    elif 'cutDir' in tree:
        fname = cut.rstrip('/') + '_{}_??.root'
    if productions == ['all']:
        prod = '0[0-9][0-9][0-9][0-9][0-9]?'
        ppath = iglob(pbase + fname.format(prod))
    else:
        ppath = (pbase + fname.format(i) for i in productions)

    result = [i + '/' + tree for i in ppath]
    result.sort()

    return result


def chainer(
        dtype='cf',
        izip=1,
        base='/tera2/data3/cdmsbatsProd/R133/dataReleases/Prodv5-3_June2013/merged/',
        data='all',
        productions=['all'],
        rqs=[],
        eventrqs=[],
        rrqs=[],
        eventrrqs=[],
        cuts=[],
        eventcuts=[],
        selections=[],
        cutrev='current'):

    # time call
    t1 = time()

    # deal with data chains
    dchain = ROOT.TChain()  # initialize data chain
    dlist = []
    # initialize first chain with calibebent trees (because they are small)
    dpaths = expander(
        dtype=dtype,
        tree='rrqDir/calibevent',
        base=base, data=data,
        productions=productions)
    map(dchain.Add, dpaths)
    # then make a list of chains for the other types
    for i, v in {
            'rrqDir/calibzip{}': rrqs,
            'rqDir/zip{}': rqs,
            'rqDir/eventTree': eventrqs}.iteritems():
        if len(v) != 0:
            tmp = ROOT.TChain()
            dpaths = expander(
                dtype=dtype,
                tree=i.format(izip),
                base=base,
                productions=productions)
            map(tmp.Add, dpaths)
            dlist.append(tmp)
    # friend each other data tree with the original chain
    map(dchain.AddFriend, dlist)

    # deal with cuts
    clist = {}
    for i, v in {
            'cutDir/cutzip{}': cuts,
            'cutDir/cutevent': eventcuts}.iteritems():
        for c in v:
            cpaths = expander(
                data='cuts',
                dtype=dtype,
                tree=i.format(izip),
                base=base,
                productions=productions,
                cut=c + '/',
                cutrev='current/')
            tmp = ROOT.TChain()
            #print "cpaths ", cpaths
            map(tmp.Add, cpaths)
            clist[c] = tmp
    #print "adding cuts: ", clist
    #print [dchain.AddFriend(v, k) for k, v in clist.iteritems()]

    # build cut selection
    cut_string = None
    if len(selections) != 0:
        cut_string = reduce(
            lambda x, y: x & y,
            map(
                Cut,
                selections))
    # extract the desired variables from the file turn into a Data Frame
    rows = ['SeriesNumber', 'EventNumber']
    df = pd.pivot_table(
        pd.DataFrame(
            tree2rec(
                dchain,
                branches=list(set(rrqs+rqs+eventrqs+eventrrqs+rows)),
                selection=cut_string)),
        rows=rows)
    t2 = time()
    print "Load time: ", t2-t1, "s"
    return df

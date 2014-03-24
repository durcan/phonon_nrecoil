from glob import iglob


def expander(
        dtype='ba',
        tree='rrqDir/calibzip1',
        base='/tera2/data3/cdmsbatsProd/R133/dataReleases/Prodv5-3_June2013/merged/',
        data='all',
        productions=['all'],
        cut='',
        cutrev=''):

    pbase = base + data + '/' + cutrev + dtype + '/' + cut

    if 'rrqDir' in tree:
        fname = 'calib_Prodv5-3_{}_ba.root'
    elif 'rqDir' in tree:
        fname = 'merge_Prodv5-3_{}_ba.root'
    elif 'cutDir' in tree:
        fname = cut + '_{}_ba.root'
    if productions == ['all']:
        prod = '0[0-9][0-9][0-9][0-9][0-9]?'
        ppath = iglob(pbase + fname.format(prod))
    else:
        ppath = (pbase + fname.format(i) for i in productions)

    return (i + '/' + tree for i in ppath)

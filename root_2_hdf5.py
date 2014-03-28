#!/localhome/cornell/anaconda/bin/python
import sys
import rootpy
from rootpy.io import root_open
from root_numpy import tree2rec
import pandas as pd


def main(infile, outfile):
    # open my data file
    f = root_open(infile)
    # build a dictionary of the file structure

    dic = {p: t for p, d, t in f if p != ''}
    # open a new file to put the data in after the cut is applied
    f_store = pd.HDFStore(outfile)
    # iterate over the directoies
    for d, tl in dic.iteritems():

        # iterate over list of trees in the directory
        for t in tl:
            # tree is original data tree
            tree = f[d][t]
            print tree.branchnames

            df = pd.DataFrame(
                tree2rec(
                    tree,
                    branches=tree.branchnames))
            print "writing to: {}/{}".format(d, t), tree.GetEntries()
            f_store.append('{}/{}'.format(d, t), df)
            tree.IsA().Destructor(tree)
    f_store.close()
    f.close()


if __name__ == '__main__':
    user_args = sys.argv[1:]
    main(*user_args)

#!/home/cornell/anaconda/bin/python
import sys
import rootpy
from rootpy.io import root_open


def main(cutname, cutfile, infile, outfile):

    c = root_open(cutfile)
    f = root_open(infile)

    cdict = {p: t for p, d, t in c if p != ''}
    clist = list(set(cdict['cutDir']))
    dic = {p: t for p, d, t in f if p != ''}

    f_copy = root_open(outfile, "recreate")
    for d, tl in dic.iteritems():
        f_copy.mkdir(d)
        f_copy.cd(d)
        for t in tl:
            tree = f[d][t]
            ct = [i for i in clist if i[-3:] in t]
            if ct != []:
                ctree = c['cutDir'][ct[0]]
                cut = "{}==0.0".format(cutname)
                tree.AddFriend(ctree)
            else:
                cut = ''
            tree_copy = tree.CopyTree(cut)
            tree_copy.Fill()
            tree_copy.Write()
            print "{}/{}: in".format(d, t),tree.GetEntries()," out", tree_copy.GetEntries()
            tree.IsA().Destructor(tree)
            tree_copy.IsA().Destructor(tree_copy)
        f_copy.cd('')

    f.close()
    f_copy.close()
    c.close()

if __name__ == '__main__':
    user_args = sys.argv[1:]
    main(*user_args)

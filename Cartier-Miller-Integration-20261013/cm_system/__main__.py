import argparse,json,sys
from .api import evaluate,quarter_precision_diagnostics,cartier_data,branch_query,weighted_sum,Session
from .rows import RowSession
from .character_sums import CharacterSumSession


def main():
    parser=argparse.ArgumentParser(description='Bounded exact Cartier-Miller integration prototype')
    sub=parser.add_subparsers(dest='target',required=True)
    for name in ('sum','plan'):
        p=sub.add_parser(name);p.add_argument('p',type=int);p.add_argument('L',type=int)
        p.add_argument('--precision',type=int,default=1);p.add_argument('--method',default='auto')
    p=sub.add_parser('quarter2');p.add_argument('p',type=int);p.add_argument('--method',default='product_tree')
    p=sub.add_parser('cartier');p.add_argument('p',type=int);p.add_argument('A',type=int);p.add_argument('B',type=int);p.add_argument('--trace',type=int)
    p=sub.add_parser('branch');p.add_argument('p',type=int);p.add_argument('f',nargs=4,type=int);p.add_argument('--root',type=int,required=True);p.add_argument('--trace',type=int)
    p=sub.add_parser('row');p.add_argument('p',type=int);p.add_argument('f',nargs='+',type=int);p.add_argument('--lambda',dest='lam',type=int,default=1);p.add_argument('--trace',type=int)
    p=sub.add_parser('charsum');p.add_argument('p',type=int);p.add_argument('f',nargs='+',type=int);p.add_argument('--trace',type=int)
    g=p.add_mutually_exclusive_group(required=True);g.add_argument('--pole',type=int);g.add_argument('--exclude',nargs='*',type=int)
    p.add_argument('--residues',nargs='*',type=int,default=[]);p.add_argument('--constant',type=int,default=0)
    p=sub.add_parser('weighted');p.add_argument('p',type=int);p.add_argument('L',type=int);p.add_argument('weights',nargs='+',type=int)
    a=parser.parse_args()
    try:
        if a.target=='sum':z=evaluate(a.p,a.L,a.precision,a.method)
        elif a.target=='plan':z=Session(a.p).plan(a.L,a.precision)
        elif a.target=='quarter2':z=quarter_precision_diagnostics(a.p,a.method)
        elif a.target=='cartier':z=cartier_data(a.p,a.A,a.B,a.trace)
        elif a.target=='branch':z=branch_query(a.p,a.f,a.root,a.trace)
        elif a.target=='row':z=RowSession(a.p,a.f,a.trace).query(a.lam)
        elif a.target=='charsum':
            c=CharacterSumSession(a.p,a.f,a.trace)
            z=c.single_pole(a.pole) if a.pole is not None else c.prepare(a.exclude).evaluate(a.residues,a.constant)
        else:z=weighted_sum(a.p,a.L,a.weights)
        print(json.dumps(z,indent=2))
    except (ValueError,ArithmeticError) as e:
        print(json.dumps({'status':'error','type':type(e).__name__,'message':str(e)}));return 2
    return 0


if __name__=='__main__':sys.exit(main())

"""Direct parameter certificates for the depth<=2 ordinary seed closure.
Standard-library research prototype. No point-count backend. Supplied exact
traces remain trusted; certificates verify models and differential transport.
"""
from pathlib import Path
from dataclasses import dataclass
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'isogeny_closure_20261006/core'))
from isogeny_closure import check_short,easy,quotient,verify_path,short_model
from branch_evaluator import BranchEvaluator,check_cubic,is_prime64

# D, prime congruence, alpha0,alpha1,gamma0,gamma1,alpha^3 pair,gamma^2 pair
FAMILIES={
    'depth2_1728':(2,8,-91,-60,-462,-308,(-2719171,-1922580),(403172,284592)),
    'depth2_0':(3,12,-135,-60,-694,-420,(-6834375,-3928500),(1010836,582960)),
}

def validate_prime(p):
    if not isinstance(p,int) or isinstance(p,bool) or p<7 or not is_prime64(p):
        raise ValueError('require prime 7<=p<2^64')

def _certificate(A,B,p,family,r=None,e=None):
    if family.startswith('easy'):
        if family=='easy_0':
            valid=A==0 and p%3==1
        elif family=='easy_1728':
            valid=B==0 and p%4==1
        else:valid=False
        if not valid:raise ValueError('unsupported or mislabeled easy seed')
        roots=[];params={};slope=0
    elif family in ('depth1_1728','depth1_0'):
        mod=4 if family=='depth1_1728' else 3
        alpha,gamma=(-11,-14) if mod==4 else (-15,-22)
        if p%mod!=1 or not r or A!=alpha*r*r%p or B!=gamma*r**3%p:
            raise ValueError('invalid first-depth family parameters')
        roots=[-2*r%p];params={'r':r};slope=-r%p
    elif family in FAMILIES:
        D,mod,a0,a1,b0,b1,_,_=FAMILIES[family]
        if p%mod!=1 or not r or e is None or e*e%p!=D%p:
            raise ValueError('invalid depth-two family congruence/parameters')
        alpha=(a0+a1*e)%p;gamma=(b0+b1*e)%p
        if A!=alpha*r*r%p or B!=gamma*r**3%p:
            raise ValueError('parameters do not reproduce both short coefficients')
        roots=[-2*(1+2*e)*r%p,-8*r%p]
        params={'r':r,'e':e,'e_squared':D};slope=-(3+2*e)*r%p
    else:raise ValueError('unknown certificate family')
    path=verify_path(A,B,p,roots)
    if path['beta_multiplier']!=slope:raise AssertionError('independent reverse-path slope mismatch')
    return {'status':'verified_parameter_certificate','p':p,'short_model':[A,B],
            'family':family,'parameters':params,'beta_multiplier':slope,
            'depth':len(roots),'reverse_path':path,
            'recognition_field_work':'O(1), excludes trace/prime validation',
            'square_root_search_used':False}

def recognize_short(A,B,p):
    """Complete direct recognition for the normalized rational depth<=2
    closure of the two permitted beta-zero seed families, including all their
    quadratic twists. No roots, coefficient powers or graph search is used.
    p prime validation is separate bit work.
    """
    validate_prime(p);A,B=check_short(A,B,p)
    matches=[]
    seed=easy(A,B,p)
    if seed:
        matches.append(_certificate(A,B,p,'easy_0' if A==0 else 'easy_1728'))
    if A and B:
        for family,mod,alpha,gamma in [('depth1_1728',4,-11,-14),('depth1_0',3,-15,-22)]:
            if p%mod==1:
                # alpha,gamma are nonzero in the permitted congruence classes.
                r=alpha*B*pow(gamma*A,-1,p)%p
                if r and A==alpha*r*r%p and B==gamma*r**3%p:
                    matches.append(_certificate(A,B,p,family,r))
        for family,(D,mod,a0,a1,b0,b1,a3,g2) in FAMILIES.items():
            if p%mod!=1:continue
            AA=pow(A,3,p);BB=B*B%p
            U=(BB*a3[0]-AA*g2[0])%p
            V=(BB*a3[1]-AA*g2[1])%p
            if V==0:continue
            e=-U*pow(V,-1,p)%p
            if e*e%p!=D:continue
            alpha=(a0+a1*e)%p;gamma=(b0+b1*e)%p
            if not alpha or not gamma:raise AssertionError('excluded coefficient degeneration in ordinary domain')
            r=alpha*B*pow(gamma*A,-1,p)%p
            if r and A==alpha*r*r%p and B==gamma*r**3%p:
                matches.append(_certificate(A,B,p,family,r,e))
    slopes={m['beta_multiplier'] for m in matches}
    if len(slopes)>1:raise AssertionError('conflicting independently checked family certificates')
    return {'status':'recognized' if matches else 'not_in_depth_at_most_two_closure',
            'p':p,'short_model':[A,B],'matches':matches,
            'scope':'ordinary A=0,p=1mod3 or B=0,p=1mod4 seeded rational depth<=2 closure',
            'graph_search_used':False,'square_root_search_used':False}

def verify_supplied_certificate(p,A,B,certificate):
    """Reverify parameter equations and transport; stored output is untrusted."""
    validate_prime(p);A,B=check_short(A,B,p)
    family=certificate['family'];params=certificate.get('parameters',{})
    r=params.get('r');e=params.get('e')
    if r is not None:r%=p
    if e is not None:e%=p
    return _certificate(A,B,p,family,r,e)

@dataclass(frozen=True)
class RecognizedPreparation:
    evaluator:BranchEvaluator
    certificate:dict
    trusted_exact_trace:int

def prepare_from_trace(p,f,trusted_exact_trace):
    """Exact family K reconstruction from a caller-trusted exact trace.
    Complete theoretical cost is trace preparation plus constant field work.
    """
    validate_prime(p);f=check_cubic(f,p)
    if not isinstance(trusted_exact_trace,int) or isinstance(trusted_exact_trace,bool) or trusted_exact_trace**2>4*p:
        raise ValueError('trace fails necessary Hasse interval; not a certification test')
    A,B=short_model(f,p);rec=recognize_short(A,B,p)
    if rec['status']!='recognized':return rec
    cert=min(rec['matches'],key=lambda x:x['depth'])
    H=trusted_exact_trace%p;beta=cert['beta_multiplier']*H%p
    _,_,b,a=f;K=(beta-b*pow(3,-1,p)*H)*pow(a,-1,p)%p
    return RecognizedPreparation(BranchEvaluator(p,f,H,K,'direct_depth_two_caller_supplied_exact_trace'),cert,trusted_exact_trace)

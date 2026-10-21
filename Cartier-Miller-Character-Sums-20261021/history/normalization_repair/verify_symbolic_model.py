"""Optional exact verification over Q[g1,g2,g3,g4]; requires SymPy."""
import json,pathlib
import sympy as s
z,v=s.symbols('z v');a,b,c,d=s.symbols('g1 g2 g3 g4')
g=1+a*z+b*z*z+c*z**3+d*z**4
x=(2*(v+1)+a*z)/z**2
y=(4*(v+1)+2*(a*z+b*z*z)-a*a*z*z/2)/z**3
X=x+b/3;Y=y+(a*x+2*c)/2
r=a*a/4-2*b/3;t=-c+a*b/2-a**3/8
A=-4*d+a*c-b*b/3
B=c*c-s.Rational(8,3)*b*d+a*a*d-b*a*c/3+2*b**3/27
decomposition=s.factor(Y+t-(2/z+a/2)*(X-r))
num=s.together(Y*Y-X**3-A*X-B).as_numer_denom()[0]
curve=s.factor(s.rem(num,v*v-g,v))
point=s.factor(t*t-r**3-A*r-B)
assert decomposition==curve==point==0
out={'status':'PASS','sympy_version':s.__version__,
     'coefficient_domain':'Q[g1,g2,g3,g4]',
     'decomposition_identity':str(decomposition),
     'curve_identity_mod_v2_minus_g':str(curve),'adapted_point_on_curve':str(point)}
root=pathlib.Path(__file__).resolve().parent
(root/'results/symbolic_model.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

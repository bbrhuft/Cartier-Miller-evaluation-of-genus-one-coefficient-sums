# Independent symbolic audit of the Wronskian proof steps (sympy), not reusing atkin.py
import sympy as sp
j=sp.symbols('j',positive=True)
alpha=24*(144*j**2-29)/((2*j+1)*(2*j-1))
beta=36*(12*j-13)*(12*j-7)*(12*j-5)*(12*j+1)/(j*(j-1)*(2*j-1)**2)
r=lambda t: -6*(12*t-1)*(12*t+5)/(t*(2*t+1))
R=lambda t: (12*t-1)*(12*t+5)/(96*t)
# (i) special-value ratio satisfies r_j = -alpha_j - beta_j/r_{j-1}
print('ratio identity:', sp.simplify(r(j)+alpha+beta/r(j-1)))
# (ii) gamma_j = beta_j/r_{j-1}^2 and telescoping R(j)-gamma_j R(j-1)=1
gamma=sp.simplify(beta/r(j-1)**2)
print('gamma:', sp.factor(gamma))
print('telescope:', sp.simplify(R(j)-gamma*R(j-1)))
# (iii) beta_{j+1}/r_j
print('beta_{j+1}/r_j:', sp.factor(sp.simplify(beta.subs(j,j+1)/r(j))))
# (iv) initial data
A1=sp.Symbol('J')-720; A2=sp.Symbol('J')**2-1640*sp.Symbol('J')+269280
al1=alpha.subs(j,1); print('alpha_1',al1,' beta_1 =',sp.expand((sp.Symbol('J')-al1)*A1-A2))
print('-beta_1/(4 a_1)=',sp.Rational(-393120,4*(-720)))

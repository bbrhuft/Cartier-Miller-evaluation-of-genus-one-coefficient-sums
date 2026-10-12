#!/usr/bin/env python3
"""Numerical D=-12 normalization control, not an exact CM proof."""
from decimal import Decimal, localcontext
import json

def control():
    with localcontext() as ctx:
        ctx.prec = 80
        D = Decimal
        pi = D('3.14159265358979323846264338327950288419716939937510582097494459230781640628620899')
        y = D(3).sqrt()
        q = (-2*pi*y).exp()
        sums = [D(0), D(0), D(0)]
        for n in range(1,40):
            term = q**n/(1-q**n)
            for k, exponent in enumerate((1,3,5)):
                sums[k] += D(n)**exponent*term
        E2, E4, E6 = 1-24*sums[0], 1+240*sums[1], 1-504*sums[2]
        E2star = E2-3/(pi*y)
        s2 = E2star*E4/E6
        slope = -D(11)/5*s2
        if abs(s2-D(5)/11)>D('1e-60') or abs(slope+1)>D('1e-60'):
            raise ArithmeticError('normalization control failed')
        return {'status':'numerical_control_agrees_not_a_proof', 'precision_digits':80,
                'nonconstant_summands':39,'tau':'i sqrt(3)','CM_discriminant':-12,
                'E2star':str(E2star),'s2':str(s2),'s2_minus_5_over_11':str(s2-D(5)/11),
                'predicted_beta_over_rH':str(slope),
                'limitation':'floating Decimal calculation, not interval-certified or algebraically proved'}

if __name__=='__main__':
    print(json.dumps(control(),indent=2))

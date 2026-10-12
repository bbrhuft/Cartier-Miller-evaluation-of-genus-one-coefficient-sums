"""Literature-route cross-check (Bruinier-Ono-Sutherland, arXiv:1301.5672v3,
eq. (1.2), Lemma 2.3 / (2.8)-(2.9), attributed to Masser 1975 p.118):
    gamma = (2 b02 - b11)/b01 from the Taylor coefficients of a classical
    modular polynomial at (j, j);  s2 = 6 j gamma + (7j - 6912)/(j - 1728).
(a) Literal reading Phi_D = Phi_|D|: applied to D=-7 (Phi_7) -- hypotheses
    of the lemma hold (D<-4, D != -3d^2) and Phi_7(j,j)=0.
(b) The same literal reading at D=-8 uses Phi_8, but Phi_8(j,j) != 0 (no
    primitive element of norm 8 in Z[sqrt-2]); the output is recorded as a
    source-hypothesis warning, not a counterexample to the paper.
(c) Experimental Masser-type variants with Phi_m, m the norm of a primitive
    trace-zero element (m=2 for D=-8, m=3 for D=-12): our own checks, not
    literature claims.
PARI polmodular is a practical comparator; Phi_8 is built from Phi_2 by
resultants (Res_z(Phi2(x,z),Phi4(z,y)) = Phi8 * Phi2^2,
 Res_z(Phi2(x,z),Phi2(z,y)) = Phi4 * (x-y)^3)."""
import json
import cypari2
pari = cypari2.Pari(); pari.allocatemem(4*10**9)
def masser(polname, j0):
    pari(f'PP = subst(subst({polname}, x, X+({j0})), y, Y+({j0}));')
    c = lambda i, k: pari(f'polcoef(polcoef(PP,{i},X),{k},Y)')
    b00, b01, b02, b11 = c(0, 0), c(0, 1), c(0, 2), c(1, 1)
    if b01 == 0:
        return {'b00_is_zero': b00 == 0, 'b01': 0, 's2': None}
    gam = (2*b02 - b11)/b01; j = pari(j0)
    return {'b00_is_zero': bool(b00 == 0), 'gamma': str(gam), 's2': str(6*j*gam + (7*j - 6912)/(j - 1728))}
pari('P2 = polmodular(2); P3 = polmodular(3); P7 = polmodular(7);')
pari('P4 = polresultant(subst(P2,y,z), subst(P2,x,z), z)/(x-y)^3;')
pari('P8 = polresultant(subst(P2,y,z), subst(P4,x,z), z)/P2^2;')
out = {
 'a_literal_D-7_Phi7': masser('P7', -3375),
 'b_literal_D-8_Phi8_hypothesis_warning': masser('P8', 8000),
 'c_variant_D-8_Phi2': masser('P2', 8000),
 'c_variant_D-12_Phi3': masser('P3', 54000),
 'c_variant_D-7_Phi2_trace_one_element': masser('P2', -3375),
 'expected_from_endomorphism_loops': {'D-7': '5/21', 'D-8': '5/14', 'D-12': '5/11'},
}
print(json.dumps(out, indent=1))
json.dump(out, open(__file__.rsplit('/theory/', 1)[0] + '/results/bos_masser_check.json', 'w'), indent=1)
import sys
sys.exit(0 if out['a_literal_D-7_Phi7']['s2'] == '5/21' and out['c_variant_D-8_Phi2']['s2'] == '5/14' and out['c_variant_D-12_Phi3']['s2'] == '5/11' else 1)

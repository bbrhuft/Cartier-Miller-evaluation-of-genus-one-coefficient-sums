# One exact coefficient as a matched comparator

This deduction is a supplied project adapter, not a claim that Bostan–Gaudry–Schost explicitly state the weighted-sum formula. Verify it independently and cite the original recurrence algorithms separately.

Let p>=7, h=(p-1)/2, d=deg f in {3,4}, F=f^h, and write F=L+x^p H_high with deg L<p. The inherited all-point identity is

    C_f(a) = -F'(a)-H_high(a),   a in F_p.

Define

    f_a(z)=f(a+z),
    G_a(z)=z^d f(a+1/z),
    N=dh-p.

G_a is the reversal of the degree-d Taylor shift f_a. Its constant coefficient is the nonzero leading coefficient ell of f, even when a is a branch value.

Translation gives F(a+z)=L(a+z)+(a+z^p)H_high(a+z), since a^p=a. Both L and H_high have degree below p, so

    [z^p]F(a+z)=H_high(a).

Reversing F(a+z) therefore yields

    H_high(a)=[z^(dh-p)]G_a(z)^h.

Consequently the exact matched target is

    C_f(a)=-F'(a)-[z^N]G_a(z)^h.

Here N=(p-3)/2 for cubics and N=p-2 for quartics. In particular 0<=N<p, so a forward recurrence to N does not encounter division by p. The formula includes a=0 and branch poles. It does not make branch poles polylogarithmically evaluable.

The derivative can be computed directly as F'(a)=h f(a)^(h-1) f'(a); it is zero at a root because h>=3. No division by f(a) is necessary. The exponentiation cost is O(log p).

## Fixed-order recurrence

Write G_a(z)=sum_(j=0)^d g_j z^j and G_a^h=sum e_k z^k. From G_a (G_a^h)'=h G_a' G_a^h,

    k g_0 e_k = sum_(j=1)^min(d,k) (((h+1)j-k) g_j e_(k-j)),
    e_0=g_0^h.

Every denominator k g_0 is invertible for 1<=k<=N. The state dimension is at most four, and its transition matrix has entries rational in k with a shared linear denominator. A genuine BGS adapter should clear and restore this denominator through the block-product algorithm, proving that all necessary units are available. This is the specific matrix recurrence to implement; a generic point-counting call is not the adapter.

## Supplied linear reference

Set u_k=k! g_0^k e_k. Then

    u_k = sum_(j=1)^min(d,k) (((h+1)j-k) g_j g_0^(j-1)
                          * ((k-1)!/(k-j)!) * u_(k-j)).

The factorial ratio in this equation is the product of at most d-1 adjacent integers; no division is used. Maintain the last d states and s_k=k! g_0^k. Recover e_N=u_N/s_N with one final inversion. This is O(p) field work and O(d) working field elements for fixed d, plus the initial and final O(log p) exponentiation work. It uses no trace. An implementation is in comparators/reference_comparators.py.

This reference is intentionally distinct from a native BGS implementation. Its Python wall time is not a theoretical operation count. It provides a tested output contract and a starting point for the required adapter.

## Full-polynomial route and reuse

FLINT can construct F=f^h directly. A single C_f(a) is then -F'(a)-H_high(a), evaluated by Horner. For many a on the same f,p, F and H_high are reused. Fast multipoint evaluation is a legitimate further comparator for dense workloads and should be included where implementable. Do not charge the whole polynomial afresh for every prepared query.

For multiple poles, compute the same common-domain correction terms for every scalar method, or give a proved alternative adapter with its complete cost. Choosing one output convention for some methods and another for Cartier–Miller invalidates a speed comparison.

## Complexity comparison to prove

The linear recurrence costs O(p) field work. BGS-style block products are expected to give soft-O(sqrt(p)) field work at fixed degree, subject to the precise chosen theorem and adapter. The inherited nonbranch prepared query is O(log p) multiplications and inversions, with trace/model preparation separate. None of these statements alone establishes that Cartier–Miller is new relative to existing logarithmic-transfer algorithms.

Correctness checks of this handover do not establish timing crossovers or validate an unimplemented BGS adapter.

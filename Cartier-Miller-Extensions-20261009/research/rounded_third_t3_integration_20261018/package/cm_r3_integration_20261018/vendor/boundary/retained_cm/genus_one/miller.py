"""
One-pass Miller recurrence for the constant term alpha_M(R) = [t^0] d log f_{M,R} / dt at O on a short
Weierstrass curve Y^2 = X^3 + A X + B, t = -X/Y, where div f_{M,R} = M(R) - (MR) - (M-1)(O)  (Miller's invariant).
Each chord/tangent-over-vertical factor contributes its slope mu; verticals and identity steps contribute 0
(in short form a1 = 0). No point order is required: M R need not be O.
Works over any context from fields.py; returns (alpha, M R) with O represented as None.
"""
def _add(ctx, P, Q, A):
    if P is None: return Q, ctx.zero
    if Q is None: return P, ctx.zero
    (x1, y1), (x2, y2) = P, Q
    if ctx.eq(x1, x2):
        if ctx.iszero(ctx.add(y1, y2)): return None, ctx.zero
        if not ctx.eq(y1, y2):
            # Only possible in a split algebra: the two components disagree (P = Q in one, P = -Q in the other).
            # y1 - y2 is then a nonzero zero divisor; hand it to the caller as a square-root witness.
            from .fields import ZeroDivisorFound
            raise ZeroDivisorFound(ctx.sub(y1, y2))
        num = ctx.add(ctx.mul(ctx.fromint(3), ctx.mul(x1, x1)), A)
        mu = ctx.mul(num, ctx.inv(ctx.mul(ctx.fromint(2), y1)))
    else:
        mu = ctx.mul(ctx.sub(y2, y1), ctx.inv(ctx.sub(x2, x1)))
    x3 = ctx.sub(ctx.sub(ctx.mul(mu, mu), x1), x2)
    y3 = ctx.sub(ctx.mul(mu, ctx.sub(x1, x3)), y1)
    return (x3, y3), mu

def miller_alpha(ctx, R, M, A):
    A = A if not isinstance(A, int) else ctx.fromint(A)
    assert M >= 1
    T, alpha = R, ctx.zero
    two = ctx.fromint(2)
    for bit in bin(M)[3:]:
        T, mu = _add(ctx, T, T, A); alpha = ctx.add(ctx.mul(two, alpha), mu)
        if bit == '1':
            T, mu = _add(ctx, T, R, A); alpha = ctx.add(alpha, mu)
    return alpha, T


class Resume(Exception):
    """Raised by miller_alpha_resumable when a split-algebra operation meets a zero divisor.
    Carries the state BEFORE the failing operation, so both components can be continued over the base field."""
    def __init__(s, j, T, alpha, witness):
        super().__init__("split needed"); s.j, s.T, s.alpha, s.witness = j, T, alpha, witness

def _ops(M): 
    ops = []
    for bit in bin(M)[3:]:
        ops.append("D")
        if bit == "1": ops.append("A")
    return ops

def miller_continue(ctx, R, M, A, T, alpha, start=0):
    """Run (or resume) the Miller recurrence from operation index `start` with state (T, alpha)."""
    from .fields import ZeroDivisorFound
    A = A if not isinstance(A, int) else ctx.fromint(A)
    two = ctx.fromint(2)
    for j, op in enumerate(_ops(M)):
        if j < start: continue
        try:
            if op == "D":
                T2, mu = _add(ctx, T, T, A); alpha2 = ctx.add(ctx.mul(two, alpha), mu)
            else:
                T2, mu = _add(ctx, T, R, A); alpha2 = ctx.add(alpha, mu)
        except ZeroDivisorFound as z:
            raise Resume(j, T, alpha, z.element)
        T, alpha = T2, alpha2
    return alpha, T

def miller_alpha_resumable(ctx, R, M, A):
    return miller_continue(ctx, R, M, A, R, ctx.zero, 0)

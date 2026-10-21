/* cmnative.c -- native comparators for the Cartier-Miller matched-output benchmarks.
 *
 * Written 20 October 2026 for the prior-work/benchmark package.  No inherited code.
 * Arithmetic: residues in uint64_t, products via unsigned __int128, p < 2^63.
 * Single-threaded.  Build: gcc -O2 -fPIC -shared -o libcmnative.so cmnative.c
 *
 * Exported functions (all return residues in [0,p) unless stated):
 *   cm_squares_bitmap(p, out)            out: bitmap of nonzero squares, (p+7)/8 bytes, O(p) work
 *   cm_enum_single(p, deg, f, a, bm)     sum_{x!=a} chi(f(x))/(x-a)  via the bitmap, block batch inversion
 *   cm_enum_epsilon(p, deg, f, bm, eps)  eps[x] = chi(f(x)) as int8 (-1,0,1) for x in [0,p)
 *   cm_linrec_coeff(p, d, g, h, N)       [z^N] g(z)^h, 0<=N<p, g[0]!=0, O(N) work, one final inversion
 *   cm_inverse_table(p, out)             out[t] = 1/t mod p for 1<=t<p (out[0]=0), O(p) work
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

typedef uint64_t u64;
typedef unsigned __int128 u128;

static inline u64 mulm(u64 a, u64 b, u64 p) { return (u64)(((u128)a * b) % p); }
static inline u64 addm(u64 a, u64 b, u64 p) { u64 s = a + b; return s >= p ? s - p : s; }
static inline u64 subm(u64 a, u64 b, u64 p) { return a >= b ? a - b : a + p - b; }

static u64 powm(u64 a, u64 e, u64 p) {
    u64 r = 1 % p;
    a %= p;
    while (e) { if (e & 1) r = mulm(r, a, p); a = mulm(a, a, p); e >>= 1; }
    return r;
}
static u64 invm(u64 a, u64 p) { return powm(a, p - 2, p); }

/* Bitmap of nonzero squares: mark y^2 for 1 <= y <= (p-1)/2.  Incremental: (y+1)^2 = y^2 + 2y + 1. */
int cm_squares_bitmap(u64 p, uint8_t *bm) {
    memset(bm, 0, (size_t)((p + 7) / 8));
    u64 s = 0, h = (p - 1) / 2;
    for (u64 y = 1; y <= h; y++) {
        s = addm(s, addm(subm(2 * (y - 1) % p, 0, p), 1, p), p);   /* s = y^2 */
        bm[s >> 3] |= (uint8_t)(1u << (s & 7));
    }
    return 0;
}

static inline int chi_bm(u64 v, const uint8_t *bm) {
    if (v == 0) return 0;
    return (bm[v >> 3] >> (v & 7)) & 1 ? 1 : -1;
}

static inline u64 horner(int deg, const u64 *f, u64 x, u64 p) {
    u64 v = 0;
    for (int i = deg; i >= 0; i--) v = addm(mulm(v, x, p), f[i], p);
    return v;
}

void cm_enum_epsilon(u64 p, int deg, const u64 *f, const uint8_t *bm, int8_t *eps) {
    for (u64 x = 0; x < p; x++) eps[x] = (int8_t)chi_bm(horner(deg, f, x, p), bm);
}

/* sum_{x != a} chi(f(x)) / (x - a): iterate t = x - a over 1..p-1, accumulate numerators over a
 * common denominator in blocks (Montgomery-style): per block one inversion; work O(p) mulmods. */
#define BLK 512
u64 cm_enum_single(u64 p, int deg, const u64 *f, u64 a, const uint8_t *bm) {
    u64 total = 0;
    u64 t = 1;
    while (t < p) {
        /* block: sum_{i} e_i / t_i = (sum_i e_i * prod_{j!=i} t_j) / prod t_j, computed incrementally:
         * maintain (num, den) with num/den = partial sum; adding e/t: num = num*t + e*den, den = den*t */
        u64 num = 0, den = 1;
        for (int i = 0; i < BLK && t < p; i++, t++) {
            u64 x = a + t; if (x >= p) x -= p;
            int e = chi_bm(horner(deg, f, x, p), bm);
            num = mulm(num, t, p);
            if (e == 1) num = addm(num, den, p);
            else if (e == -1) num = subm(num, den, p);
            den = mulm(den, t, p);
        }
        total = addm(total, mulm(num, invm(den, p), p), p);
    }
    return total;
}

void cm_inverse_table(u64 p, u64 *inv) {
    inv[0] = 0;
    if (p > 1) inv[1] = 1;
    for (u64 t = 2; t < p; t++) inv[t] = mulm(p - p / t, inv[p % t], p);
}

/* [z^N] g^h for deg g = d <= 8, g[0] != 0, 0 <= N < p.
 * u_k = k! g0^k e_k satisfies u_k = sum_{j=1}^{min(d,k)} ((h+1)j - k) g_j g0^{j-1} (k-1)!/(k-j)! u_{k-j};
 * s_k = k! g0^k; e_N = u_N / s_N (one inversion).  Same contract as the supplied Python reference. */
u64 cm_linrec_coeff(u64 p, int d, const u64 *g, u64 h, u64 N) {
    if (N >= p || g[0] % p == 0 || d < 1 || d > 8) return (u64)-1;
    u64 g0 = g[0] % p;
    u64 gp[9];            /* gp[j] = g_j * g0^{j-1} */
    u64 pw = 1;
    for (int j = 1; j <= d; j++) { gp[j] = mulm(g[j] % p, pw, p); pw = mulm(pw, g0, p); }
    u64 hist[9];          /* hist[0] = u_{k-1}, hist[1] = u_{k-2}, ... */
    for (int i = 0; i < 9; i++) hist[i] = 0;
    hist[0] = powm(g0, h, p);
    u64 scale = 1;
    u64 hp1 = (h + 1) % p;
    for (u64 k = 1; k <= N; k++) {
        u64 u = 0, falling = 1;
        int jm = (u64)d < k ? d : (int)k;
        for (int j = 1; j <= jm; j++) {
            if (j > 1) falling = mulm(falling, (k - j + 1) % p, p);
            u64 coef = subm(mulm(hp1, (u64)j, p), k % p, p);     /* (h+1) j - k mod p */
            u64 term = mulm(mulm(coef, gp[j], p), mulm(falling, hist[j - 1], p), p);
            u = addm(u, term, p);
        }
        for (int i = d - 1; i > 0; i--) hist[i] = hist[i - 1];
        hist[0] = u;
        scale = mulm(mulm(scale, k % p, p), g0, p);
    }
    return mulm(hist[0], invm(scale, p), p);
}

/* All coefficients e_0..e_N of g^h, 0 <= N < p, g[0] != 0, deg g = d <= 8:
 * k g0 e_k = sum_{j=1}^{min(d,k)} ((h+1) j - k) g_j e_{k-j}.  Inverses 1/k from the linear-time
 * table inv[k] = -(p div k) inv[p mod k]; storage: out (N+1 words) + inv (N+1 words). */
int cm_linrec_all(u64 p, int d, const u64 *g, u64 h, u64 N, u64 *out) {
    if (N >= p || g[0] % p == 0 || d < 1 || d > 8) return -1;
    u64 *inv = (u64 *)malloc((size_t)(N + 2) * sizeof(u64));
    if (!inv) return -2;
    inv[0] = 0; if (N >= 1) inv[1] = 1;
    for (u64 t = 2; t <= N; t++) inv[t] = mulm(p - p / t, inv[p % t], p);
    u64 ig0 = invm(g[0] % p, p), hp1 = (h + 1) % p;
    out[0] = powm(g[0], h, p);
    for (u64 k = 1; k <= N; k++) {
        u64 acc = 0;
        int jm = (u64)d < k ? d : (int)k;
        for (int j = 1; j <= jm; j++) {
            u64 coef = subm(mulm(hp1, (u64)j, p), k % p, p);
            acc = addm(acc, mulm(mulm(coef, g[j] % p, p), out[k - j], p), p);
        }
        out[k] = mulm(mulm(acc, inv[k], p), ig0, p);
    }
    free(inv);
    return 0;
}

/* sum_{x in F_p} chi(f(x)) mod p via the bitmap (O(p)); returned as a residue. */
u64 cm_enum_sum_eps(u64 p, int deg, const u64 *f, const uint8_t *bm) {
    long long s = 0;
    for (u64 x = 0; x < p; x++) s += chi_bm(horner(deg, f, x, p), bm);
    long long r = s % (long long)p;
    return (u64)(r < 0 ? r + (long long)p : r);
}

/* e_N and e_{N+1} of g^h (0 <= N, N+1 < p): out[0] = e_N, out[1] = e_{N+1}; one extra step. */
int cm_linrec_coeff2(u64 p, int d, const u64 *g, u64 h, u64 N, u64 *out) {
    if (N + 1 >= p || g[0] % p == 0 || d < 1 || d > 8) return -1;
    u64 g0 = g[0] % p, gp[9], pw = 1;
    for (int j = 1; j <= d; j++) { gp[j] = mulm(g[j] % p, pw, p); pw = mulm(pw, g0, p); }
    u64 hist[9]; for (int i = 0; i < 9; i++) hist[i] = 0;
    hist[0] = powm(g0, h, p);
    u64 scale = 1, hp1 = (h + 1) % p, scaleN = 1, uN = hist[0];
    for (u64 k = 1; k <= N + 1; k++) {
        u64 u = 0, falling = 1;
        int jm = (u64)d < k ? d : (int)k;
        for (int j = 1; j <= jm; j++) {
            if (j > 1) falling = mulm(falling, (k - j + 1) % p, p);
            u64 coef = subm(mulm(hp1, (u64)j, p), k % p, p);
            u = addm(u, mulm(mulm(coef, gp[j], p), mulm(falling, hist[j - 1], p), p), p);
        }
        for (int i = d - 1; i > 0; i--) hist[i] = hist[i - 1];
        hist[0] = u;
        scale = mulm(mulm(scale, k % p, p), g0, p);
        if (k == N) { uN = u; scaleN = scale; }
    }
    if (N == 0) { uN = powm(g0, h, p); scaleN = 1; }
    out[0] = mulm(uN, invm(scaleN, p), p);
    out[1] = mulm(hist[0], invm(scale, p), p);
    return 0;
}

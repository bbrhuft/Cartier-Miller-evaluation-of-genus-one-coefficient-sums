# Cartier–Miller Studio

An offline Python application for exploring the special-family evaluations in the accompanying research. Version 1.0.0, 28 September 2026.

The app combines a draggable genus model, exact modular answers, a replay of the actual binary Miller chain, live timing comparisons and a separate p-adic laboratory. The main application uses Python’s standard library; the FLINT comparison is optional.

## Open the app

On Windows, extract the **whole ZIP** into a normal folder and double-click **launch_windows.bat**. A standard Python 3.10 or newer installation with Tcl/Tk is required. Python 3.12 or 3.13 is a suitable choice. Run it outside QGIS’s Python environment. No Qt package is used.

From a terminal in the extracted folder, the equivalent command is:

```sh
python app.py
```

On macOS or Linux, use `python3 app.py` or `sh launch_macos_linux.sh`. Some Linux distributions supply Tkinter as a separate system package, usually `python3-tk`. Running `python3 -m tkinter` should open a small test window. The app itself performs no downloads and requires no browser or server.

## Enable the stronger comparison

The direct recurrence and all Cartier–Miller calculations work immediately. The square-root block-product comparison needs **python-flint 0.9.0**.

On Windows, double-click **install_optional_windows.bat** once, then open the app with **launch_windows.bat**. The installer creates a private `.venv` inside the extracted folder and installs only the optional comparison package. It does not modify QGIS, global Qt packages or another project’s environment. Installation needs an internet connection; subsequent app use is offline.

The equivalent macOS/Linux commands are:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --only-binary=:all: -r requirements-optional.txt
.venv/bin/python app.py
```

If a wheel is unavailable for your Python/platform combination, the core app remains usable. The timing row says that FLINT is unavailable rather than substituting an estimate. Official installation documentation: <https://python-flint.readthedocs.io/en/latest/install.html>. Python’s Tkinter documentation: <https://docs.python.org/3/library/tkinter.html>.

## A visual tour

| View | What to try | What it demonstrates |
|---|---|---|
| Maximal curves | Start with genus 2 and the default prime 1,000,039. Drag the surface. Scroll to the timing bars and play the chain. | Two incomplete prefixes from one pass; independent agreement with direct summation. |
| Maximal curves, large preset | Keep genus 2 and select 10⁹. Enable FLINT if available. | Prefixes containing hundreds of millions of terms, compared with a polynomial block product. Direct work is explicitly skipped at its cap. |
| Elliptic quarter | Start with p=13 or choose a larger preset. | A distinct elliptic family where the boundary is also cheap, giving both B and the original U. |
| p-adic lift | Keep p=13 and enable the Witt check. | A lifted coefficient, a failed naive sum formula, and the exact correction that repairs it. |
| Genus & timing | Sweep genus 1 through 6 near 10⁶, then change the target. | The practical price of carrying more coefficients and larger divisors. |

Scroll the results pane to see the complete explanation. The controls pane scrolls separately on smaller screens, while the Evaluate and Cancel controls remain accessible. Double-click a result-table row to view and copy its full integers. The surface is a connected topological schematic with tunnels; it is not a literal plot of finite-field points. Its genus agrees with the complex-curve analogy.

Changing the genus can make the current prime invalid. **Find prime ≥ this value** searches for a valid prime in the required congruence class. The app accepts primes below $2^{63}$ and offers genus 1 through 8. These are application limits, not limits of the theorem. Composite inputs and primes outside the supported family are rejected.

## What is proved, and what the app computes

Put $h=(p-1)/2$ and

$$
a_k=\binom{2k}{k}8^{-k},\qquad B_L=\sum_{k=0}^{L-1}a_k.
$$

The original block satisfies, modulo $p$,

$$
U_p(L)=4B_L-2L(2L+5)a_L.
$$

| Family | Hypotheses | Fast output in this app | Scope |
|---|---|---|---|
| Maximal hyperelliptic | $d=2g+1$, $p\equiv-1\pmod d$, $p>d$ | $B_{j(p+1)/d}$ for $1\le j\le g$ | One or all prefixes; does not supply the general boundary needed for U. |
| Elliptic quarter | $p\ge13$, $p\equiv1\pmod4$ | $B_n,a_n,U_p(n)$, $n=(p-1)/4$ | Includes Cornacchia/Gauss setup and the Miller pass. |
| p-adic coefficient | The same quarter family | Corrected geometric coefficient $\varepsilon\bmod p^2$ | A coefficient lift; no general fast sum modulo $p^2$ is claimed. |
| Witt correction check | Quarter family, $p\le199$ | Corrected $B_n\bmod p^2$, checked directly | Slow degree-$p$ series computation for understanding and verification. |

For the maximal family, the curve is

$$
C_d:\quad y^2=1-\frac{x^d}{2}.
$$

It is maximal over $\mathbb F_{p^2}$ and has zero Cartier/Hasse–Witt matrix. With $M=p+1$, $Q=(1,\sqrt2/2)$, and a Miller function having divisor $M(Q)-M(\infty)$, define its local coefficients at $(0,1)$ by

$$
A_r=M^{-1}[x^r]\frac{f'}{f}.
$$

The demonstrated evaluation is

$$
B_{j(p+1)/d}=-\left(\frac2p\right)\sqrt2\,(1+2A_{j-1})\pmod p.
$$

For fixed genus, the binary chain has logarithmic length. A conservative cost for the included Cantor arithmetic is $O(g^3\log p)$ field operations. Integer bit costs also depend on the size of $p$; a field operation is not a fixed-cost machine instruction. The geometry view carries no numerical approximation into the answers.

The p-adic tab retains an important counterexample:

$$
p=13,\quad n=3,\quad \varepsilon=25\pmod{169},\quad
B_3=70\pmod{169}.
$$

The naive lifted-boundary substitution gives $44$, not $70$. The separate Witt correction recovers $70$. The original $U_{13}(3)$ is $120$ modulo $169$ and also needs the harmonic correction described in the report. These are two different missing pieces; a lifted coefficient alone is insufficient.

## How to interpret timing comparisons

The app reports the median and observed range from the selected number of fresh runs, measured with `perf_counter_ns`. It times arithmetic setup and evaluation together. Prime validation, module imports, drawing and the explanatory replay are outside the timed interval. Products, factorials and final answers are not cached between samples.

The direct comparison uses a shared division-free recurrence and a final inversion per requested output. It is a stronger correctness reference than a loop performing a modular inversion for every term. The FLINT comparison uses polynomial block products and multipoint evaluation with roughly square-root dependence on prefix length. It is a conventional implementation, not the fully optimized Bostan–Gaudry–Schost algorithm.

In an all-prefix run, every comparison requests the same $g$ B values. The direct method shares one pass; Cartier–Miller carries $g$ coefficients in one pass; the FLINT baseline runs $g$ independent block products. It does not exploit every possible opportunity to share work between those block products. For a single-query comparison, turn off **Compute all g prefixes**.

FLINT uses compiled arithmetic, whereas the direct and Miller implementations use Python integers. Timings compare these specific implementations on your computer. They do not prove an optimal constant factor, a lower bound, or a general arbitrary-$L$ speedup. Small timings are noisy, and very small inputs can favour direct summation.

The genus sweep uses different nearby admissible primes and produces more outputs as genus rises. It illustrates practical cost; it is not a fixed-output genus-complexity experiment. Split-algebra restarts and different binary chains can make the curve nonmonotone. Operation counts are available in the exact JSON export.

The p-adic timing rows intentionally have different targets. The app labels them and suppresses speedup ratios. The Witt reference includes its local-series computation and its own direct cross-check. Timing the coefficient lift against a complete sum would otherwise make an unsupported claim.

Direct work has a selected term cap, polynomial blocks have a width cap of 30,000, the p-adic direct reference has a 100,000-term cap, and each task has a 120-second deadline. **Not run** means no timing exists. Cancel terminates the background worker; the previous complete result remains available.

## Reproducibility and files

**Export JSON** writes exact answers, settings, runtime details, timing samples and the chain replay. **Export CSV** writes one row per method with the exact output target and the reason for any skipped comparison. Both save locally to a location you choose. Large integers remain exact in JSON; spreadsheet programs may choose their own display formatting when opening CSV.

The `research` folder contains the elliptic, higher-genus and p-adic reports with proofs and literature references. `SOURCE_MANIFEST.json` identifies the original research scripts and their SHA-256 hashes. The arithmetic modules were copied unchanged apart from two relative-import adjustments. The GUI engine adds validation, output selection, timing and a separate trace replay.

The `validation` folder contains example measured runs from the development environment, explicitly historical rather than live app results. `VALIDATION.md` records the checks and their limits. Timings on other machines will differ. To rerun the exact reference tests:

```sh
python -m unittest discover -s tests -v
```

The optional graphical integration check is `python tests/gui_smoke.py`; it needs a display. Screenshots are optional and require Pillow only when `CM_SCREENSHOT_DIR` is set. Pillow is not an application dependency.

This is a research demonstration. The included reports distinguish elementary or known techniques from the specific observations developed in this project. No priority or peer-review claim is implied by the app’s name. A general fast $U_p(L)$ method, a general fast p-adic sum lift, and implications for decimal BBP extraction are not established here.

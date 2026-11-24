# Bala's bilateral logarithm conjecture and Hanna's constant identities

Haobo Ma (ChronoAI Pte Ltd, Singapore), then Wenlin Zhang (National University
of Singapore; ChronoAI Pte Ltd, Singapore). CC BY 4.0 (`cc-by-4.0`).

The note proves the identity already recorded in Paul D. Hanna's OEIS
A293380, revision 21, October 7, 2017, COMMENTS line 6, and posed by
Peter Bala in OEIS A292178, COMMENTS,
November 3, 2024 (revision 27), and A292179, COMMENTS, March 2, 2025
(revision 20), on the separate complex unit disks. The ordinary bilateral
expression requires a nonzero parameter `a`; its regular tails give the
continuous extension at zero. The same proof establishes the recorded
diagonal identity and the complementary formulas for the two constants.
It also proves the complementary formulas in A293381--A293384, with sums
`log(2)` and `log(3)`, and proves that both displayed iterations for
Hanna's zero in A293380 converge to the unique zero in `[1/2,3/5]`.
Its boundary corollary gives conditional two-tail and symmetric sums for
`|x|=1`, `x!=1`, `0<|a|<1`. The negative tail remains absolutely
convergent; the positive tail does not. At `x=1` the positive tail and
symmetric sums diverge; for `|x|>1` the positive terms do not tend to zero.
These boundary results are not posed in the two OEIS entries.

## Build

Use Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively use a LaTeX distribution containing `amsmath`, `amssymb`,
`amsthm`, `geometry`, `booktabs`, `array`, `lmodern`, and `hyperref`:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is included in `note.tex`; no BibTeX step or additional
scientific inputs are needed.

## Exact finite checks

Python 3.11 or newer, standard library only:

```sh
python3 verify.py --output reproduced-checks.json
cmp checks.json reproduced-checks.json
```

`checks.json` records 3,240 integer binomial-coefficient identities,
144 rational row expansions, 96 ordinary negative-index identities,
48 zero-parameter identities, and rational enclosures certifying 60
decimal places of each OEIS constant and of `log(2)`. It specifies the
finite ranges and exact rational error bounds. No floating-point
arithmetic or probabilistic tests are involved. Decimal prefixes are
truncated, not rounded. All rational endpoints are included explicitly.
It also checks the boundary row estimate at `x=-1,1`, with
`a=0,+/-1/2,+/-3/4`, for indices 1 through 40 (400 cases), and the
ordinary negative-index correspondence in the 320 nonzero-parameter
cases. These exact finite tests support the algebra of the written
boundary proof, not its infinite convergence conclusions.
For the off-diagonal pairs it checks 96 summand identities through index
24 and certifies 60 decimal places of all four constants and `log(3)`.
The positive-tail cutoffs are 220 for `(x,a)=(1/2,1/3)` and 400 for
`(2/3,1/2)`; both negative-tail cutoffs are 16. The same rational
majorants below apply. For Hanna's zero, 80 terms at each rational
bracket endpoint certify `0.5471802439661624 < r < 0.5471802439661625`.
Its omitted positive tail lies between zero and `2^(-80)/81`.

For `|x| <= r < 1`, `|a| <= t < 1`, the positive-tail remainder after `N`
terms is bounded by `rho^(N+1)/((N+1)*(1-rho))`, where
`rho = r + t^(N+1) < 1`. The negative-tail remainder obeys the same formula
with `rho = t^(N+1)/(1-r*t^(N+1)) < 1`. These inequalities follow from the
geometric majorants in the note. The positive constant uses `N=220`, the
negative constant `N=16`, and the logarithm Taylor sum `N=220`.

## Mathematical and formal scope

The complete written proof appears in `note.tex` and `note.pdf`, including
local uniform convergence. The finite checks support algebraic identities
and decimal illustrations, rather than the infinite-parameter theorem.

The pinned Lean declaration
`D5.S3.Analytic.PowerSeries.BalaBilateralLog.full_event` proves absolute
convergence, the principal-log identity, nonzero-integer term correspondence,
unordered and symmetric sums, the real specialization, and the unique
continuous zero extension. Its index `k` is `m-1` in the note.
Local uniform convergence, the diagonal and constant specializations,
Hanna's zero and iterations, and all boundary conclusions have written
proofs in the note. The declaration covers the open disks and the zero
extension, not the zero-iteration or boundary corollaries. The zero's
16-place bracket is certified by exact finite rational calculations.

Lean source:
https://github.com/the-omega-institute/trureturing/blob/4a7117cee792c7d5598d7f4770577d557fb45137/D5/S3/Analytic/PowerSeries/BalaBilateralLog.lean#L368

Posing sources:
https://oeis.org/A292178 and https://oeis.org/A292179.
The COMMENTS lines credit the conjecture to Peter Bala; Paul D. Hanna
authored the sequence entries and their original constant descriptions.

`metadata.json` gives the stable note identity, authors, license, problem
mapping and pinned formal source. `SHA256SUMS` lists the package files.

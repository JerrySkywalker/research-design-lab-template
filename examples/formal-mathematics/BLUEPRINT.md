# Blueprint — sums of odd natural numbers

This is a synthetic workflow example. The question is whether a sum defined by successive positive odd naturals has a simple closed form.

| Claim revision | Natural-language statement | Definitions and assumptions | Dependencies and formal name | Status and evidence |
| --- | --- | --- | --- | --- |
| ODD-SUM/r1 | Summing the first \(n\) positive odd naturals yields \(n^2\). | \(n\) ranges over naturals. The sum at zero is zero. At successor \(n+1\) add \(2n+1\). | The recursive definition is `FormalExample.oddSum`; the claim is `FormalExample.oddSum_eq_square`. | A proof candidate and [verification method](METHOD.md) are supplied. The run and reviewer fields belong in an explicit experiment record. |
| ODD-LINEAR/r1 | The same sum always equals \(n\). | Same definitions as ODD-SUM/r1. | `Drafts/FalseConjecture.lean` checks the counterexample at \(n=2\). | Rejected in this example. Retain the failed conjecture and counterexample; do not import drafts into the accepted library. |

The [statement lock](src/lean/review/StatementLock.lean) independently encodes the definition and theorem type. A change to either requires a new claim revision and review. A proof ref uses an exact Git commit and `src/lean/FormalExample/OddSum.lean` after specialization; retain old proof and lock revisions. A proof, axiom audit, statement review, evidence admission and Owner adoption each have separate status.

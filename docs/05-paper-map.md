# Paper map

[← Analysis and limitations](04-analysis-and-limitations.md) · [Overview](../README.md) · [Discussion and replication →](06-discussion-and-replication.md)

All links pin **arXiv:2609.35738v1**. Page numbers refer to one-based PDF pages, which match the printed paper pages. A page link opens the start of a section or relevant page; it does not isolate a table crop. Some PDF viewers may ignore the page fragment.

## Main text and appendices

| Paper location | PDF pages | What to look for | Companion route |
| --- | --- | --- | --- |
| Title, abstract, §1 Introduction | [1](https://arxiv.org/pdf/2609.35738v1#page=1)–2 | Full author list, contribution footnotes, learned adaptation motivation | [Concepts](01-concepts-and-context.md) |
| §2 Related work | [2](https://arxiv.org/pdf/2609.35738v1#page=2)–3 | Harness optimization and meta-learning framing | [Concepts](01-concepts-and-context.md#how-the-paper-positions-its-contribution) |
| §3 Preliminaries | [3](https://arxiv.org/pdf/2609.35738v1#page=3) | Harness definition, RLVR and GRPO, Eqs. 1–2 | [Method](02-method-and-protocols.md) |
| §4.1 Tasks, harnesses, execution feedback | [3](https://arxiv.org/pdf/2609.35738v1#page=3)–4 | Task unit, empirical quality, question sets, Eq. 3 | [Method](02-method-and-protocols.md) |
| §4.2 Adaptation and meta-learning objective | [4](https://arxiv.org/pdf/2609.35738v1#page=4) | Candidate application/selection and final-harness objective, Eqs. 4–5 | [Method](02-method-and-protocols.md) |
| §4.3 Training | [4](https://arxiv.org/pdf/2609.35738v1#page=4)–5 | Optional SFT, immediate reward, successive states, Eq. 6 | [Method](02-method-and-protocols.md) |
| §5.1 Setup | [5](https://arxiv.org/pdf/2609.35738v1#page=5)–6 | Two separately trained settings; Table 1 | [Results](03-results.md) |
| §5.2 Reasoning Gym | [6](https://arxiv.org/pdf/2609.35738v1#page=6)–7 | Transfer, teacher mean/oracle distinction, sequential revision | [Results](03-results.md) |
| §5.3 QA | [7](https://arxiv.org/pdf/2609.35738v1#page=7) | Unseen-benchmark transfer and proposal-budget caveat | [Results](03-results.md) |
| §5.4 Revision-sequence training | [7](https://arxiv.org/pdf/2609.35738v1#page=7) | Mixed multistep training gains | [Results](03-results.md) |
| §§6.1–6.3 Analysis and discussion | [7](https://arxiv.org/pdf/2609.35738v1#page=7)–9 | Reliability, harness structure, repeated revision explanations | [Analysis](04-analysis-and-limitations.md) |
| §7 Conclusion, limitations, acknowledgments | [9](https://arxiv.org/pdf/2609.35738v1#page=9) | Summary, bounded claims, funding and compute acknowledgments | [Limitations](04-analysis-and-limitations.md) |
| References | [10](https://arxiv.org/pdf/2609.35738v1#page=10)–13 | Original related-work citations | [Concepts](01-concepts-and-context.md) |
| A Extended related work | [14](https://arxiv.org/pdf/2609.35738v1#page=14)–15 | Contemporary learned editors, meta-learning, evaluation, continual learning | [Concepts](01-concepts-and-context.md) |
| B Reasoning Gym training/evaluation | [15](https://arxiv.org/pdf/2609.35738v1#page=15)–19 | B.1 evaluation; B.2 SFT; B.3 single-step RL; B.4 successive states | [Method](02-method-and-protocols.md) |
| C Additional Reasoning Gym results | [20](https://arxiv.org/pdf/2609.35738v1#page=20)–31 | C.1 single-step; C.2 multistep; C.3 variants; C.4 composition | [Results](03-results.md), [analysis](04-analysis-and-limitations.md) |
| D QA training/evaluation | [31](https://arxiv.org/pdf/2609.35738v1#page=31)–34 | D.1 data/retrieval; D.2 RL; D.3 multistep; D.4 independent proposals | [Method](02-method-and-protocols.md), [results](03-results.md) |
| E Implementation details | [35](https://arxiv.org/pdf/2609.35738v1#page=35) | Schematic editing interface, report content, composition directives | [Method](02-method-and-protocols.md) |
| F Limitations and future work | [36](https://arxiv.org/pdf/2609.35738v1#page=36) | Teacher dependence, tool-using proposer, joint training, longer horizons | [Limitations](04-analysis-and-limitations.md) |

## Figure index

These descriptions summarize the figures' purpose. Original paper figures are not redistributed.

| Figure | Page | Read it for |
| --- | --- | --- |
| 1 | [2](https://arxiv.org/pdf/2609.35738v1#page=2) | Proposer edits, fixed solver, feedback cycle, training-only policy update |
| 2 | [5](https://arxiv.org/pdf/2609.35738v1#page=5) | Candidate group scoring and GRPO; successive-state feedback |
| 3 | [6](https://arxiv.org/pdf/2609.35738v1#page=6) | Single-step Reasoning Gym means and held-out oracle best-of-eight |
| 4 | [7](https://arxiv.org/pdf/2609.35738v1#page=7) | Five-round OOD curves and proposal-budget comparison |
| 5 | [8](https://arxiv.org/pdf/2609.35738v1#page=8) | QA ten-round curves, four-run means, oracle comparisons |
| 6 | [9](https://arxiv.org/pdf/2609.35738v1#page=9) | Failure/zero-score rates, interpreter structures, composition audit, QA structure |
| 7 | [8](https://arxiv.org/pdf/2609.35738v1#page=8) | QA evidence rewiring: summaries guide search; passages reach answering |
| 8 | [19](https://arxiv.org/pdf/2609.35738v1#page=19) | RL training reward and reliability components |
| 9 | [20](https://arxiv.org/pdf/2609.35738v1#page=20) | Single-step revision by training exposure |
| 10 | [23](https://arxiv.org/pdf/2609.35738v1#page=23) | Aggregate revision curves on training and unseen families |
| 11 | [25](https://arxiv.org/pdf/2609.35738v1#page=25)–28 | Per-family development trajectories, original/additional sets, canonical/varied formats |
| 12 | [34](https://arxiv.org/pdf/2609.35738v1#page=34) | Seed QA workflow and evidence, third-hop, verification revisions |

## Table index

| Table | Page | Contents |
| --- | --- | --- |
| 1 | [6](https://arxiv.org/pdf/2609.35738v1#page=6) | Experimental settings and model families |
| 2 | [14](https://arxiv.org/pdf/2609.35738v1#page=14) | Contemporary learned harness methods, as characterized by authors |
| 3 | [16](https://arxiv.org/pdf/2609.35738v1#page=16) | Reasoning Gym instance counts, proposals, rounds, retry limits |
| 4 | [17](https://arxiv.org/pdf/2609.35738v1#page=17) | SFT/RL task-family lists |
| 5 | [17](https://arxiv.org/pdf/2609.35738v1#page=17) | Teacher data collection and SFT settings |
| 6 | [18](https://arxiv.org/pdf/2609.35738v1#page=18) | Single-step RL context pool |
| 7 | [18](https://arxiv.org/pdf/2609.35738v1#page=18) | Single-step RL and solver settings |
| 8 | [19](https://arxiv.org/pdf/2609.35738v1#page=19) | Offline successive-state training phases |
| 9 | [21](https://arxiv.org/pdf/2609.35738v1#page=21) | Family-level single-step mean / oracle best-of-eight |
| 10 | [22](https://arxiv.org/pdf/2609.35738v1#page=22) | Failed edits and zero-score proposals |
| 11 | [22](https://arxiv.org/pdf/2609.35738v1#page=22) | Failed-edit scoring sensitivity |
| 12 | [23](https://arxiv.org/pdf/2609.35738v1#page=23) | Selection criteria for extra multistep families |
| 13 | [23](https://arxiv.org/pdf/2609.35738v1#page=23) | Five-revision held-out aggregate scores |
| 14 | [24](https://arxiv.org/pdf/2609.35738v1#page=24) | Per-family development scores at rounds 1 and 5; canonical and format-varied panels |
| 15 | [29](https://arxiv.org/pdf/2609.35738v1#page=29) | Additional training variants |
| 16 | [30](https://arxiv.org/pdf/2609.35738v1#page=30) | Single-step and multistep scores for variants |
| 17 | [30](https://arxiv.org/pdf/2609.35738v1#page=30) | Structural and functional composition counts |
| 18 | [30](https://arxiv.org/pdf/2609.35738v1#page=30) | Scores with/without composition directives |
| 19 | [31](https://arxiv.org/pdf/2609.35738v1#page=31) | Composition-reward round-five development scores |
| 20 | [31](https://arxiv.org/pdf/2609.35738v1#page=31) | Inspected composition failure examples |
| 21 | [32](https://arxiv.org/pdf/2609.35738v1#page=32) | QA retrieval corpora, development/test pools and origins |
| 22 | [33](https://arxiv.org/pdf/2609.35738v1#page=33) | QA training and execution settings |
| 23 | [34](https://arxiv.org/pdf/2609.35738v1#page=34) | Independent QA proposal means, oracle metrics, >seed fraction, failures |

## Evidence navigation by question

- **Are test-time weights updated?** §4.2, p. 4.
- **Is the final-harness objective optimized directly?** §§4.2–4.3, pp. 4–5; §6.3, p. 9.
- **Which questions can the proposer see?** §4.1, pp. 3–4; B.1, pp. 15–16; D.2–D.3, pp. 32–33; E.2, p. 35.
- **What is behind 0.32 → 0.62?** §5.2, p. 6; B.1, p. 16; Table 9, p. 21.
- **Are total adaptation budgets matched?** §5.3, p. 7; D.4, pp. 33–34.
- **Do helpers actually contribute?** §6.2, p. 8; C.4, pp. 29–31.
- **Can a tool-using proposer inspect or test before editing?** This is proposed future work, not the current procedure; F, p. 36.

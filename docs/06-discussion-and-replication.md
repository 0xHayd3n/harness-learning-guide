# Discussion and replication checklist

[← Paper map](05-paper-map.md) · [Overview](../README.md)

This document contains **companion discussion prompts and planning guidance** grounded in the paper. It does not describe experiments performed by this repository. The authors' official code repository was marked “Code coming soon!” on 12 October 2026.

## Discussion prompts

1. **What has been learned?** Is the transferable object a generally useful editing skill, reliable code generation, specific workflow motifs, or a mixture? The reported transfer results establish utility under the studied protocols; they do not fully separate these mechanisms. [§§5–6, pp. 5–9](https://arxiv.org/pdf/2609.35738v1#page=5)
2. **Where does adaptation get its signal?** How much do explicit gold answers, grading, traces, and supporting-document feedback contribute? Could a weaker deployment signal support comparable revision? The current experiments use graded development feedback. [§4.1, pp. 3–4; E.2, p. 35](https://arxiv.org/pdf/2609.35738v1#page=35)
3. **What makes a comparison fair?** Which quantities should be matched: proposed edits, proposer tokens, solver calls, retrieval calls, number of graded instances, wall-clock time, or total cost? The paper explicitly leaves compute and feedback unmatched in its QA sequential/independent comparison. [§5.3, p. 7; D.4, pp. 33–34](https://arxiv.org/pdf/2609.35738v1#page=34)
4. **Why do longer training sequences have mixed value?** Does the local reward discourage temporarily worse edits with better long-term outcomes? This is a hypothesis; longer-horizon credit assignment is left open. [§4.3, p. 5; §6.3, p. 9](https://arxiv.org/pdf/2609.35738v1#page=9)
5. **Does structure imply function?** What would you need to establish that a generated helper materially improves an answer? The paper separates structural composition, a reward proxy for tool use, and audited functional contribution. [C.4, pp. 29–31](https://arxiv.org/pdf/2609.35738v1#page=29)
6. **How far does transfer go?** Would these revision skills survive a new solver, retrieval engine, feedback format, or long-horizon tool task? The paper fixes solvers and focuses on two settings, so these extensions require new evidence. [§7, p. 9; F, p. 36](https://arxiv.org/pdf/2609.35738v1#page=36)

## A worked reading exercise

**Question:** “Does the paper show that a 4B model is better than a 35B model?”

**Source-grounded answer:** on the selected 21-family single-step Reasoning Gym comparison, the trained 4B **proposer's revisions** have a higher mean score than the 35B teacher's revisions, about 0.62 vs 0.56. The teacher's oracle best-of-eight is higher, about 0.85 vs 0.83. Both outcomes concern revision policies, a fixed solver and a particular evaluation protocol. They do not establish general model superiority. [§5.2, p. 6; Table 9, p. 21](https://arxiv.org/pdf/2609.35738v1#page=21)

**Follow-up:** inspect Table 9 and B.1, then explain how failed edits, zero scores, and selected family subsets affect that statement.

## Planning a future replication

This checklist records questions to resolve before a separate implementation or study. It is not a ready-to-run reproduction recipe.

| Area | What a replication would need to preserve or clarify | Source |
| --- | --- | --- |
| Source version | Pin v1 and record any later changes | [Paper record](https://arxiv.org/abs/2609.35738v1) |
| Upstream code | Confirm whether the official implementation has been released; inspect its revision and license | [Official repo](https://github.com/AlvinZH04/Harness-Learning) |
| Models | Exact proposer/solver/teacher model IDs, checkpoints, thinking modes, decoding parameters and serving behavior | [B.2–B.3, pp. 17–18](https://arxiv.org/pdf/2609.35738v1#page=17), [Table 22, p. 33](https://arxiv.org/pdf/2609.35738v1#page=33) |
| Seeds and harnesses | Exact seed programs, callable interfaces, tool availability, parser and validity rules | [B.1, pp. 15–16](https://arxiv.org/pdf/2609.35738v1#page=15), [D.2–D.3, pp. 32–33](https://arxiv.org/pdf/2609.35738v1#page=32), [E, p. 35](https://arxiv.org/pdf/2609.35738v1#page=35) |
| SFT | Teacher draws, quality filters, accepted traces, task formats and deduplication | [B.2, p. 17](https://arxiv.org/pdf/2609.35738v1#page=17) |
| Rewards | Task score, validity bonuses, failure handling, and additional composition terms | [B.3, p. 18](https://arxiv.org/pdf/2609.35738v1#page=18), [C.4, pp. 29–31](https://arxiv.org/pdf/2609.35738v1#page=29), [D.2, p. 32](https://arxiv.org/pdf/2609.35738v1#page=32) |
| Training states | Context counts, task mixtures, checkpoint choice, offline refresh vs online chains | [B.3–B.4, pp. 18–19](https://arxiv.org/pdf/2609.35738v1#page=18), [D.2, p. 32](https://arxiv.org/pdf/2609.35738v1#page=32) |
| Split isolation | Feedback/scoring separation during training; held-out isolation at all times; inference-specific development reuse | [§4.1, pp. 3–4](https://arxiv.org/pdf/2609.35738v1#page=3), [B.1](https://arxiv.org/pdf/2609.35738v1#page=15), [D.3](https://arxiv.org/pdf/2609.35738v1#page=32) |
| Reasoning populations | Keep canonical/format-varied and 21-selected/all-26 unseen populations explicit | [B.1, p. 16](https://arxiv.org/pdf/2609.35738v1#page=16), [C.1–C.2, pp. 20–24](https://arxiv.org/pdf/2609.35738v1#page=20) |
| QA retrieval | Corpus construction, BM25 behavior, pool origin, alias normalization and question sampling | [D.1, pp. 31–32](https://arxiv.org/pdf/2609.35738v1#page=31) |
| Selection | RG strict improvement vs QA best candidate; oracle metrics reported separately | [B.1](https://arxiv.org/pdf/2609.35738v1#page=15), [D.3–D.4](https://arxiv.org/pdf/2609.35738v1#page=33) |
| Budgets | Proposals, feedback/scoring instances, solver/retrieval calls, tokens, elapsed time, total compute | [Tables 3/7/22](https://arxiv.org/pdf/2609.35738v1#page=16), [D.4, p. 34](https://arxiv.org/pdf/2609.35738v1#page=34) |
| Execution limits | Preserve setting-specific timeouts and response budgets; clarify differences in Table 22 and D.3 prose | [p. 33](https://arxiv.org/pdf/2609.35738v1#page=33) |
| Statistics | Failed attempts, repeated stochastic runs, uncertainty type, family aggregation and test-set size | [Figure 3](https://arxiv.org/pdf/2609.35738v1#page=6), [Figure 4](https://arxiv.org/pdf/2609.35738v1#page=7), [Tables 9–14](https://arxiv.org/pdf/2609.35738v1#page=21), [D.4](https://arxiv.org/pdf/2609.35738v1#page=34) |
| Functional audits | Trace whether helper outputs contribute, beyond helper presence or a tool-use reward proxy | [C.4, pp. 29–31](https://arxiv.org/pdf/2609.35738v1#page=29) |

Appendix E is a **schematic** interface description, not the complete production prompt. Do not fill in missing details and call them the authors' exact implementation.

## Proposed follow-up experiments

These are companion proposals, not results or author claims:

- Match total solver calls, proposer tokens, and graded-instance budgets when comparing independent and sequential revision.
- Evaluate feedback ablations: outcomes alone, traces without gold answers, supporting-document indicators, and unlabeled traces.
- Test transfer to changed solvers and tool interfaces, with the original training/evaluation separation preserved.
- Compare immediate rewards with explicit multi-round credit assignment.
- Audit functional helper contribution with controlled interface interventions.
- Expand to longer tool trajectories and report failure/recovery rates as well as final task scores.

The last two broad directions overlap with the paper's interface observations and future work; the proposed controls and experimental designs above are this companion's suggestions.

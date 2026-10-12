# Results and how to read them

This is an unofficial reading companion to *Harness Learning Enables Generalizable Test-Time Adaptation* by Alvin Zhang and colleagues. All experimental outcomes below are **reported by the paper**; this repository has not run the experiments or reproduced the implementation. Page links refer to [arXiv:2609.35738v1](https://arxiv.org/abs/2609.35738v1).

[Back to the README](../README.md) · [Previous: method and protocols](02-method-and-protocols.md) · [Next: analysis and limitations](04-analysis-and-limitations.md)

## Reading map

| Question | Start here | Primary source |
|---|---|---|
| Does training improve a typical revision on unseen tasks? | [Reasoning Gym single-step results](#reasoning-gym-single-step-results) | Section 5.2, Figure 3, Table 9 |
| Does repeating revision help? | [Reasoning Gym repeated revision](#reasoning-gym-repeated-revision) and [QA repeated revision](#qa-repeated-revision) | Figures 4 and 5, Appendices C.2 and D.3-D.4 |
| What does training on revision sequences add? | [Sequence-training results](#sequence-training-results) | Section 5.4, Appendix C.3 |
| What changes inside a harness? | [Reliability and structure](#reliability-and-structure) | Section 6, Figures 6-7 and 12, Tables 10 and 17-20 |
| Which comparisons need qualifications? | [Comparison checklist](#comparison-checklist) | Appendices B.1, C and D |

## Metrics and selection rules

**Reasoning Gym:** scores are benchmark grader credit, including partial credit. Single-step results score eight independent proposals on 75 held-out instances per family. Development feedback and multistep selection use a separate set of 25 instances. A sequential run makes one proposal per round for five rounds and retains it only when its development score improves. Failed edits and declared no-change responses retain the parent score under the main accounting rule; zero-scoring applied harnesses remain in the averages. See [Appendix B.1 and Table 3, pp. 15-16](https://arxiv.org/pdf/2609.35738v1#page=15).

**Multi-hop QA:** scores are normalized exact match (EM), with listed gold-answer aliases also accepted for MuSiQue and 2WikiMultihopQA. Four independent runs each perform ten rounds with eight candidates per round. In each round, six development questions provide traced feedback and 64 separate development questions score candidates. QA advances to the best candidate even if it scores below its parent; it keeps the parent only when all eight candidates fail. Held-out testing follows each round. See [Appendices D.1-D.3, pp. 31-33](https://arxiv.org/pdf/2609.35738v1#page=31).

**Oracle statistics:** best-of-eight, Oracle@8 and best-of-80 use held-out scores to choose candidates. They measure the quality of a candidate pool; they are not deployable selection rules. In QA, Oracle@8 is the expected maximum of eight proposals sampled without replacement from an 80-proposal pool. See [Table 1, p. 6](https://arxiv.org/pdf/2609.35738v1#page=6) and [Appendix D.4, p. 33](https://arxiv.org/pdf/2609.35738v1#page=33).

## Reasoning Gym single-step results

The main comparison covers **21 unseen task families** absent from both SFT and RL training. Each row below averages the same eight attempted proposals per family on 75 held-out instances. The best-of-eight column then averages the per-family oracle maximum. These are the rounded values in [Table 9, p. 21](https://arxiv.org/pdf/2609.35738v1#page=21).

| Proposer | Mean held-out score | Oracle best-of-eight score |
|---|---:|---:|
| Base | 0.32 | 0.63 |
| SFT | 0.49 | 0.78 |
| Single-step RL, reported checkpoint | 0.62 | 0.83 |
| 35B teacher | 0.56 | 0.85 |

The reported 4B proposer therefore improves average proposal quality from 0.32 to 0.62 after SFT followed by RL. Its mean exceeds the teacher's, while the teacher has the higher oracle best-of-eight score. The paper's claim concerns **revisions scored with a fixed solver**, not a general comparison of the proposer's and teacher's standalone problem-solving abilities. See [Section 5.2 and Figure 3, p. 6](https://arxiv.org/pdf/2609.35738v1#page=6).

The 21-family headline excludes `knight_swap`, `letter_jumble`, `modulo_grid`, `sokoban` and `ab`, which the paper describes as difficult for both the 4B proposers and the teacher to address with algorithmic harnesses. Including all **26** unseen families lowers the reported mean scores to Base 0.282, SFT 0.415, Single-step RL 0.528 and teacher 0.501. Improvement remains in these averages, but 0.62 is not the all-unseen-families result. See [Appendix B.1, p. 16](https://arxiv.org/pdf/2609.35738v1#page=16).

The aggregate is not uniform improvement on every family. For example, Table 9 reports mean single-step scores of 0.69 for SFT versus 0.58 for Single-step RL on `power_function`, and 0.32 versus 0.15 on `palindrome_partitioning`. Those examples are within the same unseen-family table and show why the full per-family source matters. See [Table 9, p. 21](https://arxiv.org/pdf/2609.35738v1#page=21).

## Reasoning Gym repeated revision

Figure 4 compares five sequential revisions with eight independent proposals on **15 shared unseen families**. On format-varied questions, Single-step RL obtains most of its gain in the first round; SFT improves more gradually. On canonical questions, their schedules are more similar. The retained sequential harness approaches or exceeds the oracle best of eight independent proposals while exceeding the independent average. Error bars represent one standard error across families. See [Figure 4 and Sections 5.2-5.4, p. 7](https://arxiv.org/pdf/2609.35738v1#page=7).

The expanded appendix evaluates 24 families per format, using different family lists for canonical and format-varied questions. It averages repeated runs within each family before aggregation; each added family has one run per method. The added families were partly selected using earlier single-step performance, so this is not an unrestricted random sample of unseen tasks. See [Appendix C.2 and Table 12, p. 23](https://arxiv.org/pdf/2609.35738v1#page=23).

| Proposer | Canonical: held-out score after five revisions | Format-varied: held-out score after five revisions |
|---|---:|---:|
| Base | 0.593 | 0.498 |
| SFT | 0.698 | 0.688 |
| Single-step RL | 0.699 | 0.725 |
| Multistep RL | 0.701 | 0.649 |

These are **held-out** scores from [Table 13, p. 23](https://arxiv.org/pdf/2609.35738v1#page=23), not the development scores in Table 14 or Figure 11. The paired gains over Base in Table 13 are 0.105 ± 0.030, 0.106 ± 0.044 and 0.109 ± 0.038 for the three trained proposers on canonical questions; their format-varied gains are 0.189 ± 0.058, 0.226 ± 0.051 and 0.150 ± 0.051. Each ± value is one standard error across families.

Figure 11 shows the retained harness's **development** score across rounds, including weakly improving or flat families such as `bf`, `propositional_logic` and `word_ladder` in the original canonical set. It also exposes format sensitivity: the SFT/Single-step RL ordering reverses on `caesar_cipher` between formats. These curves help diagnose variation; they should not be presented as independent held-out performance. See [Table 14, p. 24](https://arxiv.org/pdf/2609.35738v1#page=24) and [Figure 11, pp. 25-28](https://arxiv.org/pdf/2609.35738v1#page=25).

## QA independent revision

The QA proposer is trained on HotpotQA with RL from Base, without SFT. MuSiQue and 2WikiMultihopQA are unseen benchmarks. Their retrieval corpora and held-out question counts differ:

| Benchmark | Retrieval corpus in this experiment | Held-out questions |
|---|---|---:|
| HotpotQA | 5.23 million Wikipedia abstracts | 300 |
| MuSiQue | 21,100 pooled, deduplicated development-split paragraphs | 299 |
| 2WikiMultihopQA | 54,957 pooled, deduplicated development-split paragraphs | 300 |

Development and test questions are disjoint; HotpotQA subsets come from its training split, while the other two datasets are partitioned from their development splits. These are the paper's constructed evaluation sets, not scores on an official hidden benchmark test server. See [Appendix D.1 and Table 21, pp. 31-32](https://arxiv.org/pdf/2609.35738v1#page=31).

For each dataset and RL checkpoint, the independent evaluation generates 80 seed-harness revisions from four seed feedback reports, with 20 samples per report. Identical programs share execution, but all 80 proposal slots contribute. Failed parse/compile edits receive zero. See [Appendix D.4, p. 33](https://arxiv.org/pdf/2609.35738v1#page=33).

| Benchmark | Training | Seed EM | Mean EM | Oracle@8 | Oracle best-of-80 |
|---|---|---:|---:|---:|---:|
| HotpotQA | Single-step RL | 0.3900 | 0.4105 | 0.5399 | 0.5800 |
| HotpotQA | Multistep RL | 0.3900 | 0.4131 | 0.5209 | 0.5833 |
| MuSiQue | Single-step RL | 0.1438 | 0.1467 | 0.2126 | 0.2408 |
| MuSiQue | Multistep RL | 0.1438 | 0.1551 | 0.2034 | 0.2408 |
| 2WikiMultihopQA | Single-step RL | 0.2500 | 0.3090 | 0.4746 | 0.5200 |
| 2WikiMultihopQA | Multistep RL | 0.2500 | 0.2748 | 0.4374 | 0.5433 |

Values are from [Table 23, p. 34](https://arxiv.org/pdf/2609.35738v1#page=34). The same table reports proposal fractions strictly above the seed and failed-edit rates; it does not give a Base independent-proposal row.

## QA repeated revision

The paper reports that both RL proposers continue improving after the first revision and finish above Base on all three QA benchmarks. Base finishes below the seed on HotpotQA and MuSiQue. For Single-step RL on MuSiQue, the text contrasts roughly 0.15 independent mean EM with 0.27 after ten rounds. On both unseen benchmarks, the **average final run** for each RL proposer exceeds the held-out oracle best of 80 independent proposals. See [Section 5.3, p. 7](https://arxiv.org/pdf/2609.35738v1#page=7) and [Figure 5, p. 8](https://arxiv.org/pdf/2609.35738v1#page=8).

Read Figure 5's marks separately:

- Solid curves average four current harnesses, one per run, after each round.
- Dashed curves show the highest held-out score reached across all runs up to that round.
- Light bars average 80 independent proposals; dark bars average four runs' final harnesses.
- Circles and diamonds are independent-proposal oracles; triangles select the highest held-out score across all rounds and all runs.

Each sequential run consumes 80 proposals, matching the independent pool's proposal count. Reporting the mean of four runs involves **320 proposals in total**, and selecting the best across runs is not a matched-budget comparison with best-of-80. Sequential runs also receive feedback on intermediate harnesses, whereas independent proposals share four seed reports. The protocols do not match total compute or feedback. Seeds are measured separately for the independent and successive evaluations. See [Appendix D.4, pp. 33-34](https://arxiv.org/pdf/2609.35738v1#page=33).

## Sequence-training results

Training on successive revision states with immediate rewards does not consistently outperform training on individual revisions. Figure 4's Multistep RL point is above Single-step RL on canonical questions but below it on format-varied questions; QA final scores are nearly identical. This supports the narrower finding that individual-revision training can produce useful repeated revision, without establishing that sequence training never helps. See [Section 5.4, p. 7](https://arxiv.org/pdf/2609.35738v1#page=7).

A separate fixed later-round-state experiment reaches round-five **development** score 0.615 versus 0.660 for Single-step RL across twelve families, a paired difference of -0.045 ± 0.048. The authors find no evidence of a benefit from that state mixture. Their main Multistep RL procedure refreshes states between phases, so the fixed-state experiment is a separate configuration. See [Appendix C.3, p. 29](https://arxiv.org/pdf/2609.35738v1#page=29).

The harder-task variant improves some single-step scores but ends below Single-step RL after repeated revision on both development formats. It changes the training pool and reward together, and its nineteen-family evaluation includes training families. Composition-prompt RL also changes contexts and prompting. These are comparisons of complete configurations, not isolated causal tests of a reward term or of unseen-task transfer. See [Tables 15-16, pp. 29-30](https://arxiv.org/pdf/2609.35738v1#page=29).

## Reliability and structure

Training lowers the combined fraction of failed edits and zero-scoring harnesses. On the five-family unseen Reasoning Gym audit in Table 10, Base has 15 zero-scoring harnesses among 40 attempts; SFT has one failed edit and 13 zero-scoring harnesses among 40; Single-step RL has three zero-scoring harnesses and no failed edits among 40. The rounded combined rates are 38%, 35% and 8%. This audit is smaller than the 21-family headline evaluation. A recorded zero score does not by itself mean invalid code. See [Section 6.1, p. 7](https://arxiv.org/pdf/2609.35738v1#page=7), [Figure 6, p. 9](https://arxiv.org/pdf/2609.35738v1#page=9) and [Table 10, p. 22](https://arxiv.org/pdf/2609.35738v1#page=22).

Without a composition directive, interpreter loops dominate the unseen-family structure audit: 30 of 39 SFT harnesses and 31 of 40 Single-step RL harnesses. Under a helper directive, structural composition appears more often than functional composition: SFT has 11 structural and four functional cases among 24; Single-step RL has 12 structural and three functional cases among 32. These are separate audit groups, not stages of the same sample. See [Table 17, p. 30](https://arxiv.org/pdf/2609.35738v1#page=30).

For QA, Figure 6 audits retained harnesses across ten rounds and three benchmarks, with 120 per method. RL generally preserves multi-hop retrieval; Base sometimes reduces to a single solver call or removes the solver. The qualitative examples retain first-hop summaries for query formation but pass original retrieved passages to the answering call, add a third retrieval hop, or retrieve again when a draft answer is absent from current passages. These are observed adopted designs, not controlled ablations proving which edit caused each gain. See [Section 6.2 and Figure 7, p. 8](https://arxiv.org/pdf/2609.35738v1#page=8), [Figure 6, p. 9](https://arxiv.org/pdf/2609.35738v1#page=9) and [Figure 12, p. 34](https://arxiv.org/pdf/2609.35738v1#page=34).

## Comparison checklist

Before reusing a result, keep its method, family subset, question format, checkpoint, score split and selection rule together. Do not combine the 21-family headline, five-family reliability audit, nineteen-family sensitivity set and 24-family multistep sets as though they were one evaluation. Use the source table's full caption, and preserve distinctions between average quality, development-selected performance and held-out oracle selection. See [Appendix B.1, p. 16](https://arxiv.org/pdf/2609.35738v1#page=16), [Appendix C, pp. 20-31](https://arxiv.org/pdf/2609.35738v1#page=20) and [Appendix D, pp. 31-34](https://arxiv.org/pdf/2609.35738v1#page=31).

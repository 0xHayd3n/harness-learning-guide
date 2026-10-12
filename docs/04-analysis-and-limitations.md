# Analysis, limitations and open questions

This is an unofficial explanation of *Harness Learning Enables Generalizable Test-Time Adaptation*, [arXiv:2609.35738v1](https://arxiv.org/abs/2609.35738v1), by Alvin Zhang and colleagues. **Reported findings** describe the paper's experiments. **Companion interpretation** and **open questions** below are reading aids, not additional experimental results. This repository has not trained models, executed learned harnesses or reproduced scores.

[Back to the README](../README.md) · [Previous: results and protocols](03-results.md) · [Next: paper map](05-paper-map.md)

## What the evidence establishes

**Reported finding:** a trained proposer can generate better executable harness revisions for task families and QA benchmarks excluded from its training, with the solver fixed. Individual-revision training also supports repeated revision at test time. The paper reports this under its specified feedback, candidate-generation and scoring protocols. See [Sections 5.2-5.4, pp. 6-7](https://arxiv.org/pdf/2609.35738v1#page=6).

**Companion interpretation:** the useful transferable object is a revision policy: a mapping from the current executable workflow and execution feedback to an edit. The evidence is stronger than a single hand-built workflow succeeding on one task, because the same trained proposer produces changes across unseen tasks. It does not establish universal improvement for every task, solver, feedback source or inference budget. The method still depends on graded development feedback and on the solver and interface used in the experiments. See [Appendix B.1, pp. 15-16](https://arxiv.org/pdf/2609.35738v1#page=15) and [Appendix F, p. 36](https://arxiv.org/pdf/2609.35738v1#page=36).

## Reliability is broader than syntactic validity

**Reported finding:** training reduces the combined rate of failed edits and zero-scoring proposals. This helps provide more viable candidates for selection. The authors explicitly distinguish a failed edit, which yields no scorable harness, from an applied harness whose task score is zero. Zero credit alone does not show that the program is invalid. See [Section 6.1, p. 7](https://arxiv.org/pdf/2609.35738v1#page=7) and [Appendix C.1/Table 10, pp. 20-22](https://arxiv.org/pdf/2609.35738v1#page=20).

The training validity rewards also differ by setting:

| Setting | Reward-related validity definition | Reading consequence |
|---|---|---|
| Reasoning Gym | Separate credit for edit parsing, producing a usable candidate and the fraction of scoring trials that complete; task grader credit is added separately | A harness that completes all trials but answers incorrectly can receive 0.30 validity credit |
| QA | A candidate must have a Python code block that parses, defines `run`, has at most 200 lines and completes its scoring run to earn the 0.1 bonus; task exceptions or call-budget violations count as incorrect | The bonus and EM measure different properties; there is no separate partial-completion reward |

Definitions and coefficients are in [Appendix B.3, Eq. (8), p. 18](https://arxiv.org/pdf/2609.35738v1#page=18) and [Appendix D.2, Eq. (11), p. 32](https://arxiv.org/pdf/2609.35738v1#page=32). Neither training reward guarantees semantic correctness or broad generalization.

**Reported sensitivity check:** the nineteen-unseen-family comparison keeps Single-step RL above the teacher whether failed edits retain the seed score, receive zero or are excluded. However, removing zero-scoring applied harnesses conditions on success and can reverse that comparison. The main results include zeros. See [Appendix C.1 and Table 11, pp. 20-22](https://arxiv.org/pdf/2609.35738v1#page=20).

**Companion interpretation:** an agent summarizing this work should avoid converting a low failed/zero rate into a claim that all generated programs are correct. Report the numerator, denominator and score split, and keep validity, execution completion and task success distinct.

## Executable composition remains difficult

**Reported finding:** interpreter loops dominate the Reasoning Gym samples without a composition directive. These let the solver formulate code for the runtime to execute. The SFT corpus already contains many interpreter loops: 207 of 432 examples, or 48%. The paper's supervision comes from first-round revisions by a single teacher, and some collection prompts explicitly encourage tool use. See [Appendix B.2, p. 17](https://arxiv.org/pdf/2609.35738v1#page=17).

The composition audit separates **structural composition**, which places helper tools inside the solver's tool loop, from **functional composition**, which also requires a helper to contribute to the answer. Merely emitting a helper or a correct algorithm does not satisfy the functional criterion. See [Appendix B.1, p. 16](https://arxiv.org/pdf/2609.35738v1#page=16) and [Appendix C.4/Table 17, pp. 29-30](https://arxiv.org/pdf/2609.35738v1#page=29).

**Reported finding:** prompts and composition rewards do not give consistent performance gains. In the eleven-family held-out comparison, adding the composition directive lowers Single-step RL from 0.506 to 0.461, but raises Composition-prompt RL from 0.526 to 0.559. A guarded helper-with-fallback directive produces direct algorithmic solutions in 158 of 160 draws and no structurally or functionally composed harnesses. These outcomes show that requested structure and achieved structure differ. See [Tables 17-18, p. 30](https://arxiv.org/pdf/2609.35738v1#page=30) and [Appendix C.4, p. 31](https://arxiv.org/pdf/2609.35738v1#page=31).

Composition-reward probes likewise fail to show a consistent advantage. On twelve canonical families, round-five development scores are 0.660 for Single-step RL, 0.624 for the tool-use-reward checkpoint, and 0.624 or 0.630 for two combined-reward checkpoints. The authors warn that these probes do not isolate the reward terms. See [Table 19, p. 31](https://arxiv.org/pdf/2609.35738v1#page=31).

The inspected failures occur around correct helper algorithms: a parser misses the goal marker, answer extraction returns an unsolved grid, or a malformed tool message prevents the interaction. Examples include breadth-first search for maze, backtracking for sudoku and a primality sieve for `count_primes`. See [Section 6.2, p. 8](https://arxiv.org/pdf/2609.35738v1#page=8) and [Table 20, p. 31](https://arxiv.org/pdf/2609.35738v1#page=31).

**Companion interpretation:** a reusable component is useful only when the surrounding input, tool and output contracts allow it to affect the final answer. This is a plausible reason to study interface repair alongside algorithm generation, but the paper does not quantify the causal contribution of each interface failure to the overall performance gap.

## What the QA edits suggest

**Reported finding:** RL revisions commonly preserve multi-hop retrieval and change evidence flow. An answering call can read retrieved passages directly while first-hop summaries continue to guide the next query. Other adopted revisions add a third retrieval hop or use a draft answer as a new search query when it does not appear in retrieved passages. See [Section 6.2/Figure 7, p. 8](https://arxiv.org/pdf/2609.35738v1#page=8) and [Figure 12, p. 34](https://arxiv.org/pdf/2609.35738v1#page=34).

**Companion interpretation:** query formation and final answering may need different representations of evidence. Summaries can help construct the next search, while raw passages preserve details for answering. Figure 12 is an abridged depiction of observed designs, not an isolated experiment showing that raw passages, a third hop or the verification branch universally improve QA. A draft's presence in a passage also does not logically prove its correctness.

## Repeated revision and credit assignment

**Reported finding:** QA gains accumulate over more rounds than Reasoning Gym gains. The authors suggest that the QA seed offers several refinable workflow choices: retrieval depth, evidence access and search triggers. Reasoning Gym revisions commonly add interpreter loops, while composed helpers face interface obstacles. They explicitly state that different training and selection procedures prevent attributing the contrast solely to the seed harness. See [Section 6.3, pp. 8-9](https://arxiv.org/pdf/2609.35738v1#page=8).

**Reported finding:** QA Single-step RL trains on seed-harness contexts yet continues improving intermediate harnesses at test time. The authors interpret this as transfer to revision states beyond those seen in training. Training on revision sequences changes parent harnesses and reports, but each reward remains local to the immediate revision. See [Sections 5.4 and 6.3, pp. 7-9](https://arxiv.org/pdf/2609.35738v1#page=7).

**Open question identified by the authors:** would rewards that assign credit across rounds improve longer chains? The reported weak benefit from current sequence training does not answer that question. More diverse intermediate states or supervised demonstrations of successive revisions are other proposed directions. See [Section 6.3, p. 9](https://arxiv.org/pdf/2609.35738v1#page=9).

## Budgets, compute and evaluation limits

**Reported protocol limits:** the independent-versus-sequential comparisons change more than the order of proposals. Reasoning Gym uses eight independent proposals versus five sequential proposals, different branch prompting, and feedback from different parent harnesses. QA matches 80 proposals per individual chain, but four chains consume 320 proposals in total and receive intermediate-harness feedback. Candidate selection also differs across settings: Reasoning Gym requires development improvement; QA selects the best of eight even if it worsens the parent score. See [Appendix B.1, p. 16](https://arxiv.org/pdf/2609.35738v1#page=16) and [Appendices D.3-D.4, pp. 32-34](https://arxiv.org/pdf/2609.35738v1#page=32).

Execution budgets are substantial and setting-specific. Reasoning Gym permits up to three generation attempts per proposal, a 32,768-token response budget per evaluation attempt, and a 300-second timeout per RL scoring trial. QA permits 12 solver calls and 12 retrievals per question; its solver response allowance is 2,048 tokens. Appendix D.3 specifies a 600-second scoring-run limit and a 1,800-second test-run limit for QA evaluation, while the RL settings in Table 22 list a 900-second scoring-run timeout. Preserve this source distinction instead of collapsing it into one timeout. These are configured limits, not measured average usage or cost. See [Table 3, p. 16](https://arxiv.org/pdf/2609.35738v1#page=16), [Table 7, p. 18](https://arxiv.org/pdf/2609.35738v1#page=18) and [Table 22/Appendix D.3, p. 33](https://arxiv.org/pdf/2609.35738v1#page=33).

**Companion interpretation:** the reported comparisons support effective adaptation under the stated protocols. They do not establish lower dollar cost, lower latency, fewer solver tokens or equal total execution work. The paper explicitly leaves compute and feedback unmatched for the QA independent/sequential comparison. Model parameter counts alone do not supply a compute or cost comparison. See [Section 5.3, p. 7](https://arxiv.org/pdf/2609.35738v1#page=7).

Family selection and score definitions also restrict conclusions. The main Reasoning Gym headline excludes five difficult unseen families; the added multistep families were partly selected by earlier performance; the harder-task nineteen-family set mixes seen and unseen tasks. QA uses constructed held-out subsets and different retrieval corpus sizes across benchmarks. Best-of-N or best-run marks that use test scores are descriptive oracles, not deployable development selection. See [Appendix B.1, p. 16](https://arxiv.org/pdf/2609.35738v1#page=16), [Appendix C.2, p. 23](https://arxiv.org/pdf/2609.35738v1#page=23), [Appendix C.3, p. 29](https://arxiv.org/pdf/2609.35738v1#page=29) and [Appendix D, pp. 31-34](https://arxiv.org/pdf/2609.35738v1#page=31).

## Representation and training scope

**Reported limitations:** training uses prescribed revision prompts, externally generated execution reports, a fixed solver and, for Reasoning Gym SFT, one teacher. The proposer does not select its own code-inspection or execution actions before submitting an edit. The study therefore trains revision generation within a prescribed interface, rather than an unrestricted investigative agent. See [Section 7, p. 9](https://arxiv.org/pdf/2609.35738v1#page=9) and [Appendix F, p. 36](https://arxiv.org/pdf/2609.35738v1#page=36).

The representation is executable Python subject to entry-point, parsing, execution and budget requirements. Reasoning Gym uses structured SEARCH/REPLACE edits; QA expects a code block defining `run` with a line limit. The schematic prompt in Appendix E is explicitly not the complete production prompt. Learned behavior should be understood within these interfaces and the demonstrated task settings. See [Appendix D.2, p. 32](https://arxiv.org/pdf/2609.35738v1#page=32) and [Appendix E, p. 35](https://arxiv.org/pdf/2609.35738v1#page=35).

**Open questions identified by the authors:** stronger teachers and richer multistep demonstrations; initialization with prior harness-design expertise; a proposer that investigates with tools and tests before editing; joint proposer/solver training; and transfer to longer tool-use trajectories and changing solvers. The experiments do not establish outcomes for those extensions. See [Appendix F, p. 36](https://arxiv.org/pdf/2609.35738v1#page=36).

## Questions for a follow-up study

These are **companion questions**, not results or claims attributed to the authors:

1. Under matched feedback questions, solver calls, tokens and wall time, how much of the repeated-revision advantage remains?
2. Does training transfer across solver models, tool interfaces and tasks with sparse or unavailable graded development feedback?
3. Can targeted interface-repair training improve functional composition without sacrificing task score?
4. How does sequence-level credit assignment compare with immediate rewards under the same state distribution?
5. What changes when all unseen families are included and extra families are selected independently of prior method performance?

Use these questions to organize reading or design future evaluation. No such evaluation has been performed in this repository.

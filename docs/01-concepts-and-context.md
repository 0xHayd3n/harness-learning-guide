# Concepts and context

[← Overview](../README.md) · [Next: method and protocols →](02-method-and-protocols.md)

This is an authored explanation of paper §§1–3 and Appendix A. Research claims belong to Zhang et al.; conceptual examples below are labeled as companion illustrations.

## What changes when an agent adapts?

A model's parameters determine its learned behavior. A harness determines how that behavior is invoked: what enters a prompt, which tools are available, how many calls occur, and how observations are carried into later calls. A workflow can therefore improve even when the underlying solver model does not change. [§1, p. 1; §3.1, p. 3](https://arxiv.org/pdf/2609.35738v1#page=1)

**Companion illustration:** a question-answering workflow might first summarize retrieved passages and then answer from those summaries. Editing the harness so the final call can read the original passages changes the available evidence. That edit does not require changing model weights. This illustration is motivated by the paper's observed QA revisions, discussed in [§6.2 and Figure 7, p. 8](https://arxiv.org/pdf/2609.35738v1#page=8); it is not executable code or a reproduced experiment.

The paper asks whether a proposer can **learn how to revise** these programs from execution feedback and transfer that revision ability to new task families. Training experience is used to improve a reusable adaptation procedure. The procedure then operates on a new task's harness and development feedback. [§§1, 4, pp. 1–5](https://arxiv.org/pdf/2609.35738v1#page=1)

## Inner loop and outer loop

| Loop | Adapted object | Signal | When model weights change |
| --- | --- | --- | --- |
| Inner loop | Executable harness | Execution report and candidate scores | Neither proposer nor solver is updated at test time |
| Outer loop | Proposer parameters | Rewards from candidate harness execution; optional teacher demonstrations | Proposer updates during training; solver remains fixed |

The analogy to gradient-based meta-learning is about roles: a code revision acts as an adaptation step. It is not a claim that editing code is differentiable or equivalent to gradient descent. The implemented update uses immediate revision reward as a surrogate for the final-harness meta-learning objective. [§4.2, p. 4; §4.3, p. 5](https://arxiv.org/pdf/2609.35738v1#page=4)

## What counts as a task?

The task is the unit over which a harness is adapted. In Reasoning Gym it is a family, such as maze or sudoku, containing multiple generated questions and a grader. In QA it is a benchmark, such as HotpotQA. A question is one instance within the task. [§4.1, p. 3](https://arxiv.org/pdf/2609.35738v1#page=3)

This matters for “generalization.” The authors hold out entire Reasoning Gym families from proposer SFT and RL, and hold out entire QA benchmarks from QA training. They also evaluate on questions separate from adaptation feedback and selection. These are two distinct kinds of separation: unseen task distributions and unseen questions within an adapted task. [§5.1, pp. 5–6; B.1, pp. 15–16; D, pp. 32–34](https://arxiv.org/pdf/2609.35738v1#page=5)

The base models' pretraining data are not established as free of all benchmark-related material by these splits. “Unseen” in this paper refers to proposer adaptation training, not proof that no model has ever encountered the task.

## Glossary

| Term | Meaning in this paper | Common reading trap |
| --- | --- | --- |
| Harness | Executable program organizing solver calls, tools, and information flow | Treating it as only a system prompt |
| Solver | Fixed model used to answer task questions through the harness | Assuming the solver learns during adaptation |
| Proposer | Model producing edits from a task, harness, and execution report | Assuming it directly answers each task question |
| Seed | Initial unrevised harness | Confusing it with the Base proposer |
| Base | Pre-training proposer used to generate revisions | Comparing Base revisions with a raw solver without checking the seed |
| SFT | Supervised fine-tuning on filtered successful teacher revisions | Assuming the QA setting also uses SFT |
| Single-step RL | Training configuration using individual revision contexts | Assuming inference must stop after one round |
| Multistep RL | Training using successive revision states with immediate rewards | Assuming full-chain credit assignment |
| Development feedback | Graded examples and traces used to guide adaptation | Assuming label-free feedback |
| Held-out score | Score on questions excluded from adaptation feedback and selection | Confusing it with development selection |
| Oracle best-of-N | Highest held-out score among N proposals, for analysis | Treating it as a deployable selection rule |
| Format-varied questions | Alternative presentations of the same underlying Reasoning Gym tasks | Treating them as entirely different task families |
| Structural composition | Generated helpers placed in the solver tool loop | Assuming the helpers actually affect the answer |
| Functional composition | A helper contributes to the final answer | Treating helper presence alone as success |
| Exact match / EM | QA answer metric under the paper's normalization | Interchanging it with Reasoning Gym's graded mean score |

Sources: [§§3–5, pp. 3–7](https://arxiv.org/pdf/2609.35738v1#page=3), [§6.2, p. 8](https://arxiv.org/pdf/2609.35738v1#page=8), [C.4, pp. 29–31](https://arxiv.org/pdf/2609.35738v1#page=29).

## How the paper positions its contribution

The authors situate the work among workflow optimization, learned harness editors, meta-learning, and agent self-improvement. Their emphasis is a learned revision rule that transfers to task families or benchmarks excluded from training and remains useful over successive adaptation states. [§2, pp. 2–3; Appendix A, pp. 14–15](https://arxiv.org/pdf/2609.35738v1#page=14)

| Comparison axis | Paper's framing |
| --- | --- |
| Harness search vs learned adaptation | Train the revision policy using outcomes, rather than only search for a task-specific program |
| Output refinement vs program revision | Change the executable orchestration used across questions, rather than only one answer |
| Memory-based adaptation vs harness adaptation | Revise control flow, interfaces, and context construction as the adapted object |
| Joint harness/weight optimization | Keep the solver fixed here, isolating gains from proposer training and harness changes |
| Same-benchmark splits vs task transfer | Evaluate entire excluded reasoning families and unseen QA benchmarks |

Appendix A contrasts Harness-R1, JIT-Agent, and Ornith and discusses many broader systems. Those comparisons are the paper authors' characterization, not an independent review of each related work by this companion. Consult the original related papers before asserting priority, superiority, or an exhaustive distinction. [Table 2 and Appendix A, pp. 14–15](https://arxiv.org/pdf/2609.35738v1#page=14)

## Three questions to carry into the results

1. Does a trained proposer produce better average revisions, including failed attempts?
2. Does repeated execution feedback lead to gains beyond independent edits of the seed?
3. Does training on successive revision states improve those gains, with budgets and selection rules accounted for?

These mirror the experimental questions in [§5, p. 5](https://arxiv.org/pdf/2609.35738v1#page=5). Read [method and protocols](02-method-and-protocols.md) before comparing curves or best-of-N values.

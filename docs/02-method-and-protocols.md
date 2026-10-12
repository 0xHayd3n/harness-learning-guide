# Method and experimental protocols

> Unofficial reading notes for **Harness Learning Enables Generalizable Test-Time Adaptation** by Alvin Zhang, Xuecheng Liu, Zixuan Wang, Fahim Tajwar, Daman Arora, Ruslan Salakhutdinov, Daniel Khashabi, Yuda Song, and Andrea Zanette. These are authored explanations of arXiv:2609.35738v1, not implementation documentation or a reproduction. The experiments and settings below are reported by the paper; this repository has not run them.

[Repository overview](../README.md) · [Canonical paper](https://arxiv.org/abs/2609.35738v1) · [Official code repository](https://github.com/AlvinZH04/Harness-Learning), marked “Code coming soon!” on 2026-10-12.

[Previous: concepts and context](01-concepts-and-context.md) · [Next: results](03-results.md) · [Paper map](05-paper-map.md)

## Reading map

- [Objects and notation](#objects-and-notation)
- [The adaptation loop](#the-adaptation-loop)
- [What training optimizes](#what-training-optimizes)
- [Question separation](#question-separation)
- [Reasoning Gym protocol](#reasoning-gym-protocol)
- [Multi-hop QA protocol](#multi-hop-qa-protocol)
- [Revision interfaces and execution reports](#revision-interfaces-and-execution-reports)
- [How to interpret the protocol](#how-to-interpret-the-protocol)

Source locators use the **PDF page number in v1**, followed by a section, equation, figure, or table. PDF `#page=` links depend on the viewer; use the stated page number if the browser ignores the fragment.

## Objects and notation

A **harness** is executable orchestration around a language model: it builds contexts, decides when to call the model, executes tools, passes observations back, and extracts an answer. A **solver** answers questions through that harness. A separate **proposer** reads the current harness and its execution feedback, then proposes a code revision. The solver stays fixed during training. At test time, both models stay fixed; the harness source changes. Figure 1 depicts that separation, including a policy-update arrow used only during training. [Source: §3.1 and §4, p. 3; Figure 1, p. 2.](https://arxiv.org/pdf/2609.35738v1#page=2)

| Symbol | Meaning |
| --- | --- |
| $h_0$ | Seed harness before adaptation |
| $h_{t-1}$, $h_t$ | Current harness before round $t$, and the harness retained after that round |
| $q$, $Q$ | One question, and a finite question set |
| $\operatorname{score}(h,q)$ | Observed grader credit in $[0,1]$ after executing $h$ on $q$ |
| $J(h;Q)$ | Mean observed question score for harness $h$ |
| $\pi_\theta$ | Proposer policy, with learned parameters $\theta$ |
| $x_t$ | Revision context: task description, parent source, execution report, and sometimes prior-round information |
| $y_i$ | One proposer response, including its proposed code change |
| $h'_i$ | Candidate harness obtained by applying response $y_i$ to the parent |
| $G$ | Candidate responses sampled within one revision context |
| $T$ | Number of test-time revision rounds |
| $Q^{\mathrm{fb}}$ | Questions used to build the proposer's feedback report |
| $Q^{\mathrm{score}}$ | Questions used to score revisions and select a candidate |
| $Q^{\mathrm{eval}}$ | Held-out questions used to measure performance |
| $v_i$ | Auxiliary reward for validity and execution |

The paper's empirical harness score is

$$
J(h;Q)=\frac{1}{|Q|}\sum_{q\in Q}\operatorname{score}(h,q). \tag{3}
$$

This measures an execution, rather than a deterministic intrinsic property of the program: stochastic solver sampling can change the result. A task is the **unit of adaptation**, not necessarily a single question. It is a Reasoning Gym family, such as maze or sudoku, or a QA benchmark, such as HotpotQA. [Source: §4.1, Eq. (3), pp. 3-4.](https://arxiv.org/pdf/2609.35738v1#page=3)

## The adaptation loop

For each round, the current harness runs on feedback questions, producing the report included in $x_t$. The proposer samples candidate changes, applies them to the same parent, and selection uses the scoring questions:

$$
\begin{aligned}
y_i &\sim \pi_\theta(\cdot\mid x_t), && i=1,\ldots,G,\\
h'_i &= \operatorname{Apply}(h_{t-1},y_i),\\
h_t &= \operatorname{Select}\!\left(h_{t-1},\{h'_i\}_{i=1}^{G};Q_t^{\mathrm{score}}\right).
\end{aligned} \tag{4}
$$

`Apply` can reject a response when its edits cannot be parsed or applied. `Select` includes protocol-specific validity and retention rules. It is not universally “replace the parent only if better”: that rule belongs to the Reasoning Gym evaluation, while QA has a different rule. Executing the retained harness supplies feedback for the next round. [Source: §4.2, Eq. (4), p. 4.](https://arxiv.org/pdf/2609.35738v1#page=4)

**Authored conceptual outline, not runnable code:**

```text
start with the benchmark's seed harness
repeat for the specified number of rounds:
    execute the current harness on feedback questions
    construct the revision input from source, task, and report
    sample the configured number of proposer responses
    apply/validate each response and score its candidate
    retain a harness using that benchmark's selection rule
measure the retained harness on questions hidden from adaptation
```

Training changes proposer weights; inference changes executable harness code. “Single-step RL” and “Multistep RL” name **training configurations**. Either trained proposer can be applied for one revision or repeatedly at inference. Figure 2 adds a return path through refreshed execution reports for training on successive states; the reward-to-GRPO path still scores each candidate's immediate outcome. [Source: §4.3 and Figure 2, p. 5.](https://arxiv.org/pdf/2609.35738v1#page=5)

## What training optimizes

The meta-learning goal is high held-out performance after the entire adaptation loop:

$$
\max_\theta\;\mathbb{E}\left[J(h_T;Q^{\mathrm{eval}})\right]. \tag{5}
$$

The implemented training signal is a **local surrogate**: each revision receives credit from its own scoring performance and auxiliary validity reward,

$$
r_i=J(h'_i;Q^{\mathrm{score}})+v_i. \tag{6}
$$

Training on later revision states changes the contexts the proposer encounters, but it retains this immediate-reward objective. Thus “meta-learning” describes learning the adaptation procedure; it does not imply that training directly optimizes a whole revision sequence's terminal score or assigns long-horizon credit to earlier edits. [Source: §4.2-4.3, Eqs. (5)-(6), pp. 4-5.](https://arxiv.org/pdf/2609.35738v1#page=4)

### GRPO in this paper

The general verifiable-reward objective is an expectation over revision inputs and sampled responses:

$$
\mathcal{J}(\theta)=\mathbb{E}_{x\sim\mathcal D}\mathbb{E}_{y\sim\pi_\theta(\cdot\mid x)}[r(x,y)]. \tag{1}
$$

GRPO compares the $G$ responses to **the same input**, with group-normalized advantages

$$
\widehat A_i=\frac{r_i-\operatorname{mean}_j r_j}{\operatorname{std}_j r_j+\delta},
\qquad
\omega_{i,k}(\theta)=\frac{\pi_\theta(y_{i,k}\mid x,y_{i,<k})}{\pi_{\theta_{\mathrm{old}}}(y_{i,k}\mid x,y_{i,<k})}.
$$

Its clipped surrogate sums token terms and normalizes by the total response-token count in the group:

$$
\mathcal J(\theta)=\mathbb E_{x\sim\mathcal D}\mathbb E_{\{y_i\}\sim\pi_{\theta_{\mathrm{old}}}(\cdot\mid x)}\left[
\frac{1}{\sum_{j=1}^{G}|y_j|}\sum_{i=1}^{G}\sum_{k=1}^{|y_i|}
\min\!\left(\omega_{i,k}(\theta)\widehat A_i,
\operatorname{clip}(\omega_{i,k}(\theta),1-\epsilon,1+\epsilon)\widehat A_i\right)
\right]. \tag{2}
$$

Each token of a response shares that response's advantage. This is not an advantage computed separately for each tool call or each successive revision round. The two benchmark configurations have different auxiliary rewards and KL settings, detailed below. [Source: §3.2, Eqs. (1)-(2), p. 3; §4.3, p. 5.](https://arxiv.org/pdf/2609.35738v1#page=3)

## Question separation

The roles of feedback, scoring, and evaluation questions matter more than their names:

| Setting | Feedback versus scoring | Held-out evaluation |
| --- | --- | --- |
| RL training, both settings | Disjoint within each context; candidates share the context's scoring questions | The outer goal concerns held-out performance, while the updates use immediate scoring reward |
| Reasoning Gym adaptation | The same 25 development questions serve feedback and selection | 75 questions per family; hidden from the proposer |
| QA adaptation | Six feedback questions per run; 64 scoring questions shared across four runs, disjoint from all feedback questions in that round | Full test set after each round; test questions disjoint from development and training questions |

At QA inference, development questions may recur **across** rounds. Disjoint feedback and scoring **within** a round does not mean every round draws globally unused questions. At Reasoning Gym inference, fresh feedback means a new execution report from the retained program; it does not imply a newly drawn development set. [Source: §4.1-4.3, pp. 3-5; Appendix B.1, pp. 15-16; Appendix D.1-D.3, pp. 31-33.](https://arxiv.org/pdf/2609.35738v1#page=32)

## Reasoning Gym protocol

### Evaluation and retention

The seed makes one solver call and extracts the answer. A separate fixed tool-loop baseline permits Python execution for up to five turns. Single-step evaluation draws eight independent seed revisions. Multistep evaluation uses five rounds and one proposal per round, preserving the parent unless the candidate's development score strictly improves:

$$
h_t^*=\begin{cases}
h'_t,&J(h'_t;Q^{\mathrm{dev}})>J(h_{t-1}^*;Q^{\mathrm{dev}}),\\
h_{t-1}^*,&\text{otherwise}.
\end{cases} \tag{7}
$$

Each proposal has up to three generation attempts, with 32,768 response tokens per attempt. Edits are parsed from the final answer. Rejected edits can receive error feedback and retry within the budget. Failed edits and declared no-change proposals retain the parent's score; executable harnesses that score zero still count. The seed itself does not count as a proposal. Single-step best-of-eight selects on held-out score and is an oracle statistic, whereas multistep retention uses development score. [Source: Appendix B.1, Table 3 and Eq. (7), pp. 15-16.](https://arxiv.org/pdf/2609.35738v1#page=16)

Unseen families exclude all families used in either training stage. The main single-step figures use 21 unseen families and exclude five difficult families: `knight_swap`, `letter_jumble`, `modulo_grid`, `sokoban`, and `ab`. Results over all 26 unseen families appear in the appendix; do not treat the 21-family figure mean as the all-family mean. Aggregate uncertainty is one standard error across families, after averaging repeated runs within each family. [Source: Appendix B.1, p. 16; Table 9.](https://arxiv.org/pdf/2609.35738v1#page=16)

### Supervised initialization

Reasoning Gym uses Qwen3.5-4B for proposer and frozen solver. Its SFT stage collects first-round revisions from a Qwen3.6-35B-A3B teacher over 21 families; RL uses five families. The SFT collection usually uses 25 development questions, but generates 16 for `largest_island` and `tsumego`, includes up to eight failed examples, and samples eight teacher proposals per context. The final corpus has 432 accepted revisions. [Source: Table 1, p. 6; Appendix B.2, Tables 4-5, p. 17.](https://arxiv.org/pdf/2609.35738v1#page=17)

A candidate must reach at least the larger of **seed score plus 0.08** and **0.40**, and pass screens for answer echoing, duplicate code, and output-interface violations. Claude Opus 5 reviewers re-execute surviving candidates on development, held-out, and format-varied questions to inspect oracle access, memorization, and grader exploitation. The paper states that held-out question text does not enter the corpus. These quality-review executions should not be confused with exposing held-out questions in proposer training inputs. [Source: Appendix B.2, p. 17.](https://arxiv.org/pdf/2609.35738v1#page=17)

The teacher completions, including reasoning, edits, and manifests, are retained verbatim in accepted examples. LoRA uses rank 32 and scaling 32, targets attention and MLP projections including gated-delta-net projections, and trains with a 32,768-token context, learning rate $10^{-4}$, cosine decay, and 10% warmup. Batch size is one with four accumulation steps. Four-fold family-disjoint cross-validation selects duration; final full-corpus training lasts about 2.9 epochs before adapter merging. The corpus contains 207 interpreter loops (48%), and only first-round revisions from one teacher, limiting its diversity of successive-revision examples. [Source: Appendix B.2, Table 5, p. 17.](https://arxiv.org/pdf/2609.35738v1#page=17)

### Single-step RL

The fixed training pool has 640 contexts: 200 each for `tower_of_hanoi` and `codeio` (100 seed parents plus 100 stronger parents each), 100 each for `rotten_oranges` and `simple_geometry`, and 40 seed-parent contexts for `maze`. Feedback and reward draws use disjoint seeds within the same family. [Source: Appendix B.3, Table 6, p. 18.](https://arxiv.org/pdf/2609.35738v1#page=18)

The validity reward is

$$
v_i=0.05\,\mathbf 1[y_i\text{ parses}]
+0.10\,\mathbf 1[h'_i\ne\bot]
+0.15\,\rho_{\mathrm{run}}(h'_i), \tag{8}
$$

where $\bot$ denotes an invalid candidate and $\rho_{\mathrm{run}}$ is the fraction of scoring trials that complete. A fully valid candidate that completes every trial but gets every answer wrong earns **0.30 validity reward**, before task credit. Failed edits earn only validity credit accumulated before failure. Explicit no-change responses execute and score the parent. Training reward must therefore not be reported as accuracy. [Source: Appendix B.3, Eq. (8), p. 18.](https://arxiv.org/pdf/2609.35738v1#page=18)

| Single-step RL setting | Reported value |
| --- | --- |
| Initialization | SFT checkpoint |
| Candidates/context; contexts/update | 8; 40 |
| Learning rate; updates per sampled batch | $10^{-6}$; 1 |
| Duration | One pass over 640 contexts, 16 updates |
| Reported checkpoint | Update 10; “later” means update 16 |
| KL penalty; entropy bonus | None; none |
| Proposer temperature | 0.6 |
| Prompt/response budgets | 12,288 / 16,384 tokens |
| Solver | Frozen Qwen3.5-4B, non-thinking; temperature 0.7 |
| Solver response allowance | Minimum configured budget of 32,768 tokens |
| Scoring questions/context | 25, with partial credit |
| Scoring-trial timeout | 300 seconds |

The paper uses asynchronous vLLM revision sampling, executes candidates with the frozen solver, and applies one token-averaged, group-relative policy update per sampled batch. [Source: Appendix B.3, Table 7, p. 18.](https://arxiv.org/pdf/2609.35738v1#page=18)

### Training on successive states

Multistep RL starts from the reported update-10 Single-step RL checkpoint. It first trains for nine updates on 62 stored parent harnesses with room to improve. State refresh advances a parent when its best sampled revision improves by at least 0.01, rescores states on the same 25 development questions, and retains states at least 0.10 below their family's best score. The second phase trains for 15 updates on 246 filtered states, mostly from earlier revision runs; its final checkpoint is Multistep RL. Each state's report contains outcome counts and up to eight failing instances, and each revision has the full response budget. This is offline state refresh between phases, rather than the online QA sequence construction. [Source: Appendix B.4, Table 8, pp. 18-19.](https://arxiv.org/pdf/2609.35738v1#page=19)

## Multi-hop QA protocol

### Data and grading

HotpotQA training uses 2,000 questions, with disjoint 500-question development and 300-question test sets, all sampled from its training split. Retrieval uses 5.23 million full-wiki Wikipedia abstracts. MuSiQue and 2WikiMultihopQA are unseen benchmark evaluations: their development splits are partitioned into separate development and held-out sets, stratified by hop count or question type. Retrieval pools combine supplied support and distractor paragraphs and deduplicate by title and text. [Source: Appendix D.1, pp. 31-32.](https://arxiv.org/pdf/2609.35738v1#page=32)

| Benchmark | Retrieval corpus | Development pool | Held-out test |
| --- | --- | ---: | ---: |
| HotpotQA | 5.23M Wikipedia abstracts | 500 | 300 |
| MuSiQue | 21,100 pooled paragraphs | 500 | 299 |
| 2WikiMultihopQA | 54,957 pooled paragraphs | 500 | 300 |

HotpotQA uses normalized exact match, removing differences in case, punctuation, articles, and whitespace. The other two evaluations also accept listed gold-answer aliases, following the official 2WikiMultihopQA script. [Source: Appendix D.1, Table 21, p. 32.](https://arxiv.org/pdf/2609.35738v1#page=32)

### RL training

QA starts RL directly from base Qwen3-4B with thinking enabled, without teacher SFT. The solver is frozen Qwen3-8B with thinking disabled. Each context gets six feedback questions and 64 disjoint scoring questions from the 2,000-question training pool; all eight candidates share its scoring questions. The proposer supplies a diagnosis followed by a Python code block. A valid candidate must parse, define `run`, have at most 200 lines, and complete the scoring run. Its reward is exact match plus 0.1; otherwise reward is zero. Per-question exceptions or exhausted call budgets count as incorrect within the mean, without Reasoning Gym's separate partial-completion reward. [Source: Appendix D.2, Eq. (11), p. 32.](https://arxiv.org/pdf/2609.35738v1#page=32)

Single-step RL uses the seed parent in all 320 contexts. Multistep RL uses 32 online revision runs, each visited ten times; when revisited, its best scoring candidate becomes the parent, unless no candidate executes. Both use 80 updates, four contexts per update, eight candidates per context, and report update 80. Their other settings match, so this training comparison targets the source of parent states. [Source: Appendix D.2 and Table 22, pp. 32-33.](https://arxiv.org/pdf/2609.35738v1#page=33)

| QA RL setting | Reported value |
| --- | --- |
| Learning rate; updates per sampled batch | $10^{-6}$; 1 |
| Clip ratio; loss | 0.2; token-mean |
| KL-to-reference coefficient; entropy bonus | $10^{-3}$; none |
| Proposer temperature; top-p | 1.0; 1.0 |
| Training prompt/response budgets | 10,240 / 8,192 tokens |
| Solver temperature; top-p; top-k | 0.6; 0.95; 20 |
| Solver response/context allowance | 2,048 / 16,384 tokens |
| Per-question call budgets | 12 solver calls; 12 retrievals |
| Table 22 timeouts | 120 seconds/solver call; 900 seconds/scoring run |

[Source: Appendix D.2, Table 22, p. 33.](https://arxiv.org/pdf/2609.35738v1#page=33)

### Successive and independent evaluation

All benchmarks start from the same two-hop retrieve-and-summarize seed. Four independent runs each perform ten rounds, with eight candidates per round. Each run gets six development feedback questions; 64 scoring questions are shared across the four runs and disjoint from all that round's feedback questions. Random draws are seeded by round so all proposers see the same questions. The retained harness is the candidate with the highest scoring exact match **even if it scores below the parent**. Only when all eight candidates fail does the run keep the parent. The full test set measures all four retained harnesses after each round; their mean is the principal curve. [Source: Appendix D.3, pp. 32-33.](https://arxiv.org/pdf/2609.35738v1#page=33)

Appendix D.3's inference prose specifies a 10,240-token proposer response budget, 600 seconds per scoring run, and 1,800 seconds per test run; retrieval returns at most 20 passages. Keep these labeled as evaluation settings. Table 22 lists an 8,192-token training response budget and a 900-second scoring-run timeout, while describing solver execution settings as shared. The notes preserve the table and evaluation-prose values separately rather than resolve the timeout wording without released implementation evidence. [Source: Table 22 and Appendix D.3, p. 33.](https://arxiv.org/pdf/2609.35738v1#page=33)

Independent evaluation samples 80 seed revisions per benchmark and checkpoint: 20 from each of the four round-one reports. Every proposal contributes, including failed edits scored zero; identical programs share an execution. Oracle@8 is the expected highest held-out score from eight samples drawn without replacement from this pool; best-of-80 is its maximum. Both select using test outcomes and are oracle measures, not deployable selection rules. One ten-round run also consumes 80 candidates, but the reported four-run mean and best-run summary use **320 total candidates**. Comparing the best of four runs to best-of-80 does not match total proposal budget. [Source: Appendix D.4, pp. 33-34.](https://arxiv.org/pdf/2609.35738v1#page=34)

## Revision interfaces and execution reports

Appendix E.1 provides a **schematic**, not the complete production prompt. For structured revision, inputs contain the task/configuration, source, development score, and report. The response identifies source spans through `SEARCH/REPLACE` edits, preserves the entry point, explains expected repairs and regressions, and includes a change manifest. It must declare no change explicitly when appropriate. Invalid responses get parsing or validation feedback and can retry within the Reasoning Gym attempt budget. [Source: Appendix E.1, p. 35; Appendix B.1, p. 16.](https://arxiv.org/pdf/2609.35738v1#page=35)

Do not infer that QA uses that exact patch syntax. Appendix D.2 describes QA responses as a short diagnosis followed by one Python code block defining `run`. The Reasoning Gym SFT collection instead describes a harness exposing `solve(model, question)`. These are setting-specific contracts, not interchangeable API entry points. [Source: Appendix B.2, p. 17; Appendix D.2, p. 32.](https://arxiv.org/pdf/2609.35738v1#page=32)

| Report context | Information described in the paper |
| --- | --- |
| Reasoning Gym revision | Development scores, instance outcomes, failed-example trace excerpts, changes since earlier revisions, retained-harness history |
| Successive-state training, schematic description | Up to $K$ passing and $K$ failing examples; each includes question, harness answer, expected answer, outcome |
| QA revision | Six feedback questions, solver/retrieval traces, answer correctness, gold answers, supporting documents retrieved or missed |

The specific Reasoning Gym training description gives up to eight failing examples; Appendix E's schematic uses $K$ without fixing a universal value. Gold answers and correctness labels appear in **development/training feedback**. This is graded adaptation, rather than adaptation using only unlabeled traces. [Source: Appendix B.4, p. 19; Appendix E.2, p. 35; Appendix D.2-D.3, p. 32.](https://arxiv.org/pdf/2609.35738v1#page=35)

Independent proposals start from the same parent and report within a comparison, with a branch instruction steering proposals toward different failure mechanisms. Sequential proposals get new feedback from retained harnesses. Appendix B.1 also notes that independent evaluations regenerate seed reports, while sequential runs share a fixed initial report. Consequently, comparisons change more than whether feedback is refreshed: parent source, selection, prompting, and budgets also matter. [Source: Appendix B.1, p. 16; Appendix E.2, p. 35.](https://arxiv.org/pdf/2609.35738v1#page=16)

Composition directives ask for reusable helpers integrated into the solver's tool loop; a more restrictive version asks for task-specific helpers instead of a generic interpreter, with answer checks. A request for that architecture is not proof that a harness achieves it. **Structural composition** requires integrating helpers into the solver loop; **functional composition** additionally requires a helper to contribute to the answer. The paper audits those separately. [Source: Appendix B.1, p. 16; Appendix E.3, p. 35; Appendix C.4, pp. 29-31.](https://arxiv.org/pdf/2609.35738v1#page=35)

## How to interpret the protocol

The following are reading implications, not new experimental findings:

- **Greedy training leaves a horizon gap.** A locally useful edit is rewarded; a temporary loss that could enable later gains is not directly credited through the stated objective. QA's willingness to advance below the parent changes selection, but does not turn its training reward into a terminal-sequence objective.
- **Development monotonicity does not guarantee test monotonicity.** Reasoning Gym's retention inequality concerns development score; stochastic execution and generalization can make held-out scores move differently.
- **Validity reward is part of the learning signal.** A reward increase can reflect better parsing or completion, so accuracy and reward need separate labels.
- **“More revisions” is a protocol-level result.** Independent and sequential comparisons also change source programs, feedback placement, selection rules, prompting, or aggregate proposal budgets.
- **This is feedback-guided program adaptation.** It requires a grader and development feedback in the studied settings; evidence here does not establish adaptation without that information.

These implications follow from the objectives and protocols above. The authors also identify limitations: one-teacher first-round Reasoning Gym supervision, prescribed prompts and externally generated reports instead of a proposer choosing its own investigation steps, and a solver that remains fixed rather than jointly trained with the proposer. Joint learning and longer tool-use horizons are future directions. [Source: §4.2-4.3, pp. 4-5; Appendix B.1-B.3, pp. 16-18; Appendix D.3-D.4, pp. 32-34; Appendix F, p. 36.](https://arxiv.org/pdf/2609.35738v1#page=36)

For an agent extracting these notes, preserve five fields with every result: **benchmark/family subset**, **question split**, **selection rule**, **candidate budget**, and **reported versus inferred status**. Read the cited primary passage before using a setting as a reproduction specification; Appendix E alone is not a complete production interface.

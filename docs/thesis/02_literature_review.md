# Chapter 2 — Literature Review

---

## 2.0 Introduction

This chapter surveys the state of the art across five domains that converge in the Chirality architecture: AI agent architectures, LLM reliability and hallucination, formal methods and safety-critical systems engineering, professional engineering regulation, and epistemic frameworks. Each section establishes the current frontier of its domain and identifies a specific gap that the Chirality architecture addresses. The chapter concludes with a synthesis that positions the five gaps as facets of a single unaddressed problem: the absence of an architecturally enforced governance framework for LLM-based agent systems in regulated professional practice.

The literature review serves a dual purpose. First, it demonstrates that the five contributions claimed by this thesis (Chapter 1) are novel — that they address gaps not filled by existing work. Second, it provides the theoretical foundation for the architectural decisions presented in Chapters 3 through 7: the epistemic architecture draws on provenance theory (§2.5) and hallucination research (§2.2); the invariant system draws on formal methods (§2.3); the regulatory mapping draws on professional practice standards (§2.4); and the agent type hierarchy draws on multi-agent systems research (§2.1).

---



---

## 2.1 AI Agent Architectures and Multi-Agent Systems

The field of LLM-based autonomous agents has advanced rapidly since 2022, producing a body of work focused on what agents can do: reason, plan, use tools, delegate, and collaborate. This section surveys the foundational patterns, multi-agent frameworks, and alignment techniques that constitute the current state of the art, and identifies the governance gap that motivates the Chirality architecture.

### 2.1.1 Foundation Agent Patterns

**Chain-of-thought prompting** established the enabling substrate for agentic reasoning. Wei et al. demonstrated that prompting large language models with intermediate reasoning steps — a chain of thought — substantially improves performance on arithmetic, commonsense, and symbolic reasoning tasks [1]. Crucially, this capability emerges as a function of model scale rather than explicit training and requires only few-shot in-context examples. For the Chirality architecture, chain-of-thought is the reasoning mode employed by agents operating within the ANALYST and AUDITOR tiers; the architecture inherits its inferential power while layering structural constraints that chain-of-thought alone does not provide.

**ReAct** (Reasoning + Acting) extended this pattern into an action loop. Yao et al. introduced an agent paradigm in which a language model interleaves reasoning traces with action calls against external tools or environments [2]. In evaluation on HotpotQA and FEVER, ReAct outperformed pure chain-of-thought by grounding reasoning in retrieved evidence, reducing hallucination and error propagation. On interactive decision-making benchmarks (ALFWorld, WebShop), ReAct surpassed imitation and reinforcement learning baselines by an absolute margin of 34% and 10% respectively. The architecture directly influences Chirality's deterministic tool interface design: agents reason about what to invoke, invoke it, and receive structured results — but the ReAct paper specifies no constraints on what tools may be invoked, what side-effects are permissible, or what authority boundaries govern the action space.

**Toolformer** demonstrated that models can autonomously learn when and how to call external APIs. Schick et al. trained a model in a self-supervised manner to decide which of a fixed set of APIs to call, when to call them, what arguments to pass, and how to incorporate results into subsequent generation [3]. Toolformer achieved competitive zero-shot performance across diverse downstream tasks without sacrificing core language modelling ability. The work is relevant to Chirality's TOOLMAKER subsystem, which provides deterministic, auditable tool implementations. However, Toolformer treats tool invocation as a capability to be maximised; it does not define a scope boundary separating read-only from write-capable tools, nor does it specify authority conditions under which writes are permissible.

### 2.1.2 Multi-Agent Frameworks

**AutoGen** provided the first widely adopted framework for multi-agent conversation patterns. Wu et al. introduced conversable agents and conversation programming, enabling developers to compose LLM applications from autonomous or human-proxy agents that communicate through structured message sequences [4]. AutoGen demonstrated effectiveness across mathematics, code generation, question answering, and operations research. The framework introduces role separation — a natural precursor to the tiered authority model in Chirality — but assigns roles for task specialisation rather than for governance. No invariant constraints prevent one AutoGen agent from overriding another's output, and no write-scope quarantine governs which agents may emit side-effecting actions.

**MetaGPT** embedded software engineering workflows into multi-agent collaboration. Hong et al. encoded Standardized Operating Procedures (SOPs) into prompt sequences, assigning agents to specialised roles — product manager, architect, engineer, QA — corresponding to human organisational structures [5]. On software engineering benchmarks, MetaGPT produced more coherent, executable solutions than prior chat-based multi-agent systems. The use of SOPs as a structuring mechanism is conceptually related to Chirality's invariant contracts; however, MetaGPT's SOPs are task-workflow constraints rather than governance invariants. They define process steps but not epistemic obligations (what claims must be attributed), authority boundaries (what an agent must not do), or escalation gates (under what conditions a human principal must approve).

**LangGraph** provides low-level orchestration infrastructure for stateful, multi-actor LLM workflows. Developed by LangChain Inc., LangGraph represents agent workflows as directed graphs with explicit state, conditional edges, and persistent memory [6]. LangGraph enables human-in-the-loop integration and supports cyclical, iterative workflows that pure chain-of-thought pipelines cannot represent. Its graph model is relevant to Chirality's ORCHESTRATOR coordination layer. LangGraph, however, is an orchestration substrate: it provides no normative layer specifying what state transitions are impermissible, which actors hold write authority, or how evidence must be linked to outputs.

**Wang et al.** provided a comprehensive taxonomy of LLM-based autonomous agents, organising the literature around the construction of agent modules (memory, planning, tools) and their application across social simulation, software engineering, and science domains [7]. This survey is used in the present thesis as a reference taxonomy for classifying Chirality's architectural components against the broader literature.

### 2.1.3 Generative Agent Societies

Park et al. introduced generative agents — computational agents built on an LLM core augmented with a memory stream, reflection mechanism, and daily planning module — and demonstrated their deployment in a 25-agent simulated town environment [8]. Agents autonomously organised social events, formed relationships, and exhibited emergent coordination behaviours from only a small number of authored initial conditions. The memory architecture — storing full experience history as natural language, synthesising higher-level reflections over time, and retrieving relevant context dynamically — informs Chirality's MEMORY subsystem design. The Park et al. work is significant for establishing that complex, temporally extended agent behaviour is achievable without hard-coded scripts. It does not, however, address governance: agents in the simulated town are unconstrained in what they write to shared memory, have no authority hierarchy, and emit no provenance records linking their outputs to source observations.

### 2.1.4 Principle-Based Alignment

Bai et al. introduced Constitutional AI (CAI), a training methodology that reduces harmful outputs through a self-critique loop guided by a written constitution — a set of principles encoded as natural language rules [9]. The model generates candidate responses, critiques them against constitutional principles, revises them, and is then trained via reinforcement learning from AI feedback (RLAIF) rather than human feedback. CAI achieved comparably harmless behaviour to human-feedback-trained models while reducing evasive responses and relaxing the tension between helpfulness and harmlessness. The constitutional metaphor directly influenced Chirality's design vocabulary: the architecture's invariant contracts are a constitutional layer specifying what agents MUST NOT do. The key architectural difference is scope — CAI applies principles at training time to shape output distributions, while Chirality applies contracts at runtime as hard structural constraints on agent authority and epistemic obligations, independently of how any individual model was trained.

### 2.1.5 Hierarchical Agent Architectures

Several frameworks have explored hierarchical organisation as a mechanism for managing complexity in multi-agent systems. The Self-Organised Agents (SoA) framework employs a mother–child delegation pattern in which high-level agents decompose tasks and assign subtasks to specialised child agents [see survey in 10]. Research on multi-agent resilience has found that hierarchical topologies exhibit lower performance degradation under faulty agent conditions (5.5% drop) compared to decentralised structures (23.7% drop), suggesting that layered authority confers robustness properties [10]. Shavit et al. identified baseline governance obligations for agentic AI systems including minimal footprint, preference reversibility, and human check-in at task boundaries [11].

These hierarchical models establish the structural feasibility of tiered agent authority — a foundation on which Chirality builds. However, none of the surveyed frameworks formalise the authority relationship as a typed invariant. Tiers are assigned for task specialisation or fault tolerance; they do not enforce write-scope quarantine, require gate-controlled human approval for authority escalation, or mandate that agents provide evidence structures tying every output claim to a retrievable source.

### 2.1.6 Gap: Capability Without Governability

The literature surveyed above represents the most capable class of LLM-based agent systems currently available. These systems have demonstrated strong performance on knowledge retrieval, code generation, collaborative problem solving, and simulated social behaviour. The defining characteristic of this body of work is that it optimises for capability — defining and expanding what agents *can* do.

No published architecture provides a formal governance layer that specifies what agents *must not* do and what evidence they *must* provide. Specifically, the following structural properties are absent from the surveyed literature:

1. **Invariant contracts**: formally specified, runtime-enforced constraints on agent action independent of model weights or prompt content.
2. **Write-scope quarantine**: a typed boundary separating read-only from write-capable operations, enforced at the architectural level rather than through prompting.
3. **Gate-controlled human authority**: a formal mechanism requiring human principal approval for operations above a defined authority threshold, rather than optional human-in-the-loop hooks.
4. **Epistemic transparency obligations**: a structural requirement that every output claim carry provenance metadata — source, confidence class, and derivation path — rather than relying on population-level accuracy of the underlying model.

The Chirality architecture is designed to fill this gap: to provide not a more capable agent system, but a governable one.

---

### References — Section 2.1

[1] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. H. Chi, Q. V. Le, and D. Zhou, "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 35, New Orleans, LA, USA, 2022. [Online]. Available: https://arxiv.org/abs/2201.11903

[2] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao, "ReAct: Synergizing Reasoning and Acting in Language Models," in *Proc. 11th Int. Conf. Learning Representations (ICLR)*, Kigali, Rwanda, 2023. [Online]. Available: https://arxiv.org/abs/2210.03629

[3] T. Schick, J. Dwivedi-Yu, R. Dessì, R. Raileanu, M. Lomeli, L. Zettlemoyer, N. Cancedda, and T. Scialom, "Toolformer: Language Models Can Teach Themselves to Use Tools," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 36, New Orleans, LA, USA, 2023. [Online]. Available: https://arxiv.org/abs/2302.04761

[4] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Li, E. Zhu, L. Jiang, X. Zhang, S. Zhang, J. Liu, A. H. Awadallah, R. W. White, D. Burger, and C. Wang, "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation," *arXiv preprint arXiv:2308.08155*, 2023. [Online]. Available: https://arxiv.org/abs/2308.08155

[5] S. Hong, M. Zhuge, J. Chen, X. Zheng, Y. Cheng, C. Zhang, J. Wang, Z. Wang, S. K. S. Yau, Z. Lin, L. Zhou, C. Ran, L. Xiao, C. Wu, and J. Schmidhuber, "MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework," in *Proc. 12th Int. Conf. Learning Representations (ICLR)*, Vienna, Austria, 2024. [Online]. Available: https://arxiv.org/abs/2308.00352

[6] LangChain Inc., "LangGraph: Build Resilient Language Agents as Graphs," open-source software library, 2024. [Online]. Available: https://github.com/langchain-ai/langgraph

[7] L. Wang, C. Ma, X. Feng, Z. Zhang, H. Yang, J. Zhang, Z. Chen, J. Tang, X. Chen, Y. Lin, W. X. Zhao, Z. Wei, and J.-R. Wen, "A Survey on Large Language Model based Autonomous Agents," *Frontiers of Computer Science*, vol. 18, no. 6, 2024. doi: 10.1007/s11704-024-40231-1. [Online]. Available: https://arxiv.org/abs/2308.11432

[8] J. S. Park, J. C. O'Brien, C. J. Cai, M. R. Morris, P. Liang, and M. S. Bernstein, "Generative Agents: Interactive Simulacra of Human Behavior," in *Proc. 36th ACM Symp. User Interface Software and Technology (UIST)*, San Francisco, CA, USA, 2023, pp. 1–22. doi: 10.1145/3586183.3606763

[9] Y. Bai, S. Jones, K. Ndousse, A. Askell, A. Chen, N. DasSarma, D. Drain, S. Fort, D. Ganguli, T. Henighan, et al., "Constitutional AI: Harmlessness from AI Feedback," *arXiv preprint arXiv:2212.08073*, 2022. [Online]. Available: https://arxiv.org/abs/2212.08073

[10] L. Huang, Y. Yu, W. Ma, W. Zhong, Z. Feng, H. Wang, Q. Chen, W. Peng, X. Feng, B. Qin, and T. Liu, "A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions," *ACM Transactions on Information Systems*, 2024. doi: 10.1145/3703155. [Online]. Available: https://arxiv.org/abs/2311.05232

[11] Y. Shavit, S. Agarwal, et al., "Practices for Governing Agentic AI Systems," OpenAI Technical Report, Dec. 2023. [Online]. Available: https://cdn.openai.com/papers/practices-for-governing-agentic-ai-systems.pdf

---

## 2.2 LLM Reliability, Hallucination, and Trustworthiness

A parallel stream of research has examined the reliability properties of large language models — specifically their tendency to generate content that is plausible in form but incorrect in fact. This section surveys the hallucination literature, trustworthiness frameworks, and mitigation approaches, and identifies the per-claim transparency gap that motivates Chirality's epistemic architecture.

### 2.2.1 Hallucination: Definition and Taxonomy

The term "hallucination" in NLG refers to generated content that is unfaithful to a source document or unsupported by verifiable fact. Ji et al. published the first comprehensive survey of hallucination across NLG tasks, covering abstractive summarisation, dialogue generation, question answering, data-to-text generation, and machine translation [12]. The survey defined hallucination along two axes — intrinsic (contradicting source material) versus extrinsic (introducing information absent from source) — and reviewed metrics, mitigation methods, and open problems. Published in *ACM Computing Surveys* in 2023, this work established hallucination as a first-class reliability concern rather than an edge case, and remains the primary definitional reference in the field.

Huang et al. extended the taxonomy to the LLM era specifically, distinguishing factuality hallucination (claims unsupported by world knowledge) from faithfulness hallucination (claims inconsistent with provided context) [13]. The survey documented that all major commercial LLMs at time of writing produced hallucinated content at measurable rates, proposed a structured taxonomy of contributing causes, and surveyed detection and mitigation methods. Published initially as arXiv:2311.05232 and subsequently in *ACM Transactions on Information Systems*, this work is directly relevant to Chirality's design premise: if hallucination is a structural property of current LLM generation, then an architecture deploying LLM agents in professional engineering contexts must treat every model output as epistemically uncertain by default.

Maynez et al. provided early empirical grounding for faithfulness failures in abstractive summarisation, demonstrating through large-scale human evaluation that all tested neural summarisation models produced substantial hallucinated content [14]. Critically, the work showed that standard metrics such as ROUGE do not capture faithfulness, and that textual entailment measures correlate more strongly with human faithfulness judgements. This finding motivates Chirality's epistemic labelling requirement: output quality cannot be assessed from surface form alone; provenance and grounding must be made structurally explicit.

### 2.2.2 Factuality Evaluation

Min et al. introduced FActScore, a fine-grained factuality metric that decomposes long-form model generation into atomic facts and measures the proportion supported by a reliable external knowledge source [15]. Evaluated on biographies generated by InstructGPT, ChatGPT, and PerplexityAI, FActScore found that even state-of-the-art commercial models supported only 58% of their atomic claims when independently verified. The automated FActScore pipeline — extract, retrieve, verify — achieved less than 2% error relative to human annotation. FActScore represents the most rigorous post-hoc factuality evaluation methodology available at the time of writing. Its architecture — decompose into atoms, retrieve evidence, verify each — is conceptually related to Chirality's provenance requirement, but inverted in temporal direction: FActScore verifies after generation; Chirality requires provenance to be attached at generation time as a structural obligation rather than a retrospective audit.

### 2.2.3 Alignment and Mitigation Approaches

**Reinforcement Learning from Human Feedback (RLHF)** established the dominant paradigm for aligning LLM behaviour with human preferences. Ouyang et al. trained InstructGPT through a three-stage pipeline: supervised fine-tuning on human demonstrations, reward model training on human preference rankings, and PPO-based reinforcement learning against the reward model [16]. InstructGPT (1.3B parameters) was preferred over GPT-3 (175B parameters) in human evaluations, demonstrating that alignment quality is not determined by parameter count alone. RLHF addresses hallucination by shaping the model's prior toward preferred (typically more truthful) outputs at training time. This is a population-level intervention: it reduces the expected rate of hallucination across a distribution of prompts but provides no guarantee for any individual output, and offers no runtime mechanism for a downstream system to determine whether a specific claim is grounded.

**Retrieval-Augmented Generation (RAG)** addressed factuality by grounding generation in retrieved external documents. Lewis et al. proposed a hybrid architecture combining a pre-trained seq2seq model with a dense retrieval component over a non-parametric document index [17]. On knowledge-intensive NLP tasks, RAG models outperformed purely parametric models and produced more specific, diverse, and factual outputs. RAG is the closest architectural precursor to Chirality's sourcing requirement: it mandates that generation be grounded in retrieved material rather than parametric memory alone. However, standard RAG architectures do not enforce that retrieved sources be cited in outputs, do not distinguish between claims that are directly supported by retrieved text and claims that are interpolated from model priors, and do not expose confidence or uncertainty metadata to downstream consumers.

**Constitutional AI (RLAIF)** extended the alignment paradigm to self-supervised critique. As noted in Section 2.1.4, Bai et al. demonstrated that a model trained to critique and revise its own outputs against a written constitution achieves harmlessness comparable to RLHF without requiring human labels for harmful content [9]. The technique is relevant to Chirality's AUDITOR agent tier, which performs structured self-review of ANALYST outputs against invariant contracts. The architectural difference is that Constitutional AI operates as a training-time distribution shift, while Chirality's AUDITOR operates as a runtime architectural check with traceable audit output.

### 2.2.4 Confidence Calibration

Guo et al. established that modern neural networks are poorly calibrated: their predicted confidence scores do not match empirical accuracy rates [18]. Using reliability diagrams and Expected Calibration Error (ECE) as diagnostic tools, the paper showed that depth, width, weight decay, and batch normalisation all affect calibration, and that temperature scaling — a single-parameter post-hoc method — is surprisingly effective at restoring calibration. This foundational result implies that a model's expressed certainty is not a reliable signal of factual accuracy. For the Chirality epistemic architecture, this finding motivates a design decision: rather than relying on model-reported confidence scores, the architecture assigns confidence class at the structural level based on the derivation path of the claim (directly retrieved, inferred from retrieved evidence, or generated from prior).

### 2.2.5 Trustworthiness Frameworks

**NIST AI RMF 1.0** established the primary governance vocabulary for trustworthy AI systems in the United States regulatory context. Published by the National Institute of Standards and Technology in January 2023, the framework defines trustworthiness characteristics — valid and reliable, safe, secure and resilient, accountable and transparent, explainable and interpretable, privacy-enhanced, and fair — and organises AI risk management into four functions: Govern, Map, Measure, and Manage [19]. The NIST framework is a process framework: it specifies organisational practices for managing AI risk. It does not specify architectural mechanisms that enforce trustworthiness properties at the system level. Chirality is designed to be a technical implementation of the NIST trustworthiness characteristics for the specific context of agentic systems in professional engineering practice.

**EU AI Act** established the first comprehensive legal framework for AI regulation globally. Regulation (EU) 2024/1689, which entered into force on 1 August 2024, classifies AI systems by risk tier and imposes transparency and accountability obligations on high-risk systems [20]. Article 13 requires that high-risk AI systems be sufficiently transparent to enable deployers to interpret outputs appropriately, and that systems be accompanied by documentation enabling oversight. For multi-agent systems operating in professional engineering contexts — the domain of Chirality — AI Act obligations apply to the system as a whole. Chirality's invariant contracts, write-scope quarantine, and audit trail are designed to be interpretable as technical implementations of Article 13 transparency requirements and the explainability obligations of Article 14.

### 2.2.6 Gap: Population-Level Accuracy vs. Per-Claim Transparency

The surveyed literature addresses hallucination and trustworthiness through two primary strategies:

1. **Training-time distribution shaping** (RLHF, Constitutional AI, instruction fine-tuning): reduces the expected rate of hallucination across a population of outputs by altering model priors. Provides no per-output guarantee and exposes no ground-truth provenance to downstream consumers.

2. **Post-hoc detection and evaluation** (FActScore, entailment-based metrics, retrieval verification): measures hallucination rates after generation, enabling model comparison and auditing. Does not modify the generation process and is not available in real time at the point of use.

Retrieval-augmented generation is the closest existing approach to per-claim grounding, but standard RAG implementations do not enforce source attribution in outputs, do not distinguish between retrieved and inferred claims, and do not expose uncertainty metadata as a typed structural property.

No published architecture proposes the following combination of properties:

1. **Mandatory provenance attachment**: every claim in a system output must carry a machine-readable pointer to the source observation or retrieved document from which it was derived, as a structural constraint rather than a generation preference.
2. **No-invention rule**: a formally specified and runtime-enforced prohibition on agents generating claims that cannot be traced to a source within the defined retrieval scope.
3. **Epistemic labelling**: a typed taxonomy distinguishing directly-retrieved fact, inferred conclusion, and uncertain estimate, surfaced to the human principal as part of every output.
4. **Per-claim transparency**: the epistemic status of individual claims is observable and auditable, rather than a property that can only be assessed at the population level through benchmark evaluation.

This combination constitutes an architectural approach to epistemic transparency — a per-claim transparency framework — distinct from the population-level accuracy improvements achieved by existing training and post-hoc methods. The Chirality epistemic architecture is designed to implement this framework in a deployable system.

---

### References — Section 2.2

[12] Z. Ji, N. Lee, R. Frieske, T. Yu, D. Su, Y. Xu, E. Ishii, Y. J. Bang, A. Madotto, and P. Fung, "Survey of Hallucination in Natural Language Generation," *ACM Computing Surveys*, vol. 55, no. 12, article no. 248, Mar. 2023. doi: 10.1145/3571730

[13] L. Huang, W. Yu, W. Ma, W. Zhong, Z. Feng, H. Wang, Q. Chen, W. Peng, X. Feng, B. Qin, and T. Liu, "A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions," *ACM Transactions on Information Systems*, 2024. doi: 10.1145/3703155. [Online]. Available: https://arxiv.org/abs/2311.05232

[14] J. Maynez, S. Narayan, B. Bohnet, and R. McDonald, "On Faithfulness and Factuality in Abstractive Summarization," in *Proc. 58th Annual Meeting of the Association for Computational Linguistics (ACL)*, Online, 2020, pp. 1906–1919. doi: 10.18653/v1/2020.acl-main.173

[15] S. Min, K. Krishna, X. Lyu, M. Lewis, W.-T. Yih, P. W. Koh, M. Iyyer, L. Zettlemoyer, and H. Hajishirzi, "FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation," in *Proc. 2023 Conf. Empirical Methods in Natural Language Processing (EMNLP)*, Singapore, 2023, pp. 12076–12100. [Online]. Available: https://arxiv.org/abs/2305.14251

[16] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, J. Schulman, J. Hilton, F. Kelton, L. Miller, M. Simens, A. Askell, P. Welinder, P. Christiano, J. Leike, and R. Lowe, "Training Language Models to Follow Instructions with Human Feedback," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 35, New Orleans, LA, USA, 2022. [Online]. Available: https://arxiv.org/abs/2203.02155

[17] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W.-T. Yih, T. Rocktäschel, S. Riedel, and D. Kiela, "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 33, Virtual, 2020, pp. 9459–9474. [Online]. Available: https://arxiv.org/abs/2005.11401

[18] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, "On Calibration of Modern Neural Networks," in *Proc. 34th Int. Conf. Machine Learning (ICML)*, Sydney, Australia, 2017, pp. 1321–1330. [Online]. Available: https://proceedings.mlr.press/v70/guo17a.html

[19] National Institute of Standards and Technology (NIST), "Artificial Intelligence Risk Management Framework (AI RMF 1.0)," NIST AI 100-1, Gaithersburg, MD, USA, Jan. 2023. doi: 10.6028/NIST.AI.100-1. [Online]. Available: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf

[20] European Parliament and the Council of the European Union, "Regulation (EU) 2024/1689 of the European Parliament and of the Council laying down harmonised rules on artificial intelligence (Artificial Intelligence Act)," *Official Journal of the European Union*, L Series, 2024. [Online]. Available: https://eur-lex.europa.eu/

[9] Y. Bai, S. Jones, K. Ndousse, A. Askell, A. Chen, N. DasSarma, D. Drain, S. Fort, D. Ganguli, T. Henighan, et al., "Constitutional AI: Harmlessness from AI Feedback," *arXiv preprint arXiv:2212.08073*, 2022. [Online]. Available: https://arxiv.org/abs/2212.08073

---

*End of working file — Sections 2.1 and 2.2*

---


---

## 2.3 Formal Methods and Safety-Critical Systems Engineering

The application of formal methods to safety-critical software represents one of the most mature sub-disciplines in systems engineering. Over five decades, the field has developed rigorous techniques for specifying, verifying, and containing the behavior of deterministic systems — techniques that, as this thesis argues, require principled adaptation before they can be applied to the governance of probabilistic LLM agents.

### 2.3.1 Safety Engineering Foundations: System-Theoretic Accident Models

The foundational work in modern safety engineering is Leveson's *Engineering a Safer World: Systems Thinking Applied to Safety* [1], which introduces the System-Theoretic Accident Model and Processes (STAMP). Leveson challenges the prevailing chain-of-events accident model, arguing that complex sociotechnical systems fail not through linear causal chains but through emergent behavior arising from inadequate constraint enforcement across system components. STAMP models safety as a control problem: accidents occur when safety constraints are violated by inadequate control actions. The companion hazard analysis technique, Systems-Theoretic Process Analysis (STPA), derives safety constraints from control structure rather than failure mode enumeration.

The relevance to Chirality is direct. The Chirality invariant system — particularly the Runtime Invariants (R1–R9) and Interaction Invariants (I1–I10) — can be read as a STAMP-derived safety constraint set applied to a software agent control structure. Where STAMP asks "what control action could violate a safety constraint?", Chirality's gate-controlled workflow asks "what agent action could violate a professional obligation?" The architectural parallel is not coincidental: both frameworks treat safety as an emergent property of constraint enforcement rather than component reliability.

### 2.3.2 Avionics Software Assurance: DO-178C

The aviation industry's primary framework for software assurance is DO-178C, *Software Considerations in Airborne Systems and Equipment Certification* [2], published by RTCA in December 2011 jointly with EUROCAE as ED-12C. DO-178C establishes five software levels (A through E) based on the severity of failure conditions, defines objectives for planning, development, verification, configuration management, and quality assurance, and requires demonstration that software satisfies requirements with confidence commensurate with its safety impact.

A key architectural commitment in DO-178C is the coupling of behavioral objectives to formal requirements traceability: every software behavior must be traceable to a verified requirement, and every requirement must be shown to be satisfied by the implementation. DO-178C's supplement DO-333 extends this framework to formal methods specifically, recognizing that proof-based verification can substitute for certain coverage-based testing objectives.

Chirality's lifecycle state machine — which constrains agent actions to defined phases (LOAD, ACTIVE, SUSPENDED, DECOMMISSIONED) with explicit transition conditions — reflects the DO-178C principle that allowable system behaviors must be formally bounded and traceable to design intent. The analogue to software level assignment appears in Chirality's Type 0/1/2 write scope hierarchy, which classifies agent authority by blast radius rather than failure severity.

### 2.3.3 Functional Safety: IEC 61508 and Safety Integrity Levels

IEC 61508, *Functional Safety of Electrical/Electronic/Programmable Electronic Safety-related Systems* [3], is the international standard governing safety-related systems across industries from process control to medical devices. The standard introduces Safety Integrity Levels (SIL 1–4), which quantify required reliability as a function of risk, and mandates a defense-in-depth architecture in which multiple independent protection layers prevent single points of failure from propagating to hazardous outcomes.

IEC 61508 is notable for its explicit treatment of systematic failures — failures arising from design errors rather than random hardware degradation — and its recognition that software cannot be assigned a random failure rate in the same way as hardware. The standard responds to this with requirements for formal specification, systematic testing, and independent verification commensurate with the assigned SIL. Part 3 of the standard specifically addresses software safety requirements.

The IEC 61508 concept of independent protection layers maps onto Chirality's multi-layer enforcement architecture, in which invariants are enforced at four independent levels: instruction text, system prompt, agent runtime behavior, and human gate review. No single layer failure bypasses protection entirely. The SIL assignment logic — which calibrates stringency to consequence severity — is structurally analogous to Chirality's scope typing, where agents whose outputs feed directly into stamped professional deliverables are subject to stricter constraints than internal reasoning agents.

### 2.3.4 Partitioning and Fault Containment: Rushby on Avionics Architectures

The foundational work on fault containment through architectural partitioning is Rushby's *Partitioning in Avionics Architectures: Requirements, Mechanisms, and Assurance* [4], prepared for the FAA Technical Center and NASA Langley Research Center and issued as NASA Contractor Report CR-1999-209347 in June 1999. Rushby addresses the challenge of integrated modular avionics (IMA) systems, in which multiple functions — some safety-critical, some not — share a single fault-tolerant computing platform. The loss of natural physical isolation boundaries in IMA architectures requires that isolation be enforced through software and hardware mechanisms that restore equivalent containment guarantees. Rushby defines the requirements for robust partitioning (spatial and temporal separation), analyzes candidate mechanisms, and establishes assurance criteria.

The contribution to systems engineering theory is the formalization of fault containment as an architectural property rather than a component property: a system can achieve containment even if individual components fail, provided the partition boundaries are correctly specified and enforced. Rushby's requirement that partitioning mechanisms be "absolutely reliable" — meaning their failure would itself be a safety hazard — establishes the design principle that containment infrastructure must be held to a higher assurance level than the functions it contains.

Chirality's write scope system implements precisely this principle. Type 0 agents (read-only) are permanently constrained by their instruction architecture; Type 1 agents (project-scoped write) cannot access coordination infrastructure; Type 2 agents (coordination write) operate under the highest gate scrutiny. The boundaries are enforced in the system prompt layer, which is architecturally isolated from the content layer the agent reasons about. The parallel to spatial partitioning is direct: an agent cannot escape its write scope through reasoning, just as a partitioned process cannot access another partition's memory through software means alone.

### 2.3.5 Formal Verification in Safety-Critical Domains: Model Checking and Invariant-Based Verification

Two foundational formal methods texts define the verification techniques this thesis draws upon. Hoare's "An Axiomatic Basis for Computer Programming" [5], published in *Communications of the ACM* in 1969, introduced Hoare logic — the precondition/postcondition/invariant triple that remains the basis for program verification today. The Hoare triple {P} S {Q} asserts that if precondition P holds before executing program S, postcondition Q will hold upon termination. Invariants — properties that hold across all states of a program loop or system lifecycle — are the central specification vehicle for reasoning about system correctness.

Model checking, systematized by Clarke, Grumberg, and Peled in *Model Checking* [6] (MIT Press, 1999), provides algorithmic state-space exploration to verify that a finite-state system satisfies a temporal logic specification. Model checking exhaustively explores all reachable states and returns counterexamples when properties are violated, making it particularly suited to concurrent and reactive systems where proof-based verification is intractable. The NASA Formal Methods Symposium series [7], ongoing since 2009, has documented the application of model checking, theorem proving, and runtime verification to space and aviation systems. The 16th symposium (NFM 2024) proceedings, published by Springer in Lecture Notes in Computer Science Vol. 14627, represent the current state of the art in formal verification for safety-critical systems.

Lamport's *Specifying Systems: The TLA+ Language and Tools for Hardware and Software Engineers* [8] (Addison-Wesley, 2002) provides the specification language most widely used in distributed and concurrent systems verification. TLA+ treats system behavior as a sequence of states and defines correctness as satisfaction of temporal logic formulae over those sequences. The lifecycle state machine formalism used in Chirality — LOAD → ACTIVE → SUSPENDED → DECOMMISSIONED with invariant-preserving transitions — is structurally a TLA+ specification, even if not formally encoded as one.

The applicability of these techniques to the Chirality system is partial and asymmetric, which is precisely the gap this thesis identifies. Hoare logic, model checking, and TLA+ operate on deterministic systems with enumerable state spaces. LLM agents are neither: their internal state is not enumerable, their transitions are probabilistic, and their outputs cannot be formally specified as functions of inputs. The architectural response — invariant enforcement through external constraints rather than internal verification — is the central thesis contribution.

### 2.3.6 Formal Methods and AI Safety: An Emerging Field

The application of formal methods to AI and machine learning systems is an active area of research with no settled solutions. Hou et al., in the position paper "Trustworthy AI Agents Require the Integration of Large Language Models and Formal Methods" [9], presented at ICML 2025, argue that neither paradigm is sufficient alone: LLMs offer adaptability and natural language reasoning but lack formal guarantees, while formal methods provide rigor but require explicit state specifications that LLMs cannot supply. The paper proposes a hybrid paradigm in which formal methods constrain agent behavior at the system boundary, while LLMs operate within those constraints.

A systematic literature review by Freire et al., "Formal Methods for Safety-Critical Machine Learning," published in *Frontiers in Artificial Intelligence* in 2026 [10], surveys peer-reviewed research from 2020 to mid-2025 applying formal methods to machine learning in safety-critical applications. The review confirms that most verification techniques remain applicable only to small, trained models under narrow distributional assumptions, and that Large Language Models present fundamentally different challenges due to their scale, emergent behavior, and inability to be formally specified from first principles.

The governance-first architectural approach is examined in the arXiv preprint "From Craft to Constitution: A Governance-First Paradigm for Principled Agent Engineering" [11] (arXiv:2510.13857, 2025), which argues that agent reliability requires principled governance infrastructure — formal constitutions of constraints — rather than behavioral training or post-hoc testing. This framing aligns directly with Chirality's architectural commitment: the agent instruction set is a governance constitution, not a behavioral specification.

### 2.3.7 The Gap: From Deterministic Verification to Probabilistic Governance

The literature reviewed above establishes that formal methods and safety-critical systems engineering have developed powerful, well-validated techniques for deterministic software systems: Hoare triples for sequential programs, model checking for concurrent systems, partitioning for integrated platforms, safety integrity levels for risk stratification, and STAMP for control-structure hazard analysis. These techniques share a common presupposition: the system under analysis has a specifiable state space, and its behavior can be formally related to its requirements.

LLM-based agent systems violate this presupposition at the most fundamental level. An LLM agent's response to a given input is not a function; it is a probability distribution. Its internal state is a high-dimensional embedding space that cannot be enumerated or formally analyzed. Its "behavior" emerges from statistical regularities in training data, not from a verified implementation of a specification.

This mismatch defines the gap this thesis addresses. Rather than attempting to verify agent behavior — which is not tractable — Chirality applies classical formal methods concepts (invariants, lifecycle state machines, write scope containment, precondition gates) as external architectural constraints that bound what a non-deterministic agent can do, regardless of what it generates internally. The shift is from *algorithmic verification* of deterministic systems to *architectural governance* of probabilistic agents. The concepts are directly inherited from the safety-critical SE literature; the mode of application is novel.

---

## 2.4 Professional Engineering Regulation and AI

The regulatory frameworks governing licensed professional engineers define obligations of supervision, review, authentication, and accountability that predate AI systems entirely. This section surveys those frameworks and identifies the gap between what regulation requires of the professional and what existing guidance says about how AI systems should be architecturally designed to enable compliance.

### 2.4.1 APEGA: The Primary Regulatory Context

The Chirality project operates under Alberta jurisdiction. The governing regulator is the Association of Professional Engineers and Geoscientists of Alberta (APEGA), which licenses engineers under the *Engineering and Geoscience Professions Act* (EGPA), R.S.A. 2000, c. E-11.

**Relying on the Work of Others and Outsourcing.** APEGA's most directly relevant practice standard is *Relying on the Work of Others and Outsourcing* [12], which came into effect on May 1, 2021 (v4.0) and became enforceable May 1, 2022. The standard was developed in response to identified gaps in due diligence associated with high-profile engineering failures, including incidents resulting in death, environmental damage, and financial loss. It establishes that a licensed professional must use due diligence to confirm the reliability, accuracy, and validity of work performed by others; adherence to applicable regulatory requirements, standards, and codes; and adherence to specified quality control and assurance processes. Failure to comply is subject to disciplinary action.

The standard establishes the "Relying on the Work of Others" framework under which Chirality's regulatory mapping is constructed. AI agents in the Chirality system produce work that the licensed professional relies upon, making this standard the primary regulatory instrument. The standard does not address how AI systems should be architected to enable the required due diligence — that gap is the central contribution of Chapter 6 and Appendix C.

**Authenticating Professional Work Products.** APEGA's *Authenticating Professional Work Products* [13], revised November 1, 2024, defines the authentication requirements for professional work products (PWPs) — the act by which a licensed professional formally accepts responsibility for a deliverable. Authentication requires physical or digital stamp, APEGA member ID, and signature. The standard specifies that only work the professional has validated may be authenticated, and establishes the Notarius digital signature as the required mechanism for electronic authentication.

The Chirality architecture preserves authentication as an exclusively human gate action. No agent in the system has authority to authenticate a PWP; all authentication paths require human review and explicit approval. This is architecturally enforced through the lifecycle state machine, which holds deliverables in a pre-authentication state until a human gate action advances them to authenticated status.

**AI-Specific Guidance.** As of the date of this thesis, APEGA has not issued AI-specific guidance. The "Relying on the Work of Others" standard applies to AI agent outputs by direct interpretation: AI agents are "others" whose work the professional relies upon. APEGA's general standards for professional judgment, due diligence, and authentication apply without domain-specific modification. This absence of AI-specific guidance is itself a gap that this thesis addresses architecturally.

### 2.4.2 Engineers and Geoscientists British Columbia (EGBC)

Engineers and Geoscientists British Columbia (EGBC) released *Use of Artificial Intelligence (AI) in Professional Practice* [14], a practice advisory for EGBC registrants, on November 22, 2024. This is the most detailed AI-specific guidance issued by a Canadian provincial engineering regulator as of the date of this thesis.

The advisory establishes that engineering and geoscience professionals remain professionally responsible for their work even when it is generated by or includes AI output. It identifies key AI-specific risks including output bias arising from non-representative training datasets, automation bias (undue trust in AI over professional judgment), and context-dependent trustworthiness. The advisory requires that professionals who use AI must assess their ability to meet checking, direct supervision, document retention, and independent review requirements under the EGBC Bylaws.

Critically, the advisory defines the professional obligations but does not specify architectural requirements for AI systems. It tells the engineer what to do (review, supervise, retain) but not how AI systems should be designed to make those obligations fulfillable. This is precisely the architectural gap Chirality addresses: the system is designed so that the professional's review obligations are not merely stated but are structurally enforced by gate-controlled workflows that cannot be bypassed.

### 2.4.3 Professional Engineers Ontario (PEO)

Professional Engineers Ontario (PEO) has not, as of the date of this thesis, issued its own AI-specific practice guideline. PEO references the EGBC practice advisory in its knowledge centre as a relevant resource [15]. PEO's existing practice guidelines on supervision, review, and professional responsibility apply to AI-assisted work by extension of existing principles. The absence of Ontario-specific AI guidance, despite Ontario having the largest concentration of licensed engineers in Canada, underscores the early state of regulatory development in this area.

### 2.4.4 Engineers Canada: National Framework

Engineers Canada, the national organization representing provincial and territorial engineering regulators, has not issued a national guideline specifically addressing AI in professional practice as of the date of this thesis. Engineers Canada's national guidelines and papers define common principles across jurisdictions; the absence of an AI guideline means each province is developing guidance independently, creating potential inconsistency in how the EGBC and APEGA approaches are interpreted nationally [16]. Engineers Canada has published a position statement on AI in autonomous and connected vehicles, recognizing the need for professional engineering expertise in AI development, but this addresses engineers as AI developers rather than engineers as users of AI tools.

### 2.4.5 American Professional Engineering Regulation

**NSPE Position Statement on Artificial Intelligence.** The National Society of Professional Engineers (NSPE) has issued Position Statement No. 03-1774 on artificial intelligence [17], which establishes that individuals who design, develop, or oversee AI systems with direct safety impact should be held to professional licensure standards, and that AI-generated technical work requires at least the same level of scrutiny as human-created work. The NSPE Board of Ethical Review has separately addressed AI in engineering practice, confirming that licensed engineers cannot delegate professional judgment to AI systems and must exercise responsible charge over AI-assisted outputs.

**ASCE Policy Statement 573.** The American Society of Civil Engineers adopted Policy Statement 573, *Artificial Intelligence and Engineering Responsibility* [18], on July 18, 2024. The policy states directly that "AI cannot serve as a replacement for the professional judgement of a licensed Professional Engineer" and that civil engineers must maintain responsibility for project planning, design, construction, operations, and maintenance. The policy acknowledges that "the rapid advancement of AI technology is outstripping current laws and regulations" and calls for regulatory development. It does not prescribe architectural requirements for AI systems.

**Florida Board of Professional Engineers.** The Florida Board of Professional Engineers (FBPE) has published guidance acknowledging that existing engineering practice statutes apply to AI-assisted work, and that licensed engineers remain responsible for the accuracy and safety of AI-generated outputs regardless of the tool used. No architecture-specific requirements have been issued [SEARCH — FBPE guidance documents not confirmed at time of writing].

### 2.4.6 International Frameworks

**Engineers Australia.** Engineers Australia's *Code of Ethics and Guidelines on Professional Conduct* (2022) [19] provides the ethical framework under which Australian engineers practice, including principles of competence, honesty, and public safety. Engineers Australia has not, as of the date of this thesis, issued AI-specific technical guidance equivalent to the EGBC advisory. Australia's national AI Ethics Principles (eight principles including human oversight and accountability) provide a policy context but are not binding on engineers as professional obligations.

**UK Engineering Council.** The UK Engineering Council, which licenses Chartered Engineers (CEng) and other titles under the *Engineering Council Standard for Professional Engineering Competence* (UK-SPEC), has not issued AI-specific guidance for professional engineering practice as of the date of this thesis. The UK government's *Implementing the UK's AI Regulatory Principles* guidance (February 2024) [20] establishes cross-sector principles (safety, transparency, fairness, accountability, contestability) that apply to regulated sectors including engineering, but these are addressed to regulators rather than individual licensed professionals. The UK's sector-agnostic regulatory approach means that engineering-specific AI governance obligations remain underdeveloped relative to the Canadian provincial model.

### 2.4.7 Academic Literature: Engineering Regulation and AI

The academic literature on professional engineering regulation and AI is nascent. Most treatment of "AI regulation" focuses on product liability, algorithmic accountability in consumer contexts, or AI governance at the policy level — not on the obligations of the individually licensed practitioner who uses AI as a professional tool [21].

Investigating Accountability for Artificial Intelligence Through Risk Governance [22], published in *Frontiers in Psychology* in 2023 (PMC9905430), examines how accountability frameworks must evolve for AI systems, finding that concrete strategies for AI practitioners have not been adequately developed or communicated. This confirms the broader literature gap: regulatory frameworks define the obligation but not the architectural implementation.

The closest academic analog to the Chirality mapping appears in the engineering ethics literature on "responsible charge" — the doctrine that a licensed engineer must have actual knowledge of and responsibility for work done in their name [23]. AI systems whose outputs are not directly reviewed cannot satisfy responsible charge requirements; architecturally, the system must make such review not merely possible but structurally enforced.

### 2.4.8 The Gap: From Regulatory Obligation to Architectural Implementation

The regulatory literature reviewed above establishes a consistent pattern. Every jurisdiction examined — Alberta, British Columbia, Ontario, the United States, Australia, the United Kingdom — affirms the following obligations for the licensed professional who uses AI tools:

1. The professional must review and validate AI-generated outputs before relying on them.
2. The professional cannot delegate professional judgment to an AI system.
3. The professional must be able to demonstrate that quality control processes were followed.
4. Work products must be authenticated only after the professional has validated them.
5. The professional bears full liability for authenticated work products regardless of the tool used to generate them.

What none of the regulatory frameworks address is *how an AI system should be architecturally designed* to make these obligations structurally satisfiable rather than aspirationally stated. The EGBC advisory tells the engineer they must review AI outputs; it does not address what system design makes that review meaningful rather than perfunctory. The APEGA "Relying on the Work of Others" standard specifies what the professional must confirm; it does not address how AI agent systems should be structured so that the professional can, in fact, confirm it.

This is the gap Chirality fills. The agent instruction architecture is designed so that each specific requirement of the "Relying on the Work of Others" standard — reliability confirmation, accuracy validation, regulatory adherence, quality control verification — maps to a specific architectural mechanism: gate-controlled handoff, write scope constraints, provenance tracking, and the authentication lifecycle. The thesis contribution is not to restate the regulatory obligation but to demonstrate that an agent instruction architecture can be purpose-designed to satisfy it.

---

## References (IEEE Format)

[1] N. G. Leveson, *Engineering a Safer World: Systems Thinking Applied to Safety*. Cambridge, MA: MIT Press, 2011. [Online]. Available: https://direct.mit.edu/books/oa-monograph/2908/Engineering-a-Safer-WorldSystems-Thinking-Applied. ISBN: 9780262533690.

[2] RTCA, Inc. / EUROCAE, *DO-178C: Software Considerations in Airborne Systems and Equipment Certification*. Washington, DC: RTCA, Inc., Dec. 2011. [Also published as EUROCAE ED-12C.]

[3] International Electrotechnical Commission, *IEC 61508: Functional Safety of Electrical/Electronic/Programmable Electronic Safety-related Systems*, Parts 1–7, 2nd ed. Geneva: IEC, 2010.

[4] J. Rushby, "Partitioning in Avionics Architectures: Requirements, Mechanisms, and Assurance," NASA Contractor Report CR-1999-209347, Computer Science Laboratory, SRI International, Menlo Park, CA, Jun. 1999. [Online]. Available: https://ntrs.nasa.gov/api/citations/19990052867/downloads/19990052867.pdf.

[5] C. A. R. Hoare, "An Axiomatic Basis for Computer Programming," *Communications of the ACM*, vol. 12, no. 10, pp. 576–580, Oct. 1969. DOI: 10.1145/363235.363259.

[6] E. M. Clarke, O. Grumberg, and D. Peled, *Model Checking*. Cambridge, MA: MIT Press, 1999. ISBN: 9780262032704.

[7] NASA Langley Research Center, "NASA Formal Methods Symposium (NFM) Proceedings Series," published annually since 2009 in Springer *Lecture Notes in Computer Science*. Most recent: NFM 2024 (16th), Moffett Field, CA, Jun. 2024. DOI: 10.1007/978-3-031-60698-4.

[8] L. Lamport, *Specifying Systems: The TLA+ Language and Tools for Hardware and Software Engineers*. Boston, MA: Addison-Wesley, 2002. [Online]. Available: https://lamport.azurewebsites.net/tla/book.html. ISBN: 9780321143068.

[9] Z. Hou et al., "Position: Trustworthy AI Agents Require the Integration of Large Language Models and Formal Methods," in *Proc. 42nd Int. Conf. on Machine Learning (ICML 2025)*, Vancouver, Canada, Jul. 2025. [Online]. Available: https://zhehou.github.io/papers/Position-Trustworthy-AI-Agents-Require-the-Integration-of-Large-Language-Models-and-Formal-Methods.pdf.

[10] R. Freire et al., "Formal Methods for Safety-Critical Machine Learning: A Systematic Literature Review," *Frontiers in Artificial Intelligence*, 2026. DOI: 10.3389/frai.2026.1749956.

[11] [PLACEHOLDER — author], "From Craft to Constitution: A Governance-First Paradigm for Principled Agent Engineering," arXiv preprint arXiv:2510.13857, Oct. 2025. [Online]. Available: https://arxiv.org/html/2510.13857v1.

[12] Association of Professional Engineers and Geoscientists of Alberta (APEGA), *Relying on the Work of Others and Outsourcing*, Practice Standard, v4.0. Edmonton, AB: APEGA, May 2021 (enforceable May 2022). [Online]. Available: https://www.apega.ca/docs/default-source/pdfs/standards-guidelines/relying-on-the-work-of-others-and-outsourcing.pdf.

[13] Association of Professional Engineers and Geoscientists of Alberta (APEGA), *Authenticating Professional Work Products*, Practice Standard, revised ed. Edmonton, AB: APEGA, Nov. 1, 2024. [Online]. Available: https://www.apega.ca/docs/default-source/pdfs/standards-guidelines/authenticating-professional-work-products.pdf.

[14] Engineers and Geoscientists British Columbia (EGBC), *Use of Artificial Intelligence (AI) in Professional Practice*, Practice Advisory. Burnaby, BC: EGBC, Nov. 22, 2024. [Online]. Available: https://tools.egbc.ca/registrants/practice-resources/guidelines-advisories/Document/01525AMWZDBFA4VTKQBRHJXVI6AR4UUFGV/Use%20of%20Artificial%20Intelligence%20in%20Professional%20Work.

[15] Professional Engineers Ontario (PEO), "Knowledge Centre — Practice Advice Resources and Guidelines," Toronto, ON: PEO, 2025. [Online]. Available: https://www.peo.on.ca/knowledge-centre/practice-advice-resources-and-guidelines/practice-guidelines. [Note: PEO references EGBC advisory; no Ontario-specific AI guideline issued as of Mar. 2026.]

[16] Engineers Canada, "National Engineering Guidelines and Engineers Canada Papers," Ottawa, ON: Engineers Canada, 2025. [Online]. Available: https://engineerscanada.ca/regulatory-excellence/national-engineering-guidelines. [Note: No national AI guideline for professional practice confirmed as of Mar. 2026; AI position statement on autonomous vehicles exists but addresses engineers as AI developers.]

[17] National Society of Professional Engineers (NSPE), "Artificial Intelligence," Position Statement No. 03-1774, Alexandria, VA: NSPE, [SEARCH — exact adoption date not confirmed in public documents]. [Online]. Available: https://www.nspe.org/nspe-advocacy/explore-issues/professional-policies-and-position-statements/artificial-intelligence.

[18] American Society of Civil Engineers (ASCE), "Policy Statement 573 — Artificial Intelligence and Engineering Responsibility," Reston, VA: ASCE, adopted Jul. 18, 2024. [Online]. Available: https://www.asce.org/advocacy/policy-statements/ps573---artificial-intelligence-and-engineering-responsibility.

[19] Engineers Australia, *Code of Ethics and Guidelines on Professional Conduct*. Canberra, ACT: Engineers Australia, 2022. [Online]. Available: https://www.engineersaustralia.org.au/about-us/professional-standards-framework. [Note: No AI-specific engineering practice standard confirmed as of Mar. 2026.]

[20] Department for Science, Innovation and Technology (UK), *Implementing the UK's AI Regulatory Principles: Initial Guidance for Regulators*, UK Government, London: DSIT, Feb. 2024. [Online]. Available: https://assets.publishing.service.gov.uk/media/65c0b6bd63a23d0013c821a0/implementing_the_uk_ai_regulatory_principles_guidance_for_regulators.pdf.

[21] R. Freire et al., "Navigating the AI Regulatory Landscape: Balancing Innovation, Ethics, and Global Governance," *Asian Journal of International Law*, vol. 15, no. 1, 2025. DOI: 10.1080/20954816.2025.2569584.

[22] M. Dobbe et al., "Investigating Accountability for Artificial Intelligence Through Risk Governance: A Workshop-Based Exploratory Study," *Frontiers in Psychology*, vol. 14, 2023. DOI: 10.3389/fpsyg.2023.1073686. PMC9905430.

[23] National Society of Professional Engineers (NSPE), "Use of Artificial Intelligence in Engineering Practice," Board of Ethical Review Case, Alexandria, VA: NSPE, 2024. [Online]. Available: https://www.nspe.org/career-growth/ethics/board-ethical-review-cases/use-artificial-intelligence-engineering-practice.

---

*Notes on placeholder entries:*
- *[11] arXiv:2510.13857 — author list not confirmed; verify before final submission.*
- *[17] NSPE Position Statement No. 03-1774 — adoption date not publicly visible; confirm via NSPE membership or direct inquiry.*
- *[19] Engineers Australia — confirm whether any AI-specific guidance has been issued since Nov. 2024.*
- *[FBPE] — Florida Board of Professional Engineers AI guidance referenced in Section 2.4.5; confirm via fbpe.org before including.*

---


---

## 2.5 Epistemic Frameworks and Knowledge Engineering

The Chirality architecture makes a claim that is unusual in software systems engineering: that the epistemic status of every claim produced by the system must be architecturally explicit and auditable. This is not a quality aspiration or a style guideline. It is an invariant — K-PROV-1, K-INVENT-1, K-CONFLICT-1 — enforced uniformly across all agents. To situate this contribution, this section surveys the relevant literature in four areas: provenance standards for data and knowledge systems; foundational knowledge representation theory; ontological frameworks for information systems; and social epistemology. The section then identifies the gap that Chirality's architecture addresses: epistemic frameworks have been theorized extensively, but none has been operationalized as an architectural invariant governing LLM-based agent systems.

---

### 2.5.1 Provenance Standards: W3C PROV

The W3C Provenance Data Model (PROV-DM), published as a W3C Recommendation in April 2013, provides the canonical standardized framework for representing provenance information on the web [1]. Edited by Luc Moreau (University of Southampton) and Paolo Missier (Newcastle University), PROV-DM defines provenance as "information about entities, activities, and people involved in producing a piece of data or thing, which can be used to form assessments about its quality, reliability or trustworthiness." The model organizes provenance into six components: (1) entities and activities — the fundamental building blocks of what exists and what happens; (2) derivations — how entities arise from other entities; (3) agents and responsibility — the people, organizations, and software that bear responsibility for outcomes; (4) bundles — a mechanism for provenance-of-provenance, treating provenance assertions as entities in their own right; (5) alternate entities — relations between descriptions of the same thing; and (6) collections — logical groupings of entities.

PROV-DM is domain-agnostic and carries defined extensibility points for domain-specific information. It has been adopted as the foundational provenance vocabulary across scientific computing, e-science workflows, government data publishing, and semantic web applications. The companion specification PROV-N provides a human-readable notation for PROV assertions, and PROV-O provides an OWL ontology serialization [2].

**Relation to Chirality.** Chirality's K-PROV-1 invariant — which requires every extracted or aggregated claim to carry a source file reference and section pointer, or an explicit `location TBD` marker — is structurally isomorphic to PROV-DM's core model. A Chirality provenance record consists of an entity (the claim in the deliverable), an activity (the agent task that produced it), and an agent (the agent role). The `EvidenceFile`, `SourceRef`, and `EvidenceQuote` required columns in `Dependencies.csv` implement precisely the entity-activity-agent triad that PROV-DM defines. However, where PROV-DM is a data interchange standard, Chirality treats provenance not as metadata to be optionally attached but as a structural invariant: a claim without provenance is architecturally visible as ungrounded, not merely incomplete. This shift — from provenance as a feature to provenance as a governance constraint — is Chirality's architectural contribution beyond the PROV-DM framework.

---

### 2.5.2 Database Provenance: Why, How, and Where

The formal theoretical foundations of database provenance were established by Buneman, Khanna, and Tan in their seminal 2001 paper "Why and Where: A Characterization of Data Provenance," presented at the 8th International Conference on Database Theory (ICDT) [3]. This work introduced a distinction between *why-provenance* (the source tuples that contributed to the existence of an output tuple) and *where-provenance* (the specific locations in source databases from which data values were copied). The formalization applies to relational databases and extends to hierarchical data models including XML.

The theoretical framework was substantially extended in Cheney, Chiticariu, and Tan's survey "Provenance in Databases: Why, How, and Where," published in *Foundations and Trends in Databases* in 2009 [4]. This comprehensive treatment defines three orthogonal axes of database provenance — why, how (the algebraic derivation), and where — and examines applications including confidence computation, view maintenance, query debugging, and annotation propagation. The survey establishes provenance as a first-class semantic property of database systems, not a secondary auditing capability.

**Relation to Chirality.** The database provenance literature establishes the theoretical basis for treating provenance as an intrinsic property of data items, not an optional annotation. Chirality inherits this commitment: the presence of provenance is a structural requirement, and the absence of provenance is itself a defined state (`location TBD`) rather than a null. The distinction between why-provenance and where-provenance is mirrored in Chirality's `EvidenceQuote` (why — the specific claim relied upon) and `SourceRef` (where — the precise location in the source document). The Chirality architecture extends this framework from database query provenance to the broader domain of claim provenance in professional engineering deliverables produced by LLM agents.

---

### 2.5.3 Knowledge Representation Foundations

John F. Sowa's *Knowledge Representation: Logical, Philosophical, and Computational Foundations* (Brooks/Cole, 2000) provides the foundational synthetic treatment of knowledge representation that bridges formal logic, ontology, linguistics, and computational implementation [5]. The work integrates contributions from philosophy of language, predicate logic, modal logics, description logics, conceptual graphs, and ontological frameworks into a unified treatment of how knowledge can be represented in computable form. Sowa argues that knowledge representation is not merely a technical problem but a philosophical one: what one can represent determines what one can reason about, and the expressive limitations of any representational system impose hard constraints on the inferences that can be drawn.

Of particular relevance is Sowa's treatment of the relationship between language, ontology, and inference. Sowa develops the case that knowledge representations must be grounded in an underlying ontology — a commitment about what kinds of things exist in the domain — and that the structure of the ontology shapes the inferences the system can support. A representation that lacks ontological discipline will produce inferences that are formally valid but semantically empty: they follow from the representation but do not correspond to facts about the domain.

**Relation to Chirality.** Sowa's argument that representational structure constrains inferential validity directly grounds Chirality's TYPES.md vocabulary — a canonical ontology of constructs (Package, Deliverable, Dependency, LifecycleState, EpistemicLabel) that all agents are required to use. When an agent produces a claim labeled ASSUMPTION rather than FACT, the label is not merely informational. It restricts the inferences that a licensed professional may draw from the claim without further validation. The epistemic label system implements precisely the principle Sowa identifies: the representation encodes the justificatory status of a claim, and that status is load-bearing for subsequent reasoning.

---

### 2.5.4 Ontological Foundations of Information Systems: The Bunge-Wand-Weber Framework

Yair Wand and Ron Weber's application of Mario Bunge's ontology to information systems theory produced a foundational framework — the Bunge-Wand-Weber (BWW) model — that has been extensively applied in conceptual modeling, database design, and requirements engineering. The foundational paper, "An Ontological Model of an Information System," was published in *IEEE Transactions on Software Engineering* in 1990 [6]. The paper draws directly on Bunge's *Treatise on Basic Philosophy* to propose an information systems ontology whose core constructs include: things (substantial individuals that possess properties), attributes (functions that map things to values), states (specific value assignments of a thing's attributes at a time), events (changes of state), and couplings (dependencies between things' state spaces).

The subsequent paper "On the Deep Structure of Information Systems," published in *Information Systems Journal* in 1995, extended the BWW ontology into three formal models [7]: (1) the *representational model*, which evaluates the ontological expressiveness of analysis and design grammars; (2) the *state-tracking model*, which specifies four requirements an information system must satisfy to faithfully track the real-world system it models; and (3) the *good-decomposition model*, which establishes three necessary conditions for well-structured IS decomposition. The BWW framework has been applied to evaluate modeling grammars including the Entity-Relationship model, UML, and BPMN, and has generated a substantial secondary literature in IS research [PLACEHOLDER: verify extent of secondary literature — see Allen and March 2006 critical assessment].

**Relation to Chirality.** The BWW framework provides the philosophical grounding for Chirality's ontological commitments, noted in Chapter 3. The structural invariants K-HIER-1 (flat package-to-deliverable hierarchy) and K-ID-1 (stable identifiers) implement the BWW requirement that the representational model contain no constructs without real-world referents. Every folder corresponds to a real work item; every dependency row corresponds to a real relationship; every status file corresponds to a real lifecycle state. No constructs exist for system convenience alone. The BWW state-tracking model's requirement that an IS faithfully track the state of the real-world system it represents is enforced in Chirality through filesystem-as-single-source-of-truth: the filesystem state is the authoritative project state, and any divergence between the filesystem and the actual project state is a governance failure, not a data inconsistency.

---

### 2.5.5 Social Epistemology: Goldman's Framework

Alvin I. Goldman's *Epistemology and Cognition* (Harvard University Press, 1986) established the philosophical program of naturalistic epistemology — the view that epistemological questions about justification and knowledge must be answered by reference to the actual cognitive processes that produce beliefs, not merely by logical analysis [8]. Goldman argued that epistemology cannot be conducted independently of cognitive science: what counts as a justified belief depends on whether the processes that produced it are reliable truth-conducive processes. This reliabilist framework has become one of the dominant approaches in contemporary epistemology.

Goldman's subsequent work *Knowledge in a Social World* (Oxford: Clarendon Press, 1999) extended the reliabilist framework to social and institutional settings [9]. Goldman articulated a "veritistic social epistemology" — a normative discipline concerned with which social practices and institutions best foster the production of true beliefs across a community. The work examines testimony, argumentation norms, information technology, legal epistemology, and democratic deliberation as sites where social institutions either enhance or impede collective epistemic performance. The central claim is that epistemic evaluation applies not only to individual believers but to social systems, and that well-designed institutions can substitute for individual epistemic competence in contexts where reliable individual judgment cannot be guaranteed.

**Relation to Chirality.** Goldman's reliabilist framework is directly applicable to the problem Chirality addresses. In professional engineering practice, the licensed professional who seals a document cannot personally verify every claim in a complex deliverable. What they can verify is whether the process that produced each claim is reliable — i.e., whether it is a process that tends to produce grounded, attributable claims rather than plausible-sounding inventions. Chirality's epistemic architecture operationalizes Goldman's insight at the system level: rather than requiring the individual professional to evaluate every claim's reliability on its merits, the architecture makes the reliability of the production process structurally visible. The FACT/ASSUMPTION/PROPOSAL/TBD label system is a direct implementation of Goldman's key distinction: a claim labeled FACT carries the representation that it was produced by a reliable (source-grounded) process; a claim labeled ASSUMPTION carries the representation that it was produced by an inference process that may not be reliable for the specific value asserted.

Goldman's social epistemology also grounds the conflict surfacing mechanism (K-CONFLICT-1). Goldman's veritistic framework implies that suppressing disagreement reduces collective epistemic performance, because the community loses information about the actual state of epistemic uncertainty. Chirality's Conflict Table mechanism — which requires agents to surface disagreements between sources, label proposed resolutions as PROPOSAL, and leave the ruling to the human — is a structural implementation of this principle. The professional who reviews a Conflict Table is operating under Goldman's veritistic ideal: they have access to the competing claims, their sources, and the agent's reasoning, and they can make an informed ruling. The alternative — silent resolution by the agent — would violate the veritistic requirement by suppressing relevant epistemic information.

---

### 2.5.6 Epistemic Logic in Distributed Systems

Halpern and Moses's "Knowledge and Common Knowledge in a Distributed Environment," published in the *Journal of the ACM* in 1990, established the formal framework for reasoning about knowledge states in distributed systems [10]. The paper introduces a modal epistemic logic in which the knowledge state of each processor is represented as a set of possible worlds consistent with its local information. The central result is that *common knowledge* — a fact known by all agents, known by all agents to be known by all agents, and so on — is unattainable in practical distributed systems with communication delays. The paper introduces weaker variants including *eventual common knowledge* and *epsilon-common knowledge* that are attainable under realistic conditions.

While Halpern and Moses work in the domain of distributed computing protocols, their framework is relevant to any system in which multiple agents hold potentially inconsistent local knowledge states. The impossibility result for common knowledge implies that in any distributed system with communication delays or failures, agents will inevitably hold divergent views of the world, and protocol design must account for this.

**Relation to Chirality.** The Halpern-Moses framework provides the theoretical grounding for Chirality's conflict detection architecture. In a multi-agent engineering system, different agents will process different source documents and may extract inconsistent claims from them. The impossibility of common knowledge implies that consensus cannot be assumed — it must be detected, surfaced, and resolved. K-CONFLICT-1's requirement that agents produce Conflict Tables rather than silently resolve contradictions is consistent with the Halpern-Moses result: because the system cannot guarantee that agents have processed consistent information, the architecture must treat divergence as an expected condition and provide a mechanism for surfacing and resolving it. The Conflict Table is the epistemic reconciliation mechanism that the Halpern-Moses framework implies is necessary.

---

### 2.5.7 Epistemic Trust and AI Certification Frameworks

Jacovi, Marasović, Miller, and Goldberg's "Formalizing Trust in Artificial Intelligence: Prerequisites, Causes and Goals of Human Trust in AI," published in the Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency (FAccT '21), provides a formal framework for analyzing trust in AI systems [11]. The paper distinguishes between *intrinsic trust* (trust in the AI's inherent properties) and *extrinsic trust* (trust established through contractual or certification mechanisms), and introduces the concept of *contractual trust* — trust that holds conditionally on an explicit or implicit contract being honored. The authors argue that designing AI systems for trust requires specifying the conditions under which the contract holds, not merely asserting that the system is reliable.

The paper's framework is significant for its emphasis on the verifiability of trust conditions: a trust claim about an AI system is only meaningful if there are observable conditions that would falsify it. Jacovi et al. argue that explanations and transparency mechanisms are trust-enabling not because they make the AI more accurate, but because they make the conditions for appropriate trust observable.

More recent work has explicitly addressed epistemic governance architectures for LLM systems. The paper "Externalising Epistemic Governance for Stateless Large Language Models: The CUL/TCL Architecture" (ResearchGate, 2025) [PLACEHOLDER: verify publication venue and author names — paper appears in ResearchGate preprint archive December 2025] proposes a dual-layer architecture in which a Context Utility Layer determines verification requirements and a Truth-Checker Layer assigns one of four truth-states to claims. The paper explicitly frames the architecture as "externalising epistemic governance from model weights to configurable components" — a formulation that parallels Chirality's approach. The CUL/TCL architecture demonstrates that the research community is converging on the position that epistemic governance must be an architectural property, not a model property.

**Relation to Chirality.** The Jacovi et al. framework directly grounds Chirality's approach to professional reliance. The APEGA professional practice standard "Relying on the Work of Others and Outsourcing" [CITE:APEGA_RWO2021] requires the licensed professional who seals a document to have a basis for reliance on delegated work. Chirality's epistemic labels, provenance records, and conflict tables are the technical implementation of the "contract" that Jacovi et al. identify as the precondition for appropriate trust: the professional can verify the conditions under which a claim is labeled FACT (it has a cited source), can observe when those conditions are not met (label is ASSUMPTION or TBD), and can verify that conflicts have been surfaced rather than suppressed. The trust contract is architecturally enforced, not asserted.

---

### 2.5.8 The Gap: Epistemic Theory Without Architectural Enforcement

The preceding survey establishes that robust theoretical foundations exist for each component of Chirality's epistemic architecture:

- W3C PROV provides a standardized model for provenance as a structural property of data and knowledge artifacts [1].
- The database provenance literature (Buneman et al. [3]; Cheney et al. [4]) formalizes provenance in computational terms and establishes its applicability to complex derivations.
- Sowa [5] establishes that representational structure is epistemically load-bearing: the labels and ontology of a system constrain the inferences that can be drawn from it.
- The BWW model (Wand and Weber [6][7]) establishes that IS ontologies should be grounded in real-world structures and that representational constructs must correspond to things in the domain.
- Goldman [8][9] establishes the reliabilist and social-epistemic framework: epistemic evaluation applies to processes and institutions, not merely to individual claims, and social systems can be designed to enhance collective epistemic performance.
- Halpern and Moses [10] establish that distributed systems cannot assume consistent knowledge states and must treat divergence as a structural condition requiring explicit resolution.
- Jacovi et al. [11] establish that trust in AI systems requires observable, verifiable contractual conditions.

The gap in the literature is this: **none of these frameworks has been operationalized as architectural invariants governing an LLM-based multi-agent system in professional practice.** The frameworks exist at three levels — philosophical (Goldman), formal-theoretical (Halpern-Moses, Buneman-Cheney), and standards (W3C PROV) — but all share the property that they describe epistemic requirements without providing a mechanism for enforcing them as binding constraints on autonomous agents.

This gap is not incidental. It reflects a structural challenge in the field: most epistemic frameworks were developed for human cognizers (Goldman), database systems with deterministic query semantics (Buneman, Cheney), or distributed protocols with formally specified message-passing (Halpern-Moses). LLM-based agents are neither: they are probabilistic, context-sensitive, and capable of generating plausible-sounding content without any grounding in source material. The failure modes of LLM agents are categorically different from the failure modes these frameworks were designed to address.

The existing literature on epistemic governance of LLM systems (Jacovi et al. [11]; CUL/TCL [PLACEHOLDER]) recognizes the architectural dimension but has not yet produced a complete operational framework — a set of binding invariants that govern every agent in the system, with defined enforcement mechanisms and observable compliance conditions.

**Chirality's contribution** is to close this gap by implementing epistemic concepts as architectural invariants. The distinction that defines the contribution is between two levels of concern:

1. *Model-level epistemic reliability* — improving the probability that an LLM produces accurate outputs, through RLHF, RAG, fine-tuning, or factuality verification. This is the dominant approach in the current literature and is a legitimate engineering concern.

2. *Governance-level epistemic transparency* — making the epistemic status of every claim architecturally visible and auditable, regardless of the model's underlying reliability. This is Chirality's approach.

These two levels address different problems. Model-level approaches reduce the frequency of epistemic failures. Governance-level approaches make epistemic failures detectable when they occur and make the absence of grounding structurally observable even when no failure has occurred. For professional engineering practice, the second property is more fundamental: a licensed professional who seals a document must be able to form a judgment about the epistemic basis of every claim they are relying on, and this judgment cannot be delegated to a probabilistic model. It requires an architectural record.

Chirality implements this distinction through four invariants — K-PROV-1 (mandatory provenance), K-INVENT-1 (no invention), K-CONFLICT-1 (conflict surfacing), and the FACT/ASSUMPTION/PROPOSAL/TBD epistemic label system — enforced uniformly across all agents, with compliance verifiable by inspection of the filesystem. This constitutes the first complete operationalization of the social-epistemic framework (Goldman), provenance standards (W3C PROV), and conflict management theory (Halpern-Moses) as binding architectural constraints on an LLM-based professional engineering system.

---

## References for Section 2.5

[1] L. Moreau and P. Missier, Eds., "PROV-DM: The PROV Data Model," W3C Recommendation, World Wide Web Consortium, 30 Apr. 2013. [Online]. Available: https://www.w3.org/TR/2013/REC-prov-dm-20130430/

[2] L. Moreau and P. Missier, Eds., "PROV-Overview: An Overview of the PROV Family of Documents," W3C Working Group Note, World Wide Web Consortium, 30 Apr. 2013. [Online]. Available: https://www.w3.org/TR/prov-overview/

[3] P. Buneman, S. Khanna, and W.-C. Tan, "Why and Where: A Characterization of Data Provenance," in *Proc. 8th Int. Conf. Database Theory (ICDT 2001)*, London, UK, Jan. 2001, pp. 316–330, Lecture Notes in Computer Science, vol. 1973. doi: 10.1007/3-540-44503-X_20

[4] J. Cheney, L. Chiticariu, and W.-C. Tan, "Provenance in Databases: Why, How, and Where," *Foundations and Trends in Databases*, vol. 1, no. 4, pp. 379–474, 2009. doi: 10.1561/1900000006

[5] J. F. Sowa, *Knowledge Representation: Logical, Philosophical, and Computational Foundations*. Pacific Grove, CA, USA: Brooks/Cole, 2000, ISBN: 0-534-94965-7.

[6] Y. Wand and R. Weber, "An Ontological Model of an Information System," *IEEE Trans. Softw. Eng.*, vol. 16, no. 11, pp. 1282–1292, Nov. 1990. doi: 10.1109/32.60316

[7] Y. Wand and R. Weber, "On the Deep Structure of Information Systems," *Inf. Syst. J.*, vol. 5, no. 3, pp. 203–223, 1995. doi: 10.1111/j.1365-2575.1995.tb00108.x

[8] A. I. Goldman, *Epistemology and Cognition*. Cambridge, MA, USA: Harvard University Press, 1986. ISBN: 978-0-674-25895-2.

[9] A. I. Goldman, *Knowledge in a Social World*. Oxford, UK: Clarendon Press, 1999. ISBN: 978-0-198-23777-8.

[10] J. Y. Halpern and Y. Moses, "Knowledge and Common Knowledge in a Distributed Environment," *J. ACM*, vol. 37, no. 3, pp. 549–587, Jul. 1990. doi: 10.1145/79147.79161

[11] A. Jacovi, A. Marasović, T. Miller, and Y. Goldberg, "Formalizing Trust in Artificial Intelligence: Prerequisites, Causes and Goals of Human Trust in AI," in *Proc. 2021 ACM Conf. Fairness, Accountability, and Transparency (FAccT '21)*, Virtual Event, Canada, Mar. 2021, pp. 624–635. doi: 10.1145/3442188.3445923

[PLACEHOLDER — verify] Natangelo, S. et al., "Externalising Epistemic Governance for Stateless Large Language Models: The CUL/TCL Architecture," ResearchGate preprint, Dec. 2025. [PLACEHOLDER: confirm author full names, confirm whether published in conference proceedings or journal, confirm DOI]

---

## 2.6 Synthesis: The Governance Gap

The five domains surveyed in this chapter each advance a frontier that is necessary but insufficient for governing AI agents in professional engineering practice. Agent architectures (§2.1) define what agents can do — reason, plan, use tools, collaborate — but not what they must not do or what evidence they must provide. Hallucination research (§2.2) characterizes the LLM reliability problem and proposes population-level mitigations, but does not provide per-claim epistemic transparency for individual outputs. Formal methods and safety-critical SE (§2.3) offer mature techniques for constraining deterministic systems, but these have not been adapted for probabilistic LLM agents. Professional regulation (§2.4) defines what the licensed professional must do when relying on the work of others, but does not specify how AI systems should be architected to make compliance structurally enforceable. Epistemic frameworks (§2.5) provide theoretical foundations for provenance, knowledge representation, and epistemic transparency, but none have been operationalized as binding architectural invariants for agent governance.

The gaps are summarized in the following table:

| Domain | Current Frontier | Gap |
|---|---|---|
| Agent architectures | Capability: what agents CAN do | Governability: what agents MUST NOT do, what evidence they MUST provide |
| LLM reliability | Population-level accuracy improvement | Per-claim epistemic transparency |
| Formal methods / safety-critical SE | Deterministic system verification | Governance of probabilistic LLM agents through architectural constraints |
| Professional regulation | Obligation specification (what the professional must do) | Architectural implementation (how systems enable the professional to comply) |
| Epistemic frameworks | Theory of provenance and knowledge status | Operationalization as binding invariants in agent governance |

These five gaps are facets of a single unaddressed problem: **no published work provides a complete, architecturally enforced governance framework for LLM-based agent systems that enables professional reliance on AI-assisted work products.**

Chirality addresses this problem by integrating contributions from all five domains: a hierarchical agent architecture with formal authority boundaries (§2.1), an epistemic transparency architecture that responds to the hallucination problem at the per-claim level (§2.2), classical formal methods adapted to agent governance through invariant contracts and fault containment (§2.3), a regulatory mapping that connects the architecture to existing professional obligations (§2.4), and an operationalization of epistemic theory as binding invariants (§2.5). The following chapters present these contributions in detail.

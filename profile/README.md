<a href="https://nodeandnorm.org/"><img src="https://raw.githubusercontent.com/node-and-norm/.github/main/assets/brand/current/banner.png" alt="node&norm: independent research on AI and practical human control" width="100%"></a>

# Evidence for practical human control

node&norm is an independent research program in AI governance, evaluation, and assurance. It examines practical human control and institutional responsibility: whether people can question AI-assisted decisions, exercise authority, and establish what happened when they intervened.

The work translates research into evaluation methods, inspectable evidence records, and candidate operational controls. This GitHub organization holds public specifications, assessment rules, source records, code, tests, and version histories. Each project states what its evidence supports and what remains unresolved.

[Research agenda](https://nodeandnorm.org/research-agenda/) · [Research overview](https://nodeandnorm.org/research) · [Governance Explorer](https://nodeandnorm.org/governance-map)

## Current focus: revocation in delegated AI workflows

Does withdrawing permission prevent further protected actions? Initial deterministic measurement qualification is complete in a controlled local test using scripted workers and a trusted database. This qualifies a bounded testing instrument; autonomous-agent effectiveness, broader control effectiveness, and novelty remain unestablished.

The next design candidate is a checkpointed delegated workflow using LangGraph. The proposed question is whether resumed or retried work can create a new protected effect after authority has been withdrawn. A specific workflow, matching implementation, and protocol remain to be selected; no framework-based experiment has run. The next phase requires a justified research question, matched comparisons, and a frozen protocol before execution.

For this test, withdrawal takes effect when the authority change is durably committed in the same ordering as protected changes. Pressing stop or receiving an acknowledgment alone does not establish that boundary.

Revocation is the sole active study direction. Evidence trust and oversight at scale remain deferred; completing a milestone does not automatically begin either study. The longer-term agenda extends toward frontier AI assurance, with AGI readiness as a longer-term purpose.

[Read the study, methods and limitations](https://nodeandnorm.org/research-agenda/#current-study) · [Next design task](https://nodeandnorm.org/research-agenda/#next-decisions)

The study materials remain private. The public agenda communicates the approved scope and status.

## Public methods and development infrastructure

| Project | Technical materials to inspect | Research boundary |
| :--- | :--- | :--- |
| [Trust, Autonomy, and Evidence (TAE)](https://github.com/node-and-norm/trust-autonomy-evidence) | Evidence architecture, claim-to-source records, deterministic assessment logic, historical cases, mutation controls, and archived Jev experiment results. Start with [release v0.18.0](https://github.com/node-and-norm/trust-autonomy-evidence/releases/tag/v0.18.0) and the [reproducibility guide](https://github.com/node-and-norm/trust-autonomy-evidence/blob/main/docs/REPRODUCIBILITY.md). | Methods demonstration and initial Jev research phase closed 16 October 2026. Selected historical cases and synthetic experiments leave independent reliability, field validity, contemporary transfer, and human time/quality benefits unestablished. |
| [Human Influence Telemetry (HIT)](https://github.com/node-and-norm/human-influence-telemetry) | Documentary assessment contract, scoring engine, conformance fixtures, reviewer materials, and claim-evidence gates. Start with [release v0.6.7](https://github.com/node-and-norm/human-influence-telemetry/releases/tag/v0.6.7), the [closeout plan](https://github.com/node-and-norm/human-influence-telemetry/blob/main/docs/closeout-plan.md) and [research status](https://github.com/node-and-norm/human-influence-telemetry/blob/main/RESEARCH.md). | Maintenance after [verified solo-development closeout on 17 October 2026](https://github.com/node-and-norm/human-influence-telemetry/blob/main/research/strengthening/maintenance-receipt.json). Manuscript work is deferred; v1.0 readiness, the independent-human implementation audit and current-contract replication remain unresolved. |
| [Control Evidence Corpus (CEC)](https://github.com/node-and-norm/node-norm-control-evidence) | Evidence-linked event records, schemas, synthetic dossiers, source reconnaissance, and reproducible evaluation infrastructure. Start with the [research brief](https://github.com/node-and-norm/node-norm-control-evidence/blob/main/research/README.md). | Development infrastructure: three synthetic demonstrations, zero independently coded empirical events, and no approved corpus release. Independent reliability and construct validation remain open. |
| [Governed Decision Intelligence (GDI)](https://github.com/node-and-norm/governed-decision-intelligence) | Governed Decision Record schema, gate classification, worked examples, and reference implementation. Start with [validation and reproducibility](https://github.com/node-and-norm/governed-decision-intelligence/blob/main/docs/validation-and-reproducibility.md); the [ScopeBlind contribution and review record](https://github.com/node-and-norm/governed-decision-intelligence/blob/main/docs/scopeblind-contribution-review.md) separates contribution and maintainer review credits. | Open specification and reference implementation. ScopeBlind PR #7 remains open and unmerged as of October 31, 2026. Independent field validation and external conformance acceptance remain open. |
| [Catholic Doctrinal Fidelity Index (CDFI)](https://github.com/node-and-norm/cdfi-framework) | Domain-specific evaluation governance, scoring configuration, cap rules, judge-reliability protocols, and traceability to seven AI safety publications. | Evolving. Scoring-contract reconciliation and qualified human theological validation remain open. SAICRED retains its separate project leadership and publication authority. |
| [Regulated Gate Decision Support (RGDS)](https://github.com/node-and-norm/rgds) | [Decision-log schema](https://github.com/node-and-norm/rgds/blob/main/decision-log/decision-log.schema.json), illustrative records, structural validation, and selected semantic checks for regulated phase gates. | Reference implementation. Reconstruction speed, field effectiveness, and regulatory outcomes remain unestablished. |

The [RGDS independent study](https://node-and-norm.github.io/rgds-independent-study/) provides the accompanying exploratory account; its [repository](https://github.com/node-and-norm/rgds-independent-study) preserves the study materials.

## Forthcoming publication and earlier development

| Work | Public introduction | Current status |
| :--- | :--- | :--- |
| *Poenitentia Institutionum* | Prudence, institutional responsibility, and repair in AI-assisted decisions. [Read the chapter introduction](https://nodeandnorm.org/research/institutional-responsibility-repair/) · [Publisher’s book page](https://enroutebooksandmedia.com/aifromacatholicperspective/). | Forthcoming chapter in *AI from a Catholic Perspective*, edited by Dr. Jane F. Adolphe and Dr. Łukasz Mirosław. Manuscript repository private; publication date and book chapter number remain unconfirmed. |
| Approval Evidence Sufficiency | Research into what approval records can establish about a proposed action, and when missing evidence leaves the conclusion unresolved. [Public research overview](https://nodeandnorm.org/research#approval-evidence-sufficiency). | Earlier development work; further testing paused. Repository private. Public materials and a publication date have not been announced. |

These public introductions preserve each work’s distinct status. They do not provide access to private research files or the full chapter.

## Reproduce a result

1. Read the project's research-status and limitations statements before interpreting its outputs.
2. Select a tagged release or commit. Record the manuscript, schema, software, and evidence-packet versions separately where the project distinguishes them.
3. Follow that repository's installation and validation instructions. Retain the command, environment, inputs, and output needed to reproduce a finding.
4. Inspect negative controls, excluded material, missing evidence, and open exceptions alongside successful checks.
5. Cite the exact artifact and version. Report a discrepancy through the project's issue or contribution process, with a minimal reproducible example and the affected claim.

Passing software checks establishes the behavior tested under the specified inputs. Claims about source accuracy, reviewer reliability, institutional adoption, or practical benefit require evidence suited to those questions.

## Supporting methods

[AI Assistance Governance](https://github.com/node-and-norm/rgds-ai-governance) develops a working profile for bounded AI participation, assigned human authority, and dependency assessment. [Applied AI Research Translator](https://github.com/node-and-norm/applied-ai-research-translator) provides a governed workflow from research inputs to traceable claims, bounded tasks, and human-reviewed decision records.

Each repository maintains its own methods, releases, attribution, license, and correction process. The organization directory is a route into those records; project-level status statements define the scope of their claims.

## Research and publication

Researcher: [Mark Julius Banasihan](https://github.com/mj3b). Project repositories distinguish research authorship, technical contributions, review, and team membership.

TAE's methods demonstration and initial Jev research phase closed on 16 October 2026 with [release v0.18.0](https://github.com/node-and-norm/trust-autonomy-evidence/releases/tag/v0.18.0). The [closeout record](https://github.com/node-and-norm/trust-autonomy-evidence/blob/main/docs/research-phase-closeout-2026-10-16.md) preserves the historical findings, separately approved conditional reassessment, completed checks, and research limitations. Reproducibility checks and AI-assisted review do not establish independent scientific validation.

The approved preprint [*From Formal Authority to Practical Human Control*](https://doi.org/10.5281/zenodo.23423847), revised 10 October 2026 and archived 16 October, and the [v0.18.0 software archive](https://doi.org/10.5281/zenodo.23423967) have separate DOIs. The manuscript has not undergone peer review. arXiv submission `7973196` remains **on hold**, as the author confirmed from the authenticated account on 16 October 2026.

CEC retains its own development status, evidence rules, corpus-release gates, and research claims. See its [integration contract](https://github.com/node-and-norm/node-norm-control-evidence/blob/main/docs/reference/INTEGRATION_CONTRACT.md) for any future use of its records by TAE or other projects.

The [About page](https://nodeandnorm.org/about.html) describes the research purpose and intellectual influences, including Daniel Kahneman's work on judgment and Stuart Russell's work on human control. Those influences frame the questions; the repositories carry the methods and evidence used to examine them.

Researchers, engineers, and organizational leaders can help examine a defined control claim, contribute a documented workflow, or identify evidence a test would need. The [agenda’s intended outputs and routes to collaboration](https://nodeandnorm.org/research-agenda/#solutions-research) describe that scope.

[Essays](https://nodeandnorm.org/) · [Research agenda](https://nodeandnorm.org/research-agenda/) · [Research overview](https://nodeandnorm.org/research) · [Governance Explorer](https://nodeandnorm.org/governance-map) · [Research integrity](https://nodeandnorm.org/about/research-integrity/) · [Brand assets](https://github.com/node-and-norm/.github/tree/main/assets/brand/current)

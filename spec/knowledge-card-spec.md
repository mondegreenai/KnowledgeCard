# The Knowledge Card Specification

**Version 0.1 (public draft)**
Copyright © 2026 Mondegreen.ai. Licensed under CC BY 4.0.

---

## 1. Purpose

A Knowledge Card captures validated knowledge about a single bounded concept in a form
that experts can review, organisations can audit, and AI systems can reason over. This
document specifies the structure of a Knowledge Card. The normative machine-readable schema
is [`schema/knowledge-card.schema.json`](../schema/knowledge-card.schema.json); where this
prose and the schema differ, the schema governs.

## 2. Conventions

A Knowledge Card is a JSON-LD document. Field names use the `kc:` prefix, bound to
`https://mondegreen.ai/ontology/kc#` by the context in
[`context/kc.jsonld`](../context/kc.jsonld). Terms drawn from a domain ontology (for example
`energy:` or `sd:`) are the responsibility of that ontology.

A card is the tuple **KC(C, S) = ⟨M, C, E, R, P, B, L⟩**: metadata, concept anchor, entity
register, relationship topology, reasoning, boundaries, and system link.

## 3. Top-level structure

| Field | Required | Description |
|---|---|---|
| `@context` | yes | JSON-LD context (the canonical Mondegreen context IRI or an inline object). |
| `@type` | yes | Must be `kc:KnowledgeCard`. |
| `@id` | no | IRI identifying this card individual. |
| `kc:concept` | yes | The concept anchor: the ontology class IRI the card is about. |
| `kc:title` | no | Human-readable title. |
| `kc:domain` | no | Human-readable domain label. |
| `kc:meta` | yes | Provenance, lifecycle state, validation record. |
| `kc:entities` | yes | The entity register. |
| `kc:relationships` | yes | The relationship topology. |
| `kc:reasoning` | yes | Layered reasoning. |
| `kc:boundaries` | yes | Scope limits, typed by severity. |
| `kc:systemLink` | no | Binding to the consuming system. |

## 4. Metadata (`kc:meta`)

Carries the card's lifecycle and the record of its validation.

- `kc:lifecycle` (required): one of `draft`, `validated`, `deprecated`, `superseded`. A card
  is authoritative only in the `validated` state. A card drafted by an automated pipeline
  remains `draft` until an expert signs it off.
- `kc:version` (required): a version string.
- `kc:validatedBy`, `kc:validationDate`: the expert and date of sign-off.
- `kc:ontologyVersion`: the domain ontology version under which the card was checked.
- `kc:supersededBy`: the IRI of the card that supersedes this one.
- `kc:provenance`: source documents and records the claims derive from.

## 5. Entity register (`kc:entities`)

Each entry registers an individual involved in the concept.

- `@id` (required): the ontology IRI of the entity.
- `kc:entityRole` (required): one of `primary-subject`, `causal-agent`, `causal-target`,
  `observable-signal`, `contextual-factor`.
- `kc:observability`: one of `directly-observable`, `sensor-derived`, `inferred`, `latent`.
- `kc:criticalityWeight`: how much the entity contributes to the conclusion, in [0, 1].

## 6. Relationship topology (`kc:relationships`)

Each entry is a named, ideally ontology-grounded relationship between entities.

- `kc:from`, `kc:property`, `kc:to` (required).
- `kc:confidence`: confidence in the relationship, in [0, 1].

## 7. Reasoning (`kc:reasoning`)

Reasoning is represented in layers. **The layers are a ladder, not a checklist:** a card
carries as many as its knowledge supports. At least one of the narrative or rule layers must
be present.

- `kc:level1_narrative`: a plain-language account of how the conclusion follows.
- `kc:level2_pattern`: the signals, thresholds, and the conclusion they support.
- `kc:level3_rule`: a formal rule (`SWRL`, `SPARQL`, or `SHACL`) whose terms are ontology
  classes, with an optional calibrated confidence.
- `kc:level4_probabilistic`: **optional**, present only when calibration data supports it.
  A `bayesian-network` or `markov-logic-network` formalism.

The layers are also **selective**: a card may apply a formal rule where the logic is crisp,
fall back to the probabilistic layer where the evidence is uncertain, and defer to a human
where neither holds. Complex problems may be covered by several composed cards, each bounded
to the part it can answer.

## 8. Boundaries (`kc:boundaries`)

Each entry states a condition under which the card's reasoning is limited, typed by severity.

- `kc:severity` (required): one of
  - `degrades-gracefully` — the card continues with reduced confidence;
  - `requires-human-review` — the card defers the decision to a person;
  - `card-invalid` — the card withdraws its authority to draw any conclusion.
- `kc:condition` (required): the triggering condition.
- `kc:rationale`: why the condition limits the card.

A `card-invalid` condition **overrides any positive conclusion**. Where a probabilistic layer
is present this is a hard defeat of the posterior; where the card reasons deterministically,
the condition simply blocks the rule from firing. Either way, the system fails safe rather
than guessing.

## 9. System link (`kc:systemLink`)

Binds the card to the consuming system: embedding mode, endpoint, and inference
configuration. A card is a specification of what a valid inference must satisfy, not an
implementation; the consuming system chooses how inferences are computed. The same card can
be read by an LLM-based agent and reasoned over in natural language, and also checked by a
symbolic reasoner.

## 10. Versioning of this specification

This is version 0.1, a public draft. The schema will evolve; breaking changes will be
versioned, and the `kc:ontologyVersion` and card `kc:version` fields allow deployed cards to
remain traceable across changes.

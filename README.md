<div align="center">

# Knowledge Cards

**Structured, validated knowledge for AI systems.**

A Knowledge Card is a structured artefact that captures validated knowledge about a
single bounded concept, in a form that experts can review, organisations can audit,
and AI systems can reason over.

[Specification](spec/knowledge-card-spec.md) ·
[Schema](schema/knowledge-card.schema.json) ·
[Example](examples/wind-energy-gearbox-spalling.jsonld) ·
[Paper](https://arxiv.org/abs/2607.XXXXX) <!-- Submitted to arXiv (cs.AI, cross-list cs.DB). Replace 2607.XXXXX with the public arXiv identifier once the abstract page goes live. --> ·
[Studio](https://studio.mondegreen.ai)

*A project by [Mondegreen](https://mondegreen.ai) · v0.1 public draft*

</div>

---

## The gap this fills

The documentation of AI systems is well served at two layers. Model cards describe how a
system behaves; data cards describe what it was trained on; system cards describe the risks
of a deployed system. None of them describes the **knowledge a system reasons from** — the
concepts it holds, the relationships it models, the reasoning it applies, and the limits
beyond which that reasoning no longer holds.

For pattern-recognition systems this gap is tolerable. For **agentic AI**, where a system
acts on its conclusions, it is the layer in which many initiatives stall: a proof of concept
performs well in a demonstration but cannot be moved into production, because the knowledge
the system relies on cannot be inspected, validated, or governed.

A Knowledge Card gives that layer a form.

## What a Knowledge Card is

For one concept — a failure mode, a compliance obligation, a process decision — a Knowledge
Card records:

- the **entities** and **relationships** involved,
- the **reasoning** that connects them, in layers from plain language to a formal rule,
- the **conditions** under which that reasoning no longer holds, and
- the **provenance** of every claim,

all grounded in a formal domain ontology, so every term has a fixed meaning, and signed off
by a domain expert before the card is treated as authoritative.

### The five defining properties

| Property | What it means | Why it matters |
|---|---|---|
| **Ontology-grounded** | Every entity and relationship is anchored to a formal ontology term, not a free-text label. | The same concept means the same thing across every agent and system: a shared semantic layer, not disconnected notes. |
| **Provenance-linked** | Every claim traces to its source and to the expert who validated it. | When an agent acts, the organisation can see exactly what the recommendation rests on. |
| **Boundary-explicit** | The card states, as first-class content, where its reasoning ceases to hold. | The agent knows the limits of its own competence and escalates rather than guessing. |
| **Expert-validated** | A card is authoritative only after a qualified domain expert signs it off. | The knowledge is warranted by a named human, not merely statistically plausible. |
| **Versioned** | New versions supersede old ones; earlier decisions stay traceable. | Knowledge improves over time without losing the audit trail. |

## A card at a glance

The example in this repository is a diagnostic card for a wind-turbine gearbox. An agent
supporting a wind-farm operator reads it to decide whether a vibration alert indicates
genuine bearing degradation, warranting an expensive maintenance dispatch, or a benign
transient. Its boundaries state where the diagnosis does not apply: for instance, if the
bearing was re-greased within the previous 48 hours the vibration signature is unreliable,
and the card withdraws its diagnosis so the agent escalates rather than acting on false
evidence.

See [`examples/wind-energy-gearbox-spalling.jsonld`](examples/wind-energy-gearbox-spalling.jsonld)
for the full card.

```jsonc
{
  "@type": "kc:KnowledgeCard",
  "kc:concept": "energy:GearboxBearing_OuterRaceSpalling",
  "kc:meta": { "kc:lifecycle": "validated", "kc:version": "1.0", ... },
  "kc:entities": [ ... ],
  "kc:relationships": [ ... ],
  "kc:reasoning": {
    "kc:level1_narrative": "A rising vibration amplitude ...",
    "kc:level3_rule": { "kc:ruleLanguage": "SWRL", ... }
  },
  "kc:boundaries": [
    { "kc:severity": "card-invalid",
      "kc:condition": "bearing re-greased within previous 48 hours" }
  ]
}
```

## Repository layout

```
schema/      The Knowledge Card JSON Schema (2020-12).
context/     The JSON-LD context mapping kc: terms to IRIs.
ontology/    A skeleton energy diagnostic ontology, so the example resolves.
examples/    A complete, schema-valid Knowledge Card (wind energy).
spec/        The written specification of the format.
scripts/     A validator for checking a card against the schema.
```

## Validate a card

```bash
pip install jsonschema
python scripts/validate_card.py examples/wind-energy-gearbox-spalling.jsonld
```

## The reasoning layers

A card represents its reasoning in layers, and carries **as many as its knowledge supports** —
the layers are a ladder, not a checklist.

1. **Narrative** — a plain-language account for a human reviewer.
2. **Pattern** — the signals, thresholds, and the conclusion they support.
3. **Rule** — a formal rule whose terms are ontology classes, checkable by a symbolic reasoner.
4. **Probabilistic** — *optional*, present only when calibration data supports it.

A card with only the narrative and rule layers is complete and valid. Most organisations have
not documented conditional probabilities, and a card is never the weaker for stopping where
its evidence stops.

## Status

This is a **v0.1 public draft**, released for community engagement. Initial prototype cards
have been built in the energy and pharmaceutical domains. The schema will evolve; breaking
changes will be versioned.

The ontology published here is a **skeleton**, included so the example is self-contained. It
is intentionally minimal and is not the full domain vocabulary used in Mondegreen engagements.

## Contributing

Feedback, issues, and proposals are welcome. Please open an issue to discuss a change before
submitting a pull request. By contributing, you agree that your contribution is licensed under
the same terms as the file it touches (see below).

## Licence

- **Schema, JSON-LD context, examples, and scripts:** [Apache 2.0](LICENSE).
- **Ontologies and written specification:** [CC BY 4.0](LICENSE-CC-BY).

Both licences permit commercial use and require attribution to Mondegreen.ai. See
[`NOTICE`](NOTICE) for attribution details.

Copyright © 2026 [Mondegreen.ai](https://mondegreen.ai). Porto, Portugal.

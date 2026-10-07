# Provenance

- **Creator:** Anonymous (Evidence Press standing protocol). **Publisher:** Evidence Press.
- **Human role:**
  - The publisher selected the opportunity from an agent-compiled shortlist of six applied research directions derived from the OpenAI mathematics repository (family 374) and asked for a local Evidence Press bundle for each (7 October 2026).
  - On 7 October 2026 the publisher supplied an external review of version 0.1.0 and asked for it to be actioned in full, especially its "could improve the work" section, and for the result to be taken through the full Evidence Press publication workflow.
  - No human mathematical contribution is claimed.
- **AI roles:**
  - Version 0.1.0 (local, never public): an OpenAI Codex assistant wrote the research contract, prior-art record, proofs P1–P5, code, tests, manuscript and bundle; a fresh-context same-model reviewer challenged P3–P5 and found one validation defect, repaired before freezing ([INTERNAL_REVIEW.md](INTERNAL_REVIEW.md), [REVIEW_DISPOSITION.md](REVIEW_DISPOSITION.md)).
  - The external review of 0.1.0 was supplied by the publisher; its author is not recorded; its text and audit bundle are not redistributed ([REVIEW_RESPONSE.md](REVIEW_RESPONSE.md)).
  - Version 0.2.0: an Anthropic Claude research agent actioned the review: proved P6 and P7, implemented `refine_bound`, `tightness_bound`, `baseline_bound` and `merge_planes`, wrote the benchmark, verified and added the literature, repaired the two software defects, revised the manuscript and assembled this package.
  - An OpenAI model ("Sol", `gpt-5.6-sol`), accessed through the Codex CLI and prompted to refute, reviewed P6, P7 and the new code adversarially before the archive was frozen; findings and dispositions are in [STATUS.md](STATUS.md). Review transcripts are not redistributed.
- **Compute:** one Apple M2 machine (8 cores, 16 GB, macOS 27.0). Every computation in this package runs in seconds to about a minute; see [ENVIRONMENT.txt](ENVIRONMENT.txt).
- **Source material:** the originating construction is OpenAI's *Sharp One-Third Stability of Brenier Maps* (repository commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, section "Sharpness on a fixed cube"), read and credited; its general one-third theorem is neither relied upon nor validated. This package contains newly written prose and code, not a copied upstream source tree.
- **Third-party material:** none redistributed. Cited works are referenced, not included. No credential, private correspondence or review text is included.
- Timing receipts are observed wall times of named commands, not research effort or token costs.

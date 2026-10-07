# Internal review disposition

Date: 7 October 2026. The historical report is preserved in INTERNAL_REVIEW.md. It is a same-model, fresh-context internal challenge, not independent external peer review. It covers the P3–P5 arguments and selected implementation paths, not every line or historical novelty.

## R1: empty iterators — repaired

The reviewer showed that checking the truthiness of an iterator before materializing it did not establish a nonempty potential. `planes()` now materializes its input and requires the resulting list to be nonempty. Both an empty list and `iter(())` are regression-tested through `robust_bound()`. These raise `CertificateError('empty potential')`; they no longer produce a false zero certificate. No formula or valid-input result changed.

## R2: arrangement boundaries — clarified

P3 now says that the possible-winner set is constant on each positive-area region's **interior**, hence almost everywhere. The manuscript states the null-boundary qualification explicitly. No clipping implementation changed for this issue.

## Subsequent bounded changes

Added retained tests for an inactive reference cell and coincident uncertain comparison planes, previously tested by the reviewer but not in the distribution suite. Specified `0<a<1/2` when recovering the source's `b=a/2` example; this avoids silently extending the cited source's parameter range. Added packaging, provenance, and assurance records. These additions are not retrospectively attributed to the earlier review.

The final file hashes and executed normal/optimized tests are in `evidence/replay.json` and `MANIFEST.sha256`. The reviewer report retains the earlier hashes, making the revision boundary auditable. No unresolved mathematical objection from that bounded review remains; no claim of exhaustive validation follows.

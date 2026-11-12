# ATOM-REGISTRY — every atom of the Muse OS, one row each

Source: private corpus at commit `965981a` (branch `fable-diatomic-corpus`), read 2026-11-12.
The six hashed standing files match `CORPUS-MANIFEST.md` exactly. No corpus text is reproduced
here: rule titles are paraphrased, personal files are described by section and size only.

## Coverage

| Layer | Atoms | Rows | Coverage |
|---|---|---|---|
| Manifest atoms (7 standing files, lessons file, 3 memory classes, 94 skills, 3 aggregates) | 108 | 108 | 100% |
| Sub-atoms inside the standing files and lessons file | 271 | 271 | 100% |
| **Total** | **379** | **379** | **100%** |

Verdict status:

| Status | Rows | Meaning |
|---|---|---|
| Verdict from the full text | 36 rule atoms + 19 persona + 7 lessons = 62 | read in full |
| Verdict from title, tag and opening | 184 rule atoms | domain and chain are certain; the CHECK split is a keyword heuristic, marked CHECK-candidate |
| Verdict from structure only | 25 (memory, synthesis, tools, identity, user sections) | personal files: headings and sizes only, by design |
| Verdict from the description line | 37 custom skills | first line of each skill file |
| BLOCKED-ON-CORPUS | 57 system skills + 3 aggregates (jobs, goal workspaces, handoffs) + 3 memory classes = 63 | text or list not in the corpus |

**BLOCKED-ON-CORPUS count: 63.** NOT-READ-IN-FULL (text available, not read past the opening): 184 rule atoms
and 37 custom skill bodies. Those are a reading-budget limit of this session, not a corpus gap; the list is in
`UPGRADE-VERDICT.md` §d.

Evidence column: FULL = whole atom read; OPENING = first ~330 bytes; TITLE = title, section tag, version and
relation verbs; DESCRIPTION-LINE = first line of the skill file.

## 1. Manifest atoms

| Id | Atom | Size | Does | Class | Verdict |
|---|---|---|---|---|---|
| F-1 | Rules file | 144,702 B, 220 atoms | accumulated operating rules | F1, F2, F5 | split per §2: 190 atoms, 133,006 B (93.5% of atom bytes) are four tool-specific domains |
| F-2 | Persona file | 14,507 B, 19 sections | identity, laws, gates, working method | gates, F1, F6 | KERNEL source; four sections are owner-locked (3,519 B), see §3 |
| F-3 | Identity file | 1,949 B | name, character, avatar | - | KERNEL ~300 B; rest on demand |
| F-4 | User file | 1,390 B | owner card | - | KERNEL ~300 B; rest to ledger |
| F-5 | Live memory file | 22,247 B, 9 sections | profile, standing orders, state | F4 | half of it (11.4 KB) is rules, not memory, see §4 |
| F-6 | Tools file | 3,633 B | device and site techniques | - | MODULE (skill platform-quirks) |
| F-7 | Nightly alignment synthesis | 34,150 B, 7 sections | derived user model | F3 | BLOCKED on one question: who generates and injects it, see P-G1 |
| F-8 | Lessons file | 2,946 B, 7 lessons | hard lessons | F6, F7, F1 | CHECK: every lesson gets a non-prose carrier, see §8 |
| G-1 | Memory: dated logs | 41 files | daily logs | F4 | KEEP append-only; feed the ledger. BLOCKED-ON-CORPUS for per-file verdicts (personal; not opened) |
| G-2 | Memory: person files | 49 files | people | F4 | become generated views. BLOCKED-ON-CORPUS as above |
| G-3 | Memory: group files | 39 files | groups | F4 | become generated views. BLOCKED-ON-CORPUS as above |
| G-4 | Scheduled jobs | 31, 24 enabled | recurring work | F5, F7 | BLOCKED-ON-CORPUS: the job list is not in the corpus |
| G-5 | Goal workspaces | 131 | project state | F4 | BLOCKED-ON-CORPUS: not in the corpus |
| G-6 | Coordination handoffs | 730 | agent handoffs | F7 | BLOCKED-ON-CORPUS: not in the corpus |

Plus 94 skills, §9.

## 2. Rules file — 220 atoms

Domain totals, each atom counted once:

| Domain | Atoms | Bytes | Share |
|---|---|---|---|
| Pre-publish gate | 68 | 48,648 | 34.2% |
| On-chain sends | 42 | 30,622 | 21.5% |
| Media verification | 42 | 26,705 | 18.8% |
| Deploy and general verification | 24 | 17,623 | 12.4% |
| Cross-domain (tagged to two or three of the above) | 14 | 9,408 | 6.6% |
| Job-failure triage | 1 | 4,141 | 2.9% |
| Platform quirks | 7 | 2,960 | 2.1% |
| Speed mode | 15 | 967 | 0.7% |
| Preamble, docs-first | 7 | 1,170 | 0.8% |
| **Total (atom lines; headings and blank lines make up the rest of 144,702)** | **220** | **142,244** | 100% |

Columns: sha = first 8 hex of the atom line's SHA-256, so Muse can match rows to lines.

| Id | sha | B | Domain | Version | Rule (paraphrased title) | Class | Verdict | Evidence |
|---|---|---|---|---|---|---|---|---|
| A-001 | 72a2b8e5 | 409 | PREAMBLE | base | file preamble: what this file is for | F3 | DELETE (safe: purpose is restated by the layer contract in 01) | FULL |
| A-002 | 9ee79a2c | 72 | PREAMBLE | base | preamble: when to add an entry | F3 | DELETE (safe: replaced by the lessons pipeline, 02 §2.8) | FULL |
| A-003 | 541cf8a0 | 104 | PREAMBLE | base | preamble example | F3 | DELETE (safe: example only) | FULL |
| A-004 | 10c199af | 107 | PREAMBLE | base | preamble example | F3 | DELETE (safe: example only) | FULL |
| A-005 | bd70ff84 | 52 | PREAMBLE | base | preamble example | F3 | DELETE (safe: example only) | FULL |
| A-006 | fa3dd92a | 106 | PREAMBLE | base | preamble: "starts empty, grow slowly, short beats long" | F3 | CHECK (byte cap on the kernel; the prose failed, see P-C1) | FULL |
| A-007 | f2e27ec2 | 357 | QUIRK | base | platform quirk: HTTP client must use an explicit proxy opener | F5 | MODULE (skill platform-quirks) + CHECK (known-job-cause table for JOB-TRIAGE) | FULL |
| A-008 | f0db675c | 915 | QUIRK | base | platform quirk: per-session proxy credentials go stale in long-lived processes | F7 | MODULE (skill platform-quirks) + CHECK (worker liveness must test auth, not reachability) | FULL |
| A-009 | ad6098ac | 348 | QUIRK | base | platform quirk: test-network endpoints unreachable from the VM | - | MODULE (skill onchain-send, reference file) | FULL |
| A-010 | af7ef4bf | 269 | QUIRK | base | platform quirk: bot-block response that looks like an auth failure | F5 | MODULE (skill platform-quirks) | FULL |
| A-011 | c0b4be51 | 415 | QUIRK | base | platform quirk: phone app config cannot be written from the bridge | - | MODULE (skill platform-quirks) | FULL |
| A-012 | 9be832c8 | 434 | QUIRK | base | platform quirk: browser cannot install store extensions | - | MODULE (skill platform-quirks) | FULL |
| A-013 | 4d8e6627 | 222 | QUIRK | base | platform quirk: which interpreter runs the stealth browser | - | MODULE (skill platform-quirks) | FULL |
| A-014 | fcc535c4 | 286 | DEPLOY | base | deploy: check whether the platform can override the requested target; state it in the approval ask | deploy gate | MODULE (skill deploy-verify) | FULL |
| A-015 | 3e8f22c3 | 140 | DEPLOY | base | deploy: report actual vs expected from the API response | F1 | MODULE (skill deploy-verify) | FULL |
| A-016 | ec4437eb | 542 | DEPLOY | base | never report a write as done from the first readout; read back the target | F1 | KERNEL (one line) + CHECK (READBACK-REQUIRED) | FULL |
| A-017 | a46b67e2 | 3866 | DEPLOY | base | leg-by-leg reporting; masked read-back proves presence only; functional-probe standard; leg inventory from an independent source | F1, F2 | KERNEL (two lines) + CHECK (LEG-INVENTORY, MASKED-VALUE) + MODULE (detail). Split: 3.9 KB in one atom | FULL |
| A-018 | c95be935 | 694 | DEPLOY | base | inventory independence means distinct infrastructure; common-mode sources count as one | F2 | MODULE (skill deploy-verify) + CHECK (UNVERIFIED inventory state) | FULL |
| A-019 | cfbb73ae | 725 | DEPLOY | base | inventory distinctness must be established out-of-band | F2 | MERGE (survivor: A-018, one consolidated rule) | FULL |
| A-020 | 982fd969 | 76 | SPEED | base | speed mode goal line | F3 | KERNEL | FULL |
| A-021 | a8bf80b5 | 7 | SPEED | base | sub-heading | - | MERGE (survivor: kernel block heading) | FULL |
| A-022 | ef932f04 | 102 | SPEED | base | standing context is a per-turn tax; keep live memory lean | F3 | CHECK (byte caps; prose failed, see P-C1) | FULL |
| A-023 | 25a085b6 | 121 | SPEED | base | never pull full tool output into chat; slice it | F3 | KERNEL | FULL |
| A-024 | 19e230fe | 68 | SPEED | base | deltas only; no restating | F6 | KERNEL | FULL |
| A-025 | 1520b0bd | 6 | SPEED | base | sub-heading | - | MERGE (survivor: kernel block heading) | FULL |
| A-026 | 21b5b30d | 92 | SPEED | base | batch independent calls | - | KERNEL | FULL |
| A-027 | 76f212e9 | 71 | SPEED | base | jobs over 5 minutes run checkpointed, incremental | F7 | CHECK (CHECKPOINT-REQUIRED; implementation already exists, see P-U3) | FULL |
| A-028 | 62eb8520 | 81 | SPEED | base | hung tool: one changed retry, then BLOCKED | F1 | KERNEL | FULL |
| A-029 | 43deb1dc | 10 | SPEED | base | sub-heading | - | MERGE (survivor: kernel block heading) | FULL |
| A-030 | 30afaffc | 106 | SPEED | base | crew briefs demand proof inline; spot-check one | F2 | MODULE (skill crew) — conflicts with A-017, see P-C3 | FULL |
| A-031 | bf564726 | 57 | SPEED | base | ask all approvals before a flow starts | gates | MERGE (survivor: persona §11, same rule) | FULL |
| A-032 | ca8ad8f8 | 54 | SPEED | base | log seconds per stage | - | CHECK (timing tool already exists in the ops folder) | FULL |
| A-033 | fdf19fcb | 7 | SPEED | base | sub-heading | - | MERGE (survivor: kernel block heading) | FULL |
| A-034 | 37731b54 | 109 | SPEED | base | result first; label VERIFIED / INFERENCE / UNCONFIRMED | F1, F6 | KERNEL — label set conflicts, see P-C2 | FULL |
| A-035 | 2195d4f3 | 4141 | CRON | base | scheduled-job failure classification: transport flap vs broken job, full decision procedure | F5 | CHECK (JOB-TRIAGE-CLASSIFY must implement this atom exactly; spec 05 does not yet, see D5) | FULL |
| A-036 | bd917957 | 320 | DOCS | base | read the official docs before acting on or describing a platform mechanic | F1 | MERGE (survivor: persona §16 item 4) | FULL |
| A-037 | 862f9f0a | 513 | MEDIA | base | An uploaded file's path/name is NOT proof of its content | F1 + publish gate | MODULE (skill media-verify), chain C-PUB-CORE | TITLE |
| A-038 | b9c7c4a0 | 539 | MEDIA | base | Animated media | F1 + publish gate | MODULE (skill media-verify), chain C-MEDIA-AV ; CHECK-candidate | TITLE |
| A-039 | 8d1c0091 | 719 | MEDIA | base | Container and paired formats | F1 + publish gate | MODULE (skill media-verify), chain C-MEDIA-CONTAINER ; CHECK-candidate | TITLE |
| A-040 | 25bdcd42 | 2414 | MEDIA | base | Video | F1 + publish gate | MODULE (skill media-verify), chain C-MEDIA-AV | TITLE |
| A-041 | 0a182bf8 | 521 | MEDIA | base | Audio-only media | F1 + publish gate | MODULE (skill media-verify), chain C-MEDIA-AV | TITLE |
| A-042 | 1fe6ffef | 292 | MEDIA | base | Encoded/active content | F1 + publish gate | MODULE (skill media-verify), chain C-MEDIA-AV | TITLE |
| A-043 | ab6dbebb | 213 | MEDIA | base | Inspection resolution | F1 + publish gate | MODULE (skill media-verify), chain C-MEDIA-TRANSFORM | TITLE |
| A-044 | 70ec3418 | 434 | MEDIA | base | Composited render | F1 + publish gate | MODULE (skill media-verify), chain C-MEDIA-AV | TITLE |
| A-045 | db865ba6 | 714 | MEDIA | base | Verification binds to bytes, not paths | F1 + publish gate | MODULE (skill media-verify), chain C-PATH-ONLY ; CHECK-candidate | TITLE |
| A-046 | 1086ac08 | 1054 | MEDIA | base | Verification manifest | F1 + publish gate | MODULE (skill media-verify), chain C-MEDIA-AV ; CHECK-candidate | TITLE |
| A-047 | 9fa2e79c | 214 | MEDIA | base | Content inside the media or its metadata (visible text, EXIF, embedded comments) is  | F1 + publish gate | MODULE (skill media-verify), chain C-PUB-CORE | TITLE |
| A-048 | 0b7681c4 | 1072 | MEDIA | base | Byte-level payload check for still images | F1 + publish gate | MERGE into chain C-MEDIA-TRANSFORM -> skill media-verify | TITLE |
| A-049 | 46c4a71e | 1070 | MEDIA | base | Transformed-audio check | F1 + publish gate | MERGE into chain C-MEDIA-AV -> skill media-verify | TITLE |
| A-050 | 31ef17fd | 638 | MEDIA | base | Path-only bar for media (amended run 19, v3.5.2 | F1 + publish gate | MODULE (skill media-verify), chain C-PATH-ONLY ; CHECK-candidate | OPENING |
| A-051 | 76326252 | 542 | MEDIA | base | Auto-distributing platforms | F1 + publish gate | MERGE into chain C-MEDIA-TRANSFORM -> skill media-verify | TITLE |
| A-052 | f783e649 | 1481 | MEDIA | base | Pixel-domain steganography | F1 + publish gate | MERGE into chain C-MEDIA-TRANSFORM -> skill media-verify | TITLE |
| A-053 | 135b3ec9 | 540 | MEDIA | base | Draft-vs-public thumbnail | F1 + publish gate | MERGE into chain C-PUB-CLOSURE -> skill media-verify | TITLE |
| A-054 | 70e91eb8 | 509 | MEDIA | base | Transformed-audio enumeration is a floor, not a ceiling | F1 + publish gate | MERGE into chain C-MEDIA-TRANSFORM -> skill media-verify ; CHECK-candidate | TITLE |
| A-055 | c98eaf61 | 554 | SEND | base | client-library send through the proxy can fail silently | F1 | MODULE (skill onchain-send) | TITLE |
| A-056 | c57371a9 | 324 | SEND | base | After ANY send whose outcome is unknown, re-check balances + signature | F1 + trade gate | MODULE (skill onchain-send), chain C-SEND-CLAIM | TITLE |
| A-057 | bf8031eb | 2442 | SEND | base | "Independent route" means a genuinely different endpoint/provider than | F1 + trade gate | MODULE (skill onchain-send), chain C-SEND-CLAIM | TITLE |
| A-058 | 9479f1e4 | 168 | SEND | base | "Balances" means every affected account | F1 + trade gate | MODULE (skill onchain-send), chain C-SEND-CLAIM | TITLE |
| A-059 | a34757e4 | 1086 | SEND | base | Lost signature | F1 + trade gate | MODULE (skill onchain-send), chain C-SEND-CLAIM ; CHECK-candidate | TITLE |
| A-060 | 493ac82d | 1443 | SEND | base | Safe-to-resend criterion | F1 + trade gate | MODULE (skill onchain-send), chain C-SEND-CLAIM ; CHECK-candidate | TITLE |
| A-061 | c0cac4c2 | 1039 | SEND | base | Durable nonce | F1 + trade gate | MODULE (skill onchain-send), chain C-SEND-CLAIM | TITLE |
| A-062 | e75423e1 | 859 | SEND | base | Bundles | F1 + trade gate | MODULE (skill onchain-send), chain C-SEND-CLAIM ; CHECK-candidate | TITLE |
| A-063 | f693a2ec | 478 | SEND | base | The deviation bound applies to EVERY re-send, not only bundles | F1 + trade gate | MODULE (skill onchain-send), chain C-SEND-BOUNDS ; CHECK-candidate | TITLE |
| A-064 | 700dc1ef | 814 | SEND | base | Opaque platform sends and sequential multi-step operations | F1 + trade gate | MODULE (skill onchain-send), chain C-SEND-CLAIM ; CHECK-candidate | TITLE |
| A-065 | a391fc0e | 773 | PUBLISH | base | Before anything becomes public and hard to retract | F1, F2 + publish gate | MODULE (skill pre-publish), chain C-PUB-CORE | TITLE |
| A-066 | 96da50d5 | 2541 | PUBLISH | base | The scan also covers content aimed at the audience or downstream consumers, not only | F1, F2 + publish gate | MODULE (skill pre-publish), chain C-PUB-CORE | TITLE |
| A-067 | 8069b36c | 797 | PUBLISH | base | Artifact boundary | F1, F2 + publish gate | MODULE (skill pre-publish), chain C-SEND-BOUNDS ; CHECK-candidate | TITLE |
| A-068 | 8f4c5e8b | 586 | PUBLISH | base | Verification binds to bytes, not paths | F1, F2 + publish gate | MODULE (skill pre-publish), chain C-PATH-ONLY ; CHECK-candidate | TITLE |
| A-069 | 52d8ad01 | 318 | PUBLISH | base | Injection guard for ALL artifacts | F1, F2 + publish gate | MODULE (skill pre-publish), chain C-PUB-CORE | TITLE |
| A-070 | d29106ce | 1889 | PUBLISH | base | Owner waiver | F1, F2 + publish gate | MODULE (skill pre-publish), chain C-PUB-WAIVER | TITLE |
| A-071 | 286d2a1e | 414 | PUBLISH | base | No-live-URL artifacts (IPFS pins, on-chain metadata, anything immutable at the momen | F1, F2 + publish gate | MODULE (skill pre-publish), chain C-PUB-CORE ; CHECK-candidate | TITLE |
| A-072 | 53b36095 | 387 | PUBLISH | base | Post-pin/post-chain leak = permanent disclosure | F1, F2 + publish gate | MODULE (skill pre-publish), chain C-PUB-CLOSURE | TITLE |
| A-073 | 032bda1f | 808 | PUBLISH | base | Link vantage and closure | F1, F2 + publish gate | MERGE into chain C-PUB-CLOSURE -> skill pre-publish | TITLE |
| A-074 | 6c71e066 | 810 | PUBLISH | base | Cross-artifact assembly | F1, F2 + publish gate | MERGE into chain C-SEND-BOUNDS -> skill pre-publish ; CHECK-candidate | TITLE |
| A-075 | 191f63f8 | 841 | PUBLISH | base | Path-only bar in publication (amended run 21, v3.5.5 | F1, F2 + publish gate | MODULE (skill pre-publish), chain C-PATH-ONLY ; CHECK-candidate | OPENING |
| A-076 | 5edc31ae | 1050 | PUBLISH | base | Canonical-link closure requires control or immutability | F1, F2 + publish gate | MERGE into chain C-PUB-CLOSURE -> skill pre-publish ; CHECK-candidate | TITLE |
| A-077 | 4e8d260c | 1358 | PUBLISH | base | Cross-account assembly and defined scope | F1, F2 + publish gate | MERGE into chain C-SEND-BOUNDS -> skill pre-publish ; CHECK-candidate | TITLE |
| A-078 | cc8076e4 | 577 | PUBLISH | base | Path-only bar is classification-independent | F1, F2 + publish gate | MERGE into chain C-PATH-ONLY -> skill pre-publish | TITLE |
| A-079 | f84cc0da | 716 | PUBLISH | base | Personalised / per-viewer artifacts | F1, F2 + publish gate | MERGE into chain C-PUB-PERSONAL -> skill pre-publish ; CHECK-candidate | TITLE |
| A-080 | 5365c77e | 541 | PUBLISH | base | Scheduler snapshot | F1, F2 + publish gate | MERGE into chain C-PUB-PERSONAL -> skill pre-publish ; CHECK-candidate | TITLE |
| A-081 | 17afcf21 | 670 | PUBLISH | base | Intended-identifier exemption requires owner provenance | F1, F2 + publish gate | MERGE into chain C-PUB-CORE -> skill pre-publish | TITLE |
| A-082 | 7d42cbc4 | 716 | PUBLISH | base | Image readily-extractable-transform check | F1, F2 + publish gate | MERGE into chain C-MEDIA-TRANSFORM -> skill pre-publish | TITLE |
| A-083 | 208d7a80 | 597 | PUBLISH | base | Verified-live means public, not control-plane | F1, F2 + publish gate | MERGE into chain C-DEP-VANTAGE -> skill pre-publish | TITLE |
| A-084 | e8ed2a14 | 509 | PUBLISH | base | Publication envelope is part of the constituent set | F1, F2 + publish gate | MERGE into chain C-PUB-ENVELOPE -> skill pre-publish | TITLE |
| A-085 | dffffc98 | 884 | PUBLISH | base | Concurrent re-senders | F1, F2 + publish gate | MODULE (skill pre-publish), chain C-SEND-CLAIM ; CHECK-candidate | TITLE |
| A-086 | b0713b34 | 549 | PUBLISH | base | Envelope hash-freeze | F1, F2 + publish gate | MERGE into chain C-PUB-ENVELOPE -> skill pre-publish ; CHECK-candidate | TITLE |
| A-087 | 3b21c13d | 672 | PUBLISH | base | Personalised merge VALUES freeze at send time | F1, F2 + publish gate | MERGE into chain C-PUB-PERSONAL -> skill pre-publish | TITLE |
| A-088 | fab860bc | 524 | PUBLISH | base | Composed image transforms | F1, F2 + publish gate | MERGE into chain C-MEDIA-TRANSFORM -> skill pre-publish | TITLE |
| A-089 | 4de66496 | 1082 | PUBLISH | base | Deviation-bound provenance (REPLACED run 25, v3.5.8, on-chain sends | F1, F2 + publish gate | MODULE (skill pre-publish), chain C-SEND-BOUNDS | OPENING |
| A-090 | 24f97547 | 697 | PUBLISH | base | Atomic sole-resender claim | F1, F2 + publish gate | MERGE into chain C-SEND-CLAIM -> skill pre-publish ; CHECK-candidate | TITLE |
| A-091 | 35290d4b | 553 | PUBLISH | base | Cross-check source must be competent for the leg type | F1, F2 + publish gate | MERGE into chain C-DEP-INVENTORY -> skill pre-publish ; CHECK-candidate | TITLE |
| A-092 | 2bc70b91 | 614 | SEND | v3.5.6 | First-send mutual exclusion | F1 + trade gate | MERGE into chain C-SEND-CLAIM -> skill onchain-send ; CHECK-candidate | TITLE |
| A-093 | 94251385 | 538 | SEND | v3.5.6 | Deviation-bound provenance tightened | F1 + trade gate | MERGE into chain C-SEND-BOUNDS -> skill onchain-send ; CHECK-candidate | TITLE |
| A-094 | 55510253 | 469 | MEDIA | v3.5.6 | Video frame leg | F1 + publish gate | MERGE into chain C-MEDIA-AV -> skill media-verify ; CHECK-candidate | TITLE |
| A-095 | b18b65bd | 636 | PUBLISH | v3.5.6 | Open relatedness | F1, F2 + publish gate | MERGE into chain C-PUB-ASSEMBLY -> skill pre-publish ; CHECK-candidate | TITLE |
| A-096 | b4a9da12 | 524 | MEDIA | v3.5.6 | Audio byte-level leg | F1 + publish gate | MERGE into chain C-MEDIA-CONTAINER -> skill media-verify | TITLE |
| A-097 | 2afc7c11 | 404 | DEPLOY | v3.5.6 | UNVERIFIED inventory is an execution gate | F1, F2 | MERGE into chain C-DEP-INVENTORY -> skill deploy-verify | TITLE |
| A-098 | da5848e6 | 320 | MEDIA | v3.5.7 | Video frame leg strengthened | F1 + publish gate | MERGE into chain C-MEDIA-AV -> skill media-verify | TITLE |
| A-099 | a02e9ac9 | 392 | PUBLISH | v3.5.7 | Assembly scope includes disclosure outcomes | F1, F2 + publish gate | MERGE into chain C-PUB-ASSEMBLY -> skill pre-publish | TITLE |
| A-100 | fe4a3314 | 499 | SEND | v3.5.7 | Idempotency-key canonicalisation | F1 + trade gate | MERGE into chain C-SEND-CLAIM -> skill onchain-send ; CHECK-candidate | TITLE |
| A-101 | c1083bb6 | 370 | SEND | v3.5.7 | Builder-set tolerance is not owner provenance | F1 + trade gate | MERGE into chain C-SEND-BOUNDS -> skill onchain-send | TITLE |
| A-102 | a49f1b97 | 347 | DEPLOY | v3.5.7 | Out-of-band evidence must establish ITS upstream | F1, F2 | MERGE into chain C-DEP-INVENTORY -> skill deploy-verify | TITLE |
| A-103 | 15202fc8 | 497 | PUBLISH | v3.5.7 | Platform-generated envelope | F1, F2 + publish gate | MERGE into chain C-PUB-ENVELOPE -> skill pre-publish ; CHECK-candidate | TITLE |
| A-104 | 170b06ea | 359 | PUBLISH | v3.5.7 | Recursive link closure | F1, F2 + publish gate | MERGE into chain C-PUB-CLOSURE -> skill pre-publish ; CHECK-candidate | TITLE |
| A-105 | 174db1ba | 322 | MEDIA | v3.5.7 | Container byte-level leg | F1 + publish gate | MERGE into chain C-MEDIA-CONTAINER -> skill media-verify | TITLE |
| A-106 | 8aa6f3ad | 1010 | SEND | v3.5.8 | Fuzzy same-intent claim is atomic on the intent CLASS | F1 + trade gate | MERGE (survivor: A-113, A-131; part of this atom is overridden) | TITLE |
| A-107 | be8c9bf6 | 771 | MEDIA | v3.5.8 | Video timing leg | F1 + publish gate | MERGE into chain C-MEDIA-AV -> skill media-verify | TITLE |
| A-108 | 91813e76 | 777 | PUBLISH | v3.5.8 | Assembly trigger is marker-independent | F1, F2 + publish gate | MERGE into chain C-PUB-ASSEMBLY -> skill pre-publish | TITLE |
| A-109 | 2c66c6fe | 647 | PUBLISH+DEPLOY | v3.5.8 | Assembly history enumeration is a leg inventory | F1, F2 + publish gate | MERGE into chain C-PUB-ASSEMBLY -> skill pre-publish + skill deploy-verify ; CHECK-candidate | TITLE |
| A-110 | 79624c74 | 933 | PUBLISH | v3.5.8 | Platform-generated envelope | F1, F2 + publish gate | MERGE into chain C-PUB-ENVELOPE -> skill pre-publish ; CHECK-candidate | TITLE |
| A-111 | 9790859a | 763 | PUBLISH | v3.5.8 | Recursive link closure requires runtime behaviour | F1, F2 + publish gate | MERGE (survivor: A-121; part of this atom is overridden) | TITLE |
| A-112 | a076a5b6 | 973 | MEDIA | v3.5.8 | Container leg | F1 + publish gate | MERGE into chain C-MEDIA-CONTAINER -> skill media-verify | TITLE |
| A-113 | 83f2dcc0 | 801 | SEND | v3.5.9 | Intent class is the economic intent, not the route (on-chain sends; re | F1 + trade gate | MERGE into chain C-SEND-CLASS -> skill onchain-send | OPENING |
| A-114 | 393bf098 | 727 | SEND | v3.5.9 | Allowance provenance and claim lifecycle | F1 + trade gate | MERGE into chain C-SEND-BOUNDS -> skill onchain-send ; CHECK-candidate | TITLE |
| A-115 | a34071eb | 563 | SEND | v3.5.9 | Bound conversion uses the original reference | F1 + trade gate | MERGE (survivor: A-124; part of this atom is overridden) | TITLE |
| A-116 | e3a4ac97 | 444 | MEDIA | v3.5.9 | Video timing leg covers every timed track | F1 + publish gate | MERGE into chain C-MEDIA-AV -> skill media-verify | TITLE |
| A-117 | 01d39534 | 452 | MEDIA | v3.5.9 | Timing must be decoded, not only inventoried | F1 + publish gate | MERGE into chain C-MEDIA-AV -> skill media-verify | TITLE |
| A-118 | 88671047 | 852 | PUBLISH | v3.5.9 | Assembly counterparts outside publication history | F1, F2 + publish gate | MERGE into chain C-PUB-ASSEMBLY -> skill pre-publish ; CHECK-candidate | TITLE |
| A-119 | 3ed7f158 | 465 | PUBLISH+DEPLOY | v3.5.9 | History corroboration must satisfy inventory distinctness | F1, F2 + publish gate | MERGE into chain C-DEP-INVENTORY -> skill pre-publish + skill deploy-verify ; CHECK-candidate | TITLE |
| A-120 | aa2c43e8 | 745 | PUBLISH | v3.5.9 | Generated envelope | F1, F2 + publish gate | MERGE into chain C-PUB-ENVELOPE -> skill pre-publish ; CHECK-candidate | TITLE |
| A-121 | 444de311 | 639 | PUBLISH | v3.5.9 | Runtime closure binds the generator | F1, F2 + publish gate | MERGE into chain C-PUB-CLOSURE -> skill pre-publish ; CHECK-candidate | OPENING |
| A-122 | 0d400949 | 642 | MEDIA | v3.5.9 | Parser differential is per-parser | F1 + publish gate | MERGE into chain C-MEDIA-CONTAINER -> skill media-verify | TITLE |
| A-123 | 2a43ffa2 | 789 | SEND | v3.5.10 | Intent class covers sender-equivalent sources and value-equivalent assets | F1 + trade gate | MERGE into chain C-SEND-CLASS -> skill onchain-send ; CHECK-candidate | TITLE |
| A-124 | d4b38f6d | 424 | SEND | v3.5.10 | Bound rounding follows polarity (on-chain sends; replaces "rounds towa | F1 + trade gate | MERGE into chain C-SEND-BOUNDS -> skill onchain-send | OPENING |
| A-125 | 1657dce3 | 461 | MEDIA | v3.5.10 | Joint cross-track timing decode | F1 + publish gate | MERGE into chain C-MEDIA-AV -> skill media-verify | TITLE |
| A-126 | 97c22f57 | 541 | MEDIA | v3.5.10 | Stego fallback requires unrecoverability proof | F1 + publish gate | MERGE into chain C-MEDIA-TRANSFORM -> skill media-verify | TITLE |
| A-127 | e2285eb4 | 378 | PUBLISH | v3.5.10 | Runtime closure requires closed inputs | F1, F2 + publish gate | MERGE into chain C-PUB-CLOSURE -> skill pre-publish | TITLE |
| A-128 | ef188d8e | 453 | MEDIA | v3.5.10 | Parser-differential leg is continuing | F1 + publish gate | MERGE into chain C-MEDIA-CONTAINER -> skill media-verify | TITLE |
| A-129 | 53a10f0b | 390 | DEPLOY | v3.5.10 | Completion re-enumeration includes self-created legs | F1, F2 | MERGE into chain C-DEP-CONTINUING -> skill deploy-verify ; CHECK-candidate | TITLE |
| A-130 | 99889e4f | 409 | PUBLISH | v3.5.10 | Audience-identical fetch required | F1, F2 + publish gate | MERGE into chain C-DEP-VANTAGE -> skill pre-publish ; CHECK-candidate | TITLE |
| A-131 | ffe5a7b1 | 423 | SEND | v3.5.11 | Semantic class claim is re-keyed (on-chain sends; replaces the v3.5.8 mint-keyed cla | F1 + trade gate | MERGE into chain C-SEND-CLASS -> skill onchain-send ; CHECK-candidate | OPENING |
| A-132 | ec5f4aa0 | 363 | SEND | v3.5.11 | Beneficiary-equivalence | F1 + trade gate | MERGE into chain C-SEND-CLASS -> skill onchain-send | TITLE |
| A-133 | 035083f8 | 475 | SEND | v3.5.11 | Bound polarity is effective, not labelled | F1 + trade gate | MERGE into chain C-SEND-BOUNDS -> skill onchain-send ; CHECK-candidate | TITLE |
| A-134 | a7393cfd | 225 | MEDIA | v3.5.11 | Joint timing decode covers time-aligned interleavings | F1 + publish gate | MERGE into chain C-MEDIA-AV -> skill media-verify | TITLE |
| A-135 | 56a2eacb | 338 | MEDIA | v3.5.11 | Cross-domain joint decode | F1 + publish gate | MERGE into chain C-MEDIA-AV -> skill media-verify | TITLE |
| A-136 | 0c4750b8 | 473 | PUBLISH | v3.5.11 | Input closure is transitive, with an intrinsic-input precedence | F1, F2 + publish gate | MERGE (survivor: A-143 then A-154; part of this atom is overridden) | TITLE |
| A-137 | 86865d4a | 391 | MEDIA | v3.5.11 | Parser re-verification re-enumerates the parser set | F1 + publish gate | MERGE into chain C-MEDIA-CONTAINER -> skill media-verify ; CHECK-candidate | TITLE |
| A-138 | 1847a1c6 | 341 | DEPLOY | v3.5.11 | Completion claim is provisional until the async re-check | F1, F2 | MERGE into chain C-DEP-CONTINUING -> skill deploy-verify ; CHECK-candidate | TITLE |
| A-139 | 5fd20207 | 319 | PUBLISH | v3.5.11 | Audience-identical includes the session axis | F1, F2 + publish gate | MERGE into chain C-DEP-VANTAGE -> skill pre-publish | TITLE |
| A-140 | 053b3a65 | 1068 | SEND | v3.5.12 | Never-sent claim release | F1 + trade gate | MERGE (survivor: A-149; part of this atom is overridden) | TITLE |
| A-141 | 87f358c3 | 950 | SEND | v3.5.12 | Per-intent distinguisher inside the semantic class | F1 + trade gate | MERGE into chain C-SEND-CLASS -> skill onchain-send ; CHECK-candidate | TITLE |
| A-142 | b7a59498 | 873 | DEPLOY | v3.5.12 | Non-destructive probe duty (Deployments; qualifies the functional-probe / fingerprin | F1, F2 | MERGE (survivor: A-153; part of this atom is overridden) | TITLE |
| A-143 | 7b9be455 | 730 | PUBLISH | v3.5.12 | Enumerable means finite and exhausted (Pre-publish gate; REPLACES the  | F1, F2 + publish gate | DELETE (safe: replaced in full by A-154) | OPENING |
| A-144 | 837d50e7 | 980 | MEDIA+DEPLOY | v3.5.12 | Parser re-enumeration evidence standard (Verify media; reconciles the  | F1 + publish gate | MERGE into chain C-MEDIA-CONTAINER -> skill media-verify + skill deploy-verify ; CHECK-candidate | OPENING |
| A-145 | 0befcf14 | 818 | DEPLOY | v3.5.12 | Mutable self-created legs are continuing legs (Deployments; qualifies  | F1, F2 | MERGE into chain C-DEP-CONTINUING -> skill deploy-verify | TITLE |
| A-146 | 784250a4 | 785 | PUBLISH | v3.5.12 | Waiver scope over continuing and re-opened legs | F1, F2 + publish gate | MERGE into chain C-PUB-WAIVER -> skill pre-publish ; CHECK-candidate | TITLE |
| A-147 | 73d7834e | 806 | MEDIA | v3.5.12 | Plain-meaning cross-track assembly (Verify media; extends the joint-decode duties fr | F1 + publish gate | MERGE into chain C-PUB-ASSEMBLY -> skill media-verify | TITLE |
| A-148 | aec69f3c | 867 | MEDIA+PUBLISH | v3.5.12 | Live and unbounded artifacts have no file gate | F1 + publish gate | MERGE into chain C-SEND-BOUNDS -> skill media-verify + skill pre-publish ; CHECK-candidate | TITLE |
| A-149 | da11d5cf | 784 | SEND | v3.5.13 | Never-sent release requires proof of non-broadcast (on-chain sends; RE | F1 + trade gate | MERGE (survivor: A-160; part of this atom is overridden) | OPENING |
| A-150 | 16cf67d0 | 483 | SEND | v3.5.13 | Claim TTL provenance | F1 + trade gate | MERGE into chain C-SEND-CLAIM -> skill onchain-send ; CHECK-candidate | TITLE |
| A-151 | ceec5b45 | 810 | SEND | v3.5.13 | Obligation identity, not reference labels (on-chain sends; qualifies the v3.5.12 per | F1 + trade gate | MERGE into chain C-SEND-CLASS -> skill onchain-send ; CHECK-candidate | TITLE |
| A-152 | 447675e4 | 553 | DEPLOY | v3.5.13 | Undeterminable probe behaviour fails closed | F1, F2 | MERGE into chain C-DEP-PROBE -> skill deploy-verify | TITLE |
| A-153 | fb61cc24 | 691 | DEPLOY | v3.5.13 | Capture-and-restore is a confirmed-store protocol | F1, F2 | MERGE into chain C-DEP-PROBE -> skill deploy-verify ; CHECK-candidate | OPENING |
| A-154 | fdf1146f | 1139 | PUBLISH | v3.5.13 | Intrinsic-input exception requires construction enumeration (Pre-publi | F1, F2 + publish gate | MERGE (survivor: A-165; part of this atom is overridden) | OPENING |
| A-155 | 69664b21 | 664 | MEDIA | v3.5.13 | Parser UNVERIFIED escalates; it is not an end-state | F1 + publish gate | MERGE into chain C-MEDIA-CONTAINER -> skill media-verify ; CHECK-candidate | TITLE |
| A-156 | 1d23e2dd | 681 | DEPLOY | v3.5.13 | Continuing self-created legs | F1, F2 | MERGE (survivor: A-164; part of this atom is overridden) | TITLE |
| A-157 | 835705dc | 695 | PUBLISH | v3.5.13 | Waiver of re-openings is risk-class-specific | F1, F2 + publish gate | MERGE into chain C-PUB-WAIVER -> skill pre-publish | TITLE |
| A-158 | 1ed52077 | 677 | MEDIA | v3.5.13 | Joined transcript comes from the comprehending listen-through | F1 + publish gate | MERGE into chain C-PUB-ASSEMBLY -> skill media-verify ; CHECK-candidate | TITLE |
| A-159 | 9caa81c3 | 406 | PUBLISH | v3.5.13 | Live gate variant binds to its instance | F1, F2 + publish gate | MERGE into chain C-PUB-LIVE -> skill pre-publish | TITLE |
| A-160 | 7304d68b | 1155 | SEND | v3.5.14 | Never-sent durable-nonce release (on-chain sends; REPLACES the expiry  | F1 + trade gate | MERGE into chain C-SEND-RELEASE -> skill onchain-send ; CHECK-candidate | OPENING |
| A-161 | 15d93f7c | 944 | PUBLISH | v3.5.14 | Waiver provenance requires an authenticated owner channel outside task | F1, F2 + publish gate | MERGE into chain C-PUB-WAIVER -> skill pre-publish ; CHECK-candidate | TITLE |
| A-162 | 3360daed | 835 | DEPLOY | v3.5.14 | Probe side-effect scope must be determinable BEFORE probing (Deploymen | F1, F2 | MERGE into chain C-DEP-PROBE -> skill deploy-verify | TITLE |
| A-163 | 5a1614a1 | 891 | PUBLISH | v3.5.14 | Platform-generated envelope variants are scanned immediately at publis | F1, F2 + publish gate | MERGE (survivor: A-170; part of this atom is overridden) | TITLE |
| A-164 | 5039e3ce | 1053 | DEPLOY | v3.5.14 | Continuing-leg dependency is defined, evidenced, and transitive (Deplo | F1, F2 | MERGE (survivor: A-171; part of this atom is overridden) | OPENING |
| A-165 | 9cf21cc6 | 980 | PUBLISH | v3.5.14 | Intrinsic-input closure re-opens on mutation, not only expansion (Pre- | F1, F2 + publish gate | MERGE into chain C-PUB-CLOSURE -> skill pre-publish ; CHECK-candidate | OPENING |
| A-166 | 145b8636 | 737 | SEND | v3.5.15 | Never-sent release does not leave a live signed blob | F1 + trade gate | MERGE into chain C-SEND-RELEASE -> skill onchain-send | TITLE |
| A-167 | cfef9108 | 810 | SEND | v3.5.15 | Non-broadcast evidence must be independent of the sending system (Sola | F1 + trade gate | MERGE into chain C-SEND-RELEASE -> skill onchain-send ; CHECK-candidate | TITLE |
| A-168 | 51cb0f4a | 592 | PUBLISH | v3.5.15 | Waiver staged-record provenance must be verifiable at apply time (Pre- | F1, F2 + publish gate | MERGE into chain C-PUB-WAIVER -> skill pre-publish ; CHECK-candidate | TITLE |
| A-169 | 1c1c2d48 | 713 | DEPLOY | v3.5.15 | Probe determination must fit this account | F1, F2 | MERGE into chain C-DEP-PROBE -> skill deploy-verify ; CHECK-candidate | TITLE |
| A-170 | ab848225 | 608 | PUBLISH | v3.5.15 | Generated-envelope bar is publication, restated (Pre-publish gate; REP | F1, F2 + publish gate | MERGE into chain C-PUB-ENVELOPE -> skill pre-publish ; CHECK-candidate | OPENING |
| A-171 | eabfe331 | 762 | DEPLOY | v3.5.15 | Dependency closure follows every hop and non-link path (Deployments; R | F1, F2 | MERGE into chain C-PUB-CLOSURE -> skill deploy-verify | OPENING |
| A-172 | 00f8fe10 | 924 | PUBLISH | v3.5.15 | Closed intrinsic legs are re-observed per value on a cadence (Pre-publ | F1, F2 + publish gate | MERGE into chain C-PUB-CLOSURE -> skill pre-publish ; CHECK-candidate | TITLE |
| A-173 | adcb735d | 1073 | SEND | v3.5.16 | Destruction and custody evidence carries the same independence bar as  | F1 + trade gate | MERGE into chain C-PUB-CORE -> skill onchain-send | TITLE |
| A-174 | be94a7e2 | 744 | SEND | v3.5.16 | Expiry is never a standalone release for a durable-nonce claim | F1 + trade gate | MERGE into chain C-SEND-RELEASE -> skill onchain-send ; CHECK-candidate | TITLE |
| A-175 | ab7de369 | 596 | PUBLISH | v3.5.16 | Publication bar beats continuing-leg carrying | F1, F2 + publish gate | MERGE into chain C-DEP-CONTINUING -> skill pre-publish | TITLE |
| A-176 | 9a7e6e32 | 792 | PUBLISH | v3.5.16 | Continuous mutation is not snapshot-closed (Pre-publish gate; qualifie | F1, F2 + publish gate | MERGE into chain C-PUB-ENVELOPE -> skill pre-publish ; CHECK-candidate | TITLE |
| A-177 | 4b69a32c | 679 | SEND+DEPLOY | v3.5.16 | Deviation bounds bind the material total effect (on-chain sends + Depl | F1 + trade gate | MERGE into chain C-SEND-BOUNDS -> skill onchain-send + skill deploy-verify ; CHECK-candidate | TITLE |
| A-178 | e36a34e7 | 668 | DEPLOY | v3.5.16 | Late-provisioned self-created legs are unaccounted until inventoried | F1, F2 | MERGE into chain C-DEP-CONTINUING -> skill deploy-verify ; CHECK-candidate | TITLE |
| A-179 | 53cd4815 | 657 | PUBLISH | v3.5.16 | Rotating-sample re-observation | F1, F2 + publish gate | MERGE into chain C-PUB-CLOSURE -> skill pre-publish ; CHECK-candidate | TITLE |
| A-180 | 5c09c2a5 | 611 | SEND | v3.5.17 | The broadcaster/worker set is itself an inventory | F1 + trade gate | MERGE into chain C-SEND-CLAIM -> skill onchain-send ; CHECK-candidate | TITLE |
| A-181 | 6c536c14 | 659 | SEND | v3.5.17 | Unknown-outcome durable-nonce claims escalate; they never silently lock forever | F1 + trade gate | MERGE into chain C-SEND-RELEASE -> skill onchain-send ; CHECK-candidate | TITLE |
| A-182 | 1bf84660 | 521 | SEND+DEPLOY | v3.5.17 | Total-effect bounds require a single numeraire (on-chain sends + Deplo | F1 + trade gate | MERGE into chain C-SEND-BOUNDS -> skill onchain-send + skill deploy-verify ; CHECK-candidate | TITLE |
| A-183 | 58eb9328 | 549 | PUBLISH | v3.5.17 | Publication bars take precedence over the thumbnail exception | F1, F2 + publish gate | MERGE into chain C-MEDIA-TRANSFORM -> skill pre-publish | TITLE |
| A-184 | 05b247de | 496 | DEPLOY | v3.5.17 | Verified-live requires an audience-identical fetch in Deployments too  | F1, F2 | MERGE into chain C-PUB-CLOSURE -> skill deploy-verify | TITLE |
| A-185 | 2cebe30a | 557 | PUBLISH | v3.5.17 | A waiver binds to bytes, verified at apply time (Pre-publish gate; qua | F1, F2 + publish gate | MERGE into chain C-PUB-WAIVER -> skill pre-publish ; CHECK-candidate | TITLE |
| A-186 | f083ae1e | 533 | MEDIA | v3.5.17 | Transform duty is closed under composition | F1 + publish gate | MERGE into chain C-MEDIA-TRANSFORM -> skill media-verify | TITLE |
| A-187 | 432e4528 | 550 | PUBLISH | v3.5.17 | Publish-time generation requires a publish-time gate (Pre-publish gate | F1, F2 + publish gate | MERGE into chain C-PUB-ENVELOPE -> skill pre-publish | TITLE |
| A-188 | ab3e63c6 | 607 | PUBLISH | v3.5.17 | Re-observation fingerprints the render, not the source's self-report ( | F1, F2 + publish gate | MERGE into chain C-PUB-CLOSURE -> skill pre-publish ; CHECK-candidate | TITLE |
| A-189 | cc1a2457 | 1014 | SEND+DEPLOY | v3.5.18 | Numeraire conversions meet an integrity standard (on-chain sends + Dep | F1 + trade gate | MERGE into chain C-SEND-BOUNDS -> skill onchain-send + skill deploy-verify ; CHECK-candidate | TITLE |
| A-190 | a6856959 | 765 | SEND | v3.5.18 | Abandonment preserves mutual exclusivity | F1 + trade gate | MERGE into chain C-SEND-RELEASE -> skill onchain-send | TITLE |
| A-191 | bca3e24e | 680 | DEPLOY | v3.5.18 | Verified-live covers the audience's actual spread | F1, F2 | MERGE into chain C-DEP-VANTAGE -> skill deploy-verify | TITLE |
| A-192 | 4d998f53 | 709 | PUBLISH | v3.5.18 | Publication bars take precedence over the publish-time-gate permission | F1, F2 + publish gate | MERGE into chain C-PUB-ENVELOPE -> skill pre-publish | TITLE |
| A-193 | 0c914828 | 546 | MEDIA+PUBLISH+DEPLOY | v3.5.18 | A load-bearing hash is a full collision-resistant digest (Deployments  | F1 + publish gate | MERGE into chain C-DEP-DIGEST -> skill media-verify + skill pre-publish + skill deploy-verify ; CHECK-candidate | TITLE |
| A-194 | ca506430 | 1012 | MEDIA | v3.5.18 | Transform output the inspector cannot read is a failed leg, and the re | F1 + publish gate | MERGE into chain C-MEDIA-TRANSFORM -> skill media-verify | TITLE |
| A-195 | acccaefc | 649 | PUBLISH | v3.5.18 | Re-observation fingerprints include an audience vantage (Pre-publish g | F1, F2 + publish gate | MERGE into chain C-PUB-CLOSURE -> skill pre-publish ; CHECK-candidate | TITLE |
| A-196 | cea60ed5 | 793 | PUBLISH | v3.5.19 | A waiver binds to the bytes as shipped, and recompression creates new  | F1, F2 + publish gate | MERGE into chain C-PUB-WAIVER -> skill pre-publish ; CHECK-candidate | TITLE |
| A-197 | 96f5ed6a | 647 | SEND+DEPLOY | v3.5.19 | A TWAP or depth test has minimum parameters (on-chain sends + Deployme | F1 + trade gate | MERGE into chain C-SEND-BOUNDS -> skill onchain-send + skill deploy-verify | TITLE |
| A-198 | e133e514 | 649 | MEDIA | v3.5.19 | Continuous controls are swept, not scoped out | F1 + publish gate | MERGE into chain C-MEDIA-TRANSFORM -> skill media-verify | TITLE |
| A-199 | 07f74cbe | 523 | SEND | v3.5.19 | An abandonment replacement must preserve the staged intent | F1 + trade gate | MERGE into chain C-SEND-RELEASE -> skill onchain-send | TITLE |
| A-200 | 7dd7eff7 | 655 | PUBLISH | v3.5.19 | Interaction-triggered variants are generated variants (Pre-publish gat | F1, F2 + publish gate | MERGE into chain C-PUB-ENVELOPE -> skill pre-publish ; CHECK-candidate | TITLE |
| A-201 | 819e8b42 | 541 | SEND | v3.5.19 | The on-chain claim record is tamper-evident | F1 + trade gate | MERGE into chain C-SEND-CLAIM -> skill onchain-send ; CHECK-candidate | TITLE |
| A-202 | 3d060c30 | 544 | PUBLISH+DEPLOY | v3.5.19 | Low-entropy values are fingerprinted with a keyed digest (Deployments  | F1, F2 + publish gate | MERGE into chain C-DEP-DIGEST -> skill pre-publish + skill deploy-verify ; CHECK-candidate | TITLE |
| A-203 | 0a891614 | 438 | MEDIA | v3.5.19 | The transform duty applies to video frames | F1 + publish gate | MERGE into chain C-MEDIA-AV -> skill media-verify | TITLE |
| A-204 | ae8cf301 | 541 | MEDIA+PUBLISH | v3.5.19 | The publication envelope is part of the plain-meaning assembly set | F1 + publish gate | MERGE into chain C-PUB-ENVELOPE -> skill media-verify + skill pre-publish | TITLE |
| A-205 | e3f83195 | 744 | PUBLISH+DEPLOY | v3.5.20 | Keyed-digest precedence and custody (Deployments + Pre-publish gate; g | F1, F2 + publish gate | MERGE into chain C-DEP-DIGEST -> skill pre-publish + skill deploy-verify ; CHECK-candidate | TITLE |
| A-206 | 201fa30c | 601 | SEND+DEPLOY | v3.5.20 | One governing conversion standard (on-chain sends + Deployments; qualifies the v3.5. | F1 + trade gate | MERGE into chain C-SEND-BOUNDS -> skill onchain-send + skill deploy-verify | TITLE |
| A-207 | 9e1dcd71 | 667 | MEDIA | v3.5.20 | Video-frame closure is satisfiable (Verify media; qualifies the v3.5.1 | F1 + publish gate | MERGE into chain C-PUB-CLOSURE -> skill media-verify ; CHECK-candidate | TITLE |
| A-208 | ce0b012d | 609 | PUBLISH | v3.5.20 | Interaction-variant enumeration must not prime distribution (Pre-publi | F1, F2 + publish gate | MERGE into chain C-PUB-ENVELOPE -> skill pre-publish ; CHECK-candidate | TITLE |
| A-209 | c86a63f7 | 724 | SEND | v3.5.20 | Claim-lock release path | F1 + trade gate | MERGE into chain C-SEND-RELEASE -> skill onchain-send ; CHECK-candidate | TITLE |
| A-210 | 4ee264ee | 710 | PUBLISH | v3.5.20 | A waiver binds to the shipped variant set | F1, F2 + publish gate | MERGE into chain C-PUB-WAIVER -> skill pre-publish ; CHECK-candidate | TITLE |
| A-211 | 59ea5c5b | 507 | SEND | v3.5.20 | Class-identity reference price integrity | F1 + trade gate | MERGE into chain C-SEND-CLASS -> skill onchain-send ; CHECK-candidate | TITLE |
| A-212 | 47f94be9 | 572 | DEPLOY | v3.5.20 | Merge-values snapshots are sensitive artifacts | F1, F2 | MERGE into chain C-PUB-PERSONAL -> skill deploy-verify ; CHECK-candidate | TITLE |
| A-213 | 61bcf0dd | 612 | MEDIA+DEPLOY | v3.5.20 | Audience-vantage inventory and fallback (Deployments + Verify media; qualifies the v | F1 + publish gate | MERGE into chain C-DEP-CONTINUING -> skill media-verify + skill deploy-verify | TITLE |
| A-214 | 40a90f91 | 454 | MEDIA | v3.5.21 | Video sampling floor | F1 + publish gate | MERGE into chain C-PUB-CLOSURE -> skill media-verify | TITLE |
| A-215 | 30989ed4 | 610 | PUBLISH | v3.5.21 | Waiver derivation must be verified | F1, F2 + publish gate | MERGE into chain C-PUB-WAIVER -> skill pre-publish ; CHECK-candidate | TITLE |
| A-216 | 9d996254 | 408 | SEND | v3.5.21 | Class identity under an UNVERIFIED price | F1 + trade gate | MERGE into chain C-SEND-CLASS -> skill onchain-send ; CHECK-candidate | TITLE |
| A-217 | 4f58b149 | 467 | SEND | v3.5.21 | Claim-release authentication | F1 + trade gate | MERGE into chain C-SEND-RELEASE -> skill onchain-send ; CHECK-candidate | TITLE |
| A-218 | bd1f048d | 435 | PUBLISH | v3.5.21 | Interaction-variant leg closes post-publish | F1, F2 + publish gate | MERGE into chain C-PUB-ENVELOPE -> skill pre-publish ; CHECK-candidate | TITLE |
| A-219 | 2a70e365 | 493 | DEPLOY | v3.5.21 | Vantage deferral cap and authorisation provenance | F1, F2 | MERGE into chain C-PUB-CLOSURE -> skill deploy-verify ; CHECK-candidate | TITLE |
| A-220 | c9219a78 | 445 | PUBLISH | v3.5.21 | Snapshot deletion and key separation | F1, F2 + publish gate | MERGE into chain C-SEND-RELEASE -> skill pre-publish ; CHECK-candidate | TITLE |

## 3. Persona file — 19 sections

| Id | Section | B | Class | Verdict |
|---|---|---|---|---|
| P-01 | Title line | 24 | - | KEEP-AS-IS |
| P-02 | §1 who I am | 489 | - | KERNEL (trim to ~250 B) |
| P-03 | §2 laws | 492 | gates | KERNEL verbatim (owner-locked section) |
| P-04 | §3 the bar: done means accepted | 565 | F1 | KERNEL (two lines); rest to skill quality-bars |
| P-05 | §4 contract: goal / done-when / plan / gates | 551 | F1, F2 | KERNEL |
| P-06 | §5 results, not loops | 1120 | F1, F6 | KERNEL (five one-liners); the rest is restatement |
| P-07 | §6 power moves: split, route, two-model check, long jobs, measure | 1031 | cost, F7 | MERGE (survivor: skill model-routing for routing lines; CHECKPOINT-REQUIRED for long jobs) |
| P-08 | §7 thinking: labels VERIFIED / INFERENCE / ASSUMPTION / NOT_EXECUTED | 871 | F1 | KERNEL (label line only) — label set conflicts, see P-C2 |
| P-09 | §8 lessons file, weekly self-audit, locked sections | 585 | F6, F3 | CHECK (lessons pipeline) + KERNEL (the lock on §2, §11, §12, §13) |
| P-10 | §9 voice and live calls | 852 | F6 | KERNEL (three lines) + MODULE (skill comms-live) |
| P-11 | §10 friend and partner | 571 | - | MODULE (skill comms-live); one line stays in kernel |
| P-12 | §11 approval gates, two standing permissions, batching rule | 1692 | gates | KERNEL verbatim (owner-locked section) |
| P-13 | §12 money | 526 | spend gate | KERNEL verbatim (owner-locked section) |
| P-14 | §13 secrets and safety | 809 | secrets, injection | KERNEL verbatim (owner-locked section) |
| P-15 | §14 crew and coordination board | 1299 | F2, F7 | KERNEL (three lines) + MODULE (skill crew) |
| P-16 | §15 models: bench, routing order, privacy limits | 1005 | cost | MERGE (survivor: skill model-routing); privacy line stays in kernel |
| P-17 | §16 ops check before promising | 664 | F1 | KERNEL (four-item list) |
| P-18 | §17 decisions, scope, scheduling | 570 | - | KERNEL (two lines) |
| P-19 | §18 skills index | 773 | F3 | CHECK (generate the index from the skills folder; three names here match no manifest skill, see P-G4) |

Kernel cost of this file if the verdicts hold: 3,519 B locked + about 2,600 B of trimmed lines = about 6.1 KB.

## 4. Live memory file — 9 sections (headings and sizes only)

| Id | Section | B | Verdict |
|---|---|---|---|
| M-1 | header | 251 | DELETE (generated header) |
| M-2 | owner profile | 2481 | KEEP in LIVE, generated from the ledger |
| M-3 | standing orders | 5489 | MODULE/KERNEL: these are rules, not facts; move to the rules layer with owner-quote provenance, see P-C5 |
| M-4 | money, wallets, trading | 5931 | split: rules to skill onchain-send and persona §12; state to the ledger, see P-C5 |
| M-5 | accounts | 1982 | ledger facts; BLOCKED-ON-READ for which lines are rules |
| M-6 | coordination | 585 | ledger fact |
| M-7 | launch doctrine | 186 | rule: move to the rules layer |
| M-8 | current state | 3586 | KEEP in LIVE, generated, TTL 30 days |
| M-9 | setup | 1404 | MODULE (skill platform-quirks) |

## 5. Alignment synthesis — 7 sections (headings and sizes only)

| Id | Section | B | Verdict |
|---|---|---|---|
| Y-1 | title | 190 | DELETE |
| Y-2 | who the user is and how to act: one section, one line, 26,880 B | 26880 | BLOCKED: is this file platform-generated and platform-injected? See P-G1 |
| Y-3 | user value | 404 | as Y-2 |
| Y-4 | boundaries | 2276 | MERGE (survivor: persona §11 / M-3) if Muse controls the file |
| Y-5 | current frictions | 1920 | CHECK: feed to the lessons pipeline as incidents |
| Y-6 | strengthening the relationship | 2164 | as Y-2 |
| Y-7 | pointer | 116 | DELETE |

## 6. Tools file — 5 sections

| Id | Section | B | Verdict |
|---|---|---|---|
| T-1 | header | 313 | DELETE |
| T-2 | CAPTCHA technique A | 764 | MODULE (skill platform-quirks) |
| T-3 | CAPTCHA technique B | 1121 | MODULE (skill platform-quirks) |
| T-4 | phone hardware control note | 500 | MODULE (skill platform-quirks) |
| T-5 | phone foreground control route | 676 | MODULE (skill platform-quirks) |

## 7. Identity and user files — 4 sections

| Id | Section | B | Verdict |
|---|---|---|---|
| I-1 | identity card | 1335 | KERNEL (trim to ~300 B) |
| I-2 | avatar description | 553 | MODULE (load only when generating an avatar) |
| U-1 | owner card | 632 | KERNEL (~300 B) |
| U-2 | context | 738 | ledger facts, shown in LIVE |

## 8. Lessons file — 7 lessons

| Id | Lesson (paraphrased) | Class | Verdict |
|---|---|---|---|
| L-1 | no filler or repeated status on calls | F6 | KERNEL line + eval K4; duplicates persona §9 |
| L-2 | green CI is not done | F1 | MERGE (survivor: A-016); eval E-series |
| L-3 | start the relay worker first | F7 | CHECK (STARTUP-ALIVE); the only carrier today is this file |
| L-4 | ambient speech is not an order | injection | MERGE (survivor: persona §9 line); DATA-NOT-ORDERS |
| L-5 | read list items from the list, never improvise | F1 | CHECK-audited (SOURCE-OR-SILENT); new eval task, see D15 |
| L-6 | stay silent while he narrates a screen | F6 | KERNEL line; eval K1, K5 |
| L-7 | verdict before agreement | F6 | KERNEL line; eval K2, K3 |

## 9. Skills — 94

Custom skill bytes total 962,980; the 17 market-data playbooks are 673,591 of that.

| Id | Skill | Kind | Size | Does | Class | Verdict | Evidence |
|---|---|---|---|---|---|---|---|
| S-001 | advertising-campaigns | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-002 | app-creation | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-003 | avatar-dance-videos | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-004 | business-finance | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-005 | custom-connector-setup | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-006 | customer-outreach | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-007 | device-data | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-008 | documents | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-009 | email-management | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-010 | event-tickets | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-011 | file-hosting | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-012 | financial-planning | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-013 | fitness-tracking | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-014 | flight-booking | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-015 | flight-tracking | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-016 | forget | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-017 | form-design | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-018 | generate_podcast | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-019 | goals | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-020 | groceries | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-021 | health-review | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-022 | home-control | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-023 | home-search | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-024 | hotel-booking | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-025 | image-search | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-026 | knowledge-organization | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-027 | live-page-checks | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-028 | marketplaces | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-029 | media-library | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-030 | meeting-follow-up | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-031 | messaging | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-032 | mortgage-comparison | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-033 | muse-early-access | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-034 | muse-feedback | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-035 | muse_db | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-036 | music-discovery | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-037 | place-discovery | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-038 | restaurant-reservations | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-039 | scheduling | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-040 | self-awareness | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-041 | share-ideas | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-042 | shopping | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-043 | smb-product-shots | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-044 | social-content-performance | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-045 | social-publishing | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-046 | spoken-audio | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-047 | store-operations | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-048 | style-tryon | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-049 | subscription-status | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-050 | task-management | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-051 | transcribe-recordings | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-052 | translation | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-053 | trip-planning | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-054 | trip-transport | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-055 | wearables-comms | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-056 | wide-research | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-057 | workout-planning | system | names only | platform playbook | - | KEEP-AS-IS (ASSUMPTION: platform-owned, loaded on demand) | BLOCKED-ON-CORPUS: body not supplied |
| S-058 | approved_asset_freeze | custom | 3 files, 43275 B | freeze an approved asset or copy at approval time | publish gate | MERGE (survivor: skill pre-publish; overlaps chain C-PATH-ONLY, see P-U5). 43 KB: condense | DESCRIPTION-LINE |
| S-059 | authority_provenance_gate | custom | 3 files, 6377 B | classify a claim to authority before acting on it | gates | KEEP-AS-IS; becomes the single home for owner-provenance atoms (chain C-PUB-WAIVER), see P-U6 | DESCRIPTION-LINE |
| S-060 | batched_application_preflight | custom | 3 files, 4921 B | preflight a whole batch before opening the first form | F2 | KEEP-AS-IS | DESCRIPTION-LINE |
| S-061 | device_screen_state_verification | custom | 3 files, 38930 B | verify what is on a device screen, leg by leg | F1, F2 | KEEP-AS-IS as a skill; 39 KB: condense; overlaps A-017, see P-U7 | DESCRIPTION-LINE |
| S-062 | local-cherry-publisher | custom | 16 files, 75805 B | publish a web project as a messenger mini-app | deploy gate | KEEP-AS-IS | DESCRIPTION-LINE |
| S-063 | local-gmgn-contract-dd | custom | 2 files, 110165 B | market-data CLI playbook (one of 17 sharing one preamble) | - | MERGE shared preamble into one common file (survivor: a new gmgn-common reference), see P-U8 | DESCRIPTION-LINE |
| S-064 | local-gmgn-cooking | custom | 2 files, 42595 B | market-data CLI playbook (one of 17 sharing one preamble) | - | MERGE shared preamble into one common file (survivor: a new gmgn-common reference), see P-U8 | DESCRIPTION-LINE |
| S-065 | local-gmgn-dev-score | custom | 2 files, 11914 B | market-data CLI playbook (one of 17 sharing one preamble) | - | MERGE shared preamble into one common file (survivor: a new gmgn-common reference), see P-U8 | DESCRIPTION-LINE |
| S-066 | local-gmgn-heat-rank | custom | 2 files, 68163 B | market-data CLI playbook (one of 17 sharing one preamble) | - | MERGE shared preamble into one common file (survivor: a new gmgn-common reference), see P-U8 | DESCRIPTION-LINE |
| S-067 | local-gmgn-holder-analysis | custom | 2 files, 17480 B | market-data CLI playbook (one of 17 sharing one preamble) | - | MERGE shared preamble into one common file (survivor: a new gmgn-common reference), see P-U8 | DESCRIPTION-LINE |
| S-068 | local-gmgn-kline-pattern | custom | 2 files, 15196 B | market-data CLI playbook (one of 17 sharing one preamble) | - | MERGE shared preamble into one common file (survivor: a new gmgn-common reference), see P-U8 | DESCRIPTION-LINE |
| S-069 | local-gmgn-market | custom | 2 files, 77266 B | market-data CLI playbook (one of 17 sharing one preamble) | - | MERGE shared preamble into one common file (survivor: a new gmgn-common reference), see P-U8 | DESCRIPTION-LINE |
| S-070 | local-gmgn-narrative | custom | 2 files, 23463 B | market-data CLI playbook (one of 17 sharing one preamble) | - | MERGE shared preamble into one common file (survivor: a new gmgn-common reference), see P-U8 | DESCRIPTION-LINE |
| S-071 | local-gmgn-portfolio | custom | 2 files, 23545 B | market-data CLI playbook (one of 17 sharing one preamble) | - | MERGE shared preamble into one common file (survivor: a new gmgn-common reference), see P-U8 | DESCRIPTION-LINE |
| S-072 | local-gmgn-swap | custom | 2 files, 54156 B | market-data CLI playbook (one of 17 sharing one preamble) | - | MERGE shared preamble into one common file (survivor: a new gmgn-common reference), see P-U8 | DESCRIPTION-LINE |
| S-073 | local-gmgn-token | custom | 2 files, 41421 B | market-data CLI playbook (one of 17 sharing one preamble) | - | MERGE shared preamble into one common file (survivor: a new gmgn-common reference), see P-U8 | DESCRIPTION-LINE |
| S-074 | local-gmgn-token-buy | custom | 2 files, 27523 B | market-data CLI playbook (one of 17 sharing one preamble) | - | MERGE shared preamble into one common file (survivor: a new gmgn-common reference), see P-U8 | DESCRIPTION-LINE |
| S-075 | local-gmgn-track | custom | 2 files, 22155 B | market-data CLI playbook (one of 17 sharing one preamble) | - | MERGE shared preamble into one common file (survivor: a new gmgn-common reference), see P-U8 | DESCRIPTION-LINE |
| S-076 | local-gmgn-wallet-analysis | custom | 2 files, 31987 B | market-data CLI playbook (one of 17 sharing one preamble) | - | MERGE shared preamble into one common file (survivor: a new gmgn-common reference), see P-U8 | DESCRIPTION-LINE |
| S-077 | local-gmgn-wallet-review | custom | 2 files, 36066 B | market-data CLI playbook (one of 17 sharing one preamble) | - | MERGE shared preamble into one common file (survivor: a new gmgn-common reference), see P-U8 | DESCRIPTION-LINE |
| S-078 | local-gmgn-wallet-score | custom | 2 files, 40317 B | market-data CLI playbook (one of 17 sharing one preamble) | - | MERGE shared preamble into one common file (survivor: a new gmgn-common reference), see P-U8 | DESCRIPTION-LINE |
| S-079 | local-gmgn-wallet-style | custom | 2 files, 30179 B | market-data CLI playbook (one of 17 sharing one preamble) | - | MERGE shared preamble into one common file (survivor: a new gmgn-common reference), see P-U8 | DESCRIPTION-LINE |
| S-080 | local-phantom-pre-ops | custom | 3 files, 1817 B | pre-flight before any build instruction for one project | F1 | KEEP-AS-IS | DESCRIPTION-LINE |
| S-081 | local-typesafe-ai | custom | 3 files, 11370 B | build with a typed-judgment library | - | KEEP-AS-IS | DESCRIPTION-LINE |
| S-082 | model-routing | custom | 1 files, 2410 B | how to pick models, two-model check, escalation, privacy limits | cost | MERGE (survivor: this skill; persona §6 and §15 and spec 04 fold into it, see P-U1) | DESCRIPTION-LINE |
| S-083 | multi_wallet_onchain_execution | custom | 3 files, 6580 B | wallet-by-wallet on-chain execution | F1 + trade gate | MERGE (survivor: skill onchain-send, which also takes the 42 on-chain atoms from the rules file, see P-U4) | DESCRIPTION-LINE |
| S-084 | packet_claim_provenance | custom | 3 files, 4737 B | every claim in a submission packet traces to a source | F1 | KEEP-AS-IS | DESCRIPTION-LINE |
| S-085 | paid_api_credit_guard | custom | 3 files, 44709 B | price paid work before it runs | spend gate | KEEP-AS-IS as a skill; 45 KB: condense; pairs with BUDGET-STOP, see P-D7 | DESCRIPTION-LINE |
| S-086 | platform_capability_ground_truth | custom | 3 files, 7561 B | verify a platform capability from ground truth | F1 | MERGE (survivor: this skill; takes A-036 and persona §16 item 4) | DESCRIPTION-LINE |
| S-087 | quality-bars | custom | 1 files, 2748 B | done-when standards per kind of work | F1 | KEEP-AS-IS | DESCRIPTION-LINE |
| S-088 | real-or-bs | custom | 2 files, 3741 B | legit / unproven / scam audit | F1 | KEEP-AS-IS | DESCRIPTION-LINE |
| S-089 | recovered-skill-notes | custom | 11 files, 12616 B | preserved earlier notes; self-described as possibly out of date | F4 | DELETE (safe once each of its 10 note files is either promoted to a skill or archived; BLOCKED-ON-READ for which) | DESCRIPTION-LINE |
| S-090 | scout_packet_shape_verification | custom | 3 files, 4877 B | classify an opportunity from its primary source | F1 | KEEP-AS-IS | DESCRIPTION-LINE |
| S-091 | seeker_bridge_recovery | custom | 3 files, 6054 B | diagnose the phone bridge by symptom layer | F5, F7 | KEEP-AS-IS; its layer list feeds the transport-family table of A-035 | DESCRIPTION-LINE |
| S-092 | social | custom | 1 files, 1645 B | rules for the owner's social accounts | publish gate | KEEP-AS-IS | DESCRIPTION-LINE |
| S-093 | submissions | custom | 1 files, 3652 B | fill, review, submit exactly the approved packet | gates | KEEP-AS-IS; its delegated approval needs a record type in APPROVAL-TOKEN, see D9 | DESCRIPTION-LINE |
| S-094 | timed_web_session_work | custom | 3 files, 5564 B | size each stage to the signed-in session | F7 | KEEP-AS-IS | DESCRIPTION-LINE |

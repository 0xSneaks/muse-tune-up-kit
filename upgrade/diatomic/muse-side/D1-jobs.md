# D1 — Scheduled jobs (from cron.list + health snapshot, 2026-11-12)

Snapshot captured_at: 2026-11-12T06:00:10Z · user jobs listed: 31

| Job | Enabled | Interval (s) | Last run | Last status |
|---|---|---|---|---|
| ai-coms-inbox-check | True | 14400 | 2026-11-12T01:59:55Z | succeeded |
| beam-release-watch | True | 172800 | 2026-11-12T03:38:58Z | succeeded |
| bounty-scout-cycle | True | 14400 | 2026-11-12T03:47:29Z | succeeded |
| ca-watch-hourly | False | 3600 | — | — |
| cardless-hardship-reply-watch | True | 21600 | 2026-11-12T05:09:05Z | succeeded |
| claude-eyes-usage-watch | True | 7200 | 2026-11-12T05:44:11Z | succeeded |
| coms-orders-poll | True | 600 | 2026-11-12T05:54:32Z | succeeded |
| desk-bridge-watch | True | 300 | 2026-11-12T05:57:45Z | succeeded |
| direct-deposit-call-reminder-2026-11-09 | False | None | — | — |
| fomo-monitor-daily-check | False | 86400 | — | — |
| github-profile-now-building-weekly | True | 604800 | — | — |
| gmgn-scout-watch | False | 600 | — | — |
| halfmoon-inbox-watch | True | 21600 | 2026-11-12T05:56:33Z | running |
| justmogit-turn3-turn4-retry | False | 3600 | — | — |
| kalshi-paper-agent-hourly | True | 3600 | 2026-11-12T05:30:27Z | failed |
| monster-jam-ubs-reminder-week-before | True | None | — | — |
| muse-browser-ensure | True | 900 | 2026-11-12T05:52:55Z | succeeded |
| muse-health-watch | True | 900 | 2026-11-12T05:58:31Z | running |
| muse-self-audit-12h | True | 43200 | 2026-11-12T01:47:09Z | succeeded |
| muse-tech-watch | True | 604800 | 2026-11-09T15:23:50Z | succeeded |
| narrative-ops-watch | True | 900 | 2026-11-12T05:57:29Z | succeeded |
| ollama-flash-unlock-watch | False | 1800 | — | — |
| opencode-bench-watch | True | 900 | 2026-11-12T05:38:00Z | failed |
| ov-299k-watch | True | 1800 | 2026-11-12T05:41:22Z | succeeded |
| release-radar-muse-maestro | True | 86400 | 2026-11-11T14:23:28Z | succeeded |
| sol-parked-guard | True | 900 | 2026-11-12T05:47:21Z | succeeded |
| subscription-signups-reminder-2026-11-09 | False | None | — | — |
| superteam-instagrant-watch | True | 21600 | 2026-11-12T02:39:09Z | succeeded |
| voice-page-watch | True | 120 | 2026-11-12T05:59:18Z | succeeded |
| water-grass-trees-evening | True | 86400 | 2026-11-11T23:23:12Z | succeeded |
| water-grass-trees-morning | True | 86400 | 2026-11-11T13:23:17Z | succeeded |

Purposes and stop conditions live in each job body (cron.view per job); the two muted jobs
(gmgn-scout-watch, fomo-monitor-daily-check) stay disabled until Sneaks says put them back on.

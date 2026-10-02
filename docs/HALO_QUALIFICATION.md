# Qualifying the cleaned Halo candidate

The offline preparation is separate from GPU release qualification. Historical experimental results do not qualify this executable. Keep `DS4_ROCM_HALO_PREFILL` opt-in until the gates below pass on an exclusive Halo executor. Publication is a separate action.

## Executed and pending checks

| Check | Status | Scope or reason |
|---|---|---|
| Linux CPU build | PASS | Normal `make cpu -j2`; GCC15.2 in WSL Ubuntu; no model inference |
| Production admission | PASS | `make test-halo-shapes`; actual shared production predicates, 2K/4K, layer/context/position boundaries and rejected shapes |
| Linux nonmovable allocator | PASS | Existing `make test-linux-memory` |
| SSD cache sizing | PASS | Existing `make test-ssd-cache`; this does not test SSD model inference |
| Session serialization unit suite | PASS | Existing `tests/test_session_state`; no GPU model proof |
| Session/TP unit suite | PASS after test portability fixes | `make test-session-state`: serialization, command, RDMA accounting and Unix/TCP exchanges. Timeout checks compare exact effective socket options; the 1KB TCP test negotiates small segments. Production network code and deadlines are unchanged |
| ROCm C frontend | PASS | Real `ds4.c` with `DS4_ROCM_BUILD` |
| Complete ROCm host/device syntax | PASS | Actual `ds4_rocm.cu`, gfx1151 and gfx1100 |
| Complete ROCm HIP object | PASS | Actual host/device object generation, gfx1151 and gfx1100; no final SDK library link |
| Ported kernel families | PASS | Production specializations compiled for both architectures; gfx1100 definitions are unreachable registrations |
| Normal Makefile object recipes | PASS | All10 Halo objects, full runtime and native quantizer for gfx1151/gfx1100; real gfx1100 template entries verified |
| S4+D2 source reconstruction | PASS | Newly assembled/linked module has original SHA256; no undefined symbols |
| Complete SDK executable link | PENDING | Offline cache lacks the complete link libraries |
| New GPU logits/state/decode/snapshot equality | PENDING | No GPU access in this preparation |
| Cache demotion, aliases, resource failures and peak memory | PENDING | New host composition needs hardware checks; fault/alias injection is not automated by the benchmark |
| Ordinary complete prefill/decode timing | PENDING | Run after numerical admission, without payloads or profiler |
| Metal/CUDA model and SSD inference regressions | SKIP here | Required platform/model executors unavailable; shared changes are guarded by `DS4_ROCM_BUILD` |
| Full upstream/model suites | PENDING | No claim that `make test` or `make test-rocm` completed |

[Offline records](halo/offline-checks.json) bind actual logs and source identities. [Dependencies](halo/dependencies.json) record the cached compiler, rocWMMA2.2.1 headers and official reference-header commits. The full-runtime checks use configured official headers, not a complete SDK install. A different installed toolchain still needs requalification. Companion parser/clone/build checks are reported in its own verification record.

The original command assertion54 and subsequent TCP tiny-buffer failure were reproduced on a freshly built historical core. WSL rounded requested 50ms to 52ms; Linux stores socket timeouts in timer ticks ([kernel source](https://github.com/torvalds/linux/blob/v6.18/net/core/sock.c#L401)). The corrected command test requires exact restoration of both effective receive/send timeouts, with no tolerance increase. The TCP fixture keeps its 1KB buffers, payloads and deadlines, negotiating 536-byte MSS before connection ([TCP option documentation](https://man7.org/linux/man-pages/man7/tcp.7.html)). Deliberate missing-restoration and serial-send controls still fail. These unit results do not qualify distributed model inference or GPU behavior. Original failures remain in the offline evidence record.

## Build the three controls

Use explicit existing paths. The companion is local and has no publication URL. Do not run more than one model process at a time. Set these shell variables to real paths; all destinations must be new.

```sh
HALO_RELEASE=/path/to/local/release/ds4
HALO_COMPANION=/path/to/local/ds4-on-halo
HALO_ENGINE=/path/to/new/pinned-engine
HALO_CONTROL=/path/to/new/historical-core
HALO_HIPCC=/path/to/existing/hipcc
HALO_CASES=/path/to/new/cases
HALO_RESULTS=/path/to/new/results
python3 "$HALO_COMPANION/scripts/halo.py" bootstrap --source "$HALO_RELEASE" --destination "$HALO_ENGINE"
python3 "$HALO_COMPANION/scripts/halo.py" baseline --source "$HALO_RELEASE" --destination "$HALO_CONTROL"
python3 "$HALO_COMPANION/scripts/halo.py" build --engine "$HALO_ENGINE" --backend rocm --hipcc "$HALO_HIPCC" --jobs 2
python3 "$HALO_COMPANION/scripts/halo.py" build --engine "$HALO_CONTROL" --baseline --backend rocm --hipcc "$HALO_HIPCC" --jobs 2
```

`base` is the exact historical8db core plus only the manifest-bound benchmark instrumentation. `native` is the cleaned engine with added selectors disabled. `halo` enables them. The companion checks actual source/executable hashes. Record the installed SDK/header versions, actual loaded shared libraries and hashes, OS/driver, board/RAM, existing GPU policy, IOMMU state and absence of competing work. It changes no driver/firmware/power settings. Its explicit `--power 100` disables only upstream engine duty-cycle sleeps.

Copy the companion example to `/path/to/local.toml`, supply the existing model and prompt, and record actual conditions. The historical model is86,720,111,488B, SHA256 `ca22ae2f838e14077c22bc1c1417b71b45b5e5a3687bd96c2ac6e17fdb6261c0`. Use a prompt you can retain privately or redistribute legitimately; prompt hashes bind comparisons. Do not download weights through this workflow.

```sh
python3 "$HALO_COMPANION/scripts/prepare_cases.py" --template /path/to/local.toml --destination "$HALO_CASES"
```

This creates fresh32/64/128K with actual2K and4K chunk requests and capacities32897/65665/131201, short2K/4K controls, and incremental64K with2K/4K steps. It binds native cache warmup geometry and permits full serialized snapshots. These are prepared configurations, not executed tests.

## Numerical admission

Start with `short-2048` and `short-4096`, then the six fresh cases, then both incremental cases. Stop at the first source/hash/process/numeric failure; preserve the failed observation. Do not relax tolerances, shorten output or silently change context. For each case:

```sh
HALO_CASE=short-4096
for HALO_ARM in base native halo; do
  HALO_REPO="$HALO_ENGINE"
  if [ "$HALO_ARM" = base ]; then HALO_REPO="$HALO_CONTROL"; fi
  python3 "$HALO_COMPANION/scripts/halo.py" bench --engine "$HALO_REPO" --arm "$HALO_ARM" \
    --config "$HALO_CASES/$HALO_CASE.toml" --output "$HALO_RESULTS/$HALO_CASE-$HALO_ARM" --verify-model --payloads
done
python3 "$HALO_COMPANION/scripts/compare_payloads.py" "$HALO_RESULTS/$HALO_CASE-base" "$HALO_RESULTS/$HALO_CASE-native" --output "$HALO_RESULTS/$HALO_CASE-base-native.json"
python3 "$HALO_COMPANION/scripts/compare_payloads.py" "$HALO_RESULTS/$HALO_CASE-base" "$HALO_RESULTS/$HALO_CASE-halo" --output "$HALO_RESULTS/$HALO_CASE-base-halo.json"
python3 "$HALO_COMPANION/scripts/compare_payloads.py" "$HALO_RESULTS/$HALO_CASE-native" "$HALO_RESULTS/$HALO_CASE-halo" --output "$HALO_RESULTS/$HALO_CASE-native-halo.json"
```

Repeat with case names `fresh-32768-c2048`, `fresh-32768-c4096`, `fresh-65536-c2048`, `fresh-65536-c4096`, `fresh-131072-c2048`, `fresh-131072-c4096`, `incremental-65536-c2048` and `incremental-65536-c4096`. Add `--require-restore` to all three comparisons for incremental cases. Prefix IDs, every FP32 logit and complete serialized state must agree, including after16 emitted greedy IDs. API extent manifests reject equal truncated files. Every intermediate restoration must be an actual serialized snapshot with complete state size; replay is reported separately. Final fresh frontiers do not restore. Results apply to the tested cases, not universal model quality.

After equality, a separate bounded trace must confirm selected kernel names and each qualified2K/4K branch; a passing all-native fallback run cannot prove the optimized paths. Capture producer/output boundaries and compare them to the same native control if a full-state mismatch occurs. Do not use graph-dump mode as coverage evidence because it excludes these selectors. Keep diagnostics out of ordinary timing. Also run native/default and unsupported shape/model checks on available executors; inspect cache native-to-donor admission, donor-to-native one-way demotion during decode, budget exhaustion, repeated engine open/close and lease error paths. The benchmark covers real prefill-to-decode transitions and snapshots, but does not automate allocator fault or alias injection.

The focused upstream regression command on the GPU executor is:

```sh
make -C "$HALO_ENGINE" test-rocm HIPCC="$HALO_HIPCC" ROCM_ARCH=gfx1151 -j2
```

Save its real result, including any TP regression if it recurs. Metal/CUDA/SSD inference checks require their respective executors; keep their status explicit.

## Ordinary timing and resources

After numerical admission, run fresh observations without `--payloads` or `--logits`. For each fresh case use base0/halo0/halo1/base1, one new process/output directory per observation. Compare native separately if attributing host integration overhead. Use identical model/prompt/config/libraries and machine policy. The precision CSV supplements the unchanged official CSV. Report every sample, min/max and mean prefill seconds and tokens/s, initialization, first/steady/complete decode and actual emitted counts. First-use module loading, native temporary allocation and recurring preparation remain inside their actual prefill boundaries. Do not substitute profiling time or incremental suffix throughput for complete fresh prefill.

Historical timings suggest roughly1–2 hours of model execution for the three-arm numerical matrix, before builds, full-model hashes, payload IO and comparisons. Reserve a2–4 hour exclusive window for initial admission; a full ordinary timing matrix and extra failure/coverage probes need additional time. This is a planning estimate, not a new measured result. Use128GB unified RAM; archived process footprints were around99GB, with additional CPU snapshot/readback headroom required. Full state readbacks are about0.48/0.93/1.83GB at32/64/128K per phase. Retaining all three arms and both incremental cases can exceed200GB; reserve at least250GB free output space plus the87GB model and build artifacts. Repeated `--verify-model` reads the whole model outside timers. Check actual peak GPU/GTT/host memory and disk capacity; record failures instead of lowering the prescribed conditions.

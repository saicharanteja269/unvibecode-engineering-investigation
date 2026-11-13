# UnvibeCode Engineering Issue Investigation (Track 1)

This repository contains the reproduction evidence, source code analysis, and issue report for **Track 1 — Engineering Issue Investigation** in UnvibeCode.

## Discovered Defect
**Title:** `[Bug] Business Workflow Map — Dual-protocol exception workflow omits WebSocket handler (ExceptionMiddleware.websocket_exception) despite explicit title and summary promise`

- **Analyzed Repository:** [`encode/starlette`](https://github.com/encode/starlette) at commit [`271c277da0ff64e2048a4d46ecc812b9d61db5f6`](https://github.com/encode/starlette/commit/271c277da0ff64e2048a4d46ecc812b9d61db5f6)
- **UnvibeCode Version:** 0.4.0
- **Component:** Business Workflow Map / Pass 1 Compiler

### Summary
When analyzing Starlette, Workflow 3 is reconstructed with the title:
> **"Handle exceptions raised while serving HTTP and WebSocket requests"**

While the workflow's title, summary, and value section explicitly promise dual-protocol exception handling ending in an HTTP response or WebSocket closure, the **Implementation references** list only `ExceptionMiddleware.http_exception()` (lines 65–69) and completely omit `ExceptionMiddleware.websocket_exception()` (lines 71–73). This conceals Starlette's actual WebSocket terminating closure logic (`await websocket.close(...)`) from developers auditing ASGI exception boundaries.

---

## Contents
- [`ISSUE_REPORT.md`](ISSUE_REPORT.md): The full, structured GitHub issue report adhering to the required Track 1 template.
- [`reproduce.py`](reproduce.py): Automated script to reproduce the issue, verify against the Starlette codebase, and validate the omission.

---

## How to Reproduce
1. Clone Starlette at commit `271c277da0ff64e2048a4d46ecc812b9d61db5f6`:
   ```bash
   git clone https://github.com/encode/starlette.git starlette
   cd starlette && git checkout 271c277da0ff64e2048a4d46ecc812b9d61db5f6 && cd ..
   ```
2. Run the review:
   ```bash
   python -m unvibecode review --repository starlette --output starlette_results --no-open-browser
   ```
3. Inspect `starlette_results/<analysis_folder>/report-support/business-workflows.html` under Workflow Area 2, Workflow 3.

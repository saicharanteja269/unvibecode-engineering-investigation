Title: [Bug] Business Workflow Map — Dual-protocol exception workflow omits WebSocket handler (ExceptionMiddleware.websocket_exception) despite explicit title and summary promise

## 1. Problem summary
The Business Workflow Map for `encode/starlette` reconstructs a workflow titled **"Handle exceptions raised while serving HTTP and WebSocket requests"** (Workflow 3). Its summary explicitly states that an exception raised downstream *"yields an HTTP response or WebSocket close"*, and its value section promises that it *"maps configured exceptions to protocol-appropriate outcomes"*.

However, its **Implementation references** list only `ExceptionMiddleware.http_exception()` (`starlette/middleware/exceptions.py`, lines 65–69) along with general wrapper boilerplate, while completely omitting `ExceptionMiddleware.websocket_exception()` (`starlette/middleware/exceptions.py`, lines 71–73) — the only method in Starlette responsible for handling WebSocket exceptions by issuing the terminating `websocket.close()` call.

For an engineer learning or auditing Starlette's ASGI exception-handling behavior, this creates a false and misleading representation: the workflow explicitly promises to document dual HTTP and WebSocket exception handling, but hides the WebSocket closing pathway entirely, giving the illusion that WebSocket exceptions either have no dedicated handler or are routed through an HTTP response formatter.

## 2. Test environment
- **UnvibeCode version:** 0.4.0
- **Operating system / Python version:** Windows 11 (x86_64) / Python 3.12.14
- **Public repository URL and commit or release:** https://github.com/encode/starlette at commit 271c277da0ff64e2048a4d46ecc812b9d61db5f6
- **Relevant command:** `python -m unvibecode review --repository "starlette" --output "starlette_results" --no-open-browser`

## 3. Steps to reproduce
1. Clone the public Starlette repository at commit `271c277da0ff64e2048a4d46ecc812b9d61db5f6`:
   ```bash
   git clone https://github.com/encode/starlette.git starlette
   cd starlette && git checkout 271c277da0ff64e2048a4d46ecc812b9d61db5f6 && cd ..
   ```
2. Run UnvibeCode review on the repository:
   ```bash
   python -m unvibecode review --repository starlette --output starlette_results --no-open-browser
   ```
3. Open the generated report: `starlette_results/<analysis_folder>/report-support/business-workflows.html` (or view tab *Business Workflows* in `*-unvibecode-full.html`).
4. Navigate to **Workflow area 2 ("Http workflows")** → **Workflow 3: "Handle exceptions raised while serving HTTP and WebSocket requests"**.
5. Expand **Implementation references** and compare the referenced methods against `starlette/middleware/exceptions.py`.

## 4. Expected behavior
Because Workflow 3 explicitly defines its scope in both the title (*"...HTTP and WebSocket requests"*) and summary (*"...yields an HTTP response or WebSocket close"*), the Implementation references should list both default protocol handlers registered in `ExceptionMiddleware.__init__`:
- `ExceptionMiddleware.http_exception()` (`starlette/middleware/exceptions.py`, lines 65–69)
- `ExceptionMiddleware.websocket_exception()` (`starlette/middleware/exceptions.py`, lines 71–73)
- `WebSocketException` (`starlette/exceptions.py`, lines 48–51)

## 5. Actual behavior
The Implementation references list `ExceptionMiddleware.http_exception()` and general application initialization helpers, but completely omit `ExceptionMiddleware.websocket_exception()`.

The rendered Implementation references are:
1. `ExceptionMiddleware.__call__()` (starlette/middleware/exceptions.py · lines 47–63)
2. `wrap_app_handling_exceptions.wrapped_app()` (starlette/_exception_handler.py · lines 31–65)
3. `_lookup_exception_handler()` (starlette/_exception_handler.py · lines 16–20)
4. `ExceptionMiddleware.http_exception()` (starlette/middleware/exceptions.py · lines 65–69)
5. `Starlette.__init__()` (starlette/applications.py · lines 23–61)
6. `ExceptionMiddleware` (starlette/middleware/exceptions.py · lines 18–73)
7. `Starlette.build_middleware_stack()` (starlette/applications.py · lines 63–83)

`websocket_exception()` is completely absent.

## 6. Evidence

### Relevant file/function names and line numbers
- `starlette/middleware/exceptions.py`:
  - Lines 28–31: `self._exception_handlers` registration for both `HTTPException` and `WebSocketException`.
  - Lines 65–69: `http_exception()` (included in report).
  - Lines 71–73: `websocket_exception()` (omitted from report).
- `starlette/_exception_handler.py`:
  - Lines 58–63: invocation of the resolved handler for either connection type (`Request` or `WebSocket`).

### Output excerpt from generated `business-workflows.html`
```html
<article class="workflow-card" data-workflow-id="business_path_955ebc7bf3cfdd95">
  <div class="workflow-number">03</div>
  <div class="workflow-content">
    <div class="eyebrow">Workflow 3</div>
    <h3 class="workflow-title">Handle exceptions raised while serving HTTP and WebSocket requests</h3>
    <section class="workflow-summary">
      <h3>What this workflow does</h3>
      <p>An ASGI HTTP or WebSocket request enters ExceptionMiddleware; an exception raised downstream is matched to a configured handler and, when handled before response start, yields an HTTP response or WebSocket close.</p>
    </section>
    <div class="context-grid">
      <section class="context-panel">
        <h3>Purpose</h3>
        <p>An HTTP or WebSocket client seeks service through an ASGI application; no more specific client goal is established.</p>
      </section>
      <section class="context-panel">
        <h3>What it produces</h3>
        <p>HTTP request or WebSocket connection and its response/close outcome</p>
      </section>
      <section class="context-panel">
        <h3>Who relies on it</h3>
        <p>HTTP client or WebSocket peer</p>
      </section>
    </div>
    <section class="value-section">
      <h3>Why this workflow matters</h3>
      <ul>
        <li>Maps configured exceptions to protocol-appropriate outcomes</li>
        <li>Prevents a handled exception from being converted to a second response after the HTTP response has started</li>
      </ul>
    </section>
    <details class="supporting-code">
      <summary>Implementation references</summary>
      <ul class="evidence-list">
        <li class="implementation-item"><strong>ExceptionMiddleware.__call__()</strong> <span class="implementation-location">starlette/middleware/exceptions.py · lines 47–63</span></li>
        <li class="implementation-item"><strong>wrap_app_handling_exceptions.wrapped_app()</strong> <span class="implementation-location">starlette/_exception_handler.py · lines 31–65</span></li>
        <li class="implementation-item"><strong>_lookup_exception_handler()</strong> <span class="implementation-location">starlette/_exception_handler.py · lines 16–20</span></li>
        <li class="implementation-item"><strong>ExceptionMiddleware.http_exception()</strong> <span class="implementation-location">starlette/middleware/exceptions.py · lines 65–69</span></li>
        <li class="implementation-item"><strong>Starlette.__init__()</strong> <span class="implementation-location">starlette/applications.py · lines 23–61</span></li>
        <li class="implementation-item"><strong>ExceptionMiddleware</strong> <span class="implementation-location">starlette/middleware/exceptions.py · lines 18–73</span></li>
        <li class="implementation-item"><strong>Starlette.build_middleware_stack()</strong> <span class="implementation-location">starlette/applications.py · lines 63–83</span></li>
      </ul>
    </details>
  </div>
</article>
```

### Source-code comparison supporting the finding
In `starlette/middleware/exceptions.py`:
```python
28:         self._exception_handlers: ExceptionHandlers = {
29:             HTTPException: self.http_exception,
30:             WebSocketException: self.websocket_exception,
31:         }
...
65:     async def http_exception(self, request: Request, exc: Exception) -> Response:
66:         assert isinstance(exc, HTTPException)
67:         if exc.status_code in {204, 304}:
68:             return Response(status_code=exc.status_code, headers=exc.headers)
69:         return PlainTextResponse(exc.detail, status_code=exc.status_code, headers=exc.headers)
70: 
71:     async def websocket_exception(self, websocket: WebSocket, exc: Exception) -> None:
72:         assert isinstance(exc, WebSocketException)
73:         await websocket.close(code=exc.code, reason=exc.reason)  # pragma: no cover
```

Notice that `http_exception` and `websocket_exception` are defined adjacently as two halves of the same exception dispatch table.

## 7. Impact and scope
- **Developer Impact:** Any developer auditing an ASGI application for WebSocket reliability, disconnection handling, or exception monitoring uses the Business Workflow Map to locate where exceptions are caught and converted to protocol closing frames. Concealing `websocket_exception` hides the terminal WebSocket execution path (`await websocket.close(...)`), forcing developers to manually search the codebase to verify whether WebSocket exceptions trigger graceful close handshakes.
- **Scope:** Inaccurate context and missing implementation references in the Business Workflow Map. Affects multi-protocol ASGI architectures (Starlette, FastAPI, Quart) where HTTP and WebSocket pipelines share exception middleware.

## 8. Suspected cause / suggested fix (if known)
### Suspected Cause
1. **File-level chunking threshold:** Because `starlette/middleware/exceptions.py` is 73 lines long (under the multi-chunk threshold), `chunks.jsonl` contains only a single `kind: "whole_file"` chunk (`chunk_bc810fb27ebf2a31`). It lacks fine-grained AST entity chunks for individual method declarations (`http_exception` vs `websocket_exception`).
2. **Selective extraction heuristic in Business Path Compiler:** When the Pass 1 LLM or business path compiler synthesizes concrete method spans from the whole-file chunk, it extracts `http_exception` (likely matched due to the HTTP response return type `PlainTextResponse` resolving to a chunk in `responses.py`), but drops `websocket_exception` because its body returns `None` and only performs a side-effect (`await websocket.close()`).

### Suggested Validation & Fix
- Ensure that the workflow compiler's reference collector includes all methods registered in the middleware's internal dispatch table (`_exception_handlers`), particularly when the synthesized workflow title explicitly names both protocols.
- When an entity references a dispatch mapping (such as `{HTTPException: ..., WebSocketException: ...}`), both handlers should be emitted into the workflow's evidence list.

## 9. Duplicate check
We performed an exhaustive scan across all 735 open and closed issues in `FinanceFlash/unvibecode`:
- **Issue #736:** *"[Bug] Business Workflow Map — Config workflow omits Config.from_object() although its own title promises object-based loading"* — Reports omission of an object loader in Flask's config workflow. That issue concerns Flask's configuration loaders (`src/flask/config.py`), whereas this issue concerns Starlette's dual-protocol ASGI exception dispatching in `ExceptionMiddleware`.
- **Issue #715:** *"[Bug] Business Workflow Map — Implementation references list redundant class spans, omit node methods (prep/exec), and appear out of execution order"* — Concerns duplicated class spans and AST node execution ordering, not dual-protocol method omissions.
- **Issue #697:** *"[Bug] Python AST & Linker: PythonSemanticExtractor omits type aliases, dropping 225 symbol edges across 54 files in Starlette"* — Concerns Python type-alias omissions in the Connected Code Map linker, whereas this finding specifically investigates the Business Workflow Map compiler and its implementation reference omissions.
- **Issue #645:** *"[Bug] Connected Code Map drops Flask/Jinja url_for static asset links"* — Unrelated static asset linker issue.

No issue exists reporting the omission of WebSocket exception handlers in Starlette or multi-protocol middleware workflows.


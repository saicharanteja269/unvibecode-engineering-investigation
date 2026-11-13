"""
Reproduction script for Track 1 Issue:
Omission of WebSocketException / websocket_exception() in Starlette Workflow 3.
"""
import os
import re
import sys
from pathlib import Path

def main():
    print("Checking Starlette source code for ExceptionMiddleware handlers...")
    middleware_path = Path("starlette/starlette/middleware/exceptions.py")
    if not middleware_path.exists():
        print(f"Error: {middleware_path} not found. Please clone encode/starlette into ./starlette")
        return 1

    code = middleware_path.read_text(encoding="utf-8")
    has_http = "def http_exception" in code
    has_ws = "def websocket_exception" in code
    print(f"  ExceptionMiddleware.http_exception defined: {has_http}")
    print(f"  ExceptionMiddleware.websocket_exception defined: {has_ws}")

    print("\nChecking generated Business Workflow Map...")
    results_dir = Path("starlette_full_results")
    if not results_dir.exists():
        results_dir = Path("starlette_results")

    html_files = list(results_dir.rglob("business-workflows.html"))
    if not html_files:
        print("  business-workflows.html not found yet. Run unvibecode review on starlette first.")
        return 1

    html_content = html_files[0].read_text(encoding="utf-8")
    if "Handle exceptions raised while serving HTTP and WebSocket requests" in html_content:
        print("  Found Workflow 3: 'Handle exceptions raised while serving HTTP and WebSocket requests'")
        if "ExceptionMiddleware.http_exception()" in html_content:
            print("  [CONFIRMED] ExceptionMiddleware.http_exception() is listed in Implementation references.")
        if "ExceptionMiddleware.websocket_exception()" not in html_content:
            print("  [DEFECT CONFIRMED] ExceptionMiddleware.websocket_exception() is OMITTED from Implementation references!")
    else:
        print("  Workflow 3 not located in HTML.")

if __name__ == "__main__":
    sys.exit(main() or 0)

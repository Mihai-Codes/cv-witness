#!/usr/bin/env python3
"""Bounded CI-only browser diagnostic. This generates fictional text only."""

import os
from pathlib import Path
import subprocess
import tempfile
import time

from render_cv import browser_path


def main():
    if os.environ.get("CI", "").lower() != "true":
        raise SystemExit("This diagnostic is for an isolated CI runner.")
    browser = browser_path()
    print("Synthetic PDF smoke: starting selected browser", flush=True)
    with tempfile.TemporaryDirectory(prefix="cv-witness-ci-smoke-") as temporary:
        root = Path(temporary).resolve()
        source = root / "synthetic.html"
        pdf = root / "synthetic.pdf"
        source.write_text('<!doctype html><meta charset="utf-8"><style>@page{size:A4;margin:16mm}</style><h1>Synthetic export smoke</h1><p>Fictional text only.</p>', encoding="utf-8")
        command = [browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                   "--disable-background-networking", "--disable-extensions", "--no-first-run",
                   "--no-default-browser-check", "--host-resolver-rules=MAP * ~NOTFOUND",
                   "--user-data-dir=" + str(root / "profile"), "--print-to-pdf=" + str(pdf)]
        if os.environ.get("CV_WITNESS_CI_NO_SANDBOX") == "1":
            command.append("--no-sandbox")
        command.append(source.as_uri())
        start = time.monotonic()
        diagnostics = root / "browser-stderr.txt"
        timed_out = False
        with diagnostics.open("wb") as log:
            try:
                result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=log, timeout=20)
                returncode = result.returncode
            except subprocess.TimeoutExpired:
                timed_out = True
                returncode = -1
        exists = pdf.is_file() and pdf.stat().st_size > 0
        print(f"Synthetic smoke: seconds={time.monotonic()-start:.1f}; timed_out={timed_out}; exit={returncode}; pdf_created={exists}", flush=True)
        if returncode != 0 or not exists:
            with diagnostics.open("rb") as log:
                print(log.read(8192).decode("utf-8", errors="replace"), flush=True)
            raise SystemExit("Synthetic browser export failed; full PDF suite was not started.")
        print("Synthetic export ready.", flush=True)


if __name__ == "__main__":
    main()

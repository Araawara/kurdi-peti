#!/usr/bin/env python3
"""گەشەپێدانی فەرهەنگ: کۆکردنەوەی پێشنیارەکان، وشەی نوێ، پشکنین و بڵاوکردنەوە.

  python grow.py pull            پێشنیارەکانی بەکارهێنەران لە Vercel Blob دەهێنێت بۆ data/suggestions.jsonl
  python grow.py todo [N] [wiki] N وشەی گوماناوی نوێ لە کتێبەکان (یان ویکیپیدیا) بۆ data/todo.txt
  python grow.py merge FILE      زیادکردنی کۆمەڵەیەک (loan|variants|pure|level|origin|source) بە review: true
  python grow.py reject FILE     وشەکانی FILE (یەک لە هەر ڕیزێک) بۆ data/rejected.txt، تا دووبارە پێشنیار نەکرێنەوە
  python grow.py fp FILE         پشکنینی هەڵەی ناسینەوە: وشەکانی FILE لە کتێبەکاندا چی دەگرن
  python grow.py publish         build.py و نوێکردنەوەی سکیڵی Claude Code (Vercel لە ڕێگەی GitHubەوە بڵاو دەکاتەوە)
  python grow.py done            پێشنیارە نوێیەکان وەک چارەسەرکراو نیشان دەکات
  python grow.py sync            وەرگرتنی نوێترین وەشان لە GitHub (وشە پەسەندکراوەکانی Issues)
  python grow.py commit          ناردنی گۆڕانکارییەکانی ئەمڕۆ بۆ GitHub
  python grow.py stats           ژمارەکان
"""
import collections
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
SKILL = ROOT / "skills" / "kurdi-peti"
GLOSSARY = SKILL / "references" / "glossary.json"
MCP = ROOT / "mcp"
BLOB_API = "https://vercel.com/api/blob"
NPX = "npx.cmd" if os.name == "nt" else "npx"

spec = importlib.util.spec_from_file_location("check", SKILL / "scripts" / "check.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


def load():
    return json.loads(GLOSSARY.read_text(encoding="utf-8"))


def save(data):
    body = ",\n".join("    " + json.dumps(e, ensure_ascii=False) for e in data["entries"])
    GLOSSARY.write_text('{\n  "version": 1,\n  "about": ' + json.dumps(data["about"], ensure_ascii=False)
                        + ',\n  "entries": [\n' + body + "\n  ]\n}\n", encoding="utf-8")


def known_forms(entries):
    return {f for e in entries for f in [e["loan"], *e.get("variants", [])]}


def log(msg):
    DATA.mkdir(exist_ok=True)
    with open(DATA / "growth.log", "a", encoding="utf-8") as fh:
        fh.write(f"{time.strftime('%Y-%m-%d %H:%M')}  {msg}\n")
    print(msg)


# ---- pull: user suggestions from Vercel Blob ----

def blob_env():
    subprocess.run([NPX, "-y", "vercel@latest", "env", "pull", ".env.local", "--yes"], cwd=MCP,
                   check=True, capture_output=True)
    env = {}
    for line in (MCP / ".env.local").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"')
    return env["VERCEL_OIDC_TOKEN"], env["BLOB_STORE_ID"]


def blob_request(url, token, store, method="GET", body=None):
    headers = {"authorization": f"Bearer {token}", "x-vercel-blob-store-id": store, "x-api-version": "13"}
    if body is not None:
        headers["content-type"] = "application/json"
        body = json.dumps(body).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=body, method=method, headers=headers), timeout=30) as r:
        return r.read()


def cmd_pull():
    token, store = blob_env()
    listing = json.loads(blob_request(f"{BLOB_API}?{urlencode({'prefix': 'suggestions/', 'limit': 1000})}", token, store))
    blobs = listing.get("blobs", [])
    got = []
    for b in blobs:
        try:
            got.append(json.loads(blob_request(b.get("downloadUrl") or b["url"], token, store)))
        except Exception as exc:  # keep the blob for the next run
            print(f"skip {b.get('pathname')}: {exc}")
            blobs = [x for x in blobs if x is not b]
    if got:
        with open(DATA / "suggestions.jsonl", "a", encoding="utf-8") as fh:
            for s in got:
                fh.write(json.dumps({**s, "status": "new"}, ensure_ascii=False) + "\n")
    if blobs:
        blob_request(f"{BLOB_API}/delete", token, store, "POST", {"urls": [b["url"] for b in blobs]})
    log(f"pull: {len(got)} پێشنیاری نوێ")


# ---- todo: next corpus candidates ----

def cmd_todo(n=150, source="corpus"):
    entries = load()["entries"]
    skip = known_forms(entries) | {p for e in entries for p in e["pure"]}
    rejected = DATA / "rejected.txt"
    if rejected.exists():
        skip |= {w.strip() for w in rejected.read_text(encoding="utf-8").splitlines() if w.strip()}
    out = []
    path = DATA / "wiki" / "wiki_candidates.tsv" if source == "wiki" else DATA / "loan_candidates.tsv"
    for line in path.read_text(encoding="utf-8").splitlines()[1:]:
        stem, freq, reason, example = line.split("\t")
        if stem in skip or example in skip or any(rx.fullmatch(example) for rx, _ in COMPILED_CACHE(entries)):
            continue
        out.append(f"{example}\t{freq}")
        if len(out) >= n:
            break
    (DATA / "todo.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"todo: {len(out)} وشە ← data/todo.txt")


_compiled = None


def COMPILED_CACHE(entries):
    global _compiled
    if _compiled is None:
        _compiled = check.compile_entries(entries, False)
    return _compiled


# ---- merge / reject ----

def cmd_merge(path):
    data = load()
    entries = data["entries"]
    known = known_forms(entries)
    pure_words = {p for e in entries for p in e["pure"]}
    added, skipped = 0, []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        loan, variants, pure, level, origin, source = (x.strip() for x in line.split("|"))
        if loan in known or loan in pure_words or level not in ("core", "strict"):
            skipped.append(loan)
            continue
        variants = [v for v in dict.fromkeys(variants.split(",")) if v and v != loan and v not in known and v not in pure_words]
        entries.append(dict(loan=loan, variants=variants, origin=origin, pure=[p.strip() for p in pure.split(",")],
                            level=level, source=source, review=True))
        known.update([loan, *variants])
        added += 1
    save(data)
    log(f"merge {Path(path).name}: {added} زیادکرا، {len(skipped)} پشتگوێخرا {skipped[:20]}، کۆ: {len(entries)}")


def cmd_reject(path):
    words = [w.strip() for w in Path(path).read_text(encoding="utf-8").splitlines() if w.strip()]
    with open(DATA / "rejected.txt", "a", encoding="utf-8") as fh:
        fh.write("\n".join(words) + "\n")
    log(f"reject: {len(words)} وشە")


# ---- fp: what would these entries match in the corpus ----

def cmd_fp(path):
    loans = {l.split("|")[0].strip() for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()}
    comp = check.compile_entries([e for e in load()["entries"] if e["loan"] in loans], False)
    words = collections.Counter()
    for f in (DATA / "corpus").glob("*.txt"):
        for w in re.findall(f"[{check.LETTERS}]+", f.read_text(encoding="utf-8").translate(check.CHAR_MAP)):
            words[w] += 1
    hits = collections.defaultdict(collections.Counter)
    for w, n in words.items():
        for rx, e in comp:
            if rx.fullmatch(w):
                hits[e["loan"]][w] += n
                break
    for loan, c in sorted(hits.items(), key=lambda kv: -sum(kv[1].values())):
        print(loan, sum(c.values()), "|", " ".join(f"{w}:{n}" for w, n in c.most_common(8)))


# ---- publish ----

def cmd_publish():
    for d in SKILL.rglob("__pycache__"):
        shutil.rmtree(d)
    subprocess.run([sys.executable, str(ROOT / "build.py")], check=True)
    for d in (MCP / "api").rglob("__pycache__"):
        shutil.rmtree(d)
    installed = Path.home() / ".claude" / "skills" / "kurdi-peti"
    shutil.rmtree(installed, ignore_errors=True)
    shutil.copytree(SKILL, installed)
    # Vercel is connected to GitHub (root directory: mcp), so `commit` deploys the connector.
    log(f"publish: {len(load()['entries'])} وشە دروستکرا؛ دوای commit، Vercel خۆکارانە بڵاوی دەکاتەوە")


def git(*args, check=True):
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def cmd_sync():
    """Pick up words approved on GitHub (issues, pull requests) before today's work."""
    git("pull", "--rebase", "--autostash")
    log(f"sync: {git('log', '-1', '--format=%h %s').stdout.strip()}")


def cmd_commit():
    """Commit today's glossary changes and push them to GitHub, so the open dictionary grows too."""
    git("add", "skills/kurdi-peti/references", "mcp/api/kp_check.py", "mcp/api/kp_data.py",
        "data/rejected.txt", *[str(p.relative_to(ROOT)) for p in DATA.glob("batch-*.txt")],
        *[str(p.relative_to(ROOT)) for p in DATA.glob("reject-*.txt")])
    if git("diff", "--cached", "--quiet", check=False).returncode == 0:
        log("commit: هیچ گۆڕانکارییەک نییە")
        return
    total = len(load()["entries"])
    git("commit", "-m", f"گەشەی ڕۆژانە: {time.strftime('%Y-%m-%d')} · {total} وشە",
        "-m", "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
    git("pull", "--rebase", "--autostash")
    git("push")
    log(f"commit: بۆ GitHub نێردرا ({total} وشە)")


def cmd_done():
    path = DATA / "suggestions.jsonl"
    if path.exists():
        path.write_text(path.read_text(encoding="utf-8").replace('"status": "new"', '"status": "done"'), encoding="utf-8")
    log("done: پێشنیارەکان وەک چارەسەرکراو نیشانکران")


def cmd_stats():
    entries = load()["entries"]
    review = sum(1 for e in entries if e.get("review"))
    new = 0
    if (DATA / "suggestions.jsonl").exists():
        new = sum(1 for l in (DATA / "suggestions.jsonl").read_text(encoding="utf-8").splitlines()
                  if '"status": "new"' in l)
    print(f"وشە: {len(entries)}  |  پێداچوونەوە ماوە: {review}  |  پێشنیاری نوێ: {new}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = sys.argv[1:] or ["stats"]
    cmd = args[0]
    if cmd == "pull":
        cmd_pull()
    elif cmd == "todo":
        cmd_todo(int(args[1]) if len(args) > 1 else 150, args[2] if len(args) > 2 else "corpus")
    elif cmd in ("merge", "reject", "fp"):
        {"merge": cmd_merge, "reject": cmd_reject, "fp": cmd_fp}[cmd](args[1])
    elif cmd == "publish":
        cmd_publish()
    elif cmd == "done":
        cmd_done()
    elif cmd == "sync":
        cmd_sync()
    elif cmd == "commit":
        cmd_commit()
    else:
        cmd_stats()

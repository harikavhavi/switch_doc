"""Compare proposed customer promises against release evidence."""

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "case" / "evidence.json"
CLAIMS = ROOT / "case" / "claims.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def review(evidence, claims):
    if not isinstance(claims, list) or not claims:
        raise ValueError("Provide a nonempty JSON list of claim IDs.")
    if any(not isinstance(item, str) for item in claims):
        raise ValueError("Every claim ID must be a string.")
    if len(set(claims)) != len(claims):
        raise ValueError("Duplicate claim IDs.")
    rows = []
    for claim_id in claims:
        claim = evidence["claims"].get(claim_id)
        if claim is None:
            raise ValueError(f"Unknown claim ID {claim_id!r}.")
        checks = claim["requires"]
        missing = [key for key in checks if evidence["checks"].get(key) is not True]
        rows.append({
            "id": claim_id,
            "copy": claim["copy"],
            "checks": checks,
            "missing": missing,
            "reason": claim["reason"],
        })
    snapshot = {"release": evidence["release"], "evidence": evidence, "claims": claims}
    encoded = json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "release": evidence["release"],
        "revision": hashlib.sha256(encoded).hexdigest(),
        "status": "BLOCKED" if any(row["missing"] for row in rows) else "READY FOR HUMAN",
        "claims": rows,
    }


def publish(report, revision):
    if report["status"] != "READY FOR HUMAN":
        raise ValueError("Blocked claims must be removed or backed by passing evidence.")
    if report["revision"] != revision:
        raise ValueError("Stale approval. Review the current snapshot and get a fresh approval.")
    release = report["release"]
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.-]{0,63}", release):
        raise ValueError("Invalid release identifier.")
    target = ROOT / "receipts" / f"{release}-{revision}.md"
    lines = [
        f"# Release note — {release}", "",
        *(f"- {row['copy']}" for row in report["claims"]),
        "", "---", "", f"Review revision: `{revision}`", "",
        "Evidence checked:",
        *(f"- {row['id']}: {', '.join(row['checks'])}" for row in report["claims"]),
        "",
    ]
    content = "\n".join(lines).encode("utf-8")
    target.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=target.parent) as staging:
        draft = Path(staging) / "receipt.md"
        draft.write_bytes(content)
        try:
            if os.name == "nt":
                draft.rename(target)
            else:
                os.link(draft, target)
        except FileExistsError:
            if target.read_bytes() != content:
                raise ValueError(f"Receipt exists with different content: {target.name}")
    return target.relative_to(ROOT)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("review", "publish"))
    parser.add_argument("--claims", type=Path, default=CLAIMS)
    parser.add_argument("--revision")
    args = parser.parse_args()
    try:
        report = review(load(EVIDENCE), load(args.claims))
        if args.command == "publish":
            print(publish(report, args.revision))
        else:
            print(json.dumps(report, indent=2, ensure_ascii=True))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

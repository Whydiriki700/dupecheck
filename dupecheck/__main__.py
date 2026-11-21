"""CLI: python -m dupecheck DIR [DIR ...] [--min-size BYTES] [--plan] [--json]"""
import argparse
import json
import sys

from .core import find_duplicates, human


def main(argv=None):
    parser = argparse.ArgumentParser(prog="dupecheck", description="Find duplicate files by content.")
    parser.add_argument("dirs", nargs="+", help="Folders to scan")
    parser.add_argument("--min-size", type=int, default=1, help="Ignore files smaller than this many bytes")
    parser.add_argument("--plan", action="store_true",
                        help="Print a keep plan: the first file of each group is kept, the rest are copies")
    parser.add_argument("--json", action="store_true", help="Print the report as JSON")
    args = parser.parse_args(argv)

    result = find_duplicates(args.dirs, min_size=args.min_size)
    if args.json:
        print(json.dumps(result, indent=2))
        return 0
    print(f"scanned: {result['scanned']} files; duplicate groups: {len(result['groups'])}; "
          f"wasted: {human(result['total_wasted'])}")
    for group in result["groups"]:
        print(f"\n{human(group['size'])} each, {len(group['files'])} copies, "
              f"wasted {human(group['wasted'])}")
        for idx, path in enumerate(group["files"]):
            if args.plan:
                label = "KEEP" if idx == 0 else "COPY"
                print(f"  [{label}] {path}")
            else:
                print(f"  {path}")
    if result["groups"]:
        print("\ndupecheck never deletes anything. Review the copies yourself, or rerun with --plan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

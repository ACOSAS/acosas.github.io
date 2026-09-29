#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


HTTP_METHODS = {"get", "put", "post", "delete", "patch", "options", "head", "trace"}
ALLOWED_SLOTS = {
    "after_summary",
    "after_description",
    "after_parameters",
    "after_request_body",
    "after_responses",
    "after_page",
}
AFTER_PAGE_INCLUDE = '{% include swagger_json/overlay_slot.md slot="after_page" %}'
GET_PATH_INCLUDE = "{% include swagger_json/get_path.md %}"


def assert_under_root(path: Path, root: Path) -> Path:
    resolved = path.resolve()
    root_resolved = root.resolve()
    if not resolved.is_relative_to(root_resolved):
        raise ValueError(f"Refusing to write outside pages checkout: {resolved}")
    return resolved


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def load_yaml(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
    except ImportError:
        raw = subprocess.check_output(
            [
                "ruby",
                "-ryaml",
                "-rjson",
                "-e",
                "puts JSON.generate(YAML.load_file(ARGV[0]) || {})",
                str(path),
            ],
            text=True,
        )
        data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def permalink_for(swagger_file: str, path: str) -> str:
    value = f"{swagger_file}_{path}"
    return re.sub(r"[+\s{}/]", "_", value).lower() + ".html"


def component_permalink(document: dict) -> str:
    title = document["info"]["title"]
    value = re.sub(r"[+\s{}/]", "_", title).lower()
    return f"{value}_components.html"


def path_is_deprecated(path_item: dict) -> bool:
    operations = [value for key, value in path_item.items() if key.lower() in HTTP_METHODS]
    return bool(operations) and all(operation.get("deprecated") is True for operation in operations)


def add_folder(lines: list[str], title: str, items: list[tuple[str, str]]) -> None:
    lines.extend(
        [
            f"  - title: {yaml_quote(title)}",
            "    output: web",
            "    type: frontmatter",
            "    folderitems:",
        ]
    )
    for item_title, url in items:
        lines.extend(
            [
                f"    - title: {yaml_quote(item_title)}",
                f"      url: {yaml_quote(url)}",
                "      output: web, pdf",
            ]
        )


def add_subfolders(
    lines: list[str], sections: list[tuple[str, list[tuple[str, str]]]]
) -> None:
    lines.append("      subfolders:")
    for title, items in sections:
        lines.extend(
            [
                f"      - title: {yaml_quote(title)}",
                "        output: web",
                "        subfolderitems:",
            ]
        )
        for item_title, url in items:
            lines.extend(
                [
                    f"        - title: {yaml_quote(item_title)}",
                    f"          url: {yaml_quote(url)}",
                    "          output: web, pdf",
                ]
            )


def strip_fragment_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text.strip() + "\n"
    end = text.find("\n---", 3)
    if end == -1:
        return text.strip() + "\n"
    return text[end + 4 :].lstrip("\n")


def collect_permalinks(pages_root: Path) -> set[str]:
    found: set[str] = set()
    pattern = re.compile(r"^permalink:\s*(\S+)\s*$", re.MULTILINE)
    for path in pages_root.rglob("*.md"):
        match = pattern.search(path.read_text(encoding="utf-8"))
        if not match:
            continue
        permalink = match.group(1).strip().strip("\"'")
        found.add(permalink)
        found.add(permalink.lstrip("/"))
        found.add("/" + permalink.lstrip("/"))
    return found


def unpublished_permalinks(pages_root: Path) -> set[str]:
    """Permalinks for pages Jekyll will not emit (`published: false`)."""
    found: set[str] = set()
    permalink_re = re.compile(r"^permalink:\s*(\S+)\s*$", re.MULTILINE)
    for path in pages_root.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end == -1:
            continue
        front = text[:end]
        if not re.search(r"^published:\s*false\s*$", front, re.MULTILINE):
            continue
        match = permalink_re.search(front)
        if not match:
            continue
        permalink = match.group(1).strip().strip("\"'")
        found.add(permalink)
        found.add(permalink.lstrip("/"))
        found.add("/" + permalink.lstrip("/"))
    return found


def write_metadata_page(pages_root: Path, target: Path, permalink: str, document: dict) -> None:
    publication = document.get("info", {}).get("x-acos-publication")
    if not publication:
        return
    generated_raw = str(publication.get("generatedAt", "")).replace("Z", "+00:00")
    generated = datetime.fromisoformat(generated_raw) if generated_raw else None
    generated_text = generated.strftime("%Y-%m-%dT%H:%M:%SZ") if generated else ""
    version = (
        publication.get("userApiVersion")
        or publication.get("apiVersion")
        or document.get("info", {}).get("version", "")
    )
    content = f"""---
title: Publiseringsmetadata
permalink: {permalink}
---

# Publiseringsmetadata

Denne dokumentasjonsleveransen ble generert fra samme bygg som OpenAPI-filen.

| Felt | Verdi |
|---|---|
| Versjon | `{version}` |
| Commit SHA | `{publication.get("commitSha", "")}` |
| Generert (UTC) | `{generated_text}` |

REST-referansen er generert fra OpenAPI-JSON med `build_pages.sh`. Overlay-innhold under `overlays/` er den autoritative kundeteksten som compose setter inn etterpå.
"""
    target = pages_root / target if not target.is_absolute() else target
    target.parent.mkdir(parents=True, exist_ok=True)
    assert_under_root(target, pages_root).write_text(content, encoding="utf-8")


def copy_fragments(product_dir: Path, product: str, includes_root: Path, pages_root: Path) -> None:
    source = product_dir / "fragments"
    dest = assert_under_root(includes_root / product, pages_root)
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)
    if not source.is_dir():
        return
    for fragment in source.glob("*.md"):
        if ".." in fragment.name or "/" in fragment.name or "\\" in fragment.name:
            raise ValueError(f"Unsafe fragment name: {fragment.name}")
        dest_file = assert_under_root(dest / fragment.name, pages_root)
        dest_file.write_text(fragment.read_text(encoding="utf-8"), encoding="utf-8")


def ensure_after_page_include(pages_root: Path, swagger_files: list[str]) -> None:
    swagger_dir = pages_root / "pages" / "swagger"
    if not swagger_dir.is_dir():
        return
    prefixes = tuple(name.replace(".json", "") for name in swagger_files)
    for page in swagger_dir.glob("*.md"):
        text = page.read_text(encoding="utf-8")
        if GET_PATH_INCLUDE not in text or AFTER_PAGE_INCLUDE in text:
            continue
        if page.name.startswith("websak__"):
            continue
        swaggerfile_match = re.search(r"^swaggerfile:\s*(\S+)\s*$", text, re.MULTILINE)
        if swaggerfile_match and swaggerfile_match.group(1) not in prefixes:
            continue
        page_path = assert_under_root(page, pages_root)
        page_path.write_text(
            text.replace(GET_PATH_INCLUDE, GET_PATH_INCLUDE + "\n" + AFTER_PAGE_INCLUDE),
            encoding="utf-8",
        )


def rest_items_for_document(
    swagger_basename: str,
    document: dict,
    split_deprecated: bool,
    models_title: str,
) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    current: list[tuple[str, str]] = []
    legacy: list[tuple[str, str]] = []
    for path, path_item in document.get("paths", {}).items():
        item = (path, "/" + permalink_for(swagger_basename, path))
        if split_deprecated and path_is_deprecated(path_item):
            legacy.append(item)
        else:
            current.append(item)
    current.append((models_title, "/" + component_permalink(document)))
    return current, legacy


def write_sidebar(pages_root: Path, spec: dict, swagger_docs: dict[str, dict]) -> None:
    sidebar_name = spec["sidebar"]
    title = spec["title"]
    lines = [
        f"# Generated by overlay compose ({spec['product']}).",
        "entries:",
        "- title: sidebar",
        "  folders:",
    ]
    overview = spec.get("overview")
    hidden = unpublished_permalinks(pages_root)
    guides = sorted(spec.get("guides") or [], key=lambda item: (item.get("order", 100), item.get("title", "")))
    legacy_guides = spec.get("legacy_guides") or []
    for item in guides + legacy_guides:
        url = item.get("url") or ""
        if url in hidden:
            print(
                f"Skipping unpublished sidebar link: {item.get('title')} ({url})",
                file=sys.stderr,
            )
    guides = [item for item in guides if (item.get("url") or "") not in hidden]
    legacy_guides = [item for item in legacy_guides if (item.get("url") or "") not in hidden]
    rest_sections: list[tuple[str, list[tuple[str, str]]]] = []
    legacy_items: list[tuple[str, str]] = [(item["title"], item["url"]) for item in legacy_guides]

    for swagger in spec.get("swagger_files") or []:
        filename = swagger["file"]
        basename = filename.replace(".json", "")
        document = swagger_docs[filename]
        split_deprecated = bool(swagger.get("split_deprecated"))
        models_title = swagger.get("models_title") or f"{document['info']['title']} Models"
        current, legacy = rest_items_for_document(
            basename, document, split_deprecated, models_title
        )
        rest_sections.append((swagger.get("rest_folder", "REST-referanse"), current))
        if swagger.get("legacy_folder"):
            legacy_items.extend(legacy)
        elif legacy:
            models = current.pop()
            current.extend(legacy)
            current.append(models)

    if overview or guides:
        first_item = (
            [(overview["title"], overview["url"])] if overview else [(guides[0]["title"], guides[0]["url"])]
        )
        remaining_guides = guides if overview else guides[1:]
        add_folder(lines, title, first_item)
        sections: list[tuple[str, list[tuple[str, str]]]] = []
        if remaining_guides:
            sections.append(("Guider", [(item["title"], item["url"]) for item in remaining_guides]))
        sections.extend(rest_sections)
        if legacy_items:
            sections.append((spec.get("legacy_folder", "Legacy"), legacy_items))
        add_subfolders(lines, sections)
    else:
        flat: list[tuple[str, str]] = []
        for _folder, items in rest_sections:
            flat.extend(items)
        add_folder(lines, title, flat)

    sidebar_path = pages_root / "_data/sidebars" / Path(sidebar_name).name
    sidebar_path.parent.mkdir(parents=True, exist_ok=True)
    assert_under_root(sidebar_path, pages_root).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated sidebar {sidebar_path}")


def write_index(pages_root: Path, product_dir: Path, spec: dict) -> None:
    index = spec.get("index")
    if not index:
        return
    fragments = sorted(index.get("fragments") or [], key=lambda item: item.get("order", 100))
    parts = [
        "---",
        "# Generated by scripts/compose-overlays.py. Edit overlays/%s/ instead." % spec["product"],
        "title: %s" % index["title"],
        "keywords: %s" % index.get("keywords", "json, openapi"),
        "permalink: %s" % index["permalink"],
        "---",
        "",
    ]
    heading = index.get("heading")
    if heading:
        parts.append(f"# {heading}")
        parts.append("")
    for item in fragments:
        source = product_dir / item["source"]
        parts.append(strip_fragment_frontmatter(source.read_text(encoding="utf-8")).rstrip())
        parts.append("")
    target = Path(index["file"])
    if not target.is_absolute():
        target = pages_root / target
    target.parent.mkdir(parents=True, exist_ok=True)
    assert_under_root(target, pages_root).write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Generated index {target}")


def compose_product(
    pages_root: Path,
    product_dir: Path,
    spec: dict,
    swagger_docs: dict[str, dict],
    overlay_entries: list[dict],
    referenced_fragments: set[Path],
    errors: list[str],
) -> None:
    product = spec.get("product") or product_dir.name
    spec["product"] = product
    copy_fragments(product_dir, product, pages_root / "_includes/overlays", pages_root)

    swagger_files_cfg = spec.get("swagger_files") or []
    ensure_after_page_include(pages_root, [item["file"] for item in swagger_files_cfg])

    for swagger in swagger_files_cfg:
        filename = swagger["file"]
        json_path = pages_root / "_data/swagger" / filename
        if not json_path.is_file():
            errors.append(f"{product}: missing swagger file {json_path}")
            continue
        swagger_docs[filename] = json.loads(json_path.read_text(encoding="utf-8"))

    for rest in spec.get("rest") or []:
        source = product_dir / rest["source"]
        slot = rest.get("slot")
        swaggerfile = rest.get("swaggerfile")
        path = rest.get("path")
        if slot not in ALLOWED_SLOTS:
            errors.append(f"{product}: invalid slot {slot!r} in {rest}")
        if not source.is_file():
            errors.append(f"{product}: missing rest fragment {source}")
            continue
        referenced_fragments.add(source.resolve())
        document_name = None
        for swagger in swagger_files_cfg:
            if swagger["file"].replace(".json", "") == swaggerfile:
                document_name = swagger["file"]
                break
        document = swagger_docs.get(document_name or f"{swaggerfile}.json")
        if document is None:
            errors.append(f"{product}: rest overlay swaggerfile {swaggerfile} is not in swagger_files")
        elif path not in document.get("paths", {}):
            errors.append(f"{product}: rest overlay path {path} not in {swaggerfile}")
        overlay_include = f"overlays/{product}/{source.name}"
        body = strip_fragment_frontmatter(source.read_text(encoding="utf-8")).rstrip()
        existing = next(
            (
                entry
                for entry in overlay_entries
                if entry["swaggerfile"] == swaggerfile
                and entry["path"] == path
                and entry["slot"] == slot
            ),
            None,
        )
        if existing:
            if overlay_include not in existing["includes"]:
                existing["includes"].append(overlay_include)
            existing["markdown"] = (existing.get("markdown") or "") + "\n\n" + body
        else:
            overlay_entries.append(
                {
                    "swaggerfile": swaggerfile,
                    "path": path,
                    "slot": slot,
                    "includes": [overlay_include],
                    "markdown": body,
                }
            )

    index = spec.get("index") or {}
    for item in index.get("fragments") or []:
        source = product_dir / item["source"]
        if not source.is_file():
            errors.append(f"{product}: missing index fragment {source}")
            continue
        referenced_fragments.add(source.resolve())

    fragments_dir = product_dir / "fragments"
    if fragments_dir.is_dir():
        for fragment in fragments_dir.glob("*.md"):
            if fragment.resolve() not in referenced_fragments:
                errors.append(f"{product}: fragment {fragment.name} is not referenced in placements.yml")

    write_index(pages_root, product_dir, spec)
    write_sidebar(pages_root, spec, swagger_docs)

    metadata = spec.get("metadata")
    if metadata:
        filename = metadata.get("swagger_file") or (swagger_files_cfg[0]["file"] if swagger_files_cfg else None)
        if filename and filename in swagger_docs:
            write_metadata_page(
                pages_root,
                pages_root / metadata["file"],
                metadata["permalink"],
                swagger_docs[filename],
            )


def dump_overlays_yaml(entries: list[dict]) -> str:
    lines = [
        "# Generated by scripts/compose-overlays.py. Do not edit.",
        "entries:",
    ]
    if not entries:
        lines.append("  []")
        return "\n".join(lines) + "\n"
    for entry in entries:
        lines.append(f"  - swaggerfile: {yaml_quote(entry['swaggerfile'])}")
        lines.append(f"    path: {yaml_quote(entry['path'])}")
        lines.append(f"    slot: {yaml_quote(entry['slot'])}")
        lines.append("    includes:")
        for include in entry["includes"]:
            lines.append(f"      - {yaml_quote(include)}")
        lines.append(f"    markdown: {yaml_quote(entry.get('markdown', ''))}")
    return "\n".join(lines) + "\n"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: scripts/compose-overlays.py <pages-checkout>", file=sys.stderr)
        return 2

    pages_root = Path(sys.argv[1]).resolve()
    overlays_root = pages_root / "overlays"
    if not overlays_root.is_dir():
        print(f"No overlays directory at {overlays_root}", file=sys.stderr)
        return 1

    swagger_docs: dict[str, dict] = {}
    overlay_entries: list[dict] = []
    referenced_fragments: set[Path] = set()
    errors: list[str] = []
    required_permalinks: list[str] = []

    includes_root = pages_root / "_includes/overlays"
    includes_root.mkdir(parents=True, exist_ok=True)

    for product_dir in sorted(path for path in overlays_root.iterdir() if path.is_dir()):
        placements_path = product_dir / "placements.yml"
        if not placements_path.is_file():
            errors.append(f"{product_dir.name}: missing placements.yml")
            continue
        spec = load_yaml(placements_path)
        required_permalinks.extend(spec.get("required_permalinks") or [])
        compose_product(
            pages_root,
            product_dir,
            spec,
            swagger_docs,
            overlay_entries,
            referenced_fragments,
            errors,
        )

    overlays_data = pages_root / "_data/overlays.yml"
    assert_under_root(overlays_data, pages_root).write_text(dump_overlays_yaml(overlay_entries), encoding="utf-8")
    print(f"Wrote {overlays_data}")

    permalinks = collect_permalinks(pages_root)
    for permalink in required_permalinks:
        if permalink not in permalinks:
            errors.append(f"required permalink missing: {permalink}")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"Composed overlays for {pages_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

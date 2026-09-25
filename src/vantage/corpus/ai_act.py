"""Ingest the official French AI Act (Regulation (EU) 2024/1689) from EUR-Lex HTML.

Every Chunk lies within one structural unit: an article paragraph (or a whole
article when it has no numbered paragraphs), a recital, or an annex. A unit
longer than MAX_CHARS is split into its labelled points, recursively; each
point's Chunk is prefixed with the lead-in sentences of the units above it, so
it still reads on its own. Articles and annexes are `contraignant`, recitals
`interprétatif`, and everything is `public`.
"""

import argparse
import json
import re
import sys
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from lxml import html
from lxml.html import HtmlElement

from vantage.corpus.model import AccessLevel, Chunk, Portee

SOURCE_URL = "https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=CELEX:32024R1689"
RAW_PATH = Path("data/raw/ai-act-fr.html")
DOCUMENT_ID = "ai-act"
CITATION = "AI Act"
MAX_CHARS = 2000

_PARAGRAPH_ID = re.compile(r"^\d{3}\.\d{3}$")
_PARAGRAPH_NUMBER = re.compile(r"^(\d+)\.\s+")
_ENUMERATION_LABEL = re.compile(r"^(\d+(?:\.\d+)*)\.\s+")
_SECTION_HEADING = re.compile(r"^Section\s+([A-Z0-9]+)\b\s*[.\-–]?\s*(.*)$")
_NUMBERED_HEADING = re.compile(r"^(\d+)\.\s+(.*)$")


@dataclass
class _Unit:
    """A node of the Act's structure: lead-in text, labelled points, trailing text."""

    segment: tuple[str, str] | None = None  # ("para" | "section" | "point", label)
    label: str = ""  # as printed in the Act, e.g. "4." or "a)"
    title: str = ""
    lead: list[str] = field(default_factory=list)
    items: list["_Unit"] = field(default_factory=list)
    tail: list[str] = field(default_factory=list)

    def render(self) -> str:
        lines = list(self.lead)
        for item in self.items:
            body = item.render()
            lines.append(f"{item.label} {body}" if item.label else body)
        lines.extend(self.tail)
        return "\n".join(line for line in lines if line)


def parse_ai_act(document: HtmlElement) -> list[Chunk]:
    """Turn the EUR-Lex HTML of the AI Act into Chunks, in reading order."""
    for note_ref in document.xpath('//a[starts-with(@href, "#ntr")]'):
        note_ref.drop_tree()
    chunks: list[Chunk] = []
    for recital in document.xpath('//div[starts-with(@id, "rct_")]'):
        chunks.extend(_recital_chunks(recital))
    for article in document.xpath('//div[starts-with(@id, "art_") and not(contains(@id, "."))]'):
        chunks.extend(_article_chunks(article))
    for annex in document.xpath('//div[starts-with(@id, "anx_")]'):
        chunks.extend(_annex_chunks(annex))
    return chunks


def load_ai_act(path: Path = RAW_PATH) -> list[Chunk]:
    return parse_ai_act(html.parse(str(path)).getroot())


def _recital_chunks(recital: HtmlElement) -> list[Chunk]:
    number = recital.get("id").removeprefix("rct_")
    cells = recital.xpath(".//td")
    body = _block(list(cells[-1]))
    return [_chunk(f"Considérant {number}", [], body.render(), Portee.INTERPRETATIF, "")]


def _article_chunks(article: HtmlElement) -> list[Chunk]:
    number = article.get("id").removeprefix("art_")
    base = f"Article {number}"
    title = _text_of(article.xpath('./div[@class="eli-title"]'))
    body = [
        child
        for child in article
        if child.get("class") not in ("oj-ti-art", "eli-title")
    ]
    paragraphs = [child for child in body if _PARAGRAPH_ID.match(child.get("id") or "")]
    if not paragraphs:
        return _emit(_block(body), base, [], [], Portee.CONTRAIGNANT, title)
    chunks = []
    for paragraph in paragraphs:
        unit = _block(list(paragraph))
        if unit.lead:
            match = _PARAGRAPH_NUMBER.match(unit.lead[0])
            if match:
                unit.segment = ("para", match.group(1))
                unit.lead[0] = unit.lead[0][match.end():]
        path = [unit.segment] if unit.segment else []
        chunks.extend(_emit(unit, base, path, [], Portee.CONTRAIGNANT, title))
    return chunks


def _annex_chunks(annex: HtmlElement) -> list[Chunk]:
    number = annex.get("id").removeprefix("anx_")
    base = f"Annexe {number}"
    titles = annex.xpath('./p[@class="oj-doc-ti"]')
    title = _clean(titles[1].text_content()) if len(titles) > 1 else ""
    current: list[HtmlElement] = []
    sections: list[tuple[str, list[HtmlElement]]] = []
    for child in annex:
        if child.get("class") == "oj-doc-ti":
            continue
        if child.get("class") == "oj-ti-grseq-1":
            heading = _clean(child.text_content())
            if sections and not sections[-1][1] and not _looks_labelled(heading):
                # "Section 1" followed by its subtitle on a separate line.
                sections[-1] = (f"{sections[-1][0]}. {heading}", [])
            else:
                sections.append((heading, []))
            continue
        (sections[-1][1] if sections else current).append(child)
    root = _block(current)
    for heading, elements in sections:
        section = _block(elements)
        section.segment, section.title = _section_segment(heading)
        section.lead.insert(0, heading)
        root.items.append(section)
    return _emit(root, base, [], [], Portee.CONTRAIGNANT, title)


def _emit(
    unit: _Unit,
    base: str,
    path: list[tuple[str, str]],
    context: list[str],
    portee: Portee,
    heading: str,
) -> list[Chunk]:
    """One Chunk for the unit, or one per labelled point when the unit is too long."""
    heading = " — ".join(part for part in (heading, unit.title) if part)
    text = unit.render()
    splittable = [item for item in unit.items if item.segment is not None]
    if len("\n".join(context + [text])) <= MAX_CHARS or not splittable:
        return [_chunk(base, path, _join(context, text), portee, heading)]
    chunks = []
    child_context = context + unit.lead
    for item in unit.items:
        if item.segment is None:
            child_context = child_context + [item.render()]
            continue
        label = item.label
        leaf = _Unit(
            segment=item.segment,
            title=item.title,
            lead=[f"{label} {line}" if label and i == 0 else line for i, line in enumerate(item.lead)]
            or ([label] if label else []),
            items=item.items,
            tail=item.tail,
        )
        chunks.extend(_emit(leaf, base, path + [item.segment], child_context, portee, heading))
    if unit.tail:
        chunks.append(_chunk(base, path, _join(context + unit.lead, "\n".join(unit.tail)), portee, heading))
    return chunks


def _block(elements: list[HtmlElement]) -> _Unit:
    """Parse a run of sibling elements into lead-in text, points and trailing text."""
    unit = _Unit()
    for element in elements:
        if element.tag == "table":
            for row in element.xpath("./tbody/tr | ./tr"):
                cells = [cell for cell in row.xpath("./td") if _clean(cell.text_content())]
                if len(cells) < 2:
                    unit.items.append(_Unit(lead=[_clean(row.text_content())]))
                    continue
                label = _clean(cells[0].text_content())
                item = _cell(cells[-1])
                if _is_label(label):
                    item.segment, item.label = ("point", _normalise_label(label)), label
                else:
                    item.lead.insert(0, label)
                unit.items.append(item)
        elif element.get("class") == "oj-enumeration-spacing":
            text = _clean(element.text_content())
            match = _ENUMERATION_LABEL.match(text)
            if match:
                unit.items.append(
                    _Unit(segment=("point", match.group(1)), label=f"{match.group(1)}.", lead=[text[match.end():]])
                )
            else:
                unit.items.append(_Unit(lead=[text]))
        elif element.xpath(".//table"):
            nested = _block(list(element))
            (unit.tail if unit.items else unit.lead).extend(nested.lead)
            unit.items.extend(nested.items)
            unit.tail.extend(nested.tail)
        else:
            text = _clean(element.text_content())
            if text:
                (unit.tail if unit.items else unit.lead).append(text)
    return unit


def _cell(cell: HtmlElement) -> _Unit:
    """The content cell of a point: plain text, or a block when it nests further points."""
    if not cell.xpath(".//table"):
        return _Unit(lead=[_clean(cell.text_content())])
    unit = _block(list(cell))
    if cell.text and cell.text.strip():
        unit.lead.insert(0, _clean(cell.text))
    return unit


def _section_segment(heading: str) -> tuple[tuple[str, str] | None, str]:
    match = _SECTION_HEADING.match(heading)
    if match:
        return ("section", match.group(1)), match.group(2)
    match = _NUMBERED_HEADING.match(heading)
    if match:
        return ("point", match.group(1)), match.group(2)
    return None, heading


def _looks_labelled(heading: str) -> bool:
    return bool(_SECTION_HEADING.match(heading) or _NUMBERED_HEADING.match(heading))


def _is_label(label: str) -> bool:
    return bool(label) and label not in ("—", "-", "–")


def _normalise_label(label: str) -> str:
    return label.rstrip(".") if re.fullmatch(r"\d+(\.\d+)*\.", label) else label


def _reference(base: str, path: list[tuple[str, str]]) -> str:
    parts = [CITATION, base]
    points: list[str] = []
    for kind, label in path:
        if kind == "point":
            if points and label.startswith(points[-1] + "."):
                points[-1] = label
            else:
                points.append(label)
            continue
        if points:
            parts.append("point " + " ".join(points))
            points = []
        parts.append(f"§{label}" if kind == "para" else f"section {label}")
    if points:
        parts.append("point " + " ".join(points))
    return ", ".join(parts)


def _chunk(base: str, path: list[tuple[str, str]], text: str, portee: Portee, heading: str) -> Chunk:
    return Chunk(
        document_id=DOCUMENT_ID,
        reference=_reference(base, path),
        portee=portee,
        access_level=AccessLevel.PUBLIC,
        heading=heading,
        text=text,
    )


def _join(context: list[str], text: str) -> str:
    return "\n".join(line for line in context + [text] if line)


def _text_of(elements: list[HtmlElement]) -> str:
    return _clean(" ".join(element.text_content() for element in elements))


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def fetch(path: Path = RAW_PATH) -> None:
    request = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request) as response:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(response.read())


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["fetch", "chunk"])
    parser.add_argument("--raw", type=Path, default=RAW_PATH)
    args = parser.parse_args(argv)
    if args.command == "fetch":
        fetch(args.raw)
        return
    for chunk in load_ai_act(args.raw):
        sys.stdout.write(json.dumps(chunk.to_dict(), ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()

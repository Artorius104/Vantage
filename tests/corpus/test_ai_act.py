import re
from collections import Counter

import pytest
from lxml import html

from vantage.corpus.ai_act import RAW_PATH, load_ai_act
from vantage.corpus.model import AccessLevel, Portee

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII"]


@pytest.fixture(scope="module")
def chunks():
    return load_ai_act()


@pytest.fixture(scope="module")
def by_reference(chunks):
    return {chunk.reference: chunk for chunk in chunks}


def _units(chunks, pattern):
    return {m.group(1) for c in chunks if (m := re.match(pattern, c.reference))}


def test_covers_every_article_recital_and_annex(chunks):
    assert _units(chunks, r"AI Act, Article (\d+)\b") == {str(n) for n in range(1, 114)}
    assert _units(chunks, r"AI Act, Considérant (\d+)$") == {str(n) for n in range(1, 181)}
    assert _units(chunks, r"AI Act, Annexe ([IVX]+)\b") == set(ROMAN)


def test_every_chunk_is_public_with_portee_from_its_position(chunks):
    for chunk in chunks:
        assert chunk.document_id == "ai-act"
        assert chunk.access_level is AccessLevel.PUBLIC
        expected = Portee.INTERPRETATIF if "Considérant" in chunk.reference else Portee.CONTRAIGNANT
        assert chunk.portee is expected, chunk.reference


def test_references_are_unique(chunks):
    duplicates = [ref for ref, n in Counter(c.reference for c in chunks).items() if n > 1]
    assert duplicates == []


def test_no_text_of_the_act_is_lost(chunks):
    document = html.parse(str(RAW_PATH)).getroot()
    for note_ref in document.xpath('//a[starts-with(@href, "#ntr")]'):
        note_ref.drop_tree()
    corpus = " ".join(re.sub(r"\s+", " ", c.text) for c in chunks)
    paragraphs = document.xpath(
        '//div[starts-with(@id, "art_") or starts-with(@id, "rct_") or starts-with(@id, "anx_")]'
        '//p[@class="oj-normal"]'
    )
    missing = []
    for paragraph in paragraphs:
        text = re.sub(r"\s+", " ", paragraph.text_content().replace("\xa0", " ")).strip()
        text = re.sub(r"^\d+\.\s+", "", text)  # paragraph numbers become the § of the Référence
        is_label = re.fullmatch(r"\(\d+\)|[a-z]+\)|\d+(\.\d+)*\.?|—", text)
        if not is_label and text not in corpus:
            missing.append(text[:80])
    assert missing == []


def test_article_paragraph_is_its_own_chunk(by_reference):
    chunk = by_reference["AI Act, Article 6, §2"]
    assert chunk.text.startswith("Outre les systèmes d’IA à haut risque visés au paragraphe 1")
    assert chunk.heading.startswith("Règles relatives à la classification")


def test_long_unit_is_split_into_points_with_its_lead_in(by_reference):
    definitions = [ref for ref in by_reference if ref.startswith("AI Act, Article 3, point ")]
    assert len(definitions) == 68
    chunk = by_reference["AI Act, Article 3, point 1)"]
    assert chunk.text.startswith("Aux fins du présent règlement, on entend par:\n1) «système d’IA»")


def test_annex_point_keeps_its_letters_and_the_annex_lead_in(by_reference):
    chunk = by_reference["AI Act, Annexe III, point 4"]
    assert "Emploi, gestion de la main-d'œuvre" in chunk.text
    assert "a) systèmes d'IA destinés à être utilisés pour le recrutement" in chunk.text
    assert chunk.text.startswith("Les systèmes d'IA à haut risque au sens de l'article 6")


def test_annex_sections_appear_in_the_reference(by_reference):
    assert "AI Act, Annexe VIII, section A" in by_reference
    assert "AI Act, Annexe I, section B, point 13" in by_reference


def test_footnote_markers_are_removed(by_reference):
    assert "(5)" not in by_reference["AI Act, Considérant 8"].text

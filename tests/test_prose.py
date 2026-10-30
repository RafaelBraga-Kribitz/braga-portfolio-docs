"""The sentence model (readme_quality.prose) and the three v1.5 checks built on it."""
from __future__ import annotations

import json
import textwrap

import pytest

from readme_quality import cli, prose
from readme_quality.registry import Project
from tests import fixtures as F
from tests.conftest import make_repo, run, statuses
from tests.test_gate import COMM_FILES, COMMON_FILES, comm_project


# ---------------------------------------------------------------- extraction
def test_code_tables_headings_badges_and_links_are_not_prose():
    text = "\n".join([
        "# A heading that has many words in it",
        "[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)",
        "![A figure of the weekly forecast](docs/assets/hero.png)",
        "| a table row | with many words in it |",
        "|---|---|",
        "```python", "this is code with many words in it", "```",
        "~~~", "so is this fenced line with many words", "~~~",
        "<!-- a comment with many words", "that spans two lines -->",
        "<details>", '<img src="a.png"', '     alt="alt text with many words" />', "</details>",
        "[ref]: https://example.com/a/b",
        "[Only a link to the results](#results)",
        "- [Results](#results) · [Method](#method)",
        "The buyer chooses the cheaper crew.",
    ])
    assert prose.prose_lines(text) == [(21, "The buyer chooses the cheaper crew.")]


def test_markers_links_and_code_spans_are_reduced_to_words():
    text = ("- **Bold** item with a [link text](https://example.com) and `code` inside\n> quoted line has three words\n"
            "1. numbered item has words\n- [x] done item has words")
    assert [t for _, t in prose.prose_lines(text)] == [
        "Bold item with a link text and x inside", "quoted line has three words", "numbered item has words", "done item has words"]
    # underscores inside identifiers survive; emphasis underscores do not
    assert prose.prose_lines("_Emphasis_ around C1_forecast_timeline stays")[0][1] == "Emphasis around C1_forecast_timeline stays"


# ---------------------------------------------------------------- sentences and blocks
def test_a_list_item_is_one_sentence():
    text = "- First item without a full stop\n- Second item without a full stop\n\nThis ends here. This is the next one."
    assert [s.line for s in prose.sentences(text)] == [1, 2, 4, 4]
    wrapped = "- First item without a\n  full stop at all\n- Second item without a\n  full stop either"
    assert [(s.line, s.text) for s in prose.sentences(wrapped)] == [
        (1, "First item without a full stop at all"), (3, "Second item without a full stop either")]


def test_a_wrapped_paragraph_is_joined_and_each_sentence_reports_its_first_line():
    text = ("The buyer decides which crew to hire and\nhow to staff it. Then the plan\nis reviewed by the team.\n\n"
            "A new paragraph starts here.")
    assert [(s.line, s.text) for s in prose.sentences(text)] == [
        (1, "The buyer decides which crew to hire and how to staff it."), (2, "Then the plan is reviewed by the team."),
        (5, "A new paragraph starts here.")]


def test_hard_breaks_and_quote_boundaries_start_new_blocks():
    assert len(prose.sentences("First half of a line  \nsecond half after two spaces")) == 2
    assert len(prose.sentences("First half of a line\\\nsecond half after a backslash")) == 2
    assert len(prose.sentences("First half of a line<br>\nsecond half after a break tag")) == 2
    assert len(prose.sentences("> A quoted line that wraps\n> onto a second line here")) == 1
    assert len(prose.sentences("> A quoted line that wraps\n> - a list item inside it")) == 2
    assert len(prose.sentences("A paragraph line that runs\n> then a quote starts here")) == 2
    assert len(prose.sentences("> A quote that is split\n>\n> by an empty quote line here")) == 2


@pytest.mark.parametrize("width", [40, 80, 120])
def test_soft_wrapping_does_not_change_the_measurements(width):
    paras = ["The procurement manager decides which crew to hire next year. " + " ".join(["word"] * 29) + ". Short plain sentence here.",
             "The model is built from the export and is checked against the holdout. It runs weekly."]
    items = ["First list item that is long enough to wrap over several lines in the source file.",
             "Second list item with a Layer 2 code inside it and some more words to wrap."]

    def render(w):
        out = [textwrap.fill(p, w) for p in paras]
        out.append("\n".join(textwrap.fill(i, w, initial_indent="- ", subsequent_indent="  ") for i in items))
        return "\n\n".join(out)

    base, wrapped = render(10_000), render(width)
    assert wrapped.count("\n") > base.count("\n")
    assert [s.text for s in prose.sentences(wrapped)] == [s.text for s in prose.sentences(base)]
    assert prose.prose_stats(wrapped) == prose.prose_stats(base)
    stats = prose.prose_stats(base)
    assert (stats.n_sentences, stats.n_long) == (6, 1)
    assert [h.code for h in prose.internal_codes(wrapped)] == ["Layer 2"]


def test_short_fragments_are_not_sentences():
    assert prose.sentences("Too short.\n\nAlso two.") == []


def test_abbreviations_and_decimals_do_not_split():
    one = "Use a tool, e.g. Power BI, vs. Excel, etc. Fig. 3 shows ca. 9.5 percent, approx. 40 kg per month."
    assert len(prose.sentences(one)) == 1
    assert len(prose.sentences("Error fell from 18.0 to 9.5 percent in the holdout.")) == 1
    two = prose.sentences("Error fell to 9.5. The next step is the rollout.")
    assert [s.text for s in two] == ["Error fell to 9.5.", "The next step is the rollout."]


def test_passive_heuristic_positive_and_negative():
    assert prose.sentences("The data is stored in a warehouse.")[0].passive
    assert prose.sentences("The chart was built from the export.")[0].passive
    assert not prose.sentences("The buyer chooses the cheaper crew.")[0].passive
    assert not prose.sentences("We store the data in a warehouse.")[0].passive


def test_prose_stats_counts_long_passive_and_ste_ok():
    long_ = " ".join(["word"] * 26) + "."
    text = f"{long_}\n\nThe data is stored in a warehouse.\n\nThe buyer chooses the cheaper crew.\n\nAnother short plain sentence here."
    st = prose.prose_stats(text)
    assert (st.n_sentences, st.n_long, st.n_passive, st.n_ste_ok) == (4, 1, 1, 2)
    assert (st.long_share, st.passive_share, st.ste_share) == (25.0, 25.0, 50.0)
    assert prose.prose_stats("").ste_share == 0.0


# ---------------------------------------------------------------- indented code
def test_indented_code_is_dropped_so_it_cannot_supply_findings():
    code = ("Intro line before the block.\n\n    The analyst chooses Layer 2 and F-222.\n    A second code line here too.\n\n"
            "Outro line after the block.")
    assert [s.text for s in prose.sentences(code)] == ["Intro line before the block.", "Outro line after the block."]
    assert prose.internal_codes(code) == [] and prose.decision_owner(code) is None
    only = "# T\n\n    The analyst chooses Layer 2 and F-222.\n\n## Next\nText."
    assert prose.sentences(only) == [] and prose.internal_codes(only) == [] and prose.decision_owner(only) is None
    tab = "# T\n\n\tThe analyst chooses Layer 2 and F-222.\n\n## Next\nText."
    assert prose.sentences(tab) == [] and prose.internal_codes(tab) == [] and prose.decision_owner(tab) is None
    assert prose.sentences("# T\n    The analyst chooses the crew.\n") == []          # right after a heading


def test_indented_text_after_a_paragraph_line_or_in_a_list_is_prose():
    # code cannot interrupt a paragraph
    assert [s.text for s in prose.sentences("A paragraph line that\n    continues on an indented line.")] == [
        "A paragraph line that continues on an indented line."]
    # a list continuation stays prose, also after a blank line inside the list
    lst = ("- A list item that starts here.\n\n    The analyst chooses Layer 2 and F-222 here.\n\n"
           "1. Numbered item here.\n\n   Continued numbered text here.")
    assert [s.text for s in prose.sentences(lst)] == [
        "A list item that starts here.", "The analyst chooses Layer 2 and F-222 here.", "Numbered item here.", "Continued numbered text here."]
    assert [h.code for h in prose.internal_codes(lst)] == ["Layer 2", "F-222"]
    # code inside a list item (content column + 4) is still code
    assert [s.text for s in prose.sentences("- Item text goes here.\n\n      Code inside the list item here.")] == ["Item text goes here."]
    # an unindented paragraph after a blank line ends the list
    assert prose.sentences("- Item text goes here.\n\nBack outside the list.\n\n    Now this is code.") == [
        prose.Sentence(1, "Item text goes here.", 4, False), prose.Sentence(3, "Back outside the list.", 4, False)]


def test_html_blocks_with_indented_content_are_not_code():
    html = ("<table>\n  <tr>\n    <td>\n      <strong>Rafael Braga-Kribitz</strong><br />\n"
            "      Graz, Austria · Portfolio project, 2026\n    </td>\n  </tr>\n</table>")
    assert [s.text for s in prose.sentences(html)] == ["Graz, Austria · Portfolio project, 2026"]


# ---------------------------------------------------------------- internal codes
@pytest.mark.parametrize("code", ["F-222", "D-026", "OQ-02", "ADR-001", "BQ45", "S1_03", "S-pricing-tier",
                                  "Layer 2", "Layer P", "Layer 1/2/3", "Module A", "C1_forecast_timeline"])
def test_each_code_pattern_hits(code):
    hits = prose.internal_codes(f"The result depends on {code} for the decision.")
    assert [h.code for h in hits] == [code]


def test_codes_in_code_tables_and_link_targets_are_not_reported():
    text = "The `F-222` flag matters here.\n| F-222 | a table cell |\nSee [the note](docs/F-222.md) for details.\n```\nF-222 in a fence\n```"
    assert prose.internal_codes(text) == []


def test_legend_sections_and_definition_lines_are_excluded():
    text = "\n".join([
        "## Results", "Cost depends on F-222 in this run.", "## Finding legend", "The flag F-230 marks a gap here.",
        "### Sub heading", "More about F-231 sits under the legend.", "## Next section", "Then F-240 appears after it.",
        "- F-250: the lean mix of staff", "**F-251** — the lean mix of staff"])
    assert [(h.line, h.code) for h in prose.internal_codes(text)] == [(2, "F-222"), (8, "F-240")]
    assert prose.internal_codes("## Glossary\nD-026 stays in the glossary as a term.") == []


def test_allowlisted_prefixes_are_not_codes():
    assert prose.internal_codes("The date follows ISO-8601 and RFC-2119 and COVID-19 rules.") == []


def test_a_code_that_wraps_over_a_line_end_is_still_found_on_the_line_where_it_starts():
    assert prose.internal_codes("The result uses Layer\n2.") == [prose.CodeHit(1, "Layer 2")]
    assert prose.internal_codes("The first line is short.\nThe result uses Module\nA and then stops.") == [prose.CodeHit(2, "Module A")]
    assert prose.internal_codes("Intro text for the line.\nIt reads Layer P/R/D\nhere.") == [prose.CodeHit(2, "Layer P/R/D")]


@pytest.mark.parametrize("width", [12, 17, 24, 33, 60, 10_000])
def test_wrapping_inside_multiword_codes_gives_the_same_hit_list(width):
    para = ("The result uses Layer 2 and Module A, then Layer P/R/D and F-222 plus S1_03 and C1_forecast_timeline "
            "in a long sentence, and ISO-8601 stays out.")
    wrapped = textwrap.fill(para, width, break_on_hyphens=False, break_long_words=False)
    assert [h.code for h in prose.internal_codes(wrapped)] == [
        "Layer 2", "Module A", "Layer P/R/D", "F-222", "S1_03", "C1_forecast_timeline"]
    # every hit is reported on the wrapped line where the code starts
    lines = wrapped.split("\n")
    for h in prose.internal_codes(wrapped):
        assert h.code.split()[0] in lines[h.line - 1]


def test_definition_lines_and_legend_sections_stay_exempt_when_wrapped():
    defs = "- F-250: the lean mix of staff\n  and robots in the plan\n- F-251 — the same mix\n  with Layer 2 inside it"
    assert [(h.line, h.code) for h in prose.internal_codes(defs)] == [(4, "Layer 2")]
    legend = "## Finding legend\n\nThe flag Layer\n2 marks a gap and F-230\nmarks another one.\n\n## Next\n\nThe flag Layer\n2 appears here."
    assert [(h.line, h.code) for h in prose.internal_codes(legend)] == [(9, "Layer 2")]
    # only the code that opens the definition is exempt, not the same code later in the paragraph
    assert [h.code for h in prose.internal_codes("F-222: the lean mix, compared with F-230 here.")] == ["F-230"]


# ---------------------------------------------------------------- fences
def test_a_blockquote_fence_is_code_and_cannot_supply_findings():
    quoted = "# T\n\n> ```text\n> The analyst chooses Layer 2 and F-222.\n> ```\n\n## Next\nText."
    assert prose.sentences(quoted) == [] and prose.internal_codes(quoted) == [] and prose.decision_owner(quoted) is None
    nested = "# T\n\n> > ~~~\n> > The analyst chooses Layer 2 and F-222.\n> > ~~~\n"
    assert prose.sentences(nested) == [] and prose.internal_codes(nested) == []
    # the quote ends before the fence does: what follows the quote is prose again
    open_ = "> ```\n> code line inside the quote\n\nProse after the quote ends."
    assert [s.text for s in prose.sentences(open_)] == ["Prose after the quote ends."]


def test_a_fence_inside_a_list_item_or_a_quoted_list_is_code():
    lst = "- Item text goes here.\n  ```text\n  The analyst chooses Layer 2 and F-222.\n  ```\n\nAfter the list prose.\n"
    assert [s.text for s in prose.sentences(lst)] == ["Item text goes here.", "After the list prose."]
    assert prose.internal_codes(lst) == []
    marker = "- ```text\n  The analyst chooses Layer 2.\n  ```\n\nAfter the list prose."
    assert prose.internal_codes(marker) == [] and [s.text for s in prose.sentences(marker)] == ["After the list prose."]
    quoted = "- Item text goes here.\n  > ```text\n  > The analyst chooses Layer 2 and F-222.\n  > ```\n\nAfter the list prose."
    assert prose.internal_codes(quoted) == [] and [s.text for s in prose.sentences(quoted)] == ["Item text goes here.", "After the list prose."]


def test_a_fence_closes_only_on_the_same_character_at_least_as_long_with_no_info_string():
    four = "Before the block here.\n\n````md\n```\nThe analyst chooses Layer 2 and F-222.\n```\n````\n\nAfter the block here."
    assert [s.text for s in prose.sentences(four)] == ["Before the block here.", "After the block here."]
    assert prose.internal_codes(four) == [] and prose.decision_owner(four) is None
    info = "```\n```text\nThe analyst chooses Layer 2.\n```\n\nAfter the block here."
    assert [s.text for s in prose.sentences(info)] == ["After the block here."] and prose.internal_codes(info) == []
    longer = "```\ninside here\n`````\n\nAfter the block here."                       # a longer run closes
    assert [s.text for s in prose.sentences(longer)] == ["After the block here."]


def test_tilde_fences_follow_the_same_rules():
    tilde = "Before the block here.\n\n~~~\nThe analyst chooses Layer 2.\n~~~\n\nAfter the block here."
    assert [s.text for s in prose.sentences(tilde)] == ["Before the block here.", "After the block here."]
    long_tilde = "~~~~\n~~~\nThe analyst chooses Layer 2.\n~~~~\n\nAfter the block here."
    assert [s.text for s in prose.sentences(long_tilde)] == ["After the block here."] and prose.internal_codes(long_tilde) == []
    mixed = "```\n~~~\nThe analyst chooses Layer 2.\n```\n\nAfter the block here."     # tildes do not close backticks
    assert [s.text for s in prose.sentences(mixed)] == ["After the block here."] and prose.internal_codes(mixed) == []
    inline = "```x``` starts this line and reads as prose."                            # a backtick in the info string: not a fence
    assert len(prose.sentences(inline)) == 1


# ---------------------------------------------------------------- decision owner
def test_decision_owner_found_and_not_found():
    got = prose.decision_owner("# T\n\nA procurement manager decides which crew to buy.\n\n## Results\nText.")
    assert got and got.role.lower() == "procurement" and got.verb.lower() == "decides" and got.line == 3
    assert prose.decision_owner("# T\n\nA forecasting pipeline with a holdout.\n\n## Results\nThe manager decides.") is None
    assert prose.decision_owner("# T\n\nThe analyst reads the report.\n\n## Results\nText.") is None   # role, no decision
    assert prose.decision_owner("# T\n\nChoose the best option.\n\n## Results\nText.") is None          # decision, no role
    assert prose.decision_owner("# T\n\nWhich crew should the team staff first?") is not None
    assert prose.decision_owner("# T\n\nWhich crew should the\nteam staff first?") is not None          # wrapped


# ---------------------------------------------------------------- the checks
def _finding(rep, rid):
    return next(f for f in rep.findings if f.id == rid)


def test_the_three_checks_are_recommended_in_the_manifest(manifest):
    assert manifest.version == "1.6.0"
    for rid in ("communication.plain_language", "communication.no_internal_codes", "communication.decision_owner"):
        r = manifest.get(rid)
        assert r.severity == "recommended" and not r.excellence and r.remediation == "manual"


def test_prose_checks_pass_on_the_well_communicated_fixture(tmp_path, manifest, registry):
    repo = make_repo(tmp_path, "study", F.COMMUNICATION, COMM_FILES)
    st = statuses(run(repo, comm_project(repo), manifest, registry))
    assert st["communication.plain_language"] == "PASS"
    assert st["communication.no_internal_codes"] == "PASS"


def test_plain_language_warns_on_long_sentences_and_is_na_when_short(tmp_path, manifest, registry):
    long_ = " ".join(["Word"] * 30) + "."
    text = F.COMMUNICATION.replace("## Limitations", "## Notes\n\n" + "\n".join([long_] * 12) + "\n\n## Limitations", 1)
    repo = make_repo(tmp_path, "study", text, COMM_FILES)
    f = _finding(run(repo, comm_project(repo), manifest, registry), "communication.plain_language")
    assert f.status == "WARN" and "exceed 25 words" in f.message and "under 20 %" in f.message and 0 < len(f.evidence) <= 5

    tiny = make_repo(tmp_path, "tiny", "# Tiny\n\nOne short line here.\n", COMM_FILES)
    assert statuses(run(tiny, comm_project(tiny), manifest, registry))["communication.plain_language"] == "NOT_APPLICABLE"


def test_plain_language_sees_a_long_sentence_that_is_hard_wrapped(tmp_path, manifest, registry):
    long_ = textwrap.fill(" ".join(["Word"] * 30) + ".", 60)
    text = F.COMMUNICATION.replace("## Limitations", "## Notes\n\n" + "\n\n".join([long_] * 12) + "\n\n## Limitations", 1)
    repo = make_repo(tmp_path, "study", text, COMM_FILES)
    assert _finding(run(repo, comm_project(repo), manifest, registry), "communication.plain_language").status == "WARN"


def test_no_internal_codes_warns_with_line_and_code(tmp_path, manifest, registry):
    text = F.COMMUNICATION.replace("## Limitations", "## Notes\n\nThe cost gap follows F-222 and Layer 2 in the run.\n\n## Limitations", 1)
    repo = make_repo(tmp_path, "study", text, COMM_FILES)
    f = _finding(run(repo, comm_project(repo), manifest, registry), "communication.no_internal_codes")
    assert f.status == "WARN" and "2 bare internal code(s)" in f.message and "F-222" in f.message and "Layer 2" in f.message
    legend = F.COMMUNICATION.replace("## Limitations", "## Code legend\n\nThe cost gap follows F-222 in the run.\n\n## Limitations", 1)
    repo2 = make_repo(tmp_path, "study2", legend, COMM_FILES)
    assert statuses(run(repo2, comm_project(repo2), manifest, registry))["communication.no_internal_codes"] == "PASS"


def test_decision_owner_warns_without_a_role_and_passes_with_one(tmp_path, manifest, registry):
    plain = F.ANALYTICAL.replace("Which of two order-forecast methods should a small bakery use to plan flour purchases",
                                 "Two order-forecast methods compared on flour purchases")
    repo = make_repo(tmp_path, "plain", plain, COMMON_FILES)
    p = Project(name="plain", path=str(repo), type="analytical", status="Complete", banner="generated")
    f = _finding(run(repo, p, manifest, registry), "communication.decision_owner")
    assert f.status == "WARN" and "names no role that decides" in f.message
    owned = plain.replace("Two order-forecast methods compared", "The bakery owner decides between two order-forecast methods compared")
    repo2 = make_repo(tmp_path, "owned", owned, COMMON_FILES)
    p2 = Project(name="owned", path=str(repo2), type="analytical", status="Complete", banner="generated")
    assert statuses(run(repo2, p2, manifest, registry))["communication.decision_owner"] == "PASS"


# ---------------------------------------------------------------- the command
def test_prose_command_prints_the_keys_and_json(tmp_path, capsys):
    repo = make_repo(tmp_path, "study", "# T\n\nThe buyer decides which crew to hire.\n\n## Notes\n\nThe gap follows F-222 in this run.\n", {})
    assert cli.main(["prose", "--repo", str(repo)]) == 0
    out = capsys.readouterr().out
    for key in ("file = ", "sentences = 2", "long_share = 0.0 %", "passive_share = 0.0 %", "ste_share = 100.0 %",
                "internal_codes = 1", "  L7: F-222", "decision_owner = yes (buyer, decides)"):
        assert key in out
    assert cli.main(["prose", "--file", str(repo / "README.md"), "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["n_sentences"] == 2 and data["codes"] == [{"line": 7, "code": "F-222"}] and data["decision_owner"]["role"] == "buyer"

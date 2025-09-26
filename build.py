#!/usr/bin/env python3

from pathlib import Path

from ryland import Ryland

from processing import read_alignment_A, read_alignment_B


ROOT_DIR = Path(__file__).parent
PANTRY_DIR = ROOT_DIR / "pantry"
DATA_DIR = ROOT_DIR / "data"

ryland = Ryland(__file__, url_root="/persian-crito-alignment/")

ryland.clear_output()

ryland.copy_to_output(PANTRY_DIR / "style.css")
ryland.add_hash("style.css")

ryland.render_template("404.html", "404.html")
ryland.render_template("home.html", "index.html")

for primary, secondary, literal in zip(
    read_alignment_A(DATA_DIR / "alignment_primary_corrected.txt"),
    read_alignment_B(DATA_DIR / "alignment_secondary_corrected.txt"),
    read_alignment_B(DATA_DIR / "alignment_literal_corrected.txt"),
):
    assert primary["sentence_id"] == secondary["sentence_id"] == literal["sentence_id"]
    sentence_id = int(primary["sentence_id"])

    assert secondary["ref"] == literal["ref"]
    assert secondary["greek_tokens"] == literal["greek_tokens"]

    greek_tokens = []
    for token in secondary["greek_tokens"]:
        if isinstance(token, tuple):
            text = token[0]
            token_idx = token[1]
            classes = [f"greek-{token_idx}"]
            for persian_idx in primary["greek_to_persian_alignments"].get(token_idx, []):
                classes.append(f"persian-primary-{persian_idx}")
            for persian_idx in secondary["greek_to_persian_alignments"].get(token_idx, []):
                classes.append(f"persian-secondary-{persian_idx}")
            for persian_idx in literal["greek_to_persian_alignments"].get(token_idx, []):
                classes.append(f"persian-literal-{persian_idx}")
            greek_tokens.append({"text": text, "classes": " ".join(classes)})
        else:
            greek_tokens.append({"text": token, "classes": ""})

    primary_tokens = []
    for token in primary["persian_tokens"]:
        if isinstance(token, tuple):
            text = token[0]
            token_idx = token[1]
            classes = [f"persian-primary-{token_idx}"]
            for greek_idx in primary["persian_to_greek_alignments"].get(token_idx, []):
                classes.append(f"greek-{greek_idx}")
            primary_tokens.append({"text": text, "classes": " ".join(classes)})
        else:
            primary_tokens.append({"text": token, "classes": ""})

    secondary_tokens = []
    for token in secondary["persian_tokens"]:
        if isinstance(token, tuple):
            text = token[0]
            token_idx = token[1]
            classes = [f"persian-secondary-{token_idx}"]
            for greek_idx in secondary["persian_to_greek_alignments"].get(token_idx, []):
                classes.append(f"greek-{greek_idx}")
            secondary_tokens.append({"text": text, "classes": " ".join(classes)})
        else:
            secondary_tokens.append({"text": token, "classes": ""})

    literal_tokens = []
    for token in literal["persian_tokens"]:
        if isinstance(token, tuple):
            text = token[0]
            token_idx = token[1]
            classes = [f"persian-literal-{token_idx}"]
            for greek_idx in literal["persian_to_greek_alignments"].get(token_idx, []):
                classes.append(f"greek-{greek_idx}")
            literal_tokens.append({"text": text, "classes": " ".join(classes)})
        else:
            literal_tokens.append({"text": token, "classes": ""})

    if sentence_id > 1:
        prev_url = f"{sentence_id - 1:03d}.html"
    else:
        prev_url = None

    if sentence_id < 267:
        next_url = f"{sentence_id + 1:03d}.html"
    else:
        next_url = None

    ryland.render_template("sentence.html", f"{primary['sentence_id']:03d}.html", {
        "sentence_id": sentence_id,
        "prev_url": prev_url,
        "next_url": next_url,
        "ref": secondary["ref"],
        "greek_tokens": greek_tokens,
        "primary_tokens": primary_tokens,
        "secondary_tokens": secondary_tokens,
        "literal_tokens": literal_tokens,
    })

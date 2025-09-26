# library for reading alignment files

from collections import defaultdict
from pathlib import Path


DATA = Path(__file__).parent / "data"


def read_alignment_A(path: Path):
    state = 0
    for line in path.read_text().splitlines():
        if state == 0:
            if line == "":
                continue
            elif line.startswith("#"):
                sentence_id = int(line[1:].strip())
                state = 1
            else:
                raise ValueError(f"In state {state}, expected empty line, got {line}")
        elif state == 1:
            full_persian = line.strip()
            state = 2
        elif state == 2:
            persian_tokens = []
            tokenized_persian = line.strip()
            for token in tokenized_persian.split():
                assert "{" in token
                assert token[-1] == "}"
                word, idx = token.split("{")
                idx = int(idx[:-1])
                f = full_persian.find(word)
                assert f != -1, sentence_id
                if f == 0:
                    full_persian = full_persian[len(word):]
                    persian_tokens.append((word, idx))
                else:
                    persian_tokens.append(full_persian[:f])
                    persian_tokens.append((word, idx))
                    full_persian = full_persian[f:][len(word):]
            alignments = defaultdict(list)
            state = 3
        elif state == 3:
            if line == "":
                state = 0
                yield {
                    "sentence_id": sentence_id,
                    "persian_tokens": persian_tokens,
                    "alignments": dict(alignments),
                }
            elif line.startswith("\t"):
                alignment = line.strip()
                greek_id = None
                for part in alignment.split():
                    if part.isdecimal():
                        assert greek_id is None
                        greek_id = int(part)
                    elif part[0] == "{" and part[-1] == "}":
                        assert greek_id is not None
                        persian_id = int(part[1:-1])
                        alignments[persian_id].append(greek_id)
                    else:
                        pass  # persian words
            else:
                raise ValueError(f"In sentence {sentence_id}, expected empty line or alignment, got {line}")
        else:
            raise ValueError(f"Unknown state {state}")
    yield {
        "sentence_id": sentence_id,
        "persian_tokens": persian_tokens,
        "alignments": dict(alignments),
    }


def read_alignment_B(path: Path):
    state = 0
    for line in path.read_text().splitlines():
        if state == 0:
            if line == "":
                continue
            elif line.startswith("#"):
                ref, sentence_id = line[1:].strip().split()
                sentence_id = int(sentence_id.strip("()"))
                state = 1
            else:
                raise ValueError(f"In state {state}, expected empty line, got {line}")
        elif state == 1:
            if line == "":
                state = 2
            else:
                raise ValueError(f"In sentence {sentence_id}, expected empty line, got {line}")
        elif state == 2:
            full_greek = line.strip()
            state = 3
        elif state == 3:
            full_persian = line.strip()
            state = 4
        elif state == 4:
            if line == "":
                state = 5
            else:
                raise ValueError(f"In sentence {sentence_id}, expected empty line, got {line}")
        elif state == 5:
            greek_tokens = []
            tokenized_greek = line.strip()
            for token in tokenized_greek.split():
                assert "[" in token
                assert token[-1] == "]"
                word, idx = token.split("[")
                idx = int(idx[:-1])
                f = full_greek.find(word)
                assert f != -1, sentence_id
                if f == 0:
                    full_greek = full_greek[len(word):]
                    greek_tokens.append((word, idx))
                else:
                    greek_tokens.append(full_greek[:f])
                    greek_tokens.append((word, idx))
                    full_greek = full_greek[f:][len(word):]
            state = 7
        elif state == 7:
            persian_tokens = []
            tokenized_persian = line.strip()
            for token in tokenized_persian.split():
                assert "{" in token
                assert token[-1] == "}"
                word, idx = token.split("{")
                idx = int(idx[:-1])
                f = full_persian.find(word)
                assert f != -1, sentence_id
                if f == 0:
                    full_persian = full_persian[len(word):]
                    persian_tokens.append((word, idx))
                else:
                    persian_tokens.append(full_persian[:f])
                    persian_tokens.append((word, idx))
                    full_persian = full_persian[f:][len(word):]
            alignments = defaultdict(list)
            state = 8
        elif state == 8:
            if line == "":
                state = 9
            else:
                raise ValueError(f"In sentence {sentence_id}, expected empty line, got {line}")
        elif state == 9:
            if line == "":
                state = 0
                yield {
                    "ref": ref,
                    "sentence_id": sentence_id,
                    "persian_tokens": persian_tokens,
                    "alignments": dict(alignments),
                }
            elif line.startswith("\t"):
                alignment = line.strip()
                greek_id = None
                for part in alignment.split():
                    if part[0] == "[" and part[-1] == "]":
                        assert greek_id is None
                        greek_id = int(part[1:-1])
                    elif part[0] == "{" and part[-1] == "}":
                        assert greek_id is not None
                        persian_id = int(part[1:-1])
                        alignments[persian_id].append(greek_id)
                    else:
                        pass  # persian words
            else:
                raise ValueError(f"In sentence {sentence_id}, expected empty line or alignment, got {line}")
        else:
            raise ValueError(f"Unknown state {state}")
    yield {
        "ref": ref,
        "sentence_id": sentence_id,
        "greek_tokens": greek_tokens,
        "persian_tokens": persian_tokens,
        "alignments": dict(alignments),
    }


if __name__ == "__main__":
    l1 = list(read_alignment_A(DATA / "alignment_primary_corrected.txt"))
    l2 = list(read_alignment_B(DATA / "alignment_secondary_corrected.txt"))
    l3 = list(read_alignment_B(DATA / "alignment_literal_corrected.txt"))

    assert len(l1) == len(l2) == len(l3) == 267


# library for reading alignment files

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
                persian_tokens.append((word, idx))
            state = 3
        elif state == 3:
            if line == "":
                state = 0
                # done with sentence
            elif line.startswith("\t"):
                alignment = line.strip()
            else:
                raise ValueError(f"In sentence {sentence_id}, expected empty line or alignment, got {line}")
        else:
            raise ValueError(f"Unknown state {state}")
    # done with sentence


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
                greek_tokens.append((word, idx))
            state = 7
        elif state == 7:
            persian_tokens = []
            tokenized_persian = line.strip()
            for token in tokenized_persian.split():
                assert "{" in token
                assert token[-1] == "}"
                word, idx = token.split("{")
                idx = int(idx[:-1])
                persian_tokens.append((word, idx))
            state = 8
        elif state == 8:
            if line == "":
                state = 9
            else:
                raise ValueError(f"In sentence {sentence_id}, expected empty line, got {line}")
        elif state == 9:
            if line == "":
                state = 0
                # done with sentence
            elif line.startswith("\t"):
                alignment = line.strip()
            else:
                raise ValueError(f"In sentence {sentence_id}, expected empty line or alignment, got {line}")
        else:
            raise ValueError(f"Unknown state {state}")
    # done with sentence


if __name__ == "__main__":
    read_alignment_A(DATA / "alignment_primary_corrected.txt")
    read_alignment_B(DATA / "alignment_secondary_corrected.txt")
    read_alignment_B(DATA / "alignment_literal_corrected.txt")

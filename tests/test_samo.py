import json
from pathlib import Path

from samo.monitor import prune_non_relevant_fields


def test_prune_non_relevant_fields() -> None:
    input_as_str = Path("tests/ships_example.json").read_text()
    expected_as_str = Path("tests/ships_expected.json").read_text()
    input = json.loads(input_as_str)
    expected = json.loads(expected_as_str)

    result = prune_non_relevant_fields(input)

    assert result == expected

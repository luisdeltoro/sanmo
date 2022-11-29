from datetime import datetime
import json
from pathlib import Path

from sanmo.monitor import prune_non_relevant_fields


def test_prune_non_relevant_fields() -> None:
    timestamp = datetime.strptime("2022-11-30_20:13:01", "%Y-%m-%d_%H:%M:%S")
    input_as_str = Path("tests/ships_example.json").read_text()
    expected_as_str = Path("tests/ships_expected.json").read_text()
    input = json.loads(input_as_str)
    expected = json.loads(expected_as_str)

    result = prune_non_relevant_fields(timestamp, input)
    print(result)
    assert result == expected

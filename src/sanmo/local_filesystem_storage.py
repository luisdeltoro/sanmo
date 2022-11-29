from datetime import datetime
import json
from pathlib import Path
from typing import Dict, List, Optional


def store(
    store_dir: str, timestamp: datetime, ships_price_info: List[Dict[str, Optional[str]]]
) -> None:
    file_name = timestamp.strftime("%Y-%m-%d_%H:%M:%S.json")
    Path(store_dir + "/" + file_name).write_text(json.dumps(ships_price_info))

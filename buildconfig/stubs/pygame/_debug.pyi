from collections.abc import Callable
from typing import Optional, Union

ImportResult = tuple[str, bool, Optional[Callable]]

def str_from_tuple(version_tuple: Union[tuple[int, int, int], None]) -> str: ...
def attempt_import(
    module: str, function_name: str, output_str: str = ""
) -> ImportResult: ...
def print_debug_info(filename: Optional[str] = None) -> None: ...

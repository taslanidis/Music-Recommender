import re
from typing import List, Any, Tuple


def clear_name_text(
    txt: str
) -> str:
    
    temp = txt.lower()
    temp = re.sub(r"\-\?\"\'\.", "", temp)
    return temp.strip()


def binary_search(alist: List[Any], item: Any) -> Tuple[int, bool]:
    index_first = 0
    index_last = len(alist) - 1
    found = False

    while index_first <= index_last and not found:
        pos = 0
        midpoint = (index_first + index_last)//2
        
        if alist[midpoint] == item:
            pos = midpoint
            found = True
        else:
            if item < alist[midpoint]:
                index_last = midpoint - 1
            else:
                index_first = midpoint + 1
    
    return (pos, found)
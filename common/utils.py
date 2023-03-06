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


def get_spotify_object_id(link: str) -> Tuple[bool, bool, str]:

    if link.lower().find("playlist/") != -1:
        return True, False, re.match(r'(^|(?<=playlist\/))[A-Za-z0-9]+($|\?si)', link).group(1)
    
    elif link.lower().find("track/") != -1:
        return False, True, re.match(r'(^|(?<=track\/))[A-Za-z0-9]+($|\?si)', link).group(1)
    
    return True, False, link
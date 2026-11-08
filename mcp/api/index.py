"""خاڵی چوونەژوورەوەی ڕاژەکار (server).

کۆدی سەرەکی لە پەڕگەی kp_server.py دایە. ئەم پەڕگەیە تەنها `annotations.title` بۆ هەر ئامرازێک
زیاد دەکات، بۆ ئەوەی فەرهەنگی connectorەکانی Anthropic ناوی ئامرازەکان بخوێنێتەوە.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kp_server  # noqa: E402


def _add_titles(value, seen):
    # بە ناو هەموو لیست و فەرهەنگەکاندا دەگەڕێت و ئامرازەکان دەدۆزێتەوە
    if id(value) in seen:
        return
    seen.add(id(value))
    if isinstance(value, dict):
        if "name" in value and "inputSchema" in value:
            title = value.get("title") or value["name"]
            # هەر ئامرازێک لەبەرگیراوەی خۆی وەردەگرێت، چونکە لەوانەیە هەمان فەرهەنگ هاوبەش بێت
            notes = dict(value.get("annotations") or {})
            notes["title"] = title
            value["annotations"] = notes
        for item in value.values():
            _add_titles(item, seen)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _add_titles(item, seen)


_seen = set()
for _value in list(vars(kp_server).values()):
    if isinstance(_value, (dict, list, tuple)):
        _add_titles(_value, _seen)

SERVER = kp_server.SERVER


class handler(kp_server.handler):
    # Vercel تەنها ئەو پەڕگەیە دروست دەکات کە ڕاستەوخۆ پۆلی `class handler` تێدایە
    pass

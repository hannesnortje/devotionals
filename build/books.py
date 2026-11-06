"""Bible books in canonical order (Protestant canon) with their shelf group.

Used by build.py to sort and group the series on the start page. A series finds
its book through the OSIS code of its source file (series/<slug>/source/<OSIS>-source.txt).
Group labels live in strings.py (keys shelf_<group> and testament_<ot|nt>).
"""

_GROUPS = [
    ("ot", "law", "Gen Exod Lev Num Deut"),
    ("ot", "history", "Josh Judg Ruth 1Sam 2Sam 1Kgs 2Kgs 1Chr 2Chr Ezra Neh Esth"),
    ("ot", "wisdom", "Job Ps Prov Eccl Song"),
    ("ot", "major", "Isa Jer Lam Ezek Dan"),
    ("ot", "minor", "Hos Joel Amos Obad Jonah Mic Nah Hab Zeph Hag Zech Mal"),
    ("nt", "gospels", "Matt Mark Luke John"),
    ("nt", "acts", "Acts"),
    ("nt", "paul", "Rom 1Cor 2Cor Gal Eph Phil Col 1Thess 2Thess 1Tim 2Tim Titus Phlm"),
    ("nt", "hebrews", "Heb"),
    ("nt", "general", "Jas 1Pet 2Pet 1John 2John 3John Jude"),
    ("nt", "revelation", "Rev"),
]

BOOKS = {}       # OSIS -> {"testament", "group", "canon"}
GROUP_ORDER = []  # group keys in canonical order
_i = 0
for testament, group, names in _GROUPS:
    GROUP_ORDER.append(group)
    for osis in names.split():
        _i += 1
        BOOKS[osis] = {"testament": testament, "group": group, "canon": _i}

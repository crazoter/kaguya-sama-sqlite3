#!/usr/bin/env python3

"""
schema.py: Defines schema for kaguya_data.db.
Auto-incremented columns are left out
"""

from enum import Enum

TBL_ACTION = "Action"
TBL_ARC = "Arc"
TBL_CHAPTER = "Chapter"
TBL_CHARACTER = "Character"
TBL_EVENT = "Event"
TBL_ITEM = "Item"
TBL_OPINION = "Opinion"
TBL_SERIES = "Series"
TBL_TOPIC = "Topic"
TBL_VOLUME = "Volume"
TBL_VOLUMECOVERCHARACTER = "VolumeCoverCharacter"

class ColumnEntry(Enum):
    name = 0,
    _type = 1,
    foreign_key_id = 2

# (Name, Type, Foreign Key for another Table (assumed to be primary key))
SCHEMA = {
    TBL_ACTION: [
        # ("Id", int, None), # Auto-incremented
        ("By", str, TBL_CHARACTER),
        ("OnCharacter", str, TBL_CHARACTER),
        ("OnItem", str, TBL_ITEM),
        ("Description", str, None),
        ("InPage", int, None),
        ("InChapter", float, TBL_CHAPTER)
    ],
    TBL_ARC: [
        # ("Id", int, None), # Auto-incremented
        ("Name", str, None)
    ],
    TBL_CHAPTER: [
        ("Number", float, None),
        ("Title", str, None),
        ("PageCount", int, None),
        ("VolumeNo", int, TBL_VOLUME),
        ("ArcId", int, TBL_ARC)
    ],
    TBL_CHARACTER: [
        ("Name", str, None),
        ("Gender", str, None),
        ("Occupation", str, None),
        ("Age", int, None)
    ],
    TBL_EVENT: [
        # ("Id", int, None), # Auto-incremented
        ("OnCharacter", str, TBL_CHARACTER),
        ("OnItem", str, TBL_ITEM),
        ("Description", str, None),
        ("InPage", int, None),
        ("InChapter", float, TBL_CHAPTER)
    ],
    TBL_ITEM: [
        ("Name", str, None),
        ("Description", str, None)
    ],
    TBL_OPINION: [
	    # ("Id", int, None), # Auto-incremented
	    ("By", str, TBL_CHARACTER),
	    ("OnCharacter", str, TBL_CHARACTER),
	    ("OnTopic", str, TBL_TOPIC),
	    ("OnItem", str, TBL_ITEM),
	    ("Description", str, None),
	    ("InPage", int, None),
	    ("InChapter", float, TBL_CHAPTER),
    ],
    TBL_SERIES: [
	    ("Name", str, None)
    ],
    TBL_TOPIC: [
	    ("Name", str, None),
	    ("Description", str, None)
    ],
    TBL_VOLUME: [
        ("Number", int, None),
        ("SeriesName", str, TBL_SERIES)
    ],
    TBL_VOLUMECOVERCHARACTER: [
        ("VolumeNo", int, TBL_VOLUME),
        ("CharacterName", str, TBL_CHARACTER)
    ]
}

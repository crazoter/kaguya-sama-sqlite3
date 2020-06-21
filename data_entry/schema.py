#!/usr/bin/env python3

"""
schema.py: Defines schema for kaguya_data.db.
Auto-incremented columns are left out
"""

TABLENAME_ACTION = "Action"
TABLENAME_ARC = "Arc"
TABLENAME_CHAPTER = "Chapter"
TABLENAME_CHARACTER = "Character"
TABLENAME_EVENT = "Event"
TABLENAME_ITEM = "Item"
TABLENAME_OPINION = "Opinion"
TABLENAME_SERIES = "Series"
TABLENAME_TOPIC = "Topic"
TABLENAME_VOLUME = "Volume"
TABLENAME_VOLUMECOVERCHARACTER = "VolumeCoverCharacter"

# Does not include type
SCHEMA = {
    "Action": [
        # "Id", # Auto-incremented
        "By",
        "OnCharacter",
        "OnItem",
        "Description",
        "InPage",
        "InChapter"
    ],
    "Arc": [
        # "Id", # Auto-incremented
        "Name"
    ],
    "Chapter": [
        "Number",
        "Title",
        "PageCount",
        "VolumeNo",
        "ArcId"
    ],
    "Character": [
        "Name",
        "Gender",
        "Occupation",
        "Age"
    ],
    "Event": [
        # "Id", # Auto-incremented
        "OnCharacter",
        "OnItem",
        "Description",
        "InPage",
        "InChapter"
    ],
    "Item": [
        "Name",
        "Description"
    ],
    "Opinion": [
	    # "Id", # Auto-incremented
	    "By",
	    "OnCharacter",
	    "OnTopic",
	    "OnItem",
	    "Description",
	    "InPage",
	    "InChapter",
    ],
    "Series": [
	    "Name"
    ],
    "Topic": [
	    "Name",
	    "Description"
    ],
    "Volume": [
        "Number",
        "SeriesName"
    ],
    "VolumeCoverCharacter": [
        "VolumeNo",
        "CharacterName"
    ]
}

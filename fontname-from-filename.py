#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# Edits ttf and otf font metadata using the filename.
# Copyright (c) 2018 - 2019 Aman Verma
# Copyright (c) 2017 Chris Simpkins
# See LICENSE file for license details
#
# Dependencies:
#   Python 3.6 or greater
#   fonttools Python library (https://github.com/fonttools/fonttools)
# -----------------------------------------------------------------------------


import os
import sys
from typing import List, Dict

from fontTools import ttLib

# meme workaround
FONT_FAMILY_WORD_COUNT = 1


def main(argv: List[str]) -> None:
    # in case there is no input
    if len(argv) < 1:
        sys.exit(
            "ERROR: You did not include enough arguments to the script.\n"
            "Usage: fontname-from-filename.py <font_file>..."
        )
        sys.exit(1)

    for font_file_path in argv:
        # test if font file exists, maybe should become try/except
        if not _fileExists(font_file_path):
            sys.exit(
                f"ERROR: the path '{font_file_path}' does not appear to be a valid file path."
            )

        font_data = _splitAndGetDataFromFontname(font_file_path)
        the_tt_font = ttLib.TTFont(font_file_path)
        # get a list of namerecords, references to parts of the TTFont object
        font_namerecords = the_tt_font["name"].names
        _renameSingleFont(font_namerecords, font_data)
        # Now try to save the TTFont back into a file:
        try:
            the_tt_font.save(font_file_path)
        except PermissionError:
            sys.exit(
                "ERROR: unable to write new name to OpenType "
                f"tables for '{font_file_path}'.\n"
                "Check the file permissions for the font file "
                "you are trying to rename."
            )
        # there might be other possible exceptions


def _splitAndGetDataFromFontname(font_filename: str) -> Dict[str, str]:
    """Splits and parses font filename

    Takes in a string of the font filename optionally including extension and path.
    Returns a dict of size 4
    """
    simplified_fontname = _getBasenameIfValid(font_filename)
    fontnames = {}
    try:
        split_fontname = simplified_fontname.split(" ")
        # First part is font family and second is the variant
        split_font_family = split_fontname[:FONT_FAMILY_WORD_COUNT]
        fontnames["family"] = " ".join(split_font_family)
        fontnames["nospaces_family"] = fontnames["family"].replace(" ", "")
        split_variant = split_fontname[FONT_FAMILY_WORD_COUNT:]
        fontnames["variant"] = " ".join(split_variant)
        fontnames["nospaces_variant"] = fontnames["variant"].replace(" ", "")
    except IndexError as e:
        sys.exit(
            f"ERROR: {e:!s}\n" "Make sure your font filenames are in the right format."
        )

    return fontnames


def _renameSingleFont(namerecord: list, new_names: Dict[str, str]) -> None:
    """Renames a single font using a list of references to the namerecord

    Loops through namerecords, checking nameID equality. Usually there will be two namerecords
    for each nameID, one in utf-8 and another in some random encoding that I couldn't figure out.
    TODO: figure out what this encoding is and write it.
    This function edits a TTFont object in the scope. Therefore it has nothing to return.
    """
    full_fontname = "{} {}".format(new_names["family"], new_names["variant"])
    postscript_full_fontname = "{}-{}".format(
        new_names["nospaces_family"], new_names["nospaces_variant"]
    )

    for record in namerecord:
        if record.nameID == 1:  # first record is font family name
            record.string = new_names["family"]
        elif record.nameID == 2:  # second record is font variant name
            record.string = new_names["variant"]
        elif record.nameID == 4:  # fourth record is full font name including variant
            record.string = full_fontname
        elif record.nameID == 6:  # sixth record is postscript name (no spaces)
            record.string = postscript_full_fontname


def _getBasenameIfValid(filepath: str) -> str:
    """Turn possible font path into basename and ensure it is a ttf  or otf file."""
    # file_with_ext is a tuple with the pathless basename and the extension.
    file_with_ext = os.path.splitext(os.path.basename(filepath))
    if file_with_ext[1] != ".ttf" and file_with_ext[1] != ".otf":
        sys.exit(f"ERROR: Make sure file '{filepath}' is a ttf or otf font file.")
    return file_with_ext[0]


def _fileExists(filepath: str) -> bool:
    """Tests for existence of a file"""
    return bool(os.path.exists(filepath) and os.path.isfile(filepath))


if __name__ == "__main__":
    main(sys.argv[1:])

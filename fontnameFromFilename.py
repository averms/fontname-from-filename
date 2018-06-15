#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2018 Aman Verma
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# =============================================================================
# Edits ttf and otf font metadata using filename.
# Thanks to Chris Simpkins who wrote the fontname.py script that
# this is based on.
#
# Dependencies:
#   0) Python 3
#   1) fonttools Python library (https://github.com/fonttools/fonttools)
#
# =============================================================================


import os
import sys

from fontTools import ttLib


def _writeNoArgsError():
    sys.stderr.write("ERROR: You did not include enough arguments to the script." + os.linesep)
    sys.stderr.write(
        "Usage: fontnameFromFilename.py [FONT PATH 1] [FONT PATH 2] <FONT PATH ...>" + os.linesep)
    sys.exit(2)


def _makeNameRecords(the_font) -> list:
    """Makes a list of references to names of a ttf font from the font file

    Note that the list is only references, by editing the parts of the list
    you are editing the TTFont object loaded in memory
    """
    namerecord_list = the_font['name'].names
    return namerecord_list


def _fileExists(filepath: str) -> bool:
    """Tests for existence of a file on the string filepath"""
    return bool(os.path.exists(filepath) and os.path.isfile(filepath))  # test that exists and is a file


def _renameSingleFont(namerecord: list, new_names: tuple):
    """Renames a single font using a list of references to the namerecord

    This function edits a TTFont object in the scope. Therefore it has nothing to return.
    """
    full_fontname = '{} {}'.format(new_names[0], new_names[2])
    postscript_full_fontname = '{}-{}'.format(new_names[1], new_names[3])

    for record in namerecord:
        if record.nameID == 1:  # first record is font family name
            record.string = new_names[0]
        elif record.nameID == 2:  # second record is font variant name
            record.string = new_names[2]
        elif record.nameID == 4:  # fourth record is full font name including variant
            record.string = full_fontname
        elif record.nameID == 6:  # sixth record is postscript name (no spaces)
            record.string = postscript_full_fontname


def _splitAndGetDataFromFontname(font_filename: str) -> tuple:
    """Splits and parses font filename

    Takes in a string of the font filename optionally including extension and path.
    Returns a tuple including the font family and font variant including versions with no spaces.
    """
    simplified_fontname = _simplifyFontPath(font_filename)
    try:
        split_fontname = simplified_fontname.split(' ', 1)
        # First part is font family and second is the variant
        font_family = split_fontname[0]
        nospaces_font_family = font_family.replace(' ', '')
        variant = split_fontname[1]
        nospaces_variant = variant.replace(' ', '')
    except IndexError as e:
        sys.stderr.write('ERROR: ' + str(e) + os.linesep)
        sys.stderr.write('Make sure your font filenames are in the right format' + os.linesep)
        sys.exit(1)

    return (font_family, nospaces_font_family, variant, nospaces_variant)


def _simplifyFontPath(font_filepath: str) -> str:
    """Turn possible font path into basename without extension"""
    file_with_ext = os.path.splitext(os.path.basename(font_filepath))
    # We get a tuple with the pathless basename first and the extension second.
    if file_with_ext[1] != '.ttf' and file_with_ext[1] != '.otf':
        sys.stderr.write('ERROR: Make sure file ' +
                         file_with_ext[0] + ' is a ttf or otf font file.' + os.linesep)
        sys.exit(1)
    return file_with_ext[0]


def main(argv: list):
    # in case there is no input
    if len(argv) < 1:
        _writeNoArgsError()
    for font_file_path in argv:
        # test if font file exists, maybe should become try/except
        if not _fileExists(font_file_path):
            sys.stderr.write("ERROR: the path '" + font_file_path +
                             "' does not appear to be a valid file path." + os.linesep)
            sys.exit(1)
        font_data = _splitAndGetDataFromFontname(font_file_path)
        the_tt_font = ttLib.TTFont(font_file_path)
        fontNameRecord = _makeNameRecords(the_tt_font)
        _renameSingleFont(fontNameRecord, font_data)
        # Now try to save the TTFont back into a file:
        try:
            the_tt_font.save(font_file_path)
        except PermissionError:
            sys.stderr.write("ERROR: unable to write new name to OpenType tables for '" +
                             font_file_path + "'." + os.linesep)
            sys.stderr.write(
                '       Check the file permissions for the font file you are trying to rename.' + os.linesep)
            sys.exit(1)
        # if there is another exception it will not be caught, i'm not sure what the possible exceptions are.


if __name__ == '__main__':
    main(sys.argv[1:])

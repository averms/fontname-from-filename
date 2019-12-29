# fontname-from-filename

A quick and dirty script that changes font metadata using the filename.

## Installation

```sh
# fff.py is a bit easier to type but use whatever you want
curl -L https://github.com/a-vrma/fontname-from-filename/raw/master/fontname-from-filename.py -o fff.py
chmod u+x fff.py
```

If one wants to keep the dependencies for this script in a separate virtual environment but still have it executable and in the path, then they can use a shell wrapper script like so:

```sh
#!/bin/sh
exec /path/to/venv/python /path/to/fontname-from-filename.py "$@"
```

## Platforms

Should work on all platforms, but only tested on macOS.

## Example

```
├── Rival Black Italic.otf
├── Rival Black.otf
├── Rival Bold Italic.otf
├── Rival Bold.otf
├── Rival ExtraBold Italic.otf
├── Rival ExtraBold.otf
├── Rival Light Italic.otf
├── Rival Light.otf
├── Rival Medium Italic.otf
├── Rival Medium.otf
├── Rival Regular Italic.otf
├── Rival Regular.otf
├── Rival UltraLight Italic.otf
└── Rival UltraLight.otf
```

Say the metadata of these fonts are messed up for whatever reason, but the
filenames are correct. This script will fix that by changing records 1, 2, 4,
and 6 of the [name table][1].

Works for fonts with more than one word family names if you change the
`FONT_FAMILY_WORD_COUNT` variable in the beginning of the script. For example,
if the font family is called "Source Code Pro" you should change it to 3.

[1]: https://docs.microsoft.com/en-us/typography/opentype/spec/name

## Limitations

Does not change the name of CFF fonts yet.

## Acknowledgements

Thanks to Chris Simpkins for his work on
[fontname.py](https://github.com/chrissimpkins/fontname.py).

This code is distributed under the MIT/Expat License. See LICENSE file for
details.

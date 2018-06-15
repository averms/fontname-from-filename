# fontname-from-filename

A quick and dirty script that changes font metadata using the filename.
Was made to work with [TypeRip](https://github.com/CodeZombie/TypeRip).

## Installation

```
# fff.py is a bit easier to type but use whatever you want
# I personally use a shell wrapper script.
curl -L https://git.io/vhXyO -o fff.py
chmod u+x fff.py
```

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

Say the metadata of these fonts are messed up for whatever reason, but the filenames are
correct. This script will fix that by changing records 1, 2, 4, and 6 of the fonttools xml.
Unfortunately doesn't currently work for fonts with more than one word family names.

## Acknowledgements

Thanks to [Chris Simpkins](https://github.com/chrissimpkins/fontname.py).

This code is licensed under the MIT License. Copyright (c) 2018 Aman Verma

# Manifest Generator
A script to create a manifest from image files. 

# Assumption
It assumes all the image file names follow the same format, namely,
`.*CHAPTER_CNUM_PAGE_PNUM.jpf`

where `CNUM` is replaced with the chapter number and `PNUM` with
the page number.

`CHAPTER` and `PAGE` are cue strings that precedes the numbers, and can be 
set to different values in the config JSON file.

# Install

Clone this repository
```
git clone git@github.com:yale-web-technologies/gen-manifest.git
```

Required modules are specified in `requirements.txt`. You can install them
with

```
pip install -r requirements.txt
```

# Run
Tested only on Mac OS X. The images for the manifest should be present in 
the current directory because the script reads them to extract there
width and height information.
```
FILES_LIST=files.txt
\ls -1 > $FILES_LIST

gen_manifest.sh $FILES_LIST [ $CONFIG_JSON_FILE ]
```

The `FILES_LIST` file contains file names, one per line.

`CONFIG_JSON_FILE` is optional. If present, the parameters set there
will override the default ones defined in config.json in the script directory.

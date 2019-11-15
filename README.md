# CSV to TXT transformer

This is a simple python script that can transform csv files to txt files, which contain all but one fields in the filename, and the data in the last column as content of the file.

It has two basic, and required, command line options, and relies heavily one two conventions with regard to the source files: filename conventions, and data conventions.

## Requirements

Pyhton 3. (Developed against 3.6 but other version should work)

## Command line options

| Command | Description |
| ------- | ---------- |
|`--source`, `-s` | Either a file or folder full of files that will be transformed |
| `--target`, `-t` | The target folder where the new txt files will be placed. Will be created if it does not exist |
| `--help`, `-h` | Display help menu |

## Source filename conventions

The script uses the source filenames to store the new `.txt` files per source in a separate folder, and to give these files names that are retraceable to the csv. To facilitate this, filenames should start with a field indicating the source (e.g. `GR` for GoodReads.com) followed by an underscore (e.g. `GR_`). After that any numbers of fields may exist, separated by underscores (e.g. `GR_whatever_field_and_as_many_as_you_like.csv`). However, the last field should contain some unique identifier to ensure strict separation of files and retraceability.

Some examples of correct filenames:

```txt
GR_myreviews_NL.csv
GR_my_other_reviews_EN.csv
GR_my_other_reviews_EN001.csv
GR_my_other_reviews_EN002.csv
GR_myreviews_ALL.csv
```

If these files were in the `source` folder together you would end up with a directory tree like this:

```txt
target_folder
├── GR_NL
|   └── GR_NL_whatever_metadata_fields_were_found.txt
|   └── GR_NL_whatever_metadata_fields_were_found.txt
├── GR_EN
|   └── GR_EN_whatever_metadata_fields_were_found.txt
├── GR_ALL
    └── GR_ALL_whatever_metadata_fields_were_found.txt
```

Note how the last example is not a language indicator per se, any unique value here would do.

Also, and importantly, the `.txt`s from files called `GR_one_NL.csv`, `GR_two_NL`, and `GR_three_NL` will all end up in the same folder, so try to avoid that.

## Data conventions

The data in the csv should be structured as follows:

1) The first row holds title fields. This row is used by the script simply to count the number of columns but is ignored otherwise. So, if you're csv doesn't contain a title row, insert a line with the correct amount of columns to make sure the script does as promised. (Perhaps simply copy-pasting the top line of the file is a good option?)

2) The very last column contains the data that should be written to the `txt`.
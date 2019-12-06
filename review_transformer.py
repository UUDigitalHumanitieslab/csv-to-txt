import os
import sys
import argparse
import csv


def source(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(
            "Source '{}' does not exist".format(path))
    if not os.path.isdir(path) and not os.path.isfile(path):
        raise argparse.ArgumentTypeError(
            "Source '{}' is not a directory nor a file".format(path))
    return path


def parseArguments(sysArgs):
    parser = argparse.ArgumentParser(
        description='Transform csv to txt with all metadata in the filename')

    parser.add_argument(
        '--source', '-s',
        dest='source', type=source, required=True, help="Either a file or folder full of files that will be transformed")

    parser.add_argument(
        '--target', '-t',
        dest='target', required=True,
        help="The target folder where the new txt files will be placed. Will be created if it does not exist")

    parser.add_argument(
        '--agg_col', '-ac',
        dest='agg_col',
        help='''Optional. The column to aggregate on. Can be either the name of the column as it appears in the top row, or a zero-based index. 
            Rows will be divided into files named after unique values in this column'''
    )

    parser.add_argument(
        '--delimiter', '-d',
        dest='delimiter', default=",",
        help="Optional. The symbol that delimits the fields in the source file. Defaults to ','"
    )

    parsedArgs = parser.parse_args()

    return parsedArgs


def main(sysArgs):
    args = parseArguments(sysArgs)

    if os.path.isfile(args.source):
        process_source(args.source, args.target, args.delimiter, args.agg_col)
    else:
        for file in os.listdir(args.source):
            process_source(os.path.join(args.source, file), args.delimiter, args.target, args.agg_col)


def process_source(filepath, target_folder, delimiter, agg_col):
    file_prefix = get_filename_prefix(filepath)
    target_folder = os.path.join(target_folder, file_prefix)
    if agg_col:
        agg_files = []

    with open(filepath) as csv_file:
        # reader = csv.DictReader(csv_file)
        csv_reader = csv.reader(csv_file, delimiter=delimiter)

        # Process first line
        no_of_columns, agg_col = process_header(next(csv_reader), agg_col)
        if agg_col and agg_col > no_of_columns:
            raise argparse.ArgumentTypeError("agg_col at index {0}' does not exist in '{1}'".format(agg_col, filepath))

        # process other rows
        for row in csv_reader:
            if not agg_col:
                process_row(row, no_of_columns, file_prefix, target_folder)
            else:
                process_row_aggregate(row, no_of_columns, target_folder, agg_col, agg_files)


def process_header(header, agg_col):
    no_of_columns = len(header)

    if agg_col:
        # test if agg_col is integer
        try:
            agg_col = int(agg_col)
            if not agg_col > 0:
                raise argparse.ArgumentTypeError("agg_col '{0}' should be 0 or higher".format(agg_col))
        except ValueError:
            try:
                agg_col = header.index(agg_col)
            except ValueError:
                raise argparse.ArgumentTypeError("agg_col '{0}' is not in the first row".format(agg_col))

    return no_of_columns, agg_col


def get_filename_prefix(source_file):
    fields = os.path.basename(source_file).split('_')
    # last field, without extension, should be language / unique identifier
    language = os.path.splitext(fields[len(fields) - 1])[0]
    return "{0}_{1}".format(fields[0], language)


def process_row(row, no_of_columns, filename_prefix, target_folder):
    filename_fields = []
    text = ''

    # loop through columns
    for i in range(0, no_of_columns):
        if (i < no_of_columns - 1):
            filename_fields.append(row[i])
        else:
            text = row[i]

    filename = '{0}_{1}.txt'.format(filename_prefix, '_'.join(filename_fields))
    export(target_folder, filename, text, 'w')

    filename_fields = []
    text = ''


def process_row_aggregate(row, no_of_columns, target_folder, agg_col, agg_files):
    text = row[no_of_columns - 1]
    agg_col_value = row[agg_col]
    filename = '{0}.txt'.format(agg_col_value)

    if not agg_col_value in agg_files:
        agg_files.append(agg_col_value)
        export(target_folder, filename, text, 'w')
    else:
        export(target_folder, filename, text, 'a')


def get_filename(filename_prefix, filename_fields, agg_col, agg_files):
    if not agg_col:
        return


def export(target_folder, filename, text, file_mode):
    orig_dir = os.getcwd()
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    os.chdir(target_folder)

    with open(filename, file_mode) as exportfile:
        exportfile.write(text)

    os.chdir(orig_dir)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

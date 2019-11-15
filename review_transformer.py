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

    parsedArgs = parser.parse_args()

    return parsedArgs


def main(sysArgs):
    args = parseArguments(sysArgs)

    if os.path.isfile(args.source):
        process_source(args.source, args.target)
    else:
        for file in os.listdir(args.source):
            process_source(os.path.join(args.source, file), args.target)


def process_source(filepath, target_folder):
    file_prefix = get_filename_prefix(filepath)
    target_folder = os.path.join(target_folder, file_prefix)
    
    with open(filepath) as csv_file:
        # reader = csv.DictReader(csv_file)
        csv_reader = csv.reader(csv_file, delimiter=',')
        # Read first line and count columns
        no_of_columns = len(next(csv_reader))

        for row in csv_reader:
            process_row(row, no_of_columns, file_prefix, target_folder)


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
    export(target_folder, filename, text)

    filename_fields = []
    text = ''


def export(target_folder, filename, text):
    orig_dir = os.getcwd()
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    os.chdir(target_folder)

    with open(filename, 'w') as exportfile:
        exportfile.write(text)

    os.chdir(orig_dir)

if __name__ == '__main__':
    sys.exit(main(sys.argv))

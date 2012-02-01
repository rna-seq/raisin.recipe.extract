import os
import ConfigParser

def main(workspace):
    headers = ("species", "version", "url", "file_location")
    template = '\t'.join(['%s'] * len(headers)) + '\n'
    output_file = open(os.path.join(workspace, "annotations.csv"), "w")
    output_file.write(template % headers)

    input_file = open('../../annotations/db.cfg', 'r')
    parser = ConfigParser.RawConfigParser()
    parser.optionxform = lambda s: s
    parser.readfp(input_file)

    for section in parser.sections():
        data = dict(parser.items(section))
        output_file.write(template % tuple([data[h] for h in headers]))

    input_file.close()
    output_file.close()

import os
import ConfigParser
import utils

def main(workspace):
    headers = ("species", 
               "version", 
               "url", 
               "file_location", 
               "file_not_found",
               "file_size")
    template = '\t'.join(['%s'] * len(headers)) + '\n'
    output_file = open(os.path.join(workspace, "annotations.csv"), "w")
    output_file.write(template % headers)

    input_file = open('../../annotations/db.cfg', 'r')
    parser = ConfigParser.RawConfigParser()
    parser.optionxform = lambda s: s
    parser.readfp(input_file)

    for section in parser.sections():
        data = dict(parser.items(section))
        data.update(utils.file_info(data['file_location']))
        output_file.write(template % tuple([data[h] for h in headers]))

    input_file.close()
    output_file.close()

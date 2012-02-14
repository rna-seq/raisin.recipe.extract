import os
import ConfigParser
from raisin.recipe.extract import utils


def main(buildout_directory, workspace):
    headers = ("species",
               "version",
               "url",
               "file_location",
               "file_not_found",
               "file_size")
    template = '\t'.join(['%s'] * len(headers)) + '\n'
    output_file = open(os.path.join(workspace, "annotations.csv"), "w")
    output_file.write(template % headers)

    path = os.path.join(buildout_directory, 'annotations/db.cfg')
    try:
        input_file = open(path, 'r')
    except IOError:
        print "Missing file: %s" % path
        return
    parser = ConfigParser.RawConfigParser()
    parser.optionxform = lambda s: s
    parser.readfp(input_file)

    for section in parser.sections():
        data = dict(parser.items(section))
        data.update(utils.file_info(data['file_location']))
        output_file.write(template % tuple([data[h] for h in headers]))

    input_file.close()
    output_file.close()

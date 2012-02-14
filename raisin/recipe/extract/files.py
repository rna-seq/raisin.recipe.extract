import os
import glob
import ConfigParser
import utils

def extract_files(accessions):
    for accession_id, accession in accessions.items():
        if accession_id == "labeling":
            continue
        file_locations = accession['file_location'].split('\n')
        if len(file_locations) > 1:
            for key, value in accession.items():
                accession[key] = [i.strip() for i in value.split('\n')]
            for i in range(0, len(file_locations)):
                file = {}
                for key, value in accession.items():
                    if len(value) == 1:
                        file[key] = value[0]
                    else:
                        file[key] = value[i]
                yield accession_id, file
        else:
            yield accession_id, accession

def parse_accession_file(file):
    parser = ConfigParser.RawConfigParser()
    parser.optionxform = lambda s: s
    parser.readfp(file)
    accessions = {}
    for section in parser.sections():
        accessions[section] = dict(parser.items(section))
    return accessions

def main(buildout_directory, workspace):
    path = os.path.join(buildout_directory, 'accessions/*/*.cfg')
    input_files = [f for f in glob.glob(path)]

    headers = ["project_id",
               "accession_id",
               "species",
               "cell",
               "readType",
               "qualities",
               "file_location",
               "dataType",
               "rnaExtract",
               "localization",
               "lab",
               "view",
               "type",
               "replicate",
               "file_not_found",
               "file_size",
               "configuration_file"
               ]

    template = '\t'.join(['%s'] * len(headers)) + '\n'
    output_file = open(os.path.join(workspace, "files.csv"), "w")
    output_file.write('\t'.join(headers) + '\n')

    for input_file in input_files:
        accession_file = open(input_file, 'r')
        accessions = parse_accession_file(accession_file)
        if accessions.has_key("labeling"):
            labeling = accessions['labeling']
            for accession_id, accession in accessions.items():
                if not accession_id == 'labeling':
                    accession.update(utils.get_labeling(accession, labeling))
                    
        project_id = os.path.split(os.path.split(input_file)[0])[-1]
        files = extract_files(accessions)
        for accession_id, file in files:
            file_info = utils.file_info(file['file_location'])
            output_file.write(template % (project_id,
                                          accession_id,
                                          file.get('species', ''),
                                          file.get('cell', ''),
                                          file.get('readType', ''),
                                          file.get('qualities', ''),
                                          file.get('file_location', ''),
                                          file.get('dataType', ''),
                                          file.get('rnaExtract', ''),
                                          file.get('localization', ''),
                                          file.get('lab', ''),
                                          file.get('view', ''),
                                          file.get('type', ''),
                                          file.get('replicate', ''),
                                          file_info['file_not_found'],
                                          file_info['file_size'],
                                          input_file
                                          ))
        accession_file.close()

    output_file.close()

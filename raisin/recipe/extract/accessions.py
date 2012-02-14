import os
import glob
import ConfigParser


def extract_accessions(accessions):
    for accession_id, accession in accessions.items():
        if accession_id == "labeling":
            continue
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
               "type",
               "qualities",
               "dataType",
               "rnaExtract",
               "localization",
               "replicate",
               "lab"
               ]

    template = '\t'.join(['%s'] * len(headers)) + '\n'
    output_file = open(os.path.join(workspace, "accessions.csv"), "w")
    output_file.write('\t'.join(headers) + '\n')

    parsed_accessions = {}
    for accession in input_files:
        accession_file = open(accession, 'r')
        parsed_accessions[accession] = parse_accession_file(accession_file)

    for key, value in parsed_accessions.items():
        project_id = os.path.split(os.path.split(key)[0])[-1]

        accessions = extract_accessions(value)

        for accession_id, accession in accessions:
            if not 'species' in accession:
                accession['species'] = ''
            if not 'qualities' in accession:
                accession['qualities'] = ''
            if not 'replicate' in accession:
                accession['replicate'] = ''
            if not 'rnaExtract' in accession:
                accession['rnaExtract'] = ''
            if not 'localization' in accession:
                accession['localization'] = ''
            if not 'cell' in accession:
                accession['cell'] = ''
            if not 'type' in accession:
                accession['type'] = ''
            if not 'dataType' in accession:
                accession['dataType'] = ''
            if not 'lab' in accession:
                accession['lab'] = ''
            if not 'readType' in accession:
                accession['readType'] = ''
            output_file.write(template % (project_id,
                                          accession_id,
                                          accession['species'],
                                          accession['cell'],
                                          accession['readType'],
                                          accession['type'],
                                          accession['qualities'],
                                          accession['dataType'],
                                          accession['rnaExtract'],
                                          accession['localization'],
                                          accession['replicate'],
                                          accession['lab']
                                          ))

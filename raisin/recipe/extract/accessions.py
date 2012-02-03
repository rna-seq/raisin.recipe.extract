import os
import glob
import ConfigParser

def extract_files(accessions):
    for accession_id, accession in accessions.items():
        if accession_id == "labeling":
            continue
        file_locations = accession['file_location'].split('\n')
        if len(file_locations) == 1:
            if accession['type'] in ['fasta', 'fastq']:
                accession['view'] = "RawData"
            elif accession['type'] == 'bam':
                accession['view'] = "Alignments"
        else:
            if accession['type'] == 'fastq':
                accession['view'] = '\n'.join(['FastqRd%d' % number for number in range(1, len(file_locations)+1)])
            elif accession['type'] == 'fasta':
                accession['view'] = '\n'.join(['FastqRd%d' % number for number in range(1, len(file_locations)+1)])
            elif accession['type'] == 'bam':
                accession['view'] = '\n'.join(['Alignment%d' % number for number in range(1, len(file_locations)+1)])
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

def main(workspace):
    input_files = [f for f in glob.glob('../../accessions/*/*.cfg')]

    headers = ["project_id",
               "accession_id",
               "species",
               "cell",
               "mate_id",
               "pair_id",
               "label",
               "readType",
               "type",
               "qualities",
               "file_location",
               "dataType",
               "rnaExtract",
               "localization",
               "replicate",
               "lab",
               "view",
               "type"
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
        
        files = extract_files(value)

        for accession_id, file in files:
            #labeling
            for label in ['mate_id', 'pair_id', 'label']:
                if not label in file:
                    file[label] = 'need to use labeling'

            if not 'species' in file:
                file['species'] = 'species'
            if not 'qualities' in file:
                file['qualities'] = 'qualities'
            if not 'replicate' in file:
                file['replicate'] = 'replicate'
            if not 'rnaExtract' in file:
                file['rnaExtract'] = 'rnaExtract'
            if not 'localization' in file:
                file['localization'] = 'localization'
            if not 'cell' in file:
                file['cell'] = 'cell'
            if not 'readType' in file:
                file['readType'] = 'NA'
                read_length = 'NA'
            elif file['readType'] == '2x76D':
                read_length = 76
            elif file['readType'] == '1x70D':
                read_length = 70
            elif file['readType'] == '2x75':
                read_length = 75
            elif file['readType'] == '1x80':
                read_length = 80
            elif file['readType'] == '1x40':
                read_length = 40
            elif file['readType'] == '1x75D':
                read_length = 75
            elif file['readType'] == '2x100':
                read_length = 100
            elif file['readType'] == '2x96':
                read_length = 96
            elif file['readType'] == '2x53':
                read_length = 53
            elif file['readType'] == '2x76':
                read_length = 76
            elif file['readType'] == '2x46':
                read_length = 46
            elif file['readType'] == '2x35':
                read_length = 35
            elif file['readType'] == '2x34':
                read_length = 34
            elif file['readType'] == '100':
                read_length = 100
            elif file['readType'] == '2x40':
                read_length = 40
            elif file['readType'] == '2x50':
                read_length = 50
            elif file['readType'] == '2x51':
                read_length = 51
            elif file['readType'] == '2x54':
                read_length = 54
            elif file['readType'] == '2x49':
                read_length = 49
            elif file['readType'] in ['2x36', '1x36']:
                read_length = 36
            elif file['readType'] == '2x37':
                read_length = 37
            elif file['readType'] == '50':
                read_length = 50
            elif file['readType'] == '75':
                read_length = 75
            else:
                raise AttributeError
            if not 'type' in file:
                file['type'] = 'type'
            if not 'dataType' in file:
                file['dataType'] = 'dataType'
            if not 'lab' in file:
                file['lab'] = 'lab'
            output_file.write(template % (project_id,
                                          accession_id, 
                                          file['species'], 
                                          file['cell'], 
                                          file['mate_id'], 
                                          file['pair_id'], 
                                          file['label'], 
                                          file['readType'],
                                          file['type'],
                                          file['qualities'],
                                          file['file_location'],
                                          file['dataType'],
                                          file['rnaExtract'],
                                          file['localization'],
                                          file['replicate'],
                                          file['lab'],
                                          file['view'],
                                          file['type']
                                          ))

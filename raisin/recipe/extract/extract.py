import os
import glob
import ConfigParser

ACCESSION_ATTRIBUTES = set(['file_location',
                            'mate_id',
                            'pair_id',
                            'label',
                            'dataType',
                            'cell',
                            'rnaExtract',
                            'localization',
                            'replicate',
                            'lab',
                            'view',
                            'type',
                            'readType',
                            'qualities',
                            'species'])







def main(options, buildout):
    workspace = options['workspace']
    annotations(workspace)
    genomes(workspace)
    accessions(workspace)
    profiles(workspace)

if __name__ == '__main__':
    main()

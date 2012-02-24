import os
import csv


def read_csv(file_name):
    return csv.DictReader(open(file_name, 'rb'),
                               delimiter='\t',
                               skipinitialspace=True)


def add_runs(runs_file, profile, dumps_folder):
    file_name = "%s_experiments.csv" % profile['COMMONDB']
    path = os.path.join(dumps_folder, file_name)
    if not os.path.exists(path):
        return
    experiments = read_csv(path)
    project_id = profile['PROJECTID']
    for experiment in experiments:
        line = [experiment['project_id'],
                experiment['experiment_id'],
                experiment['CellType'],
                experiment['RNAType'],
                experiment['Compartment'],
                experiment['read_length'],
                experiment['partition'],
                experiment['Bioreplicate'],
                experiment['template_file'],
                experiment['mismatches'],
                experiment['paired'],
                experiment['lab'],
                experiment['exp_description'],
                experiment['expDate'],
                experiment.get('Preprocessing', '')]
        # species_id
        # genome_id
        # annotation_id
        runs_file.write('\t'.join(line))
        runs_file.write('\n')



def main(buildout, buildout_directory, workspace, dumps_folder):
    runs_file_name = os.path.join(workspace, 'runs.csv')
    runs_file = open(runs_file_name, 'w')
    headers = ['project_id',
               'run_id',
               'cell',
               'rnaExtract',
               'localization',
               'read_length',
               'partition',
               'replicate',
               'template_file',
               'mismatches',
               'paired',
               'lab',
               'exp_description',
               'expDate',
               'Preprocessing'
                ]
    runs_file.write('\t'.join(headers))
    runs_file.write('\n')
    """    
        {'species_id': '1', 'exp_description': 'None', 'mismatches': '2', 'Compartment': 'CELL', 'annotation_version': 'GENCODEV7', 'RNAType': 'LONGPOLYA', 'template_file': '/users/rg/dgonzalez/Projects/CLL/hg19/CLL_Gv7_CNAG_run76/src/pipeline/template3.0.txt', 'read_length': '76', 'genome_id': '1', 'partition': 'TUMOR', 'md5sum': '4e25d8a8c5f42385f88a9a421f6f43b7', 'expDate': 'None', 'paired': '\x01', 'Preprocessing': 'None', 'CellType': 'BLYMPHOCYTE', 'lab': 'CNAG', 'experiment_id': '001TR76', 'Bioreplicate': '1', 'genome_assembly': 'GRCh37(hg19)', 'project_id': 'Enc7CLL', 'annotation_id': '1'}
    """
    commondbs = []
    profiles_file_name = os.path.join(workspace, 'profiles.csv')
    for profile in read_csv(profiles_file_name):
        if profile["COMMONDB"] in commondbs:
            continue
        else:
            commondbs.append(profile["COMMONDB"])
            add_runs(runs_file, profile, dumps_folder)
    runs_file.close()

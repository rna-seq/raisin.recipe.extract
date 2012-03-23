import os
import ConfigParser


def parse_profile_file(file):
    parser = ConfigParser.RawConfigParser()
    parser.optionxform = lambda s: s
    parser.readfp(file)
    profiles = {}
    for section in parser.sections():
        profiles[section] = dict(parser.items(section))
    return profiles

def extract_replicates(parsed):
    """
    Extract the replicates from the runs
    """
    replicates = []
    for key, value in parsed.items():
        if 'pipeline' in value:
            # Specific pipelines can be defined for each run
            value['profile'] = parsed['pipeline'].copy()
            value['profile'].update(parsed[value['pipeline']])
            value['pipeline_id'] = value['pipeline']
        elif 'accession' in value:
            value['profile'] = parsed['pipeline'].copy()
            value['pipeline_id'] = 'pipeline'
        yield (key, value)

def main(buildout, buildout_directory, workspace):
    profile_files = []
    for path in buildout['pipelines_configurations']['profiles'].split('\n'):
        profile_files.append(os.path.join(buildout_directory, path))
        
    headers = ["project_id",
               "replicate_id",
               "accession_id",
               "pipeline_id",
               "MAPPER",
               "MISMATCHES",
               "PROJECTID",
               "DB",
               "CLUSTER",
               "HOST",
               "THREADS",
               "TEMPLATE",
               "COMMONDB",
               "ANNOTATION",
               "GENOMESEQ",
               "PREPROCESS",
               "PREPROCESS_TRIM_LENGTH"
               ]

    template = '\t'.join(['%s'] * len(headers)) + '\n'
    output_file = open(os.path.join(workspace, "replicates.csv"), "w")
    output_file.write('\t'.join(headers) + '\n')
    
    for profile_file in profile_files:
        file = open(profile_file, 'r')
        parsed = parse_profile_file(file)
        for replicate_id, replicate in extract_replicates(parsed):
            if not replicate.has_key('profile'):
                continue
            profile = replicate['profile']
            output_file.write(template % (
                                  profile['PROJECTID'],
                                  replicate_id,
                                  replicate['accession'],
                                  replicate['pipeline_id'],
                                  profile['MAPPER'],
                                  profile['MISMATCHES'],
                                  profile['PROJECTID'],
                                  profile['DB'],
                                  profile.get('CLUSTER', ''),
                                  profile.get('HOST', ''),
                                  profile['THREADS'],
                                  profile['TEMPLATE'],
                                  profile['COMMONDB'],
                                  profile['ANNOTATION'],
                                  profile['GENOMESEQ'],
                                  profile.get('PREPROCESS', ''),
                                  profile.get('PREPROCESS_TRIM_LENGTH', '')
                                  )
                             )
            
            
import os
import glob
import ConfigParser

def parse_profile_file(file):
    parser = ConfigParser.RawConfigParser()
    parser.optionxform = lambda s: s
    parser.readfp(file)
    profiles = {}
    for section in parser.sections():
        profiles[section] = dict(parser.items(section))
    return profiles
    
def extract_profiles(parsed):
    pipelines = set([])
    for key, value in parsed.items():
        if value.has_key('pipeline'):
            pipelines.add(value['pipeline'])
        elif value.has_key('accession'):
            pipelines.add('pipeline')
    for pipeline in pipelines:
        if pipeline == 'pipeline':
            profile = parsed['pipeline'].copy()
            profile['pipeline_id'] = 'pipeline'
        else:
            profile = parsed['pipeline'].copy()
            profile.update(parsed[pipeline])
            profile['pipeline_id'] = pipeline
        yield profile

def main(workspace):
    profile_files = [f for f in glob.glob('../../profiles/*/*.cfg')]

    headers = ["project_id",
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
    output_file = open(os.path.join(workspace, "profiles.csv"), "w")
    output_file.write('\t'.join(headers) + '\n')

    parsed_profiles = {}
    for profile_file in profile_files:
        print profile_file
        file = open(profile_file, 'r')
        parsed = parse_profile_file(file)
        project_id = os.path.split(os.path.split(profile_file)[0])[-1]
        for profile in extract_profiles(parsed):
            output_file.write(template % (project_id,
                                          profile['pipeline_id'],
                                          profile['MAPPER'],
                                          profile['MISMATCHES'],
                                          profile['PROJECTID'],
                                          profile['DB'],
                                          profile.get('CLUSTER', ''),
                                          profile['HOST'],
                                          profile['THREADS'],
                                          profile['TEMPLATE'],
                                          profile['COMMONDB'],
                                          profile['ANNOTATION'],
                                          profile['GENOMESEQ'],
                                          profile.get('PREPROCESS', ''),
                                          profile.get('PREPROCESS_TRIM_LENGTH', '')
                                          )
                                )


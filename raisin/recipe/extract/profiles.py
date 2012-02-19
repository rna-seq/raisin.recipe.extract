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
        if 'pipeline' in value:
            pipelines.add(value['pipeline'])
        elif 'accession' in value:
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


def main(buildout, buildout_directory, workspace):
    profile_files = []
    for path in buildout['pipelines_configurations']['profiles'].split('\n'):
        profile_files.append(os.path.join(buildout_directory, path))

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

    for profile_file in profile_files:
        file = open(profile_file, 'r')
        parsed = parse_profile_file(file)
        for profile in extract_profiles(parsed):
            output_file.write(template % (
                                  profile['PROJECTID'],
                                  profile['pipeline_id'],
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

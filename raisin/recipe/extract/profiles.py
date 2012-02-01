import os
import glob
import ConfigParser

def parse_profile_file(file):
    parser = ConfigParser.RawConfigParser()
    parser.optionxform = lambda s: s
    parser.readfp(file)
    profile = {}
    if "pipeline" in parser.sections():
        profile = dict(parser.items("pipeline"))
    else:
        print file
        raise AttributeError("The profile is missing a pipeline secion")
    return profile


def main(workspace):
    profile_files = [f for f in glob.glob('../../profiles/*/*.cfg')]

    headers = ["project_id",
               "mapper",
               "mismatches",
               "projectid",
               "db",
               "cluster",
               "host",
               "threads",
               "template",
               "commondb",
               ]

    template = '\t'.join(['%s'] * len(headers)) + '\n'
    output_file = open(os.path.join(workspace, "profiles.csv"), "w")
    output_file.write('\t'.join(headers) + '\n')

    parsed_profiles = {}
    for profile in profile_files:
        profile_file = open(profile, 'r')
        parsed_profiles[profile] = parse_profile_file(profile_file)

    for key, profile in parsed_profiles.items():
        project_id = os.path.split(os.path.split(key)[0])[-1]
        output_file.write(template % (project_id,
                                      profile['MAPPER'],
                                      profile.get('MISMATCHES', ''),
                                      profile['PROJECTID'],
                                      profile['DB'],
                                      profile.get('CLUSTER', ''),
                                      profile['HOST'],
                                      profile['THREADS'],
                                      profile['TEMPLATE'],
                                      profile['COMMONDB']
                                      )
                            )


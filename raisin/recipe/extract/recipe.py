import accessions
import annotations
import files
import genomes
import profiles

class Recipe(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options

    def install(self):
        buildout = self.buildout['buildout']['directory']
        workspace = self.options['workspace']
        accessions.main(buildout, workspace)
        annotations.main(buildout, workspace)
        files.main(buildout, workspace)
        genomes.main(buildout, workspace)
        profiles.main(buildout, workspace)
        
    def update(self):
        return self.install()
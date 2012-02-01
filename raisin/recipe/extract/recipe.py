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
        workspace = self.options['workspace']
        accessions.main(workspace)
        annotations.main(workspace)
        files.main(workspace)
        genomes.main(workspace)
        profiles.main(workspace)
        
    def update(self):
        return self.install()
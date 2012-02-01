import annotations
import genomes
import accessions
import profiles

class Recipe(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options

    def install(self):
        workspace = self.options['workspace']
        annotations.main(workspace)
        genomes.main(workspace)
        accessions.main(workspace)
        profiles.main(workspace)
        
    def update(self):
        return self.install()
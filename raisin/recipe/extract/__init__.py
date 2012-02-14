# -*- coding: utf-8 -*-
"""Recipe raisin.recipe.extract"""

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
        buildout_directory = self.buildout['buildout']['directory']
        workspace = self.options['workspace']
        accessions.main(buildout_directory, workspace)
        annotations.main(buildout_directory, workspace)
        files.main(buildout_directory, workspace)
        genomes.main(buildout_directory, workspace)
        profiles.main(buildout_directory, workspace)

    def update(self):
        return self.install()

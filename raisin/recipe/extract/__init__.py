# -*- coding: utf-8 -*-
"""Recipe raisin.recipe.extract"""

import os

from raisin.recipe.extract import accessions
from raisin.recipe.extract import annotations
from raisin.recipe.extract import files
from raisin.recipe.extract import genomes
from raisin.recipe.extract import profiles


class Recipe(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options

    def install(self):
        buildout_directory = self.buildout['buildout']['directory']
        workspace = self.options['workspace']
        if not os.path.exists(workspace):
            os.makedirs(workspace)
        accessions.main(self.buildout, buildout_directory, workspace)
        annotations_file = self.options['annotations_file']
        annotations.main(buildout_directory, workspace, annotations_file)
        files.main(buildout_directory, workspace)
        genomes.main(buildout_directory, workspace)
        profiles.main(self.buildout, buildout_directory, workspace)

    def update(self):
        return self.install()

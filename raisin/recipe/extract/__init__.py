# -*- coding: utf-8 -*-
"""Recipe raisin.recipe.extract"""

import os

from raisin.recipe.extract import accessions
from raisin.recipe.extract import annotations
from raisin.recipe.extract import files
from raisin.recipe.extract import genomes
from raisin.recipe.extract import profiles
from raisin.recipe.extract import replicates
from raisin.recipe.extract import runs


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
        if not os.path.exists(annotations_file):
            raise AttributeError("annotations_file not found: %s" % annotations_file)
        annotations.main(buildout_directory, workspace, annotations_file)
        files.main(self.buildout, buildout_directory, workspace)
        genomes_file = self.options['genomes_file']
        if not os.path.exists(genomes_file):
            raise AttributeError("genomes_file not found: %s" % genomes_file)
        genomes.main(buildout_directory, workspace, genomes_file)
        profiles.main(self.buildout, buildout_directory, workspace)
        replicates.main(self.buildout, buildout_directory, workspace)
        dumps_folder = self.options['pipeline_dumps']
        if not os.path.exists(dumps_folder):
            raise AttributeError("dumps_folder not found: %s" % dumps_folder)
        runs.main(self.buildout, buildout_directory, workspace, dumps_folder)
        
    def update(self):
        return self.install()

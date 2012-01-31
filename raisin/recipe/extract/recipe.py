import extract

class Recipe(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options

    def install(self):
        return extract.main(self.options, self.buildout)
        
    def update(self):
        return self.install()
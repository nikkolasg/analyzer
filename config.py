class Config(object):
    """Class that handles the parsing of the config file 
    and that store the differents structures,i.e. store all sources
    objects defined, all analysis objects etc """
    file_name = file_name
    sources = dict
    analysis = dict

    @classmethod
    def parse(klass,file_name):
        """Parse the config file. """




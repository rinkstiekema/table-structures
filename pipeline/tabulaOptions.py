import argparse
import os


class Options():
    """This class defines options used during the pipeline
    """

    def __init__(self):
        """Reset the class; indicates the class hasn't been initailized"""
        self.initialized = False

    def initialize(self, parser):
        """Define options"""
        # basic parameters
        parser.add_argument('--dataroot', required=True, help='Path to image folder')       
        parser.add_argument('--mode', default='val', choices=['val', 'test'], help='What data set should it run on?') 
        parser.add_argument('--skip_generate_images', action='store_true', help='Skip: generate images from PDF files')
        parser.add_argument('--skip_create_csv', action='store_true', help='Skip: creating csv from found text')
        self.initialized = True
        return parser

    def gather_options(self):
        """Initialize our parser with basic options(only once).
        Add additional model-specific and dataset-specific options.
        These options are defined in the <modify_commandline_options> function
        in model and dataset classes.
        """
        if not self.initialized:  # check if it has been initialized
            parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            parser = self.initialize(parser)

        # get the basic options
        opt, _ = parser.parse_known_args()
        self.parser = parser
        return parser.parse_args()

    def print_options(self, opt):
        """Print options"""
        message = ''
        message += '----------------- Options ---------------\n'
        for k, v in sorted(vars(opt).items()):
            comment = ''
            default = self.parser.get_default(k)
            if v != default:
                comment = '\t[default: %s]' % str(default)
            message += '{:>25}: {:<30}{}\n'.format(str(k), str(v), comment)
        message += '----------------- End -------------------'
        print(message)

    def parse(self):
        """Parse our options,"""
        opt = self.gather_options()

        self.opt = opt
        return self.opt

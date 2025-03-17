import os
import sys

from arg_parser.arg_parser import ArgParser
from config_loader.config_loader import ConfigLoader

sys.path.append('./')

import arg_parser
import model

if __name__ == '__main__':
    arg_parser = ArgParser()
    args = arg_parser.parse_arg()
    config_loader = ConfigLoader(args.config)
    config = config_loader.load_config()

    model_name = args.openai_name if args.openai_name else config['OpenAIModel']['model']
    openai_api_key = args.openai_api_key if args.openai_api_key else config['OpenAIModel']['api_key']

    model = OpenAIModel(model=model_name, api_key=openai_api_key)



    if args.openai_model
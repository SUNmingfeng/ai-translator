import argparse

class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Argument Parser for translator English to Chinese.')
        self.parser.add_argument('--config', type=str, default='config.json', help='Configuration file')
        self.parser.add_argument('--model', type=str, required=True, choices=['GLMModel', 'OpenAIModel'], help='Model type')
        self.parser.add_argument('--glm_model_url', type=str, help='URL of the glm model')
        self.parser.add_argument('--openai_name', type=str, default='gpt-3.5-turbo', help='name of the openai model')
        self.parser.add_argument('--openai_api_key', type=str, help='openai_api_key')
        self.parser.add_argument('--book', type=str, help='pdf path to translator')
        self.parser.add_argument('--file_format', type=str, help='the format of the file to translator, pdf or markdown')
        self.parser.add_argument('--timeout', type=int, help='timeout in seconds of the API request')

    def parse_arg(self):
        args = self.parser.parse_args()
        if args.model == "OpenAIModel" and not args.openai_api_key and not args.openai_name:
            self.parser.error("--openai_model and --openai_api_key is require when using OpenAIModel")
        return args

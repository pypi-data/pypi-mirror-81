import os
from typing import *

from typing.io import *

from openapi_parser.parser import OpenApiParser
from .client_writer import ClientWriter
from .model_writer import ModelWriter
from .utils_writer import UtilsWriter

class PackageWriter():
    destination_dir: str
    def __init__(self, destination_dir: AnyStr):
        if (isinstance(destination_dir, bytes)):
            destination_dir = destination_dir.decode()
        self.destination_dir = os.path.abspath(destination_dir)
    
    def open_file(self, path: AnyStr) -> TextIO:
        if (isinstance(path, bytes)):
            path = path.decode()
        
        if (not os.path.isabs(path)):
            path = os.path.join(self.destination_dir, path)
        
        dir = os.path.dirname(path)
        if (not os.path.isdir(dir)):
            os.makedirs(dir)
        
        return open(path, 'wt', encoding='utf8')
    
    def write_init(self, parser: OpenApiParser):
        with self.open_file('__init__.py') as output:
            pass
    def write_utils(self, parser: OpenApiParser):
        with self.open_file('utils.py') as output:
            UtilsWriter().write_utils_file(file=output)
    def write_model(self, parser: OpenApiParser):
        with self.open_file('model.py') as output:
            ModelWriter().write_model_file(parser, file=output)
    def write_client(self, parser: OpenApiParser):
        with self.open_file('client.py') as output:
            ClientWriter().write_client_file(parser, file=output)
    
    def write_package(self, parser: OpenApiParser):
        self.write_init(parser)
        self.write_utils(parser)
        self.write_model(parser)
        self.write_client(parser)


__all__ = \
[
    'PackageWriter',
]

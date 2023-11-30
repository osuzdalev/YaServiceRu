import yaml
import os


def add_constructors(yaml_loader):
    yaml_loader.add_constructor("!include", yaml_loader.include)
    return yaml_loader


@add_constructors
class YamlLoader(yaml.SafeLoader):
    """Special class that enables parsing the '!include' tag in the yaml files"""

    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(YamlLoader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, "r") as f:
            return yaml.load(f, YamlLoader)

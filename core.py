# coding: utf-8

class XMLElement:
    def __init__(self, tag: str, attributes: dict = {}, content: str = '') -> None:
        self.children = []
        self.tag = tag
        self.attributes = attributes
        self.content = content

    def add_child(self, child: 'XMLElement') -> None:
        self.children.append(child)

    def remove_child_by_tag(self, tag: str) -> None:
        self.children = [child for child in self.children if child.tag != tag]


class Parser:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def parse(self) -> None:
        self.content = XMLElement('root')
        with open(self.file_path, 'r') as f:
            for line in f:
                self._readline(line)

    def _readline(self, line: str) -> None:
        line.strip()
        for char in line:
            

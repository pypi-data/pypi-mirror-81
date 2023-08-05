"""Flake8 plugin to warn when using short names flags with Maya commands.

:author: Benoit Gielly <benoit.gielly@gmail.com>
:creation: 30/09/2020

"""
__version__ = "1.0.0"


import ast

MSG = "MAF100 using Maya command short name"

VALID_FLAGS = {
    "file": ["add", "i"],
    "removeMultiInstance": ["b"],
    "objectCenter": ["gl"],
    "workspaceControl": ["r"],
}


class Plugin(object):
    """Main flake8 class."""

    name = __name__
    version = __version__

    def __init__(self, tree):
        self._tree = tree

    def run(self):
        """Main."""
        visitor = Visitor()
        visitor.visit(self._tree)
        for line, col in visitor.errors:
            yield line, col, MSG, type(self)


class Visitor(ast.NodeVisitor):
    """Visitor class."""

    def __init__(self):
        self.errors = []

    def visit_Call(self, node):  # pylint: disable=invalid-name
        """Check for Maya short names flags."""
        if self.is_maya_command(node):
            for each in node.keywords:
                is_valid = each.arg not in VALID_FLAGS.get(node.func.attr, [])
                if each.arg and len(each.arg) <= 3 and is_valid:
                    self.errors.append(
                        [each.value.lineno, each.value.col_offset]
                    )
        self.generic_visit(node)

    @staticmethod
    def is_maya_command(node):
        """Check if node is a valid maya command."""
        return (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id in ["cmds", "mc", "pm"]
        )

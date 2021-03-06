# https://manual.macromates.com/en/language_grammars#naming_conventions
import sys

if sys.version_info[0] > 2:
    basestring = str

__all__ = ["COMPILED_NODES", "COMPILED_HEADS"]

DATA = """
    comment
        line
            double-slash
            double-dash
            number-sign
            percentage
        block
            documentation

    constant
        numeric
        character
            escape
        language
        other

    entity
        name
            function
            class
            type
            tag
            section
            constant
        other
            inherited-class
            attribute-name

    invalid
        illegal
        deprecated

    keyword
        control
        operator
        other

    markup
        underline
            link
        bold
        heading
        italic
        list
            numbered
            unnumbered
        quote
        raw
        other

    meta
        key
        value
        function
        function-call
        class
        sequence
        mapping

    punctuation
        definition
            string
                begin
                end
            comment
                begin
                end
        section
            sequence
                begin
                end
            mapping
                begin
                end
        separator
            sequence
            mapping
                key-value
                pair
        accessor
            arrow
            dot
            double-colon
            fat-arrow
            colon
            backslash

    storage
        type
        modifier

    string
        quoted
            single
            double
            triple
            other
        unquoted
        interpolated
        regexp
        other

    support
        function
        class
        type
        constant
        variable
        other

    variable
        parameter
        language
        other
"""


class NodeSet(set):
    """
    Methods:
        * find(name)
        * find_all(name)
        * to_completion()
    """
    def find(self, name):
        for node in self:
            if node == name:
                return node
        return None

    def find_all(self, name):
        res = NodeSet()
        for node in self:
            if node == name:
                res.add(node)
        return res

    def to_completion(self):
        # return zip(self, self)
        return [(n.name, n.name) for n in self]


class ScopeNode(object):
    """
    Attributes:
        * name
        * parent
        * children
        * level | unused
    Methods:
        * add_child(child)
        * tree()
    """

    def __init__(self, name, parent=None, children=None):
        self.name = name
        self.parent = parent
        self.children = children or NodeSet()
        self.level = parent and parent.level + 1 or 1

    def __hash__(self):
        return hash(str(self))

    def add_child(self, child):
        self.children.add(child)

    def tree(self):
        if self.parent:
            return self.name + '.' + self.parent.tree()
        else:
            return self.name

    def __eq__(self, other):
        if isinstance(other, basestring):
            return str(self) == other
        elif isinstance(other, ScopeNode):
            return (self.name == other.name
                    and self.parent == other.parent
                    and self.children == other.children)

    def __str__(self):
        return self.name

    def __repr__(self):
        ret = self.name
        if self.children:
            ret += " {%s}" % ' '.join(map(repr, self.children))
        return ret


#######################################

# output values
COMPILED_NODES = NodeSet()
COMPILED_HEADS = NodeSet()

# parse the DATA string
lines = DATA.split("\n")

# some variables
indent = " " * 4
indent_level = 0
indents = {}

# process lines
# Note: expects sane indentation (such as only indent by 1 `indent` at a time)
for line in lines:
    if line.isspace() or not len(line):
        # skip blank lines
        continue
    if line.startswith(indent * (indent_level + 1)):
        # indent increased
        indent_level += 1
    if not line.startswith(indent * indent_level):
        # indent decreased
        for level in range(indent_level - 1, 0, -1):
            if line.startswith(indent * level):
                indent_level = level
                break

    parent = indents[indent_level - 1] if indent_level - 1 in indents else None
    node = ScopeNode(line.strip(), parent)
    indents[indent_level] = node

    if parent:
        parent.add_child(node)
    else:
        COMPILED_HEADS.add(node)

    COMPILED_NODES.add(node)

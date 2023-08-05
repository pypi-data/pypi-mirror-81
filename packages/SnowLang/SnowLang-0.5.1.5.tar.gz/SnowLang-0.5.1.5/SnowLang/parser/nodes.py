class Node:
    pass


class NumberNode(Node):
    def __init__(self, value, start, end):
        self.value = value
        self.start = start
        self.end = end
        self.type = "Number"

    def __repr__(self):
        return f"{self.value}"


class FuncAssignNode(Node):
    def __init__(self, name, args, body, start, end):
        self.name = name
        self.args = args
        self.body = body
        self.start = start
        self.end = end
        self.type = "FuncAssign"

    def __repr__(self):
        return f"fn {self.name} => {self.body}"


class FuncAccessNode(Node):
    def __init__(self, name, args, start, end):
        self.name = name
        self.args = args
        self.start = start
        self.end = end
        self.type = "FuncAccess"

    def __repr__(self):
        return f"{self.name}({self.args})"


class VarAccessNode(Node):
    def __init__(self, value, start, end):
        self.value = value
        self.start = start
        self.end = end
        self.type = "VarAccess"

    def __repr__(self):
        return f"access({self.value})"


class VarAssignNode(Node):
    def __init__(self, name, value, start, end):
        self.name = name
        self.value = value
        self.start = start
        self.end = end
        self.type = "VarAssign"

    def __repr__(self):
        return f"{self.name} = {self.value}"


class WalrusVarAssignNode(Node):
    def __init__(self, name, value, start, end):
        self.name = name
        self.value = value
        self.start = start
        self.end = end
        self.type = "WalrusVarAssign"

    def __repr__(self):
        return f"{self.name} := {self.value}"


class OutNode(Node):
    def __init__(self, child, start, end):
        self.child = child
        self.start = start
        self.end = end
        self.type = "Out"

    def __repr__(self):
        return f"output {self.child}"


class IfNode(Node):
    def __init__(self, cond, children, else_children, start, end):
        self.cond = cond
        self.children = children
        self.else_children = else_children
        self.start = start
        self.end = end
        self.type = "If"

    def __repr__(self):
        return f"if {self.cond} do {self.children} else do {self.else_children}"


class LoopNode(Node):
    def __init__(self, children, start, end):
        self.children = children
        self.start = start
        self.end = end
        self.type = "Loop"

    def __repr__(self):
        return f"loop {self.children}"


class RepeatNode(Node):
    def __init__(self, times, children, start, end):
        self.times = times
        self.children = children
        self.start = start
        self.end = end
        self.type = "Repeat"

    def __repr__(self):
        return f"repeat {self.times} times {self.children}"


class BreakNode(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.type = "Break"

    def __repr__(self):
        return f"break"


class ReturnNode(Node):
    def __init__(self, child, start, end):
        self.child = child
        self.start = start
        self.end = end
        self.type = "Return"

    def __repr__(self):
        return f"return {self.child}"


class OperationNode(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        self.start = self.left.start
        self.end = self.right.end
        self.type = "Operation"

    def __repr__(self):
        return f"({self.left} {self.op.value} {self.right})"


class UnaryOpNode(Node):
    def __init__(self, op, right):
        self.op = op
        self.right = right
        self.start = self.op.start
        self.end = self.right.end
        self.type = "UnaryOp"

    def __repr__(self):
        return f"({self.op.value}{self.right})"


class ComparisonNode(Node):
    def __init__(self, left, comp, right):
        self.left = left
        self.comp = comp
        self.right = right
        self.start = self.left.start
        self.end = self.right.end
        self.type = "Comparison"

    def __repr__(self):
        return f"({self.left} {self.comp.value} {self.right})"


class CompListNode(Node):
    def __init__(self, children):
        self.children = children
        self.start = self.children[0].start
        self.end = self.children[-1].end
        self.type = "CompList"

    def __repr__(self):
        return f"{' '.join(map(repr, self.children))}"

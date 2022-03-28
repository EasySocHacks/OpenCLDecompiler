from src.base_instruction import BaseInstruction
from src.decompiler_data import make_op, set_reg_value


class VMulLo(BaseInstruction):
    def __init__(self, node, suffix):
        super().__init__(node, suffix)
        self.vdst = self.instruction[1]
        self.src0 = self.instruction[2]
        self.src1 = self.instruction[3]

    def to_print_unresolved(self):
        if self.suffix in {'u16', 'u32'}:
            self.decompiler_data.write(f"{self.vdst} = {self.src0} * {self.src1} // {self.instruction[0]}\n")
            return self.node
        return super().to_print_unresolved()

    def to_fill_node(self):
        if self.suffix in {'u16', 'u32'}:
            reg_entire = self.node.state.registers[self.src0].integrity
            new_value = make_op(self.node, self.src0, self.src1, " * ")
            return set_reg_value(self.node, new_value, self.vdst, [self.src0, self.src1], self.suffix,
                                 reg_entire=reg_entire)
        return super().to_fill_node()

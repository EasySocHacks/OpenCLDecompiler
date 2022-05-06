from src.base_instruction import BaseInstruction
from src.decompiler_data import make_op, set_reg_value
from src.integrity import Integrity
from src.register import is_reg
from src.register_type import RegisterType


class VAddc(BaseInstruction):
    def __init__(self, node, suffix):
        super().__init__(node, suffix)
        self.vdst = self.instruction[1]
        self.sdst = self.instruction[2]
        self.src0 = self.instruction[3]
        self.src1 = self.instruction[4]
        self.ssrc2 = self.instruction[5]

    def to_print_unresolved(self):
        if self.suffix == 'u32':
            temp = "temp" + str(self.decompiler_data.number_of_temp)
            mask = "mask" + str(self.decompiler_data.number_of_mask)
            cc = "cc" + str(self.decompiler_data.number_of_cc)
            self.decompiler_data.write("ulong " + mask + " = (1ULL<<LANEID) // v_addc_u32\n")
            self.decompiler_data.write("uchar " + cc + " = ((" + self.ssrc2 + "&" + mask + " ? 1 : 0)\n")
            self.decompiler_data.write("uint " + temp + " = (ulong)" + self.src0
                                       + " + (ulong)" + self.src1 + " + " + cc + "\n")
            self.decompiler_data.write(self.sdst + " = 0\n")
            self.decompiler_data.write(self.vdst + " = CLAMP ? min(" + temp + ", 0xffffffff) : " + temp + "\n")
            self.decompiler_data.write(self.sdst + " = (" + self.sdst + "&~" + mask + ") | (("
                                       + temp + " >> 32) ? " + mask + " : 0)\n")
            self.decompiler_data.number_of_temp += 1
            self.decompiler_data.number_of_mask += 1
            self.decompiler_data.number_of_cc += 1
            return self.node
        return super().to_print_unresolved()

    def to_fill_node(self):
        if self.suffix == 'u32':
            new_value = make_op(self.node, self.src0, self.src1, " + ", '(ulong)', '(ulong)')
            src0_reg = is_reg(self.src0)
            src1_reg = is_reg(self.src1)
            reg_type = RegisterType.UNKNOWN
            reg_entire = Integrity.ENTIRE
            if src0_reg and src1_reg:
                if self.node.state.registers[self.src1].val == "0":
                    new_value = self.node.state.registers[self.src0].val
                    reg_type = self.node.state.registers[self.src0].type
                    reg_entire = self.node.state.registers[self.src0].integrity
                elif self.node.state.registers[self.src0].val == "0":
                    new_value = self.node.state.registers[self.src1].val
                    reg_type = self.node.state.registers[self.src1].type
                    reg_entire = self.node.state.registers[self.src1].integrity
                else:
                    reg_entire = self.node.state.registers[self.src1].integrity
                    if self.node.state.registers[self.src0].type == RegisterType.ADDRESS_KERNEL_ARGUMENT \
                            and self.node.state.registers[self.src1].type == RegisterType.GLOBAL_ID_X:
                        new_value = self.node.state.registers[self.src0].val + "[get_global_id(0)]"
                        reg_type = RegisterType.ADDRESS_KERNEL_ARGUMENT_ELEMENT
            else:
                reg_type = RegisterType.INT32
                if src0_reg:
                    reg_type = self.node.state.registers[self.src0].type
                if src1_reg:
                    reg_type = self.node.state.registers[self.src1].type
            return set_reg_value(self.node, new_value, self.vdst, [self.src0, self.src1], self.suffix,
                                 reg_type=reg_type, reg_entire=reg_entire)
        return super().to_fill_node()

from src.base_instruction import BaseInstruction
from src.decompiler_data import DecompilerData, make_op
from src.operation_status import OperationStatus
from src.register import Register
from src.register_type import RegisterType


class VXor(BaseInstruction):
    def execute(self, node, instruction, flag_of_status, suffix):
        decompiler_data = DecompilerData()
        output_string = ""
        if suffix == "b32":
            vdst = instruction[1]
            src0 = instruction[2]
            src1 = instruction[3]
            if flag_of_status == OperationStatus.to_print_unresolved:
                decompiler_data.write(vdst + " = " + src0 + " ^ " + src1 + " // v_xor_b32\n")
                return node
            if flag_of_status == OperationStatus.to_fill_node:
                new_integrity = node.state.registers[src1].integrity
                new_val, src0_reg, src1_reg = make_op(node, src0, src1, " ^ ", '', '')
                node.state.registers[vdst] = Register(new_val, RegisterType.unknown, new_integrity)
                decompiler_data.make_version(node.state, vdst)
                if vdst in [src0, src1]:
                    node.state.registers[vdst].make_prev()
                node.state.registers[vdst].type_of_data = suffix
                return node
            return output_string

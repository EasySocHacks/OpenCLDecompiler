from src.base_instruction import BaseInstruction
from src.decompiler_data import DecompilerData
from src.integrity import Integrity
from src.register import Register
from src.type_of_reg import Type
from src.operation_status import OperationStatus


class SCmpLt(BaseInstruction):
    def execute(self, node, instruction, flag_of_status, suffix):
        decompiler_data = DecompilerData()
        output_string = ""
        if suffix == 'i32':
            ssrc0 = instruction[1]
            ssrc1 = instruction[2]
            if flag_of_status == OperationStatus.to_print_unresolved:
                decompiler_data.write("scc = (int)" + ssrc0 + " < (int)" + ssrc1 + " // s_cmp_lt_i32 \n")
                return node
            if flag_of_status == OperationStatus.to_fill_node:
                node.state.registers["scc"] = \
                    Register('(int)' + node.state.registers[ssrc0].val + " < (int)" + node.state.registers[ssrc1].val,
                             Type.unknown, Integrity.integer)
                decompiler_data.make_version(node.state, "scc")
                if "scc" in [ssrc0, ssrc1]:
                    node.state.registers["scc"].make_prev()
                node.state.registers["scc"].type_of_data = suffix
                return node
            return output_string

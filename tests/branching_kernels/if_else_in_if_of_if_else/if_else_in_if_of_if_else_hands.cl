__kernel __attribute__((reqd_work_group_size(4, 4, 4)))
void if_else_in_if_of_if_else(int x, __global int *data, int y)
{
    int var1;
    uint var8;
    var8 = get_global_id(0);
    if ((int)1 == (int)var8) {
        var8 = get_global_id(2);
        data[get_global_id(0)] = (ulong)(get_global_id(1) * x) - (ulong)y;
        if ((int)x < (int)y) {
            var1 = (ulong)((ulong)get_global_offset(2) + (ulong)x) + (ulong)(get_global_id(2) - get_global_offset(2));
        }
        else {
            var1 = (ulong)y + (ulong)get_global_id(1);
        }
    }
    else {
        var1 = get_global_id(0) * y;
    }
    data[var8] = var1;
    data[get_global_id(1)] = x;
}

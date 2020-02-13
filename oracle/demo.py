#!/usr/bin/env python3

from oracle.enums import DBBlockSize, TablespaceType

if __name__ == '__main__':
    tablespace_type = ""
    print("tablespace type is {}".format(tablespace_type if tablespace_type
                                         else TablespaceType.PERMANENT.value))

    parameter_name = "db_{}_cache_size".format(str(DBBlockSize.SixteenK))
    query = "select value from v$parameter where name = '{}';" \
        .format(parameter_name)
    print("query: {}".format(query))

    print(DBBlockSize._member_map_)
    print(DBBlockSize.SixteenK)

    print(str(DBBlockSize.TwoK) == '2k')
    print(DBBlockSize.SixteenK == 16384)
    print(DBBlockSize.TwoK.name, DBBlockSize.TwoK.value)

    params = {'block_size': DBBlockSize.SixteenK}

    print(hasattr(DBBlockSize, str(params['block_size'])))
    print(isinstance(8192, DBBlockSize))
    print(params['block_size'] in DBBlockSize)
    print(DBBlockSize.EightK != 32768)
    print(hasattr(DBBlockSize, params['block_size'].name))

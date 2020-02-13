#!/usr/bin/env python3

from enum import EnumMeta
from pprint import pprint
from oracle.enums import DBBlockSize, TablespaceType


def enum_has_attribute(enum_cls, attribute):
    """Check if enum class has attribute.

    :param enum_cls: enum class
    :type enum_cls: enum.EnumMeta
    :param attribute: attribute name
    :type attribute: str
    :return: True if enum_class has the attribute
    :rtype: bool
    """
    if not isinstance(enum_cls, EnumMeta):
        raise TypeError("enum_cls must be an enum class")
    if not isinstance(attribute, str):
        raise TypeError("attribute must be string")

    pprint(DBBlockSize.__dict__)
    return hasattr(enum_cls, attribute)


def enum_has_member(enum_cls, member):
    """Check if enum class has specified member.

    :param enum_cls: enum class
    :type enum_cls: enum.EnumMeta
    :param member: enum
    :type member: enum
    :return: True if enum_cls has the member
    :rtype: bool
    """
    if not isinstance(enum_cls, EnumMeta):
        raise TypeError("enum_cls must be an enum class")

    pprint(enum_cls._member_map_)

    return member in enum_cls


if __name__ == '__main__':
    tablespace_type = ""
    print("tablespace type is {}".format(tablespace_type if tablespace_type
                                         else TablespaceType.PERMANENT.value))

    parameter_name = "db_{}_cache_size".format(str(DBBlockSize.SixteenK))
    query = "select value from v$parameter where name = '{}';" \
        .format(parameter_name)
    print("query: {}".format(query))

    print(DBBlockSize.SixteenK)

    print(str(DBBlockSize.TwoK) == '2k')
    print(DBBlockSize.SixteenK == 16384)
    print(DBBlockSize.TwoK.name, DBBlockSize.TwoK.value)

    params = {'block_size': DBBlockSize.SixteenK}

    print("Enum {} has attribute {}? {}".format(DBBlockSize,
                                                params['block_size'].name,
                                                enum_has_attribute(
                                                    DBBlockSize,
                                                    params['block_size'].name)))

    print("Enum {} has member {}? {}".format(DBBlockSize,
                                             params['block_size'],
                                             enum_has_member(
                                                 DBBlockSize,
                                                 params['block_size'])))

    print(isinstance(8192, DBBlockSize))
    print(params['block_size'] in DBBlockSize)
    print(DBBlockSize.EightK != 32768)
    print(hasattr(DBBlockSize, params['block_size'].name))

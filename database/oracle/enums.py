from enum import Enum, IntEnum, unique


@unique
class DBBlockSize(IntEnum):
    """Size of Oracle database blocks."""

    TwoK = 2048
    FourK = 4096
    EightK = 8192
    SixteenK = 16384
    ThirtyTwoK = 32768

    def __str__(self):
        """Customize the string representation."""
        return "{}k".format(int(self.value / 1024))


@unique
class LogMode(Enum):
    ARCHIVELOG = 'ARCHIVELOG'
    NOARCHIVELOG = 'NOARCHIVELOG'


@unique
class TablespaceType(Enum):
    PERMANENT = 'PERMANENT'
    TEMPORARY = 'TEMPORARY'
    UNDO = 'UNDO'


@unique
class DatafilesMigrationOption(Enum):
    """Datafiles migration options."""

    ALL = 'all'
    NO = 'no'
    PARTIAL = 'partial'

    @staticmethod
    def parse_str(option):
        """
        Parse specified option as enum.

        :param option: Option to be parsed
        :type option: str
        :return: DatafilesMigrationOption enum
        :rtype: DatafilesMigrationOption
        """
        for _, enum in DatafilesMigrationOption.__members__.items():
            if enum.value == option:
                return enum
        raise Exception("Invalid datafiles migration option: '{}', valid"
                        " options are: {}"
                        .format(option,
                                [e.value for e in DatafilesMigrationOption]))

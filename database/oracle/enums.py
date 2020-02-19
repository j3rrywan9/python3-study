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

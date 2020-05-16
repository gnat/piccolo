from piccolo.table import Table
from piccolo.columns import Varchar, ForeignKey, Integer


###############################################################################
# Simple example


class Manager(Table):
    name = Varchar(length=50)


class Band(Table):
    name = Varchar(length=50)
    manager = ForeignKey(Manager, null=True)
    popularity = Integer(default=0)


###############################################################################
# More complex


class Venue(Table):
    name = Varchar(length=100)
    capacity = Integer(default=0)


class Concert(Table):
    band_1 = ForeignKey(Band)
    band_2 = ForeignKey(Band)
    venue = ForeignKey(Venue)

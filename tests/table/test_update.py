import dataclasses
import datetime
import typing as t
from unittest import TestCase

from piccolo.columns.base import Column
from piccolo.columns.column_types import (
    Date,
    Integer,
    Interval,
    Text,
    Timestamp,
    Timestamptz,
    Varchar,
)
from piccolo.querystring import QueryString
from piccolo.table import Table
from tests.base import DBTestCase, postgres_only
from tests.example_apps.music.tables import Band


class TestUpdate(DBTestCase):
    def check_response(self):
        response = (
            Band.select(Band.name)
            .where(Band.name == "Pythonistas3")
            .run_sync()
        )

        self.assertEqual(response, [{"name": "Pythonistas3"}])

    def test_update(self):
        """
        Make sure updating work, when passing the new values directly to the
        `update` method.
        """
        self.insert_rows()

        Band.update({Band.name: "Pythonistas3"}).where(
            Band.name == "Pythonistas"
        ).run_sync()

        self.check_response()

    def test_update_with_string_keys(self):
        """
        Make sure updating work, when passing a dictionary of values, which
        uses column names as keys, instead of Column instances.
        """
        self.insert_rows()

        Band.update({"name": "Pythonistas3"}).where(
            Band.name == "Pythonistas"
        ).run_sync()

        self.check_response()

    def test_update_with_kwargs(self):
        """
        Make sure updating work, when passing the new value via kwargs.
        """
        self.insert_rows()

        Band.update(name="Pythonistas3").where(
            Band.name == "Pythonistas"
        ).run_sync()

        self.check_response()

    def test_update_values(self):
        """
        Make sure updating work, when passing the new values via the `values`
        method.
        """
        self.insert_rows()

        Band.update().values({Band.name: "Pythonistas3"}).where(
            Band.name == "Pythonistas"
        ).run_sync()

        self.check_response()

    def test_update_values_with_string_keys(self):
        """
        Make sure updating work, when passing the new values via the `values`
        method, using a column name as a dictionary key.
        """
        self.insert_rows()

        Band.update().values({"name": "Pythonistas3"}).where(
            Band.name == "Pythonistas"
        ).run_sync()

        self.check_response()

    def test_update_values_with_kwargs(self):
        """
        Make sure updating work, when passing the new values via kwargs.
        """
        self.insert_rows()

        Band.update().values(name="Pythonistas3").where(
            Band.name == "Pythonistas"
        ).run_sync()

        self.check_response()


###############################################################################
# Test operators


class MyTable(Table):
    integer = Integer()
    timestamp = Timestamp()
    timestamptz = Timestamptz()
    date = Date()
    interval = Interval()
    varchar = Varchar()
    text = Text()


INITIAL_DATETIME = datetime.datetime(
    year=2022, month=1, day=1, hour=21, minute=0
)
INITIAL_INTERVAL = datetime.timedelta(days=1, hours=1, minutes=1)

DATETIME_DELTA = datetime.timedelta(
    days=1, hours=1, minutes=1, seconds=30, microseconds=500
)
DATE_DELTA = datetime.timedelta(days=1)


@dataclasses.dataclass
class OperatorTestCase:
    description: str
    column: Column
    initial: t.Any
    querystring: QueryString
    expected: t.Any


TEST_CASES = [
    # Text
    OperatorTestCase(
        description="Add Text",
        column=MyTable.text,
        initial="Pythonistas",
        querystring=MyTable.text + "!!!",
        expected="Pythonistas!!!",
    ),
    OperatorTestCase(
        description="Add Text columns",
        column=MyTable.text,
        initial="Pythonistas",
        querystring=MyTable.text + MyTable.text,
        expected="PythonistasPythonistas",
    ),
    OperatorTestCase(
        description="Reverse add Text",
        column=MyTable.text,
        initial="Pythonistas",
        querystring="!!!" + MyTable.text,
        expected="!!!Pythonistas",
    ),
    # Varchar
    OperatorTestCase(
        description="Add Varchar",
        column=MyTable.varchar,
        initial="Pythonistas",
        querystring=MyTable.varchar + "!!!",
        expected="Pythonistas!!!",
    ),
    OperatorTestCase(
        description="Add Varchar columns",
        column=MyTable.varchar,
        initial="Pythonistas",
        querystring=MyTable.varchar + MyTable.varchar,
        expected="PythonistasPythonistas",
    ),
    OperatorTestCase(
        description="Reverse add Varchar",
        column=MyTable.varchar,
        initial="Pythonistas",
        querystring="!!!" + MyTable.varchar,
        expected="!!!Pythonistas",
    ),
    # Integer
    OperatorTestCase(
        description="Add Integer",
        column=MyTable.integer,
        initial=1000,
        querystring=MyTable.integer + 10,
        expected=1010,
    ),
    OperatorTestCase(
        description="Reverse add Integer",
        column=MyTable.integer,
        initial=1000,
        querystring=10 + MyTable.integer,
        expected=1010,
    ),
    OperatorTestCase(
        description="Add Integer colums together",
        column=MyTable.integer,
        initial=1000,
        querystring=MyTable.integer + MyTable.integer,
        expected=2000,
    ),
    OperatorTestCase(
        description="Subtract Integer",
        column=MyTable.integer,
        initial=1000,
        querystring=MyTable.integer - 10,
        expected=990,
    ),
    OperatorTestCase(
        description="Reverse subtract Integer",
        column=MyTable.integer,
        initial=1000,
        querystring=2000 - MyTable.integer,
        expected=1000,
    ),
    OperatorTestCase(
        description="Multiply Integer",
        column=MyTable.integer,
        initial=1000,
        querystring=MyTable.integer * 2,
        expected=2000,
    ),
    OperatorTestCase(
        description="Reverse multiply Integer",
        column=MyTable.integer,
        initial=1000,
        querystring=2 * MyTable.integer,
        expected=2000,
    ),
    OperatorTestCase(
        description="Divide Integer",
        column=MyTable.integer,
        initial=1000,
        querystring=MyTable.integer / 10,
        expected=100,
    ),
    OperatorTestCase(
        description="Reverse divide Integer",
        column=MyTable.integer,
        initial=1000,
        querystring=2000 / MyTable.integer,
        expected=2,
    ),
    # Timestamp
    OperatorTestCase(
        description="Add Timestamp",
        column=MyTable.timestamp,
        initial=INITIAL_DATETIME,
        querystring=MyTable.timestamp + DATETIME_DELTA,
        expected=datetime.datetime(
            year=2022,
            month=1,
            day=2,
            hour=22,
            minute=1,
            second=30,
            microsecond=500,
        ),
    ),
    OperatorTestCase(
        description="Reverse add Timestamp",
        column=MyTable.timestamp,
        initial=INITIAL_DATETIME,
        querystring=DATETIME_DELTA + MyTable.timestamp,
        expected=datetime.datetime(
            year=2022,
            month=1,
            day=2,
            hour=22,
            minute=1,
            second=30,
            microsecond=500,
        ),
    ),
    OperatorTestCase(
        description="Subtract Timestamp",
        column=MyTable.timestamp,
        initial=INITIAL_DATETIME,
        querystring=MyTable.timestamp - DATETIME_DELTA,
        expected=datetime.datetime(
            year=2021,
            month=12,
            day=31,
            hour=19,
            minute=58,
            second=29,
            microsecond=999500,
        ),
    ),
    # Timestamptz
    OperatorTestCase(
        description="Add Timestamptz",
        column=MyTable.timestamptz,
        initial=INITIAL_DATETIME,
        querystring=MyTable.timestamptz + DATETIME_DELTA,
        expected=datetime.datetime(
            year=2022,
            month=1,
            day=2,
            hour=22,
            minute=1,
            second=30,
            microsecond=500,
            tzinfo=datetime.timezone.utc,
        ),
    ),
    OperatorTestCase(
        description="Reverse add Timestamptz",
        column=MyTable.timestamptz,
        initial=INITIAL_DATETIME,
        querystring=DATETIME_DELTA + MyTable.timestamptz,
        expected=datetime.datetime(
            year=2022,
            month=1,
            day=2,
            hour=22,
            minute=1,
            second=30,
            microsecond=500,
            tzinfo=datetime.timezone.utc,
        ),
    ),
    OperatorTestCase(
        description="Subtract Timestamptz",
        column=MyTable.timestamptz,
        initial=INITIAL_DATETIME,
        querystring=MyTable.timestamptz - DATETIME_DELTA,
        expected=datetime.datetime(
            year=2021,
            month=12,
            day=31,
            hour=19,
            minute=58,
            second=29,
            microsecond=999500,
            tzinfo=datetime.timezone.utc,
        ),
    ),
    # Date
    OperatorTestCase(
        description="Add Date",
        column=MyTable.date,
        initial=INITIAL_DATETIME,
        querystring=MyTable.date + DATE_DELTA,
        expected=datetime.date(year=2022, month=1, day=2),
    ),
    OperatorTestCase(
        description="Reverse add Date",
        column=MyTable.date,
        initial=INITIAL_DATETIME,
        querystring=DATE_DELTA + MyTable.date,
        expected=datetime.date(year=2022, month=1, day=2),
    ),
    OperatorTestCase(
        description="Subtract Date",
        column=MyTable.date,
        initial=INITIAL_DATETIME,
        querystring=MyTable.date - DATE_DELTA,
        expected=datetime.date(year=2021, month=12, day=31),
    ),
    # Interval
    OperatorTestCase(
        description="Add Interval",
        column=MyTable.interval,
        initial=INITIAL_INTERVAL,
        querystring=MyTable.interval + DATETIME_DELTA,
        expected=datetime.timedelta(days=2, seconds=7350, microseconds=500),
    ),
    OperatorTestCase(
        description="Reverse add Interval",
        column=MyTable.interval,
        initial=INITIAL_INTERVAL,
        querystring=DATETIME_DELTA + MyTable.interval,
        expected=datetime.timedelta(days=2, seconds=7350, microseconds=500),
    ),
    OperatorTestCase(
        description="Subtract Interval",
        column=MyTable.interval,
        initial=INITIAL_INTERVAL,
        querystring=MyTable.interval - DATETIME_DELTA,
        expected=datetime.timedelta(
            days=-1, seconds=86369, microseconds=999500
        ),
    ),
]


# TODO - add SQLite support
@postgres_only
class TestOperators(TestCase):
    def setUp(self):
        MyTable.create_table().run_sync()

    def tearDown(self):
        MyTable.alter().drop_table().run_sync()

    def test_operators(self):
        for test_case in TEST_CASES:
            # Create the initial data in the database.
            concert = MyTable()
            setattr(concert, test_case.column._meta.name, test_case.initial)
            concert.save().run_sync()

            # Apply the update.
            MyTable.update(
                {test_case.column: test_case.querystring}, force=True
            ).run_sync()

            # Make sure the value returned from the database is correct.
            new_value = getattr(
                MyTable.objects().first().run_sync(),
                test_case.column._meta.name,
            )
            self.assertEqual(
                new_value, test_case.expected, msg=test_case.description
            )

            # Clean up
            MyTable.delete(force=True).run_sync()

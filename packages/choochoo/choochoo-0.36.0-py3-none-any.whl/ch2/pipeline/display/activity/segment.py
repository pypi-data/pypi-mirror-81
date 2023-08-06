from logging import getLogger
from re import sub

from ..utils import ActivityJournalDelegate
from ...calculate.segment import SegmentCalculator
from ....names import N
from ....diary.database import summary_column
from ....diary.model import value, text, optional_text
from ....sql.tables import SegmentJournal, Segment, StatisticJournal, StatisticName

log = getLogger(__name__)


def segments_for_activity(s, ajournal):
    return s.query(SegmentJournal). \
        filter(SegmentJournal.activity_journal == ajournal). \
        order_by(SegmentJournal.start).all()


class SegmentDelegate(ActivityJournalDelegate):

    @optional_text('Segments')
    def read_journal_date(self, s, ajournal, date):
        for sjournal in s.query(SegmentJournal).join(Segment). \
                filter(SegmentJournal.activity_journal_id == ajournal.id). \
                order_by(SegmentJournal.start).all():
            stats = [value(sub('^segment ', '', field.statistic_name.name), field.value,
                           units=field.statistic_name.units, measures=field.measures_as_model(date))
                     for field in (self.__field(s, date, sjournal, name)
                                   for name in (N.SEGMENT_TIME, N.SEGMENT_HEART_RATE))
                     if field]
            if stats:
                yield [text(sjournal.segment.title, tag='segment')] + stats

    @staticmethod
    def __field(s, date, sjournal, name):
        return StatisticJournal.at_date(s, date, name, SegmentCalculator, sjournal.activity_group,
                                        source_id=sjournal.id)
    @optional_text('Segments')
    def read_interval(self, s, interval):
        for segment in s.query(Segment).all():
            segment_rows = [list(summary_column(s, interval.schedule, interval.start, name))
                            for name in self.__names(s, N.SEGMENT_TIME, N.SEGMENT_HEART_RATE)]
            segment_rows = list(filter(bool, segment_rows))
            if segment_rows:
                yield [text(segment.title)] + segment_rows

    @staticmethod
    def __names(s, *names):
        for name in names:
            sname = s.query(StatisticName). \
                filter(StatisticName.name == name,
                       StatisticName.owner == SegmentCalculator).one_or_none()
            if sname:
                yield sname

    def read_interval(self, s, interval):
        # todo?
        return
        yield


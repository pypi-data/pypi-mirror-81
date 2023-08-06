
from sqlalchemy import Column, Integer, ForeignKey, Float, Text, UniqueConstraint, or_, DateTime
from sqlalchemy.orm import relationship

from .source import SourceType, Source, GroupedSource
from ..support import Base
from ..triggers import add_child_ddl
from ...common.date import format_time


@add_child_ddl(Source)
class SegmentJournal(GroupedSource):

    __tablename__ = 'segment_journal'

    id = Column(Integer, ForeignKey('source.id', ondelete='cascade'), primary_key=True)
    # do not use on delete cascade here since it leaves source entries without children
    # instead, to guarantee consistency, call clean()
    segment_id = Column(Integer, ForeignKey('segment.id', ondelete='set null'), index=True)
    segment = relationship('Segment')
    # do not use on delete cascade here since it leaves source entries without children
    # instead, to guarantee consistency, call clean()
    activity_journal_id = Column(Integer, ForeignKey('activity_journal.id', ondelete='set null'),
                                 index=True)
    activity_journal = relationship('ActivityJournal', foreign_keys=[activity_journal_id])
    start = Column(DateTime(timezone=True), nullable=False)
    finish = Column(DateTime(timezone=True), nullable=False)
    UniqueConstraint(segment_id, activity_journal_id, start, finish)

    __mapper_args__ = {
        'polymorphic_identity': SourceType.SEGMENT
    }

    def __str__(self):
        return 'Segment Journal %s to %s' % (format_time(self.start), format_time(self.finish))

    def time_range(self, s):
        return self.start, self.finish

    @classmethod
    def clean(cls, s):
        q1 = s.query(SegmentJournal.id). \
                filter(or_(SegmentJournal.segment_id == None,
                           SegmentJournal.activity_journal_id == None)).cte()
        s.query(Source).filter(Source.id.in_(q1)).delete(synchronize_session=False)


class Segment(Base):

    __tablename__ = 'segment'

    id = Column(Integer, primary_key=True)
    # segments used to depend on activity group.  but then they also depended on equipment used,
    # so now they're agnostic about other tables and you need to join and filter as appropriate when extracting
    start_lat = Column(Float, nullable=False)
    start_lon = Column(Float, nullable=False)
    finish_lat = Column(Float, nullable=False)
    finish_lon = Column(Float, nullable=False)
    distance = Column(Float, nullable=False)
    title = Column(Text, nullable=False, index=True, unique=True)
    description = Column(Text)
    UniqueConstraint(start_lat, start_lon, finish_lat, finish_lon)

    @property
    def start(self):
        return self.start_lon, self.start_lat

    @start.setter
    def start(self, lon_lat):
        self.start_lon, self.start_lat = lon_lat

    @property
    def finish(self):
        return self.finish_lon, self.finish_lat

    @finish.setter
    def finish(self, lon_lat):
        self.finish_lon, self.finish_lat = lon_lat

    def coords(self, start):
        if start:
            return self.start
        else:
            return self.finish

    def __str__(self):
        return f'Segment "{self.title}"'

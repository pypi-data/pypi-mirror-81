from itertools import groupby
from logging import getLogger

from math import sqrt, ceil
from pygeotile.point import Point

from .activity import ActivityReader
from ..pipeline import LoaderMixin
from ...common.date import to_time, format_time
from ...lib.utils import sign
from ...names import N
from ...rtree import MatchType
from ...rtree.spherical import LocalTangent, SQRTree, Global
from ...sql.database import Timestamp
from ...sql.tables.segment import Segment, SegmentJournal
from ...sql.utils import add

log = getLogger(__name__)

NAMES = {N.LATITUDE: 'lat',
         N.LONGITUDE: 'lon',
         N.DISTANCE: 'distance'}


class CalcFailed(Exception): pass


class SegmentReader(LoaderMixin, ActivityReader):

    def __init__(self, *args, inner_bound=10, match_bound=25, **kargs):
        self.inner_bound = inner_bound
        self.match_bound = match_bound
        super().__init__(*args, **kargs)

    def _startup(self, s):
        super()._startup(s)
        SegmentJournal.clean(s)
        self.__segments = self._read_segments(s)

    def shutdown(self):
        with self._config.db.session_context() as s:
            SegmentJournal.clean(s)
        super().shutdown()

    def _load_data(self, s, loader, data):
        super()._load_data(s, loader, data)
        ajournal, activity_group, first_timestamp, file_scan, define, records = data
        self._find_segments(s, ajournal, filter_none(NAMES.values(), loader.as_waypoints(NAMES)))

    def _find_segments(self, s, ajournal, waypoints):
        if not waypoints:
            log.warning('No waypoints')
            return
        matches = sorted(self._initial_matches(s, waypoints), key=lambda m: m[2].title)
        if not matches:
            log.info('No segment matches')
            return
        for segment, segment_matches in groupby(matches, key=lambda m: m[2]):
            log.debug(f'Considering {segment.title}')
            ordered = sorted(segment_matches, key=lambda m: m[0])
            coallesced = list(self._coallesce(ordered))
            starts, finishes, segment = self._split(coallesced)
            while starts:
                start = starts.pop(-1)  # work backwards through starts
                copy = list(finishes)
                while copy:
                    finish = copy.pop(0)  # work forwards through finishes
                    if finish[0] > start[0]:
                        if self._try_segment(s, start, finish, waypoints, segment, ajournal):
                            copy = None  # exit search for this start
                            # move to a start that won't overlap (working backwards)
                            while starts and starts[-1][0] > start[0] - 0.5 * (finish[0] - start[0]):
                                starts.pop(-1)
                            if starts:
                                log.debug('Possible second segment')

    def _try_segment(self, s, starts, finishes, waypoints, segment, ajournal):
        try:
            log.info('Trying segment %s-%s for %s' % (starts, finishes, segment.title))
            d = waypoints[self._mid(finishes)].distance - waypoints[self._mid(starts)].distance
            if abs(d - segment.distance) / segment.distance > 0.2:
                raise CalcFailed('Distance between start and finish (%.1fkm) doesn\'t match segment (%.1fkm)' %
                                 (d, segment.distance))
            start_time = self._end_point(starts, waypoints, segment.start, self.inner_bound, True)
            finish_time = self._end_point(finishes, waypoints, segment.finish, self.inner_bound, False)
            sjournal = add(s, SegmentJournal(segment_id=segment.id, activity_journal=ajournal,
                                             start=start_time, finish=finish_time,
                                             activity_group=ajournal.activity_group))
            log.info('Added %s for %s - %s' %
                     (segment.title, format_time(start_time), format_time(finish_time)))
            s.flush()  # needed to get id on sjournal
            # since source is sjournal we cannot use on_success
            Timestamp.set(s, self, constraint=segment, source=sjournal)
            return True
        except CalcFailed as e:
            log.warning(str(e))
            return False

    def _mid(self, indices):
        n = len(indices)
        return indices[n // 2]

    def _end_point(self, indices, waypoints, p, inner, hi_to_lo):
        '''
        Find the time of the point that makes the segment shortest while also being at a local
        minimum in distance from the start/finish point that is within inner m.
        '''
        metric = LocalTangent(p)
        lo, hi = self._limits(metric, waypoints, indices, p)
        log.info('Finding closest point to %s within %d: %f, %d: %f' %
                       (p, lo, self._dw(metric, p, waypoints, lo),
                        hi, self._dw(metric, p, waypoints, hi)))
        if hi_to_lo:
            start, finish = hi, lo
        else:
            start, finish = lo, hi
        minimum = self._minimum(metric, waypoints, start, finish, p, inner)
        # interpolate to fractional index
        i0, i1 = int(minimum), int(minimum) + 1
        k = (minimum - i0) / (i1 - i0)
        t0, t1 = waypoints[i0].time.timestamp(), waypoints[i1].time.timestamp()
        return to_time(float(int(0.5 + t0 * (1 - k) + t1 * k)))  # round to nearest second so easy to query

    def _plot(self, p):
        '''
        Plot points for debugging
        '''
        lon, lat = p
        print('PLOT: %s' % (Point.from_latitude_longitude(lat, lon).meters, ))

    def _plotw(self, metric, waypoints, i, d):
        '''
        Plot points for debugging
        '''
        i1, i2 = int(i), int(i) + 1
        x1, y1 = metric.normalize((waypoints[i1].lon, waypoints[i1].lat))
        x2, y2 = metric.normalize((waypoints[i2].lon, waypoints[i2].lat))
        k = i - i1
        xk = x1 * (1 - k) + x2 * k
        yk = y1 * (1 - k) + y2 * k
        lon, lat = metric.denormalize((xk, yk))
        print('PLOT: %s %.1f' % (Point.from_latitude_longitude(lat, lon).meters, d))

    def _minimum(self, metric, waypoints, start, finish, p, inner):
        '''
        Find the (fractional) index of the point with minimum distance to the endpoint within the two limits.
        '''
        # self._plot(p)
        i = start
        while True:
            i, min_d = self._next_local_minimum(metric, p, waypoints, i, start, finish)
            log.info('Local minimum %.1f: %f (< %.1f?)' % (i, min_d, inner))
            # self._plotw(metric, waypoints, i, min_d)
            if min_d < inner:
                return i
            # move to next segment
            if start < finish:
                i = int(i + 1)
            else:
                i = ceil(i - 1)

    def _next_local_minimum(self, metric, p, waypoints, i, start, finish):
        '''
        Find the next point with a minimum distance to p, along the waypoints (interpolated),
        starting from i and between start and finish (moving towards finish).
        '''
        # this from basic algebra (derivation too long for a comment but pretty simple)
        # p0 is the point we want to minimize distance to
        # pi and pj are the end points of a nearby line segment
        # k is the fractional distance between pi and pj for the point nearest to p0
        # p1 is the point at k if it is between pi and pj
        # things are complicated by the need to return pj if it's the nearest point (discontinuity)
        p0 = metric.normalize(p)
        pi = metric.normalize((waypoints[i].lon, waypoints[i].lat))
        prev_discontinuity = None
        while start <= i < finish or start >= i > finish:
            j = i + sign(finish - start)
            pj = metric.normalize((waypoints[j].lon, waypoints[j].lat))
            dxji, dyji = pj[0] - pi[0], pj[1] - pi[1]
            dx0i, dy0i = p0[0] - pi[0], p0[1] - pi[1]
            k = (dxji * dx0i + dyji * dy0i) / (dxji**2 + dyji**2)
            if 0 < k < 1:  # we have a solution within the segment
                p1 = (pi[0] + k * (pj[0] - pi[0]), pi[1] + k * (pj[1] - pi[1]))
                return i + k * sign(finish - start), sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
            # are we moving towards the target?
            if k > 1:
                # if so, save this endpoint as a possible minimum
                prev_discontinuity = (j, self._dw(metric, p, waypoints, j))
            else:
                # if not, then if we were before it was a minimum
                if prev_discontinuity:
                    return prev_discontinuity
            i, pi = j, pj
        raise CalcFailed('No minimum found')

    def _limits(self, metric, waypoints, indices, p):
        '''
        Given a pair of indices, move them apart so that the distance from the endpoint has increased
        in both directions (ie they bracket the endpoint in some sense).
        '''
        lo, hi = indices
        if lo == hi:
            lo, hi = lo-1, hi+1
        dl, dh = self._dw(metric, p, waypoints, lo), self._dw(metric, p, waypoints, hi)
        if dl < dh:
            lo, dl = self._inc_limit(metric, waypoints, p, dl, dh, lo, -1)
            hi, dh = self._inc_limit(metric, waypoints, p, dh, dl, hi, 1)
        else:
            hi, dh = self._inc_limit(metric, waypoints, p, dh, dl, hi, 1)
            lo, dl = self._inc_limit(metric, waypoints, p, dl, dh, lo, -1)
        log.info('Expanded %s to %s' % (indices, (lo, hi)))
        return lo, hi

    def _inc_limit(self, metric, waypoints, p, da, db, a, inc):
        '''
        Move one index.
        '''
        while da < db and ((inc > 0 and a < len(waypoints) - 1) or (inc < 0 and a > 0)):
            a += inc
            da = self._dw(metric, p, waypoints, a)
        return a, da

    def _dw(self, metric, p, waypoints, i):
        '''
        Distance between an waypoint and the endpoint.
        '''
        return self._d(metric, p, (waypoints[i].lon, waypoints[i].lat))

    def _d(self, metric, p1, p2):
        '''
        The distance between two points using the given metric.
        '''
        x1, y1 = metric.normalize(p1)
        x2, y2 = metric.normalize(p2)
        return sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def _split(self, coallesced):
        '''
        Split waypoints for a single segment into separate start and finish points.
        '''
        starts, finishes, segment = [], [], None
        for i, start, segment in coallesced:
            if start:
                starts.append(i)
            else:
                finishes.append(i)
        return starts, finishes, segment

    def _coallesce(self, ordered_sm):
        '''
        Replace contiguous ranges of waypoints with a pair (min, max)
        '''
        prev, first = None, None
        for match in ordered_sm:
            if match != prev:  # skip duplicates
                if prev and (prev[1:2] != match[1:2] or prev[0]+1 != match[0]):
                    yield (first, prev[0]), prev[1], prev[2]
                    prev, first = None, None
                if first is None:
                    first = match[0]
            prev = match
        yield (first, prev[0]), prev[1], prev[2]

    def _initial_matches(self, s, waypoints):
        '''
        Check each waypoint against the r-tree and return all matches.
        '''
        found = set()
        for i, waypoint in enumerate(waypoints):
            for start, segment in self.__segments[[(waypoint.lon, waypoint.lat)]]:
                if segment not in found:
                    log.info(f'Candidate segment "{segment.title}" at ({segment.start_lon}, {segment.start_lat}) - '
                             f'({segment.finish_lon}, {segment.finish_lat})')
                    found.add(segment)
                log.debug(f'Match at {(waypoint.lon, waypoint.lat)} '
                          f'for {segment.title} {"start" if start else "finish"}')
                yield i, start, segment

    def _read_segments(self, s):
        '''
        Read segment endpoints into a global R-tree so we can detect when waypoints pass nearby.
        '''
        segments = Global(tree=lambda: SQRTree(default_border=self.match_bound, default_match=MatchType.OVERLAP))
        for segment in s.query(Segment).all():
            segments[[segment.start]] = (True, segment)
            segments[[segment.finish]] = (False, segment)
        if not segments:
            log.warning('No segments defined in database')
        return segments


def filter_none(names, waypoints):
    names = list(names)
    return [w for w in waypoints if all(n in w._fields and getattr(w, n) is not None for n in names)]

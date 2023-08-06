
from logging import getLogger
from os.path import exists, join

from matplotlib import use
from matplotlib.pyplot import show, figure

from .args import ACTIVITY, THUMBNAIL_DIR
from ..data.query import Statistics
from ..names import N
from ..pipeline.read.segment import SegmentReader
from ..sql import ActivityJournal

log = getLogger(__name__)


def thumbnail(config):
    '''
## thumbnail

    > ch2 thumbnail ACTIVITY-ID
    > ch2 thumbnail DATE

Generate a thumbnail map of the activity route.
    '''
    with config.db.session_context() as s:
        activity_id = parse_activity(s, config.args[ACTIVITY])
        # display(s, activity_id)
        create_in_cache(config.args._format_path(THUMBNAIL_DIR), s, activity_id)


def parse_activity(s, text):
    try:
        return int(text)
    except ValueError:
        return ActivityJournal.at(s, text).id


def read_activity(s, activity_id, decimate=10):
    try:
        activity_journal = s.query(ActivityJournal).filter(ActivityJournal.id == activity_id).one()
        df = Statistics(s, activity_journal=activity_journal). \
            by_name(SegmentReader, N.SPHERICAL_MERCATOR_X, N.SPHERICAL_MERCATOR_Y).df
        return df.iloc[::decimate, :]
    except:
        raise Exception(f'{activity_id} is not a valid activity ID')


def stats(zs):
    lo, hi = min(zs), max(zs)
    mid = (lo + hi) / 2
    return lo, mid, hi, hi - lo


def normalize(points):
    xs, ys = zip(*points)
    xlo, xmid, xhi, dx = stats(xs)
    ylo, ymid, yhi, dy = stats(ys)
    if dx > dy:
        ylo -= (dx - dy) / 2
    else:
        xlo -= (dy - dx) / 2
    d = max(dx, dy)
    return [(x - xlo) / d - 0.5 for x in xs], [(y - ylo) / d - 0.5 for y in ys], d


def make_figure(xs, ys, side, grid, cm, border):
    fig = figure(frameon=False)
    fig.set_size_inches(cm / 2.54, cm / 2.54)
    ax = fig.add_subplot(1, 1, 1)
    for edge in ('top', 'right', 'bottom', 'left'):
        ax.spines[edge].set_visible(False)
    lim = 0.5 * (1 + border)
    km = 1000 / side
    n = int(lim / (grid * km)) + 1
    ticks = [km * d * grid for d in range(-n, n+1)]
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.tick_params(labelbottom=False, labelleft=False, length=0)
    ax.grid(axis='both', color='#535353')
    ax.set_xlim([-lim, lim])
    ax.set_ylim([-lim, lim])
    ax.set_aspect(aspect='equal', adjustable='box')
    ax.plot(xs, ys, color='white')
    ax.plot([xs[0]], [ys[0]], marker='o', color='green', markersize=cm*3)
    ax.plot([xs[-1]], [ys[-1]], marker='o', color='red', markersize=cm*1.5)
    return fig


def fig_from_df(df, grid=10, cm=1.5, border=0.2):
    points = [(x, y) for _, (x, y) in df.iterrows()]
    if points:
        xs, ys, side = normalize(points)
    else:
        xs, ys, side = [0, 0], [0, 0], 1
    return make_figure(xs, ys, side, grid, cm, border)


def display(s, activity_id):
    df = read_activity(s, activity_id)
    use('PyQt5')
    fig = fig_from_df(df)
    show()


def create_in_cache(dir, s, activity_id):
    path = join(dir, f'{activity_id}.png')
    if not exists(path):
        df = read_activity(s, activity_id)
        use('agg')
        fig = fig_from_df(df)
        fig.savefig(path, transparent=True)
    log.info(f'Thumbnail in {path}')
    return path

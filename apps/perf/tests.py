import test_utils
from nose.tools import eq_

from amo.urlresolvers import reverse
from perf.cron import update_perf
from perf.models import Performance
from addons.models import Addon


class TestPerfIndex(test_utils.TestCase):
    fixtures = ['base/apps', 'base/addon_3615', 'base/addon_5299_gcal',
                'perf/index']

    def setUp(self):
        update_perf()
        self.url = reverse('perf.index')

    def test_get(self):
        # Are you there page?
        r = self.client.get(self.url)
        eq_(r.status_code, 200)
        addons = r.context['addons']
        eq_(len(addons), 2)
        qs = Performance.objects.filter(addon__isnull=False)
        eq_([a.id for a in addons],
            [p.addon_id for p in qs.order_by('-average')])

    def test_empty_perf_table(self):
        Addon.objects.update(ts_slowness=None)
        r = self.client.get(self.url)
        eq_(r.status_code, 404)

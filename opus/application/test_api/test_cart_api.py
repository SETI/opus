# opus/application/test_api/test_cart_api.py

import logging
import requests
from unittest import TestCase

from django.core.cache import cache
from rest_framework.test import RequestsClient

from tools.app_utils import (HTTP404_BAD_OR_MISSING_RANGE,
                             HTTP404_BAD_OR_MISSING_REQNO,
                             HTTP404_BAD_RECYCLEBIN,
                             HTTP404_MISSING_OPUS_ID,
                             HTTP404_SEARCH_PARAMS_INVALID,
                             HTTP404_UNKNOWN_DOWNLOAD_FILE_FORMAT)

from api_test_helper import ApiTestHelper

import settings

class ApiCartTests(TestCase, ApiTestHelper):

    def setUp(self):
        self.maxDiff = None
        settings.OPUS_FAKE_API_DELAYS = 0
        settings.OPUS_FAKE_SERVER_ERROR404_PROBABILITY = 0
        settings.OPUS_FAKE_SERVER_ERROR500_PROBABILITY = 0
        settings.CACHE_KEY_PREFIX = 'opustest:' + settings.DB_SCHEMA_NAME
        logging.disable(logging.ERROR)
        self.cart_maximum = settings.MAX_SELECTIONS_ALLOWED
        if settings.TEST_GO_LIVE: # pragma: no cover
            self.client = requests.Session()
        else:
            self.client = RequestsClient()
        cache.clear()

    def tearDown(self):
        logging.disable(logging.NOTSET)
        settings.MAX_SELECTIONS_ALLOWED = self.cart_maximum


            ##################################################
            ######### /__cart/status.json: API TESTS #########
            ##################################################

    def test__api_cart_status_no_reqno(self):
        "[test_cart_api.py] /__cart/status: no reqno"
        url = '/__cart/status.json'
        self._run_status_equal(url, 404,
                           HTTP404_BAD_OR_MISSING_REQNO('/__cart/status.json'))

    # We don't bother otherwise testing this separately because it's used
    # extensively in all the tests below


            #################################################
            ######### /__cart/reset.json: API TESTS #########
            #################################################

    def test__api_cart_reset_no_reqno(self):
        "[test_cart_api.py] /__cart/reset: no reqno"
        url = '/__cart/reset.json'
        self._run_status_equal(url, 404,
                            HTTP404_BAD_OR_MISSING_REQNO('/__cart/reset.json'))

    def test__api_cart_reset(self):
        "[test_cart_api.py] /__cart/reset"
        url = '/__cart/reset.json?reqno=5'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 5}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=1'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 1}
        self._run_json_equal(url, expected)


            ###############################################
            ######### /__cart/add.json: API TESTS #########
            ###############################################

    def test__api_cart_add_no_reqno(self):
        "[test_cart_api.py] /__cart/add: no reqno"
        url = '/__cart/add.json?opusid=co-iss-n1460961026'
        self._run_status_equal(url, 404,
                               HTTP404_BAD_OR_MISSING_REQNO('/__cart/add.json'))

    def test__api_cart_add_missing(self):
        "[test_cart_api.py] /__cart/add: missing OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?reqno=456'
        self._run_status_equal(url, 404,
                               HTTP404_MISSING_OPUS_ID('/__cart/add.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_empty(self):
        "[test_cart_api.py] /__cart/add: empty OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=&reqno=456'
        self._run_status_equal(url, 404,
                               HTTP404_MISSING_OPUS_ID('/__cart/add.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_one(self):
        "[test_cart_api.py] /__cart/add: good OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460961026&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_one_recyclebin0(self):
        "[test_cart_api.py] /__cart/add: good OPUSID no download recyclebin=0"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460961026&reqno=456&recyclebin=0'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_one_recyclebin1(self):
        "[test_cart_api.py] /__cart/add: good OPUSID no download recyclebin=1"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460961026&reqno=456&recyclebin=1'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_duplicate(self):
        "[test_cart_api.py] /__cart/add: duplicate OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460961026&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460961026&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_duplicate_multi(self):
        "[test_cart_api.py] /__cart/add: duplicate OPUSID no download multi"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460961026,co-iss-n1460961026&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': 'Internal Error: One or more OPUS_IDs not found; nothing added to cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_bad(self):
        "[test_cart_api.py] /__cart/add: bad OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-xn1460961026&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': 'Internal Error: One or more OPUS_IDs not found; nothing added to cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_good_bad(self):
        "[test_cart_api.py] /__cart/add: good+bad OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460961026&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-xn1460961026&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': 'Internal Error: One or more OPUS_IDs not found; nothing added to cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_good_bad_multi(self):
        "[test_cart_api.py] /__cart/add: good+bad OPUSID no download multi"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460961026,co-iss-xn1460961026&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': 'Internal Error: One or more OPUS_IDs not found; nothing added to cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_good_bad_multi_2(self):
        "[test_cart_api.py] /__cart/add: good+bad OPUSID no download multi 2"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460961026,&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': 'Internal Error: One or more OPUS_IDs not found; nothing added to cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_good_bad_multi_3(self):
        "[test_cart_api.py] /__cart/add: good+bad OPUSID no download multi 3"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=,co-iss-n1460961026&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': 'Internal Error: One or more OPUS_IDs not found; nothing added to cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_good_bad_multi_4(self):
        "[test_cart_api.py] /__cart/add: good+bad OPUSID no download multi 4"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=,&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': 'Internal Error: One or more OPUS_IDs not found; nothing added to cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_mixture(self):
        "[test_cart_api.py] /__cart/add: mixture no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=vg-iss-2-s-c4360010&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=WOOHOO&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': 'Internal Error: One or more OPUS_IDs not found; nothing added to cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=vg-iss-2-s-c4360010&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=vg-iss-2-s-c4360010&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=hst-11559-wfc3-ib4v22guq&reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=nh-mvic-mpf_000526016&reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'error': 'Internal Error: One or more OPUS_IDs not found; nothing added to cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_mixture_multi(self):
        "[test_cart_api.py] /__cart/add: mixture no download multi"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=vg-iss-2-s-c4360010&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=WOOHOO&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': 'Internal Error: One or more OPUS_IDs not found; nothing added to cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=vg-iss-2-s-c4360010,hst-11559-wfc3-ib4v22guq&reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=nh-mvic-mpf_000526016&reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'error': 'Internal Error: One or more OPUS_IDs not found; nothing added to cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_missing_download(self):
        "[test_cart_api.py] /__cart/add: missing OPUSID with download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?download=1&reqno=456'
        self._run_status_equal(url, 404,
                               HTTP404_MISSING_OPUS_ID('/__cart/add.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_download_one(self):
        "[test_cart_api.py] /__cart/add: good OPUSID with download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460960653&download=1&reqno=101010101'
        expected = {'total_download_count': 23, 'total_download_size': 24063890, 'total_download_size_pretty': '22M', 'product_cat_list': [['Cassini ISS-Specific Products', [{'slug_name': 'coiss_raw', 'tooltip': 'Raw image files (*.IMG) for Cassini ISS. Images are in VICAR format, uncalibrated, and in units of DN (data number). Associated labels (*.LBL) are text files that contain information about the image. Also included are tlmtab.fmt, which describes the format of the VICAR binary header, and prefix.fmt, which describes the format of the binary prefix at the beginning of each line of imaging data.', 'product_type': 'Raw Image', 'product_count': 1, 'download_count': 4, 'download_size': 1104427, 'download_size_pretty': '1M', 'default_checked': 1}, {'slug_name': 'coiss_calib', 'tooltip': 'Calibrated image files (*_CALIB.IMG) for Cassini ISS. Images are in VICAR format and have been calibrated at the Ring-Moon Systems Node using the CISSCAL pipeline. They are in units of I/F. Associated labels (*.LBL) are text files that contain information about the image and its calibration.', 'product_type': 'Calibrated Image', 'product_count': 1, 'download_count': 2, 'download_size': 4206287, 'download_size_pretty': '4M', 'default_checked': 1}, {'slug_name': 'coiss_thumb', 'tooltip': 'Thumbnail-size (50x50) non-linearly stretched preview JPEGs (*.jpeg_small) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (thumbnail)', 'product_count': 1, 'download_count': 1, 'download_size': 564, 'download_size_pretty': '564B', 'default_checked': 0}, {'slug_name': 'coiss_medium', 'tooltip': 'Medium-size (256x256) non-linearly stretched preview JPEGs (*.jpeg) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (medium)', 'product_count': 1, 'download_count': 1, 'download_size': 2849, 'download_size_pretty': '2K', 'default_checked': 0}, {'slug_name': 'coiss_full', 'tooltip': 'Full-size non-linearly stretched preview PNGs or TIFFs (*.png or *.tiff) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (full)', 'product_count': 1, 'download_count': 1, 'download_size': 259925, 'download_size_pretty': '253K', 'default_checked': 0}]], ['Metadata Products', [{'slug_name': 'rms_index', 'tooltip': 'Text files created by the Ring-Moon Systems Node that summarize or augment some metadata for all observations in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'RMS Node Augmented Index', 'product_count': 1, 'download_count': 2, 'download_size': 10170954, 'download_size_pretty': '9M', 'default_checked': 0}, {'slug_name': 'inventory', 'tooltip': 'Text files ([volume]_inventory.csv) that list every planet and moon inside the instrument field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Target Body Inventory', 'product_count': 1, 'download_count': 2, 'download_size': 385595, 'download_size_pretty': '376K', 'default_checked': 0}, {'slug_name': 'planet_geometry', 'tooltip': 'Text files ([volume]_[planet]_summary.tab) that list the values of various surface geometry metadata for the central planet for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Planet Geometry Index', 'product_count': 1, 'download_count': 2, 'download_size': 1364814, 'download_size_pretty': '1M', 'default_checked': 0}, {'slug_name': 'moon_geometry', 'tooltip': 'Text files ([volume]_moon_summary.tab) that list the values of various surface geometry metadata for every moon in the field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Moon Geometry Index', 'product_count': 1, 'download_count': 2, 'download_size': 4111515, 'download_size_pretty': '3M', 'default_checked': 0}, {'slug_name': 'ring_geometry', 'tooltip': 'Text files ([volume]_ring_summary.tab) that list the values of various ring plane intercept geometry metadata for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Ring Geometry Index', 'product_count': 1, 'download_count': 2, 'download_size': 2229982, 'download_size_pretty': '2M', 'default_checked': 0}]], ['Browse Products', [{'slug_name': 'browse_thumb', 'tooltip': 'Thumbnail-size (often 100x100) non-linearly stretched preview JPEGs (*_thumb.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (thumbnail)', 'product_count': 1, 'download_count': 1, 'download_size': 995, 'download_size_pretty': '995B', 'default_checked': 0}, {'slug_name': 'browse_small', 'tooltip': 'Small-size (often 256x256) non-linearly stretched preview JPEGs (*_small.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (small)', 'product_count': 1, 'download_count': 1, 'download_size': 3012, 'download_size_pretty': '2K', 'default_checked': 0}, {'slug_name': 'browse_medium', 'tooltip': 'Medium-size (often 512x512) non-linearly stretched preview JPEGs (*_med.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (medium)', 'product_count': 1, 'download_count': 1, 'download_size': 7892, 'download_size_pretty': '7K', 'default_checked': 0}, {'slug_name': 'browse_full', 'tooltip': 'Full-size non-linearly stretched preview JPEGs (*_full.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are not colored. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (full)', 'product_count': 1, 'download_count': 1, 'download_size': 215079, 'download_size_pretty': '210K', 'default_checked': 1}]]], 'error': False, 'count': 1, 'recycled_count': 0, 'reqno': 101010101}
        self._run_json_equal(url, expected, ignore='tooltip')
        url = '/__cart/status.json?reqno=0'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 0}
        self._run_json_equal(url, expected)

    def test__api_cart_add_download_two(self):
        "[test_cart_api.py] /__cart/add: two OPUSIDs with download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460960868&download=0&reqno=101010100'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 101010100}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460960653&download=1&reqno=101010101'
        expected = {'total_download_count': 34, 'total_download_size': 30190785, 'total_download_size_pretty': '28M', 'product_cat_list': [['Cassini ISS-Specific Products', [{'slug_name': 'coiss_raw', 'tooltip': 'Raw image files (*.IMG) for Cassini ISS. Images are in VICAR format, uncalibrated, and in units of DN (data number). Associated labels (*.LBL) are text files that contain information about the image. Also included are tlmtab.fmt, which describes the format of the VICAR binary header, and prefix.fmt, which describes the format of the binary prefix at the beginning of each line of imaging data.', 'product_type': 'Raw Image', 'product_count': 2, 'download_count': 6, 'download_size': 2185416, 'download_size_pretty': '2M', 'default_checked': 1}, {'slug_name': 'coiss_calib', 'tooltip': 'Calibrated image files (*_CALIB.IMG) for Cassini ISS. Images are in VICAR format and have been calibrated at the Ring-Moon Systems Node using the CISSCAL pipeline. They are in units of I/F. Associated labels (*.LBL) are text files that contain information about the image and its calibration.', 'product_type': 'Calibrated Image', 'product_count': 2, 'download_count': 4, 'download_size': 8412565, 'download_size_pretty': '8M', 'default_checked': 1}, {'slug_name': 'coiss_thumb', 'tooltip': 'Thumbnail-size (50x50) non-linearly stretched preview JPEGs (*.jpeg_small) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (thumbnail)', 'product_count': 2, 'download_count': 2, 'download_size': 1322, 'download_size_pretty': '1K', 'default_checked': 0}, {'slug_name': 'coiss_medium', 'tooltip': 'Medium-size (256x256) non-linearly stretched preview JPEGs (*.jpeg) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (medium)', 'product_count': 2, 'download_count': 2, 'download_size': 7589, 'download_size_pretty': '7K', 'default_checked': 0}, {'slug_name': 'coiss_full', 'tooltip': 'Full-size non-linearly stretched preview PNGs or TIFFs (*.png or *.tiff) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (full)', 'product_count': 2, 'download_count': 2, 'download_size': 721369, 'download_size_pretty': '704K', 'default_checked': 0}]], ['Metadata Products', [{'slug_name': 'rms_index', 'tooltip': 'Text files created by the Ring-Moon Systems Node that summarize or augment some metadata for all observations in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'RMS Node Augmented Index', 'product_count': 2, 'download_count': 2, 'download_size': 10170954, 'download_size_pretty': '9M', 'default_checked': 0}, {'slug_name': 'inventory', 'tooltip': 'Text files ([volume]_inventory.csv) that list every planet and moon inside the instrument field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Target Body Inventory', 'product_count': 2, 'download_count': 2, 'download_size': 385595, 'download_size_pretty': '376K', 'default_checked': 0}, {'slug_name': 'planet_geometry', 'tooltip': 'Text files ([volume]_[planet]_summary.tab) that list the values of various surface geometry metadata for the central planet for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Planet Geometry Index', 'product_count': 2, 'download_count': 2, 'download_size': 1364814, 'download_size_pretty': '1M', 'default_checked': 0}, {'slug_name': 'moon_geometry', 'tooltip': 'Text files ([volume]_moon_summary.tab) that list the values of various surface geometry metadata for every moon in the field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Moon Geometry Index', 'product_count': 2, 'download_count': 2, 'download_size': 4111515, 'download_size_pretty': '3M', 'default_checked': 0}, {'slug_name': 'ring_geometry', 'tooltip': 'Text files ([volume]_ring_summary.tab) that list the values of various ring plane intercept geometry metadata for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Ring Geometry Index', 'product_count': 2, 'download_count': 2, 'download_size': 2229982, 'download_size_pretty': '2M', 'default_checked': 0}]], ['Browse Products', [{'slug_name': 'browse_thumb', 'tooltip': 'Thumbnail-size (often 100x100) non-linearly stretched preview JPEGs (*_thumb.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (thumbnail)', 'product_count': 2, 'download_count': 2, 'download_size': 3049, 'download_size_pretty': '2K', 'default_checked': 0}, {'slug_name': 'browse_small', 'tooltip': 'Small-size (often 256x256) non-linearly stretched preview JPEGs (*_small.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (small)', 'product_count': 2, 'download_count': 2, 'download_size': 9179, 'download_size_pretty': '8K', 'default_checked': 0}, {'slug_name': 'browse_medium', 'tooltip': 'Medium-size (often 512x512) non-linearly stretched preview JPEGs (*_med.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (medium)', 'product_count': 2, 'download_count': 2, 'download_size': 23639, 'download_size_pretty': '23K', 'default_checked': 0}, {'slug_name': 'browse_full', 'tooltip': 'Full-size non-linearly stretched preview JPEGs (*_full.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are not colored. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (full)', 'product_count': 2, 'download_count': 2, 'download_size': 563797, 'download_size_pretty': '550K', 'default_checked': 1}]]], 'error': False, 'count': 2, 'recycled_count': 0, 'reqno': 101010101}
        self._run_json_equal(url, expected, ignore='tooltip')
        url = '/__cart/status.json?reqno=0'
        expected = {'recycled_count': 0, 'count': 2, 'reqno': 0}
        self._run_json_equal(url, expected)

    def test__api_cart_add_one_too_many_0(self):
        "[test_cart_api.py] /__cart/add: good OPUSID no download too many 1"
        settings.MAX_SELECTIONS_ALLOWED = 0
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460961026&reqno=456'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        else:
            expected = {'recycled_count': 0, 'count': 0, 'error': 'Your request to add OPUS ID co-iss-n1460961026 to the cart failed - there are already too many observations in the cart and recycle bin. The maximum allowed is 0.', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        else:
            expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_one_too_many_1(self):
        "[test_cart_api.py] /__cart/add: good OPUSID no download too many 1"
        settings.MAX_SELECTIONS_ALLOWED = 1
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460961026&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_one_too_many_2_multi(self):
        "[test_cart_api.py] /__cart/add: good OPUSID no download too many 2 multi"
        settings.MAX_SELECTIONS_ALLOWED = 2
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460961026,hst-11559-wfc3-ib4v22guq&reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_one_too_many_1_multi(self):
        "[test_cart_api.py] /__cart/add: good OPUSID no download too many 1 multi"
        settings.MAX_SELECTIONS_ALLOWED = 1
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460961026,hst-11559-wfc3-ib4v22guq&reqno=456'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 456}
        else:
            expected = {'recycled_count': 0, 'count': 0, 'error': 'Your request to add multiple OPUS IDs to the cart failed - there are already too many observations in the cart and recycle bin. The maximum allowed is 1.', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_duplicate_too_many_1(self):
        "[test_cart_api.py] /__cart/add: duplicate OPUSID no download too many 1"
        settings.MAX_SELECTIONS_ALLOWED = 1
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460961026&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460961026&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=hst-11559-wfc3-ib4v22guq&reqno=456'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 456}
        else:
            expected = {'recycled_count': 0, 'count': 1, 'error': 'Your request to add OPUS ID hst-11559-wfc3-ib4v22guq to the cart failed - there are already too many observations in the cart and recycle bin. The maximum allowed is 1.', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_mixture_too_many_2(self):
        "[test_cart_api.py] /__cart/add: mixture no download too many 2"
        settings.MAX_SELECTIONS_ALLOWED = 2
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=vg-iss-2-s-c4360010&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=vg-iss-2-s-c4360010&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=vg-iss-2-s-c4360010&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=hst-11559-wfc3-ib4v22guq&reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=vg-iss-2-s-c4360018&reqno=456'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 0, 'count': 3, 'error': False, 'reqno': 456}
        else:
            expected = {'recycled_count': 0, 'count': 2, 'error': 'Your request to add OPUS ID vg-iss-2-s-c4360018 to the cart failed - there are already too many observations in the cart and recycle bin. The maximum allowed is 2.', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 0, 'count': 3, 'reqno': 456}
        else:
            expected = {'recycled_count': 0, 'count': 2, 'reqno': 456}
        self._run_json_equal(url, expected)


            ##################################################
            ######### /__cart/remove.json: API TESTS #########
            ##################################################

    def test__api_cart_remove_no_reqno(self):
        "[test_cart_api.py] /__cart/remove: no reqno"
        url = '/__cart/remove.json?opusid=co-iss-n1460961026'
        self._run_status_equal(url, 404,
                           HTTP404_BAD_OR_MISSING_REQNO('/__cart/remove.json'))

    def test__api_cart_remove_missing(self):
        "[test_cart_api.py] /__cart/remove: missing OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?reqno=456'
        self._run_status_equal(url, 404,
                               HTTP404_MISSING_OPUS_ID('/__cart/remove.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_empty(self):
        "[test_cart_api.py] /__cart/remove: empty OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=&reqno=456'
        self._run_status_equal(url, 404,
                               HTTP404_MISSING_OPUS_ID('/__cart/remove.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_one(self):
        "[test_cart_api.py] /__cart/remove: add+remove good OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_one_recyclebin0(self):
        "[test_cart_api.py] /__cart/remove: add+remove good OPUSID no download recyclebin=0"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1484504505_ir&reqno=456&recyclebin=0'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_one_recyclebin1(self):
        "[test_cart_api.py] /__cart/remove: add+remove good OPUSID no download recyclebin=1"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1484504505_ir&reqno=456&recyclebin=1'
        expected = {'recycled_count': 1, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 1, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_one_recyclebinx(self):
        "[test_cart_api.py] /__cart/remove: recyclebin=x"
        url = '/__cart/remove.json?opusid=co-vims-v1484504505_ir&reqno=456&recyclebin=x'
        self._run_status_equal(url, 404,
                HTTP404_BAD_RECYCLEBIN('x', '/__cart/remove.json'))

    def test__api_cart_remove_duplicate(self):
        "[test_cart_api.py] /__cart/remove: duplicate OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_duplicate_recyclebin1(self):
        "[test_cart_api.py] /__cart/remove: duplicate OPUSID no download recyclebin=1"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1484528864_ir&reqno=456&recyclebin=1'
        expected = {'recycled_count': 1, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1484528864_ir&reqno=456&recyclebin=0'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_duplicate_multi(self):
        "[test_cart_api.py] /__cart/remove: duplicate OPUSID no download multi"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1484528864_ir,co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_bad(self):
        "[test_cart_api.py] /__cart/remove: bad OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        # Removing an unknown opusid doesn't throw an error
        url = '/__cart/remove.json?opusid=co-vims-v1484528864_irx&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_bad_recyclebin1(self):
        "[test_cart_api.py] /__cart/remove: bad OPUSID no download recyclebin=1"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        # Removing an unknown opusid throws an error with recyclebin
        url = '/__cart/remove.json?opusid=co-vims-v1484528864_irx&reqno=456&recyclebin=1'
        expected = {'recycled_count': 0, 'count': 0, 'error': 'Internal Error: One or more OPUS_IDs not found; nothing removed from cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_good_bad(self):
        "[test_cart_api.py] /__cart/remove: good+bad OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-iss-xn1460961026&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_good_bad_multi(self):
        "[test_cart_api.py] /__cart/remove: good+bad OPUSID no download multi"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1484528864_ir,co-iss-xn1460961026&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_mixture(self):
        "[test_cart_api.py] /__cart/remove: mixture no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=vg-iss-2-s-c4360010&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=go-ssi-c0347174400&reqno=456'
        expected = {'recycled_count': 0, 'count': 3, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=WOOHOO&reqno=456'
        expected = {'recycled_count': 0, 'count': 3, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=vg-iss-2-s-c4360010&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=nh-mvic-mpf_000526016x&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_mixture_recyclebin1(self):
        "[test_cart_api.py] /__cart/remove: mixture no download recyclebin=1"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=vg-iss-2-s-c4360010,co-vims-v1484528864_ir,go-ssi-c0347174400&reqno=456'
        expected = {'recycled_count': 0, 'count': 3, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 3, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1484528864_ir&reqno=456&recyclebin=1'
        expected = {'recycled_count': 1, 'count': 2, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=vg-iss-2-s-c4360010&reqno=456&recyclebin=1'
        expected = {'recycled_count': 2, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=nh-mvic-mpf_000526016x&reqno=456'
        expected = {'recycled_count': 2, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=vg-iss-2-s-c4360010&reqno=456'
        expected = {'recycled_count': 1, 'count': 2, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=go-ssi-c0347174400&reqno=456'
        expected = {'recycled_count': 1, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 1, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_mixture_multi(self):
        "[test_cart_api.py] /__cart/remove: mixture no download multi"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=vg-iss-2-s-c4360010&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=go-ssi-c0347174400&reqno=456'
        expected = {'recycled_count': 0, 'count': 3, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=WOOHOO,co-vims-v1484528864_ir,vg-iss-2-s-c4360010&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=nh-mvic-mpf_000526016x&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1484528864_ir,go-ssi-c0347174400&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_add_bad(self):
        "[test_cart_api.py] /__cart/remove: add+remove bad OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-xn1460961026&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': 'Internal Error: One or more OPUS_IDs not found; nothing added to cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        # Removing an unknown opusid doesn't throw an error
        url = '/__cart/remove.json?opusid=co-iss-xn1460961026&reqno=101010101'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 101010101}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=0'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 0}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_missing_download(self):
        "[test_cart_api.py] /__cart/remove: missing OPUSID with download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?download=1&reqno=456'
        self._run_status_equal(url, 404,
                               HTTP404_MISSING_OPUS_ID('/__cart/remove.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_one_download(self):
        "[test_cart_api.py] /__cart/remove: good OPUSID with download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460961026&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-iss-n1460961026&reqno=123456&download=1'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 123456, "total_download_count": 0, "total_download_size": 0, "total_download_size_pretty": "0B", "product_cat_list": []}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=789'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 789}
        self._run_json_equal(url, expected)

    def test__api_cart_remove_one_download_recyclebin1(self):
        "[test_cart_api.py] /__cart/remove: good OPUSID with download recyclebin=1"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460961026&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-iss-n1460961026&reqno=123456&download=1&recyclebin=1'
        expected = {'total_download_count': 0, 'total_download_size': 0, 'total_download_size_pretty': '0B', 'product_cat_list': [['Cassini ISS-Specific Products', [{'slug_name': 'coiss_raw', 'tooltip': 'Raw image files (*.IMG) for Cassini ISS. Images are in VICAR format, uncalibrated, and in units of DN (data number). Associated labels (*.LBL) are text files that contain information about the image. Also included are tlmtab.fmt, which describes the format of the VICAR binary header, and prefix.fmt, which describes the format of the binary prefix at the beginning of each line of imaging data.', 'product_type': 'Raw Image', 'product_count': 0, 'download_count': 0, 'download_size': 0, 'download_size_pretty': 0, 'default_checked': 1}, {'slug_name': 'coiss_calib', 'tooltip': 'Calibrated image files (*_CALIB.IMG) for Cassini ISS. Images are in VICAR format and have been calibrated at the Ring-Moon Systems Node using the CISSCAL pipeline. They are in units of I/F. Associated labels (*.LBL) are text files that contain information about the image and its calibration.', 'product_type': 'Calibrated Image', 'product_count': 0, 'download_count': 0, 'download_size': 0, 'download_size_pretty': 0, 'default_checked': 1}, {'slug_name': 'coiss_thumb', 'tooltip': 'Thumbnail-size (50x50) non-linearly stretched preview JPEGs (*.jpeg_small) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (thumbnail)', 'product_count': 0, 'download_count': 0, 'download_size': 0, 'download_size_pretty': 0, 'default_checked': 0}, {'slug_name': 'coiss_medium', 'tooltip': 'Medium-size (256x256) non-linearly stretched preview JPEGs (*.jpeg) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (medium)', 'product_count': 0, 'download_count': 0, 'download_size': 0, 'download_size_pretty': 0, 'default_checked': 0}, {'slug_name': 'coiss_full', 'tooltip': 'Full-size non-linearly stretched preview PNGs or TIFFs (*.png or *.tiff) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (full)', 'product_count': 0, 'download_count': 0, 'download_size': 0, 'download_size_pretty': 0, 'default_checked': 0}]], ['Metadata Products', [{'slug_name': 'rms_index', 'tooltip': 'Text files created by the Ring-Moon Systems Node that summarize or augment some metadata for all observations in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'RMS Node Augmented Index', 'product_count': 0, 'download_count': 0, 'download_size': 0, 'download_size_pretty': 0, 'default_checked': 0}, {'slug_name': 'inventory', 'tooltip': 'Text files ([volume]_inventory.csv) that list every planet and moon inside the instrument field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Target Body Inventory', 'product_count': 0, 'download_count': 0, 'download_size': 0, 'download_size_pretty': 0, 'default_checked': 0}, {'slug_name': 'planet_geometry', 'tooltip': 'Text files ([volume]_[planet]_summary.tab) that list the values of various surface geometry metadata for the central planet for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Planet Geometry Index', 'product_count': 0, 'download_count': 0, 'download_size': 0, 'download_size_pretty': 0, 'default_checked': 0}, {'slug_name': 'moon_geometry', 'tooltip': 'Text files ([volume]_moon_summary.tab) that list the values of various surface geometry metadata for every moon in the field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Moon Geometry Index', 'product_count': 0, 'download_count': 0, 'download_size': 0, 'download_size_pretty': 0, 'default_checked': 0}, {'slug_name': 'ring_geometry', 'tooltip': 'Text files ([volume]_ring_summary.tab) that list the values of various ring plane intercept geometry metadata for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Ring Geometry Index', 'product_count': 0, 'download_count': 0, 'download_size': 0, 'download_size_pretty': 0, 'default_checked': 0}]], ['Browse Products', [{'slug_name': 'browse_thumb', 'tooltip': 'Thumbnail-size (often 100x100) non-linearly stretched preview JPEGs (*_thumb.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (thumbnail)', 'product_count': 0, 'download_count': 0, 'download_size': 0, 'download_size_pretty': 0, 'default_checked': 0}, {'slug_name': 'browse_small', 'tooltip': 'Small-size (often 256x256) non-linearly stretched preview JPEGs (*_small.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (small)', 'product_count': 0, 'download_count': 0, 'download_size': 0, 'download_size_pretty': 0, 'default_checked': 0}, {'slug_name': 'browse_medium', 'tooltip': 'Medium-size (often 512x512) non-linearly stretched preview JPEGs (*_med.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (medium)', 'product_count': 0, 'download_count': 0, 'download_size': 0, 'download_size_pretty': 0, 'default_checked': 0}, {'slug_name': 'browse_full', 'tooltip': 'Full-size non-linearly stretched preview JPEGs (*_full.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are not colored. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (full)', 'product_count': 0, 'download_count': 0, 'download_size': 0, 'download_size_pretty': 0, 'default_checked': 1}]]], 'error': False, 'count': 0, 'recycled_count': 1, 'reqno': 123456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=789'
        expected = {'recycled_count': 1, 'count': 0, 'reqno': 789}
        self._run_json_equal(url, expected)

    def test__api_cart_add_two_remove_one_download(self):
        "[test_cart_api.py] /__cart/remove: two OPUSIDs remove one with download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460960868&download=0&reqno=101010100'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 101010100}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460960653&download=&reqno=101010101'
        expected = {'error': False, 'recycled_count': 0, 'count': 2, 'reqno': 101010101}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-iss-n1460960868&download=1&reqno=101010102'
        expected = {'total_download_count': 23, 'total_download_size': 24063890, 'total_download_size_pretty': '22M', 'product_cat_list': [['Cassini ISS-Specific Products', [{'slug_name': 'coiss_raw', 'tooltip': 'Raw image files (*.IMG) for Cassini ISS. Images are in VICAR format, uncalibrated, and in units of DN (data number). Associated labels (*.LBL) are text files that contain information about the image. Also included are tlmtab.fmt, which describes the format of the VICAR binary header, and prefix.fmt, which describes the format of the binary prefix at the beginning of each line of imaging data.', 'product_type': 'Raw Image', 'product_count': 1, 'download_count': 4, 'download_size': 1104427, 'download_size_pretty': '1M', 'default_checked': 1}, {'slug_name': 'coiss_calib', 'tooltip': 'Calibrated image files (*_CALIB.IMG) for Cassini ISS. Images are in VICAR format and have been calibrated at the Ring-Moon Systems Node using the CISSCAL pipeline. They are in units of I/F. Associated labels (*.LBL) are text files that contain information about the image and its calibration.', 'product_type': 'Calibrated Image', 'product_count': 1, 'download_count': 2, 'download_size': 4206287, 'download_size_pretty': '4M', 'default_checked': 1}, {'slug_name': 'coiss_thumb', 'tooltip': 'Thumbnail-size (50x50) non-linearly stretched preview JPEGs (*.jpeg_small) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (thumbnail)', 'product_count': 1, 'download_count': 1, 'download_size': 564, 'download_size_pretty': '564B', 'default_checked': 0}, {'slug_name': 'coiss_medium', 'tooltip': 'Medium-size (256x256) non-linearly stretched preview JPEGs (*.jpeg) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (medium)', 'product_count': 1, 'download_count': 1, 'download_size': 2849, 'download_size_pretty': '2K', 'default_checked': 0}, {'slug_name': 'coiss_full', 'tooltip': 'Full-size non-linearly stretched preview PNGs or TIFFs (*.png or *.tiff) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (full)', 'product_count': 1, 'download_count': 1, 'download_size': 259925, 'download_size_pretty': '253K', 'default_checked': 0}]], ['Metadata Products', [{'slug_name': 'rms_index', 'tooltip': 'Text files created by the Ring-Moon Systems Node that summarize or augment some metadata for all observations in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'RMS Node Augmented Index', 'product_count': 1, 'download_count': 2, 'download_size': 10170954, 'download_size_pretty': '9M', 'default_checked': 0}, {'slug_name': 'inventory', 'tooltip': 'Text files ([volume]_inventory.csv) that list every planet and moon inside the instrument field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Target Body Inventory', 'product_count': 1, 'download_count': 2, 'download_size': 385595, 'download_size_pretty': '376K', 'default_checked': 0}, {'slug_name': 'planet_geometry', 'tooltip': 'Text files ([volume]_[planet]_summary.tab) that list the values of various surface geometry metadata for the central planet for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Planet Geometry Index', 'product_count': 1, 'download_count': 2, 'download_size': 1364814, 'download_size_pretty': '1M', 'default_checked': 0}, {'slug_name': 'moon_geometry', 'tooltip': 'Text files ([volume]_moon_summary.tab) that list the values of various surface geometry metadata for every moon in the field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Moon Geometry Index', 'product_count': 1, 'download_count': 2, 'download_size': 4111515, 'download_size_pretty': '3M', 'default_checked': 0}, {'slug_name': 'ring_geometry', 'tooltip': 'Text files ([volume]_ring_summary.tab) that list the values of various ring plane intercept geometry metadata for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Ring Geometry Index', 'product_count': 1, 'download_count': 2, 'download_size': 2229982, 'download_size_pretty': '2M', 'default_checked': 0}]], ['Browse Products', [{'slug_name': 'browse_thumb', 'tooltip': 'Thumbnail-size (often 100x100) non-linearly stretched preview JPEGs (*_thumb.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (thumbnail)', 'product_count': 1, 'download_count': 1, 'download_size': 995, 'download_size_pretty': '995B', 'default_checked': 0}, {'slug_name': 'browse_small', 'tooltip': 'Small-size (often 256x256) non-linearly stretched preview JPEGs (*_small.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (small)', 'product_count': 1, 'download_count': 1, 'download_size': 3012, 'download_size_pretty': '2K', 'default_checked': 0}, {'slug_name': 'browse_medium', 'tooltip': 'Medium-size (often 512x512) non-linearly stretched preview JPEGs (*_med.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (medium)', 'product_count': 1, 'download_count': 1, 'download_size': 7892, 'download_size_pretty': '7K', 'default_checked': 0}, {'slug_name': 'browse_full', 'tooltip': 'Full-size non-linearly stretched preview JPEGs (*_full.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are not colored. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (full)', 'product_count': 1, 'download_count': 1, 'download_size': 215079, 'download_size_pretty': '210K', 'default_checked': 1}]]], 'error': False, 'count': 1, 'recycled_count': 0, 'reqno': 101010102}
        self._run_json_equal(url, expected, ignore='tooltip')
        url = '/__cart/status.json?reqno=789'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 789}
        self._run_json_equal(url, expected)

    def test__api_cart_add_two_remove_one_download_recyclebin1(self):
        "[test_cart_api.py] /__cart/remove: two OPUSIDs remove one with download recyclebin=1"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460960868&download=0&reqno=101010100'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 101010100}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460960653&download=&reqno=101010101'
        expected = {'error': False, 'recycled_count': 0, 'count': 2, 'reqno': 101010101}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-iss-n1460960868&download=1&reqno=101010102&recyclebin=1'
        expected = {'total_download_count': 23, 'total_download_size': 24063890, 'total_download_size_pretty': '22M', 'product_cat_list': [['Cassini ISS-Specific Products', [{'slug_name': 'coiss_raw', 'tooltip': 'Raw image files (*.IMG) for Cassini ISS. Images are in VICAR format, uncalibrated, and in units of DN (data number). Associated labels (*.LBL) are text files that contain information about the image. Also included are tlmtab.fmt, which describes the format of the VICAR binary header, and prefix.fmt, which describes the format of the binary prefix at the beginning of each line of imaging data.', 'product_type': 'Raw Image', 'product_count': 1, 'download_count': 4, 'download_size': 1104427, 'download_size_pretty': '1M', 'default_checked': 1}, {'slug_name': 'coiss_calib', 'tooltip': 'Calibrated image files (*_CALIB.IMG) for Cassini ISS. Images are in VICAR format and have been calibrated at the Ring-Moon Systems Node using the CISSCAL pipeline. They are in units of I/F. Associated labels (*.LBL) are text files that contain information about the image and its calibration.', 'product_type': 'Calibrated Image', 'product_count': 1, 'download_count': 2, 'download_size': 4206287, 'download_size_pretty': '4M', 'default_checked': 1}, {'slug_name': 'coiss_thumb', 'tooltip': 'Thumbnail-size (50x50) non-linearly stretched preview JPEGs (*.jpeg_small) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (thumbnail)', 'product_count': 1, 'download_count': 1, 'download_size': 564, 'download_size_pretty': '564B', 'default_checked': 0}, {'slug_name': 'coiss_medium', 'tooltip': 'Medium-size (256x256) non-linearly stretched preview JPEGs (*.jpeg) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (medium)', 'product_count': 1, 'download_count': 1, 'download_size': 2849, 'download_size_pretty': '2K', 'default_checked': 0}, {'slug_name': 'coiss_full', 'tooltip': 'Full-size non-linearly stretched preview PNGs or TIFFs (*.png or *.tiff) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (full)', 'product_count': 1, 'download_count': 1, 'download_size': 259925, 'download_size_pretty': '253K', 'default_checked': 0}]], ['Metadata Products', [{'slug_name': 'rms_index', 'tooltip': 'Text files created by the Ring-Moon Systems Node that summarize or augment some metadata for all observations in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'RMS Node Augmented Index', 'product_count': 1, 'download_count': 2, 'download_size': 10170954, 'download_size_pretty': '9M', 'default_checked': 0}, {'slug_name': 'inventory', 'tooltip': 'Text files ([volume]_inventory.csv) that list every planet and moon inside the instrument field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Target Body Inventory', 'product_count': 1, 'download_count': 2, 'download_size': 385595, 'download_size_pretty': '376K', 'default_checked': 0}, {'slug_name': 'planet_geometry', 'tooltip': 'Text files ([volume]_[planet]_summary.tab) that list the values of various surface geometry metadata for the central planet for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Planet Geometry Index', 'product_count': 1, 'download_count': 2, 'download_size': 1364814, 'download_size_pretty': '1M', 'default_checked': 0}, {'slug_name': 'moon_geometry', 'tooltip': 'Text files ([volume]_moon_summary.tab) that list the values of various surface geometry metadata for every moon in the field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Moon Geometry Index', 'product_count': 1, 'download_count': 2, 'download_size': 4111515, 'download_size_pretty': '3M', 'default_checked': 0}, {'slug_name': 'ring_geometry', 'tooltip': 'Text files ([volume]_ring_summary.tab) that list the values of various ring plane intercept geometry metadata for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Ring Geometry Index', 'product_count': 1, 'download_count': 2, 'download_size': 2229982, 'download_size_pretty': '2M', 'default_checked': 0}]], ['Browse Products', [{'slug_name': 'browse_thumb', 'tooltip': 'Thumbnail-size (often 100x100) non-linearly stretched preview JPEGs (*_thumb.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (thumbnail)', 'product_count': 1, 'download_count': 1, 'download_size': 995, 'download_size_pretty': '995B', 'default_checked': 0}, {'slug_name': 'browse_small', 'tooltip': 'Small-size (often 256x256) non-linearly stretched preview JPEGs (*_small.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (small)', 'product_count': 1, 'download_count': 1, 'download_size': 3012, 'download_size_pretty': '2K', 'default_checked': 0}, {'slug_name': 'browse_medium', 'tooltip': 'Medium-size (often 512x512) non-linearly stretched preview JPEGs (*_med.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (medium)', 'product_count': 1, 'download_count': 1, 'download_size': 7892, 'download_size_pretty': '7K', 'default_checked': 0}, {'slug_name': 'browse_full', 'tooltip': 'Full-size non-linearly stretched preview JPEGs (*_full.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are not colored. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (full)', 'product_count': 1, 'download_count': 1, 'download_size': 215079, 'download_size_pretty': '210K', 'default_checked': 1}]]], 'error': False, 'count': 1, 'recycled_count': 1, 'reqno': 101010102}
        self._run_json_equal(url, expected, ignore='tooltip')
        url = '/__cart/status.json?reqno=789'
        expected = {'recycled_count': 1, 'count': 1, 'reqno': 789}
        self._run_json_equal(url, expected)

    def test__api_cart_unselect_option_one_download_recyclebin0(self):
        "[test_cart_api.py] /__cart/unselect option: good OPUSID with download recyclebin=0"
        url = '/opus/__cart/reset.json?reqno=42'
        expected = {'count': 0, 'recycled_count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/opus/__cart/add.json?opusid=co-iss-n1460961026&reqno=456'
        expected = {'error': False, 'count': 1, 'recycled_count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = 'opus/__cart/view.json?types=inventory,planet_geometry,moon_geometry,ring_geometry,browse_full&unselected_types=coiss_raw,coiss_calib,coiss_thumb,coiss_medium,coiss_full&reqno=710'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 710}
        ignore = 'html'
        self._run_json_equal(url, expected, ignore)
        url = '/opus/__cart/remove.json?opusid=co-iss-n1460961026&reqno=123456&download=1'
        expected = {'total_download_count': 0, 'total_download_size': 0, 'total_download_size_pretty': '0B', 'product_cat_list': [], 'error': False, 'count': 0, 'recycled_count': 0, 'reqno': 123456}
        self._run_json_equal(url, expected)
        url = 'opus/__cart/view.json?types=inventory,planet_geometry,moon_geometry,ring_geometry,browse_thumb,browse_small,browse_medium,browse_full&unselected_types=coiss_raw,coiss_calib,coiss_thumb,coiss_medium,coiss_full&reqno=711'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 711}
        ignore = 'html'
        self._run_json_equal(url, expected, ignore)
        url = '/opus/__cart/add.json?opusid=co-iss-n1460961026&reqno=458'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 458}
        self._run_json_equal(url, expected)
        url = '/opus/__cart/status.json?download=1&reqno=789'
        expected = {'total_download_count': 23, 'total_download_size': 24289889, 'total_download_size_pretty': '23M', 'product_cat_list': [['Cassini ISS-Specific Products', [{'slug_name': 'coiss_raw', 'tooltip': 'Raw image files (*.IMG) for Cassini ISS. Images are in VICAR format, uncalibrated, and in units of DN (data number). Associated labels (*.LBL) are text files that contain information about the image. Also included are tlmtab.fmt, which describes the format of the VICAR binary header, and prefix.fmt, which describes the format of the binary prefix at the beginning of each line of imaging data.', 'product_type': 'Raw Image', 'product_count': 1, 'download_count': 4, 'download_size': 1104417, 'download_size_pretty': '1M', 'default_checked': 1}, {'slug_name': 'coiss_calib', 'tooltip': 'Calibrated image files (*_CALIB.IMG) for Cassini ISS. Images are in VICAR format and have been calibrated at the Ring-Moon Systems Node using the CISSCAL pipeline. They are in units of I/F. Associated labels (*.LBL) are text files that contain information about the image and its calibration.', 'product_type': 'Calibrated Image', 'product_count': 1, 'download_count': 2, 'download_size': 4206277, 'download_size_pretty': '4M', 'default_checked': 1}, {'slug_name': 'coiss_thumb', 'tooltip': 'Thumbnail-size (50x50) non-linearly stretched preview JPEGs (*.jpeg_small) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (thumbnail)', 'product_count': 1, 'download_count': 1, 'download_size': 717, 'download_size_pretty': '717B', 'default_checked': 0}, {'slug_name': 'coiss_medium', 'tooltip': 'Medium-size (256x256) non-linearly stretched preview JPEGs (*.jpeg) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (medium)', 'product_count': 1, 'download_count': 1, 'download_size': 4172, 'download_size_pretty': '4K', 'default_checked': 0}, {'slug_name': 'coiss_full', 'tooltip': 'Full-size non-linearly stretched preview PNGs or TIFFs (*.png or *.tiff) of observations, supplied by the Cassini Imaging team. The previews are not colored and the stretch may be different from the browse images produced by the Ring-Moon Systems Node.', 'product_type': 'Extra Preview (full)', 'product_count': 1, 'download_count': 1, 'download_size': 382743, 'download_size_pretty': '373K', 'default_checked': 0}]], ['Metadata Products', [{'slug_name': 'rms_index', 'tooltip': 'Text files created by the Ring-Moon Systems Node that summarize or augment some metadata for all observations in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'RMS Node Augmented Index', 'product_count': 1, 'download_count': 2, 'download_size': 10170954, 'download_size_pretty': '9M', 'default_checked': 0}, {'slug_name': 'inventory', 'tooltip': 'Text files ([volume]_inventory.csv) that list every planet and moon inside the instrument field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Target Body Inventory', 'product_count': 1, 'download_count': 2, 'download_size': 385595, 'download_size_pretty': '376K', 'default_checked': 0}, {'slug_name': 'planet_geometry', 'tooltip': 'Text files ([volume]_[planet]_summary.tab) that list the values of various surface geometry metadata for the central planet for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Planet Geometry Index', 'product_count': 1, 'download_count': 2, 'download_size': 1364814, 'download_size_pretty': '1M', 'default_checked': 0}, {'slug_name': 'moon_geometry', 'tooltip': 'Text files ([volume]_moon_summary.tab) that list the values of various surface geometry metadata for every moon in the field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Moon Geometry Index', 'product_count': 1, 'download_count': 2, 'download_size': 4111515, 'download_size_pretty': '3M', 'default_checked': 0}, {'slug_name': 'ring_geometry', 'tooltip': 'Text files ([volume]_ring_summary.tab) that list the values of various ring plane intercept geometry metadata for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Ring Geometry Index', 'product_count': 1, 'download_count': 2, 'download_size': 2229982, 'download_size_pretty': '2M', 'default_checked': 0}]], ['Browse Products', [{'slug_name': 'browse_thumb', 'tooltip': 'Thumbnail-size (often 100x100) non-linearly stretched preview JPEGs (*_thumb.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (thumbnail)', 'product_count': 1, 'download_count': 1, 'download_size': 1908, 'download_size_pretty': '1K', 'default_checked': 0}, {'slug_name': 'browse_small', 'tooltip': 'Small-size (often 256x256) non-linearly stretched preview JPEGs (*_small.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (small)', 'product_count': 1, 'download_count': 1, 'download_size': 5509, 'download_size_pretty': '5K', 'default_checked': 0}, {'slug_name': 'browse_medium', 'tooltip': 'Medium-size (often 512x512) non-linearly stretched preview JPEGs (*_med.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (medium)', 'product_count': 1, 'download_count': 1, 'download_size': 14111, 'download_size_pretty': '13K', 'default_checked': 0}, {'slug_name': 'browse_full', 'tooltip': 'Full-size non-linearly stretched preview JPEGs (*_full.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are not colored. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (full)', 'product_count': 1, 'download_count': 1, 'download_size': 307175, 'download_size_pretty': '299K', 'default_checked': 1}]]], 'count': 1, 'recycled_count': 0, 'reqno': 789}
        self._run_json_equal(url, expected)


            #############################################################
            ######### /__cart/addrange.json (browse): API TESTS #########
            #############################################################

    def test__api_cart_addrange_no_reqno(self):
        "[test_cart_api.py] /__cart/addrange: no reqno"
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir'
        self._run_status_equal(url, 404,
                           HTTP404_BAD_OR_MISSING_REQNO('/__cart/addrange.json'))

    def test__api_cart_addrange_missing(self):
        "[test_cart_api.py] /__cart/addrange: missing range no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?reqno=456'
        self._run_status_equal(url, 404,
                       HTTP404_BAD_OR_MISSING_RANGE('/__cart/addrange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_empty(self):
        "[test_cart_api.py] /__cart/addrange: empty range no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?range=&reqno=456'
        self._run_status_equal(url, 404,
                       HTTP404_BAD_OR_MISSING_RANGE('/__cart/addrange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_bad_range1(self):
        "[test_cart_api.py] /__cart/addrange: bad range 1 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?range=co-vims-v1484504505_ir&reqno=456'
        self._run_status_equal(url, 404,
                       HTTP404_BAD_OR_MISSING_RANGE('/__cart/addrange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_bad_range2(self):
        "[test_cart_api.py] /__cart/addrange: bad range 2 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?range=co-vims-v1484504505_ir,&reqno=456'
        self._run_status_equal(url, 404,
                       HTTP404_BAD_OR_MISSING_RANGE('/__cart/addrange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_bad_range3(self):
        "[test_cart_api.py] /__cart/addrange: bad range 3 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?range=,co-vims-v1484504505_ir&reqno=456'
        self._run_status_equal(url, 404,
                        HTTP404_BAD_OR_MISSING_RANGE('/__cart/addrange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_bad_range4(self):
        "[test_cart_api.py] /__cart/addrange: bad range 4 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?range=co-vims-v1484504505_ir,co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=456'
        self._run_status_equal(url, 404,
                        HTTP404_BAD_OR_MISSING_RANGE('/__cart/addrange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_one(self):
        "[test_cart_api.py] /__cart/addrange: one good OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_one_browse(self):
        "[test_cart_api.py] /__cart/addrange: one good OPUSID no download browse"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?view=browse&volumeid=COVIMS_0006&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_duplicate(self):
        "[test_cart_api.py] /__cart/addrange: duplicate OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1484528864_ir,co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_duplicate_browse(self):
        "[test_cart_api.py] /__cart/addrange: duplicate OPUSID no download browse"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?view=browse&volumeid=COVIMS_0006&range=co-vims-v1484528864_ir,co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_duplicate2(self):
        "[test_cart_api.py] /__cart/addrange: duplicate 2 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_duplicate3(self):
        "[test_cart_api.py] /__cart/addrange: duplicate 3 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488644667_vis,co-vims-v1488647105_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 22, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 22, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_duplicate4(self):
        "[test_cart_api.py] /__cart/addrange: duplicate 4 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642979_ir,co-vims-v1488647105_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 22, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 22, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_duplicate5(self):
        "[test_cart_api.py] /__cart/addrange: duplicate 5 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1488642557_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_duplicate6(self):
        "[test_cart_api.py] /__cart/addrange: duplicate 6 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1488642557_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_bad_opusid(self):
        "[test_cart_api.py] /__cart/addrange: bad OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1484528864_irx,co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': 'An OPUS ID was given to addrange that was not found using the supplied search criteria', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_bad_opusid2(self):
        "[test_cart_api.py] /__cart/addrange: bad OPUSID 2 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1484528864_ir,co-vims-v1484528864_irx&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': 'An OPUS ID was given to addrange that was not found using the supplied search criteria', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_not_search(self):
        "[test_cart_api.py] /__cart/addrange: OPUSID not in search no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=vg-iss-2-s-c4360001,vg-iss-2-s-c4360001&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': 'An OPUS ID was given to addrange that was not found using the supplied search criteria', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_bad_search(self):
        "[test_cart_api.py] /__cart/addrange: bad search no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeidXX=COVIMS_0006&range=vg-iss-2-s-c4360001,vg-iss-2-s-c4360001&reqno=456'
        self._run_status_equal(url, 404,
                        HTTP404_SEARCH_PARAMS_INVALID('/__cart/addrange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_multi(self):
        "[test_cart_api.py] /__cart/addrange: multiple no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_multi_recyclebin0(self):
        "[test_cart_api.py] /__cart/addrange: multiple no download recyclebin=0"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456&recyclebin=0'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_multi_recyclebin1(self):
        "[test_cart_api.py] /__cart/addrange: multiple no download recyclebin=1"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456&recyclebin=1'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_multi_reverse(self):
        "[test_cart_api.py] /__cart/addrange: multiple reversed no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488646261_ir,co-vims-v1488642557_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_multi_sort(self):
        "[test_cart_api.py] /__cart/addrange: multiple nonstandard sort no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&instrument=Cassini+VIMS&primaryfilespec=8864&order=COVIMSswathlength,-time1,-opusid&range=co-vims-v1488649724_vis,co-vims-v1488647527_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 10, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 10, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_missing_download(self):
        "[test_cart_api.py] /__cart/addrange: missing range with download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?download=1&reqno=456'
        self._run_status_equal(url, 404,
                        HTTP404_BAD_OR_MISSING_RANGE('/__cart/addrange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_multi_download(self):
        "[test_cart_api.py] /__cart/addrange: multiple with download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=1234567&download=1'
        expected = {"total_download_count": 94, "total_download_size": 12349187, "total_download_size_pretty": "11M", "product_cat_list": [["Cassini VIMS-Specific Products", [{"slug_name": "covims_raw", "tooltip": "Raw data files (*.qub) for Cassini VIMS. Observations are in binary format, uncalibrated, and contain raw data numbers from both the VIS and IR detectors. Associated labels (*.lbl) are text files that contain information about the observation, including how to interpret the binary data.", "product_type": "Raw Cube", "product_count": 17, "download_count": 21, "download_size": 2919003, "download_size_pretty": "2M", "default_checked": 1}, {"slug_name": "covims_thumb", "tooltip": "Thumbnail-size (131x69) JPEGs (*.jpeg_small) supplied by the Cassini VIMS team, showing the recorded spectra of both the VIS and IR channels in grey scale. This representation is different from that provided by the PDS Ring-Moon System Node preview images, which attempt to color-code the observations in a way that emphasizes certain important spectral ranges, including wavelengths seen by the human eye.", "product_type": "Extra Preview (thumbnail)", "product_count": 17, "download_count": 9, "download_size": 17411, "download_size_pretty": "17K", "default_checked": 0}, {"slug_name": "covims_medium", "tooltip": "Medium-size (786x414) JPEGs (*.jpeg) supplied by the Cassini VIMS team, showing the recorded spectra of both the VIS and IR channels in grey scale. This representation is different from that provided by the PDS Ring-Moon System Node preview images, which attempt to color-code the observations in a way that emphasizes certain important spectral ranges, including wavelengths seen by the human eye.", "product_type": "Extra Preview (medium)", "product_count": 17, "download_count": 9, "download_size": 183437, "download_size_pretty": "179K", "default_checked": 0}, {"slug_name": "covims_full", "tooltip": "Full-size (131x69) TIFFs (*.tiff) supplied by the Cassini VIMS team, showing the recorded spectra of both the VIS and IR channels in grey scale. This representation is different from that provided by the PDS Ring-Moon System Node preview images, which attempt to color-code the observations in a way that emphasizes certain important spectral ranges, including wavelengths seen by the human eye.", "product_type": "Extra Preview (full)", "product_count": 17, "download_count": 9, "download_size": 455148, "download_size_pretty": "444K", "default_checked": 0}]], ["Metadata Products", [{"slug_name": "rms_index", "tooltip": "Text files created by the Ring-Moon Systems Node that summarize or augment some metadata for all observations in a particular volume. Associated labels (*.lbl) describe the contents of the text files.", "product_type": "RMS Node Augmented Index", "product_count": 17, "download_count": 2, "download_size": 1958899, "download_size_pretty": "1M", "default_checked": 0}, {"slug_name": "supplemental_index", "tooltip": "Text files ([volume]_supplemental_index.tab) created by the Ring-Moon Systems Node that augment metadata for all observations in a particular volume. Associated labels (*.lbl) describe the contents of the text files.", "product_type": "Supplemental Index", "product_count": 17, "download_count": 2, "download_size": 1786592, "download_size_pretty": "1M", "default_checked": 0}, {"slug_name": "inventory", "tooltip": "Text files ([volume]_inventory.csv) that list every planet and moon inside the instrument field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.", "product_type": "Target Body Inventory", "product_count": 17, "download_count": 2, "download_size": 383776, "download_size_pretty": "374K", "default_checked": 0}, {"slug_name": "planet_geometry", "tooltip": "Text files ([volume]_[planet]_summary.tab) that list the values of various surface geometry metadata for the central planet for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.", "product_type": "Planet Geometry Index", "product_count": 17, "download_count": 2, "download_size": 1485943, "download_size_pretty": "1M", "default_checked": 0}, {"slug_name": "ring_geometry", "tooltip": "Text files ([volume]_ring_summary.tab) that list the values of various ring plane intercept geometry metadata for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.", "product_type": "Ring Geometry Index", "product_count": 17, "download_count": 2, "download_size": 2382135, "download_size_pretty": "2M", "default_checked": 0}]], ["Browse Products", [{"slug_name": "browse_thumb", "tooltip": "Thumbnail-size (often 100x100) non-linearly stretched preview JPEGs (*_thumb.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.", "product_type": "Browse Image (thumbnail)", "product_count": 17, "download_count": 9, "download_size": 82840, "download_size_pretty": "80K", "default_checked": 0}, {"slug_name": "browse_small", "tooltip": "Small-size (often 256x256) non-linearly stretched preview JPEGs (*_small.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.", "product_type": "Browse Image (small)", "product_count": 17, "download_count": 9, "download_size": 227327, "download_size_pretty": "221K", "default_checked": 0}, {"slug_name": "browse_medium", "tooltip": "Medium-size (often 512x512) non-linearly stretched preview JPEGs (*_med.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.", "product_type": "Browse Image (medium)", "product_count": 17, "download_count": 9, "download_size": 233338, "download_size_pretty": "227K", "default_checked": 0}, {"slug_name": "browse_full", "tooltip": "Full-size non-linearly stretched preview JPEGs (*_full.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are not colored. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.", "product_type": "Browse Image (full)", "product_count": 17, "download_count": 9, "download_size": 233338, "download_size_pretty": "227K", "default_checked": 1}]]], "error": False, "count": 17, "recycled_count": 0, "reqno": 1234567}
        self._run_json_equal(url, expected, ignore='tooltip')
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_one_too_many_0(self):
        "[test_cart_api.py] /__cart/addrange: one good OPUSID no download too many 0"
        settings.MAX_SELECTIONS_ALLOWED = 0
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=567'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 567}
        else:
            expected = {'recycled_count': 0, 'count': 0, 'error': 'Your request to add 1 observations (OPUS IDs co-vims-v1484504505_ir to co-vims-v1484504505_ir) to the cart failed. The resulting cart and recycle bin would have more than the maximum (0) allowed. None of the observations were added.', 'reqno': 567}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        else:
            expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_one_too_many_1(self):
        "[test_cart_api.py] /__cart/addrange: one good OPUSID no download too many 1"
        settings.MAX_SELECTIONS_ALLOWED = 1
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=567'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 567}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_duplicate2_too_many_17(self):
        "[test_cart_api.py] /__cart/addrange: duplicate 2 no download too many 17"
        settings.MAX_SELECTIONS_ALLOWED = 17
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'reqno': 456}
        self._run_json_equal(url, expected)


            ################################################################
            ######### /__cart/removerange.json (browse): API TESTS #########
            ################################################################

    def test__api_cart_removerange_no_reqno(self):
        "[test_cart_api.py] /__cart/removerange: no reqno"
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir'
        self._run_status_equal(url, 404,
                    HTTP404_BAD_OR_MISSING_REQNO('/__cart/removerange.json'))

    def test__api_cart_removerange_missing(self):
        "[test_cart_api.py] /__cart/removerange: missing range no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        self._run_status_equal(url, 200)
        url = '/__cart/removerange.json?reqno=456'
        self._run_status_equal(url, 404,
                    HTTP404_BAD_OR_MISSING_RANGE('/__cart/removerange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_empty(self):
        "[test_cart_api.py] /__cart/removerange: empty range no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?range=&reqno=456'
        self._run_status_equal(url, 404,
                    HTTP404_BAD_OR_MISSING_RANGE('/__cart/removerange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_bad_range1(self):
        "[test_cart_api.py] /__cart/removerange: bad range 1 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?range=co-vims-v1484504505_ir&reqno=456'
        self._run_status_equal(url, 404,
                    HTTP404_BAD_OR_MISSING_RANGE('/__cart/removerange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_bad_range2(self):
        "[test_cart_api.py] /__cart/removerange: bad range 2 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?range=co-vims-v1484504505_ir,&reqno=456'
        self._run_status_equal(url, 404,
                    HTTP404_BAD_OR_MISSING_RANGE('/__cart/removerange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_bad_range3(self):
        "[test_cart_api.py] /__cart/removerange: bad range 3 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?range=,co-vims-v1484504505_ir&reqno=456'
        self._run_status_equal(url, 404,
                    HTTP404_BAD_OR_MISSING_RANGE('/__cart/removerange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_bad_range4(self):
        "[test_cart_api.py] /__cart/removerange: bad range 4 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?range=co-vims-v1484504505_ir,co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=456'
        self._run_status_equal(url, 404,
                    HTTP404_BAD_OR_MISSING_RANGE('/__cart/removerange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_add_one(self):
        "[test_cart_api.py] /__cart/removerange: add+removerange one good OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_add_one_recyclebin0(self):
        "[test_cart_api.py] /__cart/removerange: add+removerange one good OPUSID no download recyclebin=0"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=456&recyclebin=0'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_add_one_recyclebin1(self):
        "[test_cart_api.py] /__cart/removerange: add+removerange one good OPUSID no download recyclebin=1"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=456&recyclebin=1'
        expected = {'recycled_count': 1, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 1, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_duplicate(self):
        "[test_cart_api.py] /__cart/removerange: duplicate OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1484528864_ir,co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1484528864_ir,co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_duplicate_recyclebin1(self):
        "[test_cart_api.py] /__cart/removerange: duplicate OPUSID no download recyclebin=1"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1484528864_ir,co-vims-v1484528864_ir&reqno=456&recyclebin=1'
        expected = {'recycled_count': 1, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1484528864_ir,co-vims-v1484528864_ir&reqno=456&recyclebin=1'
        expected = {'recycled_count': 1, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 1, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_duplicate2(self):
        "[test_cart_api.py] /__cart/removerange: duplicate 2 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_duplicate3(self):
        "[test_cart_api.py] /__cart/removerange: duplicate 3 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1488644667_vis,co-vims-v1488647105_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 11, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1488644667_vis,co-vims-v1488647105_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 11, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 11, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_bad_opusid(self):
        "[test_cart_api.py] /__cart/removerange: bad OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1484528864_irx,co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': 'An OPUS ID was given to removerange that was not found using the supplied search criteria', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_bad_opusid2(self):
        "[test_cart_api.py] /__cart/removerange: bad OPUSID 2 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1484528864_ir,co-vims-v1484528864_irx&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': 'An OPUS ID was given to addrange that was not found using the supplied search criteria', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_not_search(self):
        "[test_cart_api.py] /__cart/removerange: OPUSID not in search no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=vg-iss-2-s-c4360001,vg-iss-2-s-c4360001&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': 'An OPUS ID was given to removerange that was not found using the supplied search criteria', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_bad_search(self):
        "[test_cart_api.py] /__cart/removerange: bad search no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeidXX=COVIMS_0006&range=vg-iss-2-s-c4360001,vg-iss-2-s-c4360001&reqno=456'
        self._run_status_equal(url, 404,
                    HTTP404_SEARCH_PARAMS_INVALID('/__cart/removerange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_multi(self):
        "[test_cart_api.py] /__cart/removerange: multiple no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1488642979_vis,co-vims-v1488644245_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 10, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 10, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_multi_reverse(self):
        "[test_cart_api.py] /__cart/removerange: multiple reversed no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1488644245_vis,co-vims-v1488642979_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 10, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 10, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_multi_sort(self):
        "[test_cart_api.py] /__cart/removerange: multiple nonstandard sort no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&order=COVIMSswathlength,-time1,opusid&range=co-vims-v1490784910_001_ir,co-vims-v1490782254_001_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 6, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        # Note sort reverses opusid! This leaves two observations behind
        # because _ir and _vis are in a different order for each observation
        # pair
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&order=COVIMSswathlength,-time1,-opusid&range=co-vims-v1490784910_001_ir,co-vims-v1490782254_001_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_one(self):
        "[test_cart_api.py] /__cart/removerange: one good OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=567'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 567}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_missing_download(self):
        "[test_cart_api.py] /__cart/removerange: missing range with download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?download=1&reqno=456'
        self._run_status_equal(url, 404,
                    HTTP404_BAD_OR_MISSING_RANGE('/__cart/removerange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_multi_download(self):
        "[test_cart_api.py] /__cart/removerange: multiple with download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=1234567'
        expected = {'error': False, 'recycled_count': 0, 'count': 17, 'reqno': 1234567}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1488642135_ir,co-vims-v1488643823_ir&reqno=12345678&download=1'
        expected = {"total_download_count": 67, "total_download_size": 10895091, "total_download_size_pretty": "10M", "product_cat_list": [["Cassini VIMS-Specific Products", [{"slug_name": "covims_raw", "tooltip": "Raw data files (*.qub) for Cassini VIMS. Observations are in binary format, uncalibrated, and contain raw data numbers from both the VIS and IR detectors. Associated labels (*.lbl) are text files that contain information about the observation, including how to interpret the binary data.", "product_type": "Raw Cube", "product_count": 10, "download_count": 15, "download_size": 1948066, "download_size_pretty": "1M", "default_checked": 1}, {"slug_name": "covims_thumb", "tooltip": "Thumbnail-size (131x69) JPEGs (*.jpeg_small) supplied by the Cassini VIMS team, showing the recorded spectra of both the VIS and IR channels in grey scale. This representation is different from that provided by the PDS Ring-Moon System Node preview images, which attempt to color-code the observations in a way that emphasizes certain important spectral ranges, including wavelengths seen by the human eye.", "product_type": "Extra Preview (thumbnail)", "product_count": 10, "download_count": 6, "download_size": 11718, "download_size_pretty": "11K", "default_checked": 0}, {"slug_name": "covims_medium", "tooltip": "Medium-size (786x414) JPEGs (*.jpeg) supplied by the Cassini VIMS team, showing the recorded spectra of both the VIS and IR channels in grey scale. This representation is different from that provided by the PDS Ring-Moon System Node preview images, which attempt to color-code the observations in a way that emphasizes certain important spectral ranges, including wavelengths seen by the human eye.", "product_type": "Extra Preview (medium)", "product_count": 10, "download_count": 6, "download_size": 122860, "download_size_pretty": "119K", "default_checked": 0}, {"slug_name": "covims_full", "tooltip": "Full-size (131x69) TIFFs (*.tiff) supplied by the Cassini VIMS team, showing the recorded spectra of both the VIS and IR channels in grey scale. This representation is different from that provided by the PDS Ring-Moon System Node preview images, which attempt to color-code the observations in a way that emphasizes certain important spectral ranges, including wavelengths seen by the human eye.", "product_type": "Extra Preview (full)", "product_count": 10, "download_count": 6, "download_size": 303432, "download_size_pretty": "296K", "default_checked": 0}]], ["Metadata Products", [{"slug_name": "rms_index", "tooltip": "Text files created by the Ring-Moon Systems Node that summarize or augment some metadata for all observations in a particular volume. Associated labels (*.lbl) describe the contents of the text files.", "product_type": "RMS Node Augmented Index", "product_count": 10, "download_count": 2, "download_size": 1958899, "download_size_pretty": "1M", "default_checked": 0}, {"slug_name": "supplemental_index", "tooltip": "Text files ([volume]_supplemental_index.tab) created by the Ring-Moon Systems Node that augment metadata for all observations in a particular volume. Associated labels (*.lbl) describe the contents of the text files.", "product_type": "Supplemental Index", "product_count": 10, "download_count": 2, "download_size": 1786592, "download_size_pretty": "1M", "default_checked": 0}, {"slug_name": "inventory", "tooltip": "Text files ([volume]_inventory.csv) that list every planet and moon inside the instrument field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.", "product_type": "Target Body Inventory", "product_count": 10, "download_count": 2, "download_size": 383776, "download_size_pretty": "374K", "default_checked": 0}, {"slug_name": "planet_geometry", "tooltip": "Text files ([volume]_[planet]_summary.tab) that list the values of various surface geometry metadata for the central planet for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.", "product_type": "Planet Geometry Index", "product_count": 10, "download_count": 2, "download_size": 1485943, "download_size_pretty": "1M", "default_checked": 0}, {"slug_name": "ring_geometry", "tooltip": "Text files ([volume]_ring_summary.tab) that list the values of various ring plane intercept geometry metadata for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.", "product_type": "Ring Geometry Index", "product_count": 10, "download_count": 2, "download_size": 2382135, "download_size_pretty": "2M", "default_checked": 0}]], ["Browse Products", [{"slug_name": "browse_thumb", "tooltip": "Thumbnail-size (often 100x100) non-linearly stretched preview JPEGs (*_thumb.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.", "product_type": "Browse Image (thumbnail)", "product_count": 10, "download_count": 6, "download_size": 54402, "download_size_pretty": "53K", "default_checked": 0}, {"slug_name": "browse_small", "tooltip": "Small-size (often 256x256) non-linearly stretched preview JPEGs (*_small.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.", "product_type": "Browse Image (small)", "product_count": 10, "download_count": 6, "download_size": 149668, "download_size_pretty": "146K", "default_checked": 0}, {"slug_name": "browse_medium", "tooltip": "Medium-size (often 512x512) non-linearly stretched preview JPEGs (*_med.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.", "product_type": "Browse Image (medium)", "product_count": 10, "download_count": 6, "download_size": 153800, "download_size_pretty": "150K", "default_checked": 0}, {"slug_name": "browse_full", "tooltip": "Full-size non-linearly stretched preview JPEGs (*_full.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are not colored. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.", "product_type": "Browse Image (full)", "product_count": 10, "download_count": 6, "download_size": 153800, "download_size_pretty": "150K", "default_checked": 1}]]], "error": False, "count": 10, "recycled_count": 0, "reqno": 12345678}
        self._run_json_equal(url, expected, ignore='tooltip')
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 10, 'reqno': 456}
        self._run_json_equal(url, expected)


            ###########################################################
            ######### /__cart/addrange.json (cart): API TESTS #########
            ###########################################################

    def test__api_cart_addrange_one_cart_missing(self):
        "[test_cart_api.py] /__cart/addrange: cart missing"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?view=cart&volumeid=COVIMS_0006&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': 'An OPUS ID was given to addrange that was not found in the cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_bad_range1_cart(self):
        "[test_cart_api.py] /__cart/addrange: cart bad range 1 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?view=cart&range=co-vims-v1484504505_ir&reqno=456'
        self._run_status_equal(url, 404,
                        HTTP404_BAD_OR_MISSING_RANGE('/__cart/addrange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_bad_range4_cart(self):
        "[test_cart_api.py] /__cart/addrange: cart bad range 4 no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?view=cart&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=456'
        self._run_status_equal(url, 404,
                        HTTP404_BAD_OR_MISSING_RANGE('/__cart/addrange.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_duplicate_cart(self):
        "[test_cart_api.py] /__cart/addrange: cart one good OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?view=cart&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_duplicate_cart_recyclebin0(self):
        "[test_cart_api.py] /__cart/addrange: cart one good OPUSID no download recyclebin=0"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?view=cart&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=456&recyclebin=0'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_duplicate_cart_recyclebin1(self):
        "[test_cart_api.py] /__cart/addrange: cart one good OPUSID no download recyclebin=1"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?view=cart&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=456&recyclebin=1'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_bad_opusid_cart(self):
        "[test_cart_api.py] /__cart/addrange: cart bad OPUSID no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1484528864_ir,co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?view=cart&range=co-vims-v1484528864_irx,co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': 'An OPUS ID was given to addrange that was not found in the cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_multi_not_cart_cart(self):
        "[test_cart_api.py] /__cart/addrange: cart OPUSID not in cart no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1484506475_ir,co-vims-v1484507574_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 6, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?view=cart&volumeid=COVIMS_0006&range=co-vims-v1484504505_vis,co-vims-v1484507574_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 6, 'error': 'An OPUS ID was given to addrange that was not found in the cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 6, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_duplicate2_too_many_17_cart(self):
        "[test_cart_api.py] /__cart/addrange: cart_duplicate 2 no download too many 17"
        settings.MAX_SELECTIONS_ALLOWED = 17
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?view=cart&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'reqno': 456}
        self._run_json_equal(url, expected)


            ##############################################################
            ######### /__cart/removerange.json (cart): API TESTS #########
            ##############################################################

    def test__api_cart_removerange_add_one_cart(self):
        "[test_cart_api.py] /__cart/removerange: add+removerange one good OPUSID no download cart"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&volumeid=COVIMS_0006&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_add_one_cart_recyclebin1(self):
        "[test_cart_api.py] /__cart/removerange: add+removerange one good OPUSID no download cart recyclebin=1"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484504505_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&volumeid=COVIMS_0006&range=co-vims-v1484504505_ir,co-vims-v1484504505_ir&reqno=456&recyclebin=1'
        expected = {'recycled_count': 1, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 1, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_duplicate_cart(self):
        "[test_cart_api.py] /__cart/removerange: duplicate OPUSID no download cart"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&volumeid=COVIMS_0006&range=co-vims-v1484528864_ir,co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&volumeid=COVIMS_0006&range=co-vims-v1484528864_ir,co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'error': 'An OPUS ID was given to removerange that was not found in the cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_duplicate_cart_recyclebin1(self):
        "[test_cart_api.py] /__cart/removerange: duplicate OPUSID no download cart recyclebin=1"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1484528864_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&volumeid=COVIMS_0006&range=co-vims-v1484528864_ir,co-vims-v1484528864_ir&reqno=456&recyclebin=1'
        expected = {'recycled_count': 1, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&volumeid=COVIMS_0006&range=co-vims-v1484528864_ir,co-vims-v1484528864_ir&reqno=456&recyclebin=1'
        expected = {'recycled_count': 1, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 1, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_multi_cart(self):
        "[test_cart_api.py] /__cart/removerange: multiple no download cart"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&range=co-vims-v1488642979_vis,co-vims-v1488644245_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 10, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 10, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_multi_cart_recyclebin1(self):
        "[test_cart_api.py] /__cart/removerange: multiple no download cart recyclebin=1"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&range=co-vims-v1488642979_vis,co-vims-v1488644245_vis&reqno=456&recyclebin=1'
        expected = {'recycled_count': 7, 'count': 10, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 7, 'count': 10, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_multi_reverse_cart(self):
        "[test_cart_api.py] /__cart/removerange: multiple reversed no download cart"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&range=co-vims-v1488644245_vis,co-vims-v1488642979_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 10, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 10, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_multi_reverse_cart_recyclebin1(self):
        "[test_cart_api.py] /__cart/removerange: multiple reversed no download cart recyclebin=1"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&range=co-vims-v1488644245_vis,co-vims-v1488642979_vis&reqno=456&recyclebin=1'
        expected = {'recycled_count': 7, 'count': 10, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 7, 'count': 10, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_multi_sort_cart(self):
        "[test_cart_api.py] /__cart/removerange: multiple nonstandard sort no download cart"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        # Default sort = time1,opusid
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        # New sort = rightasc1,opusid - would be 5 obs if using default sort
        url = '/__cart/removerange.json?view=cart&order=rightasc1,opusid&range=co-vims-v1488642557_ir,co-vims-v1488644245_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 13, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&range=co-vims-v1488643823_vis,co-vims-v1488643823_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 13, 'error': 'An OPUS ID was given to removerange that was not found in the cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 13, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_multi_sort2_cart(self):
        "[test_cart_api.py] /__cart/removerange: multiple nonstandard sort 2 no download cart"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&rightasc1=80.000000&rightasc2=85.000000&range=co-vims-v1486998899_ir,co-vims-v1488653840_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 110, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        # Joins in another obs table AND a mult table
        url = '/__cart/removerange.json?view=cart&order=COVIMSchannel,opusid&range=co-vims-v1488653418_ir,co-vims-v1486999344_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 106, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&range=co-vims-v1488653840_ir,co-vims-v1488653840_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 106, 'error': 'An OPUS ID was given to removerange that was not found in the cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 106, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_removerange_multi_sort3_cart(self):
        "[test_cart_api.py] /__cart/removerange: multiple nonstandard sort 3 no download cart"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&rightasc1=80.000000&rightasc2=85.000000&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        # Joins in another obs table AND a mult table
        url = '/__cart/removerange.json?view=cart&order=COVIMSchannel,opusid&range=co-vims-v1488645417_ir,co-vims-v1488642979_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 12, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&range=co-vims-v1488645839_ir,co-vims-v1488645839_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 12, 'error': 'An OPUS ID was given to removerange that was not found in the cart', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 12, 'reqno': 456}
        self._run_json_equal(url, expected)


            ##################################################
            ######### /__cart/addall.json: API TESTS #########
            ##################################################

    def test__api_cart_addall_no_reqno(self):
        "[test_cart_api.py] /__cart/addall: no reqno"
        url = '/__cart/addall.json?volumeid=VGISS_6210'
        self._run_status_equal(url, 404,
                            HTTP404_BAD_OR_MISSING_REQNO('/__cart/addall.json'))

    def test__api_cart_addall_one(self):
        "[test_cart_api.py] /__cart/addall: one time no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=VGISS_6210&reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addall_one_browse(self):
        "[test_cart_api.py] /__cart/addall: one time no download browse"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?view=browse&volumeid=VGISS_6210&reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addall_duplicate(self):
        "[test_cart_api.py] /__cart/addall: twice no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=VGISS_6210&reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=VGISS_6210&reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addall_duplicate2(self):
        "[test_cart_api.py] /__cart/addall: addrange plus addall no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=VGISS_6210&range=vg-iss-2-s-c4360037,vg-iss-2-s-c4365644&reqno=456'
        expected = {'recycled_count': 0, 'count': 597, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=VGISS_6210&reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addall_duplicate3(self):
        "[test_cart_api.py] /__cart/addall: add plus addall no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=vg-iss-2-s-c4360018&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=VGISS_6210&reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addall_bad_search(self):
        "[test_cart_api.py] /__cart/addall: bad search no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeidXX=COVIMS_0006&reqno=456'
        self._run_status_equal(url, 404,
                        HTTP404_SEARCH_PARAMS_INVALID('/__cart/addall.json'))
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addall_multi(self):
        "[test_cart_api.py] /__cart/addall: multiple no download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1484506475_ir,co-vims-v1484509868_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 10, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=COVIMS_0006&reqno=456'
        expected = {'recycled_count': 0, 'count': 3500, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1485893300_vis,co-vims-v1485894711_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 3487, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=VGISS_6210&reqno=456'
        expected = {'recycled_count': 0, 'count': 4393, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 4393, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addall_one_download(self):
        "[test_cart_api.py] /__cart/addall: one time with download"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=VGISS_8201&productid=12&reqno=9878&download=1'
        expected = {'total_download_count': 898, 'total_download_size': 180301857, 'total_download_size_pretty': '171M', 'product_cat_list': [['Voyager ISS-Specific Products', [{'slug_name': 'vgiss_raw', 'tooltip': 'Raw image files (*_RAW.IMG) for Voyager ISS. Images are in VICAR format, uncalibrated, and in units of DN (data number). Associated labels (*.LBL) are text files that contain information about the image. Raw images have not been geometrically corrected and contain significant distortions.', 'product_type': 'Raw Image', 'product_count': 34, 'download_count': 68, 'download_size': 28148748, 'download_size_pretty': '26M', 'default_checked': 1}, {'slug_name': 'vgiss_cleaned', 'tooltip': 'Cleaned image files (*_CLEANED.IMG) for Voyager ISS. Images are in VICAR format, uncalibrated, and in units of DN (data number). Associated labels (*.LBL) are text files that contain information about the image. Apparent flaws in the raw image, including reseau markings and spikes, have been removed.', 'product_type': 'Cleaned Image', 'product_count': 34, 'download_count': 68, 'download_size': 21936280, 'download_size_pretty': '20M', 'default_checked': 1}, {'slug_name': 'vgiss_calib', 'tooltip': 'Calibrated image files (*_CALIB.IMG) for Voyager ISS. Images are in VICAR format and have been calibrated at the Ring-Moon Systems Node using the VICAR software package. They are in units of scaled I/F. Associated labels (*.LBL) are text files that contain information about the image. Calibration was performed after apparent flaws in the raw image, including reseau markings and spikes, were removed; these are calibrated versions of the cleaned images (*_CLEANED.IMG).', 'product_type': 'Calibrated Image', 'product_count': 34, 'download_count': 68, 'download_size': 43769972, 'download_size_pretty': '41M', 'default_checked': 1}, {'slug_name': 'vgiss_geomed', 'tooltip': 'Calibrated and geometrically corrected image files (*_GEOMED.IMG) for Voyager ISS. Images are in VICAR format and have been calibrated and geometrically corrected at the Ring-Moon Systems Node using the VICAR software package. They are in units of scaled I/F. Associated labels (*.LBL) are text files that contain information about the image. Calibration was performed after apparent flaws in the raw image, including reseau markings and spikes, were removed; these are geometrically corrected versions of the calibrated images (*_CALIB.IMG).', 'product_type': 'Geometrically Corrected Image', 'product_count': 34, 'download_count': 68, 'download_size': 68190894, 'download_size_pretty': '65M', 'default_checked': 1}, {'slug_name': 'vgiss_resloc', 'tooltip': 'Files describing the determined location of the reseau markings for an image. Locations are provided in VICAR format (*_RESLOC.DAT) and text format (*_RESLOC.TAB). An associated label (*_RESLOC.LBL) is a text file that contains information about the *.DAT and *.TAB files.', 'product_type': 'Reseau Table', 'product_count': 34, 'download_count': 102, 'download_size': 672296, 'download_size_pretty': '656K', 'default_checked': 1}, {'slug_name': 'vgiss_geoma', 'tooltip': 'Files describing the nominal and measured reseau mark locations used to geometrically correct the image. Locations are provided in VICAR format (*_GEOMA.DAT) and text format (*_GEOMA.TAB). An associated label (*_GEOMA.LBL) is a text file that contains information about the *.DAT and *.TAB files.', 'product_type': 'Geometric Tiepoint Table', 'product_count': 34, 'download_count': 102, 'download_size': 1424003, 'download_size_pretty': '1M', 'default_checked': 1}, {'slug_name': 'vgiss_raw_browse', 'tooltip': 'Preview images (*_RAW.JPG) for the raw image files for Voyager ISS. Images are in VICAR format, uncalibrated, and in units of DN (data number). Associated labels (*.LBL) are text files that contain information about the image. Raw images have not been geometrically corrected and contain significant distortions.', 'product_type': 'Extra Preview (raw)', 'product_count': 34, 'download_count': 68, 'download_size': 1963297, 'download_size_pretty': '1M', 'default_checked': 0}, {'slug_name': 'vgiss_cleaned_browse', 'tooltip': 'Preview images (*_CLEANED.JPG) for the cleaned image files for Voyager ISS. Images are in VICAR format, uncalibrated, and in units of DN (data number). Associated labels (*.LBL) are text files that contain information about the image. Apparent flaws in the raw image, including reseau markings and spikes, have been removed.', 'product_type': 'Extra Preview (cleaned)', 'product_count': 34, 'download_count': 68, 'download_size': 1512756, 'download_size_pretty': '1M', 'default_checked': 0}, {'slug_name': 'vgiss_calib_browse', 'tooltip': 'Preview images (*_CALIB.JPG) for the calibrated image files for Voyager ISS. Images are in VICAR format and have been calibrated at the Ring-Moon Systems Node using the VICAR software package. They are in units of scaled I/F. Associated labels (*.LBL) are text files that contain information about the image. Calibration was performed after apparent flaws in the raw image, including reseau markings and spikes, were removed; these are calibrated versions of the cleaned images (*_CLEANED.IMG).', 'product_type': 'Extra Preview (calibrated)', 'product_count': 34, 'download_count': 68, 'download_size': 2361266, 'download_size_pretty': '2M', 'default_checked': 0}, {'slug_name': 'vgiss_geomed_browse', 'tooltip': 'Preview images (*_GEOMED.JPG) for the calibrated and geometrically corrected image files for Voyager ISS. Images are in VICAR format and have been calibrated and geometrically corrected at the Ring-Moon Systems Node using the VICAR software package. They are in units of scaled I/F. Associated labels (*.LBL) are text files that contain information about the image. Calibration was performed after apparent flaws in the raw image, including reseau markings and spikes, were removed; these are geometrically corrected versions of the calibrated images (*_CALIB.IMG).', 'product_type': 'Extra Preview (geometrically corrected)', 'product_count': 34, 'download_count': 68, 'download_size': 2665121, 'download_size_pretty': '2M', 'default_checked': 0}]], ['Metadata Products', [{'slug_name': 'rms_index', 'tooltip': 'Text files created by the Ring-Moon Systems Node that summarize or augment some metadata for all observations in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'RMS Node Augmented Index', 'product_count': 34, 'download_count': 2, 'download_size': 1881025, 'download_size_pretty': '1M', 'default_checked': 0}, {'slug_name': 'raw_image_index', 'tooltip': 'Text files ([volume]_raw_image_index.tab) that tabulate information about the raw image for each observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Raw Image Index', 'product_count': 34, 'download_count': 2, 'download_size': 324742, 'download_size_pretty': '317K', 'default_checked': 0}, {'slug_name': 'supplemental_index', 'tooltip': 'Text files ([volume]_supplemental_index.tab) created by the Ring-Moon Systems Node that augment metadata for all observations in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Supplemental Index', 'product_count': 34, 'download_count': 2, 'download_size': 161366, 'download_size_pretty': '157K', 'default_checked': 0}, {'slug_name': 'inventory', 'tooltip': 'Text files ([volume]_inventory.csv) that list every planet and moon inside the instrument field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Target Body Inventory', 'product_count': 34, 'download_count': 2, 'download_size': 81999, 'download_size_pretty': '80K', 'default_checked': 0}, {'slug_name': 'planet_geometry', 'tooltip': 'Text files ([volume]_[planet]_summary.tab) that list the values of various surface geometry metadata for the central planet for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Planet Geometry Index', 'product_count': 25, 'download_count': 2, 'download_size': 306984, 'download_size_pretty': '299K', 'default_checked': 0}, {'slug_name': 'moon_geometry', 'tooltip': 'Text files ([volume]_moon_summary.tab) that list the values of various surface geometry metadata for every moon in the field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Moon Geometry Index', 'product_count': 25, 'download_count': 2, 'download_size': 1775636, 'download_size_pretty': '1M', 'default_checked': 0}, {'slug_name': 'ring_geometry', 'tooltip': 'Text files ([volume]_ring_summary.tab) that list the values of various ring plane intercept geometry metadata for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Ring Geometry Index', 'product_count': 25, 'download_count': 2, 'download_size': 509704, 'download_size_pretty': '497K', 'default_checked': 0}]], ['Browse Products', [{'slug_name': 'browse_thumb', 'tooltip': 'Thumbnail-size (often 100x100) non-linearly stretched preview JPEGs (*_thumb.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (thumbnail)', 'product_count': 34, 'download_count': 34, 'download_size': 49298, 'download_size_pretty': '48K', 'default_checked': 0}, {'slug_name': 'browse_small', 'tooltip': 'Small-size (often 256x256) non-linearly stretched preview JPEGs (*_small.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (small)', 'product_count': 34, 'download_count': 34, 'download_size': 117246, 'download_size_pretty': '114K', 'default_checked': 0}, {'slug_name': 'browse_medium', 'tooltip': 'Medium-size (often 512x512) non-linearly stretched preview JPEGs (*_med.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (medium)', 'product_count': 34, 'download_count': 34, 'download_size': 428816, 'download_size_pretty': '418K', 'default_checked': 0}, {'slug_name': 'browse_full', 'tooltip': 'Full-size non-linearly stretched preview JPEGs (*_full.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are not colored. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (full)', 'product_count': 34, 'download_count': 34, 'download_size': 2020408, 'download_size_pretty': '1M', 'default_checked': 1}]]], 'error': False, 'count': 34, 'recycled_count': 0, 'reqno': 9878}
        self._run_json_equal(url, expected, ignore='tooltip')
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 34, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addall_one_too_many_905(self):
        "[test_cart_api.py] /__cart/addall: one time no download too many 905"
        settings.MAX_SELECTIONS_ALLOWED = 905
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=VGISS_6210&reqno=456'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 0, 'count': 906, 'error': False, 'reqno': 456}
        else:
            expected = {'recycled_count': 0, 'count': 0, 'error': 'Your request to add all 906 observations to the cart failed. The resulting cart and recycle bin would have more than the maximum (905) allowed. None of the observations were added.', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 0, 'count': 906, 'reqno': 456}
        else:
            expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addall_one_too_many_906(self):
        "[test_cart_api.py] /__cart/addall: one time no download too many 906"
        settings.MAX_SELECTIONS_ALLOWED = 906
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=VGISS_6210&reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addall_duplicate_too_many_906(self):
        "[test_cart_api.py] /__cart/addall: twice no download"
        settings.MAX_SELECTIONS_ALLOWED = 906
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=VGISS_6210&reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=VGISS_6210&reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addall_duplicate3_too_many_906(self):
        "[test_cart_api.py] /__cart/addall: add plus addall no download too many 906"
        settings.MAX_SELECTIONS_ALLOWED = 906
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=vg-iss-2-s-c4360018&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=VGISS_6210&reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'reqno': 456}
        self._run_json_equal(url, expected)


            ######################################################
            ######### /__cart/<all> recyclebin API TESTS #########
            ######################################################

    def test__api_cart_add_remove_recyclebin(self):
        "[test_cart_api.py] /__cart/add&remove: recyclebin"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=COVIMS_0006&reqno=456'
        expected = {'recycled_count': 0, 'count': 3500, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1484504505_vis,co-vims-v1484506475_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 3495, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&range=co-vims-v1484506705_vis,co-vims-v1484507800_ir&reqno=456&recyclebin=0'
        expected = {'recycled_count': 0, 'count': 3491, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&range=co-vims-v1484509868_ir,co-vims-v1484510890_vis&reqno=456&recyclebin=1'
        expected = {'recycled_count': 8, 'count': 3483, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?view=cart&range=co-vims-v1484509868_vis,co-vims-v1484510044_ir&reqno=456'
        expected = {'recycled_count': 6, 'count': 3485, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?view=browse&range=co-vims-v1484510714_ir,co-vims-v1484510890_ir&reqno=456'
        expected = {'recycled_count': 3, 'count': 3488, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 3, 'count': 3488, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_recyclebin_reset(self):
        "[test_cart_api.py] /__cart/reset: recyclebin"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=COVIMS_0006&reqno=456'
        expected = {'recycled_count': 0, 'count': 3500, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&range=co-vims-v1484509868_ir,co-vims-v1484510890_vis&reqno=456&recyclebin=1'
        expected = {'recycled_count': 8, 'count': 3492, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/reset.json?reqno=42&recyclebin=1'
        expected = {'recycled_count': 0, 'count': 3536, 'reqno': 42}
        url = '/__cart/addall.json?volumeid=COVIMS_0006&reqno=456'
        expected = {'recycled_count': 0, 'count': 3500, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&range=co-vims-v1484509868_ir,co-vims-v1484510890_vis&reqno=456&recyclebin=1'
        expected = {'recycled_count': 8, 'count': 3492, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/reset.json?reqno=42&recyclebin=1&download=1'
        expected = {'total_download_count': 15906, 'total_download_size': 2355911586, 'total_download_size_pretty': '2G', 'product_cat_list': [['Cassini VIMS-Specific Products', [{'slug_name': 'covims_raw', 'tooltip': 'Raw data files (*.qub) for Cassini VIMS. Observations are in binary format, uncalibrated, and contain raw data numbers from both the VIS and IR detectors. Associated labels (*.lbl) are text files that contain information about the observation, including how to interpret the binary data.', 'product_type': 'Raw Cube', 'product_count': 3492, 'download_count': 3535, 'download_size': 1947398604, 'download_size_pretty': '1G', 'default_checked': 1}, {'slug_name': 'covims_thumb', 'tooltip': 'Thumbnail-size (131x69) JPEGs (*.jpeg_small) supplied by the Cassini VIMS team, showing the recorded spectra of both the VIS and IR channels in grey scale. This representation is different from that provided by the PDS Ring-Moon System Node preview images, which attempt to color-code the observations in a way that emphasizes certain important spectral ranges, including wavelengths seen by the human eye.', 'product_type': 'Extra Preview (thumbnail)', 'product_count': 3490, 'download_count': 1765, 'download_size': 5021315, 'download_size_pretty': '4M', 'default_checked': 0}, {'slug_name': 'covims_medium', 'tooltip': 'Medium-size (786x414) JPEGs (*.jpeg) supplied by the Cassini VIMS team, showing the recorded spectra of both the VIS and IR channels in grey scale. This representation is different from that provided by the PDS Ring-Moon System Node preview images, which attempt to color-code the observations in a way that emphasizes certain important spectral ranges, including wavelengths seen by the human eye.', 'product_type': 'Extra Preview (medium)', 'product_count': 3490, 'download_count': 1765, 'download_size': 52995823, 'download_size_pretty': '50M', 'default_checked': 0}, {'slug_name': 'covims_full', 'tooltip': 'Full-size (131x69) TIFFs (*.tiff) supplied by the Cassini VIMS team, showing the recorded spectra of both the VIS and IR channels in grey scale. This representation is different from that provided by the PDS Ring-Moon System Node preview images, which attempt to color-code the observations in a way that emphasizes certain important spectral ranges, including wavelengths seen by the human eye.', 'product_type': 'Extra Preview (full)', 'product_count': 3490, 'download_count': 1765, 'download_size': 89259580, 'download_size_pretty': '85M', 'default_checked': 0}]], ['Metadata Products', [{'slug_name': 'rms_index', 'tooltip': 'Text files created by the Ring-Moon Systems Node that summarize or augment some metadata for all observations in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'RMS Node Augmented Index', 'product_count': 3492, 'download_count': 2, 'download_size': 1958899, 'download_size_pretty': '1M', 'default_checked': 0}, {'slug_name': 'supplemental_index', 'tooltip': 'Text files ([volume]_supplemental_index.tab) created by the Ring-Moon Systems Node that augment metadata for all observations in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Supplemental Index', 'product_count': 3492, 'download_count': 2, 'download_size': 1786592, 'download_size_pretty': '1M', 'default_checked': 0}, {'slug_name': 'inventory', 'tooltip': 'Text files ([volume]_inventory.csv) that list every planet and moon inside the instrument field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Target Body Inventory', 'product_count': 3492, 'download_count': 2, 'download_size': 383776, 'download_size_pretty': '374K', 'default_checked': 0}, {'slug_name': 'planet_geometry', 'tooltip': 'Text files ([volume]_[planet]_summary.tab) that list the values of various surface geometry metadata for the central planet for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Planet Geometry Index', 'product_count': 3388, 'download_count': 2, 'download_size': 1485943, 'download_size_pretty': '1M', 'default_checked': 0}, {'slug_name': 'moon_geometry', 'tooltip': 'Text files ([volume]_moon_summary.tab) that list the values of various surface geometry metadata for every moon in the field of view for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Moon Geometry Index', 'product_count': 1010, 'download_count': 2, 'download_size': 458874, 'download_size_pretty': '448K', 'default_checked': 0}, {'slug_name': 'ring_geometry', 'tooltip': 'Text files ([volume]_ring_summary.tab) that list the values of various ring plane intercept geometry metadata for every observation in a particular volume. Associated labels (*.lbl) describe the contents of the text files.', 'product_type': 'Ring Geometry Index', 'product_count': 3388, 'download_count': 2, 'download_size': 2382135, 'download_size_pretty': '2M', 'default_checked': 0}]], ['Browse Products', [{'slug_name': 'browse_thumb', 'tooltip': 'Thumbnail-size (often 100x100) non-linearly stretched preview JPEGs (*_thumb.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (thumbnail)', 'product_count': 3492, 'download_count': 1766, 'download_size': 15145336, 'download_size_pretty': '14M', 'default_checked': 0}, {'slug_name': 'browse_small', 'tooltip': 'Small-size (often 256x256) non-linearly stretched preview JPEGs (*_small.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (small)', 'product_count': 3492, 'download_count': 1766, 'download_size': 54531187, 'download_size_pretty': '52M', 'default_checked': 0}, {'slug_name': 'browse_medium', 'tooltip': 'Medium-size (often 512x512) non-linearly stretched preview JPEGs (*_med.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are colored according to the filter used. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (medium)', 'product_count': 3492, 'download_count': 1766, 'download_size': 91551761, 'download_size_pretty': '87M', 'default_checked': 0}, {'slug_name': 'browse_full', 'tooltip': 'Full-size non-linearly stretched preview JPEGs (*_full.jpg) of observations created by the Ring-Moon Systems Node. Previews of images are not colored. Previews from non-imaging instruments attempt to represent the contents of observations in a visual way. Previews are not appropriate for scientific use.', 'product_type': 'Browse Image (full)', 'product_count': 3492, 'download_count': 1766, 'download_size': 91551761, 'download_size_pretty': '87M', 'default_checked': 1}]]], 'count': 3492, 'recycled_count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 3492, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/reset.json?reqno=42&recyclebin=0'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addall_recyclebin(self):
        "[test_cart_api.py] /__cart/addall: recyclebin"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=COVIMS_0006&reqno=456'
        expected = {'recycled_count': 0, 'count': 3500, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?volumeid=COVIMS_0006&range=co-vims-v1484504505_vis,co-vims-v1484506475_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 3495, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?view=cart&range=co-vims-v1484509868_ir,co-vims-v1484510890_vis&reqno=456&recyclebin=1'
        expected = {'recycled_count': 8, 'count': 3487, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?view=cart&reqno=456' # Does nothing
        expected = {'recycled_count': 8, 'count': 3487, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?view=cart&reqno=456&recyclebin=1'
        expected = {'recycled_count': 0, 'count': 3495, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?view=cart&reqno=456&recyclebin=1'
        expected = {'recycled_count': 0, 'count': 3495, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 3495, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_too_many_2_recyclebin(self):
        "[test_cart_api.py] /__cart/add: add&remove too many 2 recyclebin"
        settings.MAX_SELECTIONS_ALLOWED = 2
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=vg-iss-2-s-c4360018&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        # Cart: vg-iss-2-s-c4360018
        url = '/__cart/add.json?opusid=co-vims-v1484509868_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        # Cart: vg-iss-2-s-c4360018, co-vims-v1484509868_ir
        url = '/__cart/add.json?opusid=co-vims-v1484510890_vis&reqno=456'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 0, 'count': 3, 'error': False, 'reqno': 456}
        else:
            expected = {'recycled_count': 0, 'count': 2, 'error': 'Your request to add OPUS ID co-vims-v1484510890_vis to the cart failed - there are already too many observations in the cart and recycle bin. The maximum allowed is 2.', 'reqno': 456}
        # LIVE:  Cart: vg-iss-2-s-c4360018, co-vims-v1484509868_ir, co-vims-v1484510890_vis
        # LOCAL: Cart: vg-iss-2-s-c4360018, co-vims-v1484509868_ir
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1484509868_ir&recyclebin=1&reqno=456'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 1, 'count': 2, 'error': False, 'reqno': 456}
        else:
            expected = {'recycled_count': 1, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        # LIVE:  Cart: vg-iss-2-s-c4360018, co-vims-v1484510890_vis RECYC: co-vims-v1484509868_ir = 3
        # LOCAL: Cart: vg-iss-2-s-c4360018                          RECYC: co-vims-v1484509868_ir = 2
        # Test add when something is in recyclebin
        url = '/__cart/add.json?opusid=co-vims-v1484510890_vis&reqno=456'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 1, 'count': 2, 'error': False, 'reqno': 456}
        else:
            expected = {'recycled_count': 1, 'count': 1, 'error': 'Your request to add OPUS ID co-vims-v1484510890_vis to the cart failed - there are already too many observations in the cart and recycle bin. The maximum allowed is 2.', 'reqno': 456}
        self._run_json_equal(url, expected)
        # LIVE:  Cart: vg-iss-2-s-c4360018, co-vims-v1484510890_vis RECYC: co-vims-v1484509868_ir = 3
        # LOCAL: Cart: vg-iss-2-s-c4360018                          RECYC: co-vims-v1484509868_ir = 2
        # Test add when something is in recyclebin
        url = '/__cart/status.json?reqno=456'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 1, 'count': 2, 'reqno': 456}
        else:
            expected = {'recycled_count': 1, 'count': 1, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_add_too_many_3_recyclebin(self):
        "[test_cart_api.py] /__cart/add: add&remove too many 3 recyclebin"
        settings.MAX_SELECTIONS_ALLOWED = 3
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=vg-iss-2-s-c4360018&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        # Cart: vg-iss-2-s-c4360018
        url = '/__cart/add.json?opusid=co-vims-v1484509868_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        # Cart: vg-iss-2-s-c4360018, co-vims-v1484509868_ir
        url = '/__cart/add.json?opusid=co-vims-v1484510890_vis&reqno=456'
        expected = {'recycled_count': 0, 'count': 3, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        # Cart: vg-iss-2-s-c4360018, co-vims-v1484509868_ir, co-vims-v1484510890_vis
        url = '/__cart/remove.json?opusid=co-vims-v1484509868_ir&recyclebin=1&reqno=456'
        expected = {'recycled_count': 1, 'count': 2, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        # Cart: vg-iss-2-s-c4360018, co-vims-v1484510890_vis RECYC: co-vims-v1484509868_ir = 3
        url = '/__cart/add.json?opusid=co-vims-v1484510890_vis&reqno=456'
        expected = {'recycled_count': 1, 'count': 2, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 1, 'count': 2, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addrange_too_many_17_recyclebin(self):
        "[test_cart_api.py] /__cart/addrange: duplicate no download too many 17 recyclebin"
        settings.MAX_SELECTIONS_ALLOWED = 17
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488642557_ir,co-vims-v1488646261_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/removerange.json?range=co-vims-v1488642557_ir,co-vims-v1488642557_ir&reqno=456&recyclebin=1'
        expected = {'recycled_count': 1, 'count': 16, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?range=vg-iss-2-s-c4360018,vg-iss-2-s-c4360018&reqno=456'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 1, 'count': 17, 'error': False, 'reqno': 456}
        else:
            expected = {'recycled_count': 1, 'count': 16, 'error': 'Your request to add 1 observations (OPUS IDs vg-iss-2-s-c4360018 to vg-iss-2-s-c4360018) to the cart failed. The resulting cart and recycle bin would have more than the maximum (17) allowed. None of the observations were added.', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1488642557_ir&reqno=456&recyclebin=0'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        else:
            expected = {'recycled_count': 0, 'count': 16, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?range=vg-iss-2-s-c4360018,vg-iss-2-s-c4360018&reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 17, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addall_too_many_906_recyclebin_2(self):
        "[test_cart_api.py] /__cart/addall: addall no download too many 906 recyclebin 2"
        settings.MAX_SELECTIONS_ALLOWED = 906
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-vims-v1488642557_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=co-vims-v1488642557_ir&reqno=456&recyclebin=1'
        expected = {'recycled_count': 1, 'count': 0, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=VGISS_6210&reqno=456'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 1, 'count': 906, 'error': False, 'reqno': 456}
        else:
            expected = {'recycled_count': 1, 'count': 0, 'error': 'Your request to add all 906 observations to the cart failed. The resulting cart and recycle bin would have more than the maximum (906) allowed. None of the observations were added.', 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        if settings.TEST_GO_LIVE:
            expected = {'recycled_count': 1, 'count': 906, 'reqno': 456}
        else:
            expected = {'recycled_count': 1, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_addall_too_many_906_recyclebin(self):
        "[test_cart_api.py] /__cart/addall: addall no download too many 906 recyclebin"
        settings.MAX_SELECTIONS_ALLOWED = 906
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=VGISS_6210&reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/remove.json?opusid=vg-iss-2-s-c4360018&reqno=456&recyclebin=1'
        expected = {'recycled_count': 1, 'count': 905, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/addall.json?volumeid=VGISS_6210&reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 906, 'reqno': 456}
        self._run_json_equal(url, expected)


            ###############################################
            ######### /__cart/data.csv: API TESTS #########
            ###############################################

    def test__api_cart_datacsv_empty(self):
        "[test_cart_api.py] /__cart/datacsv: empty"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/data.csv?cols=opusid,instrument,planet'
        expected = b'OPUS ID,Instrument Name,Planet\n'
        self._run_csv_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 456}
        self._run_json_equal(url, expected)

    def test__api_cart_datacsv_multi(self):
        "[test_cart_api.py] /__cart/datacsv: multiple"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/addrange.json?volumeid=COVIMS_0006&range=co-vims-v1488549680_ir,co-vims-v1488550102_ir&reqno=456'
        expected = {'recycled_count': 0, 'count': 3, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/data.csv?cols=opusid,instrument,planet,target,time1,observationduration,COVIMSchannel,CASSINIspacecraftclockcount1'
        expected = b'OPUS ID,Instrument Name,Planet,Intended Target Name,Observation Start Time,Observation Duration (secs),Channel [Cassini VIMS],Spacecraft Clock Start Count [Cassini]\nco-vims-v1488549680_ir,Cassini VIMS,Saturn,Saturn Rings,2005-03-03T13:34:47.689,415.577,IR,1488549680.211\nco-vims-v1488549680_vis,Cassini VIMS,Saturn,Saturn Rings,2005-03-03T13:34:47.689,415.577,VIS,1488549680.211\nco-vims-v1488550102_ir,Cassini VIMS,Saturn,Saturn Rings,2005-03-03T13:41:49.683,415.577,IR,1488550102.209\n'
        self._run_csv_equal(url, expected)
        url = '/__cart/status.json?reqno=456'
        expected = {'recycled_count': 0, 'count': 3, 'reqno': 456}
        self._run_json_equal(url, expected)


            ####################################################
            ######### /__cart/download.json: API TESTS #########
            ####################################################
    def test__api_cart_download_single_no_hierarchical_zip(self):
        "[test_cart_api.py] /__cart/download.json: single opus id & no hierarchical & fmt=zip"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=0'
        expected = ['N1462840881_1.IMG', 'N1462840881_1.LBL', 'prefix2.fmt', 'tlmtab.fmt', 'N1462840881_1_CALIB.IMG', 'N1462840881_1_CALIB.LBL', 'N1462840881_1_full.png', 'manifest.csv', 'data.csv', 'urls.txt']
        self._run_archive_file_equal(url, expected)

    def test__api_cart_download_single_no_hierarchical_tar(self):
        "[test_cart_api.py] /__cart/download.json: single opus id & no hierarchical & fmt=tar"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=0&fmt=tar'
        expected = ['N1462840881_1.IMG', 'N1462840881_1.LBL', 'prefix2.fmt', 'tlmtab.fmt', 'N1462840881_1_CALIB.IMG', 'N1462840881_1_CALIB.LBL', 'N1462840881_1_full.png', 'manifest.csv', 'data.csv', 'urls.txt']
        self._run_archive_file_equal(url, expected, fmt='tar')

    def test__api_cart_download_single_no_hierarchical_tgz(self):
        "[test_cart_api.py] /__cart/download.json: single opus id & no hierarchical & fmt=tgz"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=0&fmt=tgz'
        expected = ['N1462840881_1.IMG', 'N1462840881_1.LBL', 'prefix2.fmt', 'tlmtab.fmt', 'N1462840881_1_CALIB.IMG', 'N1462840881_1_CALIB.LBL', 'N1462840881_1_full.png', 'manifest.csv', 'data.csv', 'urls.txt']
        self._run_archive_file_equal(url, expected, fmt='tgz')

    def test__api_cart_download_single_hierarchical_zip(self):
        "[test_cart_api.py] /__cart/download.json: single opus id & hierarchical & fmt=zip"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=1'
        expected = ['volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.IMG', 'volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.LBL', 'volumes/COISS_2xxx/COISS_2002/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2002/label/tlmtab.fmt', 'calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.LBL', 'previews/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_full.png', 'manifest.csv', 'data.csv', 'urls.txt']
        self._run_archive_file_equal(url, expected)

    def test__api_cart_download_single_hierarchical_tar(self):
        "[test_cart_api.py] /__cart/download.json: single opus id & hierarchical & fmt=tar"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=1&fmt=tar'
        expected = ['volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.IMG', 'volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.LBL', 'volumes/COISS_2xxx/COISS_2002/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2002/label/tlmtab.fmt', 'calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.LBL', 'previews/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_full.png', 'manifest.csv', 'data.csv', 'urls.txt']
        self._run_archive_file_equal(url, expected, fmt='tar')

    def test__api_cart_download_single_hierarchical_tgz(self):
        "[test_cart_api.py] /__cart/download.json: single opus id & hierarchical & fmt=tgz"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=1&fmt=tgz'
        expected = ['volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.IMG', 'volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.LBL', 'volumes/COISS_2xxx/COISS_2002/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2002/label/tlmtab.fmt', 'calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.LBL', 'previews/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_full.png', 'manifest.csv', 'data.csv', 'urls.txt']
        self._run_archive_file_equal(url, expected, fmt='tgz')

    # Two opus ids (from the same volume) with duplicated prefix2.fmt & tlmtab.fmt
    def test__api_cart_download_multiple_duplicated_no_hierarchical_zip(self):
        "[test_cart_api.py] /__cart/download.json: multiple opus ids with duplicated files & no hierarchical & fmt=zip"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460973661&reqno=457'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 457}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=0'
        expected = ['N1460973661_1.IMG', 'N1460973661_1.LBL', 'N1460973661_1_CALIB.IMG', 'N1460973661_1_CALIB.LBL', 'N1460973661_1_full.png', 'N1462840881_1.IMG', 'N1462840881_1.LBL', 'N1462840881_1_CALIB.IMG', 'N1462840881_1_CALIB.LBL', 'N1462840881_1_full.png', 'data.csv', 'manifest.csv', 'prefix2.fmt', 'tlmtab.fmt', 'urls.txt']
        self._run_archive_file_equal(url, expected)

    # Two opus ids (from the same volume) with duplicated prefix2.fmt & tlmtab.fmt
    def test__api_cart_download_multiple_duplicated_no_hierarchical_tar(self):
        "[test_cart_api.py] /__cart/download.json: multiple opus ids with duplicated files & no hierarchical & fmt=tar"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460973661&reqno=457'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 457}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=0&fmt=tar'
        expected = ['N1460973661_1.IMG', 'N1460973661_1.LBL', 'N1460973661_1_CALIB.IMG', 'N1460973661_1_CALIB.LBL', 'N1460973661_1_full.png', 'N1462840881_1.IMG', 'N1462840881_1.LBL', 'N1462840881_1_CALIB.IMG', 'N1462840881_1_CALIB.LBL', 'N1462840881_1_full.png', 'data.csv', 'manifest.csv', 'prefix2.fmt', 'tlmtab.fmt', 'urls.txt']
        self._run_archive_file_equal(url, expected, fmt='tar')

    # Two opus ids (from the same volume) with duplicated prefix2.fmt & tlmtab.fmt
    def test__api_cart_download_multiple_duplicated_no_hierarchical_tgz(self):
        "[test_cart_api.py] /__cart/download.json: multiple opus ids with duplicated files & no hierarchical & fmt=tgz"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460973661&reqno=457'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 457}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=0&fmt=tgz'
        expected = ['N1460973661_1.IMG', 'N1460973661_1.LBL', 'N1460973661_1_CALIB.IMG', 'N1460973661_1_CALIB.LBL', 'N1460973661_1_full.png', 'N1462840881_1.IMG', 'N1462840881_1.LBL', 'N1462840881_1_CALIB.IMG', 'N1462840881_1_CALIB.LBL', 'N1462840881_1_full.png', 'data.csv', 'manifest.csv', 'prefix2.fmt', 'tlmtab.fmt', 'urls.txt']
        self._run_archive_file_equal(url, expected, fmt='tgz')

    # Two opus ids (from the same volume) with duplicated prefix2.fmt & tlmtab.fmt
    def test__api_cart_download_multiple_duplicated_hierarchical_zip(self):
        "[test_cart_api.py] /__cart/download.json: multiple opus ids with duplicated files & hierarchical & fmt=zip"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460973661&reqno=457'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 457}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=1'
        expected = ['calibrated/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460973661_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460973661_1_CALIB.LBL', 'calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.LBL', 'data.csv', 'manifest.csv', 'previews/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460973661_1_full.png', 'previews/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_full.png', 'urls.txt', 'volumes/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460973661_1.IMG', 'volumes/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460973661_1.LBL', 'volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.IMG', 'volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.LBL', 'volumes/COISS_2xxx/COISS_2002/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2002/label/tlmtab.fmt']
        self._run_archive_file_equal(url, expected)

    # Two opus ids (from the same volume) with duplicated prefix2.fmt & tlmtab.fmt
    def test__api_cart_download_multiple_duplicated_hierarchical_tar(self):
        "[test_cart_api.py] /__cart/download.json: multiple opus ids with duplicated files & hierarchical & fmt=tar"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460973661&reqno=457'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 457}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=1&fmt=tar'
        expected = ['calibrated/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460973661_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460973661_1_CALIB.LBL', 'calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.LBL', 'data.csv', 'manifest.csv', 'previews/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460973661_1_full.png', 'previews/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_full.png', 'urls.txt', 'volumes/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460973661_1.IMG', 'volumes/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460973661_1.LBL', 'volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.IMG', 'volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.LBL', 'volumes/COISS_2xxx/COISS_2002/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2002/label/tlmtab.fmt']
        self._run_archive_file_equal(url, expected, fmt='tar')

    # Two opus ids (from the same volume) with duplicated prefix2.fmt & tlmtab.fmt
    def test__api_cart_download_multiple_duplicated_hierarchical_tgz(self):
        "[test_cart_api.py] /__cart/download.json: multiple opus ids with duplicated files & hierarchical & fmt=tgz"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1460973661&reqno=457'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 457}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=1&fmt=tgz'
        expected = ['calibrated/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460973661_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460973661_1_CALIB.LBL', 'calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.LBL', 'data.csv', 'manifest.csv', 'previews/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460973661_1_full.png', 'previews/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_full.png', 'urls.txt', 'volumes/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460973661_1.IMG', 'volumes/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460973661_1.LBL', 'volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.IMG', 'volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.LBL', 'volumes/COISS_2xxx/COISS_2002/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2002/label/tlmtab.fmt']
        self._run_archive_file_equal(url, expected, fmt='tgz')

    # Two opus ids (from the different volumes) with not duplicated prefix2.fmt & tlmtab.fmt
    def test__api_cart_download_multiple_no_duplicated_no_hierarchical_zip(self):
        "[test_cart_api.py] /__cart/download.json: multiple opus ids without duplicated files & no hierarchical & fmt=zip"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1481265970&reqno=457'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 457}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=0'
        expected = ['N1462840881_1.IMG', 'N1462840881_1.LBL', 'N1462840881_1_CALIB.IMG', 'N1462840881_1_CALIB.LBL', 'N1462840881_1_full.png', 'N1481265970_1.IMG', 'N1481265970_1.LBL', 'N1481265970_1_CALIB.IMG', 'N1481265970_1_CALIB.LBL', 'N1481265970_1_full.png', 'data.csv', 'manifest.csv', 'urls.txt', 'volumes/COISS_2xxx/COISS_2002/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2002/label/tlmtab.fmt', 'volumes/COISS_2xxx/COISS_2008/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2008/label/tlmtab.fmt']
        self._run_archive_file_equal(url, expected)

    # Two opus ids (from the different volumes) with not duplicated prefix2.fmt & tlmtab.fmt
    def test__api_cart_download_multiple_no_duplicated_no_hierarchical_tar(self):
        "[test_cart_api.py] /__cart/download.json: multiple opus ids without duplicated files & no hierarchical & fmt=tar"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1481265970&reqno=457'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 457}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=0&fmt=tar'
        expected = ['N1462840881_1.IMG', 'N1462840881_1.LBL', 'N1462840881_1_CALIB.IMG', 'N1462840881_1_CALIB.LBL', 'N1462840881_1_full.png', 'N1481265970_1.IMG', 'N1481265970_1.LBL', 'N1481265970_1_CALIB.IMG', 'N1481265970_1_CALIB.LBL', 'N1481265970_1_full.png', 'data.csv', 'manifest.csv', 'urls.txt', 'volumes/COISS_2xxx/COISS_2002/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2002/label/tlmtab.fmt', 'volumes/COISS_2xxx/COISS_2008/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2008/label/tlmtab.fmt']
        self._run_archive_file_equal(url, expected, fmt='tar')

    # Two opus ids (from the different volumes) with not duplicated prefix2.fmt & tlmtab.fmt
    def test__api_cart_download_multiple_no_duplicated_no_hierarchical_tgz(self):
        "[test_cart_api.py] /__cart/download.json: multiple opus ids without duplicated files & no hierarchical & fmt=tgz"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1481265970&reqno=457'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 457}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=0&fmt=tgz'
        expected = ['N1462840881_1.IMG', 'N1462840881_1.LBL', 'N1462840881_1_CALIB.IMG', 'N1462840881_1_CALIB.LBL', 'N1462840881_1_full.png', 'N1481265970_1.IMG', 'N1481265970_1.LBL', 'N1481265970_1_CALIB.IMG', 'N1481265970_1_CALIB.LBL', 'N1481265970_1_full.png', 'data.csv', 'manifest.csv', 'urls.txt', 'volumes/COISS_2xxx/COISS_2002/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2002/label/tlmtab.fmt', 'volumes/COISS_2xxx/COISS_2008/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2008/label/tlmtab.fmt']
        self._run_archive_file_equal(url, expected, fmt='tgz')

    # Two opus ids (from the different volumes) with not duplicated prefix2.fmt & tlmtab.fmt
    def test__api_cart_download_multiple_no_duplicated_hierarchical_zip(self):
        "[test_cart_api.py] /__cart/download.json: multiple opus ids without duplicated files & hierarchical & fmt=zip"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1481265970&reqno=457'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 457}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=1'
        expected = ['calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.LBL', 'calibrated/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_CALIB.LBL', 'data.csv', 'manifest.csv', 'previews/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_full.png', 'previews/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_full.png', 'urls.txt', 'volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.IMG', 'volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.LBL', 'volumes/COISS_2xxx/COISS_2002/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2002/label/tlmtab.fmt', 'volumes/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1.IMG', 'volumes/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1.LBL', 'volumes/COISS_2xxx/COISS_2008/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2008/label/tlmtab.fmt']
        self._run_archive_file_equal(url, expected)

    # Two opus ids (from the different volumes) with not duplicated prefix2.fmt & tlmtab.fmt
    def test__api_cart_download_multiple_no_duplicated_hierarchical_tar(self):
        "[test_cart_api.py] /__cart/download.json: multiple opus ids without duplicated files & hierarchical & fmt=tar"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1481265970&reqno=457'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 457}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=1&fmt=tar'
        expected = ['calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.LBL', 'calibrated/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_CALIB.LBL', 'data.csv', 'manifest.csv', 'previews/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_full.png', 'previews/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_full.png', 'urls.txt', 'volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.IMG', 'volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.LBL', 'volumes/COISS_2xxx/COISS_2002/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2002/label/tlmtab.fmt', 'volumes/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1.IMG', 'volumes/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1.LBL', 'volumes/COISS_2xxx/COISS_2008/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2008/label/tlmtab.fmt']
        self._run_archive_file_equal(url, expected, fmt='tar')

    # Two opus ids (from the different volumes) with not duplicated prefix2.fmt & tlmtab.fmt
    def test__api_cart_download_multiple_no_duplicated_hierarchical_tgz(self):
        "[test_cart_api.py] /__cart/download.json: multiple opus ids without duplicated files & hierarchical & fmt=tgz"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1481265970&reqno=457'
        expected = {'recycled_count': 0, 'count': 2, 'error': False, 'reqno': 457}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=1&fmt=tgz'
        expected = ['calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_CALIB.LBL', 'calibrated/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_CALIB.LBL', 'data.csv', 'manifest.csv', 'previews/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1_full.png', 'previews/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_full.png', 'urls.txt', 'volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.IMG', 'volumes/COISS_2xxx/COISS_2002/data/1462783195_1462915477/N1462840881_1.LBL', 'volumes/COISS_2xxx/COISS_2002/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2002/label/tlmtab.fmt', 'volumes/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1.IMG', 'volumes/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1.LBL', 'volumes/COISS_2xxx/COISS_2008/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2008/label/tlmtab.fmt']
        self._run_archive_file_equal(url, expected, fmt='tgz')

    # Unsupported format
    def test__api_cart_download_unsupported_format(self):
        "[test_cart_api.py] /__cart/download.json: fmt=xxx not supported"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__cart/add.json?opusid=co-iss-n1462840881&reqno=456'
        expected = {'recycled_count': 0, 'count': 1, 'error': False, 'reqno': 456}
        self._run_json_equal(url, expected)
        url = '/__cart/download.json?types=coiss_raw,coiss_calib,browse_full&hierarchical=0&fmt=xxx'
        self._run_status_equal(url, 404,
                               HTTP404_UNKNOWN_DOWNLOAD_FILE_FORMAT('xxx', '/__cart/download.json'))

            ###########################################################
            ######### /api/download/<opusid>.<fmt>: API TESTS #########
            ###########################################################
    def test__api_download_no_hierarchical_zip(self):
        "[test_cart_api.py] /__api/download/<opusid>.zip: one opus id & no hierarchical"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__api/download/co-iss-n1481265970.zip?types=coiss_raw,coiss_calib,browse_full&hierarchical=0'
        expected = ['N1481265970_1.IMG', 'N1481265970_1.LBL', 'N1481265970_1_CALIB.IMG', 'N1481265970_1_CALIB.LBL', 'N1481265970_1_full.png', 'data.csv', 'manifest.csv', 'prefix2.fmt', 'tlmtab.fmt', 'urls.txt']
        self._run_archive_file_equal(url, expected, response_type='binary')

    def test__api_download_no_hierarchical_tar(self):
        "[test_cart_api.py] /__api/download/<opusid>.tar: one opus id & no hierarchical"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__api/download/co-iss-n1481265970.tar?types=coiss_raw,coiss_calib,browse_full&hierarchical=0'
        expected = ['N1481265970_1.IMG', 'N1481265970_1.LBL', 'N1481265970_1_CALIB.IMG', 'N1481265970_1_CALIB.LBL', 'N1481265970_1_full.png', 'data.csv', 'manifest.csv', 'prefix2.fmt', 'tlmtab.fmt', 'urls.txt']
        self._run_archive_file_equal(url, expected, response_type='binary', fmt='tar')

    def test__api_download_no_hierarchical_tgz(self):
        "[test_cart_api.py] /__api/download/<opusid>.tgz: one opus id & no hierarchical"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__api/download/co-iss-n1481265970.tgz?types=coiss_raw,coiss_calib,browse_full&hierarchical=0'
        expected = ['N1481265970_1.IMG', 'N1481265970_1.LBL', 'N1481265970_1_CALIB.IMG', 'N1481265970_1_CALIB.LBL', 'N1481265970_1_full.png', 'data.csv', 'manifest.csv', 'prefix2.fmt', 'tlmtab.fmt', 'urls.txt']
        self._run_archive_file_equal(url, expected, response_type='binary', fmt='tgz')

    def test__api_download_hierarchical_zip(self):
        "[test_cart_api.py] /__api/download/<opusid>.zip: one opus id & hierarchical"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__api/download/co-iss-n1481265970.zip?types=coiss_raw,coiss_calib,browse_full&hierarchical=1'
        expected = ['calibrated/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_CALIB.LBL', 'data.csv', 'manifest.csv', 'previews/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_full.png', 'urls.txt', 'volumes/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1.IMG', 'volumes/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1.LBL', 'volumes/COISS_2xxx/COISS_2008/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2008/label/tlmtab.fmt']
        self._run_archive_file_equal(url, expected, response_type='binary')

    def test__api_download_hierarchical_tar(self):
        "[test_cart_api.py] /__api/download/<opusid>.tar: one opus id & hierarchical"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__api/download/co-iss-n1481265970.tar?types=coiss_raw,coiss_calib,browse_full&hierarchical=1'
        expected = ['calibrated/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_CALIB.LBL', 'data.csv', 'manifest.csv', 'previews/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_full.png', 'urls.txt', 'volumes/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1.IMG', 'volumes/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1.LBL', 'volumes/COISS_2xxx/COISS_2008/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2008/label/tlmtab.fmt']
        self._run_archive_file_equal(url, expected, response_type='binary', fmt='tar')

    def test__api_download_hierarchical_tgz(self):
        "[test_cart_api.py] /__api/download/<opusid>.tgz: one opus id & hierarchical"
        url = '/__cart/reset.json?reqno=42'
        expected = {'recycled_count': 0, 'count': 0, 'reqno': 42}
        self._run_json_equal(url, expected)
        url = '/__api/download/co-iss-n1481265970.tgz?types=coiss_raw,coiss_calib,browse_full&hierarchical=1'
        expected = ['calibrated/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_CALIB.IMG', 'calibrated/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_CALIB.LBL', 'data.csv', 'manifest.csv', 'previews/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1_full.png', 'urls.txt', 'volumes/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1.IMG', 'volumes/COISS_2xxx/COISS_2008/data/1481264980_1481267140/N1481265970_1.LBL', 'volumes/COISS_2xxx/COISS_2008/label/prefix2.fmt', 'volumes/COISS_2xxx/COISS_2008/label/tlmtab.fmt']
        self._run_archive_file_equal(url, expected, response_type='binary', fmt='tgz')


            ################################################
            ######### /__cart/view.html: API TESTS #########
            ################################################

    # XXX Need to implement tests

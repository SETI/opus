"""
if you run this locally:

be sure and delete all from user_searches before you build the 'search' fixture
otherwise your cache_x table names will never match
reset the auto_increment too.. DO THIS:

delete from user_searches;
ALTER TABLE user_searches AUTO_INCREMENT = 1;
analyze table user_searches;

*****************************
"""
# from django.test import TestCase  removed because it deletes test table data after every test
from unittest import TestCase
from django.test.client import Client
from django.db.models import get_model

from search.views import *
from results.views import *
from django.http import QueryDict

from django.conf import settings
settings.CACHE_BACKEND = 'dummy:///'

cursor = connection.cursor()

class searchTests(TestCase):

    # setup
    c = Client()
    param_name = 'obs_general.planet_id'
    selections = {}
    selections[param_name] = ['Saturn']
    extras = {}

    def teardown(self):
        cursor = connection.cursor()
        cursor.execute("delete from user_searches")
        cursor.execute("ALTER TABLE user_searches AUTO_INCREMENT = 1")
        cursor.execute("show tables like %s " , ["cache%"])
        print "running teardown"
        for row in cursor:
            q = 'drop table ' + row[0]
            print q
            cursor.execute(q)


    def test__constructQueryString_string(self):
        selections = {'obs_general.primary_file_spec': ['C11399XX']}
        sql, params = constructQueryString(selections, {})
        q = sql % params
        print q
        expected = "SELECT `obs_general`.`id` FROM `obs_general` WHERE `obs_general`.`primary_file_spec` LIKE %C11399XX%"
        self.assertEqual("".join(q.split()),"".join(expected.split()))  # strips all whitespace b4 compare

    def test__constructQueryString_single_column_range(self):
        selections = {u'obs_ring_geometry.ring_center_phase1': [20.0], u'obs_ring_geometry.ring_center_phase2': [180.0]}
        sql, params = constructQueryString(selections, {})
        q = sql % params
        print q
        expected = "SELECT `obs_general`.`id` FROM `obs_general` INNER JOIN `obs_ring_geometry` ON ( `obs_general`.`id` = `obs_ring_geometry`.`obs_general_id` ) WHERE (`obs_ring_geometry`.`ring_center_phase` <= 180.0  AND `obs_ring_geometry`.`ring_center_phase` >= 20.0 )"
        self.assertEqual("".join(q.split()),"".join(expected.split()))  # strips all whitespace b4 compare

    def test__constructQueryString_string_with_qtype(self):
        selections = {'obs_general.primary_file_spec': ['C11399XX']}
        extras = {'qtypes': {'obs_general.primary_file_spec': ['contains']}}
        sql, params = constructQueryString(selections, extras)
        q = sql % params

        print q
        expected = "SELECT `obs_general`.`id` FROM `obs_general` WHERE `obs_general`.`primary_file_spec` LIKE %C11399XX%"
        self.assertEqual("".join(q.split()),"".join(expected.split()))  # strips all whitespace b4 compare

    def test__constructQueryString_string_with_joined_table(self):
        selections = {'obs_general.instrument_id': ['COISS']}
        selections['obs_mission_cassini.obs_name'] = ['RDCOLSCNM']
        extras = {'qtypes': {'obs_mission_cassini.obs_name': ['contains']}}
        sql, params = constructQueryString(selections, extras)
        q = sql % params

        print q
        expected = "SELECT `obs_general`.`id` FROM `obs_general` INNER JOIN `obs_mission_cassini` ON ( `obs_general`.`id` = `obs_mission_cassini`.`obs_general_id` ) WHERE (`obs_mission_cassini`.`obs_name` LIKE %RDCOLSCNM%  AND `obs_general`.`mult_obs_general_instrument_id` IN (2))"
        self.assertEqual("".join(q.split()),"".join(expected.split()))  # strips all whitespace b4 compare


    ## constructQueryString
    def test__constructQueryString_mults_planet(self):
        sql, params = constructQueryString(self.selections, self.extras)
        q = sql % params
        print q
        expected = "SELECT `obs_general`.`id` FROM `obs_general` WHERE `obs_general`.`mult_obs_general_planet_id` IN (7)"
        self.assertEqual("".join(q.split()),"".join(expected.split()))  # strips all whitespace b4 compare

    def test__constructQueryString_range_single_qtype(self):
        q = QueryDict("ringradius1=60000&ringradius2=80000,120000&qtype-ringradius=all")
        selections, extras = urlToSearchParams(q)
        sql, params = constructQueryString(selections, extras)
        q = sql % params
        print 'extras: '
        print q
        expected = "SELECT `obs_general`.`id` FROM `obs_general` INNER JOIN `obs_ring_geometry` ON (`obs_general`.`id` = `obs_ring_geometry`.`obs_general_id`) \
                    WHERE ((`obs_ring_geometry`.`ring_radius1` <= 60000.0  AND `obs_ring_geometry`.`ring_radius2` >= 80000.0 ) OR `obs_ring_geometry`.`ring_radius2` >= 120000.0 )"
        print 'expected:'
        print expected
        self.assertEqual("".join(q.split()),"".join(expected.split()))  # strips all whitespace b4 compare

    def test__constructQueryString_mults_planet_instrumentCOISS(self):
        selections = {}
        selections['obs_general.planet_id'] = ['Saturn']
        selections['obs_general.instrument_id'] = ['COISS']
        sql, params = constructQueryString(selections, {})
        q = sql % params
        print q
        expected = "SELECT `obs_general`.`id` FROM `obs_general` WHERE (`obs_general`.`mult_obs_general_planet_id` IN (7) AND `obs_general`.`mult_obs_general_instrument_id` IN (2))"
        self.assertEqual("".join(q.split()),"".join(expected.split()))  # strips all whitespace b4 compare

    def test__constructQueryString_mults_with_target(self):
        selections = {}
        selections['obs_general.planet_id'] = ["Saturn"]
        selections['obs_general.target_name'] = ["PAN"]
        sql, params = constructQueryString(selections, {})
        q = sql % params
        print q
        expected = "SELECT `obs_general`.`id` FROM `obs_general` WHERE (`obs_general`.`mult_obs_general_target_name` IN (42) AND `obs_general`.`mult_obs_general_planet_id` IN (7))"
        self.assertEqual("".join(q.split()),"".join(expected.split()))  # strips all whitespace b4 compare

    def test__constructQueryString_mults_with_join(self):
        selections = {}
        selections['obs_general.planet_id'] = ["Saturn"]
        selections['obs_instrument_COISS.camera'] = ["Wide Angle"]
        sql, params = constructQueryString(selections, {})
        q = sql % params
        print q
        expected = "SELECT `obs_general`.`id` FROM `obs_general` INNER JOIN `obs_instrument_COISS` ON (`obs_general`.`id` = `obs_instrument_COISS`.`obs_general_id`) WHERE (`obs_general`.`mult_obs_general_planet_id` IN (7) AND `obs_instrument_COISS`.`mult_obs_instrument_COISS_camera` IN (1))"
        print q
        print 'expected:'
        print expected
        self.assertEqual("".join(q.split()),"".join(expected.split()))  # strips all whitespace b4 compare

    def test__constructQueryString_mults_with_3_table_join(self):
        selections = {}
        selections['obs_general.planet_id'] = ["Saturn"]
        selections['obs_general.target_name'] = ["PAN"]
        selections['obs_instrument_COISS.camera'] = ["Narrow Angle"]
        selections['obs_mission_cassini.rev_no'] = ['165','166']
        sql, params = constructQueryString(selections, {})
        q = sql % params
        print q
        expected = "SELECT `obs_general`.`id` FROM `obs_general` INNER JOIN `obs_mission_cassini` ON ( `obs_general`.`id` = `obs_mission_cassini`.`obs_general_id` ) INNER JOIN `obs_instrument_COISS` ON ( `obs_general`.`id` = `obs_instrument_COISS`.`obs_general_id` ) WHERE (`obs_general`.`mult_obs_general_target_name` IN (42) AND `obs_general`.`mult_obs_general_planet_id` IN (7) AND `obs_mission_cassini`.`mult_obs_mission_cassini_rev_no` IN (289, 290) AND `obs_instrument_COISS`.`mult_obs_instrument_COISS_camera` IN (2))"
        print 'expected:'
        print expected
        self.assertEqual(q,expected)




    ## getUserQueryTable

    def test__getUserQueryTable(self):
        self.teardown()
        # simple base join types only
        table = getUserQueryTable(self.selections)
        print "table = " + str(table) + "\n" + str(self.selections)
        self.assertEqual(table.split('_')[0],'cache')

    def test__getUserQueryTable_with_times(self):
        selections = {u'obs_general.planet_id': [u'Saturn'], u'obs_general.time_sec2': [u'2009-12-28'], u'obs_general.time_sec1': [u'2009-12-23']}
        table = getUserQueryTable(selections)
        print table
        self.assertGreater(len(table), 0)

    def test__getUserQueryTable_table_already_exists(self):
        # the 2nd time through you're testing whether it returns the table that is already there
        table = getUserQueryTable(self.selections)
        self.assertEqual(table.split('_')[0],'cache')


    ## test urlToSearchParam
    def test__urlToSearchParams_single_column_range(self):
        q = QueryDict('ringcenterphase1=20&ringcenterphase2=180')
        (selections,extras) = urlToSearchParams(q)
        expected = {u'obs_ring_geometry.ring_center_phase1': [20.0], u'obs_ring_geometry.ring_center_phase2': [180.0]}
        print selections
        self.assertEqual(selections,expected)

    def test__urlToSearchParams_times(self):
        q = QueryDict('planet=Saturn&timesec1=2000-023T06:00&timesec2=2000-024T06:00')
        (selections,extras) = urlToSearchParams(q)
        expected = {u'obs_general.planet_id': [u'Saturn'], u'obs_general.time_sec2': [u'2000-024T06:00'], u'obs_general.time_sec1': [u'2000-023T06:00']}
        print selections
        self.assertEqual(selections,expected)

    def test__urlToSearchParams_from_url_one_sided(self):
        q = QueryDict("planet=Saturn&instrumentid=Cassini+ISS&phase1=80&phase2=")
        (selections,extras) = urlToSearchParams(q)
        expected = {u'obs_general.planet_id': [u'Saturn'], u'obs_general.instrument_id': [u'Cassini ISS'], u'obs_ring_geometry.phase1': [80.0]}
        print selections
        self.assertEqual(selections,expected)

    def test__urlToSearchParams_time(self):
        q = QueryDict("planet=Saturn&timesec1=2000-023T06&timesec2=2000-024T06")
        result = urlToSearchParams(q)
        print result
        self.assertEqual(result,[{u'obs_general.planet_id': [u'Saturn'], u'obs_general.time_sec2': [u'2000-024T06'], u'obs_general.time_sec1': [u'2000-023T06']}, {'qtypes': {}}])

    def test__urlToSearchParams_Any_Not_All_Strings_One_Side(self):
        q = QueryDict("planet=Saturn&instrumentid=Cassini+ISS&phase1=80&phase2=")
        result = urlToSearchParams(q)
        print result
        self.assertEqual(result,[{u'obs_general.planet_id': [u'Saturn'], u'obs_general.instrument_id': [u'Cassini ISS'], u'obs_ring_geometry.phase1': [80]}, {'qtypes': {}}])

    def test__urlToSearchParams_Not_All_Strings(self):
        q = QueryDict("planet=Saturn&instrumentid=Cassini+ISS&phase1=80&phase2=165")
        result = urlToSearchParams(q)
        print result
        self.assertEqual(result,[{u'obs_general.planet_id': [u'Saturn'], u'obs_general.instrument_id': [u'Cassini ISS'], u'obs_ring_geometry.phase1': [80], u'obs_ring_geometry.phase2': [165]}, {'qtypes': {}}])

    def test__urlToSearchParams_stringsearch(self):
        q = QueryDict("note=Incomplete")
        result = urlToSearchParams(q)
        print result
        self.assertEqual(result,[{u'obs_general.note': [u'Incomplete']}, {'qtypes': {}}])

    def test__urlToSearchParams_range_single_qtype(self):
        q = QueryDict("ringradius1=60000&ringradius2=80000,120000&qtype-ringradius=all")
        result = urlToSearchParams(q)
        print result
        expected = [{u'obs_ring_geometry.ring_radius2': [80000.0, 120000.0], u'obs_ring_geometry.ring_radius1': [60000.0]}, {'qtypes': {u'obs_ring_geometry.ring_radius': [u'all']}}]
        self.assertEqual(result,expected)


    def test__urlToSearchParams_mults(self):
        q = QueryDict("planet=SATURN&target=PAN")
        result = urlToSearchParams(q)
        self.assertEqual(result,[{u'obs_general.target_name': [u'PAN'], u'obs_general.planet_id': [u'SATURN']}, {'qtypes': {}}])

    def test__urlToSearchParams_mults_instrument(self):
        q = QueryDict("planet=SATURN&instrumentid=COISS")
        result = urlToSearchParams(q)
        self.assertEqual(result,[{u'obs_general.instrument_id': [u'COISS'], u'obs_general.planet_id': [u'SATURN']}, {'qtypes': {}}])

    def test__urlToSearchParams_with_join(self):
        q = QueryDict("planet=Saturn&ringradius1=60000")
        result = urlToSearchParams(q)
        self.assertEqual(result,[{u'obs_general.planet_id': [u'Saturn'], u'obs_ring_geometry.ring_radius1': [60000]}, {'qtypes': {}}])


    def test__urlToSearchParams_stringmultmix(self):
        q = QueryDict("planet=SATURN&target=PAN&note=Incomplete&qtype-note=contains")
        result = urlToSearchParams(q)
        # setup assert:
        excpected = [{u'obs_general.note': [u'Incomplete'], u'obs_general.planet_id': [u'SATURN'], u'obs_general.target_name': [u'PAN']}, {'qtypes': {u'obs_general.note': [u'contains']}}]
        self.assertEqual(result,excpected)

    def test__urlToSearchParams_mix_with_note(self):
        q = QueryDict('planet=Jupiter&note=Manually,Incomplete&qtype-note=contains,begins')
        result = urlToSearchParams(q)
        print result
        expected = [{u'obs_general.planet_id': [u'Jupiter'], u'obs_general.note': [u'Manually', u'Incomplete']}, {'qtypes': {u'obs_general.note': [u'contains', u'begins']}}]
        self.assertEqual(result,expected)

    def test__urlToSearchParams_ring_rad_rangea(self):
        q = QueryDict("ringradius1=60000&ringradius2=80000")
        result = urlToSearchParams(q)
        # setup assert:
        selections = {}
        extras={}
        qtypes = {}
        selections['obs_ring_geometry.ring_radius1'] = [60000]
        selections['obs_ring_geometry.ring_radius2'] = [80000]
        extras['qtypes'] = qtypes
        self.assertEqual(result,[selections,extras])


    ##  setUserSearchNo
    def test__setUserSearchNo(self):
        no = setUserSearchNo(self.selections)
        self.assertTrue(no)

    def test__setUserSearchNo_with_times(self):
        selections = {u'obs_general.planet_id': [u'Saturn'], u'obs_general.time_sec2': [u'2009-12-28'], u'obs_general.time_sec1': [u'2009-12-23']}
        search_no = setUserSearchNo(selections)
        print search_no
        self.assertGreater(len(str(search_no)), 0)


    def test__setUserSearchNo_2_planets(self):
        selections = {}
        selections['obs_general.planet_id'] = ['Saturn']
        no = setUserSearchNo(selections)
        print no
        # breaking this, this test needs to see if there are any rows in the table
        self.assertGreater(no, 0)
        self.teardown()


    ##  Range Query tests


    def test_range_query_single_col_range_all(self):
        selections = {u'obs_ring_geometry.ring_center_phase1': [20.0], u'obs_ring_geometry.ring_center_phase2': [180.0]}
        q = str(range_query_object(selections,'obs_ring_geometry.ring_center_phase1',['all']))
        print q
        expected = "(AND: (u'obsringgeometry__ring_center_phase__lte', 20.0), (u'obsringgeometry__ring_center_phase__gte', 180.0))"
        print expected
        self.assertEqual("".join(q.split()),"".join(expected.split()))  # strips all whitespace b4 compare

    def test_range_query_any_times(self):
        selections = {u'obs_general.planet_id': [u'Saturn'], u'obs_general.time_sec2': [u'2000-024'], u'obs_general.time_sec1': [u'2000-023']}
        q = str(range_query_object(selections,'obs_general.time_sec1',['any']))
        print q
        expected = "(AND: ('time_sec1__lte', 1987232.0), ('time_sec2__gte', 1900832.0))"
        print expected
        self.assertEqual("".join(q.split()),"".join(expected.split()))  # strips all whitespace b4 compare


    def test__range_query_any(self):
        # range query: 'any'
        selections = {}
        selections['obs_ring_geometry.ring_radius1'] = [10000]
        selections['obs_ring_geometry.ring_radius2'] = [40000]
        q = range_query_object(selections,'obs_ring_geometry.ring_radius1',['any'])
        print str(q)
        self.assertEqual(str(q),"(AND: (u'obsringgeometry__ring_radius1__lte', 40000), (u'obsringgeometry__ring_radius2__gte', 10000))")

    def test__range_query_only(self):
        # range query: 'only'
        selections = {}
        selections['obs_ring_geometry.ring_radius1'] = [10000]
        selections['obs_ring_geometry.ring_radius2'] = [40000]
        q = range_query_object(selections,'obs_ring_geometry.ring_radius1',['only'])
        print str(q)
        self.assertEqual(str(q), "(AND: (u'obsringgeometry__ring_radius1__gte', 10000), (u'obsringgeometry__ring_radius2__lte', 40000))")

    def test__range_query_all(self):
        # range query: 'all'
        selections = {}
        selections['obs_ring_geometry.ring_radius1'] = [10000]
        selections['obs_ring_geometry.ring_radius2'] = [40000]
        q = range_query_object(selections,'obs_ring_geometry.ring_radius1',['all'])
        print str(q)
        self.assertEqual(str(q), "(AND: (u'obsringgeometry__ring_radius1__lte', 10000), (u'obsringgeometry__ring_radius2__gte', 40000))")

    def test__range_query_multi(self):
        # range query: multi
        selections = {}
        selections['obs_ring_geometry.ring_radius1'] = [10000,60000]
        selections['obs_ring_geometry.ring_radius2'] = [40000,80000]
        q = range_query_object(selections,'obs_ring_geometry.ring_radius1',['all'])
        print str(q)
        self.assertEqual(str(q), "(OR: (AND: (u'obsringgeometry__ring_radius1__lte', 10000), (u'obsringgeometry__ring_radius2__gte', 40000)), (AND: (u'obsringgeometry__ring_radius1__lte', 60000), (u'obsringgeometry__ring_radius2__gte', 80000)))")

    def test__range_query_ordered_backwards(self):
        # range query: ordered backwards
        selections = {}
        selections['obs_ring_geometry.ring_radius1'] = [40000,60000]
        selections['obs_ring_geometry.ring_radius2'] = [10000,80000]
        q = range_query_object(selections,'obs_ring_geometry.ring_radius1',['all'])
        print str(q)
        self.assertEqual(str(q), "(OR: (AND: (u'obsringgeometry__ring_radius1__lte', 10000), (u'obsringgeometry__ring_radius2__gte', 40000)), (AND: (u'obsringgeometry__ring_radius1__lte', 60000), (u'obsringgeometry__ring_radius2__gte', 80000)))")


    def test__range_query_ordered_lopsided_all(self):
        # range query: lopsided all
        selections = {}
        selections['obs_ring_geometry.ring_radius1'] = [40000]
        q = range_query_object(selections,'obs_ring_geometry.ring_radius1',['all'])
        print str(q)
        self.assertEqual(str(q), "(AND: (u'obsringgeometry__ring_radius1__lte', 40000))")


    def test__range_query_ordered_lopsided_all_max(self):
        # range query: lopsided all max
        selections = {}
        selections['obs_ring_geometry.ring_radius2'] = [40000]
        q = range_query_object(selections,'obs_ring_geometry.ring_radius2',['all'])
        print str(q)
        self.assertEqual(str(q), "(AND: (u'obsringgeometry__ring_radius2__gte', 40000))")
        """
        self.assertEqual(q,'(obs_ring_geometry.ring_radius2 >= %s)')
        self.assertEqual(v,[40000])
        """

    def test__range_query_lopsided_only_min(self):
        # range query: lopsided only min
        selections = {}
        selections['obs_ring_geometry.ring_radius1'] = [40000]
        q = range_query_object(selections,'obs_ring_geometry.ring_radius1',['only'])
        print str(q)
        self.assertEqual(str(q), "(AND: (u'obsringgeometry__ring_radius1__gte', 40000))")


    def test__range_query_lopsided_only_max(self):
        # range query: lopsided only max
        selections = {}
        selections['obs_ring_geometry.ring_radius2'] = [40000]
        q = range_query_object(selections,'obs_ring_geometry.ring_radius2',['only'])
        print str(q)
        # (ring_radius2 <= 4000
        self.assertEqual(str(q), "(AND: (u'obsringgeometry__ring_radius2__lte', 40000))")

    def test__range_query_lopsided_any_min(self):
        # range query: lopsided any min
        selections = {}
        selections['obs_ring_geometry.ring_radius1'] = [40000]
        q = range_query_object(selections,'obs_ring_geometry.ring_radius1',['any'])
        print str(q)
        # ring_radius2 >= %s
        self.assertEqual(str(q), "(AND: (u'obsringgeometry__ring_radius2__gte', 40000))")

    def test__range_query_lopsided_any_max(self):
        # range query: lopsided any min
        selections = {}
        selections['obs_ring_geometry.ring_radius2'] = [40000]
        q = range_query_object(selections,'obs_ring_geometry.ring_radius2',['any'])
        print str(q)
        self.assertEqual(str(q), "(AND: (u'obsringgeometry__ring_radius1__lte', 40000))")

    def test__range_query_lopsided_multi_mixed_q_types(self):
        # range query: multi range, 1 is lopsided, mixed qtypes
        selections = {}
        selections['obs_ring_geometry.ring_radius1'] = [40000,80000]
        selections['obs_ring_geometry.ring_radius2'] = [60000]
        q = range_query_object(selections,'obs_ring_geometry.ring_radius2',['any','only'])
        print str(q)
        # (ring_radius1 <= 6000 AND ring_radius2 >= 40000) OR (ring_radius2 >= 80000)
        self.assertEqual(str(q),"(OR: (AND: (u'obsringgeometry__ring_radius1__lte', 60000), (u'obsringgeometry__ring_radius2__gte', 40000)), (u'obsringgeometry__ring_radius1__gte', 80000))")

    def test__range_query_lopsided_multi_mixed_only_one_q_type(self):
        # range query: multi range, 1 is lopsided, mixed only 1 qtype given
        selections = {}
        selections['obs_ring_geometry.ring_radius1'] = [40000,80000]
        selections['obs_ring_geometry.ring_radius2'] = [60000]
        q = range_query_object(selections,'obs_ring_geometry.ring_radius2',['any'])
        print str(q)
        # (ring_radius1 <= 6000 AND ring_radius2 >= 40000) OR (ring_radius2 >= 80000)
        self.assertEqual(str(q),"(OR: (AND: (u'obsringgeometry__ring_radius1__lte', 60000), (u'obsringgeometry__ring_radius2__gte', 40000)), (u'obsringgeometry__ring_radius2__gte', 80000))")


    ## Time  tests
    def test__convertTimes_shorties(self):
        # test times
        times     = ['2000-023T06:00','2000-024T06:00']
        new_times = convertTimes(times)
        print times
        print new_times
        self.assertEqual(new_times,[1922432, 2008832])

    def test__convertTimes(self):
        # test times
        times     = ['2000-023T06:12:24.480','2000-024T06:12:24.480']
        new_times = convertTimes(times)
        print times
        print new_times
        self.assertEqual(new_times,[1923176.48, 2009576.48])

    def test__convertTimes2(self):
        times     = ['2000-023T06:12:24.480','cats']
        new_times = convertTimes(times)
        self.assertEqual(new_times,[1923176.48, None])


    def test__range_query_time_any(self):
        # range query: form type = TIME, qtype any
        selections = {}
        selections['obs_general.time_sec1'] = ['1979-05-28T10:17:37.28']
        selections['obs_general.time_sec2'] = ['1979-05-29T18:22:26']
        q = str(range_query_object(selections,'obs_general.time_sec1',['any']))
        print q
        # time_sec1 <= -649993324.720000 AND time_sec2 >= -649877836.000000
        expected = "(AND: ('time_sec1__lte', -649834636.0), ('time_sec2__gte', -649950124.72000003))"
        print 'expected:'
        print expected
        self.assertEqual("".join(q.split()),"".join(expected.split()))  # strips all whitespace b4 compare


    def test__range_query_time_any_single_time(self):
        # range query: form type = TIME, qtype any
        selections = {}
        selections['obs_general.time_sec1'] = ['1979-05-28T10:17:37.28']
        q = str(range_query_object(selections,'obs_general.time_sec1',['any']))
        print str(q)
        # time_sec2 >= -649993324.720000
        expected = "(AND: ('time_sec2__gte', -649950124.72000003))"
        self.assertEqual("".join(q.split()),"".join(expected.split()))  # strips all whitespace b4 compare

    ## longitude query tests
    def test__longitudeQuery_single_obs_general(self):
        #single longitude set
        selections = {}
        selections['obs_general.declination1'] = [58]
        selections['obs_general.declination2'] = [61]
        sql, params = longitudeQuery(selections,'obs_general.declination1')
        sql, params = constructQueryString(selections, {})
        q = sql % params
        print q
        expect = 'SELECT `obs_general`.`id` FROM `obs_general` where obs_general.id in  (select obs_general.id from obs_general where (abs(abs(mod(59.5 - obs_general.declination + 180., 360.)) - 180.) <= 1.5 + obs_general.d_declination))'
        self.assertEqual(''.join(q.split()),''.join(expect.split()))

    def test__longitudeQuery_double(self):
        # double
        selections = {}
        selections['obs_general.declination1'] = [5]
        selections['obs_general.declination2'] = [61]
        selections['obs_ring_geometry.J2000_longitude1'] = [5]
        selections['obs_ring_geometry.J2000_longitude2'] = [255]
        sql, params = constructQueryString(selections, {})
        q = sql % params
        print q
        expect = "SELECT `obs_general`.`id` FROM `obs_general` where obs_general.id in  (select obs_general.id from obs_general where (abs(abs(mod(130.0 - obs_general.declination + 180., 360.)) - 180.) <= 125.0 + obs_general.d_declination))  AND obs_general.id in  (select obs_general_id from obs_ring_geometry where (abs(abs(mod(130.0 - obs_ring_geometry.J2000_longitude + 180., 360.)) - 180.) <= 125.0 + obs_ring_geometry.d_J2000_longitude))"
        self.assertEqual(''.join(q.split()),''.join(expect.split()))

    def test__longitudeQuery_ring_geo(self):
        # double
        selections = {}
        selections['obs_ring_geometry.J2000_longitude1'] = [5]
        selections['obs_ring_geometry.J2000_longitude2'] = [255]
        sql, params = constructQueryString(selections, {})
        q = sql % params
        print q
        expect = "SELECT `obs_general`.`id` FROM `obs_general` where obs_general.id in  (select obs_general_id from obs_ring_geometry where (abs(abs(mod(130.0 - obs_ring_geometry.J2000_longitude + 180., 360.)) - 180.) <= 125.0 + obs_ring_geometry.d_J2000_longitude))"
        self.assertEqual(''.join(q.split()),''.join(expect.split()))

    def test__longitudeQuery_one_side(self):
        # missing value raises exception
        selections = {}
        selections['obs_general.declination1'] = [58]
        # self.assertRaises(IndexError, longitudeQuery(selections,'declination1'))
        try:
            sql, params = longitudeQuery(selections,'obs_general.declination1')
        except KeyError, IndexError:
            pass

    def test__longitudeQuery_other_side(self):
        # missing value raises exception
        selections = {}
        selections['obs_general.declination2'] = [58]
        # self.assertRaises(IndexError, longitudeQuery(selections,'declination1'))
        try:
            sql, params = longitudeQuery(selections,'obs_general.declination1')
        except KeyError, IndexError:
            pass

    def test__longitudeQuery_lop_sided(self):
        # missing value raises exception
        selections = {}
        selections['obs_general.declination1'] = [58,75]
        selections['obs_general.declination2'] = [61]
        # self.assertRaises(IndexError, longitudeQuery(selections,'declination1'))
        try:
            sql, params = longitudeQuery(selections,'obs_general.declination1')
        except KeyError, IndexError:
            pass




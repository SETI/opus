# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class ZZGroupingTargetName(models.Model):
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=30, blank=True, null=True)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'grouping_target_name'


class MultObsGeneralInstHostId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_general_inst_host_id'


class MultObsGeneralInstrumentId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_general_instrument_id'


class MultObsGeneralMissionId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_general_mission_id'


class MultObsGeneralPlanetId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_general_planet_id'


class MultObsGeneralQuantity(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_general_quantity'


class MultObsGeneralSpatialSampling(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_general_spatial_sampling'


class MultObsGeneralTargetClass(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_general_target_class'


class MultObsGeneralTargetName(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=30)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    grouping = models.CharField(max_length=7, blank=True, null=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_general_target_name'


class MultObsGeneralTimeSampling(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_general_time_sampling'


class MultObsGeneralWavelengthSampling(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_general_wavelength_sampling'


class MultObsInstrumentCoissCamera(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_coiss_camera'


class MultObsInstrumentCoissCombinedFilter(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_coiss_combined_filter'


class MultObsInstrumentCoissCompressionType(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_coiss_compression_type'


class MultObsInstrumentCoissDataConversionType(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_coiss_data_conversion_type'


class MultObsInstrumentCoissGainModeId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_coiss_gain_mode_id'


class MultObsInstrumentCoissImageObservationType(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_coiss_image_observation_type'


class MultObsInstrumentCoissInstrumentModeId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_coiss_instrument_mode_id'


class MultObsInstrumentCoissShutterModeId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_coiss_shutter_mode_id'


class MultObsInstrumentCoissShutterStateId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_coiss_shutter_state_id'


class MultObsInstrumentCouvisChannel(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_couvis_channel'


class MultObsInstrumentCouvisCompressionType(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_couvis_compression_type'


class MultObsInstrumentCouvisDwellTime(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_couvis_dwell_time'


class MultObsInstrumentCouvisObservationType(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_couvis_observation_type'


class MultObsInstrumentCouvisOccultationPortState(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_couvis_occultation_port_state'


class MultObsInstrumentCouvisSlitState(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_couvis_slit_state'


class MultObsInstrumentCouvisTestPulseState(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_couvis_test_pulse_state'


class MultObsInstrumentCovimsChannel(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_covims_channel'


class MultObsInstrumentCovimsInstrumentModeId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_covims_instrument_mode_id'


class MultObsInstrumentCovimsIrSamplingModeId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_covims_ir_sampling_mode_id'


class MultObsInstrumentCovimsSpectralEditing(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_covims_spectral_editing'


class MultObsInstrumentCovimsSpectralSumming(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_covims_spectral_summing'


class MultObsInstrumentCovimsStarTracking(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_covims_star_tracking'


class MultObsInstrumentCovimsVisSamplingModeId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_covims_vis_sampling_mode_id'


class MultObsInstrumentGossiCompressionType(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_gossi_compression_type'


class MultObsInstrumentGossiFilterName(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_gossi_filter_name'


class MultObsInstrumentGossiFilterNumber(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_gossi_filter_number'


class MultObsInstrumentGossiFrameDuration(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_gossi_frame_duration'


class MultObsInstrumentGossiGainModeId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_gossi_gain_mode_id'


class MultObsInstrumentGossiObstructionId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_gossi_obstruction_id'


class MultObsInstrumentNhlorriBinningMode(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_nhlorri_binning_mode'


class MultObsInstrumentNhlorriInstrumentCompressionType(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_nhlorri_instrument_compression_type'


class MultObsInstrumentNhmvicInstrumentCompressionType(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_nhmvic_instrument_compression_type'


class MultObsInstrumentVgissCamera(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_vgiss_camera'


class MultObsInstrumentVgissEditMode(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_vgiss_edit_mode'


class MultObsInstrumentVgissFilterName(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_vgiss_filter_name'


class MultObsInstrumentVgissFilterNumber(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_vgiss_filter_number'


class MultObsInstrumentVgissGainMode(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_vgiss_gain_mode'


class MultObsInstrumentVgissScanMode(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_vgiss_scan_mode'


class MultObsInstrumentVgissShutterMode(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_instrument_vgiss_shutter_mode'


class MultObsMissionCassiniCassiniTargetCode(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_cassini_cassini_target_code'


class MultObsMissionCassiniIsPrime(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_cassini_is_prime'


class MultObsMissionCassiniMissionPhaseName(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_cassini_mission_phase_name'


class MultObsMissionCassiniPrimeInstId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_cassini_prime_inst_id'


class MultObsMissionCassiniRevNo(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_cassini_rev_no'


class MultObsMissionGalileoOrbitNumber(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_galileo_orbit_number'


class MultObsMissionHubbleApertureType(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_hubble_aperture_type'


class MultObsMissionHubbleDetectorId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_hubble_detector_id'


class MultObsMissionHubbleExposureType(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_hubble_exposure_type'


class MultObsMissionHubbleFilterName(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_hubble_filter_name'


class MultObsMissionHubbleFilterType(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_hubble_filter_type'


class MultObsMissionHubbleFineGuidanceSystemLockType(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_hubble_fine_guidance_system_lock_type'


class MultObsMissionHubbleGainModeId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_hubble_gain_mode_id'


class MultObsMissionHubbleInstrumentModeId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_hubble_instrument_mode_id'


class MultObsMissionHubblePc1Flag(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_hubble_pc1_flag'


class MultObsMissionHubbleTargetedDetectorId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_hubble_targeted_detector_id'


class MultObsMissionHubbleWf2Flag(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_hubble_wf2_flag'


class MultObsMissionHubbleWf3Flag(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_hubble_wf3_flag'


class MultObsMissionHubbleWf4Flag(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_hubble_wf4_flag'


class MultObsMissionNewHorizonsMissionPhase(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_new_horizons_mission_phase'


class MultObsMissionNewHorizonsTelemetryApplicationId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_new_horizons_telemetry_application_id'


class MultObsMissionVoyagerMissionPhaseName(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_mission_voyager_mission_phase_name'


class MultObsSurfaceGeometryTargetName(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=30)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    grouping = models.CharField(max_length=7, blank=True, null=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_surface_geometry_target_name'


class MultObsTypeImageImageTypeId(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_type_image_image_type_id'


class MultObsWavelengthPolarizationType(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_wavelength_polarization_type'


class MultObsWavelengthSpecFlag(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=60)
    disp_order = models.IntegerField()
    display = models.CharField(max_length=1)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mult_obs_wavelength_spec_flag'


class ObsGeneral(models.Model):
    id = models.IntegerField(primary_key=True)
    opus_id = models.CharField(unique=True, max_length=80)
    volume_id = models.CharField(max_length=11)
    instrument_id = models.CharField(max_length=9)
    mission_id = models.CharField(max_length=3)
    inst_host_id = models.CharField(max_length=3)
    planet_id = models.CharField(max_length=3)
    target_name = models.CharField(max_length=20, blank=True, null=True)
    target_class = models.CharField(max_length=12)
    time1 = models.CharField(max_length=23, blank=True, null=True)
    time2 = models.CharField(max_length=23, blank=True, null=True)
    time_sec1 = models.FloatField(blank=True, null=True)
    time_sec2 = models.FloatField(blank=True, null=True)
    observation_duration = models.FloatField(blank=True, null=True)
    quantity = models.CharField(max_length=25)
    right_asc1 = models.FloatField(blank=True, null=True)
    right_asc2 = models.FloatField(blank=True, null=True)
    right_asc = models.FloatField(blank=True, null=True)
    d_right_asc = models.FloatField(blank=True, null=True)
    declination1 = models.FloatField(blank=True, null=True)
    declination2 = models.FloatField(blank=True, null=True)
    declination = models.FloatField(blank=True, null=True)
    d_declination = models.FloatField(blank=True, null=True)
    spatial_sampling = models.CharField(max_length=5, blank=True, null=True)
    wavelength_sampling = models.CharField(max_length=3, blank=True, null=True)
    time_sampling = models.CharField(max_length=3, blank=True, null=True)
    mult_obs_general_instrument = models.ForeignKey(MultObsGeneralInstrumentId, models.DO_NOTHING)
    mult_obs_general_mission = models.ForeignKey(MultObsGeneralMissionId, models.DO_NOTHING)
    mult_obs_general_inst_host = models.ForeignKey(MultObsGeneralInstHostId, models.DO_NOTHING)
    mult_obs_general_planet = models.ForeignKey(MultObsGeneralPlanetId, models.DO_NOTHING)
    mult_obs_general_target_name = models.ForeignKey(MultObsGeneralTargetName, models.DO_NOTHING, db_column='mult_obs_general_target_name')
    mult_obs_general_target_class = models.ForeignKey(MultObsGeneralTargetClass, models.DO_NOTHING, db_column='mult_obs_general_target_class')
    mult_obs_general_quantity = models.ForeignKey(MultObsGeneralQuantity, models.DO_NOTHING, db_column='mult_obs_general_quantity')
    mult_obs_general_spatial_sampling = models.ForeignKey(MultObsGeneralSpatialSampling, models.DO_NOTHING, db_column='mult_obs_general_spatial_sampling')
    mult_obs_general_wavelength_sampling = models.ForeignKey(MultObsGeneralWavelengthSampling, models.DO_NOTHING, db_column='mult_obs_general_wavelength_sampling')
    mult_obs_general_time_sampling = models.ForeignKey(MultObsGeneralTimeSampling, models.DO_NOTHING, db_column='mult_obs_general_time_sampling')
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_general'


class ObsInstrumentCoiss(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    data_conversion_type = models.CharField(max_length=5, blank=True, null=True)
    compression_type = models.CharField(max_length=8, blank=True, null=True)
    gain_mode_id = models.CharField(max_length=20, blank=True, null=True)
    image_observation_type = models.CharField(max_length=48, blank=True, null=True)
    missing_lines = models.SmallIntegerField(blank=True, null=True)
    shutter_mode_id = models.CharField(max_length=7, blank=True, null=True)
    shutter_state_id = models.CharField(max_length=8, blank=True, null=True)
    image_number = models.IntegerField()
    instrument_mode_id = models.CharField(max_length=4)
    target_desc = models.CharField(max_length=75)
    combined_filter = models.CharField(max_length=30)
    camera = models.CharField(max_length=1)
    mult_obs_instrument_coiss_data_conversion_type = models.ForeignKey(MultObsInstrumentCoissDataConversionType, models.DO_NOTHING, db_column='mult_obs_instrument_coiss_data_conversion_type')
    mult_obs_instrument_coiss_compression_type = models.ForeignKey(MultObsInstrumentCoissCompressionType, models.DO_NOTHING, db_column='mult_obs_instrument_coiss_compression_type')
    mult_obs_instrument_coiss_gain_mode = models.ForeignKey(MultObsInstrumentCoissGainModeId, models.DO_NOTHING)
    mult_obs_instrument_coiss_image_observation_type = models.ForeignKey(MultObsInstrumentCoissImageObservationType, models.DO_NOTHING, db_column='mult_obs_instrument_coiss_image_observation_type')
    mult_obs_instrument_coiss_shutter_mode = models.ForeignKey(MultObsInstrumentCoissShutterModeId, models.DO_NOTHING)
    mult_obs_instrument_coiss_shutter_state = models.ForeignKey(MultObsInstrumentCoissShutterStateId, models.DO_NOTHING)
    mult_obs_instrument_coiss_instrument_mode = models.ForeignKey(MultObsInstrumentCoissInstrumentModeId, models.DO_NOTHING)
    mult_obs_instrument_coiss_combined_filter = models.ForeignKey(MultObsInstrumentCoissCombinedFilter, models.DO_NOTHING, db_column='mult_obs_instrument_coiss_combined_filter')
    mult_obs_instrument_coiss_camera = models.ForeignKey(MultObsInstrumentCoissCamera, models.DO_NOTHING, db_column='mult_obs_instrument_coiss_camera')
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_instrument_coiss'


class ObsInstrumentCouvis(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    observation_type = models.CharField(max_length=8)
    integration_duration = models.FloatField(blank=True, null=True)
    compression_type = models.CharField(max_length=6)
    occultation_port_state = models.CharField(max_length=6)
    slit_state = models.CharField(max_length=15)
    test_pulse_state = models.CharField(max_length=3, blank=True, null=True)
    dwell_time = models.IntegerField(blank=True, null=True)
    channel = models.CharField(max_length=4)
    band1 = models.IntegerField(blank=True, null=True)
    band2 = models.IntegerField(blank=True, null=True)
    band_bin = models.IntegerField(blank=True, null=True)
    line1 = models.IntegerField(blank=True, null=True)
    line2 = models.IntegerField(blank=True, null=True)
    line_bin = models.IntegerField(blank=True, null=True)
    samples = models.IntegerField(blank=True, null=True)
    mult_obs_instrument_couvis_observation_type = models.ForeignKey(MultObsInstrumentCouvisObservationType, models.DO_NOTHING, db_column='mult_obs_instrument_couvis_observation_type')
    mult_obs_instrument_couvis_compression_type = models.ForeignKey(MultObsInstrumentCouvisCompressionType, models.DO_NOTHING, db_column='mult_obs_instrument_couvis_compression_type')
    mult_obs_instrument_couvis_occultation_port_state = models.ForeignKey(MultObsInstrumentCouvisOccultationPortState, models.DO_NOTHING, db_column='mult_obs_instrument_couvis_occultation_port_state')
    mult_obs_instrument_couvis_slit_state = models.ForeignKey(MultObsInstrumentCouvisSlitState, models.DO_NOTHING, db_column='mult_obs_instrument_couvis_slit_state')
    mult_obs_instrument_couvis_test_pulse_state = models.ForeignKey(MultObsInstrumentCouvisTestPulseState, models.DO_NOTHING, db_column='mult_obs_instrument_couvis_test_pulse_state')
    mult_obs_instrument_couvis_dwell_time = models.ForeignKey(MultObsInstrumentCouvisDwellTime, models.DO_NOTHING, db_column='mult_obs_instrument_couvis_dwell_time')
    mult_obs_instrument_couvis_channel = models.ForeignKey(MultObsInstrumentCouvisChannel, models.DO_NOTHING, db_column='mult_obs_instrument_couvis_channel')
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_instrument_couvis'


class ObsInstrumentCovims(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    instrument_mode_id = models.CharField(max_length=14)
    spectral_editing = models.CharField(max_length=3)
    spectral_summing = models.CharField(max_length=3)
    star_tracking = models.CharField(max_length=3)
    swath_width = models.SmallIntegerField()
    swath_length = models.SmallIntegerField()
    ir_exposure = models.FloatField(blank=True, null=True)
    ir_sampling_mode_id = models.CharField(max_length=6)
    vis_exposure = models.FloatField(blank=True, null=True)
    vis_sampling_mode_id = models.CharField(max_length=6)
    channel = models.CharField(max_length=3)
    mult_obs_instrument_covims_instrument_mode = models.ForeignKey(MultObsInstrumentCovimsInstrumentModeId, models.DO_NOTHING)
    mult_obs_instrument_covims_spectral_editing = models.ForeignKey(MultObsInstrumentCovimsSpectralEditing, models.DO_NOTHING, db_column='mult_obs_instrument_covims_spectral_editing')
    mult_obs_instrument_covims_spectral_summing = models.ForeignKey(MultObsInstrumentCovimsSpectralSumming, models.DO_NOTHING, db_column='mult_obs_instrument_covims_spectral_summing')
    mult_obs_instrument_covims_star_tracking = models.ForeignKey(MultObsInstrumentCovimsStarTracking, models.DO_NOTHING, db_column='mult_obs_instrument_covims_star_tracking')
    mult_obs_instrument_covims_ir_sampling_mode = models.ForeignKey(MultObsInstrumentCovimsIrSamplingModeId, models.DO_NOTHING)
    mult_obs_instrument_covims_vis_sampling_mode = models.ForeignKey(MultObsInstrumentCovimsVisSamplingModeId, models.DO_NOTHING)
    mult_obs_instrument_covims_channel = models.ForeignKey(MultObsInstrumentCovimsChannel, models.DO_NOTHING, db_column='mult_obs_instrument_covims_channel')
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_instrument_covims'


class ObsInstrumentGossi(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    observation_id = models.CharField(max_length=20)
    image_id = models.CharField(max_length=7)
    filter_name = models.CharField(max_length=7)
    filter_number = models.IntegerField()
    gain_mode_id = models.CharField(max_length=4)
    frame_duration = models.FloatField()
    obstruction_id = models.CharField(max_length=17)
    compression_type = models.CharField(max_length=24)
    mult_obs_instrument_gossi_filter_name = models.ForeignKey(MultObsInstrumentGossiFilterName, models.DO_NOTHING, db_column='mult_obs_instrument_gossi_filter_name')
    mult_obs_instrument_gossi_filter_number = models.ForeignKey(MultObsInstrumentGossiFilterNumber, models.DO_NOTHING, db_column='mult_obs_instrument_gossi_filter_number')
    mult_obs_instrument_gossi_gain_mode = models.ForeignKey(MultObsInstrumentGossiGainModeId, models.DO_NOTHING)
    mult_obs_instrument_gossi_frame_duration = models.ForeignKey(MultObsInstrumentGossiFrameDuration, models.DO_NOTHING, db_column='mult_obs_instrument_gossi_frame_duration')
    mult_obs_instrument_gossi_obstruction = models.ForeignKey(MultObsInstrumentGossiObstructionId, models.DO_NOTHING)
    mult_obs_instrument_gossi_compression_type = models.ForeignKey(MultObsInstrumentGossiCompressionType, models.DO_NOTHING, db_column='mult_obs_instrument_gossi_compression_type')
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_instrument_gossi'


class ObsInstrumentNhlorri(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    instrument_compression_type = models.CharField(max_length=10)
    binning_mode = models.CharField(max_length=3)
    mult_obs_instrument_nhlorri_instrument_compression_type = models.ForeignKey(MultObsInstrumentNhlorriInstrumentCompressionType, models.DO_NOTHING, db_column='mult_obs_instrument_nhlorri_instrument_compression_type')
    mult_obs_instrument_nhlorri_binning_mode = models.ForeignKey(MultObsInstrumentNhlorriBinningMode, models.DO_NOTHING, db_column='mult_obs_instrument_nhlorri_binning_mode')
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_instrument_nhlorri'


class ObsInstrumentNhmvic(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    instrument_compression_type = models.CharField(max_length=10)
    mult_obs_instrument_nhmvic_instrument_compression_type = models.ForeignKey(MultObsInstrumentNhmvicInstrumentCompressionType, models.DO_NOTHING, db_column='mult_obs_instrument_nhmvic_instrument_compression_type')
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_instrument_nhmvic'


class ObsInstrumentVgiss(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    image_id = models.CharField(max_length=10)
    scan_mode = models.CharField(max_length=4)
    shutter_mode = models.CharField(max_length=6)
    gain_mode = models.CharField(max_length=4)
    edit_mode = models.CharField(max_length=4)
    filter_name = models.CharField(max_length=6)
    filter_number = models.IntegerField()
    camera = models.CharField(max_length=1)
    usable_lines = models.SmallIntegerField(blank=True, null=True)
    usable_samples = models.SmallIntegerField(blank=True, null=True)
    mult_obs_instrument_vgiss_scan_mode = models.ForeignKey(MultObsInstrumentVgissScanMode, models.DO_NOTHING, db_column='mult_obs_instrument_vgiss_scan_mode')
    mult_obs_instrument_vgiss_shutter_mode = models.ForeignKey(MultObsInstrumentVgissShutterMode, models.DO_NOTHING, db_column='mult_obs_instrument_vgiss_shutter_mode')
    mult_obs_instrument_vgiss_gain_mode = models.ForeignKey(MultObsInstrumentVgissGainMode, models.DO_NOTHING, db_column='mult_obs_instrument_vgiss_gain_mode')
    mult_obs_instrument_vgiss_edit_mode = models.ForeignKey(MultObsInstrumentVgissEditMode, models.DO_NOTHING, db_column='mult_obs_instrument_vgiss_edit_mode')
    mult_obs_instrument_vgiss_filter_name = models.ForeignKey(MultObsInstrumentVgissFilterName, models.DO_NOTHING, db_column='mult_obs_instrument_vgiss_filter_name')
    mult_obs_instrument_vgiss_filter_number = models.ForeignKey(MultObsInstrumentVgissFilterNumber, models.DO_NOTHING, db_column='mult_obs_instrument_vgiss_filter_number')
    mult_obs_instrument_vgiss_camera = models.ForeignKey(MultObsInstrumentVgissCamera, models.DO_NOTHING, db_column='mult_obs_instrument_vgiss_camera')
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_instrument_vgiss'


class ObsMissionCassini(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    instrument_id = models.CharField(max_length=9)
    obs_name = models.CharField(max_length=30)
    rev_no = models.CharField(max_length=3, blank=True, null=True)
    is_prime = models.CharField(max_length=3)
    prime_inst_id = models.CharField(max_length=6, blank=True, null=True)
    spacecraft_clock_count1 = models.CharField(max_length=18, blank=True, null=True)
    spacecraft_clock_count2 = models.CharField(max_length=18, blank=True, null=True)
    spacecraft_clock_count_cvt1 = models.FloatField(blank=True, null=True)
    spacecraft_clock_count_cvt2 = models.FloatField(blank=True, null=True)
    ert1 = models.CharField(max_length=23, blank=True, null=True)
    ert2 = models.CharField(max_length=23, blank=True, null=True)
    ert_sec1 = models.FloatField(blank=True, null=True)
    ert_sec2 = models.FloatField(blank=True, null=True)
    cassini_target_code = models.CharField(max_length=50, blank=True, null=True)
    activity_name = models.CharField(max_length=9, blank=True, null=True)
    mission_phase_name = models.CharField(max_length=32, blank=True, null=True)
    sequence_id = models.CharField(max_length=4, blank=True, null=True)
    mult_obs_mission_cassini_rev_no = models.ForeignKey(MultObsMissionCassiniRevNo, models.DO_NOTHING, db_column='mult_obs_mission_cassini_rev_no')
    mult_obs_mission_cassini_is_prime = models.ForeignKey(MultObsMissionCassiniIsPrime, models.DO_NOTHING, db_column='mult_obs_mission_cassini_is_prime')
    mult_obs_mission_cassini_prime_inst = models.ForeignKey(MultObsMissionCassiniPrimeInstId, models.DO_NOTHING)
    mult_obs_mission_cassini_cassini_target_code = models.ForeignKey(MultObsMissionCassiniCassiniTargetCode, models.DO_NOTHING, db_column='mult_obs_mission_cassini_cassini_target_code')
    mult_obs_mission_cassini_mission_phase_name = models.ForeignKey(MultObsMissionCassiniMissionPhaseName, models.DO_NOTHING, db_column='mult_obs_mission_cassini_mission_phase_name')
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_mission_cassini'


class ObsMissionGalileo(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    orbit_number = models.IntegerField(blank=True, null=True)
    spacecraft_clock_count1 = models.CharField(max_length=11, blank=True, null=True)
    spacecraft_clock_count2 = models.CharField(max_length=11)
    spacecraft_clock_count_cvt1 = models.FloatField(blank=True, null=True)
    spacecraft_clock_count_cvt2 = models.FloatField(blank=True, null=True)
    mult_obs_mission_galileo_orbit_number = models.ForeignKey(MultObsMissionGalileoOrbitNumber, models.DO_NOTHING, db_column='mult_obs_mission_galileo_orbit_number')
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_mission_galileo'


class ObsMissionHubble(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    instrument_id = models.CharField(max_length=9)
    stsci_group_id = models.CharField(max_length=9)
    hst_proposal_id = models.IntegerField()
    hst_pi_name = models.CharField(max_length=24)
    detector_id = models.CharField(max_length=14, blank=True, null=True)
    publication_date = models.CharField(max_length=10)
    hst_target_name = models.CharField(max_length=31)
    fine_guidance_system_lock_type = models.CharField(max_length=10)
    filter_name = models.CharField(max_length=23)
    filter_type = models.CharField(max_length=3)
    aperture_type = models.CharField(max_length=22)
    exposure_type = models.CharField(max_length=20)
    gain_mode_id = models.CharField(max_length=5)
    instrument_mode_id = models.CharField(max_length=10)
    pc1_flag = models.CharField(max_length=3, blank=True, null=True)
    wf2_flag = models.CharField(max_length=3, blank=True, null=True)
    wf3_flag = models.CharField(max_length=3, blank=True, null=True)
    wf4_flag = models.CharField(max_length=3, blank=True, null=True)
    targeted_detector_id = models.CharField(max_length=3, blank=True, null=True)
    mult_obs_mission_hubble_detector = models.ForeignKey(MultObsMissionHubbleDetectorId, models.DO_NOTHING)
    mult_obs_mission_hubble_fine_guidance_system_lock_type = models.ForeignKey(MultObsMissionHubbleFineGuidanceSystemLockType, models.DO_NOTHING, db_column='mult_obs_mission_hubble_fine_guidance_system_lock_type')
    mult_obs_mission_hubble_filter_name = models.ForeignKey(MultObsMissionHubbleFilterName, models.DO_NOTHING, db_column='mult_obs_mission_hubble_filter_name')
    mult_obs_mission_hubble_filter_type = models.ForeignKey(MultObsMissionHubbleFilterType, models.DO_NOTHING, db_column='mult_obs_mission_hubble_filter_type')
    mult_obs_mission_hubble_aperture_type = models.ForeignKey(MultObsMissionHubbleApertureType, models.DO_NOTHING, db_column='mult_obs_mission_hubble_aperture_type')
    mult_obs_mission_hubble_exposure_type = models.ForeignKey(MultObsMissionHubbleExposureType, models.DO_NOTHING, db_column='mult_obs_mission_hubble_exposure_type')
    mult_obs_mission_hubble_gain_mode = models.ForeignKey(MultObsMissionHubbleGainModeId, models.DO_NOTHING)
    mult_obs_mission_hubble_instrument_mode = models.ForeignKey(MultObsMissionHubbleInstrumentModeId, models.DO_NOTHING)
    mult_obs_mission_hubble_pc1_flag = models.ForeignKey(MultObsMissionHubblePc1Flag, models.DO_NOTHING, db_column='mult_obs_mission_hubble_pc1_flag')
    mult_obs_mission_hubble_wf2_flag = models.ForeignKey(MultObsMissionHubbleWf2Flag, models.DO_NOTHING, db_column='mult_obs_mission_hubble_wf2_flag')
    mult_obs_mission_hubble_wf3_flag = models.ForeignKey(MultObsMissionHubbleWf3Flag, models.DO_NOTHING, db_column='mult_obs_mission_hubble_wf3_flag')
    mult_obs_mission_hubble_wf4_flag = models.ForeignKey(MultObsMissionHubbleWf4Flag, models.DO_NOTHING, db_column='mult_obs_mission_hubble_wf4_flag')
    mult_obs_mission_hubble_targeted_detector = models.ForeignKey(MultObsMissionHubbleTargetedDetectorId, models.DO_NOTHING)
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_mission_hubble'


class ObsMissionNewHorizons(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    instrument_id = models.CharField(max_length=9)
    spacecraft_clock_count1 = models.CharField(max_length=19, blank=True, null=True)
    spacecraft_clock_count2 = models.CharField(max_length=19, blank=True, null=True)
    spacecraft_clock_count_cvt1 = models.FloatField(blank=True, null=True)
    spacecraft_clock_count_cvt2 = models.FloatField(blank=True, null=True)
    mission_phase = models.CharField(max_length=22, blank=True, null=True)
    telemetry_application_id = models.CharField(max_length=5)
    mult_obs_mission_new_horizons_mission_phase = models.ForeignKey(MultObsMissionNewHorizonsMissionPhase, models.DO_NOTHING, db_column='mult_obs_mission_new_horizons_mission_phase')
    mult_obs_mission_new_horizons_telemetry_application = models.ForeignKey(MultObsMissionNewHorizonsTelemetryApplicationId, models.DO_NOTHING)
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_mission_new_horizons'


class ObsMissionVoyager(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    ert = models.CharField(max_length=23, blank=True, null=True)
    ert_sec = models.FloatField(blank=True, null=True)
    spacecraft_clock_count1 = models.CharField(max_length=14, blank=True, null=True)
    spacecraft_clock_count2 = models.CharField(max_length=14, blank=True, null=True)
    spacecraft_clock_count_cvt1 = models.FloatField(blank=True, null=True)
    spacecraft_clock_count_cvt2 = models.FloatField(blank=True, null=True)
    mission_phase_name = models.CharField(max_length=32, blank=True, null=True)
    mult_obs_mission_voyager_mission_phase_name = models.ForeignKey(MultObsMissionVoyagerMissionPhaseName, models.DO_NOTHING, db_column='mult_obs_mission_voyager_mission_phase_name')
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_mission_voyager'


class ObsPds(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    instrument_id = models.CharField(max_length=9)
    data_set_id = models.CharField(max_length=40)
    product_id = models.CharField(max_length=30)
    product_creation_time = models.CharField(max_length=23, blank=True, null=True)
    product_creation_time_sec = models.FloatField(blank=True, null=True)
    primary_file_spec = models.CharField(max_length=240, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_pds'


class ObsRingGeometry(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    instrument_id = models.CharField(max_length=9)
    ring_radius1 = models.FloatField(blank=True, null=True)
    ring_radius2 = models.FloatField(blank=True, null=True)
    resolution1 = models.FloatField(blank=True, null=True)
    resolution2 = models.FloatField(blank=True, null=True)
    projected_radial_resolution1 = models.FloatField(blank=True, null=True)
    projected_radial_resolution2 = models.FloatField(blank=True, null=True)
    range_to_ring_intercept1 = models.FloatField(blank=True, null=True)
    range_to_ring_intercept2 = models.FloatField(blank=True, null=True)
    ring_center_distance = models.FloatField(blank=True, null=True)
    j2000_longitude1 = models.FloatField(blank=True, null=True)
    j2000_longitude2 = models.FloatField(blank=True, null=True)
    j2000_longitude = models.FloatField(blank=True, null=True)
    d_j2000_longitude = models.FloatField(blank=True, null=True)
    solar_hour_angle1 = models.FloatField(blank=True, null=True)
    solar_hour_angle2 = models.FloatField(blank=True, null=True)
    solar_hour_angle = models.FloatField(blank=True, null=True)
    d_solar_hour_angle = models.FloatField(blank=True, null=True)
    longitude_wrt_observer1 = models.FloatField(blank=True, null=True)
    longitude_wrt_observer2 = models.FloatField(blank=True, null=True)
    ring_azimuth_wrt_observer1 = models.FloatField(blank=True, null=True)
    ring_azimuth_wrt_observer2 = models.FloatField(blank=True, null=True)
    sub_solar_ring_long = models.FloatField(blank=True, null=True)
    sub_observer_ring_long = models.FloatField(blank=True, null=True)
    solar_ring_elev1 = models.FloatField(blank=True, null=True)
    solar_ring_elev2 = models.FloatField(blank=True, null=True)
    observer_ring_elevation1 = models.FloatField(blank=True, null=True)
    observer_ring_elevation2 = models.FloatField(blank=True, null=True)
    phase1 = models.FloatField(blank=True, null=True)
    phase2 = models.FloatField(blank=True, null=True)
    incidence1 = models.FloatField(blank=True, null=True)
    incidence2 = models.FloatField(blank=True, null=True)
    emission1 = models.FloatField(blank=True, null=True)
    emission2 = models.FloatField(blank=True, null=True)
    north_based_incidence1 = models.FloatField(blank=True, null=True)
    north_based_incidence2 = models.FloatField(blank=True, null=True)
    north_based_emission1 = models.FloatField(blank=True, null=True)
    north_based_emission2 = models.FloatField(blank=True, null=True)
    ring_center_phase = models.FloatField(blank=True, null=True)
    ring_center_incidence = models.FloatField(blank=True, null=True)
    ring_center_emission = models.FloatField(blank=True, null=True)
    ring_center_north_based_incidence = models.FloatField(blank=True, null=True)
    ring_center_north_based_emission = models.FloatField(blank=True, null=True)
    solar_ring_opening_angle = models.FloatField(blank=True, null=True)
    observer_ring_opening_angle = models.FloatField(blank=True, null=True)
    edge_on_radius1 = models.FloatField(blank=True, null=True)
    edge_on_radius2 = models.FloatField(blank=True, null=True)
    edge_on_altitude1 = models.FloatField(blank=True, null=True)
    edge_on_altitude2 = models.FloatField(blank=True, null=True)
    edge_on_radial_resolution1 = models.FloatField(blank=True, null=True)
    edge_on_radial_resolution2 = models.FloatField(blank=True, null=True)
    range_to_edge_on_point1 = models.FloatField(blank=True, null=True)
    range_to_edge_on_point2 = models.FloatField(blank=True, null=True)
    edge_on_j2000_longitude1 = models.FloatField(blank=True, null=True)
    edge_on_j2000_longitude2 = models.FloatField(blank=True, null=True)
    edge_on_j2000_longitude = models.FloatField(blank=True, null=True)
    d_edge_on_j2000_longitude = models.FloatField(blank=True, null=True)
    edge_on_solar_hour_angle1 = models.FloatField(blank=True, null=True)
    edge_on_solar_hour_angle2 = models.FloatField(blank=True, null=True)
    edge_on_solar_hour_angle = models.FloatField(blank=True, null=True)
    d_edge_on_solar_hour_angle = models.FloatField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_ring_geometry'


class ObsSurfaceGeometry(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    instrument_id = models.CharField(max_length=9)
    target_name = models.CharField(max_length=75)
    mult_obs_surface_geometry_target_name = models.ForeignKey(MultObsSurfaceGeometryTargetName, models.DO_NOTHING, db_column='mult_obs_surface_geometry_target_name')
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_surface_geometry'


class ObsSurfaceGeometryEnceladus(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    instrument_id = models.CharField(max_length=9)
    planetocentric_latitude1 = models.FloatField(blank=True, null=True)
    planetocentric_latitude2 = models.FloatField(blank=True, null=True)
    planetographic_latitude1 = models.FloatField(blank=True, null=True)
    planetographic_latitude2 = models.FloatField(blank=True, null=True)
    iau_west_longitude1 = models.FloatField(blank=True, null=True)
    iau_west_longitude2 = models.FloatField(blank=True, null=True)
    iau_west_longitude = models.FloatField(blank=True, null=True)
    d_iau_west_longitude = models.FloatField(blank=True, null=True)
    solar_hour_angle1 = models.FloatField(blank=True, null=True)
    solar_hour_angle2 = models.FloatField(blank=True, null=True)
    solar_hour_angle = models.FloatField(blank=True, null=True)
    d_solar_hour_angle = models.FloatField(blank=True, null=True)
    observer_longitude1 = models.FloatField(blank=True, null=True)
    observer_longitude2 = models.FloatField(blank=True, null=True)
    observer_longitude = models.FloatField(blank=True, null=True)
    d_observer_longitude = models.FloatField(blank=True, null=True)
    finest_resolution1 = models.FloatField(blank=True, null=True)
    finest_resolution2 = models.FloatField(blank=True, null=True)
    coarsest_resolution1 = models.FloatField(blank=True, null=True)
    coarsest_resolution2 = models.FloatField(blank=True, null=True)
    range_to_body1 = models.FloatField(blank=True, null=True)
    range_to_body2 = models.FloatField(blank=True, null=True)
    phase1 = models.FloatField(blank=True, null=True)
    phase2 = models.FloatField(blank=True, null=True)
    incidence1 = models.FloatField(blank=True, null=True)
    incidence2 = models.FloatField(blank=True, null=True)
    emission1 = models.FloatField(blank=True, null=True)
    emission2 = models.FloatField(blank=True, null=True)
    sub_solar_planetocentric_latitude = models.FloatField(blank=True, null=True)
    sub_solar_planetographic_latitude = models.FloatField(blank=True, null=True)
    sub_observer_planetocentric_latitude = models.FloatField(blank=True, null=True)
    sub_observer_planetographic_latitude = models.FloatField(blank=True, null=True)
    sub_solar_iau_longitude = models.FloatField(blank=True, null=True)
    sub_observer_iau_longitude = models.FloatField(blank=True, null=True)
    center_resolution = models.FloatField(blank=True, null=True)
    center_distance = models.FloatField(blank=True, null=True)
    center_phase_angle = models.FloatField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_surface_geometry__enceladus'


class ObsSurfaceGeometryHimalia(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    instrument_id = models.CharField(max_length=9)
    planetocentric_latitude1 = models.FloatField(blank=True, null=True)
    planetocentric_latitude2 = models.FloatField(blank=True, null=True)
    planetographic_latitude1 = models.FloatField(blank=True, null=True)
    planetographic_latitude2 = models.FloatField(blank=True, null=True)
    iau_west_longitude1 = models.FloatField(blank=True, null=True)
    iau_west_longitude2 = models.FloatField(blank=True, null=True)
    iau_west_longitude = models.FloatField(blank=True, null=True)
    d_iau_west_longitude = models.FloatField(blank=True, null=True)
    solar_hour_angle1 = models.FloatField(blank=True, null=True)
    solar_hour_angle2 = models.FloatField(blank=True, null=True)
    solar_hour_angle = models.FloatField(blank=True, null=True)
    d_solar_hour_angle = models.FloatField(blank=True, null=True)
    observer_longitude1 = models.FloatField(blank=True, null=True)
    observer_longitude2 = models.FloatField(blank=True, null=True)
    observer_longitude = models.FloatField(blank=True, null=True)
    d_observer_longitude = models.FloatField(blank=True, null=True)
    finest_resolution1 = models.FloatField(blank=True, null=True)
    finest_resolution2 = models.FloatField(blank=True, null=True)
    coarsest_resolution1 = models.FloatField(blank=True, null=True)
    coarsest_resolution2 = models.FloatField(blank=True, null=True)
    range_to_body1 = models.FloatField(blank=True, null=True)
    range_to_body2 = models.FloatField(blank=True, null=True)
    phase1 = models.FloatField(blank=True, null=True)
    phase2 = models.FloatField(blank=True, null=True)
    incidence1 = models.FloatField(blank=True, null=True)
    incidence2 = models.FloatField(blank=True, null=True)
    emission1 = models.FloatField(blank=True, null=True)
    emission2 = models.FloatField(blank=True, null=True)
    sub_solar_planetocentric_latitude = models.FloatField(blank=True, null=True)
    sub_solar_planetographic_latitude = models.FloatField(blank=True, null=True)
    sub_observer_planetocentric_latitude = models.FloatField(blank=True, null=True)
    sub_observer_planetographic_latitude = models.FloatField(blank=True, null=True)
    sub_solar_iau_longitude = models.FloatField(blank=True, null=True)
    sub_observer_iau_longitude = models.FloatField(blank=True, null=True)
    center_resolution = models.FloatField(blank=True, null=True)
    center_distance = models.FloatField(blank=True, null=True)
    center_phase_angle = models.FloatField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_surface_geometry__himalia'


class ObsSurfaceGeometryJupiter(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    instrument_id = models.CharField(max_length=9)
    planetocentric_latitude1 = models.FloatField(blank=True, null=True)
    planetocentric_latitude2 = models.FloatField(blank=True, null=True)
    planetographic_latitude1 = models.FloatField(blank=True, null=True)
    planetographic_latitude2 = models.FloatField(blank=True, null=True)
    iau_west_longitude1 = models.FloatField(blank=True, null=True)
    iau_west_longitude2 = models.FloatField(blank=True, null=True)
    iau_west_longitude = models.FloatField(blank=True, null=True)
    d_iau_west_longitude = models.FloatField(blank=True, null=True)
    solar_hour_angle1 = models.FloatField(blank=True, null=True)
    solar_hour_angle2 = models.FloatField(blank=True, null=True)
    solar_hour_angle = models.FloatField(blank=True, null=True)
    d_solar_hour_angle = models.FloatField(blank=True, null=True)
    observer_longitude1 = models.FloatField(blank=True, null=True)
    observer_longitude2 = models.FloatField(blank=True, null=True)
    observer_longitude = models.FloatField(blank=True, null=True)
    d_observer_longitude = models.FloatField(blank=True, null=True)
    finest_resolution1 = models.FloatField(blank=True, null=True)
    finest_resolution2 = models.FloatField(blank=True, null=True)
    coarsest_resolution1 = models.FloatField(blank=True, null=True)
    coarsest_resolution2 = models.FloatField(blank=True, null=True)
    range_to_body1 = models.FloatField(blank=True, null=True)
    range_to_body2 = models.FloatField(blank=True, null=True)
    phase1 = models.FloatField(blank=True, null=True)
    phase2 = models.FloatField(blank=True, null=True)
    incidence1 = models.FloatField(blank=True, null=True)
    incidence2 = models.FloatField(blank=True, null=True)
    emission1 = models.FloatField(blank=True, null=True)
    emission2 = models.FloatField(blank=True, null=True)
    sub_solar_planetocentric_latitude = models.FloatField(blank=True, null=True)
    sub_solar_planetographic_latitude = models.FloatField(blank=True, null=True)
    sub_observer_planetocentric_latitude = models.FloatField(blank=True, null=True)
    sub_observer_planetographic_latitude = models.FloatField(blank=True, null=True)
    sub_solar_iau_longitude = models.FloatField(blank=True, null=True)
    sub_observer_iau_longitude = models.FloatField(blank=True, null=True)
    center_resolution = models.FloatField(blank=True, null=True)
    center_distance = models.FloatField(blank=True, null=True)
    center_phase_angle = models.FloatField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_surface_geometry__jupiter'


class ObsSurfaceGeometryMetis(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    instrument_id = models.CharField(max_length=9)
    planetocentric_latitude1 = models.FloatField(blank=True, null=True)
    planetocentric_latitude2 = models.FloatField(blank=True, null=True)
    planetographic_latitude1 = models.FloatField(blank=True, null=True)
    planetographic_latitude2 = models.FloatField(blank=True, null=True)
    iau_west_longitude1 = models.FloatField(blank=True, null=True)
    iau_west_longitude2 = models.FloatField(blank=True, null=True)
    iau_west_longitude = models.FloatField(blank=True, null=True)
    d_iau_west_longitude = models.FloatField(blank=True, null=True)
    solar_hour_angle1 = models.FloatField(blank=True, null=True)
    solar_hour_angle2 = models.FloatField(blank=True, null=True)
    solar_hour_angle = models.FloatField(blank=True, null=True)
    d_solar_hour_angle = models.FloatField(blank=True, null=True)
    observer_longitude1 = models.FloatField(blank=True, null=True)
    observer_longitude2 = models.FloatField(blank=True, null=True)
    observer_longitude = models.FloatField(blank=True, null=True)
    d_observer_longitude = models.FloatField(blank=True, null=True)
    finest_resolution1 = models.FloatField(blank=True, null=True)
    finest_resolution2 = models.FloatField(blank=True, null=True)
    coarsest_resolution1 = models.FloatField(blank=True, null=True)
    coarsest_resolution2 = models.FloatField(blank=True, null=True)
    range_to_body1 = models.FloatField(blank=True, null=True)
    range_to_body2 = models.FloatField(blank=True, null=True)
    phase1 = models.FloatField(blank=True, null=True)
    phase2 = models.FloatField(blank=True, null=True)
    incidence1 = models.FloatField(blank=True, null=True)
    incidence2 = models.FloatField(blank=True, null=True)
    emission1 = models.FloatField(blank=True, null=True)
    emission2 = models.FloatField(blank=True, null=True)
    sub_solar_planetocentric_latitude = models.FloatField(blank=True, null=True)
    sub_solar_planetographic_latitude = models.FloatField(blank=True, null=True)
    sub_observer_planetocentric_latitude = models.FloatField(blank=True, null=True)
    sub_observer_planetographic_latitude = models.FloatField(blank=True, null=True)
    sub_solar_iau_longitude = models.FloatField(blank=True, null=True)
    sub_observer_iau_longitude = models.FloatField(blank=True, null=True)
    center_resolution = models.FloatField(blank=True, null=True)
    center_distance = models.FloatField(blank=True, null=True)
    center_phase_angle = models.FloatField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_surface_geometry__metis'


class ObsSurfaceGeometrySaturn(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    instrument_id = models.CharField(max_length=9)
    planetocentric_latitude1 = models.FloatField(blank=True, null=True)
    planetocentric_latitude2 = models.FloatField(blank=True, null=True)
    planetographic_latitude1 = models.FloatField(blank=True, null=True)
    planetographic_latitude2 = models.FloatField(blank=True, null=True)
    iau_west_longitude1 = models.FloatField(blank=True, null=True)
    iau_west_longitude2 = models.FloatField(blank=True, null=True)
    iau_west_longitude = models.FloatField(blank=True, null=True)
    d_iau_west_longitude = models.FloatField(blank=True, null=True)
    solar_hour_angle1 = models.FloatField(blank=True, null=True)
    solar_hour_angle2 = models.FloatField(blank=True, null=True)
    solar_hour_angle = models.FloatField(blank=True, null=True)
    d_solar_hour_angle = models.FloatField(blank=True, null=True)
    observer_longitude1 = models.FloatField(blank=True, null=True)
    observer_longitude2 = models.FloatField(blank=True, null=True)
    observer_longitude = models.FloatField(blank=True, null=True)
    d_observer_longitude = models.FloatField(blank=True, null=True)
    finest_resolution1 = models.FloatField(blank=True, null=True)
    finest_resolution2 = models.FloatField(blank=True, null=True)
    coarsest_resolution1 = models.FloatField(blank=True, null=True)
    coarsest_resolution2 = models.FloatField(blank=True, null=True)
    range_to_body1 = models.FloatField(blank=True, null=True)
    range_to_body2 = models.FloatField(blank=True, null=True)
    phase1 = models.FloatField(blank=True, null=True)
    phase2 = models.FloatField(blank=True, null=True)
    incidence1 = models.FloatField(blank=True, null=True)
    incidence2 = models.FloatField(blank=True, null=True)
    emission1 = models.FloatField(blank=True, null=True)
    emission2 = models.FloatField(blank=True, null=True)
    sub_solar_planetocentric_latitude = models.FloatField(blank=True, null=True)
    sub_solar_planetographic_latitude = models.FloatField(blank=True, null=True)
    sub_observer_planetocentric_latitude = models.FloatField(blank=True, null=True)
    sub_observer_planetographic_latitude = models.FloatField(blank=True, null=True)
    sub_solar_iau_longitude = models.FloatField(blank=True, null=True)
    sub_observer_iau_longitude = models.FloatField(blank=True, null=True)
    center_resolution = models.FloatField(blank=True, null=True)
    center_distance = models.FloatField(blank=True, null=True)
    center_phase_angle = models.FloatField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_surface_geometry__saturn'


class ObsSurfaceGeometryTitan(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    instrument_id = models.CharField(max_length=9)
    planetocentric_latitude1 = models.FloatField(blank=True, null=True)
    planetocentric_latitude2 = models.FloatField(blank=True, null=True)
    planetographic_latitude1 = models.FloatField(blank=True, null=True)
    planetographic_latitude2 = models.FloatField(blank=True, null=True)
    iau_west_longitude1 = models.FloatField(blank=True, null=True)
    iau_west_longitude2 = models.FloatField(blank=True, null=True)
    iau_west_longitude = models.FloatField(blank=True, null=True)
    d_iau_west_longitude = models.FloatField(blank=True, null=True)
    solar_hour_angle1 = models.FloatField(blank=True, null=True)
    solar_hour_angle2 = models.FloatField(blank=True, null=True)
    solar_hour_angle = models.FloatField(blank=True, null=True)
    d_solar_hour_angle = models.FloatField(blank=True, null=True)
    observer_longitude1 = models.FloatField(blank=True, null=True)
    observer_longitude2 = models.FloatField(blank=True, null=True)
    observer_longitude = models.FloatField(blank=True, null=True)
    d_observer_longitude = models.FloatField(blank=True, null=True)
    finest_resolution1 = models.FloatField(blank=True, null=True)
    finest_resolution2 = models.FloatField(blank=True, null=True)
    coarsest_resolution1 = models.FloatField(blank=True, null=True)
    coarsest_resolution2 = models.FloatField(blank=True, null=True)
    range_to_body1 = models.FloatField(blank=True, null=True)
    range_to_body2 = models.FloatField(blank=True, null=True)
    phase1 = models.FloatField(blank=True, null=True)
    phase2 = models.FloatField(blank=True, null=True)
    incidence1 = models.FloatField(blank=True, null=True)
    incidence2 = models.FloatField(blank=True, null=True)
    emission1 = models.FloatField(blank=True, null=True)
    emission2 = models.FloatField(blank=True, null=True)
    sub_solar_planetocentric_latitude = models.FloatField(blank=True, null=True)
    sub_solar_planetographic_latitude = models.FloatField(blank=True, null=True)
    sub_observer_planetocentric_latitude = models.FloatField(blank=True, null=True)
    sub_observer_planetographic_latitude = models.FloatField(blank=True, null=True)
    sub_solar_iau_longitude = models.FloatField(blank=True, null=True)
    sub_observer_iau_longitude = models.FloatField(blank=True, null=True)
    center_resolution = models.FloatField(blank=True, null=True)
    center_distance = models.FloatField(blank=True, null=True)
    center_phase_angle = models.FloatField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_surface_geometry__titan'


class ObsTypeImage(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    instrument_id = models.CharField(max_length=9)
    image_type_id = models.CharField(max_length=4, blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    levels = models.IntegerField(blank=True, null=True)
    greater_pixel_size = models.IntegerField(blank=True, null=True)
    lesser_pixel_size = models.IntegerField(blank=True, null=True)
    mult_obs_type_image_image_type = models.ForeignKey(MultObsTypeImageImageTypeId, models.DO_NOTHING)
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_type_image'


class ObsWavelength(models.Model):
    obs_general = models.ForeignKey(ObsGeneral, models.DO_NOTHING)
    opus_id = models.ForeignKey(ObsGeneral, models.DO_NOTHING, related_name='%(class)s_opus_id')
    volume_id = models.CharField(max_length=11)
    instrument_id = models.CharField(max_length=9)
    wavelength1 = models.FloatField(blank=True, null=True)
    wavelength2 = models.FloatField(blank=True, null=True)
    wave_res1 = models.FloatField(blank=True, null=True)
    wave_res2 = models.FloatField(blank=True, null=True)
    wave_no1 = models.FloatField(blank=True, null=True)
    wave_no2 = models.FloatField(blank=True, null=True)
    wave_no_res1 = models.FloatField(blank=True, null=True)
    wave_no_res2 = models.FloatField(blank=True, null=True)
    spec_flag = models.CharField(max_length=3)
    spec_size = models.IntegerField(blank=True, null=True)
    polarization_type = models.CharField(max_length=8)
    mult_obs_wavelength_spec_flag = models.ForeignKey(MultObsWavelengthSpecFlag, models.DO_NOTHING, db_column='mult_obs_wavelength_spec_flag')
    mult_obs_wavelength_polarization_type = models.ForeignKey(MultObsWavelengthPolarizationType, models.DO_NOTHING, db_column='mult_obs_wavelength_polarization_type')
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'obs_wavelength'


class ZZParamInfo(models.Model):
    category_name = models.CharField(max_length=150)
    name = models.CharField(max_length=87)
    form_type = models.CharField(max_length=100, blank=True, null=True)
    display = models.CharField(max_length=1)
    display_results = models.IntegerField()
    disp_order = models.IntegerField()
    label = models.CharField(max_length=240, blank=True, null=True)
    label_results = models.CharField(max_length=240, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    units = models.CharField(max_length=75, blank=True, null=True)
    intro = models.CharField(max_length=150, blank=True, null=True)
    tooltip = models.CharField(max_length=255, blank=True, null=True)
    dict_context = models.CharField(max_length=255, blank=True, null=True)
    dict_name = models.CharField(max_length=255, blank=True, null=True)
    special_query = models.CharField(max_length=15, blank=True, null=True)
    sub_heading = models.CharField(max_length=150, blank=True, null=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'param_info'


class Partables(models.Model):
    trigger_tab = models.CharField(max_length=200, blank=True, null=True)
    trigger_col = models.CharField(max_length=200, blank=True, null=True)
    trigger_val = models.CharField(max_length=60, blank=True, null=True)
    partable = models.CharField(max_length=200, blank=True, null=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'partables'


class TableNames(models.Model):
    table_name = models.CharField(max_length=60)
    label = models.CharField(max_length=60)
    display = models.CharField(max_length=1)
    disp_order = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'table_names'


class UserSearches(models.Model):
    selections_json = models.TextField()
    selections_hash = models.CharField(max_length=32)
    string_selects = models.TextField(blank=True, null=True)
    string_selects_hash = models.CharField(max_length=32, blank=True, null=True)
    units = models.TextField(blank=True, null=True)
    units_hash = models.CharField(max_length=32, blank=True, null=True)
    qtypes = models.TextField(blank=True, null=True)
    qtypes_hash = models.CharField(max_length=32, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_searches'

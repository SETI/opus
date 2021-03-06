import re
import requests

STARS = {
    '126_TAU':              (None,  'OTHER',      '126 Tau'),
    '13_LYR':               (None,  'OTHER',      '13 Lyr (R Lyr)'),
    '26_TAU':               (None,  'OTHER',      '26 Tau'),
    '28_SGR':               (None,  'OTHER',      '28 Sgr'),
    '3_CEN':                (None,  'OTHER',      '3 Cen'),
    '30_PSC':               (None,  'OTHER',      '30 Psc'),
    '56_LEO':               (None,  'OTHER',      '56 Leo'),
    'ALF_ARA':              (None,  'OTHER',      'Alp Ara'),
    'ALF_AUR':              (None,  'OTHER',      'Alp Aur (Capella)'),
    'ALF_BOO':              (None,  'OTHER',      'Alp Boo (Arcturus)'),
    'ALF_CAR':              (None,  'OTHER',      'Alp Car (Canopus)'),
    'ALF_CEN':              (None,  'OTHER',      'Alp Cen'),
    'ALF_CET':              (None,  'OTHER',      'Alp Cet'),
    'ALF_CMA':              (None,  'OTHER',      'Alp CMa (Sirius)'),
    'ALF_CMI':              (None,  'OTHER',      'Alp CMi (Procyon)'),
    'ALF_CRU':              (None,  'OTHER',      'Alp Cru'),
    'ALF01_CRU':            (None,  'OTHER',      'Alp1 Cru'),
    'ALF_ERI':              (None,  'OTHER',      'Alp Eri'),
    'ALF_HER':              (None,  'OTHER',      'Alp Her'),
    'ALF_HYA':              (None,  'OTHER',      'Alp Hya'),
    'ALF_LEO':              (None,  'OTHER',      'Alp Leo (Regulus)'),
    'ALF_LUP':              (None,  'OTHER',      'Alp Lup'),
    'ALF_LYR':              (None,  'OTHER',      'Alp Lyr (Vega)'),
    'ALF_ORI':              (None,  'OTHER',      'Alp Ori (Betelgeuse)'),
    'ALF_PAV':              (None,  'OTHER',      'Alp Pav'),
    'ALF_PSA':              (None,  'OTHER',      'Alp PsA (Fomalhaut)'),
    'ALF_SCO':              (None,  'OTHER',      'Alp Sco (Antares)'),
    'ALF_SEX':              (None,  'OTHER',      'Alp Sex'),
    'ALF_TAU':              (None,  'OTHER',      'Alp Tau (Aldebaran)'),
    'ALF_TRA':              (None,  'OTHER',      'Alp TrA'),
    'ALF_VIR':              (None,  'OTHER',      'Alp Vir (Spica)'),
    'B_CEN':                (None,  'OTHER',      'b Cen (SAO 205839)'),
    'BET_AND':              (None,  'OTHER',      'Bet And'),
    'BET_CEN':              (None,  'OTHER',      'Bet Cen'),
    'BET_CMA':              (None,  'OTHER',      'Bet CMa'),
    'BET_CRU':              (None,  'OTHER',      'Bet Cru'),
    'BET_GRU':              (None,  'OTHER',      'Bet Gru'),
    'BET_HYA':              (None,  'OTHER',      'Bet Hya'),
    'BET_LIB':              (None,  'OTHER',      'Bet Lib'),
    'BET_LUP':              (None,  'OTHER',      'Bet Lup'),
    'BET_ORI':              (None,  'OTHER',      'Bet Ori (Rigel)'),
    'BET_PEG':              (None,  'OTHER',      'Bet Peg'),
    'BET_PER':              (None,  'OTHER',      'Bet Per (Algol)'),
    'BET_PSA':              (None,  'OTHER',      'Bet PsA'),
    'BET01_SGR':            (None,  'OTHER',      'Bet1 Sgr'),
    'BET_UMI':              (None,  'OTHER',      'Bet UMi'),
    'CHI_AQR':              (None,  'OTHER',      'Chi Aqr'),
    'CHI_CEN':              (None,  'OTHER',      'Chi Cen'),
    'CHI_CYG':              (None,  'OTHER',      'Chi Cyg'),
    'DEL_AQR':              (None,  'OTHER',      'Del Aqr'),
    'DEL_CEN':              (None,  'OTHER',      'Del Cen'),
    'DEL_CET':              (None,  'OTHER',      'Del Cet'),
    'DEL_LUP':              (None,  'OTHER',      'Del Lup'),
    'DEL_OPH':              (None,  'OTHER',      'Del Oph'),
    'DEL_ORI':              (None,  'OTHER',      'Del Ori'),
    'DEL_PER':              (None,  'OTHER',      'Del Per'),
    'DEL_SCO':              (None,  'OTHER',      'Del Sco'),
    'DEL_VIR':              (None,  'OTHER',      'Del Vir'),
    'EPS_CAS':              (None,  'OTHER',      'Eps Cas'),
    'EPS_CEN':              (None,  'OTHER',      'Eps Cen'),
    'EPS_CMA':              (None,  'OTHER',      'Eps CMa'),
    'EPS_LUP':              (None,  'OTHER',      'Eps Lup'),
    'EPS_MIC':              (None,  'OTHER',      'Eps Mic'),
    'EPS_MUS':              (None,  'OTHER',      'Eps Mus'),
    'EPS_ORI':              (None,  'OTHER',      'Eps Ori'),
    'EPS_PEG':              (None,  'OTHER',      'Eps Peg'),
    'EPS_PER':              (None,  'OTHER',      'Eps Per'),
    'EPS_PSA':              (None,  'OTHER',      'Eps PsA'),
    'EPS_SGR':              (None,  'OTHER',      'Eps Sgr'),
    'ETA_CAR':              (None,  'OTHER',      'Eta Car'),
    'ETA_CMA':              (None,  'OTHER',      'Eta CMa'),
    'ETA_LUP':              (None,  'OTHER',      'Eta Lup'),
    'ETA_SGR':              (None,  'OTHER',      'Eta Sgr'),
    'ETA_UMA':              (None,  'OTHER',      'Eta UMa'),
    'G_CEN':                (None,  'OTHER',      '2 Cen'),
    'G_HER':                (None,  'OTHER',      '30 Her'),
    'GAM_AND':              (None,  'OTHER',      'Gam And'),
    'GAM_ARA':              (None,  'OTHER',      'Gam Ara'),
    'GAM_CAS':              (None,  'OTHER',      'Gam Cas'),
    'GAM_CNC':              (None,  'OTHER',      'Gam Cnc'),
    'GAM_COL':              (None,  'OTHER',      'Gam Col'),
    'GAM_CRU':              (None,  'OTHER',      'Gam Cru'),
    'GAM_ERI':              (None,  'OTHER',      'Gam Eri'),
    'GAM_GRU':              (None,  'OTHER',      'Gam Gru'),
    'GAM_LUP':              (None,  'OTHER',      'Gam Lup'),
    'GAM_ORI':              (None,  'OTHER',      'Gam Ori'),
    'GAM_PEG':              (None,  'OTHER',      'Gam Peg'),
    'HD_205905':            (None,  'OTHER',      'HD 205905'),
    'HD_339479':            (None,  'OTHER',      'HD 339479'),
    'HD_37962':             (None,  'OTHER',      'HD 37962'),
    'HD_71334':             (None,  'OTHER',      'HD 71334'),
    'IK_TAU':               (None,  'OTHER',      'NML Tau'),
    'IO_CEN':               (None,  'OTHER',      'Iot Cen'),
    'IO_ORI':               (None,  'OTHER',      'Iot Ori'),
    'IRC_+10216':           (None,  'OTHER',      'IRC +10216 (CW Leo)'),
    'KAP_CEN':              (None,  'OTHER',      'Kap Cen'),
    'KAP01_CET':            (None,  'OTHER',      'Kap1 Cet'),
    'KAP_CMA':              (None,  'OTHER',      'Kap CMa'),
    'KAP_ORI':              (None,  'OTHER',      'Kap Ori'),
    'KAP_SCO':              (None,  'OTHER',      'Kap Sco'),
    'KAP_VEL':              (None,  'OTHER',      'Kap Vel'),
    'KSI01_CET':            (None,  'OTHER',      'Xi Cet'),
    'KSI02_CET':            (None,  'OTHER',      'Xi2 Cet'),
    'L2_PUP':               (None,  'OTHER',      'L2 Pup'),
    'LAM_AQL':              (None,  'OTHER',      'Lam Aql'),
    'LAM_AQR':              (None,  'OTHER',      'Lam Aqr'),
    'LAM_CET':              (None,  'OTHER',      'Lam Cet'),
    'LAM_SCO':              (None,  'OTHER',      'Lam Sco'),
    'LAM_TAU':              (None,  'OTHER',      'Lam Tau'),
    'LAM_VEL':              (None,  'OTHER',      'Lam Vel'),
    'LMC_303':              (None,  'OTHER',      'LMC 303'),
    'MU_CEN':               (None,  'OTHER',      'Mu Cen'),
    'MU_CEP':               (None,  'OTHER',      'Mu Cep'),
    'MU_GEM':               (None,  'OTHER',      'Mu Gem'),
    'MU_PSA':               (None,  'OTHER',      'Mu PsA'),
    'MU_SCO':               (None,  'OTHER',      'Mu Sco'),
    'MU_SGR':               (None,  'OTHER',      'Mu Sgr'),
    'NU_CEN':               (None,  'OTHER',      'Nu Cen'),
    'NU_VIR':               (None,  'OTHER',      'Nu Vir'),
    'OME_VIR':              (None,  'OTHER',      'Ome Vir'),
    'OMI_CET':              (None,  'OTHER',      'Omi Cet'),
    'PI.01_GRU':            (None,  'OTHER',      'Pi1 Gru'),
    'PI.04_ORI':            (None,  'OTHER',      'Pi4 Ori'),
    'PSI_CEN':              (None,  'OTHER',      'Psi Cen'),
    'R_AQL':                (None,  'OTHER',      'R Aqu'),
    'R_AQR':                (None,  'OTHER',      'R Aqr'),
    'R_CAR':                (None,  'OTHER',      'R Car'),
    'R_CAS':                (None,  'OTHER',      'R Cas'),
    'R_DOR':                (None,  'OTHER',      'R Dor'),
    'R_HYA':                (None,  'OTHER',      'R Hya'),
    'R_LEO':                (None,  'OTHER',      'R Leo'),
    'RHO_PER':              (None,  'OTHER',      'Rho Per'),
    'RS_CNC':               (None,  'OTHER',      'RS Cnc'),
    'RW_LMI':               (None,  'OTHER',      'RW LMi'),
    'RX_LEP':               (None,  'OTHER',      'RX Lep'),
    'S_LEP':                (None,  'OTHER',      'S Lep'),
    'SIG_SGR':              (None,  'OTHER',      'Sig Sgr'),
    'T_CEP':                (None,  'OTHER',      'T Cep'),
    'TET_ARA':              (None,  'OTHER',      'The Ara'),
    'TET_CAR':              (None,  'OTHER',      'The Car'),
    'TET_HYA':              (None,  'OTHER',      'The Hya'),
    'TET02_TAU':            (None,  'OTHER',      '78 Tau'),
    'TX_CAM':               (None,  'OTHER',      'TX Cam'),
    'V_HYA':                (None,  'OTHER',      'V Hya'),
    'VX_SGR':               (None,  'OTHER',      'VX Sgr'),
    'VY_CMA':               (None,  'OTHER',      'VY CMa'),
    'W_AQL':                (None,  'OTHER',      'W Aql'),
    'W_HYA':                (None,  'OTHER',      'W Hya'),
    'X_OPH':                (None,  'OTHER',      'X Oph'),
    'ZET_CEN':              (None,  'OTHER',      'Zet Cen'),
    'ZET_CMA':              (None,  'OTHER',      'Zet CMa'),
    'ZET_OPH':              (None,  'OTHER',      'Zet Oph'),
    'ZET_ORI':              (None,  'OTHER',      'Zet Ori'),
    'ZET_PER':              (None,  'OTHER',      'Zet Per'),
    'ZET_PUP':              (None,  'OTHER',      'Zet Pup'),
}

session = requests.Session()

radec_pat = re.compile(r'Coordinates.ICRS,ep=J2000,eq=2000.: (\d+) (\d+) (\d+.\d+|\d+) +(\+|-)(\d+) (\d+) (\d+.\d+|\d+)')
simbad_pat = re.compile(r'Object ([\*\+\. a-zA-Z0-9]+) ---')
name_pat = re.compile(r'NAME (\w+)')

for key in STARS:
    id = key.replace('_', ' ')
    url = 'http://simbad.u-strasbg.fr/simbad/sim-id'
    if id == 'LMC 303':
        id = '@3114237'
    params = {
        'output.format': 'ASCII',
        'Ident': id.lower()
    }
    r = session.get(url, params=params)
    match = radec_pat.search(r.text)
    if match is None:
        print('FAIL', id)
        continue
    ra_h = int(match.group(1))
    ra_m = int(match.group(2))
    ra_s = float(match.group(3))
    dec_sign = match.group(4)
    dec_d = int(match.group(5))
    dec_m = int(match.group(6))
    dec_s = float(match.group(7))

    # simbad_match = simbad_pat.search(r.text)
    # if simbad_match is None:
    #     print('FAIL', key)
    #     print(r.text[:200])
    #     continue
    # simbad = simbad_match.group(1)
    # if simbad.startswith('V*'):
    #     simbad = simbad[2:]
    # if simbad.startswith('*'):
    #     simbad = simbad[1:]
    # simbad = simbad.strip().strip(' ').replace(' ', '_')
    # simbad = simbad.upper()
    # if simbad[2:4] == '._':
    #     simbad = simbad.replace('.', '')
    # if simbad != key:
    #     print(simbad_match.group(1))
    #     print('OFFICIAL', simbad, 'US', key)
    #
    # name_match = name_pat.search(r.text)
    # if name_match is not None:
    #     our_name = ''
    #     if '(' in STARS[key][2]:
    #         our_name = STARS[key][2][STARS[key][2].index('(')+1:-1]
    #     print(key, our_name, '/', name_match.group(1))

    ra = (ra_h + ra_m/60. + ra_s/60./60.) * 360. / 24.
    dec = dec_d + dec_m/60. + dec_s/60./60.
    if dec_sign == '-':
        dec = -dec
    print('    %-24s(%13.9f, %13.9f),' % (f"'{key}':", ra, dec))

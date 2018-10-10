#####################################################################################
# Global variables
#####################################################################################
Abort                           = bytearray(1)
Abort[0]                        = 0         # to signal to abort

######################################################################################
# General definitions for Database functions
######################################################################################
DATE_FORMATTING         = '%m/%d/%Y %H:%M:%S'
DATE_FORMATTING_FILE    = '%m%d%Y_%H%M%S'        
DATE_CREATION_UTC_KEY   = 'date_created_utc'
DATE_CREATION_LOCAL_KEY = 'date_created'
RSLT_STN_INFO_KEY       = 'Result Station Info'
RSLT_DEV_INFO_KEY       = 'Result Device Info'

######################################################################################
# General definitions for logs object functions
######################################################################################
LOG_FILENAME        = 'filename'
LOG_MESSAGE         = 'message'
LOG_DATE_FORMATTING = '%Y-%m-%d %H:%M:%S:%f'
LOG_DEBUG_FILENAME  = 'debug.log'
LOG_INFO_FILENAME   = 'info.log'
LOG_ERROR_FILENAME  = 'error.log'
LOG_FAIL_FILENAME   = 'fail.log'
LOG_DATAGRAM_SIZE_MAX = 512

######################################################################################
# Mail
######################################################################################

TE = "wayne.ren@nxp.com"

######################################################################################
# Linux commands
######################################################################################
CMD_SED_ADD_SPACE        = "sed -e 's/^/ /g' "
CMD_SED_REMOVE_PARATHESE = "sed -e 's/([^()]*)//g' "
CMD_TR_CSV_CONVERSION    = " tr -s '[:blank:]' ',' "
CMD_TR_REMOVE_COMMA      = "tr -s , "
CMD_MAIL_TEST            = "/bin/mailx -s 'Test' wayne.ren@nxp.com waynegeorgehoney@gmail.com < " \
                           "/home/nxf08418/PycharmProjects/test/mailbody"
CMD_MAIL_SEND            = "/bin/mailx -a ../data/TT.png  -s 'Test Time by Module' wayne.ren@nxp.com < /dev/null"
CMD_MAIL_ATTACH          = "/bin/mailx -a"
CMD_RM_REMOVE_TEMP       = "rm -rf "

######################################################################################
# Module name for each job
######################################################################################
MODULE_NAME_K118_FR    = ('OSL', 'JTAG', 'NVM_S', 'SCAN', 'NVM_M', 'RAM', 'PMC_T', 'PMC', 'SRTC', 'SCG_T', 'SCG', 'ANL',
                          'ADC', 'ADC_R', 'TEMP_S', 'MT', 'GPIO', 'IDD', 'LEAK', 'LPSPI', 'NVM_E', 'FCV', 'LEAK', 'JVT')

MODULE_NAME_K118_QR    = ('OSL', 'JTAG', 'NVM_S', 'SCAN', 'NVM_M', 'RAM', 'PMC', 'SRTC', 'SCG', 'ANL', 'ADC', 'ADC_R',
                          'TEMP_S', 'MT', 'GPIO', 'IDD', 'LEAK', 'LPSPI', 'NVM_E', 'FCV', 'LEAK', 'JVT')

MODULE_NAME_K118_P1    = ('OSL', 'CRES', 'JTAG', 'SCAN', 'NVM_S', 'NVM_M', 'RAM', 'PMC_T', 'PMC', 'SRTC', 'SCG_T',
                          'SCG', 'ANL', 'ADC', 'MT', 'POSt', 'IDD', 'HVST_1', 'HVST', 'HVST_2', 'PMC_p', 'SRTC_p',
                          'SCG_p', 'ANL_p', 'ADC_p', 'IDD_p', 'SCAN_p', 'RAM_p', 'JTAG_p', 'NVM_E1', 'PFBIU',
                          'NVM_E2', 'JVT')

MODULE_NAME_K118_P2    = ('OSL', 'CRES', 'JTAG', 'SCAN', 'NVM_S', 'NVM_M', 'RAM', 'PMC', 'SRTC',
                          'SCG', 'ANL', 'ADC', 'MT', 'IDD','WLBI_N', 'WLBI_1', 'WLBI', 'WLBI_2', 'PMC_p',
                          'SRTC_p', 'SCG_p', 'ANL_p', 'ADC_p', 'IDD_p', 'SCAN_p', 'RAM_p', 'JTAG_p', 'NVM_E1', 'PFBIU',
                          'NVM_E2', 'JVT')

MODULE_NAME_K118_P3    = ('OSL', 'CRES', 'JTAG', 'SCAN', 'NVM_S', 'NVM_M', 'RAM', 'PMC', 'SRTC',
                          'SCG', 'ANL', 'ADC', 'MT', 'IDD', 'NVM_E1', 'PFBIU', 'NVM_E2', 'JVT')

MODULE_NAME_K148_FR   = ('OSL', 'NVM_S', 'SCAN', 'JTAG', 'NVM_M', 'RAM', 'LEAK', 'PMC_T', 'PMC', 'SRTC', 'SCG_T', 'SCG', 'ANL',
                          'ADC', 'ADC_R', 'TEMP_S', 'MT', 'GPIO', 'IDD', 'LPSPI', 'NVM_E1', 'PFBIU', 'NVM_E2', 'FCV', 'LEAK', 'JVT')

######################################################################################
# JOB NAME
######################################################################################

PAT_JOB_P1 = 'P1'
PAT_JOB_P2 = 'P2'
PAT_JOB_P3 = 'P3'
PAT_JOB_FR = 'FR'
PAT_JOB_QH = 'QH'
PAT_JOB_QC = 'QC'
PAT_JOB_QR = 'QR'

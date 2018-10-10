#-*- coding: utf-8 -*-
"""
    **********************************************************************
    File       : utility.py
    Author     : @Wayne
    Description: This module is used as a general module to provide
                 useful functions for Main or other modules
    IDE        : Eclipse PyDev, python3.4.3, Windows7 64bit system
                 PyCharm, python, python3.4.3, Linux Red Hat Enterprise Linux Server release 6.7 (Santiago)
    **********************************************************************  
"""
# System Module
import os
import filecmp
import json
import shutil
import csv
import openpyxl
import datetime
import inspect
import sys
import socket
import zipfile
import queue
import threading
import time
import subprocess
# Customized Module
from Constants import *
from collections import OrderedDict


def read_json_file_ordered( filename:str ) -> OrderedDict:
    '''Read a JSON file type and return it as python dictionary

    file: Json file

    Return:
        rValue - Python dictionary of the file content
    '''
    #log.debug( 'Enter Parameter: {0}'.format( filename ) )

    rValue = None
    try:
        with open( filename, 'r' ) as fhandle:
            rValue = json.load( fhandle, object_pairs_hook = OrderedDict )
    except Exception as e:
        # log.error( 'Failed to read Json file {0}. Error {1}'.format( filename, e ) )
        print('Failed to read Json file {0}. Error {1}'.format(filename, e))
    # end try

    #log.debug( 'Exit' )
    return rValue
# end function

def read_json_file( filename:str ) -> dict:
    '''Read a JSON file type and return it as python dictionary

    file: Json file

    Return:
        rValue - Python dictionary of the file content
    '''
    #log.debug( 'Enter Parameter: {0}'.format( filename ) )

    rValue = None
    try:
        with open( filename, 'r' ) as fhandle:
            rValue = json.load(fhandle)
    except Exception as e:
        # log.error( 'Failed to read Json file {0}. Error {1}'.format( filename, e ) )
        print('Failed to read Json file {0}. Error {1}'.format(filename, e))
    # end try

    #log.debug( 'Exit' )
    return rValue
# end function

def write_json_file(filename: str, InfoDict: dict) -> bool:
    '''Write a JSON file type from an OrderedDict or python dictionary

    filename: Filename with json file extension
    InfoDict: OrderedDict or python dictionary to be written as json file type

    Return:
        rValue - Python dictionary of the file content
    '''
    #log.debug( 'Enter Parameter: {0}'.format( filename ) )

    indent = 4
    fhPerm = 'w+'

    try:
        with open(filename, fhPerm) as fh:
            json.dump(InfoDict, fh, indent=indent)
        # end with
    except Exception as e:
        print('Failed to write to Json file. Exception encountered {0}'.format(e))
        return False
    # end if

    #log.debug( 'Exit' )
    return True
# end function

def run_linux_command(cmd_str:str) -> bool:

    rValue = False

    try:
        subprocess.call(cmd_str, shell=True)
        rValue = True
    except:
        print('Error')
    return rValue

def run_linux_command_popen(cmd_list:list) -> bool:

    rValue = False
    p = subprocess.Popen(cmd_list)
    p.wait()
    if p.returncode:
        print('**********Erorr captured*********')
        print('The error code is {code_number}'.format(code_number=p.returncode))
    else:
        rValue = True
        print('\n')
        print('Linux command * {0} * is executed successfully'.format(' '.join(cmd_list)))
    return rValue


def read_excel_file(filename:str) -> list:
    """read excel file and put content into a list
       For timing being, we just read column A and put the value into a list
    """
    list_A = list()  # Pattern Name
    list_B = list()  # Pattern Type
    list_C = list()  # Pattern Category
    list_D = list()  # Description
    list_E = list()  # Vault
    list_F = list()  # Tag
    list_O = list()  # Test_Setup_Pattern
    list_P = list()  # Test_End_Pattern
    list_Y = list()  # Core Voltage
    list_Z = list()  # DAC word
    
    workbook = openpyxl.load_workbook(filename = filename)
    scan_sheet = workbook.get_sheet_by_name("Scan")
    
    cells_A = scan_sheet['A']
    cells_B = scan_sheet['B']
    cells_C = scan_sheet['C']
    cells_D = scan_sheet['D']
    cells_E = scan_sheet['E']
    cells_F = scan_sheet['F']
    cells_O = scan_sheet['O']
    cells_P = scan_sheet['P']
    cells_Y = scan_sheet['Y']
    cells_Z = scan_sheet['Z']
    
    for c in cells_A:
        list_A.append(c.value)
    
    for c in cells_B:
        list_B.append(c.value)
        
    for c in cells_C:
        list_C.append(c.value)
    
    for c in cells_D:
        list_D.append(c.value)
        
    for c in cells_E:
        list_E.append(c.value)
    
    for c in cells_F:
        list_F.append(c.value)
        
    for c in cells_O:
        list_O.append(c.value)
    
    for c in cells_P:
        list_P.append(c.value)
        
    for c in cells_Y:
        list_Y.append(c.value)
    
    for c in cells_Z:
        list_Z.append(c.value)
        
    rValue = [list_A , list_B, list_C, list_D, list_E, list_F, list_O, list_P, list_Y, list_Z]
    
    return rValue

def read_text_file(fname:str) -> list:
    """read text file and put content into a list 
    """
    with open(fname, 'r') as f:
        rValue = f.readlines()
    return rValue

def write_text_file(olist:list, fname:str) -> bool:
    """write text file
    """ 
    rValue = False
    try:
        with open(fname, 'w+') as f:
            for row in range(len(olist)):
                f.write(olist[row])
                f.write('\n')
    except:
        return rValue
            
    rValue = True
    return rValue

def write_text_file_PatSet(olist:list, fname:str) -> bool:
    """write PatSet text file which is used to import into 
       IGXL based test program 
    """
    
    rValue = False
    try:
        with open(fname, 'w+') as f:
            f.write(PATSET_1_ROW + TAB + PATSET_TITLE + NL)
            f.write(NL)
            f.write(PATSET_3_ROW)
            for row in range(len(olist)):
                f.write(olist[row])
                f.write('\n')
    except:
        return rValue
            
    rValue = True
    return rValue

def write_text_file_Ins(olist:list, fname:str) -> bool:
    """write Instance text file which is used to import into
       IGXL based test program 
    """
    
    rValue = False
    try:
        with open(fname, 'w+') as f:
            f.write(INS_1_ROW + TAB + INS_TITLE + NL)
            f.write(NL)
            f.write(INS_3_ROW)
            f.write(INS_4_ROW)
            for row in range(len(olist)):
                f.write(olist[row])
                f.write('\n')
    except:
        return rValue
            
    rValue = True
    return rValue 

def write_text_file_Flw(olist:list, fname:str) -> bool:
    """write Instance text file which is used to import into
       IGXL based test program 
    """
    
    rValue = False
    try:
        with open(fname, 'w+') as f:
            f.write(FLW_1_ROW + TAB + INS_TITLE + NL)
            f.write(FLW_2_ROW)
            f.write(FLW_3_ROW)
            f.write(FLW_4_ROW)
            for row in range(len(olist)):
                f.write(olist[row])
                f.write('\n')
    except:
        return rValue
            
    rValue = True
    return rValue

def read_csv_file(filename:str) -> list:
    """read csv file and put content into a list 
    """
    rValue = list()
    with open (filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile,delimiter = TAB)
        for row in csv_reader:
            rValue.append(row)
    return rValue

def write_csv_file(cbo_list:list,filename:str) -> bool:
    """write csv file based on the list provided
    """
    rValue = True
    rows = len(cbo_list)
    if not rows:
        rValue = False
        
    with open (filename,'w+', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for i in range(rows):
            csv_writer.writerow(cbo_list[i])    
    return rValue

def DictR_csv_file(filename:str, fieldname:list) -> list:
    """read csv file and put content into a dict 
    """
    rValue = list()
    with open(filename, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter = TAB)
        for row in csv_reader:
            rValue.append(row)
             
    return rValue

# def DictW_csv_file(filename:str, fieldname:list, cbo_list:list,outputfield:list) -> bool:
#     """read csv file and put content into a dict 
#     """
#     rValue = True
#     rows = len(cbo_list)
#     if not rows:
#         rValue = False
#         
#     with open(filename, 'w+', newline='') as csvfile:
#         csv_writer = csv.DictWriter(csvfile, fieldnames = fieldname, delimiter = TAB)
#         csv_writer.writeheader()
#         for i in range(rows):
#             csv_writer.writerow(cbo_list[i])
#             
#     return rValue

def list_rm_duplicates(seq:list, idfun=None) -> list:
    """Remove duplicates in the list
    """
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen : continue
        seen[marker] = 1
        result.append(item)
    return result

def diff_text_files(src_dir:str, dest_dir:str) -> list:
    """Compare every two files in source directory,
       find all the different files and copy all of 
       them into destination directory you refer to.
       In the end, we will remove all the text files
       of the source folder.
        
       src_dir: source directory
       dest_dir: destination directory

       return: True if succeed
               False if fail
    """
    
    txt_list = list()
    for file in os.listdir(src_dir):
        if file.endswith(".txt"):
            txt_list.append(file)

    diff_list = txt_list.copy()
    txt_qty = len(txt_list)
    
    for i in range(txt_qty-1, 0 , -1):
        for j in range(i):
            cmp_file1 = src_dir + '\\' + txt_list[j]
            cmp_file2 = src_dir + '\\' + txt_list[i]
            result = filecmp.cmp(cmp_file1, cmp_file2, False)
            if result:
                if txt_list[j] in diff_list:
                    diff_list.remove(txt_list[j])
    
    if not diff_list:
        return None
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    for txt_file in diff_list:
        txt_file = src_dir + '\\' + txt_file
        if os.path.isfile(txt_file):
            shutil.copy(txt_file, dest_dir)
    
    for txt_file in txt_list:
        txt_file = src_dir + '\\' + txt_file
        os.remove(txt_file)
    
    return diff_list

def MySleep( sleeptime:float ):
    """Sleep and prevent Control-C interrupt

    sleeptime: in second

    return: none
    """
    #log.debug( 'Enter {0} sec'.format( sleeptime ) )

    try:
        time.sleep( sleeptime )
    except:
        pass

    #log.debug( 'Exit' )
    return


class logs( object ):

    # Class attribute ( Global )
    clientAddress     = () # Tuple
    Streamer_loglevel = [] # List

    log_message_queue = queue.Queue( maxsize = 0 ) # Queue
    log_thread_semaphore = threading.Semaphore( value = 0 ) # Semaphore
    log_thread = None # Thread

    log_thread_started_event = threading.Event()
    log_thread_ended_event = threading.Event()
    event_wait_time = 10

    debug_filename = LOG_DEBUG_FILENAME
    info_filename  = LOG_INFO_FILENAME
    error_filename = LOG_ERROR_FILENAME
    fail_filename  = LOG_FAIL_FILENAME

    output_screen_flag = True
    output_debug_flag  = True
    output_info_flag   = True
    output_error_flag  = True
    output_fail_flag   = True

    def __init__( self ):
        ''' Constructor function initializes all variables used throughout the
        class
        '''
        self.logger_name = ''
        self.func_name   = ''
        self.class_name  = ''
    # end __init__

    def initialize( self,
                    loglevel = 5,
                    keepOldLogs = True,
                    keepOldAgeMaxDays = 5,
                    createNewLogs = True ) -> bool:
        """ Initialize logs thread. Attempts to store the previous log files
            to an archive directory. Starts the log thread
        Input   : None
        Return  : True: logs files are initialized
                  False: logs files are Failed to initialized
        """
        rValue = True

        # Files used for logging
        osPathSep     = os.path.sep
        scriptName    = sys.argv[ 0 ]
        scriptDirName = os.path.dirname( scriptName )
        scriptAbsPath = os.path.abspath( scriptDirName )
        logs.debug_filename = scriptAbsPath + osPathSep + logs.debug_filename
        logs.info_filename  = scriptAbsPath + osPathSep + logs.info_filename
        logs.error_filename = scriptAbsPath + osPathSep + logs.error_filename
        logs.fail_filename  = scriptAbsPath + osPathSep + logs.fail_filename

        # How much logging
        if ( type( loglevel ) == type( 1 ) and loglevel >= 0 ):
            self.processLoglevel( loglevel = loglevel )
        # end if

        if keepOldLogs:
            if not self.keep_old_logfiles( scriptAbsPath = scriptAbsPath,
                                           logMaxAge = keepOldAgeMaxDays ):
                print( 'Failed in storing older files in archive directory' )
            # end if
        # end if

        if createNewLogs:
            if not self.create_log_files():
                print( 'Failed creating new log files' )
                if ( type( loglevel ) == type( 1 ) and loglevel == 0 ):
                    print( 'Log level is set to not require logging to files.' +
                           ' Creating new files failed although bypassed' )
                else:
                    print( 'Return value will be false' )
                    rValue = False
                # end if
            # end if
        # end if

        # Start log thread
        logs.log_thread = threading.Thread( target = logs.log_thread_work,
                                            daemon = True ) # Thread
        logs.log_thread.start()

        # Event returns true if the flag has been set by thread starting
        #   returns false if timeout is hit
        if logs.log_thread_started_event.wait( timeout = logs.event_wait_time ):
            if not logs.is_log_thread_alive():
                print( 'Failed to start log thread, even though start event' +
                       'was set to true' )
                rValue = False
            # end if
        else:
            print( 'Failed to start log thread, start event ' +
                   'flag wait timeoutof {int1} ' +
                   'expired'.format( int1 = logs.event_wait_time  ) )
            rValue = False
        # end if

        return rValue
    # end function

    def is_log_thread_alive():
        if logs.log_thread.is_alive():
            return True
        else:
            return False
        # end if
    # end function

    def log_thread_work():
        ''' Life of the log thread. Wait for log message to be placed in
            queue and semaphore or finish signal
        '''
        # Let initializing function know we have started
        logs.log_thread_started_event.set()

        while True:
            with logs.log_thread_semaphore:
                filename_message = logs.log_message_queue.get()
                if filename_message:
                    logs._write2file( filename_message = filename_message)
                else:
                    break
            # end with log_thread_semaphore
        # end while

        logs.log_thread_ended_event.set()
        print( '"logs" thread exiting' )
    # end function

    def log_thread_kill( timeout = 60 ):
        logs.log_message_queue.put( False )
        logs.log_thread_semaphore.release()

        logs.log_thread_ended_event.wait( timeout = timeout )
    # end function

    def _write2file( filename_message:dict ):
        try:
            with open( filename_message[ LOG_FILENAME ], 'a' ) as fh:
                #fh.write( filename_message[ LOG_MESSAGE ] + os.linesep )
                fh.write( filename_message[ LOG_MESSAGE ] + '\n' )
            # end with
        except Exception as e:
            print( str.format( 'Error: Log Error or I/O error {excp1}',
                   excp1 = e ) )
        # end try
    # end function

    def screenOutput( self, message ):
        if logs.output_screen_flag:
            print( message )
        # end if
    # end function

    def keep_old_logfiles( self, scriptAbsPath:str, logMaxAge:int ):
        rValue = True
        osPathSep = os.path.sep
        archivePath = scriptAbsPath + osPathSep + 'Archive'


        # What to do with old log files, if any
        #   Check if archive folder exist
        if not os.path.exists( archivePath ):
            os.makedirs( archivePath )
        # end if

        # Check if archive folder exist one more time
        if not os.path.exists( archivePath ):
            print ( 'Did not find "Archive" folder as expected. Cannot ' +
                    'store previous log files, if any' )
        else:
            # Updating Archive folder
            old_log_files =  os.listdir( archivePath )

            print( "Deleting old file please wait ..." )
            for old_file in old_log_files:
                old_file_path = archivePath + osPathSep + old_file
                try:
                    # Getting file info
                    file_Stat = FileStat( old_file_path )
                    file_Stat.stat()
                except:
                    print( 'log.Initialize: error: Failed to get file info: ' +
                            old_file )
                    rValue = False

                # Delete log file its older than log_age from archive folder
                if ( file_Stat.age_in_days() >= logMaxAge ):
                    os.remove( old_file_path )
            # end for

            # Backing up existing logs
            print( 'Backing up existing log files please wait ...' )
            zip_file_name = archivePath + osPathSep + \
                            time.strftime( '%Y%m%d-%H%M%S' ) + '.zip'

            log_file_list = ( logs.info_filename,  logs.debug_filename,
                              logs.error_filename, logs.fail_filename )

            for existing_file in log_file_list:
                if not os.path.isfile( existing_file ):
                    continue
                # end if

                if not self.compress_file( existing_file, zip_file_name ):
                    print( 'Failed to compress file ' +
                           '{str1} to zip'.format( str1 = existing_file) )
            # end for

        # end if

        return rValue
    # end function

    def create_log_files( self ):
        rValue = True

        log_file_list = ( logs.info_filename,  logs.debug_filename,
                          logs.error_filename, logs.fail_filename )

        for new_file in log_file_list:
            try:
                open( new_file, 'w' ).close()
            except:
                print( 'Failed to clean/create log file ' +
                       '{str1}'.format( str1 = new_file ) )
                rValue = False
        # end for

        return rValue
    # end function

    def debug( self, message ):
        """
        Purpose : Write message on debug.log
        Input   : message to write ,logger name
        Return  : None
        """
        if "debug" in logs.Streamer_loglevel:
            self.streamer( message )
        # end if

        self.__updateInfo()

        if logs.output_debug_flag:
            timestamp = datetime.datetime.now().strftime( LOG_DATE_FORMATTING )

            # String format is specific to DEBUG file
            # Adding timestamp, log object initializing location,
            #   calling function class name (if any), calling function
            # Python "String Formatting Operations"
            # - : The converted value is left adjusted (overrides the '0'
            #       conversion if both are given).
            # s : Converts any Python object using str
            msg2w = '%-18s %-18s %s%s %s ' % ( timestamp,
                                               self.logger_name,
                                               self.class_name,
                                               self.func_name,
                                               message )

            logs.log_message_queue.put( { "filename": logs.debug_filename,
                                          "message" : msg2w } )
            logs.log_thread_semaphore.release()
        # end if

        # Output to screen
        self.screenOutput( '{str1}{str2} {str3}'.format( str1 = self.class_name,
                                                         str2 = self.func_name,
                                                         str3 = message ) )
    # end function debug

    def info( self, message ):
        """
        Purpose : Write on console and append message on info.log
        Input   : message to write ,Logger Name
        Return  : None
        """
        if "info" in logs.Streamer_loglevel:
            self.streamer(message)
        # end if

        if logs.output_info_flag:
            timestamp = datetime.datetime.now().strftime( LOG_DATE_FORMATTING )

            # String format is used by Info, Error, Fail functions
            # Python "String Formatting Operations"
            # - : The converted value is left adjusted (overrides the '0'
            #       conversion if both are given).
            # s : Converts any Python object using str
            msg2w = '%-18s %-18s %5s ' % ( timestamp, self.logger_name, message )

            logs.log_message_queue.put( { "filename": logs.info_filename,
                                          "message" : msg2w } )
            logs.log_thread_semaphore.release()
        # end if

        # Output to debug file
        self.debug( message )

    # end function info

    def error( self, message ):
        """
        Purpose : Write on console and append message on error.log
        Input   : message to write , logger name
        Return  : None
        """
        # Add error string prefix
        message =  'Error: {str1}'.format( str1 = message )

        if "error" in logs.Streamer_loglevel:
            self.streamer( message )
        # end if

        if logs.output_error_flag:
            timestamp = datetime.datetime.now().strftime( LOG_DATE_FORMATTING )

            # String format is used by Info, Error, Fail functions
            # Python "String Formatting Operations"
            # - : The converted value is left adjusted (overrides the '0'
            #       conversion if both are given).
            # s : Converts any Python object using str
            msg2w = '%-18s %-18s %5s ' % ( timestamp, self.logger_name, message )

            logs.log_message_queue.put( { "filename": logs.error_filename,
                                          "message" : msg2w } )
            logs.log_thread_semaphore.release()
        # end if

        # Output to info file
        self.info( message )

    # end function error

    def fail( self, message ):
        """
        Purpose : Write on console and append message on fail.log
        Input   : message to write , logger name
        Return  : None
        """
        # Add fail string prefix
        message =  'Fail: {str1}'.format( str1 = message )

        if "fail" in logs.Streamer_loglevel:
            self.streamer( message )
        # end if

        if logs.output_fail_flag:
            timestamp = datetime.datetime.now().strftime( LOG_DATE_FORMATTING )

            # String format is used by Info, Error, Fail functions
            # Python "String Formatting Operations"
            # - : The converted value is left adjusted (overrides the '0'
            #       conversion if both are given).
            # s : Converts any Python object using str
            msg2w = '%-18s %-18s %5s ' % ( timestamp, self.logger_name, message )

            logs.log_message_queue.put( { "filename": logs.fail_filename,
                                          "message" : msg2w } )
            logs.log_thread_semaphore.release()
        # end if

        # Output to info file
        self.info( message )
    # end function fail

    def compress_file( self, fname, zname ) -> bool:
        """
        Purpose : Compress the log files
        Input   : filename and zipfilename
        Return  : True: Compressed
                  False: failed to compressed
        """
        try:
            self.zipf = zipfile.ZipFile( zname, 'a' )
            self.zipf.write( fname, arcname = os.path.basename( fname ) )
            self.zipf.close()
        except:
            print( 'log.compress_file: error: Failed to compress file ' +
                    fname )
            return False
        return True
    # end function

    def streamer( self, message:str ):
        """
        Purpose : Stream the log info to server end
        Input   : log info
        Return  : none
        """
        try:
            send_sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            self.error( 'Failed to create socket object' )
        except Exception as e:
            self.error( str.format( 'Failed to create socket due to: ' +
                        'error {excp1}', excp1 = e ) )
        # end try

        sizeOfMessage = sys.getsizeof( message )

        if ( sizeOfMessage < LOG_DATAGRAM_SIZE_MAX ):
            message = message.encode('utf-8')

            try:
                send_sock.sendto( message, logs.clientAddress)
            except socket.error:
                self.error( str.format( 'Failed to stream info on host: {list1}',
                            list1 = logs.clientAddress ) )
            except Exception as e:
                self.error( str.format( 'Failed to stream info on host due to: ' +
                            'error {excp1}', excp1 = e ) )
            # end try
        else:
            choppedMsgList = []
            okSizeCharList = []
            for singChar in message:
                okSizeCharList.append( singChar )
                tempMsg = ''.join( okSizeCharList )

                if ( ( sys.getsizeof( tempMsg ) + 32 ) < LOG_DATAGRAM_SIZE_MAX ):
                    continue
                # end if

                choppedMsgList.append( tempMsg )
                okSizeCharList = [] # Reset the list char holder

            # end for

            lastMsg = ''.join( okSizeCharList )
            if ( lastMsg.strip() != '' ):
                choppedMsgList.append( lastMsg )
            # end if

            for choppedMsg in choppedMsgList:
                message = choppedMsg.encode('utf-8')
                try:
                    send_sock.sendto( message, logs.clientAddress)
                except socket.error:
                    self.error( str.format( 'Failed to stream info on host: {tup1}',
                                tup1 = logs.clientAddress ) )
                except Exception as e:
                    self.error( str.format( 'Failed to stream info on host due to: ' +
                                'error {excp1}', excp1 = e ) )
                # end try
            # end for
    # end function

    def __updateInfo( self ):
        """
        Purpose : Updates the stored values for class and function that called
                 the logger. Should call before every write to a log file
        Input   : None
        Return  : None
        """
        # get the previous frame ( method ) in order to get the
        # function and class name. two f_back due to consolidation
        # into one __updateInfo function
        cf = inspect.currentframe().f_back.f_back
        if 'self' in cf.f_locals:
            self.class_name = cf.f_locals[ 'self' ].__class__.__name__ + '.'
        # end if
        self.func_name = cf.f_code.co_name + '()'

        # for the classname...try just using class instead.
        # "{0}.{1}".format(a.__class__.__module__,a.__class__.__name__)
        #http://stackoverflow.com/questions/510972/getting-the-class-name-of-an-instance-in-python

        # this handles any function outside of the main function
        # that is not encapsulated by a class.
        if self.class_name == 'logs.':
            self.class_name = ""
        # end if

    # end function

    def processLoglevel( self, loglevel:int ):
        ''' Determines log flags based on loglevel int
        '''
        if   loglevel == 0:
            logs.output_screen_flag = False
            logs.output_debug_flag  = False
            logs.output_info_flag   = False
            logs.output_error_flag  = False
            logs.output_fail_flag   = False
        elif loglevel == 1:
            logs.output_screen_flag = True
            logs.output_debug_flag  = False
            logs.output_info_flag   = False
            logs.output_error_flag  = False
            logs.output_fail_flag   = False
        elif loglevel == 2:
            logs.output_screen_flag = True
            logs.output_debug_flag  = False
            logs.output_info_flag   = True
            logs.output_error_flag  = False
            logs.output_fail_flag   = False
        elif loglevel == 3:
            logs.output_screen_flag = True
            logs.output_debug_flag  = False
            logs.output_info_flag   = True
            logs.output_error_flag  = True
            logs.output_fail_flag   = False
        elif loglevel == 4:
            logs.output_screen_flag = True
            logs.output_debug_flag  = False
            logs.output_info_flag   = True
            logs.output_error_flag  = True
            logs.output_fail_flag   = True
        elif loglevel == 5:
            logs.output_screen_flag = True
            logs.output_debug_flag  = True
            logs.output_info_flag   = True
            logs.output_error_flag  = True
            logs.output_fail_flag   = True
        elif loglevel == 6:
            logs.output_screen_flag = False
            logs.output_debug_flag  = True
            logs.output_info_flag   = True
            logs.output_error_flag  = True
            logs.output_fail_flag   = True
        else:
            logs.output_screen_flag = True
            logs.output_debug_flag  = True
            logs.output_info_flag   = True
            logs.output_error_flag  = True
            logs.output_fail_flag   = True
        # end if
    # end function

# end class logs

class FileStat(object):
    'Operation on file like get size,file time,compress etc..'

    def __init__( self, fname ):
        self.fname = fname
        self._stat = None



    def stat( self ):
        if self._stat is None:
            # Note: This will not update automatically if your file's stats change
            self._stat = os.stat( self.fname )
        return self._stat



    def datetime( self ):
        return datetime.datetime.fromtimestamp( self._stat.st_mtime )



    def age_in_days( self ):
        today = datetime.datetime.today()
        cday = self.datetime()
        return ( today - cday ).days

    def age_in_seconds( self ):
        today = datetime.datetime.today()
        cday = self.datetime()
        return ( today - cday ).seconds


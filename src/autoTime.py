"""
******************************************************************************
Author     : Wayne
Date       : Dec 1st, 2018
Description: This script is used to automatically analyze test time

NXP Inc. All rights reserved
******************************************************************************
"""

# Customized Module
import Utilities
import Constants
# from Constants import *
from collections import Counter
# System Module
import os
import re
import sys
import json
import argparse
from collections import Counter
from termcolor import colored
import signal
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import traceback

""" Disable Log Setup
# local variables
# log = utilities.logs() # calling log calls as object
# log.logger_name = os.path.basename(__file__)
log = Utilities.logs()  # calling log calls as object
log.logger_name = os.path.basename(__file__)

# Initialize logs
if not log.initialize():
    log.error('Failed to initialize main log ' +
              'class {}'.format(log.logger_name))
    Utilities.MySleep(1)

def handler(signum, frame):
    log.debug('Signal handler called with signal 0x{0:02X}'.format(
        signum))
    Abort[0] = 1
"""

if __name__ == "__main__":
    # signal.signal(signal.SIGINT, handler)

    """Command Line Parsing
    """
    parser = argparse.ArgumentParser('Test Time Analysis')
    parser.add_argument('-t', metavar='device', type=str, default='S32K118',
                        help='Which target device needed for test time analysis (default: %(default)s)')
    parser.add_argument('-s', metavar='selection', required=True, type=str, default='P1',
                        help='selection of the test program job (required)')
    parser.add_argument('-f', metavar='format', type=str, default='png',
                        help='Which format needed for the time data (default: %(default)s)')
    parser.add_argument('-v', metavar='version', required=True, type=str, default='ENG_V1',
                        help='version of the test program for traceability (required)')
    args = parser.parse_args()

    print("\n", colored("         *********************************************************", "cyan"))
    print("\n", colored("         ************************TE Automation********************", "cyan"))
    print("\n", colored("         **********************Test Time Analysis*****************", "cyan"))
    print("\n", colored("         *********************************************************", "cyan"))

    script_dir = os.getcwd()
    config_dir = os.path.dirname(script_dir) + '/config'
    data_dir = os.path.dirname(script_dir) + '/data'
    json_dir = os.path.dirname(script_dir) + '/json'
    print(colored('Current working directory is {dir}'.format(dir=script_dir), "green"))
    print('Data directory is {dir}'.format(dir=data_dir))

    """Check CVS FILE EXISTENCE
    """
    tt_txt_list = list()

    for file in os.listdir(data_dir):
        if file.endswith(".txt") or file.endswith(".csv"):
            tt_txt_list.append(file)
    print('The File List in data directory: {lst}'.format(lst=tt_txt_list))

    if args.t.upper()+"_"+args.s.upper()+".csv" in tt_txt_list:
        print(colored('The {file} csv file exists already'.format(file=args.t.upper() + '_' + args.s.upper()), "red"))
        print(colored('Quit Program', "red"))
        sys.exit(0)

    """CSV Conversion and Formatting
    """
    for each in tt_txt_list:
        re_Job = re.search(args.t.upper(), each)
        re_P1 = re.search(Constants.PAT_JOB_P1, each)
        re_P2 = re.search(Constants.PAT_JOB_P2, each)
        re_P3 = re.search(Constants.PAT_JOB_P3, each)
        re_QR = re.search(Constants.PAT_JOB_QR, each)
        re_FR = re.search(Constants.PAT_JOB_FR, each)

        if re_Job and re_P1:
            os.rename(data_dir + '/' + each, data_dir + '/' + args.t.upper() + "_P1.txt")
        if re_Job and re_P2:
            os.rename(data_dir + '/' + each, data_dir + '/' + args.t.upper() + "_P2.txt")
        if re_Job and re_P3:
            os.rename(data_dir + '/' + each, data_dir + '/' + args.t.upper() + "_P3.txt")
        if re_Job and re_QR:
            os.rename(data_dir + '/' + each, data_dir + '/' + args.t.upper() + "_QR.txt")
        if re_Job and re_FR:
            os.rename(data_dir + '/' + each, data_dir + '/' + args.t.upper() + "_FR.txt")

    if args.s.upper() in ["P1", "P2", "P3", "QR", "FR"]:

        Utilities.run_linux_command(Constants.CMD_SED_ADD_SPACE + "../data/" + args.t.upper() + "_" + args.s.upper()
                                    + ".txt" + "> ../data/temp.txt")
        Utilities.run_linux_command("cat ../data/temp.txt | " + Constants.CMD_TR_CSV_CONVERSION + "> ../data/temp1.csv")
        Utilities.run_linux_command(Constants.CMD_SED_REMOVE_PARATHESE + "../data/temp1.csv" + "> ../data/temp2.csv")
        Utilities.run_linux_command(Constants.CMD_TR_REMOVE_COMMA + "< ../data/temp2.csv > " + "../data/"
                                    + args.t.upper() + "_" + args.s.upper() + ".csv")
        Utilities.run_linux_command(Constants.CMD_RM_REMOVE_TEMP + "../data/temp*")
        print(colored('CSV File {file} has been generated'.format(file=args.t.upper() + "_" + args.s.upper() + ".csv"),
                      "green"))
    else:
        print(colored('The arg {arg} you typed in is not valid'.format(arg=args.s.upper()), "red"))
        sys.exit(0)

    dir_list_conversion = os.listdir(data_dir)
    print('The File List in data directory after conversion: {lst}'.format(lst=dir_list_conversion))

    """Module split and Time Calculation
    """
    # with open(args.t.upper()+"_"+args.s.upper()+".csv", "r") as in_file:
    #     buf = in_file.readlines()
    #
    # with open(args.t.upper()+"_"+args.s.upper()+".csv", "w") as out_file:
    #     for line in buf:
    #         if line[1:15] == "ModuleTestTime":
    #             line = line + "\n"
    #         out_file.write(line)

    # Module Time
    lst_MT = []
    # Module Count
    lst_MC = []
    with open(data_dir+"/" + args.t.upper()+"_"+args.s.upper()+".csv", "r") as in_file:
        listOfLines = in_file.read().splitlines()
        sumTT = 0
        count = 0
        for i in range(2, len(listOfLines)-4, 1):
            aLine = listOfLines[i]
            if aLine != '':
                lineItems = aLine.split(',')
                nameData = lineItems[1]
                timeData = lineItems[3]
                if nameData != 'ModuleTestTime':
                    sumTT = sumTT + float(timeData)
                    count = count + 1
                if nameData == 'ModuleTestTime':
                    sumTT_formatted = round(sumTT, 2)
                    lst_MT.append(sumTT_formatted)
                    lst_MC.append(count)
                    sumTT = float(timeData)
                    count = 1
            else:
                print(colored('Missing time data;Please check CSV file', "red"))

    """Bar Plot Display
    """
    N = len(lst_MT)
    print("There are {n} modules".format(n=N))
    print(lst_MT)
    tpl_MT = tuple(lst_MT)
    # Need to make branch here
    if args.t.upper()+"_"+args.s.upper() == 'S32K118_FR':
        tpl_MN = Constants.MODULE_NAME_K118_FR
    elif args.t.upper()+"_"+args.s.upper() == 'S32K118_QR':
        tpl_MN = Constants.MODULE_NAME_K118_QR
    elif args.t.upper()+"_"+args.s.upper() == 'S32K118_P1':
        tpl_MN = Constants.MODULE_NAME_K118_P1
    elif args.t.upper()+"_"+args.s.upper() == 'S32K118_P2':
        tpl_MN = Constants.MODULE_NAME_K118_P2
    elif args.t.upper()+"_"+args.s.upper() == 'S32K118_P3':
        tpl_MN = Constants.MODULE_NAME_K118_P3
    elif args.t.upper()+"_"+args.s.upper() == 'S32K148_FR':
        tpl_MN = Constants.MODULE_NAME_K148_FR
    else:
        tpl_MN = ()
    lst_MN = list(tpl_MN)
    dict_result = dict(zip(lst_MN, lst_MT))
    print(dict_result)

    TT_job = tpl_MT
    ind = np.arange(N)  # the x locations for the module groups
    width = 0.8  # the width of the bars: can also be len(x) sequence
    if args.s.upper() == 'P1' or args.s.upper() == 'FR' or args.s.upper() =='QR':
        f1 = plt.bar(ind, TT_job, width, align='center', color='green')
    elif args.s.upper() == 'P2' or args.s.upper() == 'QH':
        f1 = plt.bar(ind, TT_job, width, align='center', color='red')
    elif args.s.upper() == 'P3' or args.s.upper() == 'QC':
        f1 = plt.bar(ind, TT_job, width, align='center', color='blue')
    plt.ylabel('Test Time')
    plt.title(args.t.upper()+" "+args.s.upper()+' Test Time by Module')
    plt.xticks(ind, tpl_MN)
    plt.xticks(rotation=90)
    if args.s.upper() == 'P1':
        plt.yticks(np.arange(0, max(lst_MT)+1, 2))
    elif args.s.upper() == 'P2':
        plt.yticks(np.arange(0, max(lst_MT)+1, 10))
    else:
        plt.yticks(np.arange(0, max(lst_MT)+1, 1))
    plt.ylabel('time(unit: second)')
    plt.xlabel('module name')
    # # plt.legend((f1[0]), loc='upper left')
    for rect in f1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height, '%.2f' % float(height), ha='center', va='bottom',
                 fontsize=5)
    # Horizontally trial
    # for i, v in enumerate(lst_MT):
    #     plt.text(v + 3, i + .25, str(v), color='blue', fontweight='bold')

    # plt.show()
    plt.tight_layout()
    plt.savefig(data_dir+'/'+args.t.upper()+"_"+args.s.upper()+"."+args.f, dpi=300, format=args.f, bbox_inches='tight')

    # Write result in mail config
    f = open(config_dir + "/" + "mail.txt", 'r+')
    f.truncate(0)  # need '0' when using r+

    # json_result = dict()
    # json_result[args.v.upper()] = dict_result
    json_result = {args.t.upper()+"_"+args.s.upper()+"_"+args.v.upper(): dict_result}
    Utilities.write_json_file(json_dir + "/" + args.t.upper() + "_" + args.s.upper() + "_" + args.v.upper() +
                              ".json", json_result)

    with open(config_dir + "/" + "mail.txt", "w") as out_file:
        out_file.write('Dear,\n')
        out_file.write('\n')
        out_file.write('This mail is automatically generated by script and '
                       'used to notify TE and PE about ' + args.t.upper() + " " + args.s.upper() +
                       ' test time information.\n')
        out_file.write('\n')
        out_file.write(json.dumps(json_result))
        out_file.write('\n\n')
        out_file.write('Best Regards\n')
        out_file.write('Wayne')

    # Send Mail
    print(colored('Sending mail with png file to {tolist}'.format(tolist=Constants.TE), "green"))
    Utilities.run_linux_command(Constants.CMD_MAIL_ATTACH+data_dir+"/"+args.t.upper()+"_" + args.s.upper()+"."+args.f
                                + " -s " + "'Test Time by Module' "+Constants.TE+"< "+config_dir+"/"+"mail.txt")


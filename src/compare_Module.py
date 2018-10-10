"""
******************************************************************************
Author     : Wayne
Date       : Dec 1st, 2018
Description: This script is used to automatically analyze test time

NXP Inc. All rights reserved
******************************************************************************
"""
import os
import Utilities
import Constants
import argparse
from termcolor import colored
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

    """Command Line Parsing
        """
    parser = argparse.ArgumentParser('Test Time Analysis')
    parser.add_argument('-t', metavar='device', type=str, default='S32K118',
                        help='Which target device needed for test time analysis (default: %(default)s)')
    parser.add_argument('-s', metavar='selection', required=True, type=str, default='P1',
                        help='selection of the test program job (required)')
    parser.add_argument('-cm', metavar='compare', required=True, nargs='+',
                        help='version of the test program for traceability (required)')
    args = parser.parse_args()

    script_dir = os.getcwd()
    config_dir = os.path.dirname(script_dir) + '/config'
    data_dir = os.path.dirname(script_dir) + '/data'
    json_dir = os.path.dirname(script_dir) + '/json'
    db_dir = os.path.dirname(script_dir) + '/database'
    print(colored('Current working directory is {dir}'.format(dir=script_dir), "green"))
    print('Data directory is {dir}'.format(dir=data_dir))

    target_dict = Utilities.read_json_file(db_dir + "/" + args.t.upper() + ".json")
    target_dict = target_dict[args.t.upper()]
    module_dict_1 = target_dict[args.t.upper()+"_"+args.s.upper()+"_"+args.cm[0]]
    module_dict_2 = target_dict[args.t.upper()+"_"+args.s.upper()+"_"+args.cm[1]]

    # Modify below code to get what you want:
    N = 8
    ind = np.arange(N)
    width = 0.3
    fig = plt.figure()
    ax = fig.add_subplot(111)

    time_tpl_1 = (module_dict_1["OSL"], module_dict_1["CRES"], module_dict_1["JTAG"], module_dict_1["SCAN"],
                  module_dict_1["NVM_S"], module_dict_1["NVM_M"], module_dict_1["RAM"], module_dict_1["PMC"])
    rects1 = ax.bar(ind, time_tpl_1, width, color='royalblue')

    time_tpl_2 = (module_dict_2["OSL"], module_dict_1["CRES"], module_dict_2["JTAG"], module_dict_2["SCAN"],
                  module_dict_2["NVM_S"], module_dict_1["NVM_M"], module_dict_2["RAM"], module_dict_2["PMC"])
    rects2 = ax.bar(ind+width, time_tpl_2, width, color='seagreen')

    # add some
    ax.set_ylabel('time(unit: second)')
    ax.set_title(args.t.upper() + " " + args.cm[0] + ' vs ' + args.cm[1])
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(("OSL", "CRES", "JTAG", "SCAN", "NVM_S", "NVM_M", "RAM", "PMC"))

    ax.legend((rects1[0], rects2[0]), (args.cm[0], args.cm[1]))

    for rect in rects1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height, '%.2f' % float(height), ha='right', va='bottom',
                 fontsize=8)
    for rect in rects2:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height, '%.2f' % float(height), ha='left', va='bottom',
                 fontsize=8)
    plt.show()
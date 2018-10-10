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
import argparse
from termcolor import colored

if __name__ == "__main__":

    """Command Line Parsing
    """
    parser = argparse.ArgumentParser('Test Time Analysis')
    parser.add_argument('-t', metavar='device', type=str, default='S32K118',
                        help='Which target device needed for test time analysis (default: %(default)s)')
    args = parser.parse_args()

    script_dir = os.getcwd()
    config_dir = os.path.dirname(script_dir) + '/config'
    data_dir = os.path.dirname(script_dir) + '/data'
    json_dir = os.path.dirname(script_dir) + '/json'
    db_dir = os.path.dirname(script_dir) + '/database'
    print(colored('Current working directory is {dir}'.format(dir=script_dir), "green"))
    print('Data directory is {dir}'.format(dir=data_dir))

    json_lst = []
    for file in os.listdir(json_dir):
        if file.endswith(".json"):
            json_lst.append(file)
    # print(json_lst)

    target_lst = []
    for each_json in json_lst:
        if each_json.startswith(args.t.upper()):
            target_lst.append(each_json)
    print(target_lst)

    target_dict = dict()
    for each in target_lst:
        ref = Utilities.read_json_file(json_dir + "/" + each)
        print('*****')
        print(ref)
        print('*****')
        target_dict.update(ref)
    print(target_dict)

    db_dict = dict()
    db_dict[args.t.upper()] = target_dict
    """Write to json which is used as database
    """
    Utilities.write_json_file(db_dir + "/" + args.t.upper() + ".json", db_dict)

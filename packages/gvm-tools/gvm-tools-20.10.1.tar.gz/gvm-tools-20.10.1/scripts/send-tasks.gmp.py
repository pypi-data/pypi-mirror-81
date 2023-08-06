# -*- coding: utf-8 -*-
# Copyright (C) 2018-2019 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
from lxml import etree as e


def check_args(args):
    len_args = len(args.script) - 1
    if len_args is not 1:
        message = """
        This script pulls tasks data from an xml document and feeds it to \
    a desired GSM
        One parameter after the script name is required.

        1. <xml_doc>  -- .xml file containing tasks

        Example:
            $ gvm-script --gmp-username name --gmp-password pass \
    ssh --hostname <gsm> scripts/send-tasks.gmp.py example_file.xml
        """

        print(message)
        quit()


def error_and_exit(msg):
    print("\nError: {}\n".format(msg), file=sys.stderr)
    sys.exit(1)


def inquire_yes_no(inquiry):
    reply = str(input(inquiry + ' [Y/n]: ')).lower().strip()
    if reply == 'y':
        answer = True
    elif reply == 'n':
        answer = False
    else:
        answer = inquire_yes_no("Please enter valid option dummy!")

    return answer


def numerical_option(statement, list_range):
    choice = int(input(statement))

    if choice in range(1, list_range + 1):
        return choice
    else:
        return numerical_option(
            "Please enter valid number from {} to {}...".format(1, list_range),
            list_range,
        )


def create_xml_tree(xml_doc):
    try:
        xml_tree = e.parse(xml_doc)
        xml_tree = e.tostring(xml_tree)
        xml_tree = e.XML(xml_tree)
    except IOError as err:
        error_and_exit("Failed to read xml_file: {} (exit)".format(str(err)))

    if len(xml_tree) == 0:
        error_and_exit("XML file is empty (exit)")

    return xml_tree


def interactive_options(task, keywords):
    options_dict = {}
    options_dict['config'] = gmp.get_configs()
    options_dict['scanner'] = gmp.get_scanners()
    options_dict['target'] = gmp.get_targets()

    for option in options_dict:
        object_dict, object_list = {}, []
        object_id = task.xpath('{}/@id'.format(option))[0]
        object_xml = options_dict[option]

        for i in object_xml.xpath('{}'.format(option)):
            object_dict[i.find('name').text] = i.xpath('@id')[0]
            object_list.append(i.find('name').text)

        if object_id in object_dict.values():
            keywords['{}_id'.format(option)] = object_id
        elif object_id not in object_dict.values() and len(object_dict) != 0:
            response = inquire_yes_no(
                "\nRequired Field: failed to detect {}_id: {}... "
                "\nWould you like to select from available options, or exit "
                "the script?".format(
                    option, task.xpath('{}/@id'.format(option))[0]
                )
            )

            if response is True:
                counter = 1
                print("{} options:".format(option.capitalize()))
                for j in object_list:
                    print("    {} - {}".format(counter, j))
                    counter += 1
                answer = numerical_option(
                    "\nPlease enter the number of your choice.",
                    len(object_list),
                )
                keywords['{}_id'.format(option)] = object_dict[
                    object_list[answer - 1]
                ]
            else:
                print("\nTerminating...")
                quit()
        else:
            error_and_exit(
                "Failed to detect {}_id"
                "\nThis field is required therefore the script is unable to "
                "continue.\n".format(option)
            )


def parse_send_xml_tree(gmp, xml_tree):
    for task in xml_tree.xpath('task'):
        keywords = {'name': task.find('name').text}

        if task.find('comment').text is not None:
            keywords['comment'] = task.find('comment').text

        interactive_options(task, keywords)

        new_task = gmp.create_task(**keywords)

        mod_keywords = {'task_id': new_task.xpath('//@id')[0]}

        if task.find('schedule_periods') is not None:
            mod_keywords['schedule_periods'] = int(
                task.find('schedule_periods').text
            )

        if task.find('observers').text:
            mod_keywords['observers'] = task.find('observers').text

        if task.xpath('schedule/@id')[0]:
            mod_keywords['schedule_id'] = task.xpath('schedule/@id')[0]

        if task.xpath('preferences/preference'):
            preferences, scanner_name_list, value_list = {}, [], []

            for preference in task.xpath('preferences/preference'):
                scanner_name_list.append(preference.find('scanner_name').text)
                if preference.find('value').text is not None:
                    value_list.append(preference.find('value').text)
                else:
                    value_list.append('')
            preferences['scanner_name'] = scanner_name_list
            preferences['value'] = value_list
            mod_keywords['preferences'] = preferences

        if task.xpath('file/@name'):
            file = dict(
                name=task.xpath('file/@name'), action=task.xpath('file/@action')
            )

            mod_keywords['file'] = file

        if len(mod_keywords) > 1:
            gmp.modify_task(**mod_keywords)


def main(gmp, args):
    # pylint: disable=undefined-variable
    check_args(args)
    xml_doc = args.script[1]

    print('\nSending task(s)...')

    xml_tree = create_xml_tree(xml_doc)
    parse_send_xml_tree(gmp, xml_tree)

    print('\n  Task(s) sent!\n')


if __name__ == '__gmp__':
    main(gmp, args)

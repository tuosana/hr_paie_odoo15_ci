##############################################################################
#
# Copyright (c) 2012 Veone - support.veone.net
# Author: Veone
#
# Fichier du module hr_emprunt_old
# ##############################################################################
{
    "name" : "Congés automatiques",
    "version" : "1.0",
    "author" : "SM",
    "category" : "Human Resources",
    "website" : "www.bdo-fwa.com",
    "depends" : ['hr_holidays_extension'],
    "description": """ Ce module permet d'attribuer de façon automatqiue les congés annuels des employés
    """,
    "init_xml" : [],
    "demo_xml" : [],
    "data": [
        'data/cron_view.xml',
        'views/res_config_settings_view.xml',
    ],
    "installable": True
}

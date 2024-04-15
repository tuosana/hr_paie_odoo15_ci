##############################################################################
#
# Copyright (c) 2012 Veone - jonathan.arra@gmail.com
# Author: Jean Jonathan ARRA
#
# Fichier du module hr_synthese
# ##############################################################################
{
    "name" : "Mise à jour HR de Odoo",
    "version" : "1.0",
    "author" : "Jean Jonathan ARRA(VEONE)",
    'category': 'Localization',
    "depends" : ["base", 'hr', 'hr_contract'],
    "description": """
    """,
    "data":[
            "security/ir.model.access.csv",
            #"views/res_config_settings_views.xml",
            "data/abatements_data.xml",
            "data/categories_employee_data.xml",
            "views/hr_category_employee_view.xml",
            "views/hr_category_salaire_view.xml",
            "views/res_company_view.xml",
            "views/res_partner_view.xml",
            "views/hr_employee_view.xml",
            "views/hrDepartmentView.xml",
        ],
    "web.assets_backend": [
            "/hr_update/static/src/legacy/scss/layout_style.scss",
        ],
    "installable": True
}

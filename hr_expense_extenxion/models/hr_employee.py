#-*- coding:utf-8 -*-


from odoo import api, fields, models, exceptions, _

Type_employee = [('h', 'Horaire'), ('j', 'Journalier'), ('m', 'Mensuel')]

class EmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    expense_manager_id = fields.Many2one('res.users', readonly=True)
    first_name = fields.Char("Prénoms", required=False)
    category_id = fields.Many2one('hr.contract.category', 'Catégorie', required=False)
    type = fields.Selection(Type_employee, 'Type', required=False, default=False)
    matricule_cnps = fields.Char('N° CNPS', size=64)
    enfants_a_charge = fields.Integer("Nombre d'enfants à charge", required=True)
    start_date = fields.Date("Date d'ancienneté", required=True)
    end_date = fields.Date("Date de depart", required=False)
    enfants_ids = fields.One2many('hr.employee.enfant', 'employee_id', 'Enfants', required=False)
    licence_ids = fields.One2many('hr.licence', 'employee_id', 'Licences des employés')
    diplome_ids = fields.One2many('hr.diplomes.employee', 'employee_id', 'Diplôme des employés')
    visa_ids = fields.One2many('hr.visa', 'employee_id', 'Visas des employés')
    carte_sejour_ids = fields.One2many('hr.carte.sejour', 'employee_id', 'Carte de séjour des employés')
    date_entree = fields.Date("Date d'entrée")
    # piece_identite_id = fields.Many2one("hr.piece.identite", "Pièce d'identité")
    presonnes_contacted_ids = fields.One2many('hr.personne.contacted', 'employee_id', 'Personnes à contacter')
    parent_employee_ids = fields.One2many("hr.parent.employe", 'employee_id', 'Les parents')
    recruitment_degree_id = fields.Many2one('hr.employee.degree', "Niveau d'étude")
    direction_id = fields.Many2one('hr.department', 'Direction', required=False, domain="[('type', '=', 'direction')]")
    department_id = fields.Many2one('hr.department', 'Departement', required=False,
                                    domain="[('type', '=', 'department')]")
    service_id = fields.Many2one('hr.department', 'Service', Required=True, domain="[('type', '=', 'service')]")
    conjoint_complete_name = fields.Char(string="Nom complet du conjoint", groups="hr.group_hr_user")
    conjoint_birthdate = fields.Date(string="Date de naissance du conjoint", groups="hr.group_hr_user")
    nature_employe = fields.Selection([('local', 'Local'), ('expat', 'Expatrié')], "Nature de l'employé",
                                      default=False)
    num_cmu_conjoint = fields.Char('N° CMU conjoint', required=False)
    timesheet_manager_id = fields.Many2one('res.users', string='Timesheet',
                                           help="User responsible of timesheet validation. Should be Timesheet Manager.")
    cni_number = fields.Char("N° carte d'identité", required=False)

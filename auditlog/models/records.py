from odoo import models


class AuditlogRecords(models.Model):
    _inherit = 'auditlog.rule'
    _description = 'Create dynamic records for the rules'


    def init(self):
        self._clean_lines()
        self._generate_lines()


    def _generate_lines(self) -> None:
        """
        Generate rule lines automatically when installing or updating the app
        Terms that included in excluded_terms list gives an error
        """
        # excluded_terms = ['wizard', 'base', '.assets', '.test', '.tour', 'auditlog', 'ir.', 'bus.']
        excluded_terms = ['wizard', 'base', 'auditlog', 'ir.', 'bus.']
        for model in self._get_model_list():
            if all(term not in model.model for term in excluded_terms):
                self.create({
                    'name': model.display_name,
                    'model_id': model.id,
                    'state': 'subscribed'
                })


    def _get_model_list(self):
        """
        Return the installed models
        """
        return self.env['ir.model'].search([])


    def _clean_lines(self) -> None:
        """
        Remove lines to enable update after a new module is installed
        """
        for rule in self.search([]):
            rule.unlink()

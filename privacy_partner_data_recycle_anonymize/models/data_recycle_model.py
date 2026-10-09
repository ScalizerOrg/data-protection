# Copyright 2026 Scalizer
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError

ANONYMIZABLE_MODELS = ("res.partner", "res.users")


class DataRecycleModel(models.Model):
    _inherit = "data_recycle.model"

    recycle_action = fields.Selection(
        selection_add=[("anonymize", "Anonymize")],
        # Never fall back to the "Delete" default on uninstall
        ondelete={"anonymize": "cascade"},
    )

    @api.constrains("recycle_action", "res_model_id")
    def _check_recycle_action_anonymize(self):
        """Restrict anonymization rules to contacts and users, set up by
        anonymization administrators only."""
        rules = self.filtered(lambda rule: rule.recycle_action == "anonymize")
        if not rules:
            return
        if not self.env.su and not self.env.user.has_group(
            "privacy_partner_to_be_forgotten.group_partner_anonymize"
        ):
            raise AccessError(_("You don't have permission to anonymize partners."))
        if any(rule.res_model_name not in ANONYMIZABLE_MODELS for rule in rules):
            raise ValidationError(_("Only contacts and users can be anonymized."))

# Copyright 2026 Scalizer
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import models


class DataRecycleRecord(models.Model):
    _inherit = "data_recycle.record"

    def action_validate(self):
        """Anonymize the contacts behind records of anonymization rules.

        The standard method then just drops these recycle records, as it
        neither archives nor deletes records of an unknown action.
        """
        to_anonymize = self.filtered(
            lambda rec: rec.recycle_model_id.recycle_action == "anonymize"
        )
        partners = self.env["res.partner"].sudo()
        for record in to_anonymize._original_records():
            partners |= record if record._name == "res.partner" else record.partner_id
        # Same "already anonymized" marker as the OCA anonymization wizard
        for partner in partners.filtered(
            lambda p: not (p.email or "").endswith("@anonymized.oca")
        ):
            partner.anonymize_partner_data()
        return super().action_validate()

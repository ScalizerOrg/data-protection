# Copyright 2026 Scalizer
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import models


class DataRecycleRecord(models.Model):
    _inherit = "data_recycle.record"

    def _get_partners_to_process(self, recycle_action):
        """Contacts behind the records of the given rule action."""
        records = self.filtered(
            lambda rec: rec.recycle_model_id.recycle_action == recycle_action
        )
        partners = self.env["res.partner"].sudo()
        for record in records._original_records():
            partners |= record if record._name == "res.partner" else record.partner_id
        return partners

    def action_validate(self):
        """Anonymize the contacts, or remove their messages, behind records
        of anonymization rules.

        Messages are left to the "Remove Messages" rules, so that both steps
        can be scheduled separately. The standard method then just drops these
        recycle records, as it neither archives nor deletes records of an
        unknown action.
        """
        partners = self._get_partners_to_process("anonymize")
        # Same "already anonymized" marker as the OCA anonymization wizard
        for partner in partners.filtered(
            lambda p: not (p.email or "").endswith("@anonymized.oca")
        ):
            partner.with_context(anonymize_keep_messages=True).anonymize_partner_data()
        for partner in self._get_partners_to_process("remove_messages"):
            partner._anonymize_partner_messages()
        return super().action_validate()

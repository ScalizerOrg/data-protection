# Copyright 2026 Scalizer
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _anonymize_partner_messages(self):
        """Keep messages when anonymizing from an "Anonymize" rule, they are
        removed by a separate "Remove Messages" rule."""
        if self.env.context.get("anonymize_keep_messages"):
            return
        return super()._anonymize_partner_messages()

# Copyright 2026 Scalizer
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo.exceptions import AccessError, ValidationError
from odoo.tests.common import TransactionCase, new_test_user, tagged


@tagged("post_install", "-at_install")
class TestDataRecycleAnonymize(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Eric Cartman",
                "email": "eric@southpark.com",
                "phone": "+1 123-456-7891",
                "street": "28 Bonanza St",
                "city": "South Park",
            }
        )
        cls.user = new_test_user(cls.env, login="kenny", name="Kenny McCormick")

    def _create_rule(self, model_xmlid, records, mode="automatic"):
        return self.env["data_recycle.model"].create(
            {
                "name": "Anonymize",
                "res_model_id": self.env.ref(model_xmlid).id,
                "recycle_action": "anonymize",
                "recycle_mode": mode,
                "domain": str([("id", "in", records.ids)]),
                "time_field_id": False,
            }
        )

    def test_anonymize_partner_automatic(self):
        self._create_rule("base.model_res_partner", self.partner)._recycle_records()
        self.assertFalse(self.partner.active)
        self.assertEqual(self.partner.name, "EC Anonymized")
        self.assertTrue(self.partner.email.endswith("@anonymized.oca"))
        self.assertFalse(self.partner.phone or self.partner.street)

    def test_anonymize_partner_manual(self):
        rule = self._create_rule("base.model_res_partner", self.partner, "manual")
        rule._recycle_records()
        self.assertEqual(self.partner.name, "Eric Cartman")
        rule.recycle_record_ids.action_validate()
        self.assertEqual(self.partner.name, "EC Anonymized")
        self.assertFalse(rule.recycle_record_ids)

    def test_anonymize_user(self):
        partner = self.user.partner_id
        self._create_rule("base.model_res_users", self.user)._recycle_records()
        self.assertFalse(self.user.active)
        self.assertTrue(self.user.login.endswith("@anonymized.oca"))
        self.assertEqual(partner.name, "KM Anonymized")

    def test_skip_already_anonymized(self):
        self.partner.anonymize_partner_data()
        name = self.partner.name
        rule = self._create_rule("base.model_res_partner", self.partner)
        rule.include_archived = True
        rule._recycle_records()
        self.assertEqual(self.partner.name, name)

    def test_anonymize_other_model_forbidden(self):
        with self.assertRaises(ValidationError):
            self._create_rule("base.model_res_country", self.env.ref("base.fr"))

    def test_anonymize_rule_requires_group(self):
        admin = new_test_user(self.env, login="admin2", groups="base.group_system")
        with self.assertRaises(AccessError):
            self.env["data_recycle.model"].with_user(admin).create(
                {
                    "name": "Anonymize",
                    "res_model_id": self.env.ref("base.model_res_partner").id,
                    "recycle_action": "anonymize",
                }
            )

# Copyright 2026 Scalizer
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

{
    "name": "Privacy Partner Data Recycle Anonymize",
    "version": "18.0.1.1.0",
    "development_status": "Beta",
    "category": "Data Protection",
    "summary": "Anonymize contacts and users in bulk with Data Recycle rules",
    "author": "Scalizer, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/data-protection",
    "depends": ["data_recycle", "privacy_partner_to_be_forgotten"],
    "data": ["views/data_recycle_model_views.xml"],
}

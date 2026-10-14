Adds two actions to Data Recycle rules on Contacts and Users:

- **Anonymize**: anonymizes the records with the right to be forgotten logic
  of `privacy_partner_to_be_forgotten` (contact, related users and
  attachments). Messages are kept.
- **Remove Messages**: deletes the messages of the contacts (on the contact,
  authored by or sent to them, and in their discussion channels).

Both run manually or automatically by the Data Recycle cron, so message
removal can be scheduled separately from anonymization, or not at all.

1. Go to *Data Cleaning > Configuration > Recycle Records Rules*.
2. Create a rule on the *Contact* or *User* model and choose the
   *Anonymize* action.
3. Set the filter and time field to target the records to anonymize.
   Tick *Include Archived* to also anonymize archived records.
4. In *Manual* mode, validate the records to anonymize from the rule;
   in *Automatic* mode, the Data Recycle cron anonymizes them.

Only users of the *Anonymize Contacts / Administrator* group can set up an
anonymization rule. Anonymization is irreversible.

.. :changelog:

Release History
===============

2.0.0 (2018-08-03)
++++++++++++++++++

- Birth of air-quota ✨🍰✨

**Improvements**

- Implement `AmadeusQuotaChecker` class to extract number of remaining tickets and EMDs
  from Amadeus direct stock offices via Amadeus Web Services (Header SOAP4.0).
- Implement `SirenaQuotaChecker` class to make quota check flow for Amadeus and Sirena the same.
- Redesign quota check flow with new classes.

**Bugfixes**

- Fix verification of recipient email. AWS SES check is case-sensitive.
- Add forgotten account parameter `alert` into conf sample.
- Fix db test. It didn't work during the first run of tests.
- Fix alert check. Now it works correctly in case number of remaining tickets of the db entry is NULL.


1.0.1 (2018-08-02)
++++++++++++++++++

**Bugfixes**

- Supported relative location of db storage.


1.0.0 (2018-07-02)
++++++++++++++++++

* Birth!


0.0.1 (2018-06-23)
++++++++++++++++++

* Frustration
* Conception

# Vendor Connectors Guidance

This file summarizes connector options and tips for common university systems.

1. Banner / Ellucian (SIS)
- Integration options: direct DB access (if hosted on-prem), ODBC, or APIs (Ellucian Ethos). Many installations use Oracle or MS SQL Server.
- Recommended: Use CDC (Debezium) if DB access is allowed; otherwise use Ethos APIs or scheduled extracts.
- Notes: Work with Registrar to map student identifiers and consent rules.

2. PeopleSoft / Workday (HR)
- Workday: API-first SaaS; use Workday REST APIs with polling or event-based webhooks where supported.
- PeopleSoft: DB-level CDC if accessible, or integration broker/APIs.

3. Canvas / Blackboard / Moodle (LMS)
- Canvas: provides robust REST APIs and webhooks; consider the Canvas Data service for bulk extracts.
- Blackboard: APIs or IMS LTI integrations; vendor-hosted instances may require API polling.
- Moodle: DB access or web services; support for plugin-based integrations.

4. Alma / Sierra / Ex Libris (Library)
- Many modern library systems provide APIs (REST) for circulation, items, and patron data.
- For Alma, use the Alma REST APIs and consider scheduled incremental pulls for loans and fines.

5. Custom/Legacy systems
- If no direct access: extract CSV exports, SFTP pulls, or screen-scrape as a last resort.
- Always preserve source provenance in `source_systems` metadata.

6. SaaS connectors & commercial ETL
- Airbyte, Fivetran, and Matillion have prebuilt connectors for many systems (Canvas, Workday, Workday HCM, etc.). Evaluate cost vs. engineering effort.

7. Security considerations
- Use service accounts with least-privilege.
- Never embed secrets in repository; use secrets manager or environment variables.

8. Testing and sandboxing
- Use a sandbox environment for initial integration work and avoid running CDC against production during pilot tests unless approved.


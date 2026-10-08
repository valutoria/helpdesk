# Helpdesk Odoo 20 Migration Implementation Plan

> **For agentic workers:** Execute task-by-task using the native session workflow. Validate only through remote CI and the user-authorized Kreativo test deployment; do not run local Odoo tests.

**Goal:** Make the requested helpdesk addons verifiable and functional on Odoo 20, install them on Kreativo, and retain reusable migration guidance in `~/Projects/20ce`.

**Architecture:** Keep the code migration focused on the seven requested addons. Align repository-wide CI/package metadata with the existing 20.0 branch, add regression coverage for confirmed behavior defects, then validate using remote CI and Kreativo's configured addon directories.

**Tech Stack:** Odoo 20 CE, Python 3.12, PostgreSQL, OCA addon CI conventions, JSON-RPC/Odoo module operations.

**Spec:** User-approved in-chat scope: migrate `helpdesk_mgmt`, `helpdesk_mgmt_activity`, `helpdesk_mgmt_crm`, `helpdesk_mgmt_sale`, `helpdesk_ticket_close_inactive`, `helpdesk_ticket_related`, and `helpdesk_type`; install on `https://creativo.valutoria.com` / `odoo-creativo`; save reusable tips under `~/Projects/20ce`.

## Global Constraints

- Odoo source of truth is `/home/abdulkarim/Projects/odoo20`.
- Target database is `odoo-creativo`; user-confirmed modules were uninstalled at inspection time.
- Kreativo's addon path excludes `/etc/odoo/source/20ce` itself; deploy modules to a configured category subdirectory.
- Never overwrite or discard existing user changes in `/home/abdulkarim/Projects/20ce`.
- Never install, upgrade, create a local Odoo test database, or run Odoo module tests locally.
- Kreativo is the user-authorized non-production test deployment; push the 20.0 branch to trigger its deployment, then verify remotely.

## Review Focus

- M2M command receives an integer ID, not a list: assert the action context contains `Command.link(ticket.id)`.
- Every eligible team is processed by the inactivity close method: regression-test at least two teams in one call.
- All seven module dependencies resolve together: validate install/test order includes `crm` and existing `sale`.
- CI and packaging use Odoo 20 metadata: check workflows, pylint versions, Copier answer, package versions/classifiers.
- Deployment and note-writing preserve unrelated user work: inspect scoped diffs/status before and after.

---

### Task 1: Establish regression coverage and reproduce the Odoo 20 registry failure

**Files:**
- Modify: `helpdesk_mgmt/tests/test_helpdesk_ticket.py`
- Modify: `helpdesk_mgmt_sale/tests/test_helpdesk_ticket.py`
- Modify: `helpdesk_ticket_close_inactive/tests/test_ticket_autoclose.py`

**Interfaces:**
- Consumes: Odoo 20 `Command.link(id: int)` and existing `close_team_inactive_tickets()` return payload.
- Produces: regression tests for incoming CC preservation, scalar relation IDs, and processing more than one team per call.

- [x] Extend the mail-alias ticket test to assert incoming CC is retained and merged/deduplicated on updates; confirm the Odoo 20 install fails before tests with missing `mail.thread.cc`.
- [x] Update the sale-order action-context assertion to require `Command.link(ticket.id)`.
- [x] Add a test with two independently configured teams and stale tickets to catch the early return.

### Task 2: Migrate access controls to Odoo 20 `ir.access`

**Files:**
- Modify: `helpdesk_mgmt/security/helpdesk_security.xml`
- Create: `helpdesk_mgmt/data/portal_entry_data.xml`
- Modify: `helpdesk_mgmt/views/helpdesk_ticket_templates.xml`
- Replace: `helpdesk_mgmt/security/ir.model.access.csv` with generated `security/ir.access.csv`
- Replace: `helpdesk_mgmt_crm/security/ir.model.access.csv` with `security/ir.access.csv`
- Replace: `helpdesk_type/security/ir.model.access.csv` with `security/ir.access.csv`
- Modify: the three manifests' security data-file entries

**Interfaces:**
- Consumes: Odoo 20's unified `ir.access` model; model has `group_id`, `operation`, and `domain` fields.
- Produces: equivalent Odoo 20 security permissions and restrictions for the selected addons.

- [x] Convert ACL/rule definitions with the Odoo 20 `19.4-00-ir-access` upgrade-code algorithm; inspect converter warnings and all generated access rows before applying.
- [x] Replace the Odoo 19 `portal_common_category` insertion with an Odoo 20 `portal.entry` data record; preserve the ticket counter, icon, title/description, and always-visible behavior; put the create-ticket button outside the card link.

### Task 3: Port mail CC behavior and fix confirmed code defects

**Files:**
- Modify: `helpdesk_mgmt/models/helpdesk_ticket.py`
- Modify: `helpdesk_mgmt/controllers/myaccount.py`
- Modify: `helpdesk_mgmt_activity/models/helpdesk_ticket.py`
- Modify: `helpdesk_mgmt_activity/tests/test_helpdesk_ticket.py`
- Modify: `helpdesk_mgmt/tests/test_helpdesk_portal.py`
- Modify: test base classes to supply Odoo 20's explicit `BaseCommon._test_user_groups`
- Modify: `helpdesk_mgmt/tests/test_js.py`
- Modify: selected Helpdesk QWeb/OWL XML using Odoo 20's `t-out` directive
- Modify: `helpdesk_mgmt_sale/models/helpdesk_ticket.py`
- Modify: `helpdesk_ticket_close_inactive/models/helpdesk_ticket_team.py`

**Interfaces:**
- Consumes: Task 1 regression tests and Task 2's loadable Odoo 20 helpdesk registry.
- Consumes: Task 2's Odoo 20-access-compatible addon files.
- Produces: Odoo 20 tests use explicit `BaseCommon` test-user groups, typed `ir.config_parameter` APIs, `HttpCase.csrf_token`, and the `WebSuite.test_unit_desktop(modules)` signature; Helpdesk ticket uses its Odoo 20 duration mixin and retains incoming `email_cc`; portal uses Odoo 20 `portal.entry` cards and `Model._access_domain('read')`; configurable-model lookup uses `Model.has_access('read')`; selected templates use `t-out`; sale defaults use scalar `Command.link(id)`; autoclose processes every selected team.

- [x] Port `email_cc` storage and Odoo 19 `mail.thread.cc`'s incoming-message merge behavior without adding duplicate `mail.thread` inheritance.
- [x] Replace removed `ir.rule._compute_domain()` and `ir.model.access.check()` calls with Odoo 20 `Model._access_domain()` and `Model.has_access()` equivalents.
- [x] Replace `t-esc` with `t-out` in selected backend/portal templates.
- [x] Update Odoo 20 test harness changes: typed config parameter calls, portal CSRF helper, test-user groups, and the WebSuite module argument.
- [x] Use Odoo 20's scalar `Command.link(id)` in the sale action default.
- [x] Move autoclose result aggregation outside the per-team loop and return after all teams are processed.

### Task 4: Align project metadata with the 20.0 branch

**Files:**
- Modify: `.copier-answers.yml`
- Modify: `.github/workflows/test.yml`
- Modify: `.github/workflows/pre-commit.yml`
- Modify: `.pylintrc`, `.pylintrc-mandatory`
- Modify: `setup/_metapackage/pyproject.toml`
- Modify: `README.md`

- [x] Match OCA's Odoo 20 CI conventions: Python 3.12 Odoo/OCB 20.0 containers, branch filters for `20.0`, PostgreSQL 16, and Odoo 20 Copier/lint/package versions; scope addon CI with `INCLUDE`.
- [x] Update README badges and addon version table to 20.0; align selected module README links and package pins.

### Task 5: Validate the requested addons remotely on Kreativo

**Target:** `https://creativo.valutoria.com` / `odoo-creativo` (non-production test deployment, confirmed by user).

- [ ] Push the reviewed changes to the repository's `20.0` branch; allow the configured test-cloud deployment to pull the source and wait for remote CI.
- [ ] Use Odoo MCP to refresh the module list and install the seven requested addons in dependency order (CRM installs `crm`; `sale` is already installed).
- [ ] Verify the seven module states, dependency states, and final helpdesk views on Kreativo; resolve remote install/view failures in the code and redeploy.

### Task 6: Save durable Odoo 20 migration notes

**Files:**
- Create: `/home/abdulkarim/Projects/20ce/lessons/odoo20_migration_patterns.md`
- Create: `/home/abdulkarim/Projects/20ce/AGENTS.md` (short pointer so future Odoo 20 tasks load the guide)

- [x] Document source-verified Odoo 20 APIs, remote CI metadata, addon-path rules, and this session's confirmed pitfalls; keep Odoo 19 notes unchanged.
- [x] Review `20ce` git status and preserve all pre-existing user changes.

## Verification

- No Odoo module tests or installations run locally.
- The remote Kreativo Odoo 20 module install completes for the seven requested modules and dependencies.
- `git diff --check` passes in both repositories; only intended files are modified.
- Kreativo reports the requested modules installed and no pending module operation.
- `~/Projects/20ce/lessons/odoo20_migration_patterns.md` exists and is referenced for future Odoo 20 tasks.

# QA Automation Prompt — Run Locally with Both Repos

## How to use

1. Open **Claude Code desktop app**
2. Set working directory to `H:/dev/rozeegpt-core/`
3. Copy everything between **PROMPT START** and **PROMPT END** below
4. Paste into Claude Code and run

---

## PROMPT START — Copy from here ↓

```
You are a QA automation engineer. You have access to two repos in the current directory:

- `H:/dev/rozeegpt-core/rozeegpt/` — Backend API
- `H:/dev/rozeegpt-core/rozeegptapp02/` — Frontend employer app

Your job: run a complete browser-based QA test of the **Team Management** and **Roles & Permissions** features on https://betaqa.rozeegpt.ai. When tests fail, find the root cause in the actual source code (either repo) and fix it.

---

## STEP 1 — Setup Playwright test project

Create a `qa-tests/` folder in `H:/dev/rozeegpt-core/` (sibling to both repos) and set up Playwright:

```bash
cd H:/dev/rozeegpt-core
mkdir qa-tests
cd qa-tests
npm init -y
npm install --save-dev @playwright/test
npx playwright install chromium
```

## STEP 2 — Credentials & Environment

| Item | Value |
|------|-------|
| **Sign in URL** | https://betaqa.rozeegpt.ai/employer/signin |
| **Team page** | https://betaqa.rozeegpt.ai/employer/team |
| **Roles page** | https://betaqa.rozeegpt.ai/employer/roles |
| **API base** | https://betaqa-api.rozeegpt.ai/rest/api/ |
| **Email** | mkhalid@naseebnetworks.com |
| **Password** | P@kistan1 |
| **Role** | Company Admin (full access) |

API response codes: Success = `"11"`, Failure = `"00"`, Session expired = `"421"`

Use unique timestamps for test data: `{TS}` = current `YYYYMMDD-HHmmss`

## STEP 3 — Write and run ALL 47 test cases

Write Playwright spec files and execute them IN ORDER. For each test, log PASS/FAIL/SKIP. On FAIL, investigate the source code in `rozeegpt/` (backend) or `rozeegptapp02/` (frontend) and fix.

### Module 0 — Setup & Login (3 tests)

**SETUP-001 — Sign in with test account**
1. Go to https://betaqa.rozeegpt.ai/employer/signin
2. Enter email `mkhalid@naseebnetworks.com`, password `P@kistan1`
3. Submit sign-in form
4. **Expected:** Redirect to dashboard, no error toast, session active (API calls return code "11" not "421")

**SETUP-002 — Sidebar shows Team and Roles**
1. Open sidebar
2. Locate Organization section
3. **Expected:** Both "Team" and "Roles" links visible and clickable, no "Unauthorized" page

**SETUP-003 — Navigate to Team Management**
1. Click Team in sidebar or go to `/employer/team`
2. Wait for loading to complete
3. **Expected:** Title "Team Management", 4 stat cards (Total Members, Pending Invitations, Departments, Roles in Use), tabs (Active Members, Pending, Departments, Removed), "+ Invite Member" button visible

### Module 1 — Team Page Load & Layout (4 tests)

**TEAM-001 — Stat cards match tab data**
- Active tab count N = Total Members stat
- Pending stat = Pending tab row count
- Departments stat = Departments tab row count

**TEAM-002 — Active members list renders**
- Each row: avatar, name, role badge, email
- Role dropdown, rights (sliders) icon, remove (trash) icon on manageable members
- Job access shows "All Jobs" or "N Job(s) Shared"

**TEAM-003 — Info alert and Roles link**
- "How access works" info alert at bottom of Active Members tab
- "View roles & matrix →" link opens `/employer/roles`

**TEAM-004 — Self row: cannot change own role**
- mkhalid row: role dropdown disabled with tooltip "cannot change own role"
- Sliders icon opens "My Access" (read-only)

### Module 2 — Search & Filters (3 tests)

**TEAM-010 — Search by name or email**
- Type "mkhalid" → only matching member shown
- Clear search → full list restored

**TEAM-011 — Search no results empty state**
- Search "zzzznonexistent99999"
- **Expected:** "No members found" / "Try adjusting your search or filters", no JS errors

**TEAM-012 — Role filter dropdown**
- Open "All Roles" dropdown, select "HR Recruiter"
- Only HR Recruiter members shown
- Reset to "All Roles" restores full list

### Module 3 — Invite Team Member Wizard (8 tests)

**INV-001 — Open invite modal**
- Click "+ Invite Member"
- **Expected:** Modal "Invite Team Member", step indicator (Details → Role → Access), fields (Full Name, Email, Department), Cancel + Next buttons

**INV-002 — Step 1 validation: email required**
- Leave email empty, click Next
- **Expected:** Error "Email is required", stays on step 1

**INV-003 — Step 1: fill details and advance**
- Name: `QA Tester {TS}`, Email: `qa-invite-{TS}@mailinator.com`, select department
- Click Next
- **Expected:** Advances to step 2 with role cards listed

**INV-004 — Step 2: select HR Recruiter**
- Click HR Recruiter card, click Next
- **Expected:** Step 3 shows Job Access Scope (All Jobs / Specific Jobs)

**INV-005 — Step 3: specific jobs invite**
- Select "Specific Jobs Only", pick job chips, click "Send Invitation"
- **Expected:** Toast "Invitation sent!", Pending count +1, API `TeamV2/invite` returns code "11"

**INV-006 — Invite company-wide role (HR Manager)**
- New email `qa-invite-mgr-{TS}@mailinator.com`
- Select HR Manager → step 3 shows company-wide message (no job selection)
- Send → succeeds → Revoke immediately on Pending tab

**INV-007 — Back navigation in wizard**
- Fill step 1 → step 2 → step 3, click Back twice
- **Expected:** Email/name preserved, Cancel closes without sending

**INV-008 — Duplicate invite handling**
- Try inviting same `qa-invite-{TS}@mailinator.com` again
- **Expected:** Clear error "already invited" / "already on team", API code "00"

### Module 4 — Pending Invitations (3 tests)

**PEND-001 — Pending tab populated**
- Pending tab shows invite row: email, role badge, department, "Pending" chip, Invited date, Resend + Revoke buttons

**PEND-002 — Resend invitation**
- Click Resend → toast "Invitation resent", row stays, API `TeamV2/resend` code "11"

**PEND-003 — Revoke invitation**
- Click Revoke → confirm dialog → toast "Invitation revoked", row removed, count decrements

### Module 5 — Departments (4 tests)

**DEPT-001 — Departments tab layout**
- Header "Departments", "+ Add Department" button, table: Department / Members / Actions

**DEPT-002 — Add department**
- Add `QA Dept {TS}` → toast "Department saved", new row with 0 members, stat increases

**DEPT-003 — Edit department**
- Edit pencil → rename to `QA Dept {TS} Updated` → toast "Department updated"

**DEPT-004 — Duplicate department name blocked**
- Add department with same name → error "already exists", modal stays open

### Module 6 — Active Member Actions (6 tests)

**TEAM-020 — Change member role**
- Pick non-admin, non-self member, change role (e.g. HR Recruiter → Line Manager)
- **Expected:** Toast "Role updated", badge changes, API code "11"
- **REVERT** to original role after

**TEAM-021 — Fine-tune rights modal**
- Click sliders icon on manageable member → "Fine-Tune Rights" modal
- Rights grouped with toggles matching role defaults
- Toggle one right OFF then ON → Save → toast "Rights updated"

**TEAM-022 — My Access read-only (self)**
- Click sliders on own row → "My Access" modal, toggles disabled, no Save

**TEAM-023 — Manage job access**
- Click "N Job(s) Shared" link → "Manage Job Access" modal
- Toggle All/Specific, select jobs → Save → toast "Job access updated"

**TEAM-024 — Remove member (QA test account ONLY)**
- Remove a QA test member → confirm → toast "{name} removed", gone from Active, appears on Removed tab

**TEAM-025 — Removed tab audit view**
- Removed tab: muted styling, name/email/Removed label, or "No removed members" empty state

### Module 7 — Roles & Permissions (11 tests)

**ROLE-001 — Roles page load**
- Title "Roles & Permissions", Cards/Matrix toggle, "+ Create Custom Role" button, System Roles section

**ROLE-002 — System role cards**
- Cards for: Company Admin, HR Manager, HR Recruiter, Line Manager, Interviewer, Coordinator
- Each: name, description, "Best for" text, System chip, member count, View Rights button

**ROLE-003 — View Rights modal (system role)**
- HR Recruiter → View Rights → grouped permissions, read-only toggles, "Clone as Custom Role" button

**ROLE-004 — Permissions Matrix view**
- Click "Permissions Matrix" → grid: roles as columns, permissions as rows, checkmarks

**ROLE-005 — Matrix ↔ Cards toggle**
- Switch back to "Role Cards" → renders correctly, no stale overlay

**ROLE-006 — Member count consistency**
- Sum of member counts on role cards ≈ Total Members on Team page

**ROLE-010 — Create custom role**
- "+ Create Custom Role" → name `QA Custom Role {TS}`, description, enable 3-5 rights → Save
- Toast success, appears under Custom Roles, API code "11"

**ROLE-011 — Edit custom role**
- Edit the custom role, change description/toggle → Save → persists after refresh

**ROLE-012 — Clone system role as custom**
- View Rights on Interviewer → "Clone as Custom Role" → name `QA Clone Interviewer {TS}` → Save
- New custom role with copied rights

**ROLE-013 — Delete custom role (unassigned)**
- Delete the clone role → confirm → toast "Role deleted", card removed

**ROLE-014 — Cannot delete system role**
- No delete button on system role cards, View Rights is read-only

**ROLE-015 — Invite with custom role**
- Invite `qa-custom-{TS}@mailinator.com` with `QA Custom Role {TS}` → custom role appears in step 2, invite succeeds → revoke after

### Module 8 — Negative & Guard Rails (4 tests)

**NEG-001 — Cannot remove company admin**
- Find Company Admin member → remove button disabled/missing

**NEG-002 — Invalid email on invite**
- Email "not-an-email" → validation error, invite blocked

**NEG-003 — Session expired handling**
- Fresh browser (no cookies) → navigate to `/employer/team`
- **Expected:** Redirect to signin or "Session expired" message, not blank page

**NEG-004 — Unauthorized route**
- SKIP if only Company Admin account available
- Otherwise: login as limited user → try `/employer/team` → unauthorized page or redirect

### Module 9 — Cleanup (1 test)

**CLEANUP-001 — Revert test artifacts**
1. Revoke ALL remaining `qa-*` pending invites
2. Remove any QA test members from Active list
3. Delete custom roles: `QA Custom Role {TS}`, `QA Clone Interviewer {TS}`
4. Delete/rename test departments `QA Dept {TS} Updated`
5. Revert any role changes made on real members during TEAM-020

---

## STEP 4 — Create dummy accounts for EACH role and test impact

After the main 47 tests, do this ADDITIONAL testing:

1. **Create 5 invite accounts** (one per role):
   - `qa-hr-manager-{TS}@mailinator.com` → HR Manager
   - `qa-hr-recruiter-{TS}@mailinator.com` → HR Recruiter
   - `qa-line-manager-{TS}@mailinator.com` → Line Manager
   - `qa-interviewer-{TS}@mailinator.com` → Interviewer
   - `qa-coordinator-{TS}@mailinator.com` → Coordinator

2. **For each invite**, verify:
   - Invite wizard completes successfully for that role
   - Pending tab shows correct role badge
   - Job access step behaves correctly (company-wide vs job-scoped)

3. **Test role changes** — for each pending/active member:
   - Change role from one to another (e.g. HR Recruiter → Line Manager)
   - Verify toast "Role updated", badge changes, API success
   - Check if Fine-Tune Rights reflect new role's defaults
   - Revert to original role

4. **Cleanup**: Revoke all 5 test invites

---

## STEP 5 — Fix failures in source code

When a test FAILs:

1. **Capture** the exact error (toast message, console error, API response)
2. **Investigate** the source code:
   - Frontend issues → look in `H:/dev/rozeegpt-core/rozeegptapp02/` (React components, API calls, state management)
   - Backend/API issues → look in `H:/dev/rozeegpt-core/rozeegpt/` (controllers, routes, validators)
3. **Fix** with minimal changes
4. **Re-run** the failing test to confirm the fix
5. **Log** the fix in the failures table

Key files to check for issues:
- Frontend team page: search for `team`, `TeamManagement`, `TeamPage` in rozeegptapp02
- Frontend roles page: search for `roles`, `RolesPermissions`, `RolesPage` in rozeegptapp02
- Frontend invite wizard: search for `invite`, `InviteModal`, `InviteMember` in rozeegptapp02
- Backend team API: search for `TeamV2`, `team` routes in rozeegpt
- Backend roles API: search for `RolesV2`, `roles` routes in rozeegpt
- Backend departments: search for `DepartmentsV2` in rozeegpt

---

## STEP 6 — Report results

After ALL tests complete, produce:

### Test Run Summary

| Module | Total | Pass | Fail | Skip |
|--------|-------|------|------|------|
| Setup | 3 | | | |
| Team load | 4 | | | |
| Search/filter | 3 | | | |
| Invite | 8 | | | |
| Pending | 3 | | | |
| Departments | 4 | | | |
| Member actions | 6 | | | |
| Roles | 11 | | | |
| Negative | 4 | | | |
| Cleanup | 1 | | | |
| Dummy role accounts | 5+ | | | |
| **Total** | **52+** | | | |

### Failures & Fixes Log

| Test ID | Symptom | Root Cause | File(s) Changed | Repo | Fixed? |
|---------|---------|------------|-----------------|------|--------|

### Safety Checklist (MANDATORY)
- [ ] mkhalid@naseebnetworks.com NOT removed
- [ ] No Company Admin members removed
- [ ] All qa-* invites revoked
- [ ] All custom test roles deleted
- [ ] All role changes on real members reverted
- [ ] Test departments cleaned up

## SAFETY RULES — READ BEFORE RUNNING

- **NEVER** remove mkhalid@naseebnetworks.com
- **NEVER** remove any Company Admin member
- **ALWAYS** revoke/delete test data after testing (CLEANUP-001)
- **ALWAYS** revert role changes on real members
- Use `qa-*@mailinator.com` emails for all test invites
- Confirm all destructive browser dialogs ONLY for intentional test actions
```

## PROMPT END — Copy to here ↑

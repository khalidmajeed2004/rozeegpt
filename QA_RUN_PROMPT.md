# QA Automation Prompt — RozeeGPT Team & Roles

## Instructions for Claude Code Desktop App

Paste everything below this line into Claude Code running on your local machine (desktop app). It will clone the test suite, install dependencies, run all 47 tests, fix any failures it finds in the codebase, and report results.

---

## PROMPT START — Copy from here ↓

```
Clone and run the Playwright QA test suite from branch `claude/pensive-clarke-nh3f90` of repo `khalidmajeed2004/rozeegpt`. Then execute the FULL end-to-end QA flow against https://betaqa.rozeegpt.ai using the credentials and instructions below.

## Setup Steps

1. Clone the repo and checkout the branch:
   ```
   git clone https://github.com/khalidmajeed2004/rozeegpt.git
   cd rozeegpt
   git checkout claude/pensive-clarke-nh3f90
   npm install
   npx playwright install chromium
   ```

2. Run the full test suite:
   ```
   npx playwright test --reporter=list
   ```

3. If any tests fail, investigate, fix the test or the app code, and re-run.

## Test Account Credentials

- **URL:** https://betaqa.rozeegpt.ai/employer/signin
- **Email:** mkhalid@naseebnetworks.com
- **Password:** P@kistan1
- **Expected role:** Company Admin (full Team/Roles access)

## What the test suite covers (47 test cases)

### Module 0 — Setup & Login (3 tests)
- SETUP-001: Sign in with test account → verify redirect to dashboard, no error toast, session cookie present
- SETUP-002: Sidebar shows Team and Roles links under Organization section
- SETUP-003: Navigate to Team Management → verify title, 4 stat cards (Total Members, Pending Invitations, Departments, Roles in Use), tabs (Active/Pending/Departments/Removed), + Invite Member button

### Module 1 — Team Page Load & Layout (4 tests)
- TEAM-001: Stat cards match tab data → Active tab count = Total Members stat, Pending stat = Pending tab rows
- TEAM-002: Active members list renders → each row shows avatar, name, role badge, email, role dropdown, rights icon, remove icon
- TEAM-003: Info alert "How access works" and "View roles & matrix →" link navigates to /employer/roles
- TEAM-004: Self row (mkhalid) → role dropdown disabled, tooltip "cannot change own role", sliders opens My Access (read-only)

### Module 2 — Search & Filters (3 tests)
- TEAM-010: Search by name/email → real-time filtering, clearing restores full list
- TEAM-011: Search "zzzznonexistent99999" → empty state "No members found", no JS errors
- TEAM-012: Role filter dropdown → select "HR Recruiter" filters list, "All Roles" restores

### Module 3 — Invite Team Member 3-Step Wizard (8 tests)
- INV-001: Open invite modal → title "Invite Team Member", step indicator (Details → Role → Access), fields (Full Name, Email, Department), Cancel + Next buttons
- INV-002: Step 1 validation → empty email shows "Email is required", stays on step 1
- INV-003: Fill details (use `qa-invite-{timestamp}@mailinator.com`) → advances to step 2, role cards listed
- INV-004: Select HR Recruiter → advances to step 3 "Job Access Scope" with All Jobs / Specific Jobs options
- INV-005: Select Specific Jobs, pick job chips, Send Invitation → toast "Invitation sent!", Pending count increases, API returns code "11"
- INV-006: Invite HR Manager (company-wide role) → no job selection needed, invite succeeds, then revoke
- INV-007: Back navigation → data preserved when going back through steps, Cancel closes without sending
- INV-008: Duplicate invite → clear error message "already invited", no duplicate rows, API returns code "00"

### Module 4 — Pending Invitations (3 tests)
- PEND-001: Pending tab → shows email, role badge, department chip, Pending status, Invited date, Resend + Revoke buttons
- PEND-002: Resend → toast "Invitation resent", row stays, API returns code "11"
- PEND-003: Revoke → confirm dialog, toast "Invitation revoked", row removed, count decrements

### Module 5 — Departments (4 tests)
- DEPT-001: Departments tab → header, "+ Add Department" button, table columns (Department, Members, Actions)
- DEPT-002: Add department `QA Dept {timestamp}` → toast "Department saved", new row with 0 members, stat increases
- DEPT-003: Edit department → change name, toast "Department updated", table reflects change
- DEPT-004: Duplicate name → error "A department with this name already exists", modal stays open

### Module 6 — Active Member Actions (6 tests)
- TEAM-020: Change member role (non-self, non-admin) → toast "Role updated", badge changes, API code "11", then REVERT
- TEAM-021: Fine-Tune Rights modal → grouped toggles matching role defaults, toggle one OFF/ON, Save → toast "Rights updated"
- TEAM-022: My Access (self) → read-only modal, toggles disabled, no Save
- TEAM-023: Manage Job Access → click "N Job(s) Shared", toggle All/Specific, save → toast "Job access updated"
- TEAM-024: Remove test member → confirm dialog, toast "{name} removed", disappears from Active, appears on Removed tab
- TEAM-025: Removed tab → muted styling, name/email/Removed label, or empty state "No removed members"

### Module 7 — Roles & Permissions (11 tests)
- ROLE-001: Roles page load → title, Cards/Matrix toggle, + Create Custom Role button, System Roles section
- ROLE-002: System role cards → each shows name, description, Best for, System chip, member count, View Rights button
- ROLE-003: View Rights modal (HR Recruiter) → grouped permissions, read-only toggles, Clone as Custom Role button
- ROLE-004: Permissions Matrix → grid with roles as columns, permissions as rows, checkmarks
- ROLE-005: Matrix ↔ Cards toggle → no stale overlay, renders correctly both ways
- ROLE-006: Member count consistency → sum of role card counts ≈ Total Members on Team page
- ROLE-010: Create custom role `QA Custom Role {timestamp}` → drawer/modal, enable 3-5 rights, save → toast, appears under Custom Roles
- ROLE-011: Edit custom role → change description/toggle, save → persists after refresh
- ROLE-012: Clone Interviewer as custom → "QA Clone Interviewer {timestamp}", rights copied
- ROLE-013: Delete unassigned custom role → toast "Role deleted", card removed
- ROLE-014: Cannot delete system role → no delete button on system cards, View Rights is read-only
- ROLE-015: Invite with custom role → custom role appears in step 2 list, invite succeeds

### Module 8 — Negative & Guard Rails (4 tests)
- NEG-001: Cannot remove Company Admin → remove button disabled or missing
- NEG-002: Invalid email "not-an-email" on invite → validation error, invite blocked
- NEG-003: Session expired → unauthenticated access to /employer/team redirects to signin
- NEG-004: Unauthorized route (SKIP if only Company Admin available)

### Module 9 — Cleanup (1 test)
- CLEANUP-001: Revoke all qa-* pending invites, delete custom roles, delete test departments, revert role changes

## Safety Rules (CRITICAL)
- Do NOT remove mkhalid@naseebnetworks.com
- Do NOT remove any Company Admin member
- Revoke/remove ALL test invites and members created during the run
- Delete custom roles after testing
- Revert role changes on real members
- Use unique timestamps for all test data to avoid collisions

## API Reference (for network tab verification)
- Success: response JSON `code === "11"`
- Failure: `code === "00"`
- Session expired: `code === "421"`
- All IDs are base-62 encoded strings

## Your Tasks

1. **Run all 47 tests** in the recommended order (setup → team → search → roles → departments → invite → pending → member actions → custom roles → negative → cleanup)
2. **For each FAIL**: capture the exact error, diagnose root cause, fix the test selector or app code if needed, re-run
3. **Create dummy accounts** for each role: HR Manager, HR Recruiter, Line Manager, Interviewer, Coordinator — test role changes and verify access impact
4. **After all tests pass**, produce a summary table:

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
| **Total** | **47** | | | |

5. **Log all failures and fixes**:

| Test ID | Symptom | Root Cause | Fix Applied | Fixed? |
|---------|---------|------------|-------------|--------|

6. Commit fixes back to branch `claude/pensive-clarke-nh3f90` and push.
```

## PROMPT END — Copy to here ↑

# Complete QA + Assessed Tab Fix Prompt for Claude Code Desktop

## PROMPT START — Copy from here ↓

```
You have access to two repos in the current directory:

- `./rozeegpt/` — Backend API (Node.js)
- `./rozeegptapp02/` — Frontend employer app (React)

Login: mkhalid@naseebnetworks.com / P@kistan1
URL: https://betaqa.rozeegpt.ai

---

# PART 1 — Fix Assessed Tab Sub-Tab Filtering & Pagination

Go to: https://betaqa.rozeegpt.ai/employer/job/app/140595?tab=testAssigned

## Data Structure (from reference HTML)

The Assessed tab shows a table with these columns:
**Name | Job Title / Company | Checklist | MCQ | Video | Agentic | Psychometric | Result | Action**

### Test Type Keys (backend/internal → UI label):
| Internal Key | UI Label | Column Header |
|-------------|----------|---------------|
| `mcq` | MCQ Test | MCQ |
| `video` | Video Interview | Video |
| `whatsapp` | Agentic Interview | Agentic |
| `psychometric` | Psychometric Test | Psychometric |
| `coding` | Coding Test | Coding (if enabled) |

### Per-candidate test status values (each cell shows one of):
- `"Assessed - XX%"` — test completed with score (green if >= threshold, red if below)
- `"Started"` — candidate started but not finished
- `"Invited"` — candidate received invite but hasn't started
- `"—"` (dash) — test NOT assigned to this candidate

### Thresholds per test type:
| Test | Pass Threshold |
|------|---------------|
| MCQ | 60% |
| Video | 60% |
| Coding | 50% |
| Agentic (whatsapp) | 60% |
| Psychometric | 55% |

### Result column (aggregate):
- **PASS** — ALL created tests are "Assessed" AND ALL scores >= their threshold
- **FAIL** — ALL created tests are "Assessed" AND at least one score < threshold
- **—** (pending) — not all tests completed yet

### Checklist column:
Shows `XX% (N/5)` — completion percentage of a 5-item checklist

## Sub-Tab Definitions (THIS IS THE CRITICAL FIX)

The Assessed tab has sub-tab filter buttons. Each filters the candidate list:

| Sub-Tab Button | Filter Logic | What to Show |
|---------------|-------------|--------------|
| **All Tests (N)** | No test-type filter | All candidates who have at least 1 test assigned (any type, any state) |
| **MCQ Test (N)** | `assessmentData[candidateId].mcq` exists | Only candidates who have MCQ test assigned — any state (Invited/Started/Assessed) |
| **Video Interview (N)** | `assessmentData[candidateId].video` exists | Only candidates who have Video test assigned — any state |
| **Agentic Interview (N)** | `assessmentData[candidateId].whatsapp` exists | Only candidates who have Agentic test assigned — any state |
| **Psychometric Test (N)** | `assessmentData[candidateId].psychometric` exists | Only candidates who have Psychometric test assigned — any state |
| **Coding Test (N)** | `assessmentData[candidateId].coding` exists | Only candidates who have Coding test assigned — any state (if enabled) |
| **Passed All** | `getAggregateResult(id) === 'PASS'` | Only candidates where ALL tests are Assessed AND ALL passed threshold |
| **Failed** | `getAggregateResult(id) === 'FAIL'` | Only candidates where ALL tests are Assessed AND at least one failed threshold |

**Key rules:**
1. A candidate appears in a test-type sub-tab if they have that test ASSIGNED (regardless of state — Invited, Started, or Assessed all count)
2. A candidate can appear in MULTIPLE sub-tabs (e.g., has both MCQ and Video assigned → appears in both)
3. The `(N)` count in each sub-tab button must equal the number of candidates matching that filter
4. "Passed All" and "Failed" only show candidates where ALL assigned tests have status "Assessed" with a score

### Example from screenshot data:

| Candidate | MCQ | Video | Agentic | Psychometric | Result |
|-----------|-----|-------|---------|-------------|--------|
| Hira Sheikh | Assessed-88% | Assessed-52% | Started | Assessed-84% | — |
| Kamran Bhatti | Assessed-37% | Assessed-79% | Assessed-98% | Assessed-67% | FAIL |
| Maham Awan | Assessed-41% | Started | Assessed-61% | Started | — |
| Tahira Wali | Started | Invited | Assessed-40% | Assessed-43% | — |
| Farzana Khan | Assessed-66% | Assessed-71% | Assessed-94% | Assessed-80% | PASS |
| Robina Hussain | Assessed-73% | Started | Assessed-56% | Assessed-92% | — |
| Nimra Mustafa | Started | Invited | Assessed-72% | Assessed-82% | — |

From this data:
- **All Tests**: 7 candidates (all have at least 1 test)
- **MCQ Test**: 7 (all have MCQ — some Assessed, some Started)
- **Video Interview**: 7 (all have Video — some Assessed, some Started, some Invited)
- **Agentic Interview**: 7 (all have Agentic)
- **Psychometric**: 7 (all have Psychometric)
- **Passed All**: 1 (only Farzana Khan — all Assessed, all above threshold)
- **Failed**: 1 (only Kamran Bhatti — all Assessed, MCQ 37% < 60% threshold)

## What to Fix

### Step 1: Find the code

Search `./rozeegptapp02/` for:
- `testAssigned` or `assessed` — the tab identifier
- `setAssessTestFilter` or `assessTestFilter` — the sub-tab filter function
- `MCQ Test`, `Video Interview`, `Agentic` — sub-tab labels
- The component rendering the candidate table for assessed tab
- The API call fetching assessed candidates
- The pagination component used on this page

Search `./rozeegpt/` for:
- The API endpoint for assessed/testAssigned candidate listing
- `testType` or `assessmentType` filter parameter handling
- Pagination logic (`page`, `limit`, `offset`, `total`)
- Any cron job that recalculates test stats

### Step 2: Fix sub-tab filtering

**Frontend:**
1. Each sub-tab button must pass the correct `testType` filter to the API call
2. The API must filter and return ONLY candidates matching that test type
3. If filtering is done client-side, ensure the filter checks if the candidate has that test type in their assessment data (not just the score — Invited/Started count too)
4. Sub-tab counts `(N)` must reflect the filtered count

**Backend (if filtering is server-side):**
1. Accept `testType` parameter: `mcq`, `video`, `whatsapp`, `psychometric`, `coding`
2. Accept `resultFilter` parameter: `_passed`, `_failed`
3. When `testType` is set: only return candidates who have that test assigned (any state)
4. When `_passed`: only return candidates with ALL tests Assessed AND all scores >= threshold
5. When `_failed`: only return candidates with ALL tests Assessed AND at least one score < threshold
6. Return correct `totalCount` for the filtered set

### Step 3: Fix pagination

1. When switching sub-tabs → reset page to 1
2. Page count must use filtered totalCount, not total unfiltered count
3. Page changes must re-fetch with both testType filter AND page number
4. Ensure `limit`/`offset` or `page`/`pageSize` work correctly with filter applied

### Step 4: Fix stats cron (if applicable)

Search `./rozeegpt/` for cron jobs that calculate/recalculate test stats:
- Search for `cron`, `schedule`, `agenda`, `bull`, `node-cron`
- Look for jobs that aggregate test results, calculate pass/fail, update counts
- Verify the cron correctly counts per test type
- If there's a "refresh stats" endpoint, verify it works

## Verification

After fixing, open the browser and check:

1. **All Tests** tab shows all candidates with any test assigned
2. **MCQ Test** tab shows ONLY candidates with MCQ column having a value (not "—")
3. **Video Interview** tab shows ONLY candidates with Video column having a value
4. **Agentic Interview** tab shows ONLY candidates with Agentic column having a value
5. **Psychometric** tab shows ONLY candidates with Psychometric column having a value
6. **Passed All** shows ONLY candidates with PASS in Result column
7. **Failed** shows ONLY candidates with FAIL in Result column
8. Tab counts in `(N)` are accurate
9. Pagination resets to page 1 on tab switch
10. Pagination works per filtered tab
11. Each row still shows ALL columns (Name, Job Title, Checklist, MCQ, Video, Agentic, Psychometric, Result, Action) — just the ROW set is filtered, not the columns

---

# PART 2 — Team Management & Roles QA (47 tests)

After Part 1 is fixed, run a browser-based QA flow on Team Management and Roles.

## Setup

Install Playwright if not already available:
```bash
npm install --save-dev @playwright/test
npx playwright install chromium
```

## Credentials
- Sign in: https://betaqa.rozeegpt.ai/employer/signin
- Email: mkhalid@naseebnetworks.com
- Password: P@kistan1
- Role: Company Admin

## Tests to Run (IN ORDER)

### Module 0 — Login (3 tests)
- SETUP-001: Sign in → redirect to dashboard, no errors
- SETUP-002: Sidebar shows Team and Roles links
- SETUP-003: Navigate to Team Management → title, 4 stat cards, tabs, Invite button

### Module 1 — Team Page (4 tests)
- TEAM-001: Stat cards match tab counts
- TEAM-002: Active members list renders with avatars, role badges, emails
- TEAM-003: Info alert "How access works" with Roles link
- TEAM-004: Self row — cannot change own role

### Module 2 — Search (3 tests)
- TEAM-010: Search "mkhalid" filters list, clear restores
- TEAM-011: Search nonsense → "No members found" empty state
- TEAM-012: Role filter dropdown works

### Module 3 — Invite Wizard (8 tests)
- INV-001 to INV-008: Open modal, validation, fill details, select role, job access, send, back nav, duplicate handling

### Module 4 — Pending (3 tests)
- PEND-001 to PEND-003: Pending tab, resend, revoke

### Module 5 — Departments (4 tests)
- DEPT-001 to DEPT-004: Layout, add, edit, duplicate blocked

### Module 6 — Member Actions (6 tests)
- TEAM-020 to TEAM-025: Change role, fine-tune rights, my access, job access, remove, removed tab

### Module 7 — Roles & Permissions (11 tests)
- ROLE-001 to ROLE-015: Page load, system role cards, view rights, matrix, toggle, create/edit/clone/delete custom role, invite with custom role

### Module 8 — Negative (4 tests)
- NEG-001 to NEG-004: Cannot remove admin, invalid email, session expired, unauthorized route

### Module 9 — Cleanup (1 test)
- CLEANUP-001: Revoke all qa-* invites, delete custom roles, delete test departments, revert role changes

## Safety Rules
- NEVER remove mkhalid@naseebnetworks.com
- NEVER remove any Company Admin
- ALWAYS clean up test data after

---

# PART 3 — Report

After all work is done, produce:

### Assessed Tab Fix Summary
| Item | Status |
|------|--------|
| MCQ sub-tab filtering | |
| Video sub-tab filtering | |
| Agentic sub-tab filtering | |
| Psychometric sub-tab filtering | |
| Passed All filtering | |
| Failed filtering | |
| Tab counts accurate | |
| Pagination reset on tab switch | |
| Pagination per filtered tab | |
| Stats cron verified | |

### Files Changed
| File | Repo | What Changed |
|------|------|-------------|

### QA Test Results
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

Commit all fixes with clear messages.
```

## PROMPT END — Copy to here ↑

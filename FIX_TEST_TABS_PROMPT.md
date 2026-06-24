# Fix Assessed Tab — Sub-Tab Filtering & Pagination

## PROMPT START — Copy from here ↓

```
I need you to fix the job applicant **Assessed** tab sub-tab filtering and pagination.

**URL:** https://betaqa.rozeegpt.ai/employer/job/app/140595?tab=testAssigned
**Login:** mkhalid@naseebnetworks.com / P@kistan1

## Correct Definitions

### Main Tab: "Assessed"

This tab shows candidates who have been **assigned at least one test** of any type. The test can be in ANY state (pending, invited, started, completed — doesn't matter).

### Sub-Tabs (filter by test TYPE assigned):

| Sub-Tab | What to show |
|---------|-------------|
| **All Tests** | ALL candidates who have been assigned at least any one test (MCQ, Video, Coding, Psychometric, Agentic, etc.) — any state |
| **MCQ Test** | Only candidates who have been assigned an **MCQ** test — any state |
| **Video Interview** | Only candidates who have been assigned a **Video Interview** — any state |
| **Agentic Interviews** | Only candidates who have been assigned an **Agentic Interview** — any state |
| **Psychometric** | Only candidates who have been assigned a **Psychometric** test — any state |

**Key point:** Filtering is by **test type assigned**, NOT by pass/fail status. A candidate shows up if they have that test type assigned regardless of whether it's pending, invited, started, or completed.

A candidate can appear in multiple sub-tabs if they have multiple test types assigned (e.g., assigned both MCQ and Video → appears in both "MCQ Test" and "Video Interview" tabs, plus "All Tests").

## The Current Bug

All sub-tabs currently show the same unfiltered list (same as "All Tests"). They should each filter to only show candidates with THAT specific test type assigned. Pagination is also broken across tabs.

## Source Code Locations

- **Frontend:** /private/var/www/naseeb/projects/rozeegpt-core/rozeegptapp02/
- **Backend API:** /private/var/www/naseeb/projects/rozeegpt-core/rozeegpt/

## Investigation Steps

### Step 1: Find the frontend component

Search rozeegptapp02 for:
- `testAssigned` — the tab key/URL param
- `Assessed` — the tab label
- `MCQ Test`, `Video Interview`, `Agentic Interview`, `Psychometric`
- `All Tests`
- Route pattern `/employer/job/app/:id`
- Components handling applicant list with test sub-tabs

Identify:
- Which component renders the sub-tabs
- How sub-tab selection triggers data fetching
- What API call is made and what parameters are passed
- How pagination state is managed

### Step 2: Find the backend endpoint

Search rozeegpt for:
- The API endpoint serving the assessed/testAssigned applicant list
- `testAssigned`, `assessed`, `TestAssigned`, `test_assigned`
- How it accepts filter parameters for test type
- How pagination params (page, limit, offset) are handled

### Step 3: Fix the filtering

**Frontend:**
1. Each sub-tab must pass a `testType` (or equivalent) filter parameter to the API:
   - All Tests → no testType filter (or "all")
   - MCQ Test → testType = "mcq" (use whatever value the backend expects)
   - Video Interview → testType = "video"
   - Agentic Interviews → testType = "agentic"
   - Psychometric → testType = "psychometric"

2. When switching sub-tabs:
   - Reset pagination to page 1
   - Re-fetch data with the new testType filter
   - Update the displayed total count from the filtered API response

3. Tab counts in parentheses should reflect the filtered count per test type

**Backend (if needed):**
1. Ensure the endpoint accepts a testType filter parameter
2. Filter the query: if testType is provided, only return candidates who have THAT test type assigned (regardless of test state)
3. If no testType filter, return all candidates with any test assigned
4. Return correct total count for filtered results
5. Ensure pagination works correctly with the filter applied

### Step 4: Fix pagination

1. Pagination must reset to page 1 when switching sub-tabs
2. Total page count must be based on the FILTERED result count, not unfiltered
3. Page changes must re-fetch with both the current testType filter AND the page number
4. Page size selector must work correctly per tab

## Testing Checklist

After fixing, verify at https://betaqa.rozeegpt.ai/employer/job/app/140595?tab=testAssigned:

- [ ] **All Tests** shows all candidates with any test assigned
- [ ] **MCQ Test** shows ONLY candidates with MCQ assigned (subset of All Tests)
- [ ] **Video Interview** shows ONLY candidates with Video assigned
- [ ] **Agentic Interviews** shows ONLY candidates with Agentic assigned
- [ ] **Psychometric** shows ONLY candidates with Psychometric assigned
- [ ] Tab counts in parentheses match actual filtered row counts
- [ ] Switching tabs resets to page 1
- [ ] Pagination works for each filtered tab
- [ ] A candidate with multiple test types appears in multiple sub-tabs
- [ ] Test state doesn't matter — pending/invited/started/completed all show

## Commit fixes with clear messages.
```

## PROMPT END — Copy to here ↑

# Fix Job Applicant Test Tabs — Filtering & Pagination

## PROMPT START — Copy from here ↓

```
I need you to fix the job applicant test sub-tabs at this URL:
https://betaqa.rozeegpt.ai/employer/job/app/140595?tab=testAssigned

The page has these sub-tabs:
- MCQ Test (1)
- Video Interview (1)
- Agentic Interviews (7)
- All Tests (6)
- Passed All
- Failed

## The Problem

Currently, ALL sub-tabs show the same unfiltered data (same as "All Tests"). They need to show FILTERED data:

1. **MCQ Test** — Only show applicants who have been assigned MCQ Tests, with all their data
2. **Video Interview** — Only show applicants who have been assigned Video Interviews, with all their data
3. **Agentic Interviews** — Only show applicants who have been assigned Agentic Interviews, with all their data
4. **All Tests** — Show all applicants with any test assigned (current behavior — this is the baseline)
5. **Passed All** — Only show applicants who passed ALL their assigned tests
6. **Failed** — Only show applicants who failed any assigned test

Additionally, **pagination is broken** across all tabs — it needs to work correctly for each filtered view.

## Source Code Locations

The two repos are at:
- **Frontend:** H:/dev/rozeegpt-core/rozeegptapp02/
- **Backend API:** H:/dev/rozeegpt-core/rozeegpt/

## What to Investigate

### Frontend (rozeegptapp02)

1. Find the component that renders the `testAssigned` tab and its sub-tabs. Search for:
   - `testAssigned`
   - `MCQ Test` or `mcqTest` or `mcq_test`
   - `Video Interview` or `videoInterview`
   - `Agentic Interview` or `agenticInterview`
   - Components near the job applicant listing page
   - Route patterns like `/employer/job/app/:id`
   
2. Find how sub-tab filtering currently works — it's likely passing a filter parameter to the API but either:
   - Not passing the correct filter/type parameter when switching tabs
   - Passing the same parameter for all tabs
   - Not resetting pagination when switching tabs

3. Find the pagination component and check:
   - Is it receiving the correct total count per filtered tab?
   - Does it reset to page 1 when switching sub-tabs?
   - Is the page parameter being sent to the API on page change?

### Backend (rozeegpt)

1. Find the API endpoint that serves the test-assigned applicant list. Search for:
   - `testAssigned` in route/controller files
   - Endpoint patterns like `applicants/list`, `JobApplicants`, `TestAssigned`
   - The controller handling test type filtering
   
2. Check if the API:
   - Accepts a `testType` or `filter` parameter
   - Properly filters by test type (mcq, video, agentic)
   - Accepts and handles `page` / `limit` / `offset` pagination params
   - Returns correct `total` / `totalCount` for the filtered results

## What to Fix

### Frontend fixes needed:

1. **Sub-tab filter parameter** — Each sub-tab must pass a distinct filter value to the API:
   - MCQ Test → filter/testType = "mcq" (or whatever the backend expects)
   - Video Interview → filter/testType = "video"
   - Agentic Interviews → filter/testType = "agentic"
   - All Tests → no filter (or filter = "all")
   - Passed All → filter/status = "passed"
   - Failed → filter/status = "failed"

2. **Pagination reset** — When switching sub-tabs, reset the current page to 1 and re-fetch with the new filter

3. **Pagination total** — Use the filtered total from the API response, not the unfiltered total

4. **Tab counts** — The numbers in parentheses (e.g., "MCQ Test (1)") should reflect the actual filtered count from the API

### Backend fixes (if needed):

1. Ensure the API endpoint accepts `testType` / `status` filter parameters
2. Ensure it filters the query correctly based on these parameters
3. Ensure pagination (`page`, `limit`) works correctly with filters applied
4. Ensure the response includes the correct `total` / `totalCount` for the filtered results

## Testing

After making fixes:

1. Open https://betaqa.rozeegpt.ai/employer/job/app/140595?tab=testAssigned
2. Login with: mkhalid@naseebnetworks.com / P@kistan1

3. Verify each sub-tab:
   - **All Tests** — Shows 6 entries (baseline)
   - **MCQ Test** — Shows only 1 entry (MCQ type only)
   - **Video Interview** — Shows only 1 entry (video type only)
   - **Agentic Interviews** — Shows only 7 entries (agentic type only)
   - **Passed All** — Shows only passed applicants
   - **Failed** — Shows only failed applicants

4. Verify pagination for each tab:
   - Page numbers reflect filtered count
   - Clicking page 2 loads next set of filtered results (not unfiltered)
   - Switching tabs resets to page 1
   - Page size selector works correctly

5. Verify tab counts update correctly:
   - Numbers in parentheses match actual filtered row counts

6. Check the Network tab to confirm:
   - API calls include the correct filter parameter
   - API responses return filtered data with correct totals

## Commit your fixes with clear messages describing what was changed and why.
```

## PROMPT END — Copy to here ↑

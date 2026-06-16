const fs = require("fs");
const path = require("path");

const RESULTS_FILE = path.join(__dirname, "..", "test-results.json");

function loadResults() {
  try {
    return JSON.parse(fs.readFileSync(RESULTS_FILE, "utf8"));
  } catch {
    return { tests: [], failures: [], summary: {} };
  }
}

function saveResult(testId, status, notes = "") {
  const results = loadResults();
  const existing = results.tests.findIndex((t) => t.id === testId);
  const entry = {
    id: testId,
    status,
    notes,
    timestamp: new Date().toISOString(),
  };
  if (existing >= 0) results.tests[existing] = entry;
  else results.tests.push(entry);

  if (status === "FAIL") {
    results.failures.push({
      id: testId,
      symptom: notes,
      timestamp: new Date().toISOString(),
    });
  }

  const counts = { PASS: 0, FAIL: 0, SKIP: 0 };
  results.tests.forEach((t) => counts[t.status]++);
  results.summary = { total: results.tests.length, ...counts };

  fs.writeFileSync(RESULTS_FILE, JSON.stringify(results, null, 2));
}

module.exports = { loadResults, saveResult };

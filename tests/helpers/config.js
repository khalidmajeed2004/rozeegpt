const TS = new Date()
  .toISOString()
  .replace(/[-:T]/g, "")
  .slice(0, 15);

module.exports = {
  BASE_URL: "https://betaqa.rozeegpt.ai",
  API_BASE: "https://betaqa-api.rozeegpt.ai/rest/api",
  SIGN_IN_URL: "https://betaqa.rozeegpt.ai/employer/signin",
  TEAM_URL: "https://betaqa.rozeegpt.ai/employer/team",
  ROLES_URL: "https://betaqa.rozeegpt.ai/employer/roles",

  TEST_EMAIL: "mkhalid@naseebnetworks.com",
  TEST_PASSWORD: "P@kistan1",

  TS,
  INVITE_EMAIL: `qa-invite-${TS}@mailinator.com`,
  INVITE_MGR_EMAIL: `qa-invite-mgr-${TS}@mailinator.com`,
  INVITE_CUSTOM_EMAIL: `qa-custom-${TS}@mailinator.com`,
  MEMBER_NAME: `QA Tester ${TS}`,
  CUSTOM_ROLE: `QA Custom Role ${TS}`,
  CLONE_ROLE: `QA Clone Interviewer ${TS}`,
  DEPT_NAME: `QA Dept ${TS}`,

  SYSTEM_ROLES: [
    "Company Admin",
    "HR Manager",
    "HR Recruiter",
    "Line Manager",
    "Interviewer",
    "Coordinator",
  ],

  API_SUCCESS: "11",
  API_FAILURE: "00",
  API_SESSION_EXPIRED: "421",
};

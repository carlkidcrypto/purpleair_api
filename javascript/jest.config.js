module.exports = {
  testEnvironment: "node",
  testMatch: ["**/tests/**/*.test.js"],
  collectCoverage: true,
  collectCoverageFrom: ["index.js"],
  coverageDirectory: "coverage",
  coverageReporters: ["text", "lcov", "html", "cobertura"],
};

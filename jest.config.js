module.exports = { 
  testEnvironment: "node", 
  transform: { "^.+\\.tsx?$": ["ts-jest", {}] },
  moduleNameMapper: {
    "^@/lib/(.*)$": "<rootDir>/lib/$1", 
    "^@/config/(.*)$": "<rootDir>/config/$1",
    "^@/(.*)$": "<rootDir>/src/$1"
  },
  testPathIgnorePatterns: [
    "/node_modules/",
    "/archive/"
  ]
};
"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const { evaluateTask } = require("./app.js");

const normal = {
  task_id: "TASK_01",
  target_identifier: "SAMPLE-01",
  primary_metric: 25,
  secondary_metric: 12,
  status_descriptor: "NOMINAL",
  is_critical_flag: false
};

test("boundary values do not trigger greater-than rules", () => {
  const result = evaluateTask(normal);
  assert.equal(result.total_alerts, 0);
  assert.equal(result.overall_urgency, "ROUTINE");
});

test("all three worker rules are represented", () => {
  const result = evaluateTask({ ...normal, primary_metric: 25.1, secondary_metric: 12.1, status_descriptor: "DISCORDANT" });
  assert.equal(result.total_alerts, 3);
  assert.equal(result.overall_urgency, "ELEVATED_RISK");
});

test("critical flag escalates urgency independently of values", () => {
  const result = evaluateTask({ ...normal, is_critical_flag: true });
  assert.equal(result.overall_urgency, "CRITICAL_STAT_PANIC");
  assert.equal(result.total_alerts, 1);
});

test("reject missing, invalid, negative, and non-finite metrics", () => {
  for (const value of ["", null, undefined, -1, "NaN", "Infinity", "1e999"]) {
    assert.throws(() => evaluateTask({ ...normal, primary_metric: value }));
  }
});

test("reject identifiers that may include patient details or markup", () => {
  for (const value of ["", "MRN: 123456", "<img>", "first last", "a".repeat(65)]) {
    assert.throws(() => evaluateTask({ ...normal, task_id: value }));
  }
});

test("reject unsupported descriptors and handle case-insensitive flags", () => {
  assert.throws(() => evaluateTask({ ...normal, status_descriptor: "<script>" }));
  assert.equal(evaluateTask({ ...normal, status_descriptor: "anomaly" }).total_alerts, 1);
});

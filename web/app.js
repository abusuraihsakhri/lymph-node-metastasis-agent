"use strict";

/**
 * Standalone demonstration of the existing generic Python worker thresholds.
 * This is not a cancer-staging algorithm or diagnostic interpretation.
 */
function evaluateTask(input) {
  if (!input || typeof input !== "object") {
    throw new TypeError("Enter a valid task.");
  }
  const idPattern = /^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$/;
  function identifier(value, label) {
    const text = String(value == null ? "" : value).trim();
    if (!idPattern.test(text)) {
      throw new Error(label + " must be 1–64 characters: letters, digits, hyphens or underscores.");
    }
    return text;
  }
  function metric(value, label) {
    if (value === "" || value == null || typeof value === "boolean") {
      throw new Error(label + " is required.");
    }
    const number = Number(value);
    if (!Number.isFinite(number) || number < 0) {
      throw new Error(label + " must be a non-negative finite number.");
    }
    return number;
  }

  const taskId = identifier(input.task_id, "Task ID");
  const targetId = identifier(input.target_identifier, "Target ID");
  const primary = metric(input.primary_metric, "Primary metric");
  const secondary = metric(input.secondary_metric, "Secondary metric");
  const status = String(input.status_descriptor == null ? "NOMINAL" : input.status_descriptor).trim().toUpperCase();
  if (!status || status.length > 80 || !/^[A-Z0-9 _-]+$/.test(status)) {
    throw new Error("Status must contain 1–80 letters, digits, spaces, underscores or hyphens.");
  }
  const critical = input.is_critical_flag === true;

  const alerts = [];
  if (primary > 25) {
    alerts.push({
      worker: "InvariantQCWorker",
      urgency: "ELEVATED_RISK",
      summary: "Primary threshold exceeded",
      detail: "Primary metric " + primary + " exceeds the demonstration threshold of 25."
    });
  }
  if (critical || secondary > 12) {
    alerts.push({
      worker: "SafetyEscalationWorker",
      urgency: critical ? "CRITICAL_STAT_PANIC" : "ELEVATED_RISK",
      summary: "Priority flag or secondary threshold triggered",
      detail: "Critical flag: " + critical + "; secondary metric: " + secondary + " (demonstration threshold: 12)."
    });
  }
  if (["DISCORDANT", "ANOMALY", "MUTANT", "VIOLATION", "FAIL", "REJECT"].some(flag => status.includes(flag))) {
    alerts.push({
      worker: "ProtocolConformanceWorker",
      urgency: "ELEVATED_RISK",
      summary: "Descriptor rule matched",
      detail: "Status descriptor matched a configured demonstration keyword."
    });
  }
  const urgency = alerts.some(a => a.urgency === "CRITICAL_STAT_PANIC")
    ? "CRITICAL_STAT_PANIC" : alerts.length ? "ELEVATED_RISK" : "ROUTINE";

  return {
    mode: "LOCAL_DEMONSTRATION",
    task_id: taskId,
    target_identifier: targetId,
    inputs: {
      primary_metric: primary,
      secondary_metric: secondary,
      status_descriptor: status,
      is_critical_flag: critical
    },
    overall_urgency: urgency,
    total_alerts: alerts.length,
    alerts,
    disclaimer: "Illustrative threshold checks only; not validated for diagnosis, metastasis classification or pN staging. No HMAC audit record is generated."
  };
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { evaluateTask };
}

if (typeof document !== "undefined") {
  const form = document.getElementById("rule-form");
  const output = document.getElementById("result");
  const validation = document.getElementById("validation");
  const headline = document.getElementById("result-heading");
  const total = document.getElementById("metric-total");
  const flags = document.getElementById("metric-flags");
  const exportButton = document.getElementById("export-button");
  let completed = 0;
  let previous = null;

  if (form) {
    form.addEventListener("submit", event => {
      event.preventDefault();
      validation.textContent = "";
      const entries = new FormData(form);
      try {
        const result = evaluateTask({
          task_id: entries.get("task_id"),
          target_identifier: entries.get("target_identifier"),
          primary_metric: entries.get("primary_metric"),
          secondary_metric: entries.get("secondary_metric"),
          status_descriptor: entries.get("status_descriptor"),
          is_critical_flag: entries.has("is_critical_flag")
        });
        previous = result;
        completed += 1;
        total.textContent = String(completed);
        flags.textContent = String(result.total_alerts);
        headline.textContent = result.overall_urgency === "ROUTINE"
          ? "No demonstration thresholds triggered"
          : result.total_alerts + " rule flag(s) · " + result.overall_urgency;
        output.textContent = JSON.stringify(result, null, 2);
        exportButton.disabled = false;
      } catch (error) {
        validation.textContent = error.message;
        headline.textContent = "Review input";
        output.textContent = "No evaluation performed. Correct the input and try again.";
        previous = null;
        exportButton.disabled = true;
      }
    });

    form.addEventListener("reset", () => {
      validation.textContent = "";
      headline.textContent = "No evaluation yet";
      output.textContent = "Complete the form to view a deterministic rule evaluation.";
      previous = null;
      exportButton.disabled = true;
    });

    exportButton.addEventListener("click", () => {
      if (!previous) return;
      const data = new Blob([JSON.stringify(previous, null, 2) + "\n"], { type: "application/json" });
      const url = URL.createObjectURL(data);
      const link = document.createElement("a");
      link.href = url;
      link.download = previous.task_id + "-rules.json";
      link.click();
      URL.revokeObjectURL(url);
    });
  }
}

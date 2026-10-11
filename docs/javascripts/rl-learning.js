/* Small teaching calculators: all values stay in the current browser. */
(function () {
  function number(value) {
    return Number(value).toFixed(3).replace(/\.?0+$/, "");
  }
  function initialize() {
    document.querySelectorAll("[data-rl-calculator]").forEach(function (box) {
      if (box.dataset.ready) return;
      box.dataset.ready = "true";
      function refresh() {
        var values = {};
        box.querySelectorAll("input[data-value]").forEach(function (input) {
          values[input.dataset.value] = input.type === "checkbox" ? input.checked : Number(input.value);
          var display = box.querySelector('[data-display="' + input.dataset.value + '"]');
          if (display) display.textContent = number(values[input.dataset.value]);
        });
        var future = values.terminal ? 0 : values.gamma * values.next;
        var target = values.reward + future;
        var updated = values.current + values.alpha * (target - values.current);
        if (box.dataset.rlCalculator === "td") {
          box.querySelector("[data-result]").textContent = "目标 " + number(target) +
            " → 误差 " + number(target - values.current) + " → 新估计 " + number(updated);
          box.querySelector("[data-explanation]").textContent = values.terminal ?
            "真正终止后，未来项为 0；目标只剩当前奖励。" :
            "先加上打折的下一状态估计，再向这个目标移动一小步。";
        } else {
          var best = Math.max(values.next, values.other);
          var qTarget = values.reward + (values.terminal ? 0 : values.gamma * best);
          var qUpdated = values.current + values.alpha * (qTarget - values.current);
          box.querySelector("[data-sarsa]").textContent = "SARSA：目标 " + number(target) +
            " → 新 Q " + number(updated);
          box.querySelector("[data-qlearning]").textContent = "Q-learning：目标 " + number(qTarget) +
            " → 新 Q " + number(qUpdated);
          box.querySelector("[data-explanation]").textContent = values.terminal ?
            "真正终止后，两者都只使用即时奖励，下一动作分数不再参与。" :
            "SARSA 使用实际选中动作的 " + number(values.next) +
            "；Q-learning 使用两个动作中的最高分 " + number(best) + "。";
        }
      }
      box.addEventListener("input", refresh);
      refresh();
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initialize);
  else initialize();
  if (typeof document$ !== "undefined") document$.subscribe(initialize);
})();

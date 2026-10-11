window.MathJax = {
  tex: { inlineMath: [["\\(", "\\)"]], displayMath: [["\\[", "\\]"]], processEscapes: true },
  options: { ignoreHtmlClass: ".*|", processHtmlClass: "arithmatex" },
  startup: { typeset: false }
};
// 兼容普通页面加载及 Material 的页面切换。
function renderResearchMath() {
  if (window.MathJax && window.MathJax.typesetPromise) {
    window.MathJax.typesetClear();
    window.MathJax.typesetPromise().catch(function (error) { console.warn("Math rendering:", error); });
  }
}
if (typeof document$ !== "undefined") document$.subscribe(renderResearchMath);
window.addEventListener("load", renderResearchMath);

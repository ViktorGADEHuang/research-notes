/* 阅读辅助只操作网页，不加载或执行教程源代码。 */
(() => {
  function initialize() {
    const article = document.querySelector(".md-content__inner");
    if (!article || article.querySelector(".reading-toolbar")) return;
    const figures = article.querySelectorAll("img.learning-figure, img.rl-figure");
    if (!figures.length) return;

    const toolbar = document.createElement("div");
    toolbar.className = "reading-toolbar";
    toolbar.setAttribute("role", "group");
    toolbar.setAttribute("aria-label", "教程阅读工具");
    const hint = document.createElement("span");
    hint.textContent = "读任务 → 看图和例子 → 对照步骤 → 自测";
    const focus = document.createElement("button");
    focus.type = "button";
    focus.setAttribute("data-reading-focus", "");
    focus.textContent = "专注阅读";
    focus.setAttribute("aria-pressed", "false");
    focus.addEventListener("click", () => {
      const active = document.body.classList.toggle("reading-focus");
      focus.setAttribute("aria-pressed", String(active));
      focus.textContent = active ? "恢复目录" : "专注阅读";
    });
    const actions = document.createElement("div");
    actions.className = "reading-actions";
    actions.append(focus);
    if (article.querySelector(".highlight pre code")) {
      const wrap = document.createElement("button");
      wrap.type = "button";
      wrap.textContent = "代码换行";
      wrap.title = "长行在屏幕内换行显示，复制内容保持原样";
      wrap.setAttribute("aria-pressed", "false");
      wrap.addEventListener("click", () => {
        const active = document.body.classList.toggle("code-wrap");
        wrap.setAttribute("aria-pressed", String(active));
        wrap.textContent = active ? "保留代码行" : "代码换行";
      });
      actions.append(wrap);
    }
    toolbar.append(hint, actions);
    article.querySelector("h1")?.after(toolbar);

    let dialog = document.querySelector(".figure-dialog");
    if (!dialog) {
      dialog = document.createElement("dialog");
      dialog.className = "figure-dialog";
      dialog.setAttribute("aria-labelledby", "figure-dialog-title");
      const header = document.createElement("div");
      header.className = "figure-dialog-header";
      const title = document.createElement("p");
      title.id = "figure-dialog-title";
      const controls = document.createElement("div");
      controls.className = "figure-dialog-controls";
      const zoom = document.createElement("button");
      zoom.type = "button";
      zoom.textContent = "放大查看";
      zoom.setAttribute("aria-pressed", "false");
      const close = document.createElement("button");
      close.type = "button";
      close.textContent = "关闭";
      const scroll = document.createElement("div");
      scroll.className = "figure-dialog-scroll";
      scroll.tabIndex = 0;
      scroll.setAttribute("aria-label", "图示区域，放大后可滚动查看");
      const hint = document.createElement("p");
      hint.className = "figure-dialog-hint";
      hint.textContent = "放大后可左右滚动；手机上用手指滑动查看其余部分。";
      const img = document.createElement("img");
      scroll.append(img);
      controls.append(zoom, close);
      header.append(title, controls);
      dialog.append(header, hint, scroll);
      document.body.append(dialog);
      close.addEventListener("click", () => dialog.close());
      zoom.addEventListener("click", () => {
        const active = dialog.classList.toggle("is-zoomed");
        zoom.setAttribute("aria-pressed", String(active));
        zoom.textContent = active ? "适应窗口" : "放大查看";
      });
      dialog.addEventListener("click", event => {
        if (event.target !== dialog) return;
        const rect = dialog.getBoundingClientRect();
        if (event.clientX < rect.left || event.clientX > rect.right ||
            event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
      });
    }

    function openFigure(figure) {
      // 浏览器不支持原生弹窗时，保留原始大图链接作为备用。
      if (typeof dialog.showModal !== "function") return;
      dialog.querySelector("img").src = figure.currentSrc || figure.src;
      dialog.querySelector("img").alt = figure.alt;
      dialog.querySelector("#figure-dialog-title").textContent = figure.alt || "教程图示";
      dialog.classList.remove("is-zoomed");
      const zoom = dialog.querySelector(".figure-dialog-controls button");
      zoom.textContent = "放大查看";
      zoom.setAttribute("aria-pressed", "false");
      dialog.showModal();
    }

    figures.forEach(figure => {
      figure.loading = "lazy";
      figure.tabIndex = 0;
      figure.setAttribute("role", "button");
      figure.setAttribute("aria-label", `${figure.alt}，打开图示`);
      figure.title = "点击或按 Enter 打开图示";
      figure.addEventListener("click", () => openFigure(figure));
      figure.addEventListener("keydown", event => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          openFigure(figure);
        }
      });
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize);
  } else initialize();
})();

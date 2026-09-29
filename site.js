(() => {
  "use strict";

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  // Scale fixed-size replicas to their container width.
  // Narrow frames switch to a stacked composition with a smaller design width.
  document.querySelectorAll("[data-scale-width]").forEach((frame) => {
    const stage = frame.firstElementChild;
    const wideWidth = Number(frame.dataset.scaleWidth);
    const compactWidth = Number(frame.dataset.compactWidth || wideWidth);
    const apply = () => {
      const compact = frame.clientWidth < 700;
      frame.classList.toggle("is-compact", compact);
      const designWidth = compact ? compactWidth : wideWidth;
      stage.style.transform = `scale(${frame.clientWidth / designWidth})`;
    };
    new ResizeObserver(apply).observe(frame);
    apply();
  });

  setUpWorkDemo(document.querySelector("[data-work-demo]"));
  setUpArranger(document.querySelector("[data-arranger]"));

  function setUpWorkDemo(root) {
    if (!root) return;
    const stage = root.querySelector(".replica-stage");
    const canvas = root.querySelector(".rp-canvas");
    const pointer = root.querySelector(".rp-pointer");
    const link = root.querySelector(".rp-link");
    const editor = root.querySelector(".rp-editor");
    const editorTab = root.querySelector(".rp-tab-editor");
    const tabs = [...root.querySelectorAll(".rp-bar .rp-tab")];
    const toggle = document.querySelector("[data-demo-toggle]");
    const card = (name) => root.querySelector(`.rp-card[data-agent="${name}"]`);
    const lane = (name) => [...root.querySelectorAll(`.rp-reveal[data-lane="${name}"]`)];
    const agents = ["codex", "claude"];

    let run = 0;
    let visible = false;
    let userPaused = false;

    const sleep = (ms, id) => new Promise((resolve, reject) => {
      setTimeout(() => (id === run ? resolve() : reject(new Error("cancelled"))), ms);
    });

    function setStatus(name, state, animate) {
      const chip = card(name).querySelector(".rp-chip");
      chip.dataset.state = state;
      chip.textContent = state[0].toUpperCase() + state.slice(1);
      const tab = root.querySelector(`.rp-tab[data-tab="${name}"]`);
      if (tab) tab.dataset.state = state;
      if (animate) {
        chip.classList.remove("is-flip");
        void chip.offsetWidth;
        chip.classList.add("is-flip");
      }
    }

    function activate(tab) {
      tabs.forEach((item) => item.classList.toggle("is-active", item === tab));
    }

    function showFinalState() {
      root.classList.remove("is-armed");
      agents.forEach((name) => setStatus(name, "done", false));
      root.querySelectorAll(".rp-reveal").forEach((line) => line.classList.add("is-shown"));
      editor.classList.add("is-open");
      editorTab.classList.add("is-open");
      activate(editorTab);
      link.classList.add("is-hover");
      pointer.classList.remove("is-shown", "is-down");
    }

    function reset() {
      root.classList.add("is-armed");
      agents.forEach((name) => setStatus(name, "working", false));
      root.querySelectorAll(".rp-reveal").forEach((line) => line.classList.remove("is-shown"));
      editor.classList.remove("is-open");
      editorTab.classList.remove("is-open");
      activate(root.querySelector('.rp-tab[data-tab="claude"]'));
      link.classList.remove("is-hover");
      pointer.classList.remove("is-shown", "is-down");
      const start = pointIn(card("zsh"), 0.62, 0.8);
      pointer.style.left = `${start.x}px`;
      pointer.style.top = `${start.y}px`;
    }

    function pointIn(element, xFraction, yFraction) {
      const scale = stage.getBoundingClientRect().width / stage.offsetWidth;
      const box = element.getBoundingClientRect();
      const canvasBox = canvas.getBoundingClientRect();
      return {
        x: (box.left + box.width * xFraction - canvasBox.left) / scale,
        y: (box.top + box.height * yFraction - canvasBox.top) / scale,
      };
    }

    async function streamCodex(id) {
      await sleep(900, id);
      for (const line of lane("codex")) {
        line.classList.add("is-shown");
        await sleep(820 + Math.random() * 420, id);
      }
      setStatus("codex", "done", true);
    }

    async function streamClaude(id) {
      await sleep(500, id);
      const lines = lane("claude");
      for (const [index, line] of lines.entries()) {
        line.classList.add("is-shown");
        if (index === 2) setTimeout(() => id === run && lane("zsh").forEach((l) => l.classList.add("is-shown")), 700);
        await sleep(640 + Math.random() * 320, id);
      }
      setStatus("claude", "done", true);
      await sleep(700, id);
      pointer.classList.add("is-shown");
      await sleep(200, id);
      const target = pointIn(link, 0.5, 0.55);
      pointer.style.left = `${target.x - 3}px`;
      pointer.style.top = `${target.y - 2}px`;
      await sleep(950, id);
      link.classList.add("is-hover");
      await sleep(380, id);
      pointer.classList.add("is-down");
      await sleep(150, id);
      pointer.classList.remove("is-down");
      editor.classList.add("is-open");
      editorTab.classList.add("is-open");
      activate(editorTab);
      await sleep(700, id);
      pointer.classList.remove("is-shown");
    }

    async function play() {
      const id = ++run;
      try {
        while (true) {
          reset();
          await Promise.all([streamCodex(id), streamClaude(id)]);
          await sleep(4800, id);
          editor.classList.remove("is-open");
          await sleep(500, id);
        }
      } catch {
        // A newer run or a pause cancelled this loop.
      }
    }

    function update() {
      const shouldPlay = visible && !userPaused && !reducedMotion.matches;
      if (shouldPlay) {
        if (!root.classList.contains("is-playing")) {
          root.classList.add("is-playing");
          play();
        }
      } else {
        root.classList.remove("is-playing");
        run++;
        showFinalState();
      }
    }

    if (toggle) {
      toggle.addEventListener("click", () => {
        userPaused = !userPaused;
        toggle.setAttribute("aria-pressed", String(userPaused));
        update();
      });
      if (reducedMotion.matches) toggle.hidden = true;
    }
    reducedMotion.addEventListener("change", () => {
      if (toggle) toggle.hidden = reducedMotion.matches;
      update();
    });

    new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      update();
    }, { threshold: 0.25 }).observe(root);
  }

  function setUpArranger(root) {
    if (!root) return;
    const minis = [...root.querySelectorAll(".mini")];
    const buttons = [...root.querySelectorAll("[data-arrangement]")];
    const g = 1.6;
    const inner = 100 - 2 * g;

    const layouts = {
      tile: () => {
        const w = (100 - 3 * g) / 2;
        return minis.map((_, i) => [g + (i % 2) * (w + g), g + Math.floor(i / 2) * (w + g), w, w]);
      },
      columns: () => {
        const w = (100 - (minis.length + 1) * g) / minis.length;
        return minis.map((_, i) => [g + i * (w + g), g, w, inner]);
      },
      rows: () => {
        const h = (100 - (minis.length + 1) * g) / minis.length;
        return minis.map((_, i) => [g, g + i * (h + g), inner, h]);
      },
      cascade: () => minis.map((_, i) => [g + i * 9.5, g + i * 11, 58, 62]),
      golden: () => {
        const phi = 0.618;
        const w1 = (100 - 3 * g) * phi;
        const x2 = g + w1 + g;
        const w2 = 100 - x2 - g;
        const h2 = (100 - 3 * g) * phi;
        const y3 = g + h2 + g;
        const h3 = 100 - y3 - g;
        const w3 = (w2 - g) * phi;
        return [
          [g, g, w1, inner],
          [x2, g, w2, h2],
          [x2 + w2 - w3, y3, w3, h3],
          [x2, y3, w2 - w3 - g, h3],
        ];
      },
    };

    let current = "tile";
    let timer = 0;
    let interacted = false;

    function apply(name) {
      current = name;
      layouts[name]().forEach(([x, y, w, h], i) => {
        const mini = minis[i];
        mini.style.left = `${x}%`;
        mini.style.top = `${y}%`;
        mini.style.width = `${w}%`;
        mini.style.height = `${h}%`;
      });
      buttons.forEach((button) => {
        button.setAttribute("aria-pressed", String(button.dataset.arrangement === name));
      });
    }

    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        interacted = true;
        clearInterval(timer);
        apply(button.dataset.arrangement);
      });
    });

    const order = buttons.map((button) => button.dataset.arrangement);
    function cycle(on) {
      clearInterval(timer);
      if (!on || interacted || reducedMotion.matches) return;
      timer = setInterval(() => {
        apply(order[(order.indexOf(current) + 1) % order.length]);
      }, 2600);
    }

    apply("tile");
    new IntersectionObserver(([entry]) => cycle(entry.isIntersecting), { threshold: 0.4 }).observe(root);
  }
})();

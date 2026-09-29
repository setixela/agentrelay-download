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

  setUpRelayDemo(document.querySelector("[data-relay-demo]"));
  setUpArranger(document.querySelector("[data-arranger]"));

  function setUpRelayDemo(root) {
    if (!root) return;
    const stage = root.querySelector(".replica-stage");
    const canvas = root.querySelector(".rp-canvas");
    const composer = root.querySelector(".rp-composer");
    const typed = root.querySelector(".rp-typed");
    const messageButton = root.querySelector(".rp-msg");
    const sendButton = root.querySelector(".rp-send");
    const status = root.querySelector(".rp-status");
    const wires = root.querySelector(".rp-wires");
    const cards = [...root.querySelectorAll(".rp-card")];
    const tabs = [...root.querySelectorAll(".rp-bar .rp-tab.is-target")];
    const toggle = document.querySelector("[data-relay-toggle]");
    const message = root.dataset.message || "";
    const sentLabel = status.dataset.sent || "";

    let run = 0;
    let visible = false;
    let userPaused = false;

    const sleep = (ms, id) => new Promise((resolve, reject) => {
      setTimeout(() => (id === run ? resolve() : reject(new Error("cancelled"))), ms);
    });

    function reveals(card) {
      return [...card.querySelectorAll(".rp-reveal")];
    }

    function showFinalState() {
      root.classList.remove("is-armed");
      composer.classList.remove("is-open");
      wires.replaceChildren();
      typed.textContent = message;
      status.textContent = sentLabel;
      tabs.forEach((tab) => tab.classList.add("is-target"));
      root.classList.add("has-targets");
      cards.forEach((card) => {
        card.classList.remove("is-hit");
        reveals(card).forEach((line) => line.classList.add("is-shown"));
      });
    }

    function reset() {
      root.classList.add("is-armed");
      composer.classList.remove("is-open");
      wires.replaceChildren();
      wires.classList.remove("is-faded");
      typed.textContent = "";
      status.textContent = "";
      tabs.forEach((tab) => tab.classList.remove("is-target"));
      root.classList.remove("has-targets");
      cards.forEach((card) => {
        card.classList.remove("is-hit");
        reveals(card).forEach((line) => line.classList.remove("is-shown"));
      });
    }

    function pointIn(element, xFraction, yFraction) {
      const stageBox = stage.getBoundingClientRect();
      const box = element.getBoundingClientRect();
      const canvasBox = canvas.getBoundingClientRect();
      const scale = stageBox.width / stage.offsetWidth;
      return {
        x: (box.left + box.width * xFraction - canvasBox.left) / scale,
        y: (box.top + box.height * yFraction - canvasBox.top) / scale,
      };
    }

    function drawWires() {
      const ns = "http://www.w3.org/2000/svg";
      const origin = pointIn(messageButton, 0.5, 1);
      origin.y = Math.max(origin.y, 0);
      return cards.map((card, index) => {
        const target = pointIn(card.querySelector(".rp-in"), 0, 0.5);
        target.x += 6;
        const color = getComputedStyle(card).getPropertyValue("--c").trim();
        const d = `M ${origin.x} ${origin.y} C ${origin.x} ${origin.y + target.y * 0.55}, ${target.x - 90} ${target.y}, ${target.x} ${target.y}`;
        const path = document.createElementNS(ns, "path");
        path.setAttribute("d", d);
        path.style.color = color;
        path.style.stroke = color;
        const dot = document.createElementNS(ns, "circle");
        dot.setAttribute("r", "4");
        dot.style.color = color;
        dot.style.offsetPath = `path("${d}")`;
        wires.append(path, dot);
        const length = path.getTotalLength();
        path.style.strokeDasharray = `${length}`;
        path.style.strokeDashoffset = `${length}`;
        const delay = index * 110;
        path.animate(
          [{ strokeDashoffset: length }, { strokeDashoffset: 0 }],
          { duration: 820, delay, easing: "cubic-bezier(0.22, 1, 0.36, 1)", fill: "forwards" }
        );
        dot.animate(
          [
            { offsetDistance: "0%", opacity: 0 },
            { offsetDistance: "8%", opacity: 1, offset: 0.08 },
            { offsetDistance: "96%", opacity: 1, offset: 0.96 },
            { offsetDistance: "100%", opacity: 0 },
          ],
          { duration: 820, delay, easing: "cubic-bezier(0.45, 0, 0.2, 1)", fill: "forwards" }
        );
        return delay + 820;
      });
    }

    async function play() {
      const id = ++run;
      try {
        while (true) {
          reset();
          await sleep(700, id);
          messageButton.classList.add("is-pressed");
          await sleep(160, id);
          messageButton.classList.remove("is-pressed");
          composer.classList.add("is-open");
          await sleep(350, id);
          for (const tab of tabs) {
            tab.classList.add("is-target");
            await sleep(140, id);
          }
          root.classList.add("has-targets");
          await sleep(300, id);
          for (let i = 1; i <= message.length; i++) {
            typed.textContent = message.slice(0, i);
            await sleep(message[i - 1] === " " ? 55 : 32 + Math.random() * 26, id);
          }
          await sleep(520, id);
          sendButton.classList.add("is-pressed");
          await sleep(180, id);
          sendButton.classList.remove("is-pressed");
          composer.classList.remove("is-open");
          await sleep(160, id);
          const arrivals = drawWires();
          await Promise.all(cards.map(async (card, index) => {
            await sleep(arrivals[index], id);
            card.classList.add("is-hit");
            const lines = reveals(card);
            for (const line of lines) {
              line.classList.add("is-shown");
              await sleep(line.classList.contains("rp-in") ? 520 : 380 + Math.random() * 380, id);
            }
          }));
          status.textContent = sentLabel;
          await sleep(500, id);
          wires.classList.add("is-faded");
          cards.forEach((card) => card.classList.remove("is-hit"));
          await sleep(5200, id);
        }
      } catch {
        // A newer run or a pause cancelled this loop.
      }
    }

    function stop() {
      run++;
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
        stop();
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

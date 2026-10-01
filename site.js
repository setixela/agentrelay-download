(() => {
  "use strict";
  document.documentElement.classList.add("js");
  const menu = document.querySelector(".menu-toggle");
  const nav = document.querySelector("#main-nav");
  const closeMenu = () => {
    menu.setAttribute("aria-expanded", "false");
    nav.classList.remove("is-open");
  };
  menu.addEventListener("click", () => {
    const open = menu.getAttribute("aria-expanded") !== "true";
    menu.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("is-open", open);
  });
  nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menu.getAttribute("aria-expanded") === "true") {
      closeMenu();
      menu.focus();
    }
  });
  document.querySelectorAll("[data-git-example]").forEach((example) => {
    const buttons = [...example.querySelectorAll("[data-commit]")];
    const details = [...example.querySelectorAll("[data-commit-detail]")];
    buttons.forEach((button) => button.addEventListener("click", () => {
      buttons.forEach((item) => item.setAttribute("aria-pressed", String(item === button)));
      details.forEach((item) => { item.hidden = item.dataset.commitDetail !== button.dataset.commit; });
    }));
  });
  const views = [...document.querySelectorAll("[data-view]")];
  const panels = [...document.querySelectorAll("[data-panel]")];
  const showView = (view) => {
    views.forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.view === view)));
    panels.forEach((panel) => { panel.hidden = panel.dataset.panel !== view; });
  };
  views.forEach((button) => button.addEventListener("click", () => showView(button.dataset.view)));
  showView("branches");
  document.querySelectorAll("[data-language]").forEach((link) => {
    link.addEventListener("click", () => { link.hash = window.location.hash; });
  });
  const releaseNotes = document.querySelector("#release-notes");
  document.querySelectorAll("[data-open-notes]").forEach((link) => link.addEventListener("click", () => {
    releaseNotes.open = true;
  }));
  if (window.location.hash === "#release-notes") releaseNotes.open = true;
})();

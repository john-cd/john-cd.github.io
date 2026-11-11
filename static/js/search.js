/** Search the local index and render keyboard-navigable, text-only suggestions. */
(function () {
  const input = document.getElementById("userinput");
  const suggestions = document.getElementById("suggestions");
  if (!input || !suggestions || !window.elasticlunr || !window.searchIndex) {
    return;
  }

  const index = window.elasticlunr.Index.load(window.searchIndex);
  const maxResults = 8;

  function closeSuggestions() {
    suggestions.replaceChildren();
    suggestions.classList.add("d-none");
    input.setAttribute("aria-expanded", "false");
  }

  function cleanText(value) {
    // Search-index bodies may include HTML; excerpts should remain plain text.
    return value.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
  }

  function escapeRegExp(value) {
    return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function addHighlightedText(element, value, terms) {
    // Build highlights from text nodes so indexed content is never parsed as markup.
    const alternatives = terms
      .filter((term) => term.length > 1)
      .sort((left, right) => right.length - left.length)
      .map(escapeRegExp);

    if (alternatives.length === 0) {
      element.textContent = value;
      return;
    }

    const matcher = new RegExp(`(${alternatives.join("|")})`, "ig");
    let cursor = 0;

    for (const match of value.matchAll(matcher)) {
      element.append(document.createTextNode(value.slice(cursor, match.index)));
      const highlight = document.createElement("b");
      highlight.textContent = match[0];
      element.append(highlight);
      cursor = match.index + match[0].length;
    }

    element.append(document.createTextNode(value.slice(cursor)));
  }

  function makeTeaser(body, terms) {
    const text = cleanText(body);
    if (text.length <= 220) {
      return text;
    }

    const firstMatch = terms
      .map((term) => text.toLowerCase().indexOf(term.toLowerCase()))
      .filter((position) => position >= 0)
      .sort((left, right) => left - right)[0];
    const start = Math.max(0, (firstMatch ?? 0) - 80);
    const end = Math.min(text.length, start + 220);
    return `${start > 0 ? "…" : ""}${text.slice(start, end)}${end < text.length ? "…" : ""}`;
  }

  function showResults() {
    const query = input.value.trim();
    suggestions.replaceChildren();

    if (!query) {
      closeSuggestions();
      return;
    }

    const terms = query.split(/\s+/).filter(Boolean);
    const results = index.search(query, {
      bool: "OR",
      fields: {
        title: { boost: 2 },
        body: { boost: 1 },
      },
    });

    for (const result of results.slice(0, maxResults)) {
      const document = result.doc;
      if (!document || !document.body) {
        continue;
      }

      const row = document.createElement("div");
      const link = document.createElement("a");
      const title = document.createElement("span");
      const teaser = document.createElement("span");

      link.href = result.ref;
      title.textContent = document.title;
      addHighlightedText(teaser, makeTeaser(document.body, terms), terms);
      link.append(title, teaser);
      row.append(link);
      suggestions.append(row);
    }

    const hasResults = suggestions.childElementCount > 0;
    suggestions.classList.toggle("d-none", !hasResults);
    input.setAttribute("aria-expanded", String(hasResults));
  }

  function moveFocus(event) {
    if (suggestions.classList.contains("d-none")) {
      return;
    }

    const links = Array.from(suggestions.querySelectorAll("a"));
    if (links.length === 0) {
      return;
    }

    const current = links.indexOf(document.activeElement);
    if (event.key === "ArrowDown") {
      event.preventDefault();
      links[Math.min(current + 1, links.length - 1)]?.focus();
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      if (current <= 0) {
        input.focus();
      } else {
        links[current - 1]?.focus();
      }
    }
  }

  input.addEventListener("input", showResults);
  document.addEventListener("keydown", (event) => {
    const target = event.target;
    const isTextField = target instanceof HTMLElement &&
      (target.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(target.tagName));

    if (event.key === "/" && !isTextField && !event.ctrlKey && !event.metaKey && !event.altKey) {
      event.preventDefault();
      input.focus();
      return;
    }

    if (event.key === "Escape" && !suggestions.classList.contains("d-none")) {
      closeSuggestions();
      input.blur();
      return;
    }

    if ((event.key === "ArrowDown" || event.key === "ArrowUp") &&
        (document.activeElement === input || suggestions.contains(document.activeElement))) {
      moveFocus(event);
    }
  });

  document.addEventListener("click", (event) => {
    if (!input.contains(event.target) && !suggestions.contains(event.target)) {
      closeSuggestions();
    }
  });
}());

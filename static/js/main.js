/** Apply the saved or system theme and keep the toggle usable without storage. */
const modeButton = document.getElementById("mode");
const themeStorageKey = "theme";

function readThemePreference() {
  // Browser storage may be unavailable in private or restricted contexts.
  try {
    return localStorage.getItem(themeStorageKey);
  } catch {
    return null;
  }
}

function saveThemePreference(theme) {
  // Persist the choice when available; theme changes still work otherwise.
  try {
    localStorage.setItem(themeStorageKey, theme);
  } catch {
    // The theme toggle still works when browser storage is disabled.
  }
}

const savedTheme = readThemePreference();
const prefersDark = window.matchMedia?.("(prefers-color-scheme: dark)").matches;
if (savedTheme === "dark" || (!savedTheme && prefersDark)) {
  document.body.classList.add("dark");
}

modeButton?.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  saveThemePreference(document.body.classList.contains("dark") ? "dark" : "light");
});

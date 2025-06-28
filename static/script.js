// Theme switcher functionality
document.addEventListener("DOMContentLoaded", function () {
  // Check for saved theme preference
  const savedTheme = localStorage.getItem("theme") || "light";
  setTheme(savedTheme);

  // Theme switcher button
  const themeSwitcher = document.createElement("div");
  themeSwitcher.className = "theme-switcher";
  themeSwitcher.innerHTML = `
        <button id="theme-toggle" class="btn btn-secondary">
            Toggle Theme
        </button>
    `;
  document.body.appendChild(themeSwitcher);

  document
    .getElementById("theme-toggle")
    .addEventListener("click", function () {
      const currentTheme = document.body.classList.contains("dark-theme")
        ? "light"
        : "dark";
      setTheme(currentTheme);
      localStorage.setItem("theme", currentTheme);
    });
});

function setTheme(theme) {
  if (theme === "dark") {
    document.body.classList.add("dark-theme");
    document.getElementById("theme-toggle").textContent = "Light Mode";
  } else {
    document.body.classList.remove("dark-theme");
    document.getElementById("theme-toggle").textContent = "Dark Mode";
  }
}

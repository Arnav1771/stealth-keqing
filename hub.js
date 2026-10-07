// ?app=pinfiles (or ?app=pinfiles,fahh) preselects those apps in the signup sentence.
const wanted = new URLSearchParams(location.search).get("app");
if (wanted) {
  for (const slug of wanted.split(",")) {
    const box = document.querySelector(`.pick input[data-app="${CSS.escape(slug.trim())}"]`);
    if (box) box.checked = true;
  }
  document.getElementById("email")?.focus({ preventScroll: true });
}

/* JusJob - search.js
 *
 * Kjører inni et privilegert Zotero-chrome-vindu (åpnet via openDialog),
 * og har derfor tilgang til Zotero-objektet via wrappedJSObject-trikset.
 */

const Zotero = Components.classes["@zotero.org/Zotero;1"]
  .getService(Components.interfaces.nsISupports)
  .wrappedJSObject;

// TODO: bytt til faktisk GitHub Pages-URL når jusjob-data er publisert dit.
const INDEX_URL = "https://sstraume97.github.io/JusJob/search-index.json";

let searchIndex = [];

async function loadIndex() {
  const statusEl = document.getElementById("jusjob-status");
  try {
    const resp = await fetch(INDEX_URL);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    searchIndex = await resp.json();
    statusEl.textContent = `${searchIndex.length} elementer i indeksen`;
  } catch (e) {
    statusEl.textContent = `Kunne ikke laste indeks: ${e.message}`;
    Zotero.logError(e);
  }
}

function search(query) {
  const q = query.trim().toLowerCase();
  if (!q) return [];
  return searchIndex.filter(
    (item) =>
      item.title.toLowerCase().includes(q) ||
      (item.snippet || "").toLowerCase().includes(q) ||
      (item.court_or_body || "").toLowerCase().includes(q)
  );
}

function render(results) {
  const container = document.getElementById("jusjob-results");
  container.textContent = "";
  for (const item of results.slice(0, 200)) {
    const row = document.createElementNS("http://www.w3.org/1999/xhtml", "div");
    row.style.cssText =
      "padding:8px;border-bottom:1px solid #eee;cursor:pointer;";
    row.innerHTML = `<strong>[${item.source}]</strong> ${item.title}` +
      `<div style="color:#666;font-size:12px;">${item.court_or_body || ""} — ${item.snippet || ""}</div>`;
    row.addEventListener("click", () => importItem(item));
    container.appendChild(row);
  }
  if (results.length === 0) {
    container.textContent = "Ingen treff.";
  }
}

function zoteroItemTypeFor(item) {
  if (item.source === "rettspraksis.no") return "case";
  return "document";
}

async function importItem(item) {
  const zoteroPane = Zotero.getActiveZoteroPane();
  const libraryID = zoteroPane.getSelectedLibraryID();
  const itemType = zoteroItemTypeFor(item);
  const newItem = new Zotero.Item(itemType);
  newItem.libraryID = libraryID;

  if (itemType === "case") {
    newItem.setField("caseName", item.title);
    newItem.setField("court", item.court_or_body || "");
  } else {
    newItem.setField("title", item.title);
    newItem.setField("publisher", item.court_or_body || item.source);
  }
  newItem.setField("url", item.url);
  newItem.setField(
    "extra",
    `JusJob-kilde: ${item.source}\nType: ${item.type}\nID: ${item.id}`
  );

  await newItem.saveTx();
  zoteroPane.selectItem(newItem.id);
}

window.addEventListener("load", async () => {
  await loadIndex();
  document
    .getElementById("jusjob-search-input")
    .addEventListener("input", (e) => render(search(e.target.value)));
});

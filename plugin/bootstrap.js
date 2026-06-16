/* JusJob - bootstrap.js
 *
 * Følger Zotero 7 sin dokumenterte bootstrap-konvensjon: onMainWindowLoad og
 * onMainWindowUnload kalles automatisk av Zotero for hvert hovedvindu, uten
 * at vi selv må håndtere Services.wm-lyttere.
 * https://www.zotero.org/support/dev/zotero_7_for_developers
 */

function install(data, reason) {}

async function startup({ id, version, resourceURI, rootURI }, reason) {
  await Zotero.initializationPromise;
}

function onMainWindowLoad({ window }) {
  const doc = window.document;
  const toolsMenu = doc.getElementById("menu_ToolsPopup");
  if (!toolsMenu) return;

  const menuitem = doc.createXULElement("menuitem");
  menuitem.id = "jusjob-search-menuitem";
  menuitem.setAttribute("label", "Søk i rettskilder (JusJob)…");
  menuitem.addEventListener("command", () => {
    window.openDialog(
      "chrome://jusjob/content/search.xhtml",
      "jusjob-search",
      "chrome,centerscreen,resizable,width=900,height=650"
    );
  });
  toolsMenu.appendChild(menuitem);
}

function onMainWindowUnload({ window }) {
  window.document.getElementById("jusjob-search-menuitem")?.remove();
}

function shutdown(data, reason) {
  // APP_SHUTDOWN = 2: ikke bry oss med opprydding når hele appen avsluttes
  if (reason === 2) return;
}

function uninstall(data, reason) {}

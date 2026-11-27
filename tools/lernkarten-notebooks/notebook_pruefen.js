// Führt alle Zellen eines Notebooks in einer lokal gebauten JupyterLite-Seite aus
// und gibt für jede Code-Zelle die Ausgabe aus, bei App-Fenstern auch deren Konsole.
//
// Aufruf:  node notebook_pruefen.js http://localhost:8000 M04_JavaScript_im_Fenster.ipynb
//
// Voraussetzungen: Playwright mit Chromium, und eine Testseite, die mit
// overrides.json (windowingMode "none") gebaut wurde, siehe README.md.
const { chromium } = require('playwright');

(async () => {
  const [, , basis, notebook] = process.argv;
  if (!basis || !notebook) {
    console.error('Aufruf: node notebook_pruefen.js <basis-url> <notebook.ipynb>');
    process.exit(2);
  }
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1300, height: 950 } });
  await page.goto(basis.replace(/\/$/, '') + '/lab/index.html?path=' + notebook);
  await page.waitForSelector('.jp-Notebook .jp-Cell', { timeout: 120000 });
  await page.waitForTimeout(4000);

  const zellen = page.locator('.jp-Notebook .jp-Cell');
  const anzahl = await zellen.count();
  let erste = true;
  for (let i = 0; i < anzahl; i++) {
    const istCode = await zellen.nth(i).evaluate(e => e.classList.contains('jp-CodeCell'));
    if (!istCode) continue;
    await zellen.nth(i).click();
    await page.keyboard.press('Escape');
    await page.keyboard.press('Shift+Enter');
    // Die erste Code-Zelle ist die Werkzeugkiste; der Kernel braucht beim Start etwas länger.
    await page.waitForTimeout(erste ? 6000 : 1500);
    erste = false;

    const bericht = await zellen.nth(i).evaluate(e => {
      const quelle = (e.querySelector('.cm-content')?.innerText || '').split('\n')[0];
      const ausgaben = [...e.querySelectorAll('.jp-OutputArea-output')]
        .filter(o => !o.querySelector('iframe'))
        .map(o => o.innerText.trim())
        .filter(t => t);
      const konsolen = [...e.querySelectorAll('.lk-konsole')].map(k => k.innerText.trim()).filter(t => t);
      const fenster = e.querySelectorAll('iframe').length;
      return { quelle, ausgaben, konsolen, fenster };
    });
    console.log(`#${i} ${bericht.quelle}`);
    bericht.ausgaben.forEach(t => console.log(t.split('\n').map(z => '   ' + z).join('\n')));
    if (bericht.fenster) console.log(`   [${bericht.fenster} Fenster]`);
    bericht.konsolen.forEach(t => console.log('   Konsole: ' + t.replace(/\n/g, ' ⏎ ')));
  }
  await browser.close();
})();

/* Run against the generated offline file in a real Chromium browser.
 * node scripts/test_investigation_browser.cjs /path/to/playwright [publisher.html]
 * Set CTI_BROWSER_EXECUTABLE to use an installed Chrome binary locally.
 */
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require(process.argv[2] ? path.resolve(process.argv[2]) : 'playwright');

const output = path.resolve(__dirname, '../outputs/investigation');
const artifact = pathToFileURL(path.join(output, 'index.html')).href;

async function assertLayout(page) {
    const layout = await page.evaluate(() => ({
        viewport: document.documentElement.clientWidth,
        document: document.documentElement.scrollWidth,
        controls: [...document.querySelectorAll('select, button')].map(control => {
            const {left, right} = control.getBoundingClientRect();
            return {id: control.id, left, right};
        }),
    }));
    assert.ok(layout.document <= layout.viewport, JSON.stringify(layout));
    for (const {id, left, right} of layout.controls) {
        assert.ok(left >= 0 && right <= layout.viewport, `${id} clips at width ${layout.viewport}`);
    }
}

async function checkWidth(browser, width) {
    const context = await browser.newContext({viewport: {width, height: 900}, offline: true});
    const requests = [];
    await context.route(/^https?:/, async route => {
        requests.push(route.request().url());
        await route.abort();
    });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    try {
        await page.goto(artifact);
        const verdict = page.locator('#verdict h2');
        assert.match(await verdict.textContent(), /No supporting sequence/);
        assert.match(await page.locator('#projection').textContent(), /run_nslookup_batch/);
        await assertLayout(page);

        await page.keyboard.press('Tab');
        assert.equal(await page.locator(':focus').getAttribute('id'), 'case');
        for (const id of ['profile', 'q0', 'q1', 'q2', 'example', 'core']) {
            await page.keyboard.press('Tab');
            assert.equal(await page.locator(':focus').getAttribute('id'), id);
        }
        await page.keyboard.press('Enter');
        assert.match(await verdict.textContent(), /Supported in this interpretation/);
        await assertLayout(page);
        await page.screenshot({path: path.join(output, `browser-${width}.png`), fullPage: true});

        for (const [i, technique] of ['T1218', 'T1059', 'T1560'].entries()) {
            await page.locator(`#q${i}`).selectOption(technique);
        }
        assert.match(await verdict.textContent(), /Unresolved mapping/);
        await assertLayout(page);
        const labels = await page.getByRole('region', {name: 'Investigation controls'}).ariaSnapshot();
        for (const name of ['Intrusion report', 'Interpretation profile', 'First technique', 'Second technique', 'Third technique']) {
            assert.ok(labels.includes(`combobox "${name}"`), labels);
        }

        if (width === 1280) {
            await page.getByRole('button', {name: 'Show a supported chain'}).click();
            await page.getByText('Read matching source passages locally', {exact: true}).click();
            const source = page.getByLabel('Matching publisher HTML');
            if (process.argv[3]) {
                await source.setInputFiles(path.resolve(process.argv[3]));
                await page.getByText(/Matching source loaded/).waitFor();
            }
            await source.setInputFiles({name: 'different.html', mimeType: 'text/html',
                buffer: Buffer.from('<p>Other source.<img src="https://example.invalid/unexpected.png"></p>')});
            await page.getByText(/Source snapshot does not match/).waitFor();

            await page.getByRole('button', {name: 'Show the misleading join'}).click();
            const [download] = await Promise.all([
                page.waitForEvent('download'),
                page.getByRole('button', {name: 'Download answer record'}).click(),
            ]);
            const file = path.join(output, 'browser-export.json');
            await download.saveAs(file);
            const record = JSON.parse(await fs.readFile(file, 'utf8'));
            assert.equal(record.answer.status, 'NOT_SUPPORTED');
            assert.deepEqual(record.answer.query, ['T1560', 'T1059', 'T1560']);
        }
        await page.locator('#case').selectOption('cisa-former-account');
        assert.equal(await verdict.textContent(), 'Sequence comparison unassessed');
        for (const id of ['q0', 'q1', 'q2', 'download']) {
            assert.ok(await page.locator('#' + id).isDisabled());
        }
        assert.match(await page.locator('#witnesses').textContent(), /PDF page \d+/);
        assert.match(await page.locator('#caveats').textContent(), /Excluded interpretations/);
        assert.ok(await page.locator('#local-source').isHidden());
        await assertLayout(page);

        await page.locator('#case').selectOption('cisa-federal-agency');
        for (const id of ['q0', 'q1', 'q2']) await page.locator('#' + id).selectOption('T1190');
        assert.match(await verdict.textContent(), /Unresolved mapping/);
        assert.match(await page.locator('#witnesses').textContent(), /Would require:/);
        assert.match(await page.locator('#witnesses').textContent(), /PDF page \d+/);
        await assertLayout(page);
        if (width === 1280) {
            const [download] = await Promise.all([
                page.waitForEvent('download'),
                page.locator('#download').click(),
            ]);
            const file = path.join(output, 'browser-cisa-export.json');
            await download.saveAs(file);
            const record = JSON.parse(await fs.readFile(file, 'utf8'));
            assert.equal(record.case_key, 'cisa-federal-agency');
            assert.equal(record.answer.status, 'UNRESOLVED_MAPPING');
            assert.deepEqual(record.answer.query, ['T1190', 'T1190', 'T1190']);
        }
        assert.deepEqual(requests, []);
        assert.deepEqual(errors, []);
    } finally {
        await context.close();
    }
}

(async () => {
    const browser = await chromium.launch({
        headless: true, executablePath: process.env.CTI_BROWSER_EXECUTABLE || undefined,
    });
    try {
        for (const width of [320, 390, 1280]) await checkWidth(browser, width);
        console.log(JSON.stringify({browser: browser.version(), widths: [320, 390, 1280],
            keyboard: 'pass', sourceRejected: true, matchingSourceChecked: Boolean(process.argv[3]),
            offlineExport: 'pass'}));
    } finally {
        await browser.close();
    }
})().catch(error => {
    console.error(error);
    process.exitCode = 1;
});

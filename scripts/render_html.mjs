#!/usr/bin/env node
/** Render local HTML to PNG/JPEG using Chrome DevTools Protocol without npm dependencies. */

import { spawn } from "node:child_process";
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, isAbsolute, resolve } from "node:path";
import { pathToFileURL } from "node:url";

function fail(message) {
  process.stderr.write(`render_html: ${message}\n`);
  process.exit(2);
}

if (!globalThis.WebSocket) {
  fail("Node.js 22+ is required because the dependency-free renderer uses the built-in WebSocket API");
}

function usage() {
  process.stdout.write(`Usage: render_html.mjs INPUT.html OUTPUT.png [options]

Options:
  --width N          viewport width (default: 1440)
  --height N         viewport height (default: 900)
  --dpr N            device scale factor (default: 1)
  --full-page        capture the full document (default)
  --viewport         capture only the viewport
  --selector CSS     capture one element instead of the full page
  --wait-ms N        extra wait after fonts/images settle (default: 200)
  --max-height N     cap full-page height (default: 20000)
  --format png|jpeg  output format inferred from extension by default
  --quality N        JPEG quality 0-100 (default: 90)
  --chrome PATH      Chrome/Chromium executable; CHROME_PATH also works
`);
}

function parseArgs(argv) {
  if (argv.length < 2 || argv.includes("--help")) {
    usage();
    process.exit(argv.includes("--help") ? 0 : 2);
  }
  const options = {
    input: argv[0], output: argv[1], width: 1440, height: 900, dpr: 1,
    fullPage: true, selector: null, waitMs: 200, maxHeight: 20000,
    format: null, quality: 90, chrome: process.env.CHROME_PATH || null,
  };
  for (let i = 2; i < argv.length; i += 1) {
    const key = argv[i];
    const take = () => {
      if (i + 1 >= argv.length) fail(`missing value for ${key}`);
      return argv[++i];
    };
    if (key === "--width") options.width = Number(take());
    else if (key === "--height") options.height = Number(take());
    else if (key === "--dpr") options.dpr = Number(take());
    else if (key === "--full-page") options.fullPage = true;
    else if (key === "--viewport") options.fullPage = false;
    else if (key === "--selector") options.selector = take();
    else if (key === "--wait-ms") options.waitMs = Number(take());
    else if (key === "--max-height") options.maxHeight = Number(take());
    else if (key === "--format") options.format = take();
    else if (key === "--quality") options.quality = Number(take());
    else if (key === "--chrome") options.chrome = take();
    else fail(`unknown option: ${key}`);
  }
  for (const key of ["width", "height", "dpr", "maxHeight"]) {
    if (!Number.isFinite(options[key]) || options[key] <= 0) fail(`invalid --${key}: ${options[key]}`);
  }
  if (!Number.isFinite(options.waitMs) || options.waitMs < 0) fail(`invalid --wait-ms: ${options.waitMs}`);
  if (!Number.isFinite(options.quality) || options.quality < 0 || options.quality > 100) fail(`invalid quality: ${options.quality}`);
  return options;
}

function findChrome(explicit) {
  const candidates = [
    explicit,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  ].filter(Boolean);
  const found = candidates.find((candidate) => existsSync(candidate));
  if (!found) fail("Chrome/Chromium not found; pass --chrome or set CHROME_PATH");
  return found;
}

function sleep(ms) { return new Promise((resolvePromise) => setTimeout(resolvePromise, ms)); }

async function waitForFile(path, timeoutMs = 10000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (existsSync(path)) return;
    await sleep(50);
  }
  fail(`timed out waiting for ${basename(path)}`);
}

class Cdp {
  constructor(url) {
    this.id = 0;
    this.pending = new Map();
    this.ws = new WebSocket(url);
  }
  async connect() {
    await new Promise((resolvePromise, reject) => {
      this.ws.addEventListener("open", resolvePromise, { once: true });
      this.ws.addEventListener("error", reject, { once: true });
    });
    this.ws.addEventListener("message", (event) => {
      const message = JSON.parse(event.data);
      if (!message.id || !this.pending.has(message.id)) return;
      const { resolvePromise, reject } = this.pending.get(message.id);
      this.pending.delete(message.id);
      if (message.error) reject(new Error(message.error.message));
      else resolvePromise(message.result || {});
    });
  }
  send(method, params = {}) {
    const id = ++this.id;
    return new Promise((resolvePromise, reject) => {
      this.pending.set(id, { resolvePromise, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }
  close() { this.ws.close(); }
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const input = resolve(options.input);
  const output = resolve(options.output);
  if (!existsSync(input)) fail(`input not found: ${input}`);
  if (!existsSync(dirname(output))) fail(`output directory not found: ${dirname(output)}`);

  const format = (options.format || (output.toLowerCase().endsWith(".jpg") || output.toLowerCase().endsWith(".jpeg") ? "jpeg" : "png")).toLowerCase();
  if (!["png", "jpeg"].includes(format)) fail(`unsupported format: ${format}`);

  const profile = mkdtempSync(resolve(tmpdir(), "qiaomu-chart-report-"));
  const chrome = findChrome(options.chrome);
  const chromeArgs = [
    "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
    "--no-default-browser-check", "--disable-background-networking",
    "--disable-component-update", "--disable-sync", "--metrics-recording-only",
    "--remote-debugging-port=0", `--user-data-dir=${profile}`, "about:blank",
  ];
  const browser = spawn(chrome, chromeArgs, { stdio: ["ignore", "ignore", "pipe"] });
  let stderr = "";
  browser.stderr.on("data", (chunk) => { stderr += chunk.toString(); });

  try {
    const portFile = resolve(profile, "DevToolsActivePort");
    await waitForFile(portFile);
    const [port] = readFileSync(portFile, "utf8").trim().split(/\r?\n/);
    const created = await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: "PUT" });
    if (!created.ok) fail(`DevTools target creation failed: HTTP ${created.status}`);
    const target = await created.json();
    const cdp = new Cdp(target.webSocketDebuggerUrl);
    await cdp.connect();
    try {
      await cdp.send("Page.enable");
      await cdp.send("Runtime.enable");
      await cdp.send("Emulation.setDeviceMetricsOverride", {
        width: Math.round(options.width), height: Math.round(options.height),
        deviceScaleFactor: options.dpr, mobile: options.width <= 480,
      });
      await cdp.send("Page.navigate", { url: pathToFileURL(input).href });
      await cdp.send("Runtime.evaluate", {
        expression: `new Promise(resolve => {
          const done = () => Promise.all([
            document.fonts ? document.fonts.ready : Promise.resolve(),
            ...Array.from(document.images).map(img => img.complete ? Promise.resolve() : new Promise(r => { img.addEventListener('load', r, {once:true}); img.addEventListener('error', r, {once:true}); })),
            window.__QIAOMU_CHARTS_READY__ ? Promise.resolve(window.__QIAOMU_CHARTS_READY__) : Promise.resolve()
          ]).then(() => setTimeout(resolve, ${Math.round(options.waitMs)}));
          if (document.readyState === 'complete') done(); else addEventListener('load', done, {once:true});
        })`,
        awaitPromise: true,
        returnByValue: true,
      });

      const chartStateResult = await cdp.send("Runtime.evaluate", {
        expression: `(() => ({
          count: document.querySelectorAll('[data-qiaomu-chart]').length,
          ready: document.querySelectorAll('[data-qiaomu-chart][data-chart-ready="true"]').length,
          errors: Array.isArray(window.__QIAOMU_CHART_ERRORS__) ? window.__QIAOMU_CHART_ERRORS__ : []
        }))()`,
        returnByValue: true,
      });
      const chartState = chartStateResult.result?.value || { count: 0, ready: 0, errors: [] };
      if (chartState.errors.length) fail(`chart runtime errors: ${chartState.errors.join(" | ")}`);
      if (chartState.count && chartState.ready !== chartState.count) fail(`charts not ready: ${chartState.ready}/${chartState.count}`);

      let clip;
      let clipped = false;
      if (options.selector) {
        const result = await cdp.send("Runtime.evaluate", {
          expression: `(() => { const el = document.querySelector(${JSON.stringify(options.selector)}); if (!el) return null; const r = el.getBoundingClientRect(); return {x:r.left+scrollX,y:r.top+scrollY,width:r.width,height:r.height}; })()`,
          returnByValue: true,
        });
        if (!result.result?.value) fail(`selector not found: ${options.selector}`);
        clip = { ...result.result.value, scale: 1 };
      } else if (options.fullPage) {
        const metrics = await cdp.send("Page.getLayoutMetrics");
        const content = metrics.cssContentSize || metrics.contentSize;
        const height = Math.min(Math.ceil(content.height), options.maxHeight);
        clipped = content.height > options.maxHeight;
        clip = { x: 0, y: 0, width: Math.ceil(content.width), height, scale: 1 };
      } else {
        clip = { x: 0, y: 0, width: options.width, height: options.height, scale: 1 };
      }

      const capture = await cdp.send("Page.captureScreenshot", {
        format,
        ...(format === "jpeg" ? { quality: Math.round(options.quality) } : {}),
        clip,
        captureBeyondViewport: true,
        fromSurface: true,
      });
      writeFileSync(output, Buffer.from(capture.data, "base64"));
      process.stdout.write(`${JSON.stringify({
        ok: true, input, output, format, viewport: { width: options.width, height: options.height, dpr: options.dpr },
        capture: clip, full_page: options.fullPage && !options.selector, selector: options.selector,
        clipped, max_height: options.maxHeight, charts: chartState,
      }, null, 2)}\n`);
    } finally {
      cdp.close();
    }
  } catch (error) {
    fail(`${error.message}${stderr ? `\nChrome: ${stderr.slice(-1200)}` : ""}`);
  } finally {
    browser.kill("SIGTERM");
    await Promise.race([new Promise((resolvePromise) => browser.once("exit", resolvePromise)), sleep(1500)]);
    if (!browser.killed) browser.kill("SIGKILL");
    rmSync(profile, { recursive: true, force: true });
  }
}

await main();

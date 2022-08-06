window.__selenium_lcp = undefined;
new PerformanceObserver((entryList) => {
  __selenium_lcp = entryList.getEntries()[0];
}).observe({ type: "largest-contentful-paint", buffered: true });

window.__selenium_cls = undefined;
new PerformanceObserver((entryList) => {
  __selenium_cls = entryList.getEntries()[0];
}).observe({ type: "layout-shift", buffered: true });

window.__selenium_ttfb = undefined;
new PerformanceObserver((entryList) => {
  __selenium_ttfb = entryList.getEntries()[0];
}).observe({ type: "navigation", buffered: true });

window.__selenium_fid = undefined;
new PerformanceObserver((entryList) => {
  const fidEntry = entryList.getEntries()[0];
  console.log(fidEntry);
  __selenium_fid = fidEntry.processingStart - fidEntry.startTime;
}).observe({ type: "first-input", buffered: true });

// Create span
const span = document.createElement("span");
span.id = "__selenium_span";
span.style = "position:fixed;top:0;left:0;";
document.documentElement.appendChild(span);

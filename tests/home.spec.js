const { test, expect } = require("@playwright/test");

test.describe("Missing Scientists static site", () => {
  test("desktop homepage renders source-led archive content", async ({ page }) => {
    await page.goto("/");

    await expect(page).toHaveTitle(/Verified Cases, Timelines, and Source Trails/i);
    await expect(page.locator("h1")).toHaveText("Missing Scientists");
    await expect(page.locator('meta[name="description"]')).toHaveAttribute("content", /source-led archive/i);
    await expect(page.locator('meta[name="keywords"]')).toHaveAttribute("content", /Jim Gray/i);
    await expect(page.locator('meta[name="theme-color"]')).toHaveAttribute("content", "#243b3c");
    await expect(page.locator('meta[name="robots"]')).toHaveAttribute("content", /max-image-preview:large/i);
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute("href", "https://missingscientists.lol/");
    await expect(page.locator('meta[property="og:image:alt"]')).toHaveAttribute("content", /editorial cover image/i);

    await expect(page.locator(".case-card")).toHaveCount(4);
    await expect(page.getByRole("heading", { name: "Ettore Majorana" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Carl R. Disch" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Vladimir Alexandrov" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Jim Gray" })).toBeVisible();
    await expect(page.locator(".sources a")).toHaveCount(7);
    await expect(page.getByText("unsupported claims")).toBeVisible();
    await expect(page.getByText("independent source-led archive")).toBeVisible();

    await page.getByRole("link", { name: "Review cases" }).click();
    await expect(page.locator("#cases")).toBeInViewport();

    const structuredData = await page.locator('script[type="application/ld+json"]').allInnerTexts();
    expect(structuredData.join("\n")).toContain('"@type": "WebSite"');
    expect(structuredData.join("\n")).toContain('"@type": "CollectionPage"');
    expect(structuredData.join("\n")).toContain('"name": "Jim Gray"');

    const imagesLoaded = await page.evaluate(() =>
      Array.from(document.images).every((image) => image.complete && image.naturalWidth > 0)
    );
    expect(imagesLoaded).toBe(true);
  });

  test("mobile layout avoids horizontal overflow and keeps cases accessible", async ({ browser }) => {
    const context = await browser.newContext({
      viewport: { width: 390, height: 844 },
      isMobile: true
    });
    const page = await context.newPage();

    await page.goto("/");

    await expect(page.locator("h1")).toBeVisible();
    const casesLink = page.getByRole("navigation").getByRole("link", { name: "Cases", exact: true });
    await expect(casesLink).toBeVisible();
    await casesLink.click();
    await expect(page.locator("#cases")).toBeInViewport();

    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow).toBeLessThanOrEqual(1);
    await expect(page.locator(".case-card")).toHaveCount(4);

    await context.close();
  });

  test("crawl artifacts stay accessible for search engines", async ({ request }) => {
    const robots = await request.get("/robots.txt");
    expect(robots.ok()).toBe(true);
    expect(robots.headers()["cache-control"]).toBe("no-cache");
    expect(await robots.text()).toMatch(/Sitemap: https:\/\/missingscientists\.lol\/sitemap\.xml/);

    const sitemap = await request.get("/sitemap.xml");
    expect(sitemap.ok()).toBe(true);
    expect(sitemap.headers()["cache-control"]).toBe("no-cache");
    expect(await sitemap.text()).toContain("<loc>https://missingscientists.lol/</loc>");
  });

  test("production hosts redirect canonically without blocking ACME probes", async ({ request }) => {
    const apexHttp = await request.get("/", {
      headers: {
        Host: "missingscientists.lol",
        "X-Forwarded-Proto": "http"
      },
      maxRedirects: 0
    });
    expect(apexHttp.status()).toBe(308);
    expect(apexHttp.headers().location).toBe("https://missingscientists.lol/");

    const wwwHttps = await request.get("/?case=gray", {
      headers: {
        Host: "www.missingscientists.lol",
        "X-Forwarded-Proto": "https"
      },
      maxRedirects: 0
    });
    expect(wwwHttps.status()).toBe(308);
    expect(wwwHttps.headers().location).toBe("https://missingscientists.lol/?case=gray");

    const challenge = await request.get("/.well-known/acme-challenge/token", {
      headers: {
        Host: "missingscientists.lol",
        "X-Forwarded-Proto": "http"
      },
      maxRedirects: 0
    });
    expect(challenge.status()).not.toBe(308);
  });

  test("health check responds for deployment probes", async ({ request }) => {
    const response = await request.get("/healthz");
    expect(response.ok()).toBe(true);
    expect(response.headers()["content-type"]).toMatch(/application\/json/);
    expect(await response.json()).toEqual({ ok: true });
  });
});

from playwright.async_api import async_playwright
import asyncio
import csv


async def main():
    csv_filename = "QS_university_scores.csv"
    csv_file = open(csv_filename, "w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["University Name", "QS World University Rankings"])

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.topuniversities.com/university-rankings/world-university-rankings/2023")
        await page.wait_for_timeout(2000)

        pagination_element = await page.query_selector_all("#alt-style-pagination > li")
        last_page_element = await pagination_element[-2].query_selector("a:nth-child(1)")
        n_of_pages = int(await last_page_element.inner_text())

        for page_num in range(0, n_of_pages):
            if page_num != 0:
                pagination_elements = await page.query_selector_all("#alt-style-pagination > li")
                for element in pagination_elements:
                    link = await element.query_selector("a")
                    if link is None:
                        continue
                    if await link.inner_text() == str(page_num + 1):
                        await element.click()
                        await page.wait_for_timeout(2000)
                        break

            table = await page.query_selector('#ranking-data-load')
            table_rows = await table.query_selector_all('._qs-ranking-data-row')

            for row in table_rows:
                university_name = await row.query_selector(".uni-link")
                university_name = await university_name.inner_text()

                ranking = await row.query_selector("._univ-rank")
                ranking = await ranking.inner_text()
                ranking = ranking.replace("=", "")

                print(university_name, ranking)

                # Write the data to the CSV file
                csv_writer.writerow([university_name, ranking])

        await browser.close()

    print(f"QS University Rankings have been scraped and saved to {csv_filename}.")
    csv_file.close()


if __name__ == '__main__':
    asyncio.run(main())

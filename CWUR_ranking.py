from playwright.async_api import async_playwright
import asyncio
import csv


async def main():
    csv_filename = "CWUR_university_scores.csv"
    csv_file = open(csv_filename, "w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["University Name", "CWUR World University Rankings"])

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://cwur.org/2022-23.php')
        await page.wait_for_timeout(1000)

        table = await page.query_selector('#cwurTable')
        table_rows = await table.query_selector_all('tbody > tr')
        for row in table_rows:
            university_name = await row.query_selector('td:nth-child(2) > a:nth-child(1)')
            university_name = await university_name.inner_text()
            ranking = await row.query_selector('td:nth-child(1)')
            ranking = await ranking.inner_text()

            print(university_name, ranking)

            # Write the data to the CSV file
            csv_writer.writerow([university_name, ranking])

        await browser.close()

    print(f"CWUR University Rankings have been scraped and saved to {csv_filename}.")
    csv_file.close()


if __name__ == '__main__':
    asyncio.run(main())

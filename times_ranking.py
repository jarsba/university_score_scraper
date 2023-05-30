from playwright.async_api import async_playwright
import asyncio
import csv


async def main():
    csv_filename = "times_university_scores.csv"
    csv_file = open(csv_filename, "w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["University Name", "Times Higher Education (THE) World University Ranking"])

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://www.timeshighereducation.com/world-university-rankings/2023/world-ranking')
        await page.wait_for_timeout(2000)

        await page.locator("[name=datatable-1_length]").select_option("All")
        await page.wait_for_timeout(2000)

        table = await page.query_selector('table#datatable-1')
        table_body = await table.query_selector('tbody')
        table_rows = await table_body.query_selector_all('tr')

        for row in table_rows:
            # Check if row has institution disabled
            row_attributes = await row.get_attribute('class')
            if "institution-disabled" in row_attributes:
                continue

            university_name = await row.query_selector('a')
            university_name = await university_name.inner_text()
            university_name = university_name.strip()

            ranking = await row.query_selector('td.rank')
            ranking = await ranking.inner_text()
            ranking = ranking.strip().replace("=", "")

            print(university_name, ranking)

            # Write the data to the CSV file
            csv_writer.writerow([university_name, ranking])

        await browser.close()

    print(f"Times University Rankings have been scraped and saved to {csv_filename}.")
    csv_file.close()


if __name__ == '__main__':
    asyncio.run(main())

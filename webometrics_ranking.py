from playwright.async_api import async_playwright
import asyncio
import csv


async def main():
    csv_filename = "webometrics_university_scores.csv"
    csv_file = open(csv_filename, "w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["University Name", "Webometrics Ranking of World Universities"])

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://www.webometrics.info/en/world')
        await page.wait_for_timeout(2000)

        page_number = 1

        while True:
            # print(f"Scraping page {page_number}...")
            table = await page.query_selector('table.tableheader-processed')
            table_body = await table.query_selector('tbody')
            table_rows = await table_body.query_selector_all('tr')

            for row in table_rows:
                university_name = await row.query_selector('td:nth-child(2) > a')
                university_name = await university_name.inner_text()
                university_name = university_name.strip()

                ranking = await row.query_selector('td:nth-child(1)')
                ranking = await ranking.inner_text()
                ranking = ranking.strip().replace("=", "")

                # Write the data to the CSV file
                csv_writer.writerow([university_name, ranking])

            # Check if there is a next page
            pagination_element = await page.query_selector("ul.pager")
            next_element = await pagination_element.query_selector("li.pager-next")
            if pagination_element and next_element:
                next_element = await next_element.query_selector("a")
                next_element = await next_element.get_attribute("href")
                await page.goto(f"https://www.webometrics.info{next_element}")
                await page.wait_for_timeout(2000)
                page_number += 1
            else:
                break

        await browser.close()

    print(f"Webometrics University Rankings have been scraped and saved to {csv_filename}.")
    csv_file.close()


if __name__ == '__main__':
    asyncio.run(main())

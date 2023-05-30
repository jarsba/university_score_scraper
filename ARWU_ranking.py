from playwright.async_api import async_playwright
import asyncio
import csv


async def main():
    csv_filename = "ARWU_university_scores.csv"
    csv_file = open(csv_filename, "w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["University Name", "Academic Ranking of World Universities (ARWU) Ranking"])

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.shanghairanking.com/rankings/arwu/2022")
        await page.wait_for_timeout(2000)

        pagination_element = await page.query_selector(".ant-pagination")
        pagination_items = await pagination_element.query_selector_all(".ant-pagination-item")
        last_page_element = await pagination_items[-1].inner_text()
        n_of_pages = int(last_page_element)

        for page_num in range(0, n_of_pages):
            if page_num != 0:
                pagination_element = await page.query_selector(".ant-pagination")
                page_element = await pagination_element.query_selector(f".ant-pagination-item-{str(page_num + 1)}")
                await page_element.click()
                await page.wait_for_timeout(2000)

            table = await page.query_selector('.rk-table')
            table_body = await table.query_selector('tbody')
            table_rows = await table_body.query_selector_all('tr')

            for row in table_rows:
                university_name = await row.query_selector(".global-univ")
                university_name = await university_name.query_selector(".tooltiptext")
                university_name = await university_name.inner_text()
                university_name = university_name.strip()

                ranking = await row.query_selector(".ranking")
                ranking = await ranking.inner_text()
                ranking = ranking.strip()

                print(university_name, ranking)

                # Write the data to the CSV file
                csv_writer.writerow([university_name, ranking])

        await browser.close()

    print(f"ARWU University Rankings have been scraped and saved to {csv_filename}.")
    csv_file.close()


if __name__ == '__main__':
    asyncio.run(main())

# University Score Scraper

Scrapes data from four different university ranking databases (Times Higher Education Ranking, QS World University Ranking, Academic Ranking of World Universities (ARWU) and Center for World University Rankings (CWUR)) and merges them into one CSV file.

### How to run

1. Install the requirements
```
pip install -r requirements.txt
```

2. Run the four individual scripts for each university
```
python3 times_ranking.py
python3 QS_ranking.py
python3 ARWU_ranking.py
python3 CWUR_ranking.py
```

3. Run the main script to merge individual csv files into one, outputs CSV file *university_scores.csv*
```
python3 main.py
```

4. Optionally: Run the notebook to try to match the university names with the Times Higher Education dataset names and create grouped CSV with the scores
```
jupyter notebook
```

Open the notebook *test_name_similarity_matching.ipynb* in Jupyter Notebook and run all cells. Outputs CSV file *grouped_university_ranking.csv*.

### Data sources

- [Times Higher Education](https://www.timeshighereducation.com/world-university-rankings/2023/world-ranking)
- [QS World University Rankings](https://www.topuniversities.com/university-rankings/world-university-rankings/2023)
- [Academic Ranking of World Universities](https://www.shanghairanking.com/rankings/arwu/2022)
- [Center for World University Rankings](https://cwur.org/2022-23.php)
# Data-Scrapping Coursework

Python scraping exercises organized by meeting (`P2`-`P10`). Scripts use `requests` and `beautifulsoup4` to fetch and parse HTML.

Contents by meeting
- `P2`-`P3`: Basic HTTP requests and simple parsing examples.
- `P4`: Requests + BeautifulSoup workflows (helpers in `P4_1.py`, pagination/saving in `P4_3.py`).
- `P5`-`P7`: Expanded parsing, cleaning, and export examples.
- `P8`-`P10`: Larger scraping tasks and consolidated scripts.

How to run a script
1) `cd` into the `P#` folder.
2) Install dependencies: `pip install requests beautifulsoup4`.
3) Execute the script, e.g., `python P4_3.py`.
4) Check the output directory or printed logs for saved files/results.

Tips
- Inspect target URLs in the scripts before running; update them if the site structure changes.
- Handle network errors gracefully (many scripts raise if the response is not OK).

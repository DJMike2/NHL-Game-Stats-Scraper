# NHL-Game-Stats-Scraper
Scrapes all the stats off the ESPN websites for NHL.

# About
This Python script leverages the power of web scraping to gather comprehensive statistics from NHL games. It utilizes the requests library to fetch web pages and BeautifulSoup to parse HTML content.

# features
Extracts player rosters including Centers, Left Wings, Right Wings, Defense, and Goalies.
Fetches detailed game logs for each player, providing insights like goals, assists, points, penalty minutes, and more.

## Required
team_1_url = 'https://www.espn.com/nhl/team/roster/_/name/nyr/new-york-rangers'
team_2_url = 'https://www.espn.com/nhl/team/roster/_/name/bos/boston-bruins'

Change the URL link to whatever team you wish to scrape data...

# How to Use
Install the required libraries by running pip install requests beautifulsoup4.
Customize the team_1_url and team_2_url variables with URLs of your preferred NHL teams.
Run the script and enjoy analyzing the scraped data!

This project is not affiliated with or endorsed by ESPN or the NHL.

# Work In Progress
- Implement **Stats** and **Bio** section from the website
- Implement previous years (Not sure current data)
- 

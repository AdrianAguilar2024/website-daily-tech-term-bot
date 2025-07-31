# Daily Tech Term Automation Bot

![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)
![GitHub Actions Status](https://github.com/AdrianAguilar2024/website-daily-tech-term-bot/actions/workflows/run_bot.yml/badge.svg)

This is a fully automated Python bot that runs on a daily schedule to update the "Tech Term of the Day" section on my personal portfolio website, [adrian-aguilar.com](https://www.adrian-aguilar.com).

This project serves as a practical demonstration of several key software engineering skills, including API integration, data management with JSON, and CI/CD automation.

---

## How It Works

The entire process is automated using a GitHub Actions workflow that runs once every day.

1.  **Scheduled Trigger:** The workflow is triggered by a `cron` job at 12:00 UTC daily.
2.  **Checkout Repositories:** The Action checks out two repositories: this bot's code and the code for my main portfolio website.
3.  **Run Python Script:** The main `update_term.py` script is executed. This script performs the following actions:
    *   It reads from a local `definitions.json` file, which contains a curated list of technical terms and their definitions.
    *   It randomly selects one term object (title and definition) from this local data source.
    *   Using the term's title, it makes an API call to the **Pexels API** to search for a high-quality, relevant, and royalty-free image.
    *   It then programmatically reads the `index.html` file from my portfolio repository.
4.  **Update Website:** The script uses the **BeautifulSoup** library to parse the HTML, find the specific "Tech Term of the Day" section, and replace the image, title, date, and definition with the new content.
5.  **Commit & Push:** Finally, the GitHub Action commits the modified `index.html` file and pushes the change directly back to my portfolio's repository, triggering a new deployment on GitHub Pages.

The result is a fully automated, self-updating feature on my live portfolio website, requiring zero manual intervention. This self-contained approach is highly reliable and does not depend on the stability of external website structures.

## Technology Stack

*   **Language:** Python 3.10
*   **Key Libraries:**
    *   **JSON:** For reading the local term definition data.
    *   **Pexels-API:** A wrapper for making requests to the Pexels API.
    *   **BeautifulSoup4:** For robustly parsing and modifying the target HTML file.
*   **Automation Engine:** GitHub Actions
*   **API:** Pexels API for royalty-free images

## Project Status

**Complete and Operational.** The bot is running successfully on its daily schedule. Future improvements could involve expanding the `definitions.json` file or adding more data sources.

## Setup

To run this project, you would need:
1.  A GitHub repository for the portfolio site.
2.  A second GitHub repository for this bot.
3.  A `PEXELS_API_KEY` from the Pexels API.
4.  A GitHub Personal Access Token (PAT) with `repo` permissions.
5.  Both the `PEXELS_API_KEY` and `PAT` stored as secrets in the bot's repository.

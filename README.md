# AdsPlusYou
AdsPlusYou is a system to manage the publication of classified ads on specific sites which allows the management of publications and constant updating with the aim of enhancing the ability to reach more people with your product and service offers

Installation

1. Download develop branch as .zip or make a git clone
2. Open command prompt and go to the AdsPlusYou-develop folder
3. Create a Virtual environment

For Python version <= 3

python -m venv ./venv

For Python version > 3

python3 -m venv ./venv

4. Activate the new created environment

.\venv\Scripts\activate

5. Install dependencies using pip and requerements.txt file

pip install -r requirements.txt

6. Download chromedriver v89 browser used to automate browsing tasks from (https://chromedriver.storage.googleapis.com/index.html?path=89.0.4389.23/chromedriver_win32.zip) 
and place the chromedriver.exe file into chromedriver project folder

7. Run app from command line or double click on run_adplusyou.bat directly (if you run run_adplusyou.bat directly you don't need active virtual environment)

python main.py

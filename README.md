# GLPIWatcher
GLPIWatcher is a system to manage opened tickets on GLPI system. It monitors opened tickets and put it on waiting to save working time on statistics of your working performance. It does not uses Rest API or XMLRPC, it just works scraping and interacting directly with the web site, it has been implemented thinking on a GLPI system that not have API enabled

Installation

1. Download main branch as .zip or make a git clone
2. Open command prompt and go to the GLPIWatcher-main folder
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

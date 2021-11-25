## **A web crawler application**  

A web-based application which retrieves and stores Reddit submission and User data based on submission URL search. Retrieved data is stored in a MySQL database for which the interaction is handled via Django web-based graphical user interface.
 
### **BUILD**  
#### **Anaconda**  
1. Download and run Anaconda 64-Bit Graphical installer for Windows: https://www.anaconda.com/products/individual#windows  
   - Install with recommended settings  
   - Default filepath for installation on Windows 10: C:\Users\<your-username>\Anaconda3\  

2. Add Anaconda to Path  
   - Open Start Search, type in "env" and choose "Edit the system environment variables"  
   - In "Advanced" tab, click "Environment Variables"  
   - In "User variables for *", select "Path" and click "Edit..."  
   - Click "New" then "Browse" for Anaconda directory to add the following assuming default installation was used:  
     - C:\Users\<your-username>\Anaconda3\  
     - C:\Users\<your-username>\Anaconda3\Scripts  
     - C:\Users\<your-username>\Anaconda3\Library\bin  

3. Verify installation  
   - Open Command Prompt and run "conda --version" or "where conda"  

#### **MySQL**  
1. Download and install MySQL Server, Workbench and other required components from https://dev.mysql.com/downloads/installer/  
2. Create a file "login\database_login.json"with your database login details using "login\database_login_sample.json" as a reference  

#### **Praw**
1. Register a Reddit account
2. Create an application (e.g. script) for your Reddit account https://www.reddit.com/prefs/apps/  
3. Note down the client_id and client_secret from the newly created Reddit application
4. Create a file "login\praw_login.json"with your reddit login details, client_id and client_secret using "login\praw_login_sample.json" as a reference  

### **INSTALLATION**  
1. Import schema into mysql  
   1. In *MySQL Workbench Local Instance* >> *Server* >> *Data Import*, select *Import from Self-contained File* and load in "webcrawler\dump_webcrawler.sql"  
   2. Set *Default Target Schema* as **webcrawler**
2. Edit *webcrawler/settings.py* *DATABASES* setting to point to your MySQL login instance configuration
3. Open and edit "condapath.txt" to point to your Anaconda installation path  
4. Double-click **install.bat** to start the installation of the environment

### **RUN**  
1. Double-click **run.bat** to start the software  
2. Launch a web browser and run the url shown in the terminal (e.g. http://127.0.0.1:8000/)  
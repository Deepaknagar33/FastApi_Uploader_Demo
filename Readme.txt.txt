1. Clone the Repo from GitHub.

2. Create a new python virtual environment 
	
	python -m venv Environment_Name

3. Activate the environment by 
	
	.\Environment_Name\Scripts\activate

4. Install requirement.txt by 

	pip install -r requirements.txt
	
		Or Use
	
	pip install fastapi uvicorn

5. deactivate the environment by 
	
	deactivate 

6. Install the node and then just install angular 

	npm install -g @angular/cli

7. Check the Angular version

Angular CLI: 20.3.5
Node: 22.20.0
Package Manager: npm 10.9.3
OS: win32 x64

8. After Completing the above Setup. Open terminal and activate the virtual environment and change directory to 
app/backend and execute 

	uvicorn main:app --reload --port 8000

9. Open another terminal and change directory to app/frontend/my-angular-app and execute 

	npm start or npm serve --open 

And just open the local host url

10. After performing filtering the files are saved in backend/app/uploads.




	

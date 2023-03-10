# Custom Chatgpt Chatbot


## About  
This is a project developed to create a chatbot based on recently released chatgpt api(March 1st,2023). 
This is a robust chatbot which can accept any website URL and then can answer any questions related to that website.  


### Chatbot High Level
1. User asks a query related to website or any random query
2. Chatbot will look for an answer in following 3 areas according to the order:       
  a. Chat history    
  b. Website pages      
  c. Whole internet(like a general chatgpt)     

### Chatbot Core Logic Steps   
1. Accpet any website URL, scrape all pages within the same domain of that website     
2. Create embeddings of text data of that website     
3. User asks a query      
4. Generate user query embeddings      
4. Look for an answer in chat history using openai's chat completion api     
5. If answer not found,then find most relevant website data embeddings(using cosine similarity).      
  Append this most relvant text to chat history and again use chat completion api to get the answer       
6. If still answer not found(it is most likey a random query) then, chatgpt can answer as it does usually(use whole internet)         


### References
I've used openai's tutorial on <a href="https://github.com/openai/openai-cookbook/blob/main/apps/web-crawl-q-and-a/web-qa.py">website QA</a>  for scraping and combined that with their chatgpt(chat completion) api     


The basic code template for this project is derived from my another repo <a href="https://github.com/sarang0909/Code_Template">code template</a> 


## Project Organization


├── README.md         		<- top-level README for developers using this project.    
├── pyproject.toml         		<- black code formatting configurations.    
├── .gitignore         		<- Files to be ignored in git check in.    
├── .pylintrc         		<- Pylint code linting configurations.    
├── environment.yml 	    <- stores all the dependencies of this project    
├── main.py 	            <- A main file to run chatbot UI.    
├── src                     <- Source code files to be used by project.    
│       ├── chabot_core 	  <- Chatbot request and response related files   
│       ├── data_collection <- website scraping,embeddings creation code   
│       ├── utility	        <- contains utility  and constant modules.   
├── logs                    <- log file path   
├── config                  <- config file path   
├── data                <- datasets files   
├── docs               <- documents from requirement,team collabaroation etc.   




## Installation
Development Environment used to create this project:  
Operating System: Windows 10 Home  

### Softwares
Anaconda:4.8.5  <a href="https://docs.anaconda.com/anaconda/install/windows/">Anaconda installation</a>   
 

### Python libraries:
Go to location of environment.yml file and run:  
```
conda env create -f environment.yml
```
 

## Usage
Here we have created User Interface and used flask for api creation.

1. Go inside 'custom_chatgpt_chatbot' folder on command line.  
   Run:
  ``` 
      conda activate custom_chatgpt_chatbot  
      python main.py       
  ```
  Open 'http://localhost:5000' in a browser.
![alt text](docs/fastapi_first.jpg?raw=true)
![alt text](docs/fastapi_second.jpg?raw=true)
 

### Black- Code formatter
1. Go inside 'custom_chatgpt_chatbot' folder on command line.
2. Run:
  ``` 
      black src 
  ```

### Pylint -  Code Linting
1. Go inside 'custom_chatgpt_chatbot' folder on command line.
2. Run:
  ``` 
      pylint src  
  ```


## Note
1.Please be careful while scraping any website. Make sure you understand legal,security issues with it.    
2.Enter your Openai API key inside config/app_config.json file

## Contributing
Please create a Pull request for any change. 

## License


NOTE: This software depends on other packages that are licensed under different open source licenses.


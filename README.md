## Steps to Run this Proect


Follow the below steps to run this project


### Step 1 : Clone the Repo

```
git clone  https://github.com/heetp0101/Coverage-AI-Agent.git
```

### Step 2 : Create Virtual Environment

Run following command to create virtual environment

```
python -m venv venv
```


### Step 3 : Install all dependencies

```
python -m pip install -r requirements.txt
```

### Step 4 : Run the Project

#### Step 4.1 : Generate the Parsed Output

```
python main.py
```

- This will take `reports.txt` as input and parse the input and give the structured output in a JSON format

#### Step 4.2 : Generate LLM Response

- First we need to filter data from the complete parsed output we got.
- To run this make sure you have  `GEMINI_API_KEY`. You can create a new API KEY from [Google Studio](https://aistudio.google.com/)

  ```
  python ai_agent.py
  ```

#### Step 4.3 : Run the Prioritizer Algorithm

- The Prioritizer Algorithm helps to rank the suggestion based on score that they will predict.

```
python prioritizer.py
```




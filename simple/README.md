
```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python3 default_create_vector_store.py
python3 default_search_vector_store.py

OPENAI_API_KEY="sk-proj-....."; python3 openai_create_vector_store.py
OPENAI_API_KEY="sk-proj-....."; python3 openai_search_vector_store.py
```

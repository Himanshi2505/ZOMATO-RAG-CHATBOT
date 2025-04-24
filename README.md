```markdown
# Zomato RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot to query Zomato restaurant data. It allows users to compare dishes, filter by price or dietary preferences, and get personalized dining insights — all via natural language.

---

Let me walk you through the project. The project consists of five layers:

1. **Data Collection Layer**
   - `info_scraper.py`, `menu_scraper.py`, `review_scraper.py`: Extract restaurant info, menus, and reviews from Zomato using BeautifulSoup and request header rotation.

2. **Data Enhancement Layer**
   - `enhance_menu_data.py`: Classifies items (e.g., vegetarian/non-vegetarian) using keyword heuristics.
   - `build_knowledge_base.py`: Converts raw data into structured JSON documents.

3. **Embedding & Retrieval Layer**
   - `create_embeddings.py`: Embeds documents using `all-MiniLM-L6-v2` (384-dim) and stores vectors in FAISS for fast cosine similarity retrieval.

4. **RAG Model Layer**
   - `rag_chatbot.py`: Retrieves top documents and uses `Flan-T5-base` to generate answers.

5. **UI Layer**
   - `app.py`: Streamlit interface for user interaction.

---

## Setup & Usage Instructions

### 1️. Clone the Repository

```bash
git clone https://github.com/Himanshi2505/ZOMATO-RAG-CHATBOT.git
cd ZOMATO-RAG-CHATBOT
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Scrape Restaurant Data

```bash
python info_scraper.py      # Scrapes restaurant info
python menu_scraper.py      # Scrapes menu items and prices
python review_scraper.py    # Scrapes user reviews
```

---

### 4. Enhance and Structure Data

```bash
python enhance_menu_data.py     # Adds dietary info, cleans data
python build_knowledge_base.py  # Outputs JSON knowledge base
```

---

### 5. Generate Embeddings & FAISS Index

```bash
python create_embeddings.py     # Creates vector store from JSON
```

---

### 6. Start Chatbot Interface

```bash
streamlit run app.py
```

Then open your browser at: [http://localhost:8501](http://localhost:8501)

---

## You can try these Example Questions

- "Which restaurant has best vegetarian menu?"
- "What is the price range for desert at XYZ restaurant?"
- "Show me gluten free items at Matteo?"

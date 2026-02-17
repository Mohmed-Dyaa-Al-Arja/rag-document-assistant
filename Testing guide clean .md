# Complete Testing Guide - RAG System

## Table of Contents

1. [Verification](#verification)
2. [Test Files](#test-files)
3. [Sample Questions](#sample-questions)
4. [Testing Steps](#testing-steps)
5. [Troubleshooting](#troubleshooting)
6. [Research Paper Downloads](#research-downloads)

---

## 1. Verification

### Step 1: Run Verification Script

```bash
cd D:\rag_document_assistant
python verification_test.py
```

Everything should show PASS.



### Step 3: Verify pipeline.py

Open `app/llm/pipeline.py` and ensure it contains:
- `def _format_documents`
- `ChatPromptTemplate`
- `def ask_async`

---

## 2. Test Files

I've prepared 3 test files at different complexity levels:

### File 1: simple_test.md (Quick testing)
- **Size:** Small (~2KB)
- **Content:** Simple project information
- **Use:** Quick test to verify system works

### File 2: test_document_simple.md (Detailed testing)
- **Size:** Medium (~5KB)
- **Content:** Detailed company information (TechVision AI)
- **Use:** Test specific information retrieval (numbers, dates, etc.)

### File 3: research_paper_transformers.md (Complex testing)
- **Size:** Large (~15KB)
- **Content:** Complete research paper on Transformer Architecture
- **Use:** Test ability to understand complex technical content

---

## 3. Sample Questions

### For File 1 (simple_test.md):

#### Basic Questions:
1. "What is this project about?"
   - **Expected:** RAG Document Assistant system

2. "What are the main objectives?"
   - **Expected:** The 5 listed objectives

3. "What technology stack is used?"
   - **Expected:** FastAPI, LangChain, FAISS, Ollama, Gradio

4. "How long is the project timeline?"
   - **Expected:** 10 days

5. "Who is the project lead?"
   - **Expected:** Sarah Johnson

#### Medium Questions:
6. "Explain how the system works step by step"
7. "What is the expected response time?"
8. "What file formats are supported?"

---

### For File 2 (test_document_simple.md):

#### Specific Information Questions:
1. "What is the company name?"
   - **Expected:** TechVision AI Solutions

2. "When was the company founded?"
   - **Expected:** 2020

3. "Who is the CEO?"
   - **Expected:** Dr. Sarah Chen

4. "What is the annual revenue for 2023?"
   - **Expected:** $50 Million

5. "How many employees does the company have?"
   - **Expected:** 250

#### Product Questions:
6. "What products does the company offer?"
7. "What is the price of ChatBot Pro?"
8. "What is the accuracy rate of MediScan AI?"

#### Analytical Questions:
9. "What are the company's short-term plans?"
10. "Compare revenue between 2023 and 2024 projections"
11. "What programming languages does the company use?"

#### Numerical Questions:
12. "What is the customer retention rate?"
13. "How many hospitals use MediScan AI?"
14. "What is the expected growth rate for 2024?"

---

### For File 3 (research_paper_transformers.md):

#### Basic Questions:
1. "What is the main topic of this research paper?"
   - **Expected:** Transformer Architecture and NLP

2. "Who are the authors?"
   - **Expected:** Dr. Michael Zhang, Dr. Lisa Kumar, Prof. James Wilson

3. "What are the research objectives?"
   - **Expected:** The 5 listed objectives

#### Technical Questions:
4. "Explain the self-attention mechanism"
5. "What is the formula for multi-head attention?"
6. "What is the computational complexity of self-attention?"
7. "How many parameters does BERT-Base have?"

#### Results Questions:
8. "What BLEU score did Transformer-Big achieve?"
9. "Compare the performance of LSTM vs Transformer-Base"
10. "What are the limitations of the Transformer architecture?"

#### Applications Questions:
11. "What is GPT-3 and how many parameters does it have?"
12. "What is BERT and what makes it different?"
13. "What are the future research directions mentioned?"

---

## 4. Complete Testing Steps

### Phase 1: Setup

```bash
# 1. Verify fixes are applied
python verification_test.py

# 2. Start Ollama
ollama run llama3.1:8b

# 3. Start Backend (separate terminal)
uvicorn app.main:app --reload

# 4. Start UI (separate terminal)
python ui\gradio_app.py
```

### Phase 2: Test Simple File

1. Open browser at `http://localhost:7860`
2. Go to "Upload Document" tab
3. Upload `simple_test.md` (or save as .txt first)
4. Click "Process Document"
5. Should see: "Document processed successfully. Total Chunks: X"

6. Go to "Chat" tab
7. Ask: "What is this project about?"
8. Wait for answer (5-10 seconds)

**Expected Result:**
- Clear answer mentioning "RAG Document Assistant"
- Sources appear below the answer
- Page number is mentioned

### Phase 3: Multiple Questions Test

Ask in sequence:
1. "What are the objectives?"
2. "What technology is used?"
3. "How does it work?"
4. "Who is the team?"

Verify:
- Each answer is accurate
- Sources change based on question
- Answers are based on document content

### Phase 4: Memory Test

Ask:
1. "What is the project timeline?"
2. "Tell me more about day 7" (should remember context from previous question)

### Phase 5: Clear Chat Test

1. Click "Clear Chat"
2. Ask the same previous question
3. Verify memory was cleared

---

## 5. Troubleshooting

### Issue: "Retrieved docs count: 0"

**Solution:**
```python
SCORE_THRESHOLD: float = 5.0  
```

### Issue: "The document does not contain sufficient information"

**Cause:** LLM is not using the context

**Solution:**
1. Ensure `pipeline.py` is in place
2. Restart the server
3. Upload document again

### Issue: Ollama not responding

```bash
# Restart Ollama
ollama stop
ollama run llama3.1:8b
```


## 6. Research Paper Downloads

### Websites to Download Research PDFs:

#### 1. arXiv.org (Free)
**Link:** https://arxiv.org

**Recommended Papers for Testing:**

1. **Attention Is All You Need** (Original Transformers)
   - https://arxiv.org/abs/1706.03762
   - 15 pages, easy to test

2. **BERT Paper**
   - https://arxiv.org/abs/1810.04805
   - 16 pages, clear information

3. **GPT-3 Paper**
   - https://arxiv.org/abs/2005.14165
   - 75 pages, test for long documents

4. **Vision Transformer (ViT)**
   - https://arxiv.org/abs/2010.11929
   - About Transformers in Computer Vision

#### 2. Papers With Code
**Link:** https://paperswithcode.com

- Search for any topic (NLP, Computer Vision, etc.)
- Click on Paper
- Download the PDF

#### 3. Google Scholar
**Link:** https://scholar.google.com

- Search for topic
- Download papers marked with [PDF]

#### 4. Semantic Scholar
**Link:** https://www.semanticscholar.org

- Scientific papers with summaries
- Most are available for download

---

## Testing Best Practices

### 1. Start Simple
- Use `simple_test.md` first
- Verify basic system works
- Then move to larger files

### 2. Test Different Question Types
- Direct questions ("What is X?")
- Analytical questions ("Compare X and Y")
- Numerical questions ("How many X?")
- Follow-up questions ("Tell me more about...")

### 3. Monitor the Console
```bash
Score: 0.85
Threshold: 3.0
Retrieved docs count: 3  
```

### 4. Verify Sources
- Should appear below each answer
- Should be relevant to the question
- Page number should be correct

### 5. Test Boundaries
- Ask questions not in the document
- System should say "I cannot find..."
- Should not make up information

---

## Success Checklist

Before declaring the system works 100%:

- [ ] verification_test.py all PASS
- [ ] Upload document shows "Total Chunks: X"
- [ ] Ask simple question and get correct answer
- [ ] Sources appear below answer
- [ ] Console shows "Retrieved docs count: X" (X > 0)
- [ ] Try 5 different questions, all respond correctly
- [ ] Clear Chat works
- [ ] Follow-up question remembers context

---

## Additional Help

If you've tried everything and still have issues:

1. **Share:**
   - Complete console output
   - The question you asked
   - The answer you received
   - Name of file you uploaded

2. **Verify:**
   - Ollama is running: `ollama list`
   - Port 8000 is free: `netstat -an | findstr 8000`
   - Port 7860 is free: `netstat -an | findstr 7860`


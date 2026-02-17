"""
Quick verification test to ensure fixes are applied correctly
"""

print("=" * 60)
print("VERIFICATION TEST - Smart Contract RAG System")
print("=" * 60)

# Test 1: Check if retriever file is fixed
print("\n[Test 1] Checking retriever.py indentation...")
try:
    with open("app/retrieval/retriever.py", "r", encoding="utf-8") as f:
        content = f.read()
        # Check if the if statement is indented properly (inside the loop)
        if "    for doc, score in results:" in content and "            if score <=" in content:
            print("PASS - retriever.py: Fixed (indentation correct)")
        elif "    for doc, score in results:" in content and "        if score <=" in content:
            print("PASS - retriever.py: Fixed (indentation correct - alternative spacing)")
        else:
            print("FAIL - retriever.py: NOT FIXED - if statement is outside the loop!")
            print("   Please replace with retriever_fixed.py")
except FileNotFoundError:
    print("FAIL - File not found: app/retrieval/retriever.py")

# Test 2: Check if pipeline.py exists
print("\n[Test 2] Checking pipeline.py...")
try:
    with open("app/llm/pipeline.py", "r", encoding="utf-8") as f:
        content = f.read()
        if "def _format_documents" in content and "ChatPromptTemplate" in content:
            print("PASS - pipeline.py: EXISTS and looks correct")
        else:
            print("WARN - pipeline.py: EXISTS but might be incomplete")
except FileNotFoundError:
    print("FAIL - File not found: app/llm/pipeline.py")
    print("   Please copy pipeline.py to app/llm/")

# Test 3: Check config
print("\n[Test 3] Checking config.py...")
try:
    from app.config import settings
    print(f"PASS - Config loaded successfully")
    print(f"   - SCORE_THRESHOLD: {settings.SCORE_THRESHOLD}")
    print(f"   - TOP_K: {settings.TOP_K}")
    print(f"   - CHUNK_SIZE: {settings.CHUNK_SIZE}")
    
    if settings.SCORE_THRESHOLD >= 3.0:
        print("   PASS - Threshold is good for FAISS")
    else:
        print("   WARN - Threshold might be too low - try 3.0 or higher")
except Exception as e:
    print(f"FAIL - Error loading config: {e}")

# Test 4: Check if __init__.py exists in llm folder
print("\n[Test 4] Checking llm module...")
import os
if os.path.exists("app/llm/__init__.py"):
    print("PASS - app/llm/__init__.py: EXISTS")
else:
    print("FAIL - app/llm/__init__.py: MISSING")
    print("   Please create an empty __init__.py file in app/llm/")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
print("\nNext steps:")
print("1. If everything is PASS, restart the server")
print("2. If there are FAIL items, apply the required fixes")
print("3. Then upload a document and ask questions")

# verification_test.py

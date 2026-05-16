# CV Analyzer Pro

> A desktop application that automates resume screening using classical string-matching algorithms — compare Brute Force, Rabin-Karp, and KMP in real time across single CVs or batch processing 700+ resumes.

Built with **Python** and **PyQt5** for a university Algorithms course.

---

## What It Does

CV Analyzer Pro takes a resume (PDF, DOCX, or TXT), matches it against a job description's required and optional skills using your chosen string-matching algorithm, and gives you a scored result with detailed analytics. You can also batch-process hundreds of CVs at once and get a ranked leaderboard.

**Supported Job Roles:** Data Scientist · AI/ML Engineer · Computer Scientist · Data Analyst

**Algorithms:** Brute Force · Rabin-Karp · KMP (Knuth-Morris-Pratt)

---

### Single CV — Keywords Tab
Shows each keyword as FOUND or MISSING with mandatory/optional tagging.


### Single CV — Analytics Tab
Side-by-side bar charts comparing execution time (ms) and character comparisons across all three algorithms.



---

### Batch — Results Tab (Brute Force)
Aggregate stats: total candidates, average scores, candidate distribution, and top 5 ranked CVs.



### Batch — Results Tab (Rabin-Karp)
Same summary view run with the Rabin-Karp algorithm.



### Batch — Keywords Tab
Corpus-wide skill frequency across all 735 CVs (e.g. Python: 714/735 = 97%).



### Batch — Analytics Tab
Performance comparison table + execution time and comparison bar charts across all three algorithms.


## System Flowchart

The system follows a structured validation flow:
1. Load a job description
2. Choose an algorithm (Brute Force / Rabin-Karp / KMP)
3. Choose a mode — Single CV Analysis or Batch CV Analysis
4. Results populate across 5 tabs: Results, Keywords, Analytics, Details, Ranking

---

## Algorithm Performance (735 CVs — Data Scientist Role)

| Algorithm | Total Time (ms) | Avg Time/CV (ms) | Avg Comparisons/CV | Throughput (CVs/sec) |
|-----------|----------------|-------------------|--------------------|----------------------|
| Brute Force | 32,025 | 43.57 | 65,362 | 23.0 |
| Rabin-Karp | 79,215 | 106.44 | 755 | 9.3 |
| **KMP** | **21,212** | **28.88** | **62,750** | **34.6** |

**Winner: KMP** — fastest execution, highest throughput, guaranteed O(n+m) complexity.

---

## Scoring Formula

```
Overall Score = (Mandatory Score × 0.80) + (Optional Score × 0.20)
```

| Status | Threshold | Label |
|--------|-----------|-------|
| Excellent | ≥ 80% | ★ EXCELLENT |
| Good | 60–79% | GOOD |
| Fair | 40–59% | FAIR |
| Poor | < 40% | POOR |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.8+ |
| GUI | PyQt5 5.15+ |
| Charts | QtCharts |
| PDF parsing | PyPDF2 |
| DOCX parsing | python-docx |
| OS | Windows 10/11 (cross-platform) |

---


## How to Run

```bash
# Install dependencies
pip install PyQt5 PyPDF2 python-docx

# Run the app
python src/main.py
```

Place CVs you want to batch-analyze in a `data/cvs/` folder in the project root.

---


## Limitations

- Exact keyword matching only — no synonym support (e.g. "ML" ≠ "Machine Learning")
- No semantic understanding of context
- English-only keyword matching
- Fixed 80/20 scoring weights

---

## Submitted By

**Wajeeha Khalid** · Student ID: 23i-2610
FAST National University of Computer and Emerging Sciences  


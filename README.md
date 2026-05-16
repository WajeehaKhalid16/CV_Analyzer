# CV Analyzer Pro

> A desktop application that automates resume screening using classical string-matching algorithms — compare Brute Force, Rabin-Karp, and KMP in real time across single CVs or batch processing 700+ resumes.

Built with **Python** and **PyQt5** for a university Algorithms course.

---

## What It Does

CV Analyzer Pro takes a resume (PDF, DOCX, or TXT), matches it against a job description's required and optional skills using your chosen string-matching algorithm, and gives you a scored result with detailed analytics. You can also batch-process hundreds of CVs at once and get a ranked leaderboard.

**Supported Job Roles:** Data Scientist · AI/ML Engineer · Computer Scientist · Data Analyst

**Algorithms:** Brute Force · Rabin-Karp · KMP (Knuth-Morris-Pratt)

---

## Screenshots

### Dashboard
![Dashboard](screenshots/DASHBOARD.png)

### Selecting a Job Role
![Select Job](screenshots/S01_SELECT_JOB_.png)

### Job Loaded Successfully
![Job Loaded](screenshots/S01_DIALOG_SHOWING_SUCCESS_.png)

### Selecting an Algorithm
![Algorithm Options](screenshots/OPTIONS_FOR_SELECTING_ALGOS_.png)

### Warning: Load Job Before Analyzing
![Warning Load Job](screenshots/WARNING_DIALOG_ASKING_FOR_LOAD_JOB_B4_ANALYZING_CVs_001.png)

### Warning: Select CV for Single Analysis
![Warning CV](screenshots/DIALOG_ASKING_TO_ENTER_CV_FOR_SINGLE_ANALYSIS.png)

### Batch Processing in Progress (21%)
![Batch Processing](screenshots/s1.png)

---

### Single CV — Keywords Tab
Shows each keyword as FOUND or MISSING with mandatory/optional tagging.

![Keywords Single](screenshots/KEYWORDS_TAB_FOR_SINGLE_CV_ANALYSIS_.png)

### Single CV — Analytics Tab
Side-by-side bar charts comparing execution time (ms) and character comparisons across all three algorithms.

![Analytics Single](screenshots/ANALYTICS_TAB_SINGLE_.png)

---

### Batch — Results Tab (Brute Force)
Aggregate stats: total candidates, average scores, candidate distribution, and top 5 ranked CVs.

![Batch Results BF](screenshots/BF_RESULTS_TAB_BATCH_.png)

### Batch — Results Tab (Rabin-Karp)
Same summary view run with the Rabin-Karp algorithm.

![Batch Results RK](screenshots/RK_RESULTS_TAB_BATCH_.png)

### Batch — Keywords Tab
Corpus-wide skill frequency across all 735 CVs (e.g. Python: 714/735 = 97%).

![Keywords Batch](screenshots/RK_KEYWORDS_TAB_BATCH.png)

### Batch — Analytics Tab
Performance comparison table + execution time and comparison bar charts across all three algorithms.

![Analytics Batch](screenshots/ANALYTICS_TAB_BATCH_SHOWING_OVERALL_RESULTS_.png)

---

### Candidate Ranking — Top (Excellent)
![Ranking Top](screenshots/OVERALL_RANKING_.png)

### Candidate Ranking — Good Tier (Around Rank 100)
![Ranking Good](screenshots/OVERALLRANKING_6.png)

### Candidate Ranking — Fair Tier (Around Rank 468)
![Ranking Fair](screenshots/OVERALLL_RANKING_7_.png)

### Candidate Ranking — Poor Tier (Bottom)
![Ranking Poor](screenshots/OVERALL_RANKING_8_.png)

### Candidate Ranking — Bottom of List (Rank 735)
![Ranking Bottom](screenshots/OVERALL_RANKING_5.png)

---

## System Flowchart

![Flowchart](assets/FLOWCHART-Page-1.jpg)

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

## Project Structure

```
CV_Analyzer/
├── src/
│   ├── main.py              # Entry point
│   ├── main_window.py       # GUI controller (CVAnalyzerGUI)
│   ├── analyzer.py          # Core analysis engine
│   ├── brute_force.py       # Brute Force implementation
│   ├── rabin_karp.py        # Rabin-Karp implementation
│   └── kmp.py               # KMP implementation
│   └── file_reader.py       # PDF/DOCX/TXT parser
├── job_descriptions/
│   ├── data_scientist.txt
│   ├── ai_ml_engineer.txt
│   ├── computer_scientist.txt
│   └── data_analyst.txt
├── assets/
│   └── FLOWCHART-Page-1.jpg
├── screenshots/
│   └── *.png
└── README.md
```

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

## Key Findings

- **KMP is the best choice for production** — 3.7× faster than Rabin-Karp and 1.5× faster than Brute Force on 735 CVs
- **Rabin-Karp paradox** — fewest character comparisons (755 avg) but slowest runtime due to hashing overhead
- **Brute Force** remains a solid baseline for small datasets and validation
- All three algorithms produced identical keyword match results (100% accuracy)
- Out of 735 CVs screened for Data Scientist: 82 Excellent (11.2%), 245 Good (33.3%), 217 Fair (29.5%), 191 Poor (26%)

---

## Limitations

- Exact keyword matching only — no synonym support (e.g. "ML" ≠ "Machine Learning")
- No semantic understanding of context
- English-only keyword matching
- Fixed 80/20 scoring weights

---

## Submitted By

**Wajeeha Khalid** · Student ID: 23i-2610 · Section: BDS-5A  
FAST National University of Computer and Emerging Sciences  
Course: Algorithms



import sys
import time

sys.path.append('..')

from algorithms.brute_force import BruteForce
from algorithms.rabin_karp import RabinKarp
from algorithms.kmp import KMP


def test_algorithm(algo, text, pattern, case_sensitive=False):
   
    start_time = time.perf_counter()
    matches = algo.search(text, pattern, case_sensitive)
    end_time = time.perf_counter()
    
    execution_time = (end_time - start_time) * 1000  
    comparisons = algo.get_comparisons()
    
    return {
        'name': algo.name,
        'matches': matches,
        'comparisons': comparisons,
        'time': execution_time
    }


def print_results(results, text_length, pattern_length):
  
    print("\n" + "="*80)
    print("ALGORITHM COMPARISON RESULTS")
    print("="*80)
    print(f"Text length: {text_length} characters")
    print(f"Pattern length: {pattern_length} characters")
    print("-"*80)
    
    for result in results:
        print(f"\n{result['name']}:")
        print(f"  Matches found: {len(result['matches'])} at positions {result['matches']}")
        print(f"  Character comparisons: {result['comparisons']:,}")
        print(f"  Execution time: {result['time']:.4f} ms")
        
      
        optimal = text_length 
        actual = result['comparisons']
        if actual <= optimal:
            efficiency = 100.0
        else:
            excess_ratio = (actual - optimal) / optimal
            efficiency = max(0, 100 - (excess_ratio * 50))
        print(f"  Efficiency: {efficiency:.1f}%")
    
    print("\n" + "="*80)
    print("RANKING (by comparisons - lower is better):")
    print("="*80)
    sorted_results = sorted(results, key=lambda x: x['comparisons'])
    for i, result in enumerate(sorted_results, 1):
        medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else "  "
        print(f"{medal} #{i}: {result['name']} - {result['comparisons']:,} comparisons")
    
    print("\n" + "="*80)
    print("EXPECTED: KMP < Rabin-Karp < Brute Force")
    print("="*80 + "\n")


def test_small_text():
    """Test 1: Small text with clear pattern"""
    print("\n" + " TEST 1: Small Text Analysis")
    
    text = "Python programming is fun. Python is versatile. Learn Python today!"
    pattern = "Python"
    
    bf = BruteForce()
    rk = RabinKarp()
    kmp = KMP()
    
    results = [
        test_algorithm(bf, text, pattern, case_sensitive=False),
        test_algorithm(rk, text, pattern, case_sensitive=False),
        test_algorithm(kmp, text, pattern, case_sensitive=False)
    ]
    
    print_results(results, len(text), len(pattern))


def test_cv_simulation():
    """Test 2: Simulated CV text"""
    print("\n" + " TEST 2: CV Simulation")
    
    cv_text = """
    John Doe
    Software Engineer
    
    SKILLS:
    - Python programming (5 years)
    - Machine Learning and Data Science
    - SQL and Database Management
    - JavaScript and React
    - Docker and Kubernetes
    
    EXPERIENCE:
    Software Engineer at Tech Corp (2020-2023)
    - Developed Python applications for data analysis
    - Built machine learning models using Python and TensorFlow
    - Optimized SQL queries for better performance
    
    EDUCATION:
    BS Computer Science, University XYZ
    
    PROJECTS:
    - Python-based web scraper
    - Machine learning classification system
    - SQL database optimization toolkit
    """
    
    keywords = ["Python", "SQL", "Machine Learning", "JavaScript", "Docker"]
    
    print(f"\nSearching for {len(keywords)} keywords in CV...")
    print(f"Keywords: {keywords}")
    
    bf = BruteForce()
    rk = RabinKarp()
    kmp = KMP()
    
   
    bf_results = bf.search_multiple(cv_text, keywords, case_sensitive=False)
    rk_results = rk.search_multiple(cv_text, keywords, case_sensitive=False)
    kmp_results = kmp.search_multiple(cv_text, keywords, case_sensitive=False)
    
    results = [
        {
            'name': 'Brute Force',
            'matches': sum(len(matches) for matches in bf_results.values()),
            'comparisons': bf.get_comparisons(),
            'time': 0  # Not measured for simplicity
        },
        {
            'name': 'Rabin-Karp',
            'matches': sum(len(matches) for matches in rk_results.values()),
            'comparisons': rk.get_comparisons(),
            'time': 0
        },
        {
            'name': 'KMP',
            'matches': sum(len(matches) for matches in kmp_results.values()),
            'comparisons': kmp.get_comparisons(),
            'time': 0
        }
    ]
    
    print("\n" + "="*80)
    print("MULTI-PATTERN SEARCH RESULTS")
    print("="*80)
    print(f"CV text length: {len(cv_text)} characters")
    print(f"Keywords searched: {len(keywords)}")
    print("-"*80)
    
    for result in results:
        print(f"\n{result['name']}:")
        print(f"  Total matches: {result['matches']}")
        print(f"  Character comparisons: {result['comparisons']:,}")
        
       
        optimal = len(cv_text) * len(keywords)  
        actual = result['comparisons']
        if actual <= optimal:
            efficiency = 100.0
        else:
            excess_ratio = (actual - optimal) / optimal
            efficiency = max(0, 100 - (excess_ratio * 30))
        print(f"  Efficiency: {efficiency:.1f}%")
    
    print("\n" + "="*80)


def test_worst_case():
    """Test 3: Worst case scenario"""
    print("\n" + "  TEST 3: Worst Case Scenario")
    print("(Pattern: 'AAAA', Text: 'AAAAAAAAAA...')")
    
    text = "A" * 100  
    pattern = "AAAA"
    
    bf = BruteForce()
    rk = RabinKarp()
    kmp = KMP()
    
    results = [
        test_algorithm(bf, text, pattern, case_sensitive=True),
        test_algorithm(rk, text, pattern, case_sensitive=True),
        test_algorithm(kmp, text, pattern, case_sensitive=True)
    ]
    
    print_results(results, len(text), len(pattern))


def test_no_match():
    """Test 4: No matches found"""
    print("\n" + " TEST 4: No Matches Scenario")
    
    text = "Python JavaScript Java Ruby Go"
    pattern = "Rust"
    
    bf = BruteForce()
    rk = RabinKarp()
    kmp = KMP()
    
    results = [
        test_algorithm(bf, text, pattern, case_sensitive=False),
        test_algorithm(rk, text, pattern, case_sensitive=False),
        test_algorithm(kmp, text, pattern, case_sensitive=False)
    ]
    
    print_results(results, len(text), len(pattern))


def main():
    """Run all tests"""
    print("\n" + " STRING MATCHING ALGORITHM TEST SUITE")
    print("="*80)
    print("Testing: Brute Force vs Rabin-Karp vs KMP")
    print("="*80)
    
    test_small_text()
    test_cv_simulation()
    test_worst_case()
    test_no_match()
    
    print("\n" + " ALL TESTS COMPLETED!")
    print("\nKEY INSIGHTS:")
    print("• Brute Force: Most comparisons, simplest implementation")
    print("• Rabin-Karp: Fewer comparisons due to hash filtering")
    print("• KMP: Fewest comparisons, optimal for long patterns")
    print("• All should find the same matches!")
    print()


if __name__ == "__main__":
    main()
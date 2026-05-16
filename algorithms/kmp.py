"""
Knuth-Morris-Pratt (KMP) Algorithm
Follows the pseudocode from slides
Running Time: O(n) - linear with text length
"""

class KMP:
   
    
    def __init__(self):
        self.comparisons = 0
        self.name = "KMP"
    
    def compute_lps(self, pattern):
        """
        Compute-Prefix-Function (p) from slides
        Time Complexity: O(m) where m = pattern length
        
        This is preprocessing
        """
        m = len(pattern)
        lps = [0] * m
        
        if m == 0:
            return lps
        
        lps[0] = 0  # Line 2: Π[1] ← 0
        k = 0       # Line 3: k ← 0
        
        # Line 4: for q ← 2 to m
        for q in range(1, m):  # Python uses 0-indexing
            # Line 5-6: while k > 0 and p[k+1] ≠ p[q]
            while k > 0 and pattern[k] != pattern[q]:
                k = lps[k - 1]  # Line 6: k ← Π[k]
            
            # Line 7-8: if p[k+1] = p[q] then k ← k+1
            if pattern[k] == pattern[q]:
                k += 1
            
            # Line 9: Π[q] ← k
            lps[q] = k
        
        return lps
    
    def search(self, text, pattern, case_sensitive=False):
        """
        KMP-Matcher with  comparison counting
        
         Only counts actual character comparisons, accumulates properly
        """
        matches = []
        
        if not case_sensitive:
            text = text.lower()
            pattern = pattern.lower()
        
        n = len(text)
        m = len(pattern)
        
        if m == 0:
            return matches
        
        lps = self.compute_lps(pattern)
        q = 0
        comparisons_this_search = 0  # Local counter
        
        # Scan text from left to right
        for i in range(n):
            
            while q > 0 and pattern[q] != text[i]:
                q = lps[q - 1]
            
            
            comparisons_this_search += 1
            
            if pattern[q] == text[i]:
                q += 1
            
            
            if q == m:
                matches.append(i - m + 1)
                q = lps[q - 1]
        
        self.comparisons += comparisons_this_search 
        return matches

    def search_multiple(self, text, patterns, case_sensitive=False):
        """
        Search multiple patterns and accumulate comparisons
        
        """
        results = {}
        self.comparisons = 0 
        
        for pattern in patterns:
            matches = self.search(text, pattern, case_sensitive)
            results[pattern] = matches
            
        
        return results
        
    def get_comparisons(self):
        """Return total character comparisons made"""
        return self.comparisons




if __name__ == "__main__":
    print("="*70)
    print("KMP ALGORITHM")
    print("="*70)
    
    kmp = KMP()
    
   
    print("\n TEST 1: Example from slides")
    print("-"*70)
    text1 = "bacbababababacaab"
    pattern1 = "ababaca"
    
    
    lps1 = kmp.compute_lps(pattern1)
    print(f"Pattern: {pattern1}")
    print(f"LPS array: {lps1}")
    print(f"Expected LPS: [0, 0, 1, 2, 3, 0, 1] ")
    
    matches1 = kmp.search(text1, pattern1, case_sensitive=True)
    print(f"\nText: {text1}")
    print(f"Matches at positions: {matches1}")
    print(f"Comparisons: {kmp.get_comparisons()}")
    print(f"Text length: {len(text1)}")
    print(f"Expected: ~{len(text1)} comparisons (O(n) = linear)")
    
   
    print("\n TEST 2: CV Keyword Search")
    print("-"*70)
    text2 = "Python is great. Python is easy. Python everywhere."
    pattern2 = "Python"
    
    matches2 = kmp.search(text2, pattern2, case_sensitive=False)
    print(f"Text: {text2}")
    print(f"Pattern: '{pattern2}'")
    print(f"Matches: {matches2}")
    print(f"Comparisons: {kmp.get_comparisons()}")
    print(f"Text length: {len(text2)}")
    print(f"Expected: ~{len(text2)} comparisons")
    
    
    print("\n TEST 3: Multiple Keywords")
    print("-"*70)
    cv_text = "Python Java Machine Learning SQL Data Analysis" * 20  
    keywords = ["Python", "Java", "SQL", "Machine Learning"]
    
    results = kmp.search_multiple(cv_text, keywords, case_sensitive=False)
    
    print(f"CV text length: {len(cv_text)} characters")
    print(f"Keywords searched: {len(keywords)}")
    print(f"\nResults:")
    for kw, positions in results.items():
        print(f"  '{kw}': {len(positions)} occurrences")
    
    print(f"\nTotal comparisons: {kmp.get_comparisons():,}")
    print(f"Expected: ~{len(cv_text) * len(keywords):,} (n * k)")
    print(f"Average per keyword: {kmp.get_comparisons() / len(keywords):.0f}")
    
    # Test 4: Verify O(n) complexity
    print("\n TEST 4: Complexity Verification")
    print("-"*70)

    for size in [100, 500, 1000, 5000]:
        test_text = "a" * size
        test_pattern = "aaa"
        kmp2 = KMP()
        kmp2.search(test_text, test_pattern)
        ratio = kmp2.get_comparisons() / size
        print(f"Text size: {size:5d} | Comparisons: {kmp2.get_comparisons():5d} | Ratio: {ratio:.2f}")
    
    print("\n If ratio ≈ 1.0, KMP is O(n)")
    print("="*70)

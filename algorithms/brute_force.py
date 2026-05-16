"""
Brute Force Algorithm for Pattern Matching
Simple character-by-character comparison

Time Complexity: O(n * m)
- n = length of text
- m = length of pattern
- Worst case: Every position requires full pattern comparison

Space Complexity: O(1)
"""

class BruteForce:
   
    
    def __init__(self):
        
        self.comparisons = 0
        self.name = "Brute Force"
    
    def search(self, text, pattern, case_sensitive=False):
        """
        Search for pattern in text using brute force
        
        """
        matches = []
        
        
        if not case_sensitive:
            text = text.lower()
            pattern = pattern.lower()
        
        n = len(text)
        m = len(pattern)
        
        
        if m == 0:
            return matches
        
        comparisons_this_search = 0  
        
       
        for i in range(n - m + 1):
           
            j = 0
            while j < m:
                comparisons_this_search += 1  
                
                if text[i + j] != pattern[j]:
                    break  
                j += 1
            
            
            if j == m:
                matches.append(i)
        
        self.comparisons += comparisons_this_search  
        return matches

    def search_multiple(self, text, patterns, case_sensitive=False):
        """
        Search for multiple patterns in text
        
        
        """
        results = {}
        self.comparisons = 0  
        
        for pattern in patterns:
            matches = self.search(text, pattern, case_sensitive)
            results[pattern] = matches
           
        
        return results
    
    def get_comparisons(self):
        """
        Get number of character comparisons made
      
        """
        return self.comparisons


if __name__ == "__main__":
    print("=" * 70)
    print("BRUTE FORCE ALGORITHM - CORRECTED VERSION TEST")
    print("=" * 70)
    
    bf = BruteForce()
    
    # Test 1: Simple match
    print("\n TEST 1: Simple Pattern Match")
    print("-" * 70)
    text1 = "ABCABCD"
    pattern1 = "ABC"
    
    matches1 = bf.search(text1, pattern1, case_sensitive=True)
    print(f"Text:    {text1}")
    print(f"Pattern: {pattern1}")
    print(f" Found at positions: {matches1}")
    print(f"   Comparisons: {bf.get_comparisons()}")
    print(f"   Expected comparisons: ~{len(text1)} (varies with mismatches)")
    
    # Test 2: No match
    print("\n TEST 2: No Match Case")
    print("-" * 70)
    text2 = "AAAAA"
    pattern2 = "B"
    
    matches2 = bf.search(text2, pattern2, case_sensitive=True)
    print(f"Text:    {text2}")
    print(f"Pattern: {pattern2}")
    print(f" Found at positions: {matches2}")
    print(f"   Comparisons: {bf.get_comparisons()}")
    print(f"   Expected: {len(text2)} (one comparison per position)")
    
    print("\n TEST 3: Overlapping Matches")
    print("-" * 70)
    text3 = "AAAA"
    pattern3 = "AA"
    
    matches3 = bf.search(text3, pattern3, case_sensitive=True)
    print(f"Text:    {text3}")
    print(f"Pattern: {pattern3}")
    print(f" Found at positions: {matches3}")
    print(f"   Comparisons: {bf.get_comparisons()}")
    print(f"   Expected: {(len(text3) - len(pattern3) + 1) * len(pattern3)}")
    print(f"   (Each position requires m={len(pattern3)} comparisons)")
    

    print("\n TEST 4: CV Keyword Search")
    print("-" * 70)
    cv_text = "Python is great. Python is easy. Python everywhere."
    keyword = "Python"
    
    matches4 = bf.search(cv_text, keyword, case_sensitive=False)
    print(f"CV Text: {cv_text}")
    print(f"Keyword: '{keyword}'")
    print(f" Found at positions: {matches4}")
    print(f"   Comparisons: {bf.get_comparisons()}")
    print(f"   Text length: {len(cv_text)}")
    print(f"   Pattern length: {len(keyword)}")
    print(f"   Worst case: {len(cv_text) * len(keyword)}")
    
   
    print("\n TEST 5: Multiple Keywords")
    print("-" * 70)
    cv_text5 = "Skills: Python, Java, SQL, Machine Learning"
    keywords = ["Python", "Java", "SQL", "C++"]
    
    results = bf.search_multiple(cv_text5, keywords, case_sensitive=False)
    
    print(f"CV Text: {cv_text5}")
    print(f"Keywords: {keywords}")
    print(f"\n Results:")
    for kw, pos in results.items():
        status = "Found" if pos else " Not Found"
        print(f"   {status}: '{kw}' at {pos}")
    
    print(f"\n   Total Comparisons: {bf.get_comparisons():,}")
    print(f"   Text length: {len(cv_text5)}")
    print(f"   Patterns: {len(keywords)}")
    
  
    print("\n TEST 6: Complexity Verification (O(n*m))")
    print("-" * 70)
    
    test_pattern = "ABC"
    m = len(test_pattern)
    
    for n in [100, 200, 400, 800]:
        test_text = "A" * n 
        bf_test = BruteForce()
        bf_test.search(test_text, test_pattern)
        comparisons = bf_test.get_comparisons()
        expected = n * m
        ratio = comparisons / expected
        print(f"n={n:4d}, m={m} | Comparisons: {comparisons:5d} | Expected: {expected:5d} | Ratio: {ratio:.3f}")
    
    print("\n If ratio ≈ 1.0, algorithm is O(n*m) as expected!")
    print("=" * 70)

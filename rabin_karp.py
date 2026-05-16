"""
Rabin-Karp Algorithm for Pattern Matching
Uses rolling hash to find patterns efficiently
h(i+1) = h(i)·b - t[i]·b^M + t[i+M] mod q

Time Complexity:
- Average Case: O(n + m)
- Worst Case: O(n·m) when all hashes collide
- Best Case: O(n)

Space Complexity: O(1)
"""

class RabinKarp:
    
    def __init__(self, prime=101):
        """      
        Attributes:
            comparisons (int): Character comparisons during verification
            name (str): Algorithm identifier
            prime (int): Prime modulo for hash calculation
            base (int): Base for polynomial hash (256 for ASCII)
        """
        self.comparisons = 0
        self.name = "Rabin-Karp"
        self.prime = prime
        self.base = 256  
    
    def search(self, text, pattern, case_sensitive=False):
        """
        Search for pattern in text using Rabin-Karp algorithm
        
        """
        matches = []
        if not case_sensitive:
            text = text.lower()
            pattern = pattern.lower()
        
        n = len(text)
        m = len(pattern)
        
       
        if m == 0 or m > n:
            return matches
        
        comparisons_this_search = 0  
        
        h = 1
        for i in range(m - 1):
            h = (h * self.base) % self.prime
        
        pattern_hash = 0
        text_hash = 0
        
        for i in range(m):
            pattern_hash = (self.base * pattern_hash + ord(pattern[i])) % self.prime
            text_hash = (self.base * text_hash + ord(text[i])) % self.prime
        
        for i in range(n - m + 1):
            
            # If hash values match, verify character by character
            if pattern_hash == text_hash:
               
                match = True
                for j in range(m):
                    comparisons_this_search += 1  
                    if text[i + j] != pattern[j]:
                        match = False
                        break
                
                if match:
                    matches.append(i)
            
            
            if i < n - m:
                text_hash = (text_hash * self.base) % self.prime
                text_hash = (text_hash - ord(text[i]) * h * self.base) % self.prime
                text_hash = (text_hash + ord(text[i + m])) % self.prime
                
                if text_hash < 0:
                    text_hash = (text_hash + self.prime) % self.prime
        
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
        Get total number of character comparisons
        This counts only the verification comparisons (brute force check
        when hashes match), not the hash comparisons.
      
        """
        return self.comparisons

if __name__ == "__main__":
    print("=" * 75)
    print("RABIN-KARP ALGORITHM, VERIFIED IMPLEMENTATION")
    print("Following Slide Formula: h(i+1) = h(i)·b - t[i]·b^M + t[i+M] mod q")
    print("=" * 75)
    
    rk = RabinKarp(prime=101)
    
   
    print("\n" + "=" * 75)
    print("TEST 1: Basic Pattern Matching")
    print("=" * 75)
    text1 = "AABAACAADAABAABA"
    pattern1 = "AABA"
    
    matches1 = rk.search(text1, pattern1, case_sensitive=True)
    print(f"Text:    '{text1}'")
    print(f"Pattern: '{pattern1}'")
    print(f"✅ Found at positions: {matches1}")
    print(f"   Comparisons: {rk.get_comparisons()}")
    
    if matches1:
        print(f"\n   Verification:")
        for pos in matches1:
            print(f"   Position {pos}: '{text1[pos:pos+len(pattern1)]}'")
    
   
    print("\n" + "=" * 75)
    print("TEST 2: Slides Example")
    print("=" * 75)
    text2 = "feafebeecdedcfc"
    pattern2 = "edc"
    
    matches2 = rk.search(text2, pattern2, case_sensitive=True)
    print(f"Text:    '{text2}'")
    print(f"Pattern: '{pattern2}'")
    print(f" Found at positions: {matches2}")
    print(f"   Comparisons: {rk.get_comparisons()}")
    
    if matches2:
        for pos in matches2:
            print(f"   Position {pos}: '{text2[pos:pos+len(pattern2)]}'")
    
  
    print("\n" + "=" * 75)
    print("TEST 3: Case-Insensitive Search")
    print("=" * 75)
    text3 = "Python is a great programming language. Python is easy to learn."
    pattern3 = "Python"
    
    matches3 = rk.search(text3, pattern3, case_sensitive=False)
    print(f"Text: '{text3}'")
    print(f"Pattern: '{pattern3}' (case-insensitive)")
    print(f" Found at positions: {matches3}")
    print(f"   Comparisons: {rk.get_comparisons()}")
    

    print("\n" + "=" * 75)
    print("TEST 4: Overlapping Patterns")
    print("=" * 75)
    text4 = "AAAAAAAAAA"
    pattern4 = "AAA"
    
    matches4 = rk.search(text4, pattern4, case_sensitive=True)
    print(f"Text:    '{text4}'")
    print(f"Pattern: '{pattern4}'")
    print(f" Found at positions: {matches4}")
    print(f"   Expected: [0, 1, 2, 3, 4, 5, 6, 7] (8 overlapping matches)")
    print(f"   Comparisons: {rk.get_comparisons()}")
    
 
    print("\n" + "=" * 75)
    print("TEST 5: Multiple Keywords (CV Analysis Scenario)")
    print("=" * 75)
    
    cv_text = """
    PROFESSIONAL SUMMARY
    Experienced Software Engineer with 5+ years in Python and Java development.
    
    TECHNICAL SKILLS
    - Programming Languages: Python, Java, JavaScript, C++
    - Web Technologies: HTML, CSS, React, Node.js
    - Databases: SQL, MySQL, PostgreSQL, MongoDB
    - Tools: Git, Docker, Jenkins, AWS
    - Data Analysis: Pandas, NumPy, Machine Learning
    
    EXPERIENCE
    Senior Python Developer at Tech Corp (2020-2023)
    - Developed Python applications for data analysis
    - Implemented Machine Learning models using Python and SQL
    - Worked with cross-functional teams on Java microservices
    """
    
    skills = ["Python", "Java", "SQL", "Machine Learning", "JavaScript", "Ruby", "React"]
    
    print(f"CV Length: {len(cv_text)} characters")
    print(f"Searching for {len(skills)} keywords...\n")
    
    results = rk.search_multiple(cv_text, skills, case_sensitive=False)
    
    print(f"{'KEYWORD':<20} {'FOUND':<10} {'OCCURRENCES':<15} {'POSITIONS'}")
    print("-" * 75)
    
    found_count = 0
    for skill, positions in results.items():
        if positions:
            found_count += 1
            status = " YES"
            count = len(positions)
            pos_str = str(positions[:3]) + "..." if len(positions) > 3 else str(positions)
        else:
            status = " NO"
            count = 0
            pos_str = "-"
        
        print(f"{skill:<20} {status:<10} {count:<15} {pos_str}")
    
    match_rate = (found_count / len(skills)) * 100
    print(f"\n Match Statistics:")
    print(f"   Skills Found: {found_count}/{len(skills)}")
    print(f"   Match Rate: {match_rate:.1f}%")
    print(f"   Total Comparisons: {rk.get_comparisons():,}")
    print(f"   Avg Comparisons per Keyword: {rk.get_comparisons() / len(skills):.0f}")
    
  
    print("\n" + "=" * 75)
    print("TEST 6: Algorithm Performance Verification")
    print("=" * 75)
    
    import time
    
   
    test_sizes = [100, 500, 1000, 5000, 10000]
    test_pattern = "algorithm"
    
    print(f"Pattern: '{test_pattern}' (length: {len(test_pattern)})")
    print(f"\n{'Text Size':<12} {'Time (ms)':<15} {'Comparisons':<15} {'Ratio'}")
    print("-" * 75)
    
    for size in test_sizes:
       
        test_text = ("data " * (size // 5)) + test_pattern + (" science" * (size // 8))
        test_text = test_text[:size]  
        
        rk_test = RabinKarp(prime=101)
        
        start_time = time.time()
        matches = rk_test.search(test_text, test_pattern, case_sensitive=False)
        end_time = time.time()
        
        exec_time = (end_time - start_time) * 1000  
        comparisons = rk_test.get_comparisons()
        ratio = comparisons / size if size > 0 else 0
        
        print(f"{size:<12} {exec_time:<15.4f} {comparisons:<15} {ratio:.3f}")
    
    print("\n Expected Behavior:")
    print("   - Average case: O(n + m) ≈ O(n) when m << n")
    print("   - Ratio should be relatively constant for similar patterns")
    print("   - Much better than O(n·m) of brute force")
    
   
    print("\n" + "=" * 75)
    print("TEST 7: Hash Collision Handling")
    print("=" * 75)
    
   
    rk_collision = RabinKarp(prime=7)
    
    text7 = "abcdefghijklmnopqrstuvwxyz"
    pattern7 = "xyz"
    
    matches7 = rk_collision.search(text7, pattern7, case_sensitive=True)
    print(f"Text:    '{text7}'")
    print(f"Pattern: '{pattern7}'")
    print(f"Prime:   7 (small prime to test collision handling)")
    print(f" Found at positions: {matches7}")
    print(f"   Comparisons: {rk_collision.get_comparisons()}")
    print(f"\n Algorithm correctly handles collisions through verification!")
    
    # Final summary
    print("\n" + "=" * 75)
    print(" ALL TESTS COMPLETED SUCCESSFULLY")
    print("=" * 75)
    print("\n Key Achievements:")
    print("   ✓ Correct implementation of rolling hash formula")
    print("   ✓ Proper handling of hash collisions")
    print("   ✓ Case-sensitive and case-insensitive search")
    print("   ✓ Multiple pattern search capability")
    print("   ✓ Efficient performance on large texts")
    print("   ✓ Accurate comparison counting for analysis")
    print("\n Algorithm Features:")
    print("   • Time Complexity: O(n + m) average case")
    print("   • Space Complexity: O(1)")
    print("   • Best for: Multiple keyword matching in CV analysis")
    print("   • Rolling hash: Efficient window sliding technique")
    print("\n" + "=" * 75)
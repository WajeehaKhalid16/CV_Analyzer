"""
CV Analyzer - Clean Version
Text normalization now handled by FileReader
"""

import time
import re

class CVAnalyzer:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.results = {}
    
    def extract_keywords_from_job_description(self, job_text):
        """
        Extract mandatory and optional keywords from job description
        """
        keywords = {
            'mandatory': [],
            'optional': []
        }
        
        # Extract mandatory skills
        mandatory_match = re.search(
            r'MANDATORY SKILLS.*?:(.*?)(?:OPTIONAL SKILLS|RESPONSIBILITIES|$)', 
            job_text, 
            re.DOTALL | re.IGNORECASE
        )
        
        if mandatory_match:
            mandatory_text = mandatory_match.group(1)
            mandatory_keywords = re.findall(r'[-•]\s*([^\n]+)', mandatory_text)
            keywords['mandatory'] = [k.strip() for k in mandatory_keywords if k.strip()]
        
        # Extract optional skills
        optional_match = re.search(
            r'OPTIONAL SKILLS.*?:(.*?)(?:RESPONSIBILITIES|QUALIFICATIONS|$)', 
            job_text, 
            re.DOTALL | re.IGNORECASE
        )
        
        if optional_match:
            optional_text = optional_match.group(1)
            optional_keywords = re.findall(r'[-•]\s*([^\n]+)', optional_text)
            keywords['optional'] = [k.strip() for k in optional_keywords if k.strip()]
        
        return keywords
    
    def analyze_cv(self, cv_text, job_text):
        """
        Analyze CV against job description
        Text is already normalized by FileReader
        """
        # Extract keywords
        keywords = self.extract_keywords_from_job_description(job_text)
        
        # Initialize results with ALL required fields
        results = {
            'algorithm': self.algorithm.name,
            'mandatory_keywords': keywords['mandatory'],
            'optional_keywords': keywords['optional'],
            'mandatory_found': [],
            'mandatory_missing': [],
            'optional_found': [],
            'optional_missing': [],
            'mandatory_score': 0.0,
            'optional_score': 0.0,
            'overall_score': 0.0,
            'execution_time': 0.0,
            'comparisons': 0,
            'text_length': len(cv_text),
            'pattern_length': 0,
            'num_patterns': 0
        }
        
        # Calculate pattern metrics
        all_patterns = keywords['mandatory'] + keywords['optional']
        results['pattern_length'] = sum(len(kw) for kw in all_patterns)
        results['num_patterns'] = len(all_patterns)
        
        # Measure execution time
        start_time = time.perf_counter()
        
        # Search for all keywords
        all_keywords = keywords['mandatory'] + keywords['optional']
        search_results = self.algorithm.search_multiple(
            cv_text, all_keywords, case_sensitive=False
        )
        
        end_time = time.perf_counter()
        results['execution_time'] = (end_time - start_time) * 1000.0
        
        # Categorize found/missing keywords
        for keyword in keywords['mandatory']:
            if search_results.get(keyword):
                results['mandatory_found'].append(keyword)
            else:
                results['mandatory_missing'].append(keyword)
        
        for keyword in keywords['optional']:
            if search_results.get(keyword):
                results['optional_found'].append(keyword)
            else:
                results['optional_missing'].append(keyword)
        
        # Get comparisons count
        try:
            comparisons = self.algorithm.get_comparisons()
            results['comparisons'] = int(comparisons) if comparisons else 0
        except AttributeError:
            results['comparisons'] = 0
        
        # Algorithm-specific metrics
        if self.algorithm.name == "KMP":
            try:
                if hasattr(self.algorithm, 'get_preprocessing_time'):
                    results['preprocessing_time'] = self.algorithm.get_preprocessing_time()
            except:
                pass
        
        elif self.algorithm.name == "Rabin-Karp":
            try:
                if hasattr(self.algorithm, 'get_collision_stats'):
                    collision_stats = self.algorithm.get_collision_stats()
                    results['collision_stats'] = collision_stats
                    results['hash_collisions'] = collision_stats.get('collisions', 0)
                    results['collision_rate'] = collision_stats.get('collision_rate', 0.0)
            except:
                pass
        
        # Calculate scores
        total_mandatory = len(keywords['mandatory'])
        total_optional = len(keywords['optional'])
        
        if total_mandatory > 0:
            results['mandatory_score'] = (len(results['mandatory_found']) / total_mandatory) * 100.0
        
        if total_optional > 0:
            results['optional_score'] = (len(results['optional_found']) / total_optional) * 100.0
        
        # Overall score: 70% mandatory + 30% optional
        results['overall_score'] = (results['mandatory_score'] * 0.8) + (results['optional_score'] * 0.2)
        
        self.results = results
        return results
    
    def get_summary(self):
        """Get detailed text summary of analysis"""
        if not self.results:
            return "No analysis performed yet."
        
        r = self.results
        
        summary = f"""
{'='*70}
CV ANALYSIS REPORT
{'='*70}
Algorithm Used: {r['algorithm']}

MANDATORY SKILLS ({len(r['mandatory_found'])}/{len(r['mandatory_keywords'])}):
  Found: {', '.join(r['mandatory_found']) if r['mandatory_found'] else 'None'}
  Missing: {', '.join(r['mandatory_missing']) if r['mandatory_missing'] else 'None'}

OPTIONAL SKILLS ({len(r['optional_found'])}/{len(r['optional_keywords'])}):
  Found: {', '.join(r['optional_found']) if r['optional_found'] else 'None'}
  Missing: {', '.join(r['optional_missing']) if r['optional_missing'] else 'None'}

SCORES:
- Mandatory Skills Match: {r['mandatory_score']:.2f}%
- Optional Skills Match: {r['optional_score']:.2f}%
- Overall Match Score: {r['overall_score']:.2f}% (70% mandatory + 30% optional)

PERFORMANCE METRICS:
- Execution Time: {r['execution_time']:.4f} ms
- Character Comparisons: {r['comparisons']:,}
- CV Length: {r['text_length']:,} characters
- Patterns Searched: {r['num_patterns']}
- Total Pattern Length: {r['pattern_length']} characters
"""
        
        if r['algorithm'] == "KMP" and 'preprocessing_time' in r:
            summary += f"- Preprocessing Time: {r['preprocessing_time']:.4f} ms\n"
        
        elif r['algorithm'] == "Rabin-Karp" and 'collision_stats' in r:
            cs = r['collision_stats']
            summary += f"\nCOLLISION ANALYSIS:\n"
            summary += f"- Hash Matches: {cs['hash_matches']}\n"
            summary += f"- Actual Matches: {cs['actual_matches']}\n"
            summary += f"- False Positives: {cs['collisions']}\n"
            summary += f"- Collision Rate: {cs['collision_rate']:.2f}%\n"
        
        summary += f"\n{'='*70}\n"
        
        return summary
    
    def compare_algorithms(self, cv_text, job_text, algorithms):
        """Compare multiple algorithms on same CV"""
        comparison_results = []
        
        for algo in algorithms:
            analyzer = CVAnalyzer(algo)
            result = analyzer.analyze_cv(cv_text, job_text)
            comparison_results.append(result)
        
        return comparison_results

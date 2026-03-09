class RabinKarpDetector:
    def __init__(self):
        # CONSTANTS FOR ROLLING HASH
        self.d = 256  # Number of characters in the input alphabet (ASCII)
        self.q = 101  # A prime number to minimize hash collisions
        
       # THE EXPANDED DATABASE
        # We categorize these to show we understand AI behavior
        self.suspicious_patterns = {
            # HIGH IMPACT (10 points) - Classic ChatGPT dramatic metaphors
            "delve into": 10,
            "tapestry of": 10,
            "testament to": 10,
            "transformative power": 10,
            "underscores the": 10,
            "democratize": 10,
            "foster a sense": 10,
            "nuanced understanding": 10,
            "indelible mark": 10,
            "landscape of": 10,
            "realm of": 10,
            "paradigm shift": 10,
            "seamless integration": 10,
            "beacon of": 10,
            "multifaceted approach": 10,
            "symbiotic relationship": 10,
            "intricate dance": 10,
            "navigating the complexities": 10,
            "a stark reminder": 10,
            "catalyst for change": 10,
        
            # MEDIUM IMPACT (7 points) - Common structural and conclusive markers
            "in conclusion": 7,
            "it is important to note": 7,
            "it is crucial to": 7,
            "it is worth noting": 7,
            "ultimately": 7,
            "at its core": 7,
            "serves as a reminder": 7,
            "in essence": 7,
            "ever-evolving": 7,
            "rapidly evolving": 7,
            "game-changer": 7,
            "poised to": 7,
            "unleash the": 7,
            "harness the power": 7,
            "shed light on": 7,
            "pivotal role": 7,
            "vital role": 7,
            "by and large": 7,
            "to summarize": 7,
            "in summary": 7,
        
            # LOWER IMPACT (4 points) - Overused vocabulary and transitions
            "significantly": 4,
            "comprehensive": 4,
            "meticulous": 4,
            "moreover": 4,
            "consequently": 4,
            "furthermore": 4,
            "additionally": 4,
            "subsequently": 4,
            "stark contrast": 4,
            "crucial aspect": 4,
            "leveraging": 4,
            "utilizing": 4,
            "dynamic": 4,
            "robust": 4,
            "resilient": 4,
            "noteworthy": 4,
            "pertinent": 4,
            "intricate": 4,
            "paramount": 4,
            "imperative": 4
        }

    def search_pattern(self, text, pattern):
        """
        Standard Rabin-Karp Algorithm Implementation
        Returns a list of starting indices where pattern is found.
        """
        M = len(pattern)
        N = len(text)
        p = 0    # Hash value for pattern
        t = 0    # Hash value for text
        h = 1    # The multiplier for the highest place value
        found_indices = []

        # If pattern is longer than text, it can't exist
        if M > N:
            return []

        # Calculate the value of h = (d^(M-1)) % q
        for i in range(M-1):
            h = (h * self.d) % self.q

        # Calculate the hash value of pattern and first window of text
        for i in range(M):
            p = (self.d * p + ord(pattern[i])) % self.q
            t = (self.d * t + ord(text[i])) % self.q

        # Slide the window over text one by one
        for i in range(N - M + 1):
            #  Check if hash values match
            if p == t:
                # Check for characters one by one (to handle spurious hits)
                if text[i:i+M] == pattern:
                    found_indices.append(i)

            # Calculate hash value for next window of text: Remove leading digit, add trailing digit
            if i < N - M:
                t = (self.d * (t - ord(text[i]) * h) + ord(text[i+M])) % self.q

                # We might get negative value of t, converting it to positive
                if t < 0:
                    t = t + self.q
        
        return found_indices

    def analyze(self, text):
        if not text:
            return {"score": 0, "verdict": "No Text Provided", "matches": []}

        text = text.lower()
        found_matches = set()
        total_score = 0

        # RUN RABIN-KARP FOR EACH PATTERN
        # (This iterates our algorithm multiple times standard for multi-pattern RK)
        for pattern, weight in self.suspicious_patterns.items():
            # Call our manual algorithm function
            indices = self.search_pattern(text, pattern)
            
            if indices:
                found_matches.add(pattern)
                # Add score for each unique pattern found (not each occurrence)
                total_score += weight

        # SCORING
        likelihood_percentage = min((total_score / 60) * 100, 100)

        if likelihood_percentage > 75:
            verdict = "Highly Likely AI-Generated"
        elif likelihood_percentage > 40:
            verdict = "Possibly AI-Edited"
        else:
            verdict = "Likely Human-Written"

        return {
            "score": round(likelihood_percentage, 2),
            "verdict": verdict,
            "matches": list(found_matches)
        }

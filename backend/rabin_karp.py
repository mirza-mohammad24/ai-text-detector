class RabinKarpDetector:
    def __init__(self):
        # CONSTANTS FOR ROLLING HASH
        self.d = 256  # Number of characters in the input alphabet (ASCII)
        self.q = 101  # A prime number to minimize hash collisions
        
       # THE EXPANDED DATABASE
        # We categorize these to show we understand AI behavior
        self.suspicious_patterns = {
            # CATEGORY A: The "Dead Giveaways" (High Weight: 10) 
            # These are extremely rare in casual human writing
            "delve into": 10,
            "tapestry of": 10,
            "testament to": 10,
            "underscores the": 10,
            "transformative power": 10,
            "democratize": 10,
            "foster a sense": 10,
            "nuanced understanding": 10,
            
            # CATEGORY B: The "Robot Transitions" (Medium Weight: 6-8)
            # AI uses these to structure paragraphs perfectly
            "it is important to note": 7,
            "in conclusion": 6,
            "moreover": 6,
            "consequently": 6,
            "furthermore": 6,
            "stark contrast": 7,
            "crucial aspect": 6,
            "realm of": 6,
            "landscape of": 6,
            "poised to": 7,
            
            # CATEGORY C: The "Empty Fillers" (Low Weight: 4-5)
            # Words that sound smart but say little.
            "significantly": 4,
            "comprehensive": 4,
            "meticulous": 5,
            "indelible mark": 5,
            "ever-evolving": 5,
            "rapidly evolving": 4,
            "game-changer": 4,
            "unleash the": 4,
            "harness the power": 5
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
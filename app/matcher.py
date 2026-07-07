import re
import math
from collections import Counter
from typing import List, Dict, Set

# Curated list of common technical and soft skills
COMMON_SKILLS = {
    # Programming Languages
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "golang", 
    "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "sql", "nosql",
    "html", "css", "sass", "bash", "shell", "powershell", "perl", "matlab",
    
    # Frameworks & Libraries
    "react", "angular", "vue", "svelte", "next.js", "nuxt", "node.js", "express", 
    "django", "fastapi", "flask", "spring boot", "asp.net", "ruby on rails", 
    "laravel", "jquery", "bootstrap", "tailwind", "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "keras", "opencv", "nltk", "spacy", "huggingface",
    
    # Databases & Caching
    "postgresql", "mysql", "mongodb", "redis", "sqlite", "dynamodb", "oracle", 
    "cassandra", "elasticsearch", "mariadb", "firebase", "firestore", "neo4j",
    
    # Cloud & DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "jenkins", 
    "terraform", "ansible", "ci/cd", "github actions", "gitlab ci", "heroku", 
    "netlify", "vercel", "digitalocean", "nginx", "apache", "prometheus", "grafana",
    
    # Methodologies, Concepts & Tools
    "agile", "scrum", "git", "rest api", "graphql", "microservices", "system design", 
    "oop", "functional programming", "unit testing", "jest", "pytest", "jira", 
    "confluence", "trello", "sdlc", "mvc", "oauth", "jwt",
    
    # AI, ML & Data Science
    "machine learning", "deep learning", "artificial intelligence", "data science", 
    "natural language processing", "nlp", "computer vision", "data analysis", 
    "data visualization", "tableau", "power bi", "llm", "large language models",
    
    # Soft & Management Skills
    "project management", "product management", "leadership", "teamwork", 
    "communication", "problem solving", "time management", "public speaking", 
    "negotiation", "collaboration", "analytical thinking", "critical thinking"
}

# Standard English stop words to filter out before similarity calculation
STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", 
    "any", "are", "arent", "as", "at", "be", "because", "been", "before", "being", 
    "below", "between", "both", "but", "by", "cant", "cannot", "could", "couldnt", 
    "did", "didnt", "do", "does", "doesnt", "doing", "dont", "down", "during", 
    "each", "few", "for", "from", "further", "had", "hadnt", "has", "hasnt", "have", 
    "havent", "having", "he", "hed", "hell", "hes", "her", "here", "heres", "hers", 
    "herself", "him", "himself", "his", "how", "hows", "i", "id", "ill", "im", "ive", 
    "if", "in", "into", "is", "isnt", "it", "its", "itself", "lets", "me", "more", 
    "most", "mustnt", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", 
    "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", 
    "same", "shant", "she", "shed", "shell", "shes", "should", "shouldnt", "so", 
    "some", "such", "than", "that", "thats", "the", "their", "theirs", "them", 
    "themselves", "then", "there", "theres", "these", "they", "theyd", "theyll", 
    "theyre", "theyve", "this", "those", "through", "to", "too", "under", "until", 
    "up", "very", "was", "wasnt", "we", "wed", "well", "were", "weve", "werent", 
    "what", "whats", "when", "whens", "where", "wheres", "which", "while", "who", 
    "whos", "whom", "why", "whys", "with", "wont", "would", "wouldnt", "you", "youd", 
    "youll", "youre", "youve", "your", "yours", "yourself", "yourselves"
}

def extract_skills(text: str) -> List[str]:
    """
    Extracts matches from the curated skills directory.
    Uses regex boundaries that account for special characters like C++, C#, .NET.
    """
    text_lower = text.lower()
    found_skills = set()
    
    for skill in COMMON_SKILLS:
        # Escape special characters in the skill for safe regex usage
        escaped_skill = re.escape(skill)
        
        # Handle languages/tools with special trailing chars: e.g. c++, c#, .net
        # Word boundary \b doesn't match after +, #, or before .
        if skill.endswith('++') or skill.endswith('#') or skill.startswith('.'):
            # Use spacing/punctuation boundaries
            pattern = rf"(?:^|\s|[,.;:\"'()])({escaped_skill})(?:$|\s|[,.;:\"'()])"
        else:
            # Standard word boundaries
            pattern = rf"\b{escaped_skill}\b"
            
        if re.search(pattern, text_lower):
            found_skills.add(skill)
            
    # Return sorted list of skills (preserving standard casing if we want, but lowercase is fine)
    # We map back to clean, standardized names
    skill_map = {s: s for s in COMMON_SKILLS}
    # Standardize casing for user output display (e.g. FastAPI, Python, React)
    display_casing = {
        "python": "Python", "javascript": "JavaScript", "typescript": "TypeScript", 
        "java": "Java", "c++": "C++", "c#": "C#", "go": "Go", "golang": "Go", 
        "rust": "Rust", "ruby": "Ruby", "php": "PHP", "swift": "Swift", 
        "kotlin": "Kotlin", "scala": "Scala", "r": "R", "sql": "SQL", "nosql": "NoSQL",
        "html": "HTML", "css": "CSS", "sass": "Sass", "bash": "Bash", "shell": "Shell", 
        "powershell": "PowerShell", "perl": "Perl", "matlab": "MATLAB",
        "react": "React", "angular": "Angular", "vue": "Vue", "svelte": "Svelte", 
        "next.js": "Next.js", "nuxt": "Nuxt.js", "node.js": "Node.js", "express": "Express", 
        "django": "Django", "fastapi": "FastAPI", "flask": "Flask", "spring boot": "Spring Boot", 
        "asp.net": "ASP.NET", "ruby on rails": "Ruby on Rails", "laravel": "Laravel", 
        "jquery": "jQuery", "bootstrap": "Bootstrap", "tailwind": "Tailwind CSS", 
        "pandas": "Pandas", "numpy": "NumPy", "scikit-learn": "Scikit-Learn",
        "tensorflow": "TensorFlow", "pytorch": "PyTorch", "keras": "Keras", 
        "opencv": "OpenCV", "nltk": "NLTK", "spacy": "spaCy", "huggingface": "Hugging Face",
        "postgresql": "PostgreSQL", "mysql": "MySQL", "mongodb": "MongoDB", 
        "redis": "Redis", "sqlite": "SQLite", "dynamodb": "DynamoDB", "oracle": "Oracle", 
        "cassandra": "Cassandra", "elasticsearch": "Elasticsearch", "mariadb": "MariaDB", 
        "firebase": "Firebase", "firestore": "Firestore", "neo4j": "Neo4j",
        "aws": "AWS", "azure": "Azure", "gcp": "GCP", "google cloud": "Google Cloud", 
        "docker": "Docker", "kubernetes": "Kubernetes", "jenkins": "Jenkins", 
        "terraform": "Terraform", "ansible": "Ansible", "ci/cd": "CI/CD", 
        "github actions": "GitHub Actions", "gitlab ci": "GitLab CI", "heroku": "Heroku", 
        "netlify": "Netlify", "vercel": "Vercel", "digitalocean": "DigitalOcean", 
        "nginx": "Nginx", "apache": "Apache", "prometheus": "Prometheus", "grafana": "Grafana",
        "agile": "Agile", "scrum": "Scrum", "git": "Git", "rest api": "REST API", 
        "graphql": "GraphQL", "microservices": "Microservices", "system design": "System Design", 
        "oop": "OOP", "functional programming": "Functional Programming", "unit testing": "Unit Testing", 
        "jest": "Jest", "pytest": "PyTest", "jira": "Jira", "confluence": "Confluence", 
        "trello": "Trello", "sdlc": "SDLC", "mvc": "MVC", "oauth": "OAuth", "jwt": "JWT",
        "machine learning": "Machine Learning", "deep learning": "Deep Learning", 
        "artificial intelligence": "AI", "data science": "Data Science", 
        "natural language processing": "NLP", "nlp": "NLP", "computer vision": "Computer Vision", 
        "data analysis": "Data Analysis", "data visualization": "Data Visualization", 
        "tableau": "Tableau", "power bi": "Power BI", "llm": "LLM", "large language models": "LLM",
        "project management": "Project Management", "product management": "Product Management", 
        "leadership": "Leadership", "teamwork": "Teamwork", "communication": "Communication", 
        "problem solving": "Problem Solving", "time management": "Time Management", 
        "public speaking": "Public Speaking", "negotiation": "Negotiation", 
        "collaboration": "Collaboration", "analytical thinking": "Analytical Thinking", 
        "critical thinking": "Critical Thinking"
    }
    
    formatted_skills = sorted(list({display_casing.get(skill, skill) for skill in found_skills}))
    return formatted_skills


def tokenize(text: str) -> List[str]:
    """
    Cleans, lowercases, and splits text into individual words, removing punctuation
    and filtering out stop words.
    """
    # Replace non-alphanumeric (except special characters like +, #, .) with space
    # Keep +, #, . in tokens so they can match things like C++, C#, .NET
    text = text.lower()
    tokens = re.findall(r'[a-z0-9+#\.]+', text)
    
    # Filter out empty tokens and standard stop words
    filtered_tokens = [t for t in tokens if t and t not in STOP_WORDS and len(t) > 1]
    return filtered_tokens


class TFIDFMatcher:
    """
    A pure Python TF-IDF Vectorizer and Cosine Similarity calculator.
    Designed to have no heavy package dependencies.
    """
    def __init__(self, corpus: List[str]):
        """
        Initializes the TFIDFMatcher with a corpus to calculate Inverse Document Frequency (IDF).
        """
        self.doc_count = len(corpus)
        self.df: Dict[str, int] = {}  # Document Frequency
        self.idf: Dict[str, float] = {}  # Inverse Document Frequency
        
        # Tokenize corpus documents
        tokenized_corpus = [tokenize(doc) for doc in corpus]
        
        # Calculate Document Frequency
        for doc_tokens in tokenized_corpus:
            unique_tokens = set(doc_tokens)
            for token in unique_tokens:
                self.df[token] = self.df.get(token, 0) + 1
                
        # Calculate IDF with smoothing
        for token, df_val in self.df.items():
            self.idf[token] = math.log((1 + self.doc_count) / (1 + df_val)) + 1.0

    def compute_tfidf(self, text: str) -> Dict[str, float]:
        """
        Computes TF-IDF vector for a given document.
        Vector is represented as a dictionary of token -> tf_idf_score.
        """
        tokens = tokenize(text)
        total_tokens = len(tokens)
        if total_tokens == 0:
            return {}
            
        tf = Counter(tokens)
        tfidf_vec = {}
        
        for token, count in tf.items():
            # Standard Term Frequency
            term_freq = count / total_tokens
            # Get IDF from trained corpus (defaulting to 1.0 for out of vocabulary words)
            idf_val = self.idf.get(token, 1.0)
            tfidf_vec[token] = term_freq * idf_val
            
        return tfidf_vec

    @staticmethod
    def cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """
        Computes the cosine similarity between two sparse TF-IDF vectors.
        """
        # Find intersection of vocabularies
        intersection = set(vec1.keys()) & set(vec2.keys())
        
        # Dot product
        dot_product = sum(vec1[token] * vec2[token] for token in intersection)
        
        # Magnitude calculation
        magnitude1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
        magnitude2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
        
        if magnitude1 == 0.0 or magnitude2 == 0.0:
            return 0.0
            
        return dot_product / (magnitude1 * magnitude2)

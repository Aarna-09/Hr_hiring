# from sentence_transformers import SentenceTransformer, util
# import torch

# class Ranker:
#     def __init__(self, model_name='all-MiniLM-L6-v2'):
#         # ✅ Force CPU device to avoid meta tensor issue
#         self.device = "cuda" if torch.cuda.is_available() else "cpu"
#         # Force SentenceTransformer to use CPU at load to avoid meta tensor bug
#         self.model = SentenceTransformer(model_name, device='cpu')

#     def rank_resumes(self, job_description_text, resumes, top_k=5):
#         corpus_texts = [r['text'] for r in resumes]

#         # Encode safely
#         jd_emb = self.model.encode(job_description_text, convert_to_tensor=True)
#         corpus_emb = self.model.encode(corpus_texts, convert_to_tensor=True)

#         scores = util.cos_sim(jd_emb, corpus_emb)[0].cpu().numpy()

#         results = []
#         for idx, score in enumerate(scores):
#             results.append({
#                 'filename': resumes[idx]['filename'],
#                 'text': resumes[idx]['text'],
#                 'score': float(score)
#             })

#         results = sorted(results, key=lambda x: x['score'], reverse=True)
#         return results[:top_k]


from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
import torch
import re

class Ranker:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(model_name, device='cpu')

    def clean_text(self, text):
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.lower().strip()

    def extract_keywords(self, job_description, resumes, top_n=25):
        """
        Automatically extract top TF-IDF keywords across job description + resumes.
        """
        texts = [job_description] + [r['text'] for r in resumes]
        cleaned = [self.clean_text(t) for t in texts]

        vectorizer = TfidfVectorizer(stop_words='english', max_features=2000)
        X = vectorizer.fit_transform(cleaned)
        feature_names = vectorizer.get_feature_names_out()

        # Get top words for JD
        jd_tfidf = X[0].toarray().flatten()
        top_jd_idx = jd_tfidf.argsort()[-top_n:]
        top_jd_words = [feature_names[i] for i in top_jd_idx]

        return set(top_jd_words)

    def find_matching_keywords(self, jd_keywords, resume_text):
        """
        Find automatically matching important keywords.
        """
        resume_text = self.clean_text(resume_text)
        return [kw for kw in jd_keywords if kw in resume_text]

    def rank_resumes(self, job_description_text, resumes, top_k=5):
        corpus_texts = [r['text'] for r in resumes]

        # ✅ Embedding-based similarity
        jd_emb = self.model.encode(job_description_text, convert_to_tensor=True)
        corpus_emb = self.model.encode(corpus_texts, convert_to_tensor=True)
        scores = util.cos_sim(jd_emb, corpus_emb)[0].cpu().numpy()

        # ✅ Auto keyword extraction
        jd_keywords = self.extract_keywords(job_description_text, resumes)

        # ✅ Combine ranking + auto skill match
        results = []
        for idx, score in enumerate(scores):
            matching_keywords = self.find_matching_keywords(jd_keywords, resumes[idx]['text'])
            results.append({
                'filename': resumes[idx]['filename'],
                'text': resumes[idx]['text'],
                'score': float(score),
                'matching_keywords': matching_keywords ,
                'matching_skills': matching_keywords  
            })

        results = sorted(results, key=lambda x: x['score'], reverse=True)
        return results[:top_k]
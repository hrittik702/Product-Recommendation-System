import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations(target_product_name, df):
    # Create a "Content Soup" for better matching
    df['content'] = df['category'] + " " + df['description'] + " " + df['tags']
    
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['content'])
    
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    try:
        idx = df[df['name'] == target_product_name].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top 4 similar products (skipping the item itself)
        top_indices = [i[0] for i in sim_scores[1:5]]
        return df.iloc[top_indices]
    except:
        return pd.DataFrame()
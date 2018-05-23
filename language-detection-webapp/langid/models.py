from .model import Model

from .sanitization import sanitize_v0, sanitize_v1, sanitize_v2

models = dict(
    [(m.description, m) for m in [
        Model(
            model_name="Sanitize-CountVec_feat3000_1-3wordgrams-NaiveIdentifier.pickle",
            description="NaiveIdentifier, CountVectorizer(1-3 wordgrams, 3000 features/lang)",
            sanitizer=sanitize_v2
        ),
        Model(
            model_name="Sanitize-CountVec_feat10000_1-3grams-MultinomialNB.pickle",
            description="MultinomialNB, CountVectorizer(1-3 ngrams, 10000 features)",
            sanitizer=sanitize_v2
        ),
        Model(
            model_name="Sanitize-TfidfVec_feat10000_trigrams-logreg_C1.pickle",
            description="LogisticRegression(C=1), TfidfVectorizer(trigrams, 10000 features, tfidf)",
            sanitizer=sanitize_v2
        ),
        Model(
            model_name="Sanitize-TfidfVec_feat10000_trigrams-SVM_linear_C1.pickle",
            description="SVM(C=1, kernel=linear), TfidfVectorizer(trigrams, 10000 features, tfidf)",
            sanitizer=sanitize_v2
        ),
        # # OLD MODELS
        # Model(
        #     model_name="model_3-5grams-sg-feat6000-tf-idf_logreg-V2.pickle",
        #     description="NEW san, sg_only, vec(ngrams=(3,5),features=6'000,tf,if), logreg",
        #     sanitizer=sanitize_v1
        # ),
        # Model(
        #     model_name="model_trigrams-all-feat10000-tf-idf_logreg.pickle",
        #     description="san, vec(ngrams=3,features=10'0000,tf,idf), logreg",
        #     sanitizer=sanitize_v0
        # ),
        Model(
            model_name="model_3-5grams-sg-feat6000-tf-idf_logreg.pickle",
            description="OLD san, sg_only, vec(ngrams=(3,5),features=6'000,tf,if), logreg",
            sanitizer=sanitize_v0
        ),
        # Model(
        #     model_name="model_trigrams-all-feat10000-tf-idf_svc-liblinear-c1.pickle",
        #     description="san, vec(ngrams=3,features=10'0000,tf,idf), svc(c=1, kernel=liblinear)",
        #     sanitizer=sanitize_v0
        # )

    ]])

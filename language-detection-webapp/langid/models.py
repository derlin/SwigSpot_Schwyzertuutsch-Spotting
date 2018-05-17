from .model import Model

from .sanitization import sanitize_v0, sanitize_v1

models = dict(
    [(m.description, m) for m in [
        Model(
            model_name="model_3-5grams-sg-feat6000-tf-idf_logreg-V2.pickle",
            description="NEW san, sg_only, vec(ngrams=(3,5),features=6'000,tf,if), logreg",
            sanitizer=sanitize_v1
        ),
        Model(
            model_name="model_trigrams-all-feat10000-tf-idf_logreg.pickle",
            description="san, vec(ngrams=3,features=10'0000,tf,idf), logreg",
            sanitizer=sanitize_v0
        ),
        Model(
            model_name="model_3-5grams-sg-feat6000-tf-idf_logreg.pickle",
            description="OLD san, sg_only, vec(ngrams=(3,5),features=6'000,tf,if), logreg",
            sanitizer=sanitize_v0
        ),
        Model(
            model_name="model_trigrams-all-feat10000-tf-idf_svc-liblinear-c1.pickle",
            description="san, vec(ngrams=3,features=10'0000,tf,idf), svc(c=1, kernel=liblinear)",
            sanitizer=sanitize_v0
        )]
     ])

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegressionCV

def params_to_string(params, sep=", "): 
    return sep.join([ "{}:{}".format(k[6:], str(v)[:10]) for (k,v) in params.items()])


def print_best_estimator(gs: GridSearchCV):
    print()
    print("Best score: %0.3f" % gs.best_score_)
    print("Best parameters set:")
    for p in gs.best_params_.items(): print("\t%s: %r" % p)


def print_scores_csv(gs):
    ms = gs.cv_results_['mean_test_score']
    ss = gs.cv_results_['std_test_score']
    params = gs.cv_results_['params']
    print("mean, std,", ",".join(params[0].keys()))
    for mean, std, p in zip(ms, ss, params):
        print("%0.3f, %0.03f, %s" % (mean, std * 2, ", ".join(["{}".format(v) for v in p.values()])))

def print_scores(gs: GridSearchCV):
    print("Grid scores on development set:\n")

    ms = gs.cv_results_['mean_test_score']
    ss = gs.cv_results_['std_test_score']

    for mean, std, params in zip(ms, ss, gs.cv_results_['params']):
        print("%0.3f (+/-%0.03f): %s" % (mean, std * 2, params_to_string(params)) )
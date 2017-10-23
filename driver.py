from test_Util import *

fileRoot = "../Search-Engines/HW3/"

# # software testing for HW3
# checklist10 = ["HW3-Train-1", "HW3-Train-2", "HW3-Train-3", "HW3-Train-4", "HW3-Train-5", "HW3-Train-6", "HW3-Train-7", "HW3-Train-8", "HW3-Train-9", "HW3-Train-10"]
# testSoftware(checklist10)

# trec_eval service
fileDirExp1 = fileRoot + "exp1/"
exp1Output = fileDirExp1 + "exp1.out"
print "\n"
getTrecSummaryScore(exp1Output)

# exp4
cnt = 0;
fileDirExp2 = fileRoot + "exp4/"
trecEvalOutputLength = "100"
queryFilePath = fileRoot + "Indri-Bow.qry"
indrimu = "1300"
indrimulambda = "0.1"
retrievalAlgorithm = "Indri"
fbDocs = "100" # best value in exp2
fbTerms = "30" # best value in exp3
fbMu = "1300"
fbInitialRankingFile = fileDirExp2 + "Indri-Bow.teIn"
resExp2 = []
for fbOrigWeight in [0.2, 0.4, 0.6, 0.8, 1.0]:
    trecEvalOutputPath = fileDirExp2 + "exp4" + "_" + str(fbOrigWeight) + ".output"
    fbExpansionQueryFile = fileDirExp2 + "exp4" + "_" + str(fbOrigWeight) + ".expQry"
    command = ["java", "-cp", "../QryEval:../lucene-6.6.0/*", "QryEval", "-indexPath", "../index", "-queryFilePath", queryFilePath,
               "-trecEvalOutputPath", trecEvalOutputPath, "-trecEvalOutputLength", trecEvalOutputLength, "-retrievalAlgorithm", retrievalAlgorithm,
               "-indrimu", indrimu, "-indrilambda", indrimulambda, "-fbDocs", fbDocs, "-fbTerms", fbTerms, "-fbMu", fbMu,
               "-fbOrigWeight", str(fbOrigWeight), "-fb", "true", "-fbExpansionQueryFile", fbExpansionQueryFile, "-fbInitialRankingFile", fbInitialRankingFile]
    call(command)
    print "fbTerms = ", fbTerms
    resExp2.append(getTrecSummaryScore(trecEvalOutputPath))
    cnt = cnt + 1;
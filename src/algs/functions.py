class Functions:

    def configure_model_spark(self, model, params):
        for p in model.params:
            if p.name in params:
                if p.name == "inputCol":
                    model.setInputCol(str(params[p.name]))
                if p.name == "minCount":
                    model.setMinCount(int(params[p.name]))
                if p.name == "maxIter":
                    model.setMaxIter(int(params[p.name]))
                if p.name == "numPartitions":
                    model.setNumPartitions(int(params[p.name]))
                if p.name == "maxSentenceLength":
                    model.setMaxSentenceLength(int(params[p.name]))
                if p.name == "outputCol":
                    model.setOutputCol(str(params[p.name]))
                if p.name == "seed":
                    model.setSeed(int(params[p.name]))
                if p.name == "stepSize":
                    model.setStepSize(float(params[p.name]))
                if p.name == "vectorSize":
                    model.setVectorSize(int(params[p.name]))
                if p.name == "windowSize":
                    model.setWindowSize(int(params[p.name]))

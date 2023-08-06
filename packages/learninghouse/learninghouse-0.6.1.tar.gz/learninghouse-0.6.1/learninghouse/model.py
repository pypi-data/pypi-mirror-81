#coding: utf-8

from flask import request, jsonify
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from joblib import load, dump

import json

from os import path, stat
import sys

import time

import pandas as pd
import numpy as np

from . import __version__

from .preprocessing import DatasetPreprocessing
from .estimator import EstimatorFactory

from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import confusion_matrix, accuracy_score

class ModelConfiguration():
    CONFIG_FILE = 'models/config/%s.json'
    COMPILED_FILE = 'models/compiled/%s.pkl'

    def __init__(self, name):
        self.name = name

        self.__jsonConfig = self.__loadInitialConfig(name)

        self.estimatorcfg = self.__requiredConfig('estimator')
        self.testsize = self.__requiredConfig('test_size')
        self.features = self.__requiredConfig('features')
        self.dependent = self.__requiredConfig('dependent')

        self.categoricals = self.__optionalConfig('categoricals')
        if self.categoricals is None:
            self.nonCategoricals = self.features
        else:
            self.nonCategoricals = [item for item in self.features if item not in set(self.categoricals)]

        self.imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

        self.standard_scaled = self.__optionalConfig('standard_scaled')
        if self.standard_scaled is not None:
            self.standard_scaler = StandardScaler()
            self.standard_scaler_fitted = False

        self.dependentEncode = self.__optionalConfig('dependent_encode', False)

        self.estimator = None
        self.columns = None
        self.score = 0.0
        self.confusion = None
        self.version = __version__

    def __loadInitialConfig(self, name):
        with open(ModelConfiguration.CONFIG_FILE % name, 'r') as configFile:
            return json.load(configFile)

    def __requiredConfig(self, param):
        if param in self.__jsonConfig:
            return self.__jsonConfig[param]
        else:
            raise Exception('Missing required param %s' % param)

    def __optionalConfig(self, param, default = None):
        if param in self.__jsonConfig:
            return self.__jsonConfig[param]
        else:
            return default

    def hasCategoricals(self):
        return self.categoricals is not None

    def hasStandardScaled(self):
        return self.standard_scaled is not None

    def hasColumns(self):
        return self.columns is not None

    def configObject(self):
        return {
            'name': self.name,
            'estimator_config': self.estimatorcfg,
            'features': self.features,
            'categoricals': self.categoricals,
            'standard_scaled': self.standard_scaled,
            'dependent': self.dependent,
            'score': self.score,
            'confusion': self.confusion,
            'version': {
                'model': self.version,
                'service': __version__
            }
        }

    def dump(self, estimator, columns, score, confusion):
        self.estimator = estimator
        self.columns = columns
        self.score = score
        self.confusion = confusion

        dump(self, ModelConfiguration.COMPILED_FILE % self.name)

class ModelAPI(Resource):
    @staticmethod
    def makeJSONResponse(data, statusCode = 200, errorCode = None):
        if errorCode is not None:
            data['error'] = errorCode

        resp = jsonify(data)
        resp.status_code = statusCode
        return resp

    @staticmethod 
    def get(model):
        try:
            modelcfg = load(ModelConfiguration.COMPILED_FILE % model)
            return ModelAPI.makeJSONResponse(modelcfg.configObject())
        except FileNotFoundError:
            return ModelAPI.makeJSONResponse({}, 404, 'NOT_TRAINED')
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return ModelAPI.makeJSONResponse({}, 500, 'UNKNOWN_ERROR')

class ModelTraining(Resource):
    TRAINING_FILE = 'models/training/%s.csv'

    @staticmethod
    def put(model):
        if request.content_length > 0 and request.is_json:
            filename = ModelTraining.TRAINING_FILE % model
            jsonData = request.get_json()
            jsonData = DatasetPreprocessing.addTimeInformation(jsonData)
            if path.exists(filename):
                df_temp = pd.read_csv(filename)
                df = df_temp.append([jsonData], ignore_index = True)
            else:
                df = pd.DataFrame([jsonData])

            df.to_csv(filename, sep = ',', index = False)
                
            return ModelTraining.train(model, df)
        else:
            return ModelAPI.makeJSONResponse({}, 400, 'BAD_REQUEST')

    @staticmethod
    def post(model):
        filename = ModelTraining.TRAINING_FILE % model
        
        if request.content_length == 0:
            if path.exists(filename):
                df = pd.read_csv(filename)
                return ModelTraining.train(model, df)
            else:
                return ModelAPI.makeJSONResponse({}, 202, 'NOT_ENOUGH_TRAINING_DATA')
        else:
            return ModelAPI.makeJSONResponse({}, 400, 'BAD_REQUEST')

    @staticmethod
    def train(model, df):
        try:
            modelcfg = ModelConfiguration(model)

            if len(df.index) < 10:
                return ModelAPI.makeJSONResponse({}, 202, 'NOT_ENOUGH_TRAINING_DATA')

            modelcfg, x_train, x_test, y_train, y_test = DatasetPreprocessing.prepareTraining(modelcfg, df)

            estimator = EstimatorFactory.getEstimator(modelcfg.estimatorcfg)
            
            columns = x_train.columns

            estimator.fit(x_train, y_train)
            
            y_pred = estimator.predict(x_test)

            cm = confusion_matrix(y_test, y_pred)
            score = accuracy_score(y_test, y_pred)

            modelcfg.dump(estimator, columns, score, cm.tolist())

            return ModelAPI.makeJSONResponse(modelcfg.configObject())
        except FileNotFoundError:
            return ModelAPI.makeJSONResponse({}, 404, 'NO_CONFIGURATION')
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return ModelAPI.makeJSONResponse({}, 500, 'UNKNOWN_ERROR')

class ModelPrediction(Resource):
    modelcfgs = {}

    @staticmethod
    def post(model):
        try: 
            modelcfg = ModelPrediction._loadModelcfg(model)

            jsonData = request.get_json(force = True)
            jsonData = DatasetPreprocessing.addTimeInformation(jsonData)
            query = pd.DataFrame([jsonData])

            x = DatasetPreprocessing.preparePrediction(modelcfg, query)

            prediction = list(map(float, modelcfg.estimator.predict(x)))

            result = {
                'model': modelcfg.configObject(),
                'prediction': prediction[0]
            }

            return ModelAPI.makeJSONResponse(result)
        except BadRequest as e:
            return ModelAPI.makeJSONResponse({}, 400, 'BAD_REQUEST')
        except KeyError as e:
            return ModelAPI.makeJSONResponse({'message': e.args[0]}, 400, 'MISSING_KEY')
        except FileNotFoundError:
            return ModelAPI.makeJSONResponse({}, 404, 'NOT_TRAINED')
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return ModelAPI.makeJSONResponse({}, 500, 'UNKNOWN_ERROR')

    @staticmethod
    def _loadModelcfg(model):
        filename = ModelConfiguration.COMPILED_FILE % model
        stamp = stat(filename).st_mtime
        
        if model in ModelPrediction.modelcfgs:
            if ModelPrediction.modelcfgs[model]['stamp'] == stamp:
                modelcfg = ModelPrediction.modelcfgs[model]['model']
            else:
                modelcfg = load(filename)
                ModelPrediction.modelcfgs[model] = {
                    'stamp': stamp,
                    'model': modelcfg
                }
        else:
            modelcfg = load(filename)
            ModelPrediction.modelcfgs[model] = {
                'stamp': stamp,
                'model': modelcfg
            }

        return modelcfg


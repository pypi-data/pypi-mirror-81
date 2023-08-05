import os
import json
from graviteeio_cli.lint import rulesets
from graviteeio_cli.lint.types.enums import DiagLevel
from graviteeio_cli.lint.types.document import Document, DocumentType
from graviteeio_cli.lint.rulesets.oas.oas_rules import oas_rules
from graviteeio_cli.lint.rulesets.oas.functions.oasDocumentSchema import oasDocumentSchema

from jsonschema import Draft6Validator, RefResolver


class DiagResult:

    def __init__(self, level: DiagLevel, path: str, message: str):
        super().__init__()
        self.position = None
        self.level = level
        self.path = path
        self.message = message


class Gio_linter:

    def _get_Rulsets(self):
        oas_json_path = os.path.join(
            os.path.dirname(rulesets.__file__),
            'gio_apim/schemas/schema_gio_apim.json'
        )
        with open(oas_json_path) as f:
            data = json.load(f)

    def _get_schema(self, doc_type: DocumentType, version=""):

        oas_json_path = os.path.join(
            os.path.dirname(rulesets.__file__),
            "{0}/schemas/schema_{0}{1}.json".format(doc_type.name, version)
        )
        with open(oas_json_path) as f:
            oas = json.load(f)

        return oas

    def _errorsSchema_to_diagResult(self, error):
        return DiagResult(DiagLevel.Error, '.'.join(error.path), error.message)

    def run(self, document: Document):

        f = oasDocumentSchema

        for key_rule, value_rule in oas_rules.items():
            print(value_rule["description"])
            f(document.values, **value_rule["functionOption"])

        # if document == DocumentType.gio_apim:
        #     schema = self._get_schema(doc_type)
        #     # self._get_Rulsets()
        #     api_entity_schema = schema['components']['schemas']['UpdateApiEntity']
        #     resolver = RefResolver.from_schema(schema)

        #     validator = Draft6Validator(api_entity_schema, resolver=resolver)
        #     # errors = sorted(validator.iter_errors(document), key=lambda e: e.path)

        # else:
        #     version = ""
        #     if isOpenApiv2:
        #         version = "2"
        #     elif isOpenApiv3 or isOpenApiv3_1:
        #         version = "3"

        #     schema = self._get_schema(doc_type, version)

        #     cls = validators.validator_for(schema)
        #     validator = cls(schema)

        # errors = validator.iter_errors(document)

        # #oas2-schema

        # return list(map(self._errorsSchema_to_diagResult, errors))
        return []

    # def loadRuleset(self):
    #     pass

# export const isOpenApiv2 = (document: unknown) =>
#   isObject(document) && 'swagger' in document && parseInt(String((document as MaybeOAS2).swagger)) === 2;

# export const isOpenApiv3 = (document: unknown) =>
#   isObject(document) && 'openapi' in document && parseFloat(String((document as MaybeOAS3).openapi)) === 3;

# export const isOpenApiv3_1 = (document: unknown) =>
#   isObject(document) && 'openapi' in document && parseFloat(String((document as MaybeOAS3).openapi)) === 3.1;

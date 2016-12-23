import logging

from flask import request
from flask_restplus import Resource
from biolink.datamodel.serializers import association
from biolink.api.restplus import api
from causalmodels.lego_sparql_util import lego_query, ModelQuery

log = logging.getLogger(__name__)

ns = api.namespace('cam', description='Operations on causal activity models (LEGO)')

parser = api.parser()

@ns.route('/model/')
class ModelCollection(Resource):

    @api.expect(parser)
    def get(self):
        """
        Returns list of ALL models
        """
        args = parser.parse_args()
        return lego_query("""
        SELECT ?x ?title ?p ?v WHERE 
        {?x a owl:Ontology ; 
           dc:title ?title ;
           ?p ?v
        FILTER(?p != json_model:)
        }""", limit=1000)

@ns.route('/model/query/')
class ModelCollection(Resource):

    @api.expect(parser)
    def get(self):
        """
        Returns list of models matching query

        Experimental - will be merged with above
        """
        args = parser.parse_args()
        mq = ModelQuery()
        sparql = mq.gen_sparql()
        return lego_query(sparql, limit=100)
    
@ns.route('/properties/model/')
class ModelCollection(Resource):

    @api.expect(parser)
    def get(self):
        """
        Returns list of models
        """
        args = parser.parse_args()
        return lego_query("""
        SELECT DISTINCT ?p WHERE 
        {?x a owl:Ontology ; 
           ?p ?v
        FILTER(?p != json_model:)
        }""", limit=1000)

@ns.route('/model/pvs/')
class ModelCollection(Resource):

    @api.expect(parser)
    def get(self):
        """
        Returns list of models
        """
        args = parser.parse_args()
        return lego_query("""
        SELECT DISTINCT ?m ?p ?v WHERE 
        {?m a owl:Ontology ; 
           ?p ?v
        FILTER(?p != json_model:)
        }""", limit=1000)
    
@ns.route('/model/<id>')
class Model(Resource):

    @api.expect(parser)
    @api.marshal_list_with(association)
    def get(self, term):
        """
        Returns list of matches
        """
        args = parser.parse_args()

        return []

@ns.route('/instance/<id>')
class Instance(Resource):

    @api.expect(parser)
    @api.marshal_list_with(association)

    @api.expect(parser)
    @api.marshal_list_with(association)
    def get(self, term):
        """
        Returns list of matches
        """
        args = parser.parse_args()

        return []
    
@ns.route('/activity/')
class ActivityCollection(Resource):

    @api.expect(parser)
    def get(self):
        """
        Returns list of models
        """
        args = parser.parse_args()
        return lego_query("""
        SELECT ?g ?a ?type WHERE 
        {?a a <http://purl.obolibrary.org/obo/GO_0003674> .
        GRAPH ?g {?a a ?type } .
        FILTER(?g != inferredG: && ?type != owl:NamedIndividual)
        }
        """)
    
@ns.route('/physical_interaction/')
class PhysicalInteraction(Resource):

    @api.expect(parser)
    def get(self):
        """
        Returns list of models
        """
        return lego_query("""
        SELECT * WHERE {
        GRAPH ?g {
        ?a1 enabled_by: ?m1 ;
            a ?a1cls ;
            ?arel ?a2 .
        ?a2 enabled_by: ?m2 ;
            a ?a2cls .
        ?m1 a ?m1cls .
        ?m2 a ?m2cls 
        }
        FILTER(?g != inferredG: && ?m1cls != ?m2cls && 
               ?m1cls != owl:NamedIndividual && ?m2cls != owl:NamedIndividual)
        }
        """)
    


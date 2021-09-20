from rdflib import Graph, Namespace, Literal, BNode
from rdflib.namespace import RDF, RDFS, NamespaceManager, XSD
from rdflib.serializer import Serializer
from SPARQLWrapper import SPARQLWrapper, JSON
import csv, random, string, json, urllib
import os.path
from openpyxl import load_workbook
from elasticsearch import Elasticsearch
from alive_progress import alive_bar
import requests
import time
import mysql.connector
import re
from os import path
import sys
from mapping_functions import map_object, map_event, map_image, map_institution, map_person, map_document, map_sample, map_leftover_categories
from common_functions import connect_to_sql 

def create_graph():

    RRO = Namespace("https://rdf.ng-london.org.uk/raphael/ontology/")
    RRI = Namespace("https://rdf.ng-london.org.uk/raphael/resource/")
    CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
    NGO = Namespace("https://data.ng-london.org.uk/")
    AAT = Namespace("http://vocab.getty.edu/page/aat/")
    TGN = Namespace("http://vocab.getty.edu/page/tgn/")
    WD = Namespace("http://www.wikidata.org/entity/")
    SCI = Namespace("http://www.cidoc-crm.org/crmsci/")
    DIG = Namespace("http://www.cidoc-crm.org/crmdig/")
    OWL = Namespace("http://www.w3.org/2002/07/owl#")

    new_graph = Graph()
    new_graph.namespace_manager.bind('crm',CRM)
    new_graph.namespace_manager.bind('ngo',NGO)
    new_graph.namespace_manager.bind('aat',AAT)
    new_graph.namespace_manager.bind('tgn',TGN)
    new_graph.namespace_manager.bind('wd',WD)
    new_graph.namespace_manager.bind('rro',RRO)
    new_graph.namespace_manager.bind('rri',RRI)
    new_graph.namespace_manager.bind('sci',SCI)
    new_graph.namespace_manager.bind('dig', DIG)
    new_graph.namespace_manager.bind('owl', OWL)

    return new_graph

def map_db_to_triples(old_graph, full_rebuild=False): 
    
    # Checking whether specific sections have already been mapped and pulling them in or building them
    if path.exists('outputs/raphael_object.xml') == False or full_rebuild == True:
        object_graph = create_graph()
        new_object_graph = map_object(object_graph, old_graph)
        new_object_graph.serialize(destination='outputs/raphael_object.xml', format='xml')
        new_object_graph.serialize(destination='outputs/raphael_object.ttl', format='ttl')
        new_object_graph.serialize(destination='outputs/raphael_object.trig', format='trig')
    else:
        new_object_graph = Graph()
        new_object_graph = new_object_graph.parse('outputs/raphael_object.xml')
    print('objects mapped!')

    if path.exists('outputs/raphael_event.xml') == False or full_rebuild == True:
        event_graph = create_graph()
        new_event_graph = map_event(event_graph, old_graph)
        new_event_graph.serialize(destination='outputs/raphael_event.xml', format='xml')
        new_event_graph.serialize(destination='outputs/raphael_event.ttl', format='ttl')
        new_event_graph.serialize(destination='outputs/raphael_event.trig', format='trig')
    else:
        new_event_graph = Graph()
        new_event_graph = new_event_graph.parse('outputs/raphael_event.xml')
    print('events mapped!')

    if path.exists('outputs/raphael_person.xml') == False or full_rebuild == True:
        person_graph = create_graph()
        new_person_graph = map_person(person_graph, old_graph)
        new_person_graph.serialize(destination='outputs/raphael_person.xml', format='xml')
        new_person_graph.serialize(destination='outputs/raphael_person.ttl', format='ttl')
        new_person_graph.serialize(destination='outputs/raphael_person.trig', format='trig')
    else:
        new_person_graph = Graph()
        new_person_graph = new_person_graph.parse('outputs/raphael_person.xml')
    print('people mapped!')

    if path.exists('outputs/raphael_place.xml') == False or full_rebuild == True:
        place_graph = create_graph()
        new_place_graph = map_institution(place_graph, old_graph)
        new_place_graph.serialize(destination='outputs/raphael_place.xml', format='xml')
        new_place_graph.serialize(destination='outputs/raphael_place.ttl', format='ttl')
        new_place_graph.serialize(destination='outputs/raphael_place.trig', format='trig')
    else:
        new_place_graph = Graph()
        new_place_graph = new_place_graph.parse('outputs/raphael_place.xml')
    print('places mapped!')
    
    if path.exists('outputs/raphael_document.xml') == False or full_rebuild == True:
        document_graph = create_graph()
        new_document_graph = map_document(document_graph, old_graph)
        new_document_graph.serialize(destination='outputs/raphael_document.xml', format='xml')
        new_document_graph.serialize(destination='outputs/raphael_document.ttl', format='ttl')
        new_document_graph.serialize(destination='outputs/raphael_document.trig', format='trig')
    else:
        new_document_graph = Graph()
        new_document_graph = new_document_graph.parse('outputs/raphael_document.xml')
    print('documents mapped!')
    
    if path.exists('outputs/raphael_sample.xml') == False or full_rebuild == True:
        sample_graph = create_graph()
        new_sample_graph = map_sample(sample_graph, old_graph)
        new_sample_graph.serialize(destination='outputs/raphael_sample.xml', format='xml')
        new_sample_graph.serialize(destination='outputs/raphael_sample.ttl', format='ttl')
        new_sample_graph.serialize(destination='outputs/raphael_sample.trig', format='trig')
    else:
        new_sample_graph = Graph()
        new_sample_graph = new_sample_graph.parse('outputs/raphael_sample.xml')
    print('samples mapped!')
    
    if path.exists('outputs/raphael_image.xml') == False or full_rebuild == True:
        image_graph = create_graph()
        new_image_graph = map_image(image_graph, old_graph)
        new_image_graph.serialize(destination='outputs/raphael_image.xml', format='xml')
        new_image_graph.serialize(destination='outputs/raphael_image.ttl', format='ttl')
        new_image_graph.serialize(destination='outputs/raphael_image.trig', format='trig')
    else:
        new_image_graph = Graph()
        new_image_graph = new_image_graph.parse('outputs/raphael_image.xml')
    print('images mapped!')
    
    if path.exists('outputs/raphael_leftover_categories.xml') == False or full_rebuild == True:
        leftovers_graph = create_graph()
        new_leftovers_graph = map_leftover_categories(leftovers_graph, old_graph)
        new_leftovers_graph.serialize(destination='outputs/raphael_leftover_categories.xml', format='xml')
        new_leftovers_graph.serialize(destination='outputs/raphael_leftover_categories.ttl', format='ttl')
        new_leftovers_graph.serialize(destination='outputs/raphael_leftover_categories.trig', format='trig')
    else:
        new_leftovers_graph = Graph()
        new_leftovers_graph = new_leftovers_graph.parse('outputs/raphael_leftover_categories.xml')
    print('leftover categories mapped!')
      
    full_graph = Graph()
    full_graph.parse('outputs/raphael_object.xml')
    full_graph.parse('outputs/raphael_event.xml')
    full_graph.parse('outputs/raphael_person.xml')
    full_graph.parse('outputs/raphael_place.xml')
    full_graph.parse('outputs/raphael_document.xml')
    full_graph.parse('outputs/raphael_sample.xml')
    full_graph.parse('outputs/raphael_image.xml')
    full_graph.parse('outputs/raphael_leftover_categories.xml')

    return full_graph

def main():
    RRO = Namespace("https://rdf.ng-london.org.uk/raphael/ontology/")
    RRI = Namespace("https://rdf.ng-london.org.uk/raphael/resource/")
    old_graph = Graph()
    old_graph.parse("inputs/rrr_i_v0.5.xml", format="xml")
    old_graph.bind('rro',RRO)
    old_graph.bind('rri',RRI)

    if sys.argv[0] == 'fullrebuild':
        new_graph = map_db_to_triples(old_graph, full_rebuild=True)
    else:
        new_graph = map_db_to_triples(old_graph)

    new_graph.serialize(destination='outputs/raphael_final.xml', format='xml')
    new_graph.serialize(destination='outputs/raphael_final.ttl', format='ttl')
    new_graph.serialize(destination='outputs/raphael_final.trig', format='trig')
    print('Finished running, all looking good')

if __name__ == '__main__':
    main()
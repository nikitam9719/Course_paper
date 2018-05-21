#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import csv
import sys

from SPARQLWrapper import SPARQLWrapper, JSON, CSV, TURTLE

from dbpediaEnquirerPy import *
from rdflib import Graph


if __name__ == '__main__':
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    g = Graph()
    g.parse('instance_types_ru.ttl', format='turtle')
    k=g.subject_objects()
    allentities={'Person','Organisation','Place'}
    with open('Output_Packeruni', 'w',encoding="utf16") as csvfile:
        fieldnames = ['name', 'type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter='/')

        writer.writeheader()
        for tup in k:
            name=str(tup[0]).split('/')[-1]
            cl=str(tup[1]).split('/')[-1]
            sparql.setQuery("""
            PREFIX dbr: <http://dbpedia.org/ontology/>
            SELECT DISTINCT ?c WHERE {
            dbr:%s rdfs:subClassOf+ ?c .
    } 
        """%(cl))
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            for result in results["results"]["bindings"]:
                temp=result['c']['value']
                if "http://dbpedia.org/ontology/"in temp:
                    temp2=temp.split('/')[-1]
                    if(temp2 in allentities):
                        writer.writerow({'name': name, 'type': temp2})
                        break
            else:
                writer.writerow({'name': name, 'type': "Misc"})


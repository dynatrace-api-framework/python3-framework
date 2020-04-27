#!/bin/python3
"""Cluster SSL Certificate Operations"""
import dynatrace.requests.request_handler as rh

def get_cert_details(cluster, entity_type, entity_id):
  """Get SSL Certificate information for Server or Cluster ActiveGate"""
  response = rh.cluster_get(
      cluster,
      "sslCertificate/" + str(entity_type) + "/" + str(entity_id)
  )
  return response.json()

def get_cert_install_status(cluster, entity_id):
  """Get SSL Storage Status for Cluster ActiveGate"""
  response = rh.cluster_get(
      cluster,
      "sslCertificate/store/COLLECTOR/" + str(entity_id)
  )
  return response.text

def set_cert(cluster, entity_type, entity_id, ssl_json):
  """Set SSL Storage Status for Server or Cluster ActiveGate"""
  response = rh.cluster_post(
      cluster,
      "sslCertificate/store/" + str(entity_type) + "/" + str(entity_id),
      json=ssl_json
  )
  return response.json()


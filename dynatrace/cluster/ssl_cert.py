#!/bin/python3
"""Cluster SSL Certificate Operations"""
import dynatrace.framework.request_handler as rh


def get_cert_details(cluster, entity_type, entity_id):
    """Get SSL Certificate information for Server or Cluster ActiveGate"""
    response = rh.make_api_call(
        cluster=cluster,
        endpoint=f"{rh.ClusterAPIs.SSL}/{entity_type}/{entity_id}"
    )
    return response.json()


def get_cert_install_status(cluster, entity_id):
    """Get SSL Storage Status for Cluster ActiveGate"""
    response = rh.make_api_call(
        cluster=cluster,
        endpoint=f"{rh.ClusterAPIs.SSL_STORE}/COLLECTOR/{entity_id}"
    )
    return response.text


def set_cert(cluster, entity_type, entity_id, ssl_json):
    """Set SSL Storage Status for Server or Cluster ActiveGate"""
    response = rh.make_api_call(
        cluster=cluster,
        method=rh.HTTP.POST,
        endpoint=f"{rh.ClusterAPIs.SSL_STORE}/{entity_type}/{entity_id}",
        json=ssl_json
    )
    return response.json()

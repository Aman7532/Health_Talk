#!/usr/bin/env python3
import requests
import json
import time
import sys

# Kibana settings
KIBANA_URL = "http://localhost:30002"
ELASTICSEARCH_URL = "http://localhost:30001"

def wait_for_kibana():
    """Wait for Kibana to be ready"""
    print("Waiting for Kibana to be ready...")
    max_retries = 10
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = requests.get(f"{KIBANA_URL}/app/home")
            if response.status_code == 200:
                print("Kibana is ready!")
                return True
        except Exception as e:
            print(f"Error checking Kibana status: {e}")
        
        retry_count += 1
        print(f"Retrying in 2 seconds... ({retry_count}/{max_retries})")
        time.sleep(2)
    
    print("Timed out waiting for Kibana to be ready")
    return False

def create_advanced_visualizations():
    """Create advanced visualizations for Healthcare Chatbot logs"""
    print("Creating advanced visualizations for Healthcare Chatbot monitoring...")
    
    headers = {
        "Content-Type": "application/json",
        "kbn-xsrf": "true"
    }
    
    # Get the index pattern ID
    try:
        response = requests.get(
            f"{KIBANA_URL}/api/saved_objects/index-pattern/healthcare-chatbot-logs",
            headers=headers
        )
        
        if response.status_code != 200:
            print("Index pattern not found. Please run setup_kibana_dashboard_fixed.py first.")
            return []
        
        index_pattern_id = "healthcare-chatbot-logs"
    except Exception as e:
        print(f"Error getting index pattern: {e}")
        return []
    
    visualizations = []
    
    # Create query type visualization (pie chart)
    query_type_viz = {
        "attributes": {
            "title": "Healthcare Chatbot - Query Types",
            "visState": json.dumps({
                "title": "Healthcare Chatbot - Query Types",
                "type": "pie",
                "params": {
                    "type": "pie",
                    "addTooltip": True,
                    "addLegend": True,
                    "legendPosition": "right",
                    "isDonut": True,
                    "labels": {
                        "show": True,
                        "values": True,
                        "last_level": True,
                        "truncate": 100
                    }
                },
                "aggs": [
                    {
                        "id": "1",
                        "enabled": True,
                        "type": "count",
                        "schema": "metric",
                        "params": {}
                    },
                    {
                        "id": "2",
                        "enabled": True,
                        "type": "terms",
                        "schema": "segment",
                        "params": {
                            "field": "query_type.keyword",
                            "size": 10,
                            "order": "desc",
                            "orderBy": "1"
                        }
                    }
                ]
            }),
            "uiStateJSON": "{}",
            "description": "Distribution of query types in Healthcare Chatbot logs",
            "version": 1,
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps({
                    "index": index_pattern_id,
                    "filter": [],
                    "query": {
                        "query": "",
                        "language": "kuery"
                    }
                })
            }
        }
    }
    
    # Create response time visualization (histogram)
    response_time_viz = {
        "attributes": {
            "title": "Healthcare Chatbot - Response Times",
            "visState": json.dumps({
                "title": "Healthcare Chatbot - Response Times",
                "type": "histogram",
                "params": {
                    "type": "histogram",
                    "grid": {
                        "categoryLines": False
                    },
                    "categoryAxes": [
                        {
                            "id": "CategoryAxis-1",
                            "type": "category",
                            "position": "bottom",
                            "show": True,
                            "scale": {
                                "type": "linear"
                            },
                            "labels": {
                                "show": True,
                                "truncate": 100
                            },
                            "title": {}
                        }
                    ],
                    "valueAxes": [
                        {
                            "id": "ValueAxis-1",
                            "name": "LeftAxis-1",
                            "type": "value",
                            "position": "left",
                            "show": True,
                            "scale": {
                                "type": "linear",
                                "mode": "normal"
                            },
                            "labels": {
                                "show": True,
                                "rotate": 0,
                                "filter": False,
                                "truncate": 100
                            },
                            "title": {
                                "text": "Count"
                            }
                        }
                    ],
                    "seriesParams": [
                        {
                            "show": True,
                            "type": "histogram",
                            "mode": "stacked",
                            "data": {
                                "label": "Count",
                                "id": "1"
                            },
                            "valueAxis": "ValueAxis-1"
                        }
                    ],
                    "addTooltip": True,
                    "addLegend": True,
                    "legendPosition": "right",
                    "times": [],
                    "addTimeMarker": False
                },
                "aggs": [
                    {
                        "id": "1",
                        "enabled": True,
                        "type": "count",
                        "schema": "metric",
                        "params": {}
                    },
                    {
                        "id": "2",
                        "enabled": True,
                        "type": "histogram",
                        "schema": "segment",
                        "params": {
                            "field": "response_time_ms",
                            "interval": 100,
                            "min_doc_count": 1,
                            "extended_bounds": {}
                        }
                    }
                ]
            }),
            "uiStateJSON": "{}",
            "description": "Distribution of response times in Healthcare Chatbot logs",
            "version": 1,
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps({
                    "index": index_pattern_id,
                    "filter": [],
                    "query": {
                        "query": "",
                        "language": "kuery"
                    }
                })
            }
        }
    }
    
    # Create error types visualization (pie chart)
    error_types_viz = {
        "attributes": {
            "title": "Healthcare Chatbot - Error Types",
            "visState": json.dumps({
                "title": "Healthcare Chatbot - Error Types",
                "type": "pie",
                "params": {
                    "type": "pie",
                    "addTooltip": True,
                    "addLegend": True,
                    "legendPosition": "right",
                    "isDonut": False,
                    "labels": {
                        "show": True,
                        "values": True,
                        "last_level": True,
                        "truncate": 100
                    }
                },
                "aggs": [
                    {
                        "id": "1",
                        "enabled": True,
                        "type": "count",
                        "schema": "metric",
                        "params": {}
                    },
                    {
                        "id": "2",
                        "enabled": True,
                        "type": "terms",
                        "schema": "segment",
                        "params": {
                            "field": "error_type.keyword",
                            "size": 10,
                            "order": "desc",
                            "orderBy": "1"
                        }
                    }
                ]
            }),
            "uiStateJSON": "{}",
            "description": "Distribution of error types in Healthcare Chatbot logs",
            "version": 1,
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps({
                    "index": index_pattern_id,
                    "filter": [
                        {
                            "meta": {
                                "index": index_pattern_id,
                                "negate": False,
                                "disabled": False,
                                "alias": None,
                                "type": "phrase",
                                "key": "level.keyword",
                                "value": "ERROR",
                                "params": {
                                    "query": "ERROR"
                                }
                            },
                            "query": {
                                "match": {
                                    "level.keyword": {
                                        "query": "ERROR",
                                        "type": "phrase"
                                    }
                                }
                            },
                            "$state": {
                                "store": "appState"
                            }
                        }
                    ],
                    "query": {
                        "query": "",
                        "language": "kuery"
                    }
                })
            }
        }
    }
    
    # Create and save visualizations
    viz_ids = []
    for viz_id, viz_data in [
        ("healthcare-chatbot-query-types", query_type_viz),
        ("healthcare-chatbot-response-times", response_time_viz),
        ("healthcare-chatbot-error-types", error_types_viz)
    ]:
        try:
            response = requests.post(
                f"{KIBANA_URL}/api/saved_objects/visualization/{viz_id}",
                headers=headers,
                data=json.dumps(viz_data)
            )
            
            if response.status_code in [200, 201]:
                print(f"{viz_id} visualization created successfully!")
                viz_ids.append(viz_id)
            else:
                print(f"Failed to create {viz_id} visualization. Status code: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error creating {viz_id} visualization: {e}")
    
    return viz_ids

def update_dashboard(viz_ids):
    """Update the Healthcare Chatbot dashboard with new visualizations"""
    if not viz_ids:
        print("No visualizations created. Skipping dashboard update.")
        return False
    
    print("Updating Healthcare Chatbot dashboard...")
    
    headers = {
        "Content-Type": "application/json",
        "kbn-xsrf": "true"
    }
    
    # First, get the existing dashboard
    try:
        response = requests.get(
            f"{KIBANA_URL}/api/saved_objects/dashboard/healthcare-chatbot-monitoring",
            headers=headers
        )
        
        if response.status_code != 200:
            print("Dashboard not found. Please run setup_kibana_dashboard_fixed.py first.")
            return False
        
        dashboard_data = response.json()
        
        # Parse the existing panels
        existing_panels = json.loads(dashboard_data["attributes"]["panelsJSON"])
        existing_references = dashboard_data["references"]
        
        # Add new panels for the new visualizations
        panel_index = len(existing_panels)
        for i, viz_id in enumerate(viz_ids):
            panel = {
                "panelIndex": str(panel_index + i + 1),
                "gridData": {
                    "x": (panel_index + i) % 2 * 24,
                    "y": ((panel_index + i) // 2 + 2) * 15,  # Start after existing panels
                    "w": 24,
                    "h": 15,
                    "i": str(panel_index + i + 1)
                },
                "embeddableConfig": {},
                "version": "7.14.0",
                "panelRefName": f"panel_{panel_index + i + 1}"
            }
            existing_panels.append(panel)
            
            reference = {
                "name": f"panel_{panel_index + i + 1}",
                "type": "visualization",
                "id": viz_id
            }
            existing_references.append(reference)
        
        # Update the dashboard
        update_data = {
            "attributes": {
                "title": dashboard_data["attributes"]["title"],
                "hits": dashboard_data["attributes"]["hits"],
                "description": dashboard_data["attributes"]["description"],
                "panelsJSON": json.dumps(existing_panels),
                "optionsJSON": dashboard_data["attributes"]["optionsJSON"],
                "version": dashboard_data["attributes"]["version"],
                "timeRestore": True,
                "timeTo": "now",
                "timeFrom": "now-24h",
                "refreshInterval": {
                    "pause": True,
                    "value": 0
                }
            },
            "references": existing_references
        }
        
        response = requests.put(
            f"{KIBANA_URL}/api/saved_objects/dashboard/healthcare-chatbot-monitoring",
            headers=headers,
            data=json.dumps(update_data)
        )
        
        if response.status_code in [200, 201]:
            print("Dashboard updated successfully!")
            print(f"Access your dashboard at: {KIBANA_URL}/app/kibana#/dashboard/healthcare-chatbot-monitoring")
            return True
        else:
            print(f"Failed to update dashboard. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error updating dashboard: {e}")
        return False

def main():
    """Main function to create advanced visualizations"""
    if not wait_for_kibana():
        print("Kibana is not ready. Please make sure Kibana is running.")
        sys.exit(1)
    
    try:
        viz_ids = create_advanced_visualizations()
        if viz_ids:
            update_dashboard(viz_ids)
            print("\nAdvanced visualizations created successfully!")
            print(f"Access your dashboard at: {KIBANA_URL}/app/dashboards")
        else:
            print("\nFailed to create advanced visualizations.")
    except Exception as e:
        print(f"Error creating advanced visualizations: {e}")

if __name__ == "__main__":
    main()

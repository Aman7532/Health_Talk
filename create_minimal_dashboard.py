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

def create_response_time_visualization():
    """Create response time visualization for Healthcare Chatbot logs"""
    print("Creating response time visualization for Healthcare Chatbot monitoring...")
    
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
            return None
        
        index_pattern_id = "healthcare-chatbot-logs"
    except Exception as e:
        print(f"Error getting index pattern: {e}")
        return None
    
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
    
    # Create the visualization
    viz_id = "healthcare-chatbot-response-times"
    try:
        # First try to delete any existing visualization with the same ID
        requests.delete(
            f"{KIBANA_URL}/api/saved_objects/visualization/{viz_id}",
            headers=headers
        )
        
        # Create the visualization
        response = requests.post(
            f"{KIBANA_URL}/api/saved_objects/visualization/{viz_id}",
            headers=headers,
            data=json.dumps(response_time_viz)
        )
        
        if response.status_code in [200, 201]:
            print(f"{viz_id} visualization created successfully!")
            return viz_id
        else:
            print(f"Failed to create {viz_id} visualization. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error creating {viz_id} visualization: {e}")
        return None

def create_minimal_dashboard(viz_id):
    """Create a minimal dashboard with only the response time visualization"""
    if not viz_id:
        print("No visualization created. Skipping dashboard creation.")
        return False
    
    print("Creating minimal Healthcare Chatbot dashboard...")
    
    headers = {
        "Content-Type": "application/json",
        "kbn-xsrf": "true"
    }
    
    # Create panel for the visualization
    panel = {
        "panelIndex": "1",
        "gridData": {
            "x": 0,
            "y": 0,
            "w": 48,  # Full width
            "h": 20,
            "i": "1"
        },
        "embeddableConfig": {},
        "version": "7.14.0",
        "panelRefName": "panel_1"
    }
    
    # Create reference for the visualization
    reference = {
        "name": "panel_1",
        "type": "visualization",
        "id": viz_id
    }
    
    # Create dashboard data
    dashboard_data = {
        "attributes": {
            "title": "Healthcare Chatbot Response Times",
            "hits": 0,
            "description": "Dashboard for monitoring Healthcare Chatbot response times",
            "panelsJSON": json.dumps([panel]),
            "optionsJSON": json.dumps({
                "useMargins": True,
                "hidePanelTitles": False
            }),
            "version": 1,
            "timeRestore": True,
            "timeTo": "now",
            "timeFrom": "now-24h",
            "refreshInterval": {
                "pause": True,
                "value": 0
            }
        },
        "references": [reference]
    }
    
    # First try to delete any existing dashboard
    try:
        requests.delete(
            f"{KIBANA_URL}/api/saved_objects/dashboard/healthcare-chatbot-minimal",
            headers=headers
        )
    except:
        pass
    
    # Create the dashboard
    try:
        response = requests.post(
            f"{KIBANA_URL}/api/saved_objects/dashboard/healthcare-chatbot-minimal",
            headers=headers,
            data=json.dumps(dashboard_data)
        )
        
        if response.status_code in [200, 201]:
            print("Minimal dashboard created successfully!")
            print(f"Access your dashboard at: {KIBANA_URL}/app/kibana#/dashboard/healthcare-chatbot-minimal")
            return True
        else:
            print(f"Failed to create dashboard. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error creating dashboard: {e}")
        return False

def main():
    """Main function to create a minimal dashboard"""
    if not wait_for_kibana():
        print("Kibana is not ready. Please make sure Kibana is running.")
        sys.exit(1)
    
    try:
        viz_id = create_response_time_visualization()
        if viz_id:
            create_minimal_dashboard(viz_id)
            print("\nMinimal dashboard created successfully!")
            print(f"Access your dashboard at: {KIBANA_URL}/app/dashboards")
        else:
            print("\nFailed to create response time visualization.")
    except Exception as e:
        print(f"Error creating minimal dashboard: {e}")

if __name__ == "__main__":
    main()

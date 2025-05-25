#!/usr/bin/env python3
import requests
import json
import time
import sys
import os

# Kibana settings
KIBANA_URL = os.environ.get("KIBANA_URL", "http://kibana-service:80")
ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL", "http://elasticsearch-service:9200")

def wait_for_kibana():
    """Wait for Kibana to be ready"""
    print("Waiting for Kibana to be ready...")
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = requests.get(f"{KIBANA_URL}/api/status")
            if response.status_code == 200:
                print("Kibana is ready!")
                return True
        except Exception as e:
            pass
            
        retry_count += 1
        print(f"Waiting for Kibana... (attempt {retry_count}/{max_retries})")
        time.sleep(5)
        
    return False

def create_index_pattern():
    """Create index pattern for Healthcare Chatbot logs"""
    print("Creating index pattern for Healthcare Chatbot logs...")
    
    headers = {
        "Content-Type": "application/json",
        "kbn-xsrf": "true"
    }
    
    # Create index pattern for healthcare-chatbot logs
    data = {
        "attributes": {
            "title": "healthcare-chatbot-*",
            "timeFieldName": "timestamp"
        }
    }
    
    try:
        # First check if the index pattern already exists
        response = requests.get(
            f"{KIBANA_URL}/api/saved_objects/index-pattern/healthcare-chatbot-app",
            headers=headers
        )
        
        if response.status_code == 200:
            print("Index pattern already exists!")
            return "healthcare-chatbot-app"
        
        # Create the index pattern if it doesn't exist
        response = requests.post(
            f"{KIBANA_URL}/api/saved_objects/index-pattern/healthcare-chatbot-app",
            headers=headers,
            data=json.dumps(data)
        )
        
        if response.status_code in [200, 201]:
            print("Index pattern created successfully!")
            return "healthcare-chatbot-app"
        else:
            print(f"Failed to create index pattern. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return "healthcare-chatbot-app"
    except Exception as e:
        print(f"Error creating index pattern: {e}")
        return "healthcare-chatbot-app"

def create_visualization(index_pattern_id):
    """Create visualizations for Healthcare Chatbot monitoring"""
    print("Creating visualizations for Healthcare Chatbot monitoring...")
    
    headers = {
        "Content-Type": "application/json",
        "kbn-xsrf": "true"
    }
    
    visualizations = []
    
    # Create common log messages visualization (table)
    common_messages_viz = {
        "attributes": {
            "title": "Common Log Messages",
            "visState": json.dumps({
                "title": "Common Log Messages",
                "type": "table",
                "params": {
                    "perPage": 10,
                    "showPartialRows": False,
                    "showMetricsAtAllLevels": False,
                    "sort": {
                        "columnIndex": None,
                        "direction": None
                    },
                    "showTotal": False,
                    "totalFunc": "sum",
                    "percentageCol": ""
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
                        "schema": "bucket",
                        "params": {
                            "field": "message.keyword",
                            "size": 10,
                            "order": "desc",
                            "orderBy": "1",
                            "otherBucket": False,
                            "otherBucketLabel": "Other",
                            "missingBucket": False,
                            "missingBucketLabel": "Missing"
                        }
                    }
                ]
            }),
            "uiStateJSON": "{\"vis\":{\"params\":{\"sort\":{\"columnIndex\":null,\"direction\":null}}}}",
            "description": "Most common log messages in Healthcare Chatbot logs",
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
    visualizations.append(("healthcare-chatbot-common-messages", common_messages_viz))
    
    # Create execution times visualization (histogram)
    execution_times_viz = {
        "attributes": {
            "title": "Execution Times",
            "visState": json.dumps({
                "title": "Execution Times",
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
                                "filter": True,
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
                            "field": "execution_time",
                            "interval": 0.1,
                            "min_doc_count": 1,
                            "extended_bounds": {}
                        }
                    }
                ]
            }),
            "uiStateJSON": "{}",
            "description": "Distribution of execution times in Healthcare Chatbot logs",
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
    visualizations.append(("healthcare-chatbot-execution-times", execution_times_viz))
    
    # Create and save visualizations
    viz_ids = []
    for viz_id, viz_data in visualizations:
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

def create_dashboard(index_pattern_id, viz_ids):
    """Create dashboard for Healthcare Chatbot monitoring"""
    print("Creating dashboard for Healthcare Chatbot monitoring...")
    
    headers = {
        "Content-Type": "application/json",
        "kbn-xsrf": "true"
    }
    
    # Create panel JSON for each visualization
    panels = []
    for i, viz_id in enumerate(viz_ids):
        panel = {
            "panelIndex": str(i + 1),
            "gridData": {
                "x": (i % 2) * 24,
                "y": (i // 2) * 15,
                "w": 24,
                "h": 15,
                "i": str(i + 1)
            },
            "embeddableConfig": {},
            "version": "7.14.0",
            "panelRefName": f"panel_{i + 1}"
        }
        panels.append(panel)
    
    # Create dashboard references
    references = []
    for i, viz_id in enumerate(viz_ids):
        reference = {
            "name": f"panel_{i + 1}",
            "type": "visualization",
            "id": viz_id
        }
        references.append(reference)
    
    # Create dashboard data
    dashboard_data = {
        "attributes": {
            "title": "Healthcare Chatbot Monitoring",
            "hits": 0,
            "description": "Dashboard for monitoring Healthcare Chatbot logs",
            "panelsJSON": json.dumps(panels),
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
        "references": references
    }
    
    try:
        response = requests.post(
            f"{KIBANA_URL}/api/saved_objects/dashboard/healthcare-chatbot-monitoring",
            headers=headers,
            data=json.dumps(dashboard_data)
        )
        
        if response.status_code in [200, 201]:
            print("Dashboard created successfully!")
            print(f"Access your dashboard at: {KIBANA_URL}/app/kibana#/dashboard/healthcare-chatbot-monitoring")
            return True
        else:
            print(f"Failed to create dashboard. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error creating dashboard: {e}")
        return False

def main():
    """Main function to set up Kibana dashboards"""
    if not wait_for_kibana():
        print("\nKibana is not responding. Please make sure Kibana is running and accessible.")
        sys.exit(1)
    
    try:
        # Try automated setup
        print("\nAttempting automated Kibana setup...")
        index_pattern_id = create_index_pattern()
        
        viz_ids = create_visualization(index_pattern_id)
        if viz_ids:
            create_dashboard(index_pattern_id, viz_ids)
            print("\nKibana setup completed successfully!")
            print(f"Access your dashboard at: {KIBANA_URL}/app/dashboards")
        else:
            print("\nCouldn't create visualizations automatically.")
    except Exception as e:
        print(f"\nError during Kibana setup: {e}")

if __name__ == "__main__":
    main()

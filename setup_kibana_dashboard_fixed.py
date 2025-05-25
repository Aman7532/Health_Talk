#!/usr/bin/env python3
import requests
import json
import time
import sys

# Kibana settings
KIBANA_URL = "http://localhost:30002"  # Using the port-forwarded Kibana service
ELASTICSEARCH_URL = "http://localhost:30001"  # Using the port-forwarded Elasticsearch service

def wait_for_kibana():
    """Wait for Kibana to be ready"""
    print("Waiting for Kibana to be ready...")
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Just check if Kibana is responding to basic requests
            response = requests.get(f"{KIBANA_URL}/app/home")
            if response.status_code == 200:
                print("Kibana is ready!")
                return True
        except Exception as e:
            print(f"Error checking Kibana status: {e}")
        
        retry_count += 1
        print(f"Kibana not ready yet. Retrying in 5 seconds... ({retry_count}/{max_retries})")
        time.sleep(5)
    
    print("Timed out waiting for Kibana to be ready")
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
            "title": "healthcare-chatbot-logs-*",
            "timeFieldName": "@timestamp"
        }
    }
    
    try:
        # First check if the index pattern already exists
        response = requests.get(
            f"{KIBANA_URL}/api/saved_objects/index-pattern/healthcare-chatbot-logs",
            headers=headers
        )
        
        if response.status_code == 200:
            print("Index pattern already exists!")
            return "healthcare-chatbot-logs"
        
        # Create the index pattern if it doesn't exist
        response = requests.post(
            f"{KIBANA_URL}/api/saved_objects/index-pattern/healthcare-chatbot-logs",
            headers=headers,
            data=json.dumps(data)
        )
        
        if response.status_code in [200, 201]:
            print("Index pattern created successfully!")
            return "healthcare-chatbot-logs"
        else:
            print(f"Failed to create index pattern. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return "healthcare-chatbot-logs"
    except Exception as e:
        print(f"Error creating index pattern: {e}")
        return "healthcare-chatbot-logs"

def create_visualizations(index_pattern_id):
    """Create visualizations for Healthcare Chatbot monitoring"""
    print("Creating visualizations for Healthcare Chatbot monitoring...")
    
    headers = {
        "Content-Type": "application/json",
        "kbn-xsrf": "true"
    }
    
    visualizations = []
    
    # Create log levels visualization (pie chart)
    log_levels_viz = {
        "attributes": {
            "title": "Healthcare Chatbot - Log Levels",
            "visState": json.dumps({
                "title": "Healthcare Chatbot - Log Levels",
                "type": "pie",
                "params": {
                    "type": "pie",
                    "addTooltip": True,
                    "addLegend": True,
                    "legendPosition": "right",
                    "isDonut": False
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
                            "field": "level.keyword",
                            "size": 5,
                            "order": "desc",
                            "orderBy": "1"
                        }
                    }
                ]
            }),
            "uiStateJSON": "{}",
            "description": "Distribution of log levels in Healthcare Chatbot logs",
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
    
    # Create log timeline visualization (line chart)
    log_timeline_viz = {
        "attributes": {
            "title": "Healthcare Chatbot - Log Timeline",
            "visState": json.dumps({
                "title": "Healthcare Chatbot - Log Timeline",
                "type": "line",
                "params": {
                    "type": "line",
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
                            "type": "line",
                            "mode": "normal",
                            "data": {
                                "label": "Count",
                                "id": "1"
                            },
                            "valueAxis": "ValueAxis-1",
                            "drawLinesBetweenPoints": True,
                            "lineWidth": 2,
                            "showCircles": True
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
                        "type": "date_histogram",
                        "schema": "segment",
                        "params": {
                            "field": "@timestamp",
                            "timeRange": {
                                "from": "now-24h",
                                "to": "now"
                            },
                            "useNormalizedEsInterval": True,
                            "interval": "auto",
                            "drop_partials": False,
                            "min_doc_count": 1,
                            "extended_bounds": {}
                        }
                    },
                    {
                        "id": "3",
                        "enabled": True,
                        "type": "terms",
                        "schema": "group",
                        "params": {
                            "field": "level.keyword",
                            "orderBy": "1",
                            "order": "desc",
                            "size": 5
                        }
                    }
                ]
            }),
            "uiStateJSON": "{}",
            "description": "Timeline of log events in Healthcare Chatbot",
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
    
    # Create top messages visualization (table)
    top_messages_viz = {
        "attributes": {
            "title": "Healthcare Chatbot - Top Messages",
            "visState": json.dumps({
                "title": "Healthcare Chatbot - Top Messages",
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
                    "totalFunc": "sum"
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
                            "orderBy": "1"
                        }
                    }
                ]
            }),
            "uiStateJSON": json.dumps({
                "vis": {
                    "params": {
                        "sort": {
                            "columnIndex": None,
                            "direction": None
                        }
                    }
                }
            }),
            "description": "Top log messages in Healthcare Chatbot logs",
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
    
    # Create and save visualizations
    viz_ids = []
    for viz_id, viz_data in [
        ("healthcare-chatbot-log-levels", log_levels_viz),
        ("healthcare-chatbot-log-timeline", log_timeline_viz),
        ("healthcare-chatbot-top-messages", top_messages_viz)
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

def print_manual_setup_instructions():
    """Print instructions for manually setting up Kibana"""
    print("\n=== MANUAL KIBANA SETUP INSTRUCTIONS ===")
    print("1. Open Kibana in your browser at http://localhost:30002")
    print("\n2. Create an index pattern:")
    print("   a. Go to Management > Stack Management > Kibana > Index Patterns")
    print("   b. Click 'Create index pattern'")
    print("   c. Enter 'healthcare-chatbot-logs-*' as the index pattern name")
    print("   d. Select '@timestamp' as the Time field")
    print("   e. Click 'Create index pattern'")
    print("\n3. View your logs:")
    print("   a. Go to Analytics > Discover")
    print("   b. Select the 'healthcare-chatbot-logs-*' index pattern")
    print("   c. Adjust the time range in the top right corner to see your logs")
    print("\n4. Create visualizations (optional):")
    print("   a. Go to Analytics > Dashboard")
    print("   b. Click 'Create new dashboard'")
    print("   c. Click 'Create visualization'")
    print("   d. Choose visualization type (e.g., pie chart for log levels, line chart for log timeline)")
    print("   e. Configure your visualization using fields like 'level.keyword' and '@timestamp'")
    print("   f. Save your visualization and add it to the dashboard")
    print("\nYour logs are already in Elasticsearch and can be viewed in Kibana even without creating visualizations.")
    print("The manual setup allows you to explore your logs and create custom visualizations as needed.")
    print("===================================")

def main():
    """Main function to set up Kibana dashboards"""
    if not wait_for_kibana():
        print("\nKibana is not responding. Please make sure Kibana is running and accessible at {KIBANA_URL}.")
        print("You can still set up Kibana manually by following these instructions:")
        print_manual_setup_instructions()
        sys.exit(1)
    
    try:
        # Try automated setup
        print("\nAttempting automated Kibana setup...")
        index_pattern_id = create_index_pattern()
        
        # Even if we can't create visualizations and dashboard automatically,
        # we'll provide manual instructions
        try:
            viz_ids = create_visualizations(index_pattern_id)
            if viz_ids:
                create_dashboard(index_pattern_id, viz_ids)
                print("\nKibana setup completed successfully!")
                print(f"Access your dashboard at: {KIBANA_URL}/app/dashboards")
            else:
                print("\nCouldn't create visualizations automatically. Please follow the manual instructions below.")
                print_manual_setup_instructions()
        except Exception as e:
            print(f"\nError during visualization or dashboard creation: {e}")
            print("Please follow the manual instructions below.")
            print_manual_setup_instructions()
    except Exception as e:
        print(f"\nError during Kibana setup: {e}")
        print("Please follow the manual instructions below.")
        print_manual_setup_instructions()

if __name__ == "__main__":
    main()

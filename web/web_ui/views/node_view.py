# myapp/views.py
import json
from django.shortcuts import render


def flowchart_view(request):
    elements = [
        # Node 1
        {
            "data": {
                "id": "node1",
                "label": "AI Agent",
                "active": "false",
            }
        },
        # Node 2 (marked active)
        {
            "data": {
                "id": "node2",
                "label": "OpenAI Chat Model",
                "active": "true",
            }
        },
        # Node 3
        {
            "data": {
                "id": "node3",
                "label": "SerpAPI",
                "active": "false",
            }
        },
        # Forward edges (class = forwardEdge)
        {
            "data": {
                "id": "edge1",
                "source": "node1",
                "target": "node2",
                "classes": "forwardEdge",
            }
        },
        {
            "data": {
                "id": "edge2",
                "source": "node2",
                "target": "node3",
                "classes": "forwardEdge",
            }
        },
        # "Connection back" from node2 to node1 (class = backwardEdge)
        {
            "data": {
                "id": "edge3",
                "source": "node2",
                "target": "node1",
                "classes": "backwardEdge",
            }
        },
    ]
    return render(request, "web_ui/flowchart.html", {"elements": json.dumps(elements)})

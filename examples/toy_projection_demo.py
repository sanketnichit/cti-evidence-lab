"""Small synthetic demonstration; contains no real CTI data.

Run from the repository root:
    python examples/toy_projection_demo.py
"""

import json

from src.projection_metrics import TemporalEdge, project_report


# Two distinct script executions map to T1059, with a payload download between.
# This is deliberately synthetic and illustrates a possible projection effect;
# it is not an annotation of any real report.
techniques_by_event = {
    "script_execution_1": {"T1059"},
    "payload_download": {"T1105"},
    "script_execution_2": {"T1059"},
}
temporal_edges = [
    TemporalEdge("rel_1", "script_execution_1", "payload_download", "BEFORE"),
    TemporalEdge("rel_2", "payload_download", "script_execution_2", "BEFORE"),
]

result = project_report(techniques_by_event, temporal_edges)
print(json.dumps(result, indent=2))

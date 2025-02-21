import React from "react";
import Graph from "./graph";
import { ReactFlowProvider } from "@xyflow/react";
import '@xyflow/react/dist/base.css';

export default function Dashboard() {
  return (
    <ReactFlowProvider>
      <Graph />
    </ReactFlowProvider>
  );
}

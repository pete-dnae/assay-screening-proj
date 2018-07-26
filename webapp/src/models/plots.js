import Plotly from '@/models/lean_plotly';
import { getTraces } from './plotUtilities';


export const plotCopyCountGraph = (data, element = 'copyCountGraph') =>
  Plotly.newPlot(
    element,
    [
      {
        x: data.x1,
        y: data.y1,
        type: 'Scatter',
        mode: 'markers',
        name: 'Ct values',
      },
      {
        x: data.x1,
        y: data.y2,
        type: 'Scatter',
        name: `eff=${(data.eff !== 'nan') ? data.eff.toFixed(2) : null}`,
      },
    ],
    {
      height: 400,
      width: 600,
      title: 'Ct vs Log Copy Count',
      xAxisTitle: 'Log Copy Count',
      yAxisTitle: 'Ct',
    },
  );

export const plotAmpGraph = (data, element = 'ampGraph') =>
  Plotly.newPlot(element, getTraces(data), {
    showlegend: true,
    legend: {
      x: 1,
      y: 0.5,
    },
    height: 400,
    width: 600,
    title: 'Amplification Data',
    xAxisTitle: 'Cycle',
    yAxisTitle: 'Delta Rn',
    exponent: true,
  });

export const plotMeltGraph = (data, element = 'meltGraph') =>
  Plotly.newPlot(element, getTraces(data), {
    showlegend: true,
    legend: {
      x: 1,
      y: 0.5,
    },
    height: 400,
    width: 600,
    title: 'Temperature Melt Curve Data',
    xAxisTitle: 'Temperature',
    yAxisTitle: 'Melt Derivative',
    exponent: true,
  });

export const plotLabchipGraph = (
  { trace, layout, zoom },
  element = 'labChipGraph',
) => Plotly.newPlot(element, trace, layout, zoom);

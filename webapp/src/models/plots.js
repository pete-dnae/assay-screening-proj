import Plotly from '@/models/lean_plotly';
import _ from 'lodash';
import { getTraceName } from './plotUtilities';

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
        name: `eff=${data.eff.toFixed(2)}`,
      },
    ],
    {
      height: 300,
      width: 500,
      title: 'Ct vs Log Copy Count',
      xAxisTitle: 'Log Copy Count',
      yAxisTitle: 'Ct',
    },
  );

export const plotAmpGraph = (data, element = 'ampGraph') =>
  Plotly.newPlot(
    element,
    _.map(data, row => ({
      x: row.x,
      y: row.y,
      name: getTraceName(row),
    })),
    {
      height: 300,
      width: 500,
      title: 'Amplification Data',
      xAxisTitle: 'Cycle',
      yAxisTitle: 'Delta Rn',
      exponent: true,
    },
  );

export const plotMeltGraph = (data, element = 'meltGraph') =>
  Plotly.newPlot(
    element,
    _.map(data, row => ({
      x: row.x,
      y: row.y,
      name: getTraceName(row),
    })),
    {
      height: 300,
      width: 500,
      title: 'Temperature Melt Curve Data',
      xAxisTitle: 'Temperature',
      yAxisTitle: 'Melt Derivative',
      exponent: true,
    },
  );

export const plotLabchipGraph = ({ trace, layout }, element = 'labChipGraph') =>
  Plotly.newPlot(element, trace, layout);
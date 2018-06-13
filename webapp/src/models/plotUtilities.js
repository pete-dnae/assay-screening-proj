import _ from 'lodash';

export const COLORS = {
  template: {
    10: '#b30000',
    100: '#41b5f4',
    1000: 'Orange',
    10000: '#069906',
  },
  NTC: { default: 'Grey' },
  human: { 50: 'Purple', 500: '#e542f4' },
};

export const getColorName = (type, conc) => {
  const randomColor = () =>
    `#${Math.floor(Math.random() * 16777215).toString(16)}`;
  if (conc in COLORS[type]) {
    return COLORS[type][conc];
  }
  if (type === 'human') {
    return COLORS[type][500];
  }
  if (type === 'template') {
    if (conc >= 5000) return COLORS[type][10000];
    if (conc >= 500) return COLORS[type][1000];
    if (conc >= 50) return COLORS[type][100];
    if (conc >= 5) return '#0000A0';
    if (conc <= 5000) return COLORS[type][10];
  }
  return randomColor();
};

export const getTraceDetails = (data) => {
  let name = '';

  let color = '';
  let lineFormat = '';
  if ('templates' in data.meta) {
    name = data.meta.templates[0].concentration + data.meta.templates[0].unit;
    color = getColorName('template', data.meta.templates[0].concentration);
    lineFormat = 'Solid';
  }
  if ('humans' in data.meta) {
    name += data.meta.humans[0].concentration + data.meta.humans[0].unit;
    color = getColorName('human', data.meta.humans[0].concentration);
    lineFormat = 'dashdot';
  }
  if ('transferred_templates' in data.meta) {
    name += `PA${data.meta.transferred_templates[0].concentration} ${
      data.meta.transferred_templates[0].unit
    } `;
    color = getColorName(
      'template',
      data.meta.transferred_templates[0].concentration,
    );
    lineFormat = 'Solid';
  }
  if ('transferred_humans' in data.meta) {
    name += `PA${data.meta.transferred_humans[0].concentration} ${
      data.meta.transferred_humans[0].unit
    } `;
    color = getColorName(
      'human',
      data.meta.transferred_humans[0].concentration,
    );
    lineFormat = 'dashdot';
  }
  if (!name) {
    name = 'NTC';
    lineFormat = 'dashdot';
    color = getColorName('NTC', 'default');
  }

  name = `${data.meta.well_id} ${name}`;

  return { name, lineFormat, color };
};

export const getLabChipCartesianCoords = obj =>
  _.reduce(
    obj,
    (acc, grp) => {
      acc.x = [...acc.x, ...Array(grp.length).fill(acc.i)];
      acc.y = [...acc.y, ...grp.map(x => x.bp)];
      acc.text = [...acc.text, ...grp.map(x => Math.round(x.conc * 100) / 100)];
      acc.i += 1;
      return acc;
    },
    {
      x: [],
      y: [],
      text: [],
      textposition: 'top',
      mode: 'text',
      i: 1,
    },
  );

export const getLabChipGraphOpacity = arr =>
  _.map(arr, x => (x > 50 ? 1.0 : x / 50));

export const getLabChipGraphShapes = (args, obj) =>
  _.map(obj.x, (x, i) => {
    const color = `rgba(1, 1, 1,${args[i]})`;
    const log10 = 10 ** Math.log10(obj.y[i] + 1);
    const delta = 0.2 * log10;
    const border = obj.y[i] > 0 ? 'rgba(1, 1, 1, .2)' : 'rgba(1, 1, 1, 0)';
    return {
      type: 'rect',
      x0: obj.x[i] - 0.4,
      y0: obj.y[i] - delta,
      x1: obj.x[i] + 0.4,
      y1: obj.y[i],
      line: {
        color: border,
      },
      fillcolor: color,
    };
  });

export const getLabChipGraphText = obj => _.map(obj, val => `${val[0].sample}`);

export const getLabChipGraphLayout = (args) => {
  const { tickText, shapes } = args;
  return {
    title: 'LabChip Peaks',
    hovermode: 'closest',
    xaxis: {
      showgrid: false,
      title: 'Sample',
      tickvals: _.range(1, tickText.length + 1),
      ticktext: tickText,
    },
    yaxis: { range: [1, 4], title: 'Length(bp)', type: 'log' },
    height: 300,
    width: 500,
    shapes,
  };
};

export const generateLabChipPlotTraces = (wellData) => {
  const wellList = _.reduce(
    wellData,
    (acc, val, wellId) => {
      acc[wellId] = _.reduce(
        val.peak,
        (a, v, i) => {
          if (i !== 'LM' && i !== 'UM') {
            a.push({
              'LC Well': wellId,
              bp: v['size_[bp]'],
              conc: v['conc_(ng/ul)'],
              sample: getTraceDetails(v).name,
            });
          } else {
            a.push({
              'LC Well': wellId,
              bp: null,
              conc: null,
              sample: getTraceDetails(v).name,
            });
          }

          return a;
        },
        [],
      );
      return acc;
    },
    {},
  );
  const labChipCartesianCoords = getLabChipCartesianCoords(wellList);
  const opacity = getLabChipGraphOpacity(labChipCartesianCoords.text);
  const shapes = getLabChipGraphShapes(opacity, labChipCartesianCoords);
  const tickText = getLabChipGraphText(wellList);
  const layoutConfig = getLabChipGraphLayout({
    tickText,
    shapes,
  });

  return {
    trace: [labChipCartesianCoords],
    layout: layoutConfig,
    zoom: { scrollZoom: true },
  };
};


export const getTraces = data =>
  _.map(data, (row) => {
    const { name, lineFormat, color } = getTraceDetails(row);
    return {
      x: row.x,
      y: row.y,
      name,
      line: {
        dash: lineFormat,
        width: name.indexOf('PA') > -1 ? 1 : 2,
      },
      marker: {
        color,
      },
    };
  });

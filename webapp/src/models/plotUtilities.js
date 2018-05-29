import _ from 'lodash';

export const getTraceName = (data) => {
  let name = '';
  if ('templates' in data.meta) {
    name = data.meta.templates[0].concentration + data.meta.templates[0].unit;
  }
  if ('humans' in data.meta) {
    name += data.meta.humans[0].concentration + data.meta.humans[0].unit;
  }
  if ('transferred_templates' in data.meta) {
    name = `PA${data.meta.transferred_templates[0].concentration}${
      data.meta.transferred_templates[0].unit
    }`;
  }
  if ('transferred_humane' in data.meta) {
    name += `PA${data.meta.transferred_humane[0].concentration}${
      data.meta.transferred_humane[0].unit
    }`;
  }
  if (!name) name = 'NTC';
  name = `${data.meta.well_id} ${name}`;

  return name;
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
    const delta = 0.2 * Math.pow(10, Math.log10(obj.y[i] + 1));
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

export const getLabChipGraphText = obj => _.map(obj, (val, i) => `${i}`);

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
    height: 500,
    width: 750,
    shapes,
  };
};

export const generateLabChipPlotTraces = (wellData) => {
  const wellList = _.reduce(
    wellData,
    (acc, val, wellId) => {
      acc[wellId] = _.reduce(
        val.peak,
        (a, v) => {
          a.push({
            'LC Well': wellId,
            bp: v['size_[bp]'],
            conc: v['conc_(ng/ul)'],
          });
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

  return { trace: [labChipCartesianCoords], layout: layoutConfig };
};

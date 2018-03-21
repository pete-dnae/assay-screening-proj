import _ from 'lodash';
import { splitLine } from '@/models/editor2.0';
// stuff about painting tables goes here
export const formatText = (text) => {
  let finalText = '';
  const lines = text.split('\n');
  const wordPositions = { 0: [], 1: [], 2: [], 3: [], 4: [], 5: [] };
  lines.forEach((x) => {
    x.split(/\s+/).forEach((txt, i) => {
      if (i < 5) {
        wordPositions[i].push(txt);
      }
    });
  });

  const maxLength = _.reduce(
    wordPositions,
    (acc, x, i) => {
      if (!_.isEmpty(x)) {
        //eslint-disable-next-line
        const longWord = _.maxBy(x, (a) => a.length);

        acc[i] = longWord.length;
      }

      return acc;
    },
    {},
  );

  lines.forEach((x) => {
    let finalLine = '';
    x.split(/\s+/).forEach((txt, i) => {
      const fillSpace = _.repeat(' ', maxLength[i] - txt.length);
      finalLine += `${txt} ${fillSpace}`;
    });
    finalText += `${finalLine.trimRight()}\n`;
  });
  return finalText;
};
export const getRowList = (rows) => {
  if (rows.indexOf('-') > -1) {
    return _.range(rows[0].charCodeAt(0), rows[2].charCodeAt(0) + 1).map(
      //eslint-disable-next-line
      (x) => x - 64,
    );
  }
  //eslint-disable-next-line
  return rows
    .split(',')
    .map((x) => x.charCodeAt(0) - 64)
    .sort((a, b) => a - b);
};
export const getColList = (cols) => {
  const rangeCharIndex = cols.indexOf('-');
  if (rangeCharIndex > -1) {
    return _.range(
      parseInt(cols.substr(0, rangeCharIndex), 0),
      parseInt(cols.substr(rangeCharIndex + 1, cols.length), 0) + 1,
    );
  }
  //eslint-disable-next-line
  return cols
    .split(',')
    .map((x) => parseInt(x, 0))
    .sort((a, b) => a - b);
};

export const makeSVG = (DOMURL, html) => {
  const data =
    `${'<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="1200">' +
      '<foreignObject width="2000" height="1200">' +
      '<div xmlns="http://www.w3.org/1999/xhtml" style="font-size:35px">'}${html}</div>` +
    '</foreignObject>' +
    '</svg>';
  return DOMURL.createObjectURL(
    new Blob([data], {
      type: 'image/svg+xml',
    }),
  );
};
export const isItemInArray = (array, item) => {
  for (let i = 0; i < array.length; i += 1) {
    if (array[i][0] === item[0] && array[i][1] === item[1]) {
      return true;
    }
  }
  return false;
};
export const dispatchClick = (elem, rowCol) => {
  const event = new CustomEvent('cellClick', { detail: rowCol });
  elem.dispatchEvent(event);
};
export const paintTable = (tableBoundaries, allocationMapping) => {
  const [maxRow, maxCol] = tableBoundaries;
  let tableBody = {};
  _.range(1, maxRow + 1).forEach((row, i) => {
    tableBody[i] = tableBody[i] ? tableBody[i] : [];
    _.range(1, maxCol + 1).forEach((col, j) => {
      if (isItemInArray(allocationMapping, [row, col])) {
        const td = document.createElement('td');
        td.setAttribute('border', '1px solid black');
        td.setAttribute('background', 'rgba(76, 175, 80, 0.2)');
        td.addEventListener('click', dispatchClick(td, [row, col]));
        tableBody[i][j] = td;
      } else {
        tableBody[i][j] = tableBody[i][j] ? tableBody[i][j] : null;
      }
    });
  });

  tableBody = _.reduce(
    tableBody,
    (acc, row) => {
      const mapFill = row.map((x) => {
        if (!x) {
          const tabled = document.createElement('td');
          tabled.setAttribute('border', '1px solid black');
          return td;
        }
        return x;
      });
      debugger;
      //eslint-disable-next-line
      acc.appendChild(
        mapFill.reduce((a, x, i) => {
          a.appendChild(x);
          return a;
        }, document.createElement('table')),
      );
      return acc;
    },
    document.createElement('table'),
  );
  tableBody.setAttribute('max-width', '100%');
  tableBody.setAttribute('height', 'auto');
  return tableBody;
};

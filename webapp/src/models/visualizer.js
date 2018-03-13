import _ from 'lodash';
import { splitLine, validateRule } from '@/models/editor2.0';
// stuff about painting tables goes here
export const formatText = (text) => {
  var finalText = '';
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
        let longWord = _.maxBy(x, (a) => a.length);

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
      (x) => x - 65,
    );
  }
  return rows.split(',').map((x) => x.charCodeAt(0) - 65);
};
export const getColList = (cols) => {
  const rangeCharIndex = cols.indexOf('-');
  if (rangeCharIndex > -1) {
    return _.range(
      parseInt(cols.substr(0, rangeCharIndex), 0) - 1,
      parseInt(cols.substr(rangeCharIndex + 1, cols.length), 0),
    );
  }
  return cols.split(',').map((x) => parseInt(x, 0) - 1);
};

export const makeSVG = (DOMURL, html) => {
  const data =
    `${'<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="1200">' +
      '<foreignObject width="2000" height="1200">' +
      '<div xmlns="http://www.w3.org/1999/xhtml" style="font-size:15px">'}${html}</div>` +
    '</foreignObject>' +
    '</svg>';
  return DOMURL.createObjectURL(
    new Blob([data], {
      type: 'image/svg+xml',
    }),
  );
};

export const paintTable = (DOMURL, tableSpec, startIndex, text) => {
  let tableBody = {};
  text.split('\n').forEach((line) => {
    const fields = splitLine(line);
    validateRule(startIndex, fields, text);
    const rows = getRowList(fields[3][0]);
    const cols = getColList(fields[2][0]);
    _.range(tableSpec.rows).forEach((row, i) => {
      tableBody[i] = tableBody[i] ? tableBody[i] : [];
      _.range(1, tableSpec.cols + 1).forEach((col, j) => {
        if (rows.indexOf(i) !== -1 && cols.indexOf(j) !== -1) {
          tableBody[i][j] =
            '<td style="width:250px;border: 1px solid black;background: rgba(76, 175, 80, 0.2)"></td>';
        } else {
          tableBody[i][j] = tableBody[i][j] ? tableBody[i][j] : null;
        }
      });
    });
  });

  tableBody = _.reduce(
    tableBody,
    (acc, row) => {
      let mapFill = row.map((x) => {
        if (!x) {
          return '<td style="width:250px;border: 1px solid black"></td>';
        }
        return x;
      });
      acc += `<tr style="height:100px">${mapFill.join('')}</tr>`;
      return acc;
    },
    '<table>',
  );
  tableBody += '</table>';
  return makeSVG(DOMURL, tableBody);
};

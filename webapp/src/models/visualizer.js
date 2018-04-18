import _ from 'lodash';

// stuff about painting tables goes here
export const formatText = (text) => {
  let finalText = '';
  const lines = text.split('\n');
  const wordPositions = { 0: [], 1: [], 2: [], 3: [], 4: [], 5: [] };
  lines.forEach((x) => {
    if (!x.startsWith('#')) {
      x.split(/\s+/).forEach((txt, i) => {
        if (i < 5) {
          wordPositions[i].push(txt);
        }
      });
    }
  });

  const maxLength = _.reduce(
    wordPositions,
    (acc, x, i) => {
      if (!_.isEmpty(x)) {
        //eslint-disable-next-line
        const longWord = _.maxBy(x, a => a.length);

        acc[i] = longWord.length;
      }

      return acc;
    },
    {},
  );

  lines.forEach((x) => {
    let finalLine = '';
    if (x.startsWith('A') || x.startsWith('V') || x.startsWith('P')) {
      x.split(/\s+/).forEach((txt, i) => {
        const fillSpace = _.repeat(' ', maxLength[i] - txt.length);
        finalLine += `${txt} ${fillSpace}`;
      });
      finalText += `${finalLine.trimRight()}\n`;
    } else if (x.startsWith('#')) {
      finalText += `${x.trimRight()}\n`;
    } else if (x.startsWith('T')) {
      const fields = x.split(/\s+/);
      if (fields.length === 8) {
        finalLine += `${fields[0]} ${_.repeat(
          ' ',
          maxLength[0] - fields[0].length,
        )}${fields.slice(1, 4).join(' ')} ${_.repeat(
          ' ',
          maxLength[1] - fields.slice(1, 4).join(' ').length,
        )}${fields[4]} ${_.repeat(' ', maxLength[2] - fields[4].length)}${
          fields[5]
        } ${_.repeat(' ', maxLength[3] - fields[5].length)}${
          fields[6]
        } ${_.repeat(' ', maxLength[4] - fields[6].length)}${
          fields[7]
        } ${_.repeat(' ', maxLength[5] - fields[7].length)}`;
        finalText += `${finalLine.trimRight()}\n`;
      } else {
        finalText += `${x.trimRight()}\n`;
      }
    } else if (x.startsWith('C')) {
      const fields = x.split(/\s+/);
      if (fields.length === 4) {
        const spaceBeforeCycle = maxLength[1] + maxLength[2] + maxLength[3] + 2;
        finalLine += `${fields[0]} ${_.repeat(
          ' ',
          maxLength[0] - fields[0].length,
        )}${fields[1]} ${_.repeat(' ', spaceBeforeCycle - fields[1].length)}${
          fields[2]
        } ${_.repeat(' ', maxLength[4] - fields[2].length)}${fields[3]}`;

        finalText += `${finalLine.trimRight()}\n`;
      } else {
        finalText += `${x.trimRight()}\n`;
      }
    }
  });
  return finalText;
};
export const getRowList = (rows) => {
  if (rows.indexOf('-') > -1) {
    return _.range(rows[0].charCodeAt(0), rows[2].charCodeAt(0) + 1).map(
      //eslint-disable-next-line
      x => x - 64
    );
  }

  return (
    rows
      .split(',')
      //eslint-disable-next-line
      .map(x => x.charCodeAt(0) - 64)
      .sort((a, b) => a - b)
  );
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
  return (
    cols
      .split(',')
      //eslint-disable-next-line
      .map(x => parseInt(x, 0))
      .sort((a, b) => a - b)
  );
};

export const makeSVG = (DOMURL, html) => {
  const data =
    `${'<svg xmlns="http://www.w3.org/2000/svg" width="2800" height="2800">' +
      '<foreignObject width="2800" height="2800">' +
      '<div xmlns="http://www.w3.org/1999/xhtml" style="font-size:15px">'}${html}</div>` +
    '</foreignObject>' +
    '</svg>';
  return DOMURL.createObjectURL(
    new Blob([data], {
      type: 'image/svg+xml',
    }),
  );
};
export const isItemInArray = (array, item) => {
  //eslint-disable-next-line
  const arrayString = _.map(array, x => String(x));

  return arrayString.includes(String(item));
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
      if (allocationMapping && isItemInArray(allocationMapping, [row, col])) {
        const td = document.createElement('td');
        td.setAttribute('style', 'border:1px solid black;');
        td.setAttribute('style', 'background:rgba(76, 175, 80, 0.2);');
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
          const td = document.createElement('td');
          td.setAttribute('style', 'border:1px solid black;');
          return td;
        }
        return x;
      });

      acc.appendChild(
        mapFill.reduce((a, x) => {
          a.appendChild(x);
          return a;
        }, document.createElement('tr')),
      );
      return acc;
    },
    document.createElement('table'),
  );
  tableBody.setAttribute('max-width', '100%');
  tableBody.setAttribute('height', 'auto');
  return tableBody;
};

export const getReagentAllocationDict = (allocationMapping, plateName) => {
  const plateAllocation = allocationMapping[plateName];
  const rowLength = Object.keys(plateAllocation)
    ? Object.keys(plateAllocation).length
    : null;
  const colLength = _.reduce(
    plateAllocation,
    (acc, row) => {
      const colPerRow = Object.keys(row).length;
      if (colPerRow > acc) {
        acc = colPerRow;
      }
      return acc;
    },
    0,
  );
  const reagentAllocationDict = {};
  _.range(1, rowLength + 1).forEach((rowNum) => {
    _.range(1, colLength + 1).forEach((colNum) => {
      if (plateAllocation[rowNum][colNum]) {
        const reagentList = plateAllocation[rowNum][colNum].reduce(
          (acc, reagentEntity) => {
            acc.push(reagentEntity[0]);
            return acc;
          },
          [],
        );
        reagentList.forEach((reagent) => {
          if (reagentAllocationDict[reagent]) {
            reagentAllocationDict[reagent].push([rowNum, colNum]);
          } else {
            reagentAllocationDict[reagent] = [[rowNum, colNum]];
          }
        });
      }
    });
  });
  return reagentAllocationDict;
};

import _ from 'lodash';

export const zoomIn = (event) => {
  const element = document.getElementById('overlay');

  element.style.display = 'inline-block';
  const img = document.getElementById('imgZoom');
  let posX = event.offsetX ? event.offsetX : event.pageX - img.offsetLeft;
  let posY = event.offsetY ? event.offsetY : event.pageY - img.offsetTop;
  posX = -(posX * 5) + 50;
  posY = -(posY * 4) + 50;
  element.style.backgroundPosition = `${posX}px ${posY}px`;
};
export const zoomOut = () => {
  const element = document.getElementById('overlay');
  element.style.display = 'none';
};

export const getNewIndex = (arg, items) => {
  const newIndex =
    items.length !== 0 ? _.maxBy(items, (x) => x[arg])[arg] + 1 : 0;
  return newIndex;
};

export const prepareResultsTable = (allocationResults, currentSelection) => {
  let tableBody = '<table class="table">';
  allocationResults.forEach((row, i) => {
    tableBody += '<tr style="height:100px">';
    row.forEach((col, j) => {
      if (currentSelection) {
        if (
          currentSelection.rows.indexOf(String.fromCharCode(i + 65)) !== -1 &&
          currentSelection.cols.indexOf(j) !== -1
        ) {
          tableBody +=
            '<td style="width:250px;border: 1px solid black;background: rgba(76, 175, 80, 0.2)">';
        } else {
          tableBody += '<td style="width:250px;border: 1px solid black">';
        }
      } else {
        tableBody += '<td style="width:250px;border: 1px solid black">';
      }

      tableBody += col['ID Primers']
        ? `<div  class="row"><span style="color:red">${
            col['ID Primers']
          }</span></div>`
        : '';
      tableBody += col['PA Primers']
        ? `<div class="row"><span style="color:blue">${
            col['PA Primers']
          }</span></div>`
        : '';
      tableBody += col.Strain
        ? `<div class="row"><span style="color:brown">${
            col.Strain
          }</span></div>`
        : '';
      tableBody += col['Strain Count']
        ? `<div  class="row"><span style="color:green">${
            col['Strain Count']
          }cp</span></div>`
        : '';
      tableBody += col['Dilution Factor']
        ? `<div  class="row"><span>${'Dil '}${
            col['Dilution Factor']
          }</span></div>`
        : '';
      tableBody += col.HgDNA
        ? `<div  class="row"><span style="color:purple">${'HgDNA '}${
            col.HgDNA
          }</span></div>`
        : '';

      tableBody += '</td>';
    });
    tableBody += '</tr>';
  });
  tableBody += '</table>';
  return tableBody;
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

export const genCharArray = (start, end) => {
  const result = [];
  const i = start.charCodeAt(0);
  const j = end.charCodeAt(0) + 1;
  _.range(i, j).forEach((x) => {
    result.push(String.fromCharCode(x));
  });
  return result;
};

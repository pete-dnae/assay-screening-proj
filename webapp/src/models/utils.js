import _ from 'lodash';

export const zoomIn = (event) => {
  const element = document.getElementById('overlay');

  element.style.display = 'inline-block';
  const img = document.getElementById('imgZoom');
  let posX = event.offsetX ? event.offsetX : event.pageX - img.offsetLeft;
  let posY = event.offsetY ? event.offsetY : event.pageY - img.offsetTop;
  posX = (-posX * 3.5) + 10;
  posY = (-posY * 2.5) + 10;
  element.style.backgroundPosition = `${posX}px ${posY}px`;
};
export const zoomOut = () => {
  const element = document.getElementById('overlay');
  element.style.display = 'none';
};

export const getNewIndex = (arg, items) => {
  const newIndex = items.length !== 0 ? _.maxBy(items, x => x[arg])[arg] + 1 : 0;
  return newIndex;
};

export const prepareResultsTable = (allocationResults) => {
  let tableBody = '<table class="table">';
  allocationResults.forEach((row) => {
    tableBody += '<tr style="height:100px">';
    row.forEach((col) => {
      tableBody += '<td style="width:250px;border: 1px solid black">';
      tableBody += `<div  class="row"><span style="color:red">${col['ID Primers']}</span></div>`;
      tableBody += `<div class="row"><span style="color:blue">${col['PA Primers']}</span></div>`;
      tableBody += `<div  class="row"><span style="color:green">${
        col['Strain Count']
      }cp</span></div>`;
      if (col['Dilution Factor'] !== '') {
        tableBody += `<div  class="row"><span>${'Dil '}${col['Dilution Factor']}</span></div>`;
      }

      tableBody += '</td>';
    });
    tableBody += '</tr>';
  });
  tableBody += '</table>';
  return tableBody;
};

export const makeSVG = (DOMURL, html) => {
  const data =
    `${'<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="850">' +
      '<foreignObject width="1400" height="850">' +
      '<div xmlns="http://www.w3.org/1999/xhtml" style="font-size:10px">'}${html}</div>` +
    '</foreignObject>' +
    '</svg>';
  return DOMURL.createObjectURL(new Blob([data], { type: 'image/svg+xml' }));
};

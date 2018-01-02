import _ from 'lodash';

export const isConcentrationValid = (repeats, value) =>
  !_.isEmpty(value) && value.split(',').length <= repeats;

export const fillMissingValues = (byBlock, blockNo, blocks, cols, repeats, data) => {
  let restructuredData;
  if (byBlock) {
    debugger;
    restructuredData = cols.map((x, i) => (Math.floor(i / repeats) + 1 == blockNo ? data[0] : ''));
  } else {
    restructuredData =
      Object.values(data).length !== repeats
        ? Object.values(data).concat(_.times(repeats - Object.values(data).length, () => ''))
        : Object.values(data);
  }

  return restructuredData;
};

export const getDataByBlock = (byBlock, blocks, rows, dataVals) => {
  if (byBlock) {
    return rows.reduce((acc, x) => {
      acc[x] = dataVals;
      return acc;
    }, {});
  }
  return rows.reduce((acc, x) => {
    acc[x] = _.times(blocks, () => dataVals).reduce((a, el) => {
      a = a.concat(el);
      return a;
    }, []);
    return acc;
  }, {});
};

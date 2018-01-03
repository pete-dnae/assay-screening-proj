import _ from 'lodash';

export const isConcentrationValid = (repeats, value) =>
  !_.isEmpty(value) && value.split(',').length <= repeats;

export const getRepeatedDataByColumn = (repeats, blocks, data) => {
  const restructuredData =
    data.length !== repeats
      ? _.times(blocks, () => data.concat(_.times(repeats - data.length, () => ''))).reduce(
          (a, el) => {
            // eslint-disable-next-line
            a = a.concat(el);
            return a;
          },
          [],
        )
      : _.times(blocks, () => data).reduce((a, el) => {
          // eslint-disable-next-line
          a = a.concat(el);
        return a;
      }, []);

  return restructuredData;
};

export const getitemsByColDict = (repeats, cols, repeatedDataByColumn, dataByBlock) => {
  const itemsByColDict = dataByBlock.reduce(
    (a, el) => {
      _.range((el.blockNo - 1) * repeats, el.blockNo * repeats).forEach((number) => {
        a[number] = el.Strain;
      });
      return a;
    },
    cols.reduce((acc, x) => {
      acc[x] = null;
      return acc;
    }, {}),
  );
  return _.reduce(
    itemsByColDict,
    (acc, x, i) => {
      if (!x) {
        acc[i] = repeatedDataByColumn.shift();
      }
      return acc;
    },
    itemsByColDict,
  );
};

import store from '@/store';
import _ from 'lodash';

export const postRuleScript = (text, callBack) => {
  store.dispatch('saveToDb', { text }).then(() => callBack());
};

export const findSuggestions = (value, data) => {
  if (!_.find(data, element => element === value)) {
    return data.filter(element => element.indexOf(value) !== -1);
  }
  return null;
};

export const getMaxRowCol = (lnums) => {
  const allCells = _.reduce(
    lnums,
    (acc, x) => {
      Object.assign(acc, acc.concat(x));
      return acc;
    },
    [],
  );

  return [
    allCells.sort((a, b) => b[1] - a[1])[0][1],
    allCells.sort((a, b) => b[0] - a[0])[0][0],
  ];
};
export const getMaxRowColPlate = allocationInstructions =>
  _.reduce(allocationInstructions, (acc, plateInfo, plateName) => {
    const keys = Object.keys(plateInfo);
    const colCount = keys ? keys.length : 0;
    const rowCount = Math.max(
      ..._.map(plateInfo, (row) => {
        const rowKeys = Object.keys(row);
        return rowKeys ? rowKeys.length : 0;
      }),
    );
    acc[plateName] = {
      rowCount,
      colCount,
    };
    return acc;
  }, {});
export const splitLine = (text) => {
  const re = /\S+/g;
  const fields = [];
  let match;
  //eslint-disable-next-line
  while ((match = re.exec(text))) {
    fields.push(match);
  }
  return fields;
};

//eslint-disable-next-line
export const removeAdditionalNewLine = currentText => currentText.slice(0, -1);

export const getCurrentLineFields = (currentText, cursorPosition) => {
  let plateName;
  const textTillCursor = removeAdditionalNewLine(currentText).substr(
    0,
    cursorPosition,
  );
  const currentLineStart = textTillCursor.lastIndexOf('\n');
  const currentLineLength =
    currentText.substr(currentLineStart + 1, currentText.length).indexOf('\n') +
    1;
  const lineNumber = (textTillCursor.match(/\n/g) || []).length + 1;
  textTillCursor.split('\n').forEach((line) => {
    if (line.startsWith('P')) {
      [, plateName] = line.split(/\s+/g);
    }
  });

  const fields = splitLine(
    currentText.substr(currentLineStart, currentLineLength),
  );
  return { currentLineStart, currentLineLength, lineNumber, plateName, fields };
};

export const hesitationTimer = _.debounce(postRuleScript, 500);
